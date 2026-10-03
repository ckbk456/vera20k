use super::*;
use serde_json::Value;

fn coord(v: &Value) -> ProjectileCoord {
    ProjectileCoord::new(
        v[0].as_i64().unwrap() as i32,
        v[1].as_i64().unwrap() as i32,
        v[2].as_i64().unwrap() as i32,
    )
}

#[test]
fn native_line_trail_ring_fades_on_each_composite_and_detaches_before_retirement() {
    let fixture: Value = serde_json::from_str(include_str!(
        "../../../tools/projectile_oracle/line_trail.json"
    ))
    .unwrap();
    for row in fixture["rows"].as_array().unwrap() {
        let initial = &row["initial"]["trail"];
        let color = std::array::from_fn(|i| initial["rgb"][i].as_u64().unwrap() as u8);
        let mut runtime = LineTrails::default();
        runtime.attach(7, color, 16, row["detail"].as_i64().unwrap() as i32);
        let mut last = ProjectileCoord::new(256, 256, 0);
        for step in row["steps"].as_array().unwrap() {
            let visit = step["visit"].as_u64().unwrap() as i32;
            if visit <= 36 {
                last = ProjectileCoord::new(
                    256 + 16 * visit,
                    256,
                    if visit % 2 == 1 { 104 } else { 0 },
                );
            }
            if visit == 40 {
                runtime.detach(7);
            }
            runtime.advance_legacy_composite(|_| Some(last));
            assert_eq!(
                runtime.trails.len(),
                step["registry_count"].as_u64().unwrap() as usize,
                "detail={}, visit={visit}",
                row["detail"]
            );
            if let Some(trail) = runtime.trails.first() {
                let native = &step["trail"];
                assert_eq!(trail.head, native["head"].as_u64().unwrap() as usize);
                assert_eq!(
                    trail.decrement,
                    native["decrement"].as_i64().unwrap() as i32
                );
                for (actual, native) in trail.samples.iter().zip(native["ring"].as_array().unwrap())
                {
                    assert_eq!(actual.coord, coord(&native["xyz"]), "visit={visit}");
                    assert_eq!(
                        actual.strength,
                        native["strength"].as_i64().unwrap() as i32,
                        "visit={visit}"
                    );
                }
            }
            let native_draws = step["calls"]
                .as_array()
                .unwrap()
                .iter()
                .filter(|c| c["address"] == "0x4beac0")
                .count();
            assert_eq!(runtime.segments.len(), native_draws, "visit={visit}");
        }
    }
}

#[test]
fn native_line_trail_save_load_drops_ring_and_does_not_reconstruct_from_live_owner() {
    let fixture: Value = serde_json::from_str(include_str!(
        "../../../tools/projectile_oracle/line_trail.json"
    ))
    .unwrap();
    for row in fixture["persistence"].as_array().unwrap() {
        assert_eq!(row["loaded_trail_pointer"], 0);
        assert_eq!(row["postload_registry_count"], 0);
        let mut runtime = LineTrails::default();
        runtime.attach(7, [216, 216, 255], 16, 2);
        runtime.advance_legacy_composite(|_| Some(ProjectileCoord::new(256, 256, 0)));
        runtime.clear_on_load();
        assert!(
            runtime
                .advance_legacy_composite(|_| Some(ProjectileCoord::new(384, 256, 104)))
                .is_empty()
        );
        assert!(runtime.trails.is_empty());
    }
}

