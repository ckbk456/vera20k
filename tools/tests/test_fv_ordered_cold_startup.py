"""Authenticated selected-startup controls; no joined movement parity claim."""
import os
from pathlib import Path
import unittest
from unittest.mock import patch

from unicorn import UC_HOOK_CODE

from tools.rules_oracle.bridge_anim_inputs import Reader
from tools.spatial_oracle.fv_cell_attack import steam_movement_profile as driver


@unittest.skipUnless(os.environ.get('VERA20K_GAMEMD_EXE'), 'Requires authenticated native executable')
class OrderedColdStartupTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.visits=[]
        original=Reader.__init__
        def initialize(owner,*args,**kwargs):
            original(owner,*args,**kwargs)
            watched={row[4]for row in driver.TYPED_MASTER_FAMILIES}
            watched.update((0x40FB30,0x47B150,0x4AF330,0x4E7A60,0x4E7B60,
                0x4E7CF0,0x5B3700,0x565060,0x5F6FF0,0x725350,0x6832C0))
            def observe(uc,address,size,data):
                if address in watched:cls.visits.append((address,owner.read32(0xA8B230)))
            owner.u.hook_add(UC_HOOK_CODE,observe)
        with patch.object(Reader,'__init__',initialize):
            cls.owner,ptr,cls.receipt=driver.constructor_inputs(profile=driver.ordered_startup_profile(),
                heap_bytes=0x2000000,initial_counter=None,scenario_bytes=driver.NATIVE_SCENARIO_BYTES,
                native_scenario=True,construct_selected_type=False,initialize_options=True,
                initialize_physical=True,ordered_cold_startup=True)
        if ptr is not None:raise AssertionError('Selected startup must not construct isolated FV')

    def test_actual_native_callbacks_precede_scenario_without_restarts(self):
        addresses=[address for address,_ in self.visits]
        self.assertTrue(all(pointer==0 for _,pointer in self.visits))
        self.assertEqual(addresses.count(0x5B3700),32)
        for address in (0x40FB30,0x47B150,0x4AF330,0x4E7CF0,0x565060,0x5F6FF0,0x725350,0x6832C0):
            self.assertEqual(addresses.count(address),1,hex(address))
        ordered=(0x40F490,0x40FB30,0x47B150,0x4AF330,0x4E6F60,0x4E6FE0,
            0x4E7CF0,0x565060,0x5F6FF0,0x725350,0x6832C0)
        self.assertEqual(sorted(addresses.index(address)for address in ordered),
            [addresses.index(address)for address in ordered])
        self.assertEqual(self.receipt['scenario_counter_before'],1000000)
        self.assertTrue(self.owner.read32(0xA8B230))

    def test_repeated_startup_is_rejected_before_native_mutation(self):
        scene=self.owner.read32(0xA8B230)
        before=bytes(self.owner.u.mem_read(scene,driver.NATIVE_SCENARIO_BYTES))
        with patch.object(self.owner,'invoke',side_effect=AssertionError('must not execute')):
            with self.assertRaisesRegex(ValueError,'published or initialized'):
                driver.initialize_ordered_cold_crt(self.owner)
        self.assertEqual(bytes(self.owner.u.mem_read(scene,driver.NATIVE_SCENARIO_BYTES)),before)

    def test_historical_route_cannot_admit_ordered_startup(self):
        with patch.object(Reader,'__init__',side_effect=AssertionError('must not construct VM')):
            with self.assertRaisesRegex(ValueError,'requires fresh native Scenario'):
                driver.constructor_inputs(ordered_cold_startup=True)
            with self.assertRaisesRegex(ValueError,'requires the fresh retained startup owner'):
                driver.typed_master_inputs(Path('/nonexistent'),ordered_cold_startup=True)

    def test_weapon_layer_adopts_existing_native_registries(self):
        headers=bytes(self.owner.u.mem_read(0x8874C0,24)),bytes(self.owner.u.mem_read(0x887568,24))
        exits=list(self.owner.exit_registrations)
        with patch.object(self.owner,'invoke',side_effect=AssertionError('must not restart registry')):
            with self.assertRaisesRegex(AssertionError,'required layer absent'):
                driver.movement_key_layers(Path('/nonexistent'),native_state=(self.owner,None,self.receipt),include_weapons=True)
        self.assertEqual((bytes(self.owner.u.mem_read(0x8874C0,24)),bytes(self.owner.u.mem_read(0x887568,24))),headers)
        self.assertEqual(self.owner.exit_registrations,exits)

    def test_weapon_layer_rejects_missing_startup_without_repair(self):
        with patch.object(self.owner,'read32',return_value=0),patch.object(self.owner,'invoke',side_effect=AssertionError('must not repair')):
            with self.assertRaisesRegex(ValueError,'retain its Weapon and Warhead registries'):
                driver.movement_key_layers(Path('/nonexistent'),native_state=(self.owner,None,self.receipt),include_weapons=True)


if __name__=='__main__':unittest.main()
