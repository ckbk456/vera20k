//! Event-loop runtime services, independent of ordinary surface redraws.
//!
//! One opportunity admits at most one frame through the existing pacer/runtime.
//! Surface stalls can still delay this single-thread owner; worker execution is
//! a separate lifecycle mechanism. Native composite updates remain draw-owned.

use std::time::{Duration, Instant};

use super::{ActiveEventLoop, App, AppState, ControlFlow, GameScreen, sim_tick};

/// Exact diagnostics own their gameplay steps; their render prelude only pumps
/// existing audio/exit services. Shell diagnostics retain ordinary admission.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub(super) enum RuntimeServicePass {
    Ordinary,
    ExactCapture,
}

/// Maximum app service wake latency, not a claimed native gameplay cadence.
const SERVICE_WAKE_BOUND: Duration = Duration::from_millis(16);

impl App {
    /// Return false after requesting process exit, so callers stop their pass.
    pub(super) fn pump_runtime_services(
        state: &mut AppState,
        event_loop: &ActiveEventLoop,
        pass: RuntimeServicePass,
    ) -> bool {
        // Startup chrome owns its minimum visible interval. The former render
        // prelude did not service audio or gameplay before that interval ended.
        if state
            .frontend
            .startup_splash
            .as_ref()
            .is_some_and(|splash| splash.is_active(Instant::now()))
        {
            return true;
        }
        // HouseClass keeps simulating for SavourDelay, then blocks on the
        // current outcome Vox before it raises the victory/defeat exit global.
        // Drive that gate before deciding whether another sim frame is legal.
        let scenario_now_ms =
            crate::app::match_runtime::sim_tick::monotonic_frame_pacer_ms(state, Instant::now());
        Self::consume_executed_abort_exit(state, scenario_now_ms);
        crate::app::match_runtime::sim_tick::drive_local_player_outcome_voice_wait(
            state,
            scenario_now_ms,
        );

        // The native victory/defeat handlers synchronously finish their audio
        // teardown before entering the score dialog. Drive the equivalent
        // sequence before either another sim frame or the destination screen.
        Self::drive_scenario_exit(state, scenario_now_ms);

        // Drive the graceful quit cascade (started on Exit-confirm OK). Compute the
        // voice poll before borrowing the cascade mutably to avoid aliasing.
        if state.frontend.quit_cascade.is_some() {
            let now = Instant::now();
            let voices_active = state
                .audio
                .sfx_player
                .as_ref()
                .is_some_and(|sfx| sfx.voices_active());
            let tick = state
                .frontend
                .quit_cascade
                .as_mut()
                .expect("cascade present")
                .tick(now, voices_active);
            if let (Some(vol), Some(player)) =
                (tick.music_volume, state.audio.music_player.as_mut())
            {
                player.set_volume(vol);
            }
            if tick.stop_music {
                state.audio.stop_theme();
            }
            if tick.finished {
                state.frontend.quit_cascade = None;
                event_loop.exit();
                return false;
            }
        }

        // The audio service pass. gamemd drives `AudioSystem::Pump @
        // 0x00406F70` from `Network_ServiceLoop @ 0x0048D080`, which the main
        // tick, the frame throttler, the modal dialog pump, the shell dialog
        // loop and the loading screens all reach — so the sound arbiter, the
        // EVA queue and `ThemeClass::AI` keep being serviced on the main menu,
        // behind a pause or an open menu, and while the window is not the
        // foreground. It therefore sits here, outside every screen and
        // simulation gate, and carries its own `> 33 ms` rate limit.
        crate::app::match_runtime::sim_tick::pump_audio_service(state, scenario_now_ms);

        // Deactivated windows do not simulate. gamemd parks its main tick in a
        // sleep-and-network-only loop while the app is not the foreground, so
        // the world is exactly where the player left it on Alt+Tab return. The
        // gate sits at the call site, not inside the runtime, so a focus edge
        // never re-anchors the frame pacer on its own.
        if pass == RuntimeServicePass::Ordinary
            && matches!(state.frontend.screen, GameScreen::InGame)
            && state.platform.window_active
            && state.match_state.scenario_exit.is_none()
            && state.match_state.scenario_outcome.is_none()
        {
            let now = Instant::now();
            let now_ms = sim_tick::monotonic_frame_pacer_ms(state, now);
            sim_tick::advance_in_game_runtime(state, now_ms);
            // EventClass EXIT is dispatched at the simulation tail. Consume
            // its terminal edge before any outcome route can claim teardown.
            Self::consume_executed_abort_exit(state, now_ms);
            // The SavourDelay expiry is decided in the late house rung of this
            // exact frame. Anchor its 0x78-bucket wall wait to the same observed
            // wall time instead of delaying it to the next render pass.
            crate::app::match_runtime::sim_tick::drive_local_player_outcome_voice_wait(
                state, now_ms,
            );
            Self::drive_scenario_exit(state, now_ms);
        }

        true
    }

