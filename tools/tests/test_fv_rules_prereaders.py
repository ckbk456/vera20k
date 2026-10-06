"""Bounded native reader controls; these do not claim retained startup parity."""
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from tools.spatial_oracle.fv_cell_attack import steam_movement_profile as driver


class PrereaderAdmissionTests(unittest.TestCase):
    def test_incomplete_history_is_rejected_before_creating_vm(self):
        with patch.object(driver,'constructor_inputs',side_effect=AssertionError('must not create VM')):
            with self.assertRaisesRegex(ValueError,'ordered cold startup'):
                driver.typed_master_inputs(Path('/nonexistent'),retained_prereaders=True)
            with self.assertRaisesRegex(ValueError,'complete profile/cache'):
                driver.typed_master_inputs(Path('/nonexistent'),retained_startup=True,retained_dialog=True,
                    ordered_cold_startup=True,retained_prereaders=True,native_state=object())

    def test_cli_cannot_overwrite_historical_corpus_without_explicit_path(self):
        result=subprocess.run([sys.executable,'-m','tools.spatial_oracle.fv_cell_attack.steam_movement_profile',
            '--retained-prereaders-only','--write'],capture_output=True,text=True)
        self.assertNotEqual(result.returncode,0)
        self.assertIn('separate explicit --output',result.stderr)


