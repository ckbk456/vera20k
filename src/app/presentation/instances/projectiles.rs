//! Retained Bullet rendering: original Object5F4B10 -> Bullet468090.
//! Coordinates, lifetime and Display order stay with the simulation; this
//! read-only adapter resolves the current bridge surface and emits draw pieces.

use super::helpers::projection_admitted;
use crate::app::AppState;
use crate::app::presentation::render::draw_plan_lowering::{
    NativeDisplayOrder, ObjectPieceInstance, ObjectTexture, PlannedObjectInstance,
};
use crate::map::resolved_terrain::ResolvedTerrainGrid;
use crate::render::batch::{DepthAxis, SpriteInstance};
use crate::render::palette_light::PaletteLight;
use crate::render::sprite_atlas::SpriteAtlas;
use crate::render::tactical_draw_plan::{ObjectDraw, RenderZPolicy, SpriteEncoding};
use crate::render::terrain_draw::TerrainPiece;
use crate::rules::projectile_type::ProjectileType;
use crate::sim::projectile::{Projectile, ProjectileCoord, projectile_shp_frame};
use crate::util::lepton::{absolute_leptons_to_screen, ground_height_leptons};
use crate::util::native_x87::adjust_for_z_standard;

#[derive(Debug, Clone, Copy, PartialEq)]
struct BulletPieceGeometry {
    point: [f32; 2],
    z_adjust: i32,
}

#[derive(Debug, Clone, Copy, PartialEq)]
struct BulletGeometry {
    body: BulletPieceGeometry,
    shadow: Option<BulletPieceGeometry>,
}

/// Full original draw-call arguments are pinned in bridge_render.json.
/// Raw Z is in leptons, and OnBridge is independent of structural Cell flags.
fn geometry(
    coord: ProjectileCoord,
    ground_z: i32,
    structural: bool,
    on_bridge: bool,
    shadow: bool,
) -> BulletGeometry {
    let (x, y) = absolute_leptons_to_screen(coord.x, coord.y, coord.z);
    let body = BulletPieceGeometry {
        point: [x, y],
        z_adjust: (-30i32).wrapping_sub(adjust_for_z_standard(coord.z)),
    };
    let mut height = coord.z.wrapping_sub(ground_z).wrapping_sub(if on_bridge {
        crate::util::lepton::BRIDGE_DECK_HEIGHT_LEPTONS
    } else {
        0
    });
    let mut surface_z = ground_z;
    if !on_bridge && structural && height >= crate::util::lepton::BRIDGE_DECK_HEIGHT_LEPTONS {
        height = height.wrapping_sub(crate::util::lepton::BRIDGE_DECK_HEIGHT_LEPTONS);
        surface_z = surface_z.wrapping_add(crate::util::lepton::BRIDGE_DECK_HEIGHT_LEPTONS);
    }
    let shadow = (shadow && height > 0).then(|| BulletPieceGeometry {
        point: [x, y + adjust_for_z_standard(height) as f32],
        z_adjust: (-10i32).wrapping_sub(adjust_for_z_standard(surface_z)),
    });
    BulletGeometry { body, shadow }
}

/// Cell578080 arithmetic without its shared dummy-coordinate write. Rendering
/// must not change a retained DummyCell target or future gameplay/RNG state.
fn ground_probe(terrain: &ResolvedTerrainGrid, coord: ProjectileCoord) -> (i32, bool) {
    let cell = super::foot_depth::depth_cell(
        terrain,
        None,
        None,
        [(coord.x / 256) as i16, (coord.y / 256) as i16],
    );
    let ground = ground_height_leptons(cell.level as u8, cell.ramp, coord.x, coord.y)
        .expect("Bullet draw requires a supported native Cell slope");
    (ground, cell.flags & 0x100 != 0)
}

/// Immutable draw inputs captured at the same pre-Logic Tactical composite as
/// LineTrail556D40. No simulation, atlas or camera state is duplicated here.
struct ProjectileDrawRecord {
    parent: ObjectDraw,
    type_id: String,
    frame: u16,
    geometry: BulletGeometry,
    depth_row: f32,
}

#[derive(Default)]
pub(crate) struct ProjectileDraws {
    records: Vec<ProjectileDrawRecord>,
}

impl ProjectileDraws {
    pub(crate) fn clear(&mut self) {
        self.records.clear();
    }

    pub(crate) fn capture(
        &mut self,
        sim: &crate::sim::world::Simulation,
        rules: &crate::rules::ruleset::RuleSet,
        order: &NativeDisplayOrder,
    ) {
        self.records.clear();
        let Some(terrain) = sim.resolved_terrain.as_ref() else {
            return;
        };
        for (_, projectile) in sim.projectiles.iter() {
            let Some(type_id) = rules
                .weapon(sim.interner.resolve(projectile.payload.weapon))
                .and_then(|weapon| weapon.projectile.as_deref())
            else {
                continue;
            };
            let Some(kind) = rules.projectile(type_id) else {
                continue;
            };
            if let Some(record) = capture_projectile_draw(projectile, kind, type_id, terrain, order)
            {
                self.records.push(record);
            }
        }
    }
}

/// Main55D8F2 precedes Logic55DC9E. Modal display suffix683F66 also admits one
/// Tactical visit; offline modal pump623120 admits none. Actual caller controls:
/// tools/projectile_oracle/line_trail_steam_cadence.json. Publish body and trail
/// together before Logic can construct, move or physically remove a Bullet.
pub(crate) fn advance_projectile_legacy_composite(state: &mut AppState) {
    let Some(runtime) = state.match_state.sim_runtime.as_ref() else {
        return;
    };
    let sim = &runtime.simulation;
    let presentation = &mut state.match_state.match_presentation;
    presentation
        .legacy_composite
        .advance(sim, &runtime.resources.rules);
}