    pub(super) fn runtime_service_delay(state: &AppState, now: Instant) -> Duration {
        if state.frontend.screen != GameScreen::InGame
            || !state.platform.window_active
            || state.match_state.paused()
            || !state.match_state.startup.admits_ordinary_tick()
            || state.match_state.sim_runtime.is_none()
            || state.match_state.scenario_exit.is_some()
            || state.match_state.scenario_outcome.is_some()
            || state
                .frontend
                .startup_splash
                .as_ref()
                .is_some_and(|splash| splash.is_active(now))
        {
            return SERVICE_WAKE_BOUND;
        }
        let game_speed = state.match_state.sim_runtime.as_ref().map_or_else(
            || {
                state
                    .match_state
                    .match_presentation
                    .in_game_options
                    .game_speed
                    .min(6) as u8
            },
            |runtime| {
                runtime
                    .simulation
                    .session
                    .game_options
                    .game_speed
                    .clamp(0, 6) as u8
            },
        );
        state
            .platform
            .frame_pacer
            .poll_delay(sim_tick::monotonic_frame_pacer_ms(state, now), game_speed)
            .min(SERVICE_WAKE_BOUND)
    }
}

/// Scheduling decisions remain independent: a hidden or poisoned surface can
/// suppress drawing but cannot suppress audio/exit or gameplay opportunities.
pub(super) struct RuntimeWake {
    pub(super) control_flow: ControlFlow,
    pub(super) request_redraw: bool,
}

