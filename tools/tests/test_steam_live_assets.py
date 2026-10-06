"""Immutable supplier/Win32 IO controls; native execution is a separate witness."""
import hashlib
import os
from pathlib import Path
import struct
import tempfile
import unittest
from unittest.mock import Mock,patch

from tools.sidebar_oracle.stock import mix, mix_hash, mix_index
from tools.spatial_oracle.fv_cell_attack.steam_live_assets import PhysicalAssets, ReadOnlyFiles, Span
from tools.storage_oracle.keyboard_bindings import parse_csf
from tools.rules_oracle.bridge_anim_inputs import Reader


class ImmutableSupplierTests(unittest.TestCase):
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
