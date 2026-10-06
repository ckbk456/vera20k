"""Native controls for the actual retained live type caller, not retail parity."""
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from tools.spatial_oracle.fv_cell_attack import steam_movement_profile as driver
from tools.spatial_oracle.fv_cell_attack import steam_live_types as live
from tools.spatial_oracle.fv_cell_attack import steam_live_assets as assets


class LiveAdmissionTests(unittest.TestCase):
    def test_missing_retained_history_fails_before_vm_creation(self):
        with patch.object(driver, 'constructor_inputs', side_effect=AssertionError('must not create VM')):
            with self.assertRaisesRegex(ValueError, 'complete retained prereaders'):
                driver.typed_master_inputs(Path('/nonexistent'), retained_live_types=True)
            with self.assertRaisesRegex(ValueError, 'complete profile/cache'):
                driver.typed_master_inputs(Path('/nonexistent'), retained_startup=True,
                    retained_dialog=True, ordered_cold_startup=True, retained_prereaders=True,
                    retained_live_types=True, native_state=object())


@unittest.skipUnless(os.environ.get('VERA20K_GAMEMD_EXE'), 'Requires authenticated native executable')
class NativeLiveCallerControls(unittest.TestCase):
    def test_absent_type_sections_reach_original_caller_and_all_missions(self):
        # FV exists in the original master registry, but no live Rules/ART
        # section exists. This executes genuine absent-reader returns and
        # original32 MissionControl reads without any physical asset request.
        # Explicit absent supplier initialization is a control boundary, never
        # authorization to skip retail localization/asset prerequisites.
        with tempfile.TemporaryDirectory(prefix='vera-w02-live-absent-') as directory:
            root = Path(directory)
            (root / 'RULESMD.INI').write_text('[VehicleTypes]\n0=FV\n[JumpjetControls]\nTurnRate=4\n[MultiplayerDialogSettings]\nMinPlayers=2\n')
            (root / 'ARTMD.INI').write_text('')
            with patch.object(assets, 'initialize_live_asset_inputs',
                    return_value=dict(boundary='Empty physical supplier control; no retail assets'), create=True):
                owner, selected, _, receipt = driver.typed_master_inputs(root,
                    retained_startup=True, retained_dialog=True, ordered_cold_startup=True,
                    retained_prereaders=True, retained_live_types=True, live_assets=object())
        observation = receipt['retained_live_types']
        self.assertEqual(observation['end'], 0x668EF5)
        self.assertTrue(all(observation['checks'].values()))
        self.assertEqual([(row['family'], row['name']) for row in observation['calls']], [('Unit', 'FV')])
        self.assertEqual([row['index'] for row in observation['missions']], list(range(32)))
        self.assertEqual(observation['constructors'], [])
        self.assertEqual(observation['counter_before'], observation['counter_after'])
        self.assertEqual(observation['asset_requests'], [])
        self.assertEqual(owner.string(selected + 0x24), 'FV')
        with self.assertRaisesRegex(ValueError, 'cannot restart'):
            live.continue_live_types(owner, owner.read32(0x8871E0),
                receipt['retained_prereaders']['rules_ini'], receipt)


if __name__ == '__main__':
    unittest.main()