pub(super) fn plan_runtime_wake(
    now: Instant,
    service_delay: Duration,
    window_hidden: bool,
    surface_poisoned: bool,
    surface_deadline: Option<Instant>,
    scroll_deadline: Option<Instant>,
) -> RuntimeWake {
    let display_allowed = !window_hidden && !surface_poisoned;
    let display_deadline = surface_deadline
        .map(|deadline| scroll_deadline.map_or(deadline, |scroll| deadline.min(scroll)));
    let request_redraw = display_allowed && display_deadline.is_none_or(|deadline| now >= deadline);
    let mut deadline = now + service_delay;
    for next in [display_deadline, scroll_deadline].into_iter().flatten() {
        if next > now {
            deadline = deadline.min(next);
        }
    }
    RuntimeWake {
        control_flow: if service_delay.is_zero() {
            ControlFlow::Poll
        } else {
            ControlFlow::WaitUntil(deadline)
        },
        request_redraw,
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn hidden_or_poisoned_surface_keeps_service_timer_without_redraw() {
        let now = Instant::now();
        for (hidden, poisoned) in [(true, false), (false, true), (true, true)] {
            let wake = plan_runtime_wake(now, SERVICE_WAKE_BOUND, hidden, poisoned, None, None);
            assert!(!wake.request_redraw);
            assert_eq!(
                wake.control_flow,
                ControlFlow::WaitUntil(now + SERVICE_WAKE_BOUND)
            );
        }
    }

    #[test]
    fn service_wake_does_not_release_first_paint_before_its_deadline() {
        let now = Instant::now();
        let paint = now + Duration::from_millis(100);
        let wake = plan_runtime_wake(now, SERVICE_WAKE_BOUND, false, false, Some(paint), None);
        assert!(!wake.request_redraw);
        assert_eq!(
            wake.control_flow,
            ControlFlow::WaitUntil(now + SERVICE_WAKE_BOUND)
        );
        let due = plan_runtime_wake(paint, SERVICE_WAKE_BOUND, false, false, Some(paint), None);
        assert!(due.request_redraw);
    }

    #[test]
    fn earlier_browser_repeat_wakes_before_service_timer() {
        let now = Instant::now();
        let repeat = now + Duration::from_millis(3);
        let wake = plan_runtime_wake(now, SERVICE_WAKE_BOUND, false, false, None, Some(repeat));
        assert!(wake.request_redraw);
        assert_eq!(wake.control_flow, ControlFlow::WaitUntil(repeat));
    }

    #[test]
    fn uncapped_gameplay_polls_without_requiring_a_surface() {
        let now = Instant::now();
        let wake = plan_runtime_wake(now, Duration::ZERO, true, false, None, None);
        assert_eq!(wake.control_flow, ControlFlow::Poll);
        assert!(!wake.request_redraw);
    }

    #[test]
    fn committed_frames_commands_and_events_ignore_display_sampling_schedule() {
        use crate::app::match_runtime::frame_pacer::LocalFramePacer;
        use crate::app::match_runtime::sim_tick::{
            RuntimePassInputs, SessionMode, decide_runtime_pass,
        };
        use crate::sim::command::{Command, CommandEnvelope};
        use crate::sim::runtime::{SimResources, SimRuntime};
        use crate::sim::world::{Simulation, TickLane};

        let run = |display_period: Option<u64>| {
            let map = crate::map::map_file::MapFile::from_bytes(
                b"[Map]\nTheater=TEMPERATE\nSize=0,0,40,40\nLocalSize=2,2,36,32\n\
                  [IsoMapPack5]\n1=CAAEABUAAAAAEQAA\n\
                  [VariableNames]\n9=Ready,1\n\
                  [Triggers]\nREADY=Neutral,<none>,Ready,0,1,1,1,0\n\
                  [Events]\nREADY=1,36,0,9\n\
                  [Actions]\nREADY=1,112,0,0,0,0,0,0,A\n",
            )
            .unwrap();
            let mut simulation = Simulation::new();
            let terrain =
                crate::map::resolved_terrain::ResolvedTerrainGrid::from_cells(0, 0, Vec::new());
            crate::sim::runtime::populate_staged_scenario_with_generated_inits(
                &mut simulation,
                &map,
                &terrain,
                "TEMPERATE",
                None,
                None,
                None,
                crate::map::basic::BridgeDestroyabilityMode::CampaignOrEditor,
                &crate::sim::scenario_session::ScenarioDescriptor::default(),
                None,
                |_| {},
            )
            .unwrap();
            let owner = simulation.interner.intern("Neutral");
            // An invalid target still has to be consumed at its attributed frame,
            // including while presentation has no sampling opportunities.
            simulation.queue_command(CommandEnvelope::new(
                owner,
                2,
                Command::Stop { entity_id: 999 },
            ));
            let mut resources = SimResources::empty();
            resources.trigger_graph = map.trigger_graph;
            resources.triggers = map.triggers;
            resources.events = map.events;
            resources.actions = map.actions;
            let mut runtime = SimRuntime {
                simulation,
                resources,
            };
            let mut pacer = LocalFramePacer::new();
            let mut trace = Vec::new();
            let mut effects = Vec::new();
            for now_ms in 0..=192 {
                let decision = decide_runtime_pass(RuntimePassInputs {
                    exact_step: false,
                    window_active: true,
                    startup_admitted: true,
                    frame_stepping: false,
                    paused: false,
                    menu_open: false,
                    session_mode: SessionMode::Skirmish,
                    pacer_timing_admits: pacer.should_admit(now_ms, 1, false),
                });
                if decision.run_sim {
                    let due = runtime.simulation.take_due_commands();
                    let output = runtime
                        .advance_frame(&due, crate::app::types::SIM_TICK_MS, TickLane::Ordinary)
                        .unwrap();
                    assert!(output.tick.frame_committed);
                    trace.push((
                        output.tick.tick,
                        output.tick.state_hash,
                        due,
                        runtime.simulation.rng_state(),
                    ));
                    effects.extend(output.trigger_effects);
                    pacer.record_admitted_frame(now_ms);
                }
                if display_period.is_some_and(|period| now_ms % period == 0) {
                    let before = runtime.simulation.rng_state();
                    let view = runtime.view();
                    let _ = (
                        view.entities(),
                        view.fog(),
                        view.session(),
                        view.simulation().parity_digest(),
                    );
                    assert_eq!(runtime.simulation.rng_state(), before);
                }
            }
            (trace, effects)
        };
        let expected = run(Some(16));
        assert_eq!(expected.0.len(), 13);
        assert_eq!(expected.0.iter().map(|row| row.2.len()).sum::<usize>(), 1);
        assert_eq!(
            expected.1.len(),
            1,
            "one-shot trigger output must survive missing displays"
        );
        for schedule in [Some(1), Some(7), Some(33), Some(192), None] {
            assert_eq!(run(schedule), expected, "display period {schedule:?}");
        }
    }

    #[test]
    fn exact_capture_sidebar_reconciliation_precedes_sound_drain() {
        // idle_tick -> refresh_sidebar_projection -> note_cameos may enqueue
        // EVA_NewConstructionOptions in this exact frame, including its final
        // capture step. Guard the production producer/consumer order rather
        // than maintain a second implementation of that sound pipeline.
        let source = include_str!("match_runtime/sim_tick.rs");
        let tail = &source[source.find("fn advance_in_game_runtime_mode(").unwrap()
            ..source
                .find("pub(crate) fn update_in_game_presentation(")
                .unwrap()];
        let sidebar = tail
            .find("update_in_game_presentation_data(state)")
            .unwrap();
        let drain = tail
            .find("building_anim::drain_sound_events(state)")
            .unwrap();
        assert!(
            sidebar < drain,
            "final-step sidebar EVA must reach the same drain"
        );
    }

    #[test]
    fn ordinary_redraw_only_uses_explicit_diagnostic_service_branch() {
        // Source wiring is intentionally guarded in addition to scheduling
        // behavior: bypassing this seam would couple gameplay back to redraws.
        let frame = include_str!("frame.rs");
        assert!(!frame.contains("sim_tick::advance_in_game_runtime("));
        assert!(!frame.contains("sim_tick::pump_audio_service("));
        assert!(!frame.contains("Self::consume_executed_abort_exit("));
        assert!(!frame.contains("Self::drive_scenario_exit("));
        let diagnostic_gate = frame
            .find("if (shell_capture.is_some() || tactical_capture.is_some())")
            .unwrap();
        let pump = frame.find("Self::pump_runtime_services(").unwrap();
        let presentation = frame
            .find("sim_tick::update_in_game_presentation(state)")
            .unwrap();
        assert!(diagnostic_gate < pump && pump < presentation);
    }
}
