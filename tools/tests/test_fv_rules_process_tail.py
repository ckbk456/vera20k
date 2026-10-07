"""Rules tail admission and actual original return controls; no gameplay parity."""
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from tools.spatial_oracle.fv_cell_attack import steam_movement_profile as driver
from tools.spatial_oracle.fv_cell_attack import steam_rules_process_tail as tail
from tools.spatial_oracle.fv_cell_attack import steam_live_assets as assets


class RulesTailAdmissionTests(unittest.TestCase):
    def test_tail_cannot_run_without_the_complete_live_route(self):
        with self.assertRaisesRegex(ValueError, 'complete retained live-type route'):
            driver.typed_master_inputs(Path('/nonexistent'), retained_rules_process_tail=True)

    def test_tail_cannot_adopt_another_vm_or_change_the_selected_profile(self):
        with self.assertRaisesRegex(ValueError, 'complete profile/cache'):
            driver.typed_master_inputs(Path('/nonexistent'), retained_startup=True,
                retained_dialog=True, ordered_cold_startup=True, retained_prereaders=True,
                retained_live_types=True, retained_rules_process_tail=True, native_state=object())


@unittest.skipUnless(os.environ.get('VERA20K_GAMEMD_EXE'), 'Requires authenticated native executable')
class NativeRulesTailControls(unittest.TestCase):
    def _assert_rejected_before_process(self, source, message, *, mode=0):
        from unicorn import UC_HOOK_CODE
        constructor = driver.constructor_inputs
        observations = []

        def observed_constructor(**kwargs):
            result = constructor(**kwargs)
            owner = result[0]
            self.assertEqual(owner.read32(0xA8B238), 0)
            if mode:
                # Unsupported incoming mode is the control's input prior;
                # no native result or registry is supplied or repaired.
                owner.u.mem_write(0xA8B238, mode.to_bytes(4, 'little'))
            process_entries = []
            owner.u.hook_add(UC_HOOK_CODE,
                lambda u, address, size, data: process_entries.append(address),
                begin=0x668BF0, end=0x668BF0)
            observations.append((owner, process_entries))
            return result

        with tempfile.TemporaryDirectory(prefix='vera-rules-tail-present-') as directory:
            root = Path(directory)
            (root / 'RULESMD.INI').write_text(source)
            with patch.object(driver, 'constructor_inputs', side_effect=observed_constructor), \
                 patch.object(assets, 'initialize_live_asset_inputs', return_value={}):
                with self.assertRaisesRegex(ValueError, message):
                    driver.typed_master_inputs(root,
                        retained_startup=True, retained_dialog=True, ordered_cold_startup=True,
                        retained_prereaders=True, retained_live_types=True,
                        retained_rules_process_tail=True, live_assets=object())
        self.assertEqual(len(observations), 1)
        owner, process_entries = observations[0]
        self.assertEqual(process_entries, [])
        self.assertEqual(owner.read32(0xA8B238), mode)

    def test_present_command_bar_is_rejected_before_entering_the_root_process(self):
        self._assert_rejected_before_process('[AdvancedCommandBar]\n0=Move\n',
            'Populated command-bar sections')

    def test_present_multiplayer_command_bar_is_rejected_before_process(self):
        self._assert_rejected_before_process('[MultiplayerAdvancedCommandBar]\n0=Move\n',
            'Populated command-bar sections')

    def test_nonzero_mode_is_rejected_before_process_without_repairing_the_prior(self):
        self._assert_rejected_before_process('', 'unchanged cold mode-zero prior', mode=1)

    def test_empty_sections_complete_the_original_frame_and_ordered_tiberium_crt(self):
        with tempfile.TemporaryDirectory(prefix='vera-rules-tail-absent-') as directory:
            root = Path(directory)
            (root / 'RULESMD.INI').write_text('[VehicleTypes]\n0=FV\n[JumpjetControls]\nTurnRate=4\n[MultiplayerDialogSettings]\nMinPlayers=2\n')
            (root / 'ARTMD.INI').write_text('')
            (root / 'dragon-cadence.map').write_text('[Map]\nTheater=TEMPERATE\n')
            # Explicit omitted physical-supplier control; no retail catalog or
            # asset result is supplied or claimed. The original tail executes.
            with patch.object(assets, 'initialize_live_asset_inputs', return_value={}), \
                 patch.object(assets, 'initialize_live_theater_assets', return_value={}):
                owner, _, _, receipt = driver.typed_master_inputs(root,
                    retained_startup=True, retained_dialog=True, ordered_cold_startup=True,
                    retained_prereaders=True, retained_live_types=True,
                    retained_rules_process_tail=True, live_assets=object())
        observation = receipt['retained_rules_process_tail']
        self.assertTrue(all(observation['checks'].values()))
        self.assertEqual(observation['end'], tail.RET_MAGIC)
        self.assertEqual(observation['tiberium_after']['members'], [])
        self.assertEqual(observation['constructors'], [])
        self.assertEqual(observation['warhead_rereads'], [])
        self.assertEqual(observation['rng_before'], observation['rng_after'])
        self.assertEqual(observation['saved_registers_before'], observation['restored_registers_after'])
        cold = receipt['setup']['ordered_cold_startup']
        row = next(row for row in cold['callbacks'] if row['family'] == 'Tiberium')
        self.assertEqual((row['ordinal'], row['slot'], row['entry']),
                         (3220, 0x815250, 0x721640))
        self.assertTrue(row['unpublished_scenario'])
        self.assertEqual(owner.read32(tail.TIBERIUM_REGISTRY), 0x7F56BC)
        with self.assertRaisesRegex(ValueError, 'cannot restart'):
            tail.continue_rules_process_tail(owner, owner.read32(0x8871E0),
                receipt['retained_prereaders']['rules_ini'], receipt)


if __name__ == '__main__':unittest.main()