pub(crate) fn seed_legacy_composite_for_timeline(state: &mut AppState) {
    let presentation = &mut state.match_state.match_presentation;
    if let Some(runtime) = state.match_state.sim_runtime.as_ref() {
        presentation
            .legacy_composite
            .seed(&runtime.simulation, &runtime.resources.rules);
    } else {
        presentation.legacy_composite.clear();
    }
}

pub(crate) fn build_projectile_visual_instances(
    state: &AppState,
    objects: &mut Vec<PlannedObjectInstance>,
) {
    let (Some(rt), Some(atlas)) = (
        state.match_state.sim_runtime.as_ref(),
        state.match_state.match_presentation.sprite_atlas.as_ref(),
    ) else {
        return;
    };
    let rules = &rt.resources.rules;
    let input = &state.match_state.input;
    let (_, _, width, height) = crate::app::input::camera::tactical_viewport_px(state);
    let width = width as f32 / input.zoom_level;
    let height = height as f32 / input.zoom_level;
    let axis = super::helpers::depth_axis(state);
    for record in &state
        .match_state
        .match_presentation
        .legacy_composite
        .projectile_draws()
        .records
    {
        let Some(kind) = rules.projectile(&record.type_id) else {
            continue;
        };
        if let Some(object) = lower_projectile_draw(
            record,
            kind,
            atlas,
            [input.camera_x, input.camera_y],
            [width, height],
            axis,
        ) {
            objects.push(object);
        }
    }
}

/// Native comparison adapter uses the production capture and lowering owners.
/// Retained Display membership is admission; storage alone never draws a Bullet.
#[cfg(test)]
#[allow(clippy::too_many_arguments)]
pub(crate) fn projectile_draw_instance(
    projectile: &Projectile,
    kind: &ProjectileType,
    type_id: &str,
    atlas: &SpriteAtlas,
    terrain: &ResolvedTerrainGrid,
    camera: [f32; 2],
    viewport: [f32; 2],
    axis: DepthAxis,
    order: &NativeDisplayOrder,
) -> Option<PlannedObjectInstance> {
    let record = capture_projectile_draw(projectile, kind, type_id, terrain, order)?;
    lower_projectile_draw(&record, kind, atlas, camera, viewport, axis)
}

fn capture_projectile_draw(
    projectile: &Projectile,
    kind: &ProjectileType,
    type_id: &str,
    terrain: &ResolvedTerrainGrid,
    order: &NativeDisplayOrder,
) -> Option<ProjectileDrawRecord> {
    let parent = order.object_draw(projectile.id, SpriteEncoding::Plain)?;
    if kind.inviso || kind.voxel {
        return None;
    }
    let frame = u16::from(projectile_shp_frame(projectile, kind));
    let (ground_z, structural) = ground_probe(terrain, projectile.position);
    let geometry = geometry(
        projectile.position,
        ground_z,
        structural,
        projectile.on_bridge,
        kind.shadow,
    );
    Some(ProjectileDrawRecord {
        parent,
        type_id: type_id.to_owned(),
        frame,
        geometry,
        depth_row: geometry.body.point[1] + adjust_for_z_standard(projectile.position.z) as f32,
    })
}

fn lower_projectile_draw(
    record: &ProjectileDrawRecord,
    kind: &ProjectileType,
    atlas: &SpriteAtlas,
    camera: [f32; 2],
    viewport: [f32; 2],
    axis: DepthAxis,
) -> Option<PlannedObjectInstance> {
    let entry = atlas.projectile_sprite(&record.type_id, kind, record.frame, None)?;
    let geometry = record.geometry;
    // Object6D2140's padded projection admission precedes the shape clip.
    if !projection_admitted(geometry.body.point, camera, viewport) {
        return None;
    }
    let depth =
        crate::render::native_z::depth_for_row(record.depth_row, axis.origin_y, axis.world_height);
    let mut pieces = Vec::with_capacity(2);
    for (piece, geometry) in geometry
        .shadow
        .map(|shadow| (TerrainPiece::Shadow, shadow))
        .into_iter()
        .chain(std::iter::once((TerrainPiece::Body, geometry.body)))
    {
        pieces.push(ObjectPieceInstance {
            target: ObjectTexture::ProjectileShp(entry.page as usize, piece),
            render_z: RenderZPolicy::ReadOnly,
            instance: SpriteInstance {
                position: [
                    geometry.point[0] + entry.offset_x,
                    geometry.point[1] + entry.offset_y,
                ],
                size: entry.pixel_size,
                uv_origin: entry.uv_origin,
                uv_size: entry.uv_size,
                depth,
                tint: crate::map::lighting::DEFAULT_TINT,
                palette_light: PaletteLight::plain(53, 1000),
                alpha: 1.0,
                z_adjust: geometry.z_adjust as f32,
                z_gradient: 0,
                ..Default::default()
            },
        });
    }
    Some(PlannedObjectInstance::object(record.parent, pieces))
}

#[cfg(test)]
#[path = "projectile_render_tests.rs"]
mod native_tests;

#[cfg(test)]
#[path = "projectile_flight_tests.rs"]
mod flight_tests;

#[cfg(test)]
#[path = "projectile_cadence_tests.rs"]
mod cadence_tests;

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn projectile_bridge_height_matches_original_object_projection() {
        // Original5F4B10 ->6D2140: native(-300,315), VERA world row bias15.
        // This regression first failed on the old production builder: Y494.
        let actual = geometry(
            ProjectileCoord::new(2688, 5248, 1040),
            624,
            true,
            false,
            true,
        );
        assert_eq!(actual.body.point, [-300.0, 330.0]);
        assert_eq!(actual.body.z_adjust, -180);
        assert!(actual.shadow.is_none());
    }
}
