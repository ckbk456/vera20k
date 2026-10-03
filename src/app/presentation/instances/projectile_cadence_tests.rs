//! Joined pre-Logic presentation controls. Coordinates/clock/admissions are
//! executed Steam caller outputs; movement and physical removal are prepared
//! lifecycle inputs, not a second physics or impact implementation.
use super::*;
use crate::app::presentation::state::LegacyComposite;
use crate::rules::{art_data::ArtRegistry, ruleset::RuleSet};
use crate::sim::projectile::{
    ProjectileCollisionPolicy, ProjectilePayload, ProjectileSpawn, ProjectileTarget,
    ProjectileTrajectory, ProjectileVelocity, ProjectileVisualState, TargetExpiryPolicy,
};
use crate::sim::world::Simulation;
use serde_json::Value;

fn coord(value: &Value) -> ProjectileCoord {
    ProjectileCoord::new(
        value[0].as_i64().unwrap() as i32,
        value[1].as_i64().unwrap() as i32,
        value[2].as_i64().unwrap() as i32,
    )
}

fn retail_rules() -> Option<RuleSet> {
    let (rules_ini, art_ini) = crate::rules::retail_ini_fixture::retail_rules_and_art()?;
    let mut rules = RuleSet::from_ini_with_fixed_art_for_test(&rules_ini, &art_ini).unwrap();
    rules.install_art_data(ArtRegistry::from_ini(&art_ini));
    Some(rules)
}

fn prepared_sim() -> Simulation {
    let mut sim = Simulation::with_seed(31);
    let mut terrain = crate::map::resolved_terrain::test_flat_ground_grid(32);
    terrain.test_set_native_allocated_cells(&[(1, 1), (2, 1), (3, 1)]);
    sim.install_resolved_terrain_for_new_map(terrain);
    sim
}

fn spawn_dragon(sim: &mut Simulation, rules: &RuleSet, origin: ProjectileCoord) -> u64 {
    let weapon = rules.weapon("HoverMissile").unwrap();
    let kind = rules
        .projectile(weapon.projectile.as_deref().unwrap())
        .unwrap();
    let weapon_id = sim.interner.intern(&weapon.id);
    let warhead = sim.interner.intern(weapon.warhead.as_deref().unwrap());
    let id = sim.allocate_stable_id();
    sim.admit_projectile(
        id,
        ProjectileSpawn {
            native_unique_id: 0,
            line_trail: None,
            flat: kind.flat,
            source_id: 0,
            origin,
            target: ProjectileTarget::None,
            initial_target_position: origin,
            payload: ProjectilePayload::new(weapon.damage, warhead, weapon_id),
            speed_leptons_per_frame: 0,
            velocity: ProjectileVelocity::new(0, 0, 0),
            trajectory: ProjectileTrajectory::Straight,
            guidance: None,
            visual: ProjectileVisualState::new(
                kind.anim_low as u8,
                kind.anim_high as u8,
                kind.anim_rate as u8,
            ),
            arm_frames: 0,
            fuse_frames: None,
            ranged_fuse: false,
            tracks_target: false,
            target_expiry: TargetExpiryPolicy::Expire,
            collision: ProjectileCollisionPolicy::NONE,
        },
    );
    id
}