#[test]
fn native_line_trail_registry_emits_reverse_attached_order() {
    let fixture: Value = serde_json::from_str(include_str!(
        "../../../tools/projectile_oracle/line_trail.json"
    ))
    .unwrap();
    for row in fixture["ordered_pixel_cases"].as_array().unwrap() {
        let input = &row["input"];
        let origin = coord(&input["origin"]);
        let delta = coord(&input["delta"]);
        let mut runtime = LineTrails::default();
        for (index, color) in input["colors"].as_array().unwrap().iter().enumerate() {
            runtime.attach(
                index as u64,
                std::array::from_fn(|i| color[i].as_u64().unwrap() as u8),
                16,
                2,
            );
        }
        assert!(
            runtime
                .advance_legacy_composite(|_| Some(origin))
                .is_empty()
        );
        let actual = runtime.advance_legacy_composite(|_| {
            Some(ProjectileCoord::new(
                origin.x + delta.x,
                origin.y + delta.y,
                origin.z + delta.z,
            ))
        });
        let expected = row["draw_calls"].as_array().unwrap();
        assert_eq!(actual.len(), expected.len());
        for (actual, expected) in actual.iter().zip(expected) {
            assert_eq!(
                actual.color,
                std::array::from_fn(|i| expected["rgb"][i].as_u64().unwrap() as u8)
            );
            assert_eq!(
                actual.strength,
                expected["intensity"].as_i64().unwrap() as i32
            );
        }
    }
}

#[test]
fn authenticated_caller_admissions_retain_history_across_display_schedules() {
    let corpus: Value = serde_json::from_str(include_str!(
        "../../../tools/projectile_oracle/line_trail_steam_cadence.json"
    ))
    .unwrap();
    for displays in [0, 1, 7, 240] {
        for case in corpus["cases"].as_array().unwrap() {
            let mut runtime = LineTrails::default();
            let initial = &case["initial"]["trail"];
            runtime.attach(
                7,
                std::array::from_fn(|i| initial["rgb"][i].as_u64().unwrap() as u8),
                initial["decrement"].as_i64().unwrap() as i32,
                2,
            );
            let mut xyz = coord(&corpus["supplied_initial_state"]["owner_xyz"]);
            for step in case["steps"].as_array().unwrap() {
                if step["input"]["entry"] == "detach" {
                    runtime.detach(7);
                }
                let samples = step["output"]["events"]
                    .as_array()
                    .unwrap()
                    .iter()
                    .filter(|event| event["call"] == "trail_sample")
                    .count();
                for _ in 0..samples {
                    runtime.advance_legacy_composite(|_| Some(xyz));
                }
                let native = &step["output"]["ring"];
                assert_eq!(
                    runtime.trails.len(),
                    native["registry_count"].as_u64().unwrap() as usize,
                    "{}: {}",
                    case["input"]["name"],
                    step["input"]
                );
                if let Some(actual) = runtime.trails.first() {
                    assert_eq!(
                        actual.head,
                        native["trail"]["head"].as_u64().unwrap() as usize
                    );
                    for (actual, native) in actual
                        .samples
                        .iter()
                        .zip(native["trail"]["ring"].as_array().unwrap())
                    {
                        assert_eq!(actual.coord, coord(&native["xyz"]));
                        assert_eq!(actual.strength, native["strength"].as_i64().unwrap() as i32);
                    }
                    let retained = actual.samples;
                    for index in 0..displays {
                        // Production display lowering can reproject camera/shroud
                        // every frame; it only receives this immutable segment slice.
                        for segment in runtime.segments() {
                            let _ = segment.project([index, -index]);
                        }
                        assert_eq!(runtime.trails[0].samples, retained);
                    }
                }
                if step["input"]["xyz"].is_array() {
                    xyz = coord(&step["input"]["xyz"]);
                }
            }
        }
    }
}

#[test]
fn production_display_submission_cannot_advance_projectile_history() {
    let render = include_str!("render/mod.rs");
    assert!(!render.contains("line_trails.composite("));
    assert!(!render.contains("advance_legacy_composite("));
    assert!(render.contains("legacy_composite.line_segments()"));
    let runtime = include_str!("../match_runtime/sim_tick.rs");
    let admitted = &runtime[runtime.find("if decision.run_sim {").unwrap()..];
    assert!(
        admitted
            .find("advance_projectile_legacy_composite(state)")
            .unwrap()
            < admitted.find("advance_one_simulation_frame(state").unwrap()
    );
}
