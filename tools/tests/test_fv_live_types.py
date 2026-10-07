"""Native controls for the actual retained live type caller, not retail parity."""
import os
import hashlib
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
    def test_borrowed_startup_matches_existing_scoped_owner_on_fresh_vms(self):
        from types import SimpleNamespace
        from unicorn import Uc, UC_ARCH_X86, UC_MODE_32
        from tools import native_oracle as oracle
        from tools.spatial_oracle import mapgen_range
        observed = []
        for borrowed in (False, True):
            u = Uc(UC_ARCH_X86, UC_MODE_32)
            image = oracle.load_image(u, profile=live.live_types_profile())
            u.mem_map(oracle.STACK_BASE, oracle.STACK_SIZE)
            u.mem_map(oracle.RET_MAGIC, 0x1000)
            receiver = (SimpleNamespace(u=u, image=image) if borrowed
                        else mapgen_range.Machine.__new__(mapgen_range.Machine))
            receiver.u, receiver.image = u, image
            observed.append(mapgen_range.Machine.startup(receiver))
            image.verify_code()
        self.assertEqual(observed[0], observed[1])

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
            (root / 'dragon-cadence.map').write_text('[Map]\nTheater=TEMPERATE\n')
            with patch.object(assets, 'initialize_live_asset_inputs',
                    return_value=dict(boundary='Empty physical supplier control; no retail assets'), create=True), \
                 patch.object(assets, 'initialize_live_theater_assets',
                    return_value=dict(boundary='No physical theater assets in absent-section control'), create=True):
                owner, selected, _, receipt = driver.typed_master_inputs(root,
                    retained_startup=True, retained_dialog=True, ordered_cold_startup=True,
                    retained_prereaders=True, retained_live_types=True, live_assets=object())
        observation = receipt['retained_live_types']
        binding = receipt['setup']['live_map_theater']
        self.assertEqual((binding['before'], binding['value']), (0xFFFFFFFF, 0))
        self.assertEqual(owner.read32(owner.read32(0xA8B230) + 0x1258), binding['value'])
        self.assertEqual(binding['source_value'], 'TEMPERATE')
        self.assertEqual(binding['map_sha256'], hashlib.sha256(b'[Map]\nTheater=TEMPERATE\n').hexdigest())
        self.assertEqual((binding['native_entry'], binding['native_end']), (0x687631, 0x68764F))
        self.assertTrue(binding['before_process'])
        self.assertTrue(binding['retained_cache_counter_rng'])
        self.assertEqual(binding['original_order'],
            (0x68763E, 0x687649, 0x68765B, 0x6876AC, 0x668A27, 0x68774F))
        self.assertEqual(binding['rules_receiver'], receipt['cache_preparation']['rules_receiver'])
        self.assertEqual(binding['art_receiver'], receipt['cache_preparation']['art_receiver'])
        self.assertNotIn(binding['ini_pointer'], (binding['rules_receiver'], binding['art_receiver']))
        self.assertEqual(owner.ini_cache_snapshot(binding['art_receiver'])['sections'], [])
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