#[test]
fn dragon_body_and_trail_publish_same_native_pre_logic_phase_and_lifetime() {
    let Some(rules) = retail_rules() else { return };
    let weapon = rules.weapon("HoverMissile").unwrap();
    let kind = rules
        .projectile(weapon.projectile.as_deref().unwrap())
        .unwrap();
    assert_eq!(kind.image.as_deref(), Some("DRAGON"));
    let corpus: Value = serde_json::from_str(include_str!(
        "../../../../tools/projectile_oracle/line_trail_steam_cadence.json"
    ))
    .unwrap();
    for case in corpus["cases"].as_array().unwrap() {
        let mut sim = prepared_sim();
        let id = spawn_dragon(
            &mut sim,
            &rules,
            coord(&corpus["supplied_initial_state"]["owner_xyz"]),
        );
        let mut composite = LegacyComposite::default();
        composite.seed(&sim, &rules);
        composite.attach_line_trail(id, [216, 216, 255], 16, 2);
        for step in case["steps"].as_array().unwrap() {
            if step["input"]["entry"] == "detach" {
                // The existing ifv_trail_impact corpus establishes physical
                // destruction's ObjectDtor→556B30 producer; this controls its
                // already-delivered presentation transaction.
                sim.projectiles.remove(id).unwrap();
                composite.detach_line_trail(id);
            }
            for sample in step["output"]["events"]
                .as_array()
                .unwrap()
                .iter()
                .filter(|event| event["call"] == "trail_sample")
            {
                let before = sim.state_hash();
                let rng = sim.rng_state();
                composite.advance(&sim, &rules);
                assert_eq!(sim.state_hash(), before, "capture changed simulation");
                assert_eq!(sim.rng_state(), rng, "capture consumed gameplay RNG");
                if sim.projectiles.get(id).is_some() {
                    let record = &composite.projectile_draws().records[0];
                    let native_xyz = coord(&sample["owner_xyz"]);
                    let (x, y) =
                        absolute_leptons_to_screen(native_xyz.x, native_xyz.y, native_xyz.z);
                    assert_eq!(record.geometry.body.point, [x, y]);
                    assert_eq!(record.parent.id, id);
                    assert_eq!(
                        record.parent,
                        NativeDisplayOrder::from_display(sim.display_layers())
                            .object_draw(id, SpriteEncoding::Plain)
                            .unwrap()
                    );
                    assert_eq!(
                        record.frame,
                        u16::from(projectile_shp_frame(sim.projectiles.get(id).unwrap(), kind))
                    );
                } else {
                    assert!(composite.projectile_draws().records.is_empty());
                }
            }
            let retained: Vec<_> = composite
                .projectile_draws()
                .records
                .iter()
                .map(|r| (r.parent, r.frame, r.geometry, r.depth_row))
                .collect();
            if step["input"]["xyz"].is_array() {
                sim.projectiles.get_mut(id).unwrap().position = coord(&step["input"]["xyz"]);
            }
            // Post-Logic changes or physical detach cannot rewrite the already
            // published body/membership until another legacy composite.
            for _ in 0..240 {
                assert_eq!(
                    composite
                        .projectile_draws()
                        .records
                        .iter()
                        .map(|r| (r.parent, r.frame, r.geometry, r.depth_row))
                        .collect::<Vec<_>>(),
                    retained
                );
                let _ = composite.line_segments();
            }
        }
        composite.clear();
        assert!(composite.projectile_draws().records.is_empty());
        assert!(composite.line_segments().is_empty());
    }
}