@unittest.skipUnless(os.environ.get('VERA20K_GAMEMD_EXE'),'Requires authenticated native executable')
class NativePrereaderControls(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from tools.rules_oracle.weapon_speed_order import construct_rules
        cls.profile=driver.rules_prereader_profile()
        cls.owner,_,cls.setup=driver.constructor_inputs(profile=cls.profile,heap_bytes=0x2000000,
            initial_counter=None,scenario_bytes=driver.NATIVE_SCENARIO_BYTES,native_scenario=True,
            construct_selected_type=False,initialize_options=True,initialize_physical=True,ordered_cold_startup=True)
        cls.rules=construct_rules(cls.owner,pointer=cls.owner.alloc(0x18C0))

    def test_scope_keeps_new_native_data_unwritable_by_fixture(self):
        from tools.native_oracle import OracleError
        from tools.spatial_oracle.fv_cell_attack.steam_rules_prereader_scope import PREREADER_NATIVE_DATA
        for address,size in PREREADER_NATIVE_DATA:
            with self.subTest(address=hex(address)):
                with self.assertRaises(OracleError)as raised:
                    self.owner.fixture_write(address,b'\0'*size)
                self.assertIn('fixture',str(raised.exception).lower())

    def test_original_absent_section_returns_preserve_rules_and_rng(self):
        from tools.spatial_oracle.fv_cell_attack.steam_rules_prereader_scope import READER_ENTRIES
        from tools.spatial_oracle.building_body_rules import INI
        self.owner.make_ini({})
        scene=self.owner.read32(0xA8B230)
        before=bytes(self.owner.u.mem_read(self.rules,0x18C0))
        rngs=(0x886B88,scene+0x218,0xABE890)
        states=[bytes(self.owner.u.mem_read(address,0x3F4))for address in rngs]
        counter=self.owner.read32(scene+0x214);cursor=self.owner.cursor
        for name,entry in READER_ENTRIES:
            self.owner.invoke(entry,self.rules,(INI,),context=dict(case='isolated-absent-section-'+name))
        self.assertEqual(bytes(self.owner.u.mem_read(self.rules,0x18C0)),before)
        self.assertEqual([bytes(self.owner.u.mem_read(address,0x3F4))for address in rngs],states)
        self.assertEqual(self.owner.read32(scene+0x214),counter)
        self.assertEqual(self.owner.cursor,cursor)

    def test_powerups_initial_state_is_file_defaults_and_supplied_bss(self):
        import struct
        owner=self.owner
        self.assertEqual(struct.unpack('<19i',bytes(owner.u.mem_read(0x81DA8C,76))),
            (50,20,1,3,5,5,20,1,1,10,10,10,1,3,1,1,1,1,1))
        self.assertEqual(bytes(owner.u.mem_read(0x81DAD8,76)),b'\xff'*76)
        self.assertEqual(bytes(owner.u.mem_read(0x89EC28,152)),bytes(152))
        self.assertEqual(bytes(owner.u.mem_read(0x89ECC0,19)),bytes(19))


@unittest.skipUnless(os.environ.get('VERA20K_GAMEMD_EXE'),'Requires authenticated native executable')
class IsolatedRetailScopeTests(unittest.TestCase):
    def test_retail_reader_paths_fail_closed_before_retained_prefix(self):
        from tools.rules_oracle.weapon_speed_order import construct_rules
        from tools.rules_oracle.bridge_anim_inputs import physical_sections
        from tools.spatial_oracle.fv_cell_attack.steam_rules_prereader_scope import READER_ENTRIES
        from tools.spatial_oracle.building_body_rules import INI
        from unicorn import UC_HOOK_CODE
        from unicorn.x86_const import UC_X86_REG_ECX,UC_X86_REG_ESP
        profile=driver.rules_prereader_profile()
        owner,_,_=driver.constructor_inputs(profile=profile,heap_bytes=0x2000000,
            initial_counter=None,scenario_bytes=driver.NATIVE_SCENARIO_BYTES,native_scenario=True,
            construct_selected_type=False,initialize_options=True,initialize_physical=True,ordered_cold_startup=True)
        rules=construct_rules(owner,pointer=owner.alloc(0x18C0))
        root=Path(os.environ['VERA20K_FV_MOVEMENT_ASSETS'])
        selected=('AI','Powerups','IQ','General','Clear','Rough','Road','Water','Rock','Beach','Ore','Weeds','Ice','Railroad','Tunnel')
        owner.make_ini(physical_sections((root/'RULESMD.INI').read_bytes(),names=selected))
        scene=owner.read32(0xA8B230);counter=owner.read32(scene+0x214)
        rngs=(0x886B88,scene+0x218,0xABE890)
        before=[bytes(owner.u.mem_read(address,0x3F4))for address in rngs]
        names={entry:family for family,_,entry,_,_,_,_ in driver.TYPED_MASTER_FAMILIES}
        # Original771C7A calls the same AbstractType410800 constructor; the
        # first DropPodWeapon also consumes an actual Scenario ID.
        names[0x771C70]='Weapon'
        constructors=[]
        def observe(uc,address,size,data):
            if address not in names:return
            sp=uc.reg_read(UC_X86_REG_ESP)
            constructors.append((names[address],owner.string(owner.read32(sp+4)),uc.reg_read(UC_X86_REG_ECX)))
        hook=owner.u.hook_add(UC_HOOK_CODE,observe)
        try:
            for name,entry in READER_ENTRIES:
                owner.invoke(entry,rules,(INI,),timeout_us=180_000_000,context=dict(
                    case='isolated-retail-prereader-scope-'+name,
                    limitation='No typed master prefix, ART cache or retained Process frame; this only tests declared reader admission.'))
        finally:owner.u.hook_del(hook)
        self.assertEqual([bytes(owner.u.mem_read(address,0x3F4))for address in rngs],before)
        self.assertEqual(owner.read32(scene+0x214),counter+len(constructors))
        self.assertTrue(any(family=='Unit'and name=='VISC_LRG'for family,name,_ in constructors))
        weapon=owner.read32(owner.read32(0x88756C))
        self.assertEqual(owner.string(weapon+0x24),'Vulcan2')


@unittest.skipUnless(os.environ.get('VERA20K_GAMEMD_EXE'),'Requires authenticated native executable')
class SmallRetainedCallerTests(unittest.TestCase):
    def test_actual_process_continuation_retains_frame_and_native_ids(self):
        # Small explicit INI fixture tests the original retained ABI/history,
        # not retail coverage. The expensive retail prefix is a separate run.
        rules='''[VehicleTypes]
0=FV
[JumpjetControls]
TurnRate=4
[MultiplayerDialogSettings]
MinPlayers=2
[AI]
AttackInterval=0.5
[Powerups]
Money=50,NONE,yes,100
[IQ]
MaxIQLevels=5
[General]
LargeVisceroid=VISC_LRG
SmallVisceroid=VISC_SML
DropPodWeapon=Vulcan2
'''
        with tempfile.TemporaryDirectory(prefix='vera-w02-small-native-')as directory:
            root=Path(directory)
            (root/'RULESMD.INI').write_text(rules)
            (root/'ARTMD.INI').write_text('[FV]\nImage=FV\n')
            owner,selected,_,receipt=driver.typed_master_inputs(root,retained_startup=True,
                retained_dialog=True,ordered_cold_startup=True,retained_prereaders=True)
        continuation=receipt['retained_prereaders']
        self.assertEqual(continuation['end'],0x668EED)
        self.assertTrue(all(continuation['checks'].values()))
        self.assertEqual([row['name']for row in continuation['constructors']],['VISC_LRG','VISC_SML','Vulcan2'])
        self.assertEqual(continuation['counter_after']-continuation['counter_before'],3)
        self.assertEqual(owner.string(selected+0x24),'FV')
        with self.assertRaisesRegex(ValueError,'cannot restart'):
            driver.continue_rules_prereaders(owner,owner.read32(0x8871E0),continuation['rules_ini'],receipt)


if __name__=='__main__':unittest.main()
