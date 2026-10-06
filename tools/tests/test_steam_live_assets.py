"""Immutable supplier/Win32 IO controls; native execution is a separate witness."""
import hashlib
import os
from pathlib import Path
import struct
import tempfile
import unittest
from unittest.mock import Mock,patch

from tools.sidebar_oracle.stock import mix, mix_hash, mix_index
from tools.spatial_oracle.fv_cell_attack.steam_live_assets import (
    PhysicalAssets, ReadOnlyFiles, Span, initialize_live_theater_assets,
    _activate_live_palette_theater)
from tools.storage_oracle.keyboard_bindings import parse_csf
from tools.rules_oracle.bridge_anim_inputs import Reader


class ImmutableSupplierTests(unittest.TestCase):
    @staticmethod
    def theater_record(label,long,iso_long,iso_short,short):
        record=bytearray(112)
        for offset,width,value in((0,16,label),(0x30,10,long),(0x3A,10,iso_long),(0x44,10,iso_short),(0x4E,4,short)):
            raw=value.encode('ascii')+b'\0';assert len(raw)<=width
            record[offset:offset+len(raw)]=raw
        return bytes(record)

    @staticmethod
    def archive_owner(directory,payloads):
        owner=PhysicalAssets.__new__(PhysicalAssets);owner.root=Path(directory)
        owner.loose={};owner.archives=[];owner.winners={};owner.buffers={};owner.requests=[]
        owner.audio_pair={};owner.theater_registration=None
        for name,entries in payloads.items():
            body=b'';index=b''
            for leaf,blob in entries.items():
                index+=struct.pack('<III',mix_hash(leaf),len(body),len(blob));body+=blob
            path=owner.root/name;path.write_bytes(struct.pack('<HI',len(entries),len(body))+index+body)
            owner.loose[name.upper()]=Span.disk(path)
        return owner

    def test_theater_registration_preserves_crc_winners_and_existing_buffers(self):
        with tempfile.TemporaryDirectory()as directory:
            assets=self.archive_owner(directory,{
                'CORE.MIX':{'CACHED.SHP':b'core'},
                'URBAN.MIX':{'CACHED.SHP':b'theater','NEW.URB':b'long'},
                'URB.MIX':{'NEW.URB':b'short'},
                'ISOURBMD.MIX':{'NEW.URB':b'iso override'},
                'ISOURB.MIX':{'NEW.URB':b'iso base'}})
            assets.mount('CORE.MIX');cached=assets.read('CACHED.SHP')[0]
            buffers=assets.buffers;winner=assets.winners[mix_hash('CACHED.SHP')]
            record=self.theater_record('URBAN','URBAN','ISOURB','ISOURB','URB')
            receipt=assets.register_theater(2,record)
            self.assertEqual(receipt['archive_order'],['URBAN.MIX','URB.MIX','ISOURBMD.MIX','ISOURB.MIX'])
            self.assertTrue(all(row['present']for row in receipt['mounts']))
            self.assertIs(assets.buffers,buffers);self.assertIs(assets.read('CACHED.SHP')[0],cached)
            self.assertIs(assets.winners[mix_hash('CACHED.SHP')],winner)
            self.assertEqual(assets.read('NEW.URB')[0],b'long')

    def test_theater_snow_only_override_records_real_absence_and_is_idempotent(self):
        with tempfile.TemporaryDirectory()as directory:
            assets=self.archive_owner(directory,{'SNOWMD.MIX':{'WATER.SNO':b'override'},
                                                 'SNOW.MIX':{'WATER.SNO':b'base'}})
            record=self.theater_record('SNOW','SNOW','ISOSNOW','ISOSNO','SNO')
            receipt=assets.register_theater(1,record)
            self.assertEqual(receipt['archive_order'],['SNOWMD.MIX','SNOW.MIX','SNO.MIX','ISOSNOMD.MIX','ISOSNOW.MIX'])
            self.assertEqual([row['present']for row in receipt['mounts']],[True,True,False,False,False])
            self.assertEqual(assets.read('WATER.SNO')[0],b'override')
            count=len(assets.archives)
            self.assertIs(assets.register_theater(1,record),receipt)
            self.assertEqual(len(assets.archives),count)
            with self.assertRaisesRegex(ValueError,'switch'):
                assets.register_theater(2,self.theater_record('URBAN','URBAN','ISOURB','ISOURB','URB'))

    def test_theater_registration_rejects_cold_or_invalid_native_record(self):
        with tempfile.TemporaryDirectory()as directory:
            assets=self.archive_owner(directory,{})
            record=self.theater_record('URBAN','URBAN','ISOURB','ISOURB','URB')
            for index in(-1,6,True):
                with self.assertRaisesRegex(ValueError,'index'):assets.register_theater(index,record)
            with self.assertRaisesRegex(ValueError,'extent'):assets.register_theater(2,record[:-1])
            malformed=bytearray(record);malformed[0x30:0x3A]=b'X'*10
            with self.assertRaisesRegex(ValueError,'Unterminated'):assets.register_theater(2,malformed)
            self.assertEqual(assets.archives,[])

    def test_theater_attached_helper_rejects_wrong_native_image_before_mounting(self):
        with tempfile.TemporaryDirectory()as directory:
            assets=self.archive_owner(directory,{})
            owner=Mock();owner.asset_source=assets;owner.image.machine=owner.u
            owner.image.profile.native_sha256='wrong image'
            with self.assertRaisesRegex(ValueError,'Authenticated original Steam'):
                initialize_live_theater_assets(owner,assets)
            self.assertEqual(assets.archives,[])
            owner.image.verify_code.assert_not_called()

    def test_palette_activation_requires_scenario_and_rejects_warm_prior_before_native_entry(self):
        owner=Mock();owner.read32.return_value=0
        with self.assertRaisesRegex(ValueError,'Native Scenario theater'):
            _activate_live_palette_theater(owner,0)
        owner.invoke.assert_not_called()
        owner.read32.return_value=0x24001000
        owner.u.mem_read.return_value=struct.pack('<4I',0,0x24001100,0x24001200,0x24001300)
        with self.assertRaisesRegex(ValueError,'Original cold palette manager'):
            _activate_live_palette_theater(owner,0)
        owner.invoke.assert_not_called()

    def test_palette_activation_preserves_warm_entries_and_checks_scenario_index(self):
        owner=Mock();manager=0x24001000;table=0x24001300;buckets=0x24001400;scene=0x24002000
        state={manager:struct.pack('<4I',0xFFFFFFFF,0x24001100,0x24001200,table),
               table:struct.pack('<4I',buckets,0x626660,31,10),buckets:bytes(31*24)}
        occupied=bytearray(state[buckets]);struct.pack_into('<I',occupied,16,1)
        state[buckets]=bytes(occupied)
        owner.u.mem_read.side_effect=lambda address,size:state[address][:size]
        owner.read32.side_effect=lambda address:{0xAC48F0:manager,0xA8B230:scene,scene+0x1258:1}[address]
        with self.assertRaisesRegex(ValueError,'Warm palette entries'):
            _activate_live_palette_theater(owner,0)
        self.assertEqual(struct.unpack_from('<I',state[buckets],16)[0],1)
        owner.invoke.assert_not_called()
        state[buckets]=bytes(31*24)
        with self.assertRaisesRegex(ValueError,'Native Scenario theater'):
            _activate_live_palette_theater(owner,0)
        owner.invoke.assert_not_called()

    @staticmethod
    def lexical_owner():
        owner=Reader.__new__(Reader);owner.u=object();owner.image=Mock()
        owner.image.machine=owner.u;owner.image.profile=object()
        owner.cursor=0x24010000;owner.heap_end=0x24100000
        owner.fixture_write=Mock()
        return owner

    def test_scoped_lexical_crc_reuses_one_native_result_across_receivers(self):
        owner=self.lexical_owner()
        with patch('tools.rules_oracle.bridge_anim_inputs.crc',return_value=0x12345678)as native:
            for pointer in (0x887180,0x8871C0,0x887200):
                owner.make_ini({'Repeated':{'Repeated':'actual bytes'}},pointer=pointer)
        native.assert_called_once_with('Repeated',profile=owner.image.profile)
        self.assertEqual(owner.image.verify_code.call_count,3)
        owner.image=Mock(machine=owner.u,profile=object())
        with self.assertRaisesRegex(ValueError,'another native image'):
            owner.make_ini({'Repeated':{'Repeated':'new bytes'}})

    def test_failed_crc_observation_is_not_cached(self):
        owner=self.lexical_owner()
        with patch('tools.rules_oracle.bridge_anim_inputs.crc',side_effect=[ValueError('native fail'),0x1234])as native:
            with self.assertRaisesRegex(ValueError,'native fail'):
                owner.make_ini({'Repeated':{'Repeated':'bytes'}})
            self.assertEqual(owner._lexical_crc_values,{})
            owner.make_ini({'Repeated':{'Repeated':'bytes'}})
            self.assertEqual(native.call_count,2)

    def test_shared_mix_decoder_rejects_outside_and_duplicate_members(self):
        payload=b'HELLO'
        good=struct.pack('<HI',1,len(payload))+struct.pack('<III',mix_hash('TEST.SHP'),0,len(payload))+payload
        self.assertEqual(mix(good),{mix_hash('TEST.SHP'):payload})
        entries,_=mix_index(lambda o,n:good[o:o+n],len(good))
        self.assertEqual(entries[mix_hash('TEST.SHP')],(18,5))
        bad=bytearray(good);struct.pack_into('<I',bad,14,6)
        with self.assertRaisesRegex(ValueError,'outside'):mix(bad)
        duplicate=struct.pack('<HI',2,0)+struct.pack('<III',1,0,0)*2
        with self.assertRaisesRegex(ValueError,'Duplicate'):mix(duplicate)

    def test_frozen_extent_rejects_replacement(self):
        with tempfile.TemporaryDirectory()as directory:
            path=Path(directory)/'TEST.VXL';path.write_bytes(b'ORIGINAL')
            span=Span.disk(path)
            self.assertEqual(span.child(2,3,'member').read(),b'IGI')
            with self.assertRaisesRegex(ValueError,'extent'):span.child(8,1,'outside')
            replacement=Path(directory)/'REPLACEMENT';replacement.write_bytes(b'ORIGINAL');replacement.replace(path)
            with self.assertRaisesRegex(ValueError,'changed'):span.read()

    def test_read_only_file_protocol_preserves_eof_seek_and_missing(self):
        class Supplied:
            def read(self,name,buffer=False):
                blob=b'ABCDE'if name.upper()=='FV.HVA'else None
                return blob,dict(source='locked-test',sha256=hashlib.sha256(blob).hexdigest()if blob else None)
        files=ReadOnlyFiles(Supplied())
        self.assertEqual(files.open('missing.vxl',0x80000000,1,0,3,0x80,0),0xFFFFFFFF)
        self.assertEqual(files.last_error,2)
        handle=files.open('FV.HVA',0x80000000,3,0,3,0x08000080,0)
        self.assertEqual(files.read(handle,3),b'ABC')
        self.assertEqual(files.seek(handle,0xFFFFFFFE,0,1),1)
        self.assertEqual(files.read(handle,20),b'BCDE')
        self.assertEqual(files.read(handle,1),b'')
        with self.assertRaisesRegex(ValueError,'exceeds'):files.seek(handle,1,0,2)
        self.assertEqual(files.close(handle),1)
        with self.assertRaisesRegex(ValueError,'unowned'):files.close(handle)
        with self.assertRaisesRegex(ValueError,'read-only'):files.open('FV.HVA',0x40000000,0,0,2,0x80,0)

    def test_csf_shared_parser_retains_extra_payloads(self):
        value='A';raw=bytes(v^255 for v in value.encode('utf-16-le'))
        csf=bytes(24)+b' LBL'+struct.pack('<II',1,4)+b'TEST'+b'WRTS'+struct.pack('<I',1)+raw+struct.pack('<I',3)+b'xyz'
        texts,digest,extras=parse_csf(csf,include_extras=True)
        self.assertEqual(texts,{'TEST':'A'});self.assertEqual(extras,{'TEST':b'xyz'})
        self.assertEqual(parse_csf(csf),(texts,digest))