#[test]
fn review_regression_peer_removal_preserves_one_pre_logic_parent_order() {
    use crate::app::presentation::render::draw_plan_lowering::lower_object_instances;
    let Some(rules) = retail_rules() else { return };
    let mut sim = prepared_sim();
    // Prepared Air membership A/B/C. The C draw piece represents the unit
    // family's earlier emission; texture/class must never replace Display rank.
    let a = spawn_dragon(&mut sim, &rules, ProjectileCoord::new(256, 256, 0));
    let b = spawn_dragon(&mut sim, &rules, ProjectileCoord::new(256, 256, 0));
    let c = spawn_dragon(&mut sim, &rules, ProjectileCoord::new(256, 256, 0));
    let mut composite = LegacyComposite::default();
    composite.seed(&sim, &rules);
    let old_order = composite.display_order();
    let bullet = composite
        .projectile_draws()
        .records
        .iter()
        .find(|r| r.parent.id == b)
        .unwrap()
        .parent;
    sim.unregister_non_entity_object(a);
    sim.projectiles.remove(a).unwrap();
    let d = spawn_dragon(&mut sim, &rules, ProjectileCoord::new(256, 256, 0));
    // This is the same shared Arc read by build_world_instances for every peer
    // family. No post-Logic lookup is rebuilt by the display consumer.
    let peers = composite.display_order();
    assert!(std::sync::Arc::ptr_eq(&old_order, &peers));
    assert!(peers.object_draw(d, SpriteEncoding::Plain).is_none());
    let peer_parent = peers.object_draw(c, SpriteEncoding::Plain).unwrap();
    assert_eq!(bullet.display_order, 1);
    assert_eq!(peer_parent.display_order, 2);
    assert_eq!(
        NativeDisplayOrder::from_display(sim.display_layers())
            .object_draw(c, SpriteEncoding::Plain)
            .unwrap()
            .display_order,
        1
    );
    let piece = |target| ObjectPieceInstance {
        target,
        render_z: RenderZPolicy::ReadOnly,
        instance: SpriteInstance::default(),
    };
    let passes = lower_object_instances(vec![
        PlannedObjectInstance::object(peer_parent, vec![piece(ObjectTexture::UnitAtlasPage(0))]),
        PlannedObjectInstance::object(
            bullet,
            vec![piece(ObjectTexture::ProjectileShp(0, TerrainPiece::Body))],
        ),
    ]);
    assert_eq!(
        passes[3].owners,
        [b, c],
        "ReadOnly peers must preserve native B-before-C"
    );
    composite.advance(&sim, &rules);
    let next = composite.display_order();
    assert!(!std::sync::Arc::ptr_eq(&old_order, &next));
    assert_eq!(
        next.object_draw(b, SpriteEncoding::Plain)
            .unwrap()
            .display_order,
        0
    );
    assert!(next.object_draw(d, SpriteEncoding::Plain).is_some());
    assert_eq!(
        old_order
            .object_draw(b, SpriteEncoding::Plain)
            .unwrap()
            .display_order,
        1
    );
}

#[test]
fn review_regression_joint_clear_and_zero_step_restore_seed_preserve_owner_contract() {
    let Some(rules) = retail_rules() else { return };
    let mut sim = prepared_sim();
    let id = spawn_dragon(&mut sim, &rules, ProjectileCoord::new(256, 256, 0));
    let mut composite = LegacyComposite::default();
    let state = sim.state_hash();
    composite.seed(&sim, &rules);
    assert_eq!(sim.state_hash(), state);
    assert_eq!(
        composite.projectile_draws().records.len(),
        1,
        "zero-step body survives initial/load display"
    );
    assert!(
        composite.line_segments().is_empty(),
        "seed never admits a trail visit"
    );
    composite.attach_line_trail(id, [216, 216, 255], 16, 2);
    composite.advance(&sim, &rules);
    sim.projectiles.get_mut(id).unwrap().position = ProjectileCoord::new(512, 256, 0);
    composite.advance(&sim, &rules);
    assert!(!composite.line_segments().is_empty());
    assert!(
        composite
            .display_order()
            .object_draw(id, SpriteEncoding::Plain)
            .is_some()
    );
    composite.clear();
    assert!(composite.line_segments().is_empty());
    assert!(composite.projectile_draws().records.is_empty());
    assert!(
        composite
            .display_order()
            .object_draw(id, SpriteEncoding::Plain)
            .is_none()
    );
    // Paused restore/new map seed shares that same clear transaction. It
    // restores body/order immediately and cannot reconstruct an old ring.
    composite.seed(&sim, &rules);
    assert_eq!(composite.projectile_draws().records.len(), 1);
    assert!(composite.line_segments().is_empty());
    assert_eq!(
        composite
            .display_order()
            .object_draw(id, SpriteEncoding::Plain),
        NativeDisplayOrder::from_display(sim.display_layers())
            .object_draw(id, SpriteEncoding::Plain)
    );
    composite.advance(&sim, &rules);
    assert!(
        composite.line_segments().is_empty(),
        "live body does not reattach loaded trail history"
    );
}
