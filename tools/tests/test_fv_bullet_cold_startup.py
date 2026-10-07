"""Original-order Bullet CRT controls; no live type/movement parity claim."""
from dataclasses import replace
import os
import struct
import unittest
from unittest.mock import patch

from unicorn import UC_HOOK_CODE

from tools.native_oracle import OracleError
from tools.rules_oracle.bridge_anim_inputs import Reader
from tools.spatial_oracle.fv_cell_attack import steam_movement_profile as driver
from tools.spatial_oracle.fv_cell_attack import steam_bullet_startup_scope as bullet


class BulletDeclarationTests(unittest.TestCase):
    def test_wrong_binary_or_historical_unordered_profile_is_rejected(self):
        for profile in (driver.STEAM_CONSTRUCTOR_PROFILE,
                replace(driver.ordered_startup_profile(),native_sha256='0'*64)):
            with self.assertRaisesRegex(ValueError,'authenticated ordered startup'):
                bullet.extend_ordered_startup_profile(profile)


@unittest.skipUnless(os.environ.get('VERA20K_GAMEMD_EXE'), 'Requires authenticated native executable')
class OrderedBulletStartupTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.visits=[]
        original=Reader.__init__
        def initialize(owner,*args,**kwargs):
            original(owner,*args,**kwargs)
            watched={bullet.BULLET_COLD_ENTRY,0x4E7560,0x4E7660,0x4E7CF0,
                0x5B3700,0x565060,0x6832C0}
            def observe(uc,address,size,data):
                if address in watched:cls.visits.append((address,owner.read32(0xA8B230)))
            owner.u.hook_add(UC_HOOK_CODE,observe)
        cls.profile=bullet.extend_ordered_startup_profile(driver.ordered_startup_profile())
        with patch.object(Reader,'__init__',initialize):
            cls.owner,ptr,cls.receipt=driver.constructor_inputs(profile=cls.profile,
                heap_bytes=0x2000000,initial_counter=None,scenario_bytes=driver.NATIVE_SCENARIO_BYTES,
                native_scenario=True,construct_selected_type=False,initialize_options=True,
                initialize_physical=True,ordered_cold_startup=True)
        if ptr is not None:raise AssertionError('Fresh CRT control must not construct isolated FV')

    def test_original_table_and_execution_order_precede_scenario(self):
        self.assertEqual(self.owner.read32(bullet.BULLET_COLD_TABLE_SLOT),bullet.BULLET_COLD_ENTRY)
        addresses=[address for address,_ in self.visits]
        self.assertTrue(all(pointer==0 for _,pointer in self.visits))
        self.assertEqual(addresses.count(bullet.BULLET_COLD_ENTRY),1)
        self.assertEqual(addresses.count(0x5B3700),32)
        order=(0x4E7560,bullet.BULLET_COLD_ENTRY,0x4E7660,0x4E7CF0,0x565060,0x6832C0)
        self.assertEqual([addresses.index(address)for address in order],
            sorted(addresses.index(address)for address in order))
        row,=[row for row in self.receipt['ordered_cold_startup']['callbacks']if row['family']=='Bullet']
        self.assertEqual((row['ordinal'],row['slot'],row['entry']),
            (bullet.BULLET_COLD_TABLE_INDEX,bullet.BULLET_COLD_TABLE_SLOT,bullet.BULLET_COLD_ENTRY))
        self.assertEqual(self.receipt['scenario_counter_before'],1_000_000)

    def test_native_header_and_exit_registration_without_allocation_or_rng(self):
        header=bytes(self.owner.u.mem_read(bullet.BULLET_REGISTRY,bullet.BULLET_REGISTRY_BYTES))
        # Checked original execution establishes the vtable/pointer/capacity,
        # enabled flags, count and growth increment; no fixture supplies them.
        self.assertEqual(struct.unpack('<6I',header),
            (bullet.BULLET_REGISTRY_VTABLE,0,0,1,0,10))
        self.assertEqual(self.owner.exit_registrations.count(bullet.BULLET_EXIT_CALLBACK),1)
        crt=self.receipt['ordered_cold_startup']
        self.assertEqual(crt['rng_before'],crt['rng_after'])
        self.assertEqual(crt['allocation_count_before'],crt['allocation_count_after'])

    def test_registry_fixture_writes_and_retained_restart_are_rejected(self):
        before=bytes(self.owner.u.mem_read(bullet.BULLET_REGISTRY,bullet.BULLET_REGISTRY_BYTES))
        with self.assertRaisesRegex(OracleError,'undeclared fixture write'):
            self.owner.fixture_write(bullet.BULLET_REGISTRY,bytes(bullet.BULLET_REGISTRY_BYTES))
        with patch.object(self.owner,'invoke',side_effect=AssertionError('must not repair')):
            with self.assertRaisesRegex(ValueError,'published or initialized'):
                driver.initialize_ordered_cold_crt(self.owner)
        self.assertEqual(bytes(self.owner.u.mem_read(bullet.BULLET_REGISTRY,bullet.BULLET_REGISTRY_BYTES)),before)

    def test_historical_profiles_do_not_enroll_bullet(self):
        for profile in (driver.ordered_startup_profile(),driver.rules_prereader_profile()):
            self.assertFalse(any(start<=bullet.BULLET_COLD_ENTRY<end for start,end,_ in profile.regions))
            self.assertFalse(any(entry==bullet.BULLET_COLD_ENTRY for entry,_ in profile.entries))


if __name__=='__main__':unittest.main()