@unittest.skipUnless(os.environ.get('VERA20K_GAMEMD_EXE'),'Requires explicit authenticated Steam install')
class PhysicalRetailSupplierTests(unittest.TestCase):
    @unittest.skipUnless(os.environ.get('VERA20K_FV_MOVEMENT_ASSETS'),
                         'Requires explicit physical Rules/Map inputs')
    def test_native_palette_activation_creates_or_retains_manager_and_reads_real_palette(self):
        from dataclasses import replace
        from tools.native_oracle import configured_gamemd,RET_MAGIC
        from tools.spatial_oracle.fv_cell_attack.steam_live_types import live_types_profile,LIVE_HEAP_BYTES
        from tools.spatial_oracle.fv_cell_attack.steam_movement_profile import (
            constructor_inputs,NATIVE_SCENARIO_BYTES)
        from tools.spatial_oracle.anytown_damage.navigation_inputs import Inputs
        from tools.projectile_oracle.bridge_render_inputs_palette import initialize,initialize_named_colors,PALETTE_ASSETS
        from tools.rules_oracle.bridge_anim_inputs import physical_sections
        from tools.rules_oracle.weapon_speed_order import construct_rules
        root=Path(os.environ['VERA20K_FV_MOVEMENT_ASSETS'])
        colors=physical_sections((root/'RULESMD.INI').read_bytes(),names=('Colors',))['Colors']
        self.assertTrue(colors,'Retained control requires an actual physical Colors entry')
        name,value=next(iter(colors.items()))
        # A single unchanged source entry exercises the original Colors owner;
        # this is a source-subset control, not full retail Colors chronology.
        profile=live_types_profile()
        # Original626966 proves ECX=manager, one name argument, native627590.
        # Only this additional invocation entry changes; code/data grants do not.
        profile=replace(profile,entries=profile.entries+((0x627590,(RET_MAGIC,)),))
        with tempfile.TemporaryDirectory(prefix='vera-native-palette-')as directory:
            layer=Path(directory)/'colors-subset.ini'
            layer.write_text('[Colors]\n'+name+'='+value+'\n',encoding='ascii')
            for retained in (False,True):
                with self.subTest(retained_manager=retained):
                    owner,_,_=constructor_inputs(profile=profile,heap_bytes=LIVE_HEAP_BYTES,
                        initial_counter=None,scenario_bytes=NATIVE_SCENARIO_BYTES,native_scenario=True,
                        construct_selected_type=False,initialize_options=True,initialize_physical=True,
                        ordered_cold_startup=True)
                    assets=PhysicalAssets(configured_gamemd().parent)
                    assets.attach(owner);ReadOnlyFiles(assets).attach(owner)
                    rules=construct_rules(owner,pointer=owner.alloc(0x18C0))
                    # Existing initializer accepts physical files. Stage the
                    # unchanged bytes from this VM's locked supplier, so the
                    # test needs no preexisting private extraction directory.
                    for palette_name in PALETTE_ASSETS:
                        blob,_=assets.read(palette_name)
                        self.assertIsNotNone(blob)
                        (Path(directory)/palette_name).write_bytes(blob)
                    initialize(owner,surface_service='rgb565-plain-cpu',
                               palette_root=Path(directory),inputs_only=True)
                    scene=owner.read32(0xA8B230);counter=owner.read32(scene+0x214)
                    rng={address:bytes(owner.u.mem_read(address,0x3F4))
                         for address in (0x886B88,scene+0x218,0xABE890)}
                    native_colors=initialize_named_colors(owner,rules,(layer,)if retained else ())
                    manager_before=owner.read32(0xAC48F0)
                    snapshots={}
                    if retained:
                        self.assertTrue(manager_before)
                        self.assertEqual(owner.read32(manager_before),0xFFFFFFFF)
                        # Original Colors may also construct a companion;
                        # preserve every actual record without supplying its count.
                        self.assertIn(name,[color['name']for color in native_colors['colors']])
                        snapshots[manager_before+4]=bytes(owner.u.mem_read(manager_before+4,12))
                        for offset in (4,8):
                            pointer=owner.read32(manager_before+offset)
                            snapshots[pointer]=bytes(owner.u.mem_read(pointer,24))
                        for color in native_colors['colors']:
                            snapshots[color['pointer']]=bytes(owner.u.mem_read(color['pointer'],0x33C))
                    else:self.assertEqual(manager_before,0)
                    binding=Inputs.read_map_theater(owner,root/'dragon-cadence.map',
                                                   ini_pointer=owner.alloc(0x58))
                    self.assertEqual(binding['value'],0)
                    mark=len(owner.allocation_events)
                    registration=initialize_live_theater_assets(owner,assets)
                    activation=registration['palette_activation'];manager=owner.read32(0xAC48F0)
                    self.assertEqual((activation['manager'],owner.read32(manager)),(manager,0))
                    self.assertEqual(activation['native_created'],not retained)
                    self.assertEqual(activation['bucket_entry_counts'],[0]*31)
                    self.assertEqual(activation['native_allocation_sizes'],[]if retained else [16,24,24,16,748])
                    self.assertEqual(len(owner.allocation_events)-mark,0 if retained else 5)
                    if retained:
                        self.assertEqual(manager,manager_before)
                        for address,blob in snapshots.items():
                            self.assertEqual(bytes(owner.u.mem_read(address,len(blob))),blob)
                    request_mark=len(assets.requests)
                    pointer=owner.invoke(0x627590,manager,(owner.cstring('lib'),))
                    self.assertTrue(0x24000000<=pointer<owner.heap_end)
                    requests=[row for row in assets.requests[request_mark:]if row['name']=='LIBTEM.PAL']
                    self.assertTrue(requests,'Original palette lookup must request the actual physical file')
                    self.assertTrue(all(not row['missing']and row['bytes']==768 and
                        row['sha256']=='79e668c9bd08bc5eed811df19de2af418cf8b434b97abf1fe2d65809321507e0'
                        for row in requests))
                    self.assertEqual(owner.read32(scene+0x214),counter)
                    for address,blob in rng.items():
                        self.assertEqual(bytes(owner.u.mem_read(address,len(blob))),blob)

    def test_theater_helper_authenticates_table_and_uses_existing_scenario_field(self):
        from tools.native_oracle import configured_gamemd,file_span
        from tools.spatial_oracle.fv_cell_attack.steam_bullet_startup_scope import STEAM_NATIVE_SHA256
        from tools.spatial_oracle.fv_cell_attack.steam_live_assets import THEATER_TABLE_ADDRESS,THEATER_TABLE_BYTES
        data=configured_gamemd().read_bytes();assets=PhysicalAssets(configured_gamemd().parent)
        owner=Mock();owner.asset_source=assets;owner.image.machine=owner.u
        owner.image.data=data;owner.image.profile.native_sha256=STEAM_NATIVE_SHA256
        table=file_span(data,THEATER_TABLE_ADDRESS,THEATER_TABLE_BYTES)[1]
        owner.u.mem_read.return_value=table
        owner.read32.side_effect=lambda address:{0xA8B230:0x24001000,0x24002258:2}[address]
        # Mocked Scenario words check the supplier protocol, not native execution.
        with patch('tools.spatial_oracle.fv_cell_attack.steam_live_assets._activate_live_palette_theater',
                   return_value=dict(boundary='Mocked protocol control; native activation not executed')):
            receipt=initialize_live_theater_assets(owner,assets)
        self.assertEqual((receipt['native_index'],receipt['name']),(2,'URBAN'))
        self.assertEqual(receipt['archive_order'],['URBAN.MIX','URB.MIX','ISOURBMD.MIX','ISOURB.MIX'])
        owner.u.mem_read.return_value=table[:-1]+bytes([table[-1]^1])
        with self.assertRaisesRegex(ValueError,'Mapped original theater table changed'):
            initialize_live_theater_assets(owner,assets)

    def test_original_csf_lookup_uses_native_sort_for_all_labels_and_missing_label(self):
        from unicorn.x86_const import UC_X86_REG_EDX,UC_X86_REG_ESP
        from tools.native_oracle import configured_gamemd,file_span
        from tools.spatial_oracle.fv_cell_attack.steam_live_types import live_types_profile,LIVE_HEAP_BYTES
        from tools.spatial_oracle.fv_cell_attack.steam_movement_profile import constructor_inputs,NATIVE_SCENARIO_BYTES
        from tools.spatial_oracle.fv_cell_attack.steam_live_assets import prepare_csf
        from tools.spatial_oracle.fv_cell_attack.steam_live_formatter_scope import (
            MISSING_LOOKUP_ENTRY,MISSING_LOOKUP_SOURCE_FILE,MISSING_LOOKUP_SOURCE_LINE)
        from tools.rules_oracle.bridge_anim_inputs import physical_sections
        from tools.spatial_oracle.building_body_rules import SP
        owner,_,_=constructor_inputs(profile=live_types_profile(),heap_bytes=LIVE_HEAP_BYTES,
            initial_counter=None,scenario_bytes=NATIVE_SCENARIO_BYTES,native_scenario=True,
            construct_selected_type=False,initialize_options=True,initialize_physical=True,ordered_cold_startup=True)
        assets=PhysicalAssets(configured_gamemd().parent)
        prepare_csf(owner,assets)
        entries,_,extras=parse_csf(assets.read('RA2MD.CSF',buffer=False)[0],include_extras=True)
        rules=Path(os.environ['VERA20K_FV_MOVEMENT_ASSETS'])/'RULESMD.INI'
        sections=physical_sections(rules.read_bytes(),names=None)
        missing=list(dict.fromkeys(values['UIName']for values in sections.values()
            if 'UIName'in values and values['UIName'].upper()not in entries))
        self.assertTrue(missing,'Control requires actually absent physical UIName labels')
        scene=owner.read32(0xA8B230);counter=owner.read32(scene+0x214)
        rng={address:bytes(owner.u.mem_read(address,0x3F4))for address in (0x886B88,scene+0x218,0xABE890)}
        extra_output=owner.alloc(4)
        for label in ('Name:Alliance',*entries,*missing):
            owner.u.reg_write(UC_X86_REG_EDX,extra_output)
            mark=len(owner.allocation_events)
            prior_missing_head=owner.read32(0xB1CF88)
            pointer=owner.invoke(MISSING_LOOKUP_ENTRY,owner.cstring(label),
                (MISSING_LOOKUP_SOURCE_FILE,MISSING_LOOKUP_SOURCE_LINE))
            self.assertEqual(owner.u.reg_read(UC_X86_REG_ESP),SP+12)
            if label in missing:
                pattern=file_span(owner.image.data,0x845820,28)[1].decode('utf-16-le').rstrip('\0')
                expected=pattern.replace('%hs',label)
                head=owner.read32(0xB1CF88)
                self.assertEqual(pointer,head+4)
                self.assertEqual(owner.read32(head),prior_missing_head)
                self.assertEqual(owner.allocation_events[-1]['size'],0x208)
                self.assertEqual(owner.read32(0xB78BA4),0)
                events=owner.u._vera20k_last_import_transports
                self.assertEqual([row['site']for row in events],[0x7D9D8B,0x7D9DD2]*len(label))
                self.assertTrue(all(row['arguments']==[0xB78BA4]for row in events))
            else:
                expected=entries[label.upper()]
                self.assertEqual(len(owner.allocation_events),mark) # Native lookup allocates nothing for a hit.
            self.assertEqual(bytes(owner.u.mem_read(pointer,len((expected+'\0').encode('utf-16-le')))),
                (expected+'\0').encode('utf-16-le'))
            extra=extras.get(label.upper())
            extra_pointer=owner.read32(extra_output)
            if extra is None:self.assertEqual(extra_pointer,0)
            else:self.assertEqual(bytes(owner.u.mem_read(extra_pointer,len(extra)+1)),extra+b'\0')
        self.assertEqual(owner.read32(scene+0x214),counter)
        self.assertTrue(all(bytes(owner.u.mem_read(address,0x3F4))==value for address,value in rng.items()))

    def test_selected_native_names_use_real_sources_and_missing_barrels(self):
        from tools.native_oracle import configured_gamemd
        assets=PhysicalAssets(configured_gamemd().parent)
        expected={'FV.VXL':(35583,'31e78a7559bbfb19a8e763550d17366e4e386d934c695188cd7336cef68a8f3e'),
                  'FV.HVA':(88,'16f3cd28642a66b1a0dc3f6cb4b063889c9f4721e46f12054fd60ed88cdc32ca'),
                  'RA2MD.CSF':(573269,'f3382231d7eb3bd713bf3908ecdba175a1b2e20d9d80fa2702e9ab84c3a79deb')}
        for name,(size,digest)in expected.items():
            blob,source=assets.read(name)
            self.assertEqual((len(blob),source['sha256']),(size,digest))
            cached,again=assets.read(name.lower())
            self.assertIs(blob,cached);self.assertEqual(source,again)
            self.assertTrue(assets.requests[-1]['cached'])
        for number in ('','1','2','3'):
            for extension in ('.VXL','.HVA'):
                blob,source=assets.read('FVBARL'+number+extension)
                self.assertIsNone(blob);self.assertTrue(source['missing'])
        self.assertIn('AUDIOMD.MIX',assets.manifest()['audio_pair']['audio.idx'])
        self.assertEqual(len(parse_csf(assets.read('RA2MD.CSF')[0])[0]),5211)


if __name__=='__main__':unittest.main()
