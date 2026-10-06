"""Synthetic scoped runner failures, never retail behavioral evidence."""
from contextlib import contextmanager
from dataclasses import FrozenInstanceError, replace
import hashlib
import os
from pathlib import Path
import struct
import tempfile
import unittest
from unittest.mock import patch

from unicorn import Uc, UC_ARCH_X86, UC_MODE_32
from unicorn.x86_const import UC_X86_REG_EAX, UC_X86_REG_EIP, UC_X86_REG_ESP, UC_X86_REG_FPCW

from tools import native_oracle as oracle
from tools.input_oracle import fast_scroll
from tools.tests.pe_fixture import pe_image


class OleRunMeasurementGuardTests(unittest.TestCase):
    """Receipt admission/negative controls; no extra OS model or emulation."""
    def packet(self):
        import json
        return json.loads(Path('tools/spatial_oracle/fv_cell_attack/windows_olerun_functional_projection.json').read_text())

    def test_functional_native_receipt_and_matching_source_are_admitted(self):
        from tools.spatial_oracle.anytown_damage.mission import olerun_measurement, validate_olerun_packet, OLERUN_PACKET_SHA256, OLERUN_PROJECTION_SHA256
        packet=self.packet()
        self.assertEqual(packet['projection_of_packet_sha256'],OLERUN_PACKET_SHA256)
        source=Path('tools/spatial_oracle/fv_cell_attack/windows_olerun_probe.ps1').read_bytes()
        self.assertEqual(validate_olerun_packet(packet,hashlib.sha256(source).hexdigest())['hresult'],0)
        receipt=olerun_measurement()
        self.assertEqual(receipt['packet_sha256'],OLERUN_PACKET_SHA256)
        self.assertEqual(receipt['projection_sha256'],OLERUN_PROJECTION_SHA256)

    def test_public_projection_loader_rejects_modified_receipt(self):
        from tools.spatial_oracle.anytown_damage import mission
        root=Path('tools/spatial_oracle/fv_cell_attack')
        with tempfile.TemporaryDirectory() as directory:
            folder=Path(directory)/'fv_cell_attack'
            folder.mkdir()
            (folder/'windows_olerun_functional_projection.json').write_bytes(
                (root/'windows_olerun_functional_projection.json').read_bytes()+b' ')
            with patch.object(mission,'HERE',Path(directory)/'anytown_damage'):
                with self.assertRaisesRegex(ValueError,'packet identity'):
                    mission.olerun_measurement()

    def test_measurement_rejects_incompatible_source_architecture_or_effects(self):
        from tools.spatial_oracle.anytown_damage.mission import validate_olerun_packet, OLERUN_SCRIPT_SHA256
        mutations = [
            lambda p: p.update(script_sha256='0' * 64),
            lambda p: p.update(process_64bit=True),
            lambda p: p['measurement'].update(PointerBytes=8),
            lambda p: p['measurement']['Modules'][0].update(LoadedPeMachine='0x8664'),
            lambda p: p['measurement']['Modules'][0].update(ResolvedFilePath=r'C:\Windows\System32\combase.dll'),
            lambda p: p['measurement']['Measurements'][0].update(UnknownIdentityMatches=False),
            lambda p: p['measurement']['Measurements'][0].update(CallbackErrors=['callback failed']),
            lambda p: p['measurement']['Measurements'][0].update(ReferencesAfter=2),
            lambda p: p['measurement']['Measurements'][0].update(OleRunCalls=[]),
            lambda p: p['measurement']['Measurements'][0].update(OleRunHresult='0x80004002'),
            lambda p: p['execution'].update(child_exit_code=1),
            lambda p: p['measurement']['Measurements'][2].update(Control='STA-CoInitializeEx'),
            lambda p: p['measurement']['Measurements'][2].update(OleInitializeHresults=['0x00000000']),
            lambda p: p['measurement']['Measurements'][2].update(Apartment='MTA'),
        ]
        for index, mutate in enumerate(mutations):
            with self.subTest(index=index):
                packet = self.packet()
                mutate(packet)
                with self.assertRaises(ValueError):
                    validate_olerun_packet(packet, OLERUN_SCRIPT_SHA256)

    def test_transport_rejects_unqualified_object_class_or_refcount(self):
        from tools.spatial_oracle.anytown_damage.mission import nonrunnable_drive_olerun
        for base_vtable, interface_vtable, refs in ((0x7E7F7C, 0x7E7EB0, 2), (0, 0x7E7EB0, 1), (0x7E7F7C, 0, 1)):
            values = {0x1000: base_vtable, 0x1004: interface_vtable, 0x1014: refs}
            with self.assertRaises(ValueError):
                nonrunnable_drive_olerun(lambda p, n: struct.pack('<I', values[p]), 0x1004)

CODE = oracle.IMAGE_BASE + 0x1000
DATA = oracle.IMAGE_BASE + 0x3000
SINK = CODE + 0x100


class FullCpuContextTests(unittest.TestCase):
    """Real Unicorn controls for the retained caller guard, not retail parity."""

    def machine(self):
        from unicorn import x86_const as registers
        uc = Uc(UC_ARCH_X86, UC_MODE_32)
        uc.mem_map(CODE, 0x1000)
        uc.mem_map(DATA, 0x1000)
        uc.mem_write(CODE, bytes.fromhex('b8efbeadde83c00190'))
        values = {
            'EAX': 0x12345678, 'EBX': 0xfedcba98, 'ECX': 0x11223344,
            'EDX': 0x55667788, 'ESI': 0x99887766, 'EDI': 0x88776655,
            'EBP': 0x12348765, 'ESP': DATA+0x800, 'EIP': CODE+0x40,
            'EFLAGS': 0x246, 'FPCW': 0x0e7f, 'FPSW': 0x4500,
            'FIP': 0x12345678, 'FDP': 0xfedcba98, 'FOP': 0x345,
            'FCS': 0x23, 'FDS': 0x2b, 'MXCSR': 0x7fa0,
        }
        values.update({f'FP{i}': (0x8000000000000000+i, 0x3fff+i) for i in range(8)})
        values.update({f'YMM{i}': int.from_bytes(bytes([i+33])*32, 'little') for i in range(8)})
        for name, value in values.items():
            uc.reg_write(getattr(registers, 'UC_X86_REG_'+name), value)
        # Read x87 tags and XMM aliases too; storing a YMM seeds its XMM half.
        names = tuple(values) + ('FPTAG',) + tuple(f'XMM{i}' for i in range(8))
        readback = {name: uc.reg_read(getattr(registers, 'UC_X86_REG_'+name)) for name in names}
        return uc, readback

    def test_no_execution_and_repeated_observations_compare_every_byte(self):
        uc, _ = self.machine()
        saved = uc.context_save()
        expected = bytes(saved)
        # Keep independent allocations live; their unused header metadata is
        # deliberately NOT an equality oracle. The actual guard must compare
        # all CPU bytes without depending on allocator contents.
        independent = [uc.context_save() for _ in range(4)]
        for _ in range(4):
            result = oracle.compare_cpu_context(uc, saved)
            self.assertTrue(result['matches'])
            self.assertEqual(result['expected_context_hex'], expected.hex())
            self.assertEqual(result['observed_context_hex'], expected.hex())
            self.assertEqual(result['context_bytes'], len(expected))
            self.assertEqual(result['different_offsets'], [])
            self.assertEqual(bytes(saved), expected)
        self.assertTrue(all(context.size == saved.size for context in independent))

    def test_restore_preserves_full_x87_vectors_flags_and_original_snapshot(self):
        from unicorn import x86_const as registers
        uc, readback = self.machine()
        saved = uc.context_save()
        expected = bytes(saved)
        uc.reg_write(registers.UC_X86_REG_FP0, (0x923456789abcdef0, 0x4000))
        uc.reg_write(registers.UC_X86_REG_YMM0, 0)
        uc.emu_start(CODE, CODE+9)
        uc.context_restore(saved)
        result = oracle.compare_cpu_context(uc, saved)
        self.assertTrue(result['matches'])
        self.assertEqual(result['observed_context_hex'], expected.hex())
        self.assertEqual(bytes(saved), expected)
        for name, value in readback.items():
            with self.subTest(register=name):
                self.assertEqual(uc.reg_read(getattr(registers, 'UC_X86_REG_'+name)), value)
        # The observation clone never consumes or overwrites the restore owner.
        uc.reg_write(registers.UC_X86_REG_EAX, 0)
        uc.context_restore(saved)
        self.assertEqual(uc.reg_read(registers.UC_X86_REG_EAX), readback['EAX'])

    def test_register_corruption_is_rejected_without_guest_memory_rollback(self):
        from unicorn import x86_const as registers
        uc, _ = self.machine()
        saved = uc.context_save()
        expected = bytes(saved)
        controls = (
            ('EAX', 0), ('EFLAGS', 0x202), ('FP0', (0x9999999999999999, 0x4001)),
            ('YMM0', 0), ('XMM7', 0), ('FPCW', 0x027f), ('FPSW', 0),
            ('FPTAG', 0xffff), ('MXCSR', 0x1f80), ('FIP', 0), ('FDP', 0), ('FOP', 0),
        )
        for name, value in controls:
            with self.subTest(register=name):
                uc.context_restore(saved)
                uc.reg_write(getattr(registers, 'UC_X86_REG_'+name), value)
                uc.mem_write(DATA, name.encode().ljust(16, b'\0'))
                result = oracle.compare_cpu_context(uc, saved)
                self.assertFalse(result['matches'])
                self.assertTrue(result['different_offsets'])
                self.assertEqual(result['expected_context_hex'], expected.hex())
                self.assertEqual(bytes(saved), expected)
                self.assertEqual(bytes(uc.mem_read(DATA, 16)), name.encode().ljust(16, b'\0'))


class IniCacheRetentionTests(unittest.TestCase):
    """Real guest-memory guard controls, not native parser or CRC parity.

    Scalar/cache behavior is established by the original-reader controls.
    These checks corrupt prepared memory and exercise the shared cache owner.
    Synthetic CRC inputs avoid requiring a licensed binary for guard tests.
    """

    def reader(self):
        from types import SimpleNamespace
        from tools.rules_oracle.bridge_anim_inputs import Reader
        from tools.rules_oracle.bridge_anim_lists import HEAP
        from tools.spatial_oracle.building_body_rules import INI
        reader = Reader.__new__(Reader)
        reader.u = Uc(UC_ARCH_X86, UC_MODE_32)
        reader.u.mem_map(HEAP, 0x10000)
        reader.u.mem_map(INI & ~0xfff, 0x1000)
        reader.image = None
        reader.cursor, reader.heap_end = HEAP+0x1000, HEAP+0x10000
        reader.f = SimpleNamespace(fixture_write=reader.u.mem_write)
        root = reader.alloc(0x58)
        with patch('tools.rules_oracle.bridge_anim_inputs.crc', side_effect=range(1, 20)):
            reader.make_ini({'Art': {'Value': '73'}}, pointer=INI)
            reader.make_ini({'First': {'Value': '37', 'Other': '91'}, 'Second': {'Value': '12'}}, pointer=root)
        return reader, root, INI

    def test_native_cache_words_preserve_content_and_are_independently_owned(self):
        from tools.spatial_oracle.building_body_rules import dwords
        reader, root, art = self.reader()
        before, art_before = reader.ini_cache_snapshot(root), reader.ini_cache_snapshot(art)
        first, second = before['sections']
        reader.fixture_write(root+4, dwords(reader.read32(first['pointer']+0xC), first['pointer']))
        other_row = next(before['index_pointer']+i*8 for i in range(before['index_count'])
                         if reader.read32(before['index_pointer']+i*8+4) == second['pointer'])
        reader.fixture_write(root+0x38, dwords(other_row))
        reader.fixture_write(first['pointer']+0x3C, dwords(first['index_pointer']+8))
        after = reader.ini_cache_snapshot(root)
        self.assertNotEqual(before['header_hex'], after['header_hex'])
        self.assertEqual(before['immutable_sha256'], after['immutable_sha256'])
        self.assertNotEqual(reader.read32(after['section_index_cache_pointer']+4), after['last_section_pointer'])
        self.assertTrue(after['cache_pointer_membership_valid'])
        self.assertEqual(reader.ini_cache_snapshot(art), art_before)

    def test_index_strings_nodes_and_structural_pointer_corruption_are_detected(self):
        reader, root, _ = self.reader()
        before = reader.ini_cache_snapshot(root)
        section = before['sections'][0]
        entry = reader.read32(section['index_pointer']+4)
        cases = {
            'root_index': before['index_pointer'],
            'key_index': section['index_pointer'],
            'entry_node': entry,
            'key_string': reader.read32(entry+0xC),
            'value_string': reader.read32(entry+0x10),
            'section_name': reader.read32(section['pointer']+0xC),
            'root_index_pointer': root+0x28,
            'section_index_pointer': section['pointer']+0x2C,
        }
        for label, address in cases.items():
            with self.subTest(corruption=label):
                original = bytes(reader.u.mem_read(address, 1))
                reader.fixture_write(address, bytes([original[0] ^ 1]))
                self.assertNotEqual(reader.ini_cache_snapshot(root)['immutable_sha256'], before['immutable_sha256'])
                reader.fixture_write(address, original)
                self.assertEqual(reader.ini_cache_snapshot(root)['immutable_sha256'], before['immutable_sha256'])

    def test_foreign_misaligned_and_unmapped_cache_pointers_are_rejected(self):
        from unicorn import UcError
        from tools.spatial_oracle.building_body_rules import dwords
        reader, root, art = self.reader()
        state, foreign = reader.ini_cache_snapshot(root), reader.ini_cache_snapshot(art)
        section = state['sections'][0]
        name = reader.read32(section['pointer']+0xC)
        cases = (
            (root+4, dwords(name, foreign['sections'][0]['pointer'])),
            (root+4, dwords(0, section['pointer'])),
            (root+4, dwords(0xdeadbeef, section['pointer'])),
            (root+0x38, dwords(foreign['index_pointer'])),
            (root+0x38, dwords(state['index_pointer']+1)),
            (section['pointer']+0x3C, dwords(state['sections'][1]['index_pointer'])),
            (section['pointer']+0x3C, dwords(section['index_pointer']+1)),
        )
        for address, value in cases:
            with self.subTest(address=address, value=value.hex()):
                original = bytes(reader.u.mem_read(address, len(value)))
                reader.fixture_write(address, value)
                with self.assertRaises((ValueError, UcError)):
                    reader.ini_cache_snapshot(root)
                reader.fixture_write(address, original)

    def test_repreparing_receiver_replaces_derived_layout_and_preserves_other_receiver(self):
        from tools.spatial_oracle.building_body_rules import dwords
        reader, root, art = self.reader()
        before, art_before = reader.ini_cache_snapshot(root), reader.ini_cache_snapshot(art)
        with patch('tools.rules_oracle.bridge_anim_inputs.crc', side_effect=range(30, 40)):
            reader.make_ini({'Replacement': {'Value': 'new'}}, pointer=root)
        after = reader.ini_cache_snapshot(root)
        self.assertEqual(after['index_count'], 1)
        self.assertEqual(after['sections'][0]['name'], 'Replacement')
        self.assertEqual(after['last_section_pointer'], 0)
        self.assertEqual(reader.ini_cache_snapshot(art), art_before)
        reader.fixture_write(root+0x38, dwords(before['index_pointer']))
        with self.assertRaises(ValueError):
            reader.ini_cache_snapshot(root)


class RetainedDialogFormatterTests(unittest.TestCase):
    """Synthetic formatting controls; runtime CPU guards have real UC tests."""
    def packet(self):
        from tools.spatial_oracle.fv_cell_attack.steam_movement_profile import DIALOG_READER_FIELDS
        comparison=dict(matches=True,arch=UC_ARCH_X86,mode=UC_MODE_32,context_bytes=32,
            expected_context_hex=bytes(32).hex(),observed_context_hex=bytes(32).hex(),
            different_offsets=[],method='full bytes on inspection clone',saved_restore_snapshot_unchanged=True)
        reads=[];fields=[]
        for key,offset,width,key_pointer,site in DIALOG_READER_FIELDS:
            reads.append(dict(key=key,site=site,field_offset=offset,width=width,key_pointer=key_pointer,
                ini_receiver=0x24000000,section_pointer=0x83079C,section='MultiplayerDialogSettings',
                default_argument_raw=0,retained_default_hex=bytes(width).hex()))
            fields.append(dict(key=key,offset=offset,width=width,default_hex=bytes(width).hex(),after_hex=bytes(width).hex()))
        return dict(source_sha256='a'*64,counter_after=7,rng_after=dict(main='00'),
            original_prefix_frame_hex='abcd',
            boundary_observation=dict(observational_lookup_cpu_context=comparison),
            observational_lookup=dict(full_cpu_context_comparison=comparison),
            retained_suffix=dict(inherited_cpu_context_hex=bytes(32).hex()),
            retained_dialog=dict(inherited_cpu_context_hex=bytes(32).hex(),
                constructor=dict(entry=0x665650,receiver=0x24000100,fields_hex=bytes(0x3C).hex()),
                begin=0x668EBD,end=0x668EC5,reader=0x671EA0,section='MultiplayerDialogSettings',
                reader_before_hex=bytes(0x3C).hex(),reader_after_hex=bytes(0x3C).hex(),
                physical_keys={'GameSpeed':'1'},reads=reads,reader_fields=fields,
                lexical_cache_after=dict(rules=dict(header_hex='abcd',immutable_sha256='b'*64)),
                excluded='Accepted Session settings are a separate owner.'))

    def test_allocation_header_only_variation_keeps_reference_and_original_raw(self):
        from copy import deepcopy
        from tools.spatial_oracle.fv_cell_attack.steam_movement_profile import retained_dialog_reference
        raw=self.packet();before=deepcopy(raw);changed=deepcopy(raw)
        # Offset24 lies in Unicorn2.1.4's host last_block allocation header.
        varied=(bytes(24)+b'\x12\x34\x56'+bytes(5)).hex()
        for key in ('expected_context_hex','observed_context_hex'):
            changed['boundary_observation']['observational_lookup_cpu_context'][key]=varied
        for key in ('retained_suffix','retained_dialog'):changed[key]['inherited_cpu_context_hex']=varied
        self.assertEqual(retained_dialog_reference(raw),retained_dialog_reference(changed))
        self.assertEqual(raw,before)
        self.assertIs(raw['boundary_observation']['observational_lookup_cpu_context'],raw['observational_lookup']['full_cpu_context_comparison'])
        self.assertNotEqual(oracle._canonical(raw),oracle._canonical(changed))
        summary=retained_dialog_reference(raw)['observational_lookup']['full_cpu_context_comparison']
        self.assertTrue(summary['matches']);self.assertEqual(summary['different_offsets'],[])

    def test_reader_rng_frame_cache_and_guard_mutations_remain_compared(self):
        from copy import deepcopy
        from tools.spatial_oracle.fv_cell_attack.steam_movement_profile import retained_dialog_reference
        raw=self.packet();reference=retained_dialog_reference(raw)
        mutations=[lambda p:p['retained_dialog']['reader_fields'][8].update(after_hex='06000000'),
            lambda p:p['retained_dialog'].update(reader_before_hex='01'+bytes(0x3B).hex()),
            lambda p:p['retained_dialog']['constructor'].update(fields_hex='01'+bytes(0x3B).hex()),
            lambda p:p['rng_after'].update(main='01'),lambda p:p.update(counter_after=8),
            lambda p:p.update(original_prefix_frame_hex='abce'),
            lambda p:p['retained_dialog']['lexical_cache_after']['rules'].update(immutable_sha256='c'*64),
            lambda p:p['retained_dialog']['lexical_cache_after']['rules'].update(header_hex='abce'),
            lambda p:p['retained_dialog']['reads'][0].update(default_argument_raw=1),
            lambda p:p['retained_dialog']['physical_keys'].update(GameSpeed='6'),
            lambda p:p['boundary_observation']['observational_lookup_cpu_context'].update(matches=False,different_offsets=[32])]
        for index,mutate in enumerate(mutations):
            with self.subTest(index=index):
                changed=deepcopy(raw);mutate(changed)
                self.assertIsNotNone(oracle.first_difference(reference,retained_dialog_reference(changed)))

    def test_raw_sidecars_are_unique_complete_and_bind_semantic_native_sources(self):
        import json
        from tools.spatial_oracle.fv_cell_attack.steam_movement_profile import retained_dialog_reference,retain_dialog_execution
        raw=self.packet();reference=retained_dialog_reference(raw)
        identity=dict(native_sha256='c'*64);sources={'driver':'d'*64}
        with tempfile.TemporaryDirectory() as directory:
            with patch('builtins.print'):
                first=retain_dialog_execution(raw,reference,native_identity=identity,source_identity=sources,directory=directory)
                prior=first.read_bytes()
                second=retain_dialog_execution(raw,reference,native_identity=identity,source_identity=sources,directory=directory)
            self.assertNotEqual(first,second);self.assertEqual(first.read_bytes(),prior)
            packet=json.loads(prior)
            self.assertEqual(packet['raw_receipt'],raw)
            self.assertEqual(packet['raw_receipt_sha256'],hashlib.sha256(oracle._canonical(raw)).hexdigest())
            self.assertEqual(packet['semantic_payload_sha256'],hashlib.sha256(oracle._canonical(reference)).hexdigest())
            self.assertEqual(packet['native_identity'],identity);self.assertEqual(packet['source_normalized_lf_sha256'],sources)
            self.assertNotIn(str(first),json.dumps(reference));self.assertNotIn(hashlib.sha256(prior).hexdigest(),json.dumps(reference))

    def test_strict_vector_check_accepts_new_raw_allocation_and_rejects_guest_mutation(self):
        from copy import deepcopy
        from tools.spatial_oracle.fv_cell_attack.steam_movement_profile import retained_dialog_reference,retain_dialog_execution
        raw=self.packet();reference=retained_dialog_reference(raw)
        metadata=dict(native_sha256='c'*64,scope='Synthetic formatter control')
        with tempfile.TemporaryDirectory() as directory,patch('builtins.print'):
            target=Path(directory)/'reference.json'
            oracle.finish_vectors(reference,target,provenance=metadata,argv=['--write'])
            changed=deepcopy(raw)
            for key in ('expected_context_hex','observed_context_hex'):
                changed['boundary_observation']['observational_lookup_cpu_context'][key]=(bytes(24)+bytes([3])+bytes(7)).hex()
            semantic=retained_dialog_reference(changed)
            retain_dialog_execution(changed,semantic,native_identity=metadata,source_identity={},directory=directory)
            oracle.finish_vectors(semantic,target,provenance=metadata,argv=['--check'])
            changed['retained_dialog']['reader_fields'][8]['after_hex']='06000000'
            with self.assertRaisesRegex(oracle.OracleError,'reader_fields'):
                oracle.finish_vectors(retained_dialog_reference(changed),target,provenance=metadata,argv=['--check'])

    def test_compact_artifact_extracts_all_calls_and_cannot_change_field_identity(self):
        from tools.spatial_oracle.fv_cell_attack.steam_movement_profile import retained_dialog_reference,retained_dialog_reader_reference
        reference=retained_dialog_reference(self.packet());identity=dict(native_sha256='c'*64);sources={'driver':'d'*64}
        compact=retained_dialog_reader_reference(reference,native_identity=identity,source_identity=sources)
        self.assertEqual(len(compact['reader_fields']),27);self.assertEqual(compact['reads'],reference['retained_dialog']['reads'])
        self.assertEqual(compact['physical_rules_sha256'],reference['source_sha256'])
        self.assertEqual(compact['source_normalized_lf_sha256'],sources)
        self.assertEqual(compact['semantic_payload_sha256'],hashlib.sha256(oracle._canonical(reference)).hexdigest())
        self.assertTrue(all(field['constructor_hex']==field['default_hex']for field in compact['reader_fields']))
        reference['retained_dialog']['reads'][0]['key_pointer']+=1
        with self.assertRaisesRegex(ValueError,'field/call identity'):retained_dialog_reader_reference(reference,native_identity=identity,source_identity=sources)

    def test_incomplete_raw_blobs_fail_and_historical_selectors_keep_raw_payload(self):
        from tools.spatial_oracle.fv_cell_attack import steam_movement_profile as driver
        raw=self.packet();del raw['retained_suffix']['inherited_cpu_context_hex']
        with self.assertRaises(KeyError):driver.retained_dialog_reference(raw)
        for retained in (False,True):
            raw=self.packet()
            with patch.dict(os.environ,VERA20K_FV_MOVEMENT_ASSETS='/synthetic'),patch.object(driver,'typed_master_inputs',return_value=(None,None,None,raw)),patch.object(driver,'retain_dialog_execution') as save:
                self.assertIs(driver.generate_typed_master(retained_startup=retained),raw)
                save.assert_not_called()

    def test_companion_output_cannot_overwrite_full_reference(self):
        from tools.spatial_oracle.fv_cell_attack.steam_movement_profile import retained_dialog_companion_argv
        for argv in (['--write','--output','/tmp/custom.json'],['--check','--output=/tmp/custom.json']):
            result,path=retained_dialog_companion_argv(argv,Path('default.json'))
            self.assertEqual(path,Path('/tmp/custom_reader.json'))
            self.assertNotEqual(result,argv);self.assertNotIn('/tmp/custom.json',result)

    def test_companion_rejects_drift_since_generation_inside_strict_lazy_supplier(self):
        from functools import partial
        from tools.spatial_oracle.fv_cell_attack.steam_movement_profile import retained_dialog_reader_vectors
        with tempfile.TemporaryDirectory() as directory,patch('builtins.print'):
            source=Path(directory)/'driver.py';source.write_text('original\n')
            paths={'driver':source};reader=dict(source_normalized_lf_sha256=oracle.source_identity(paths))
            supplier=partial(retained_dialog_reader_vectors,reader,source_paths=paths)
            target=Path(directory)/'reader.json'
            oracle.finish_vectors(supplier,target,provenance={},source_paths=paths,argv=['--write'])
            prior=target.read_bytes();source.write_text('changed\n')
            with self.assertRaisesRegex(oracle.OracleError,'since retained dialog generation'):
                oracle.finish_vectors(supplier,target,provenance={},source_paths=paths,argv=['--write'])
            self.assertEqual(target.read_bytes(),prior)

    def test_shared_source_identity_keeps_original_utf8_lf_semantics(self):
        with tempfile.TemporaryDirectory() as directory:
            source=Path(directory)/'source.py';source.write_bytes('café\r\nnext\rlast\n'.encode('utf-8'))
            expected=hashlib.sha256('café\nnext\nlast\n'.encode('utf-8')).hexdigest()
            self.assertEqual(oracle.source_identity({'name':source}),{'name':expected})
            self.assertEqual(oracle.source_identity(),{})
            with self.assertRaises(FileNotFoundError):oracle.source_identity({'missing':source.with_name('absent')})


class LegacyConstructorTests(unittest.TestCase):
    def test_timegettime_checked_transport_is_bounded_and_requires_exact_consumption(self):
        class Call:
            spec=oracle.ImportTransport(0x6C8C40,0x7E1530,0)
            arguments=()
            def return_to_native(self,value):self.result=value
        for value in (0,0xFFFFFFFF):
            service=fast_scroll.ThrottleServices(dict(frame_clock=[value],millisecond_clock=[]))
            call=Call();service.import_transport(call);service.require_consumed()
            self.assertEqual(call.result,value)
            self.assertEqual(service.clock_reads,[dict(reader='0x6c8c40',wall_ms=value)])
            with self.assertRaisesRegex(RuntimeError,'extra timeGetTime'):service.import_transport(call)
        for value in (-1,0x100000000,True,0.5):
            with self.subTest(value=value):
                service=fast_scroll.ThrottleServices(dict(frame_clock=[value],millisecond_clock=[]))
                with self.assertRaisesRegex(ValueError,'DWORD'):service.import_transport(Call())
        service=fast_scroll.ThrottleServices(dict(frame_clock=[1],millisecond_clock=[]))
        wrong=Call();wrong.spec=replace(wrong.spec,iat=0x7E1534)
        with self.assertRaisesRegex(ValueError,'Unsupported'):service.import_transport(wrong)
        with self.assertRaisesRegex(RuntimeError,'unused'):service.require_consumed()

    def test_drag_constructor_supplies_original_two_argument_x87_initialization(self):
        """Real register API, mocked PE/startup; this is no retail parity claim."""
        def map_fixture(uc):
            uc.mem_map(oracle.IMAGE_BASE, oracle.IMAGE_SIZE)

        def startup(uc, start, end, **kwargs):
            self.assertEqual((start, end), (0x006BBFB7, 0x006BBFCE))
            self.assertEqual(kwargs, dict(count=1000, required_addresses=[0x007CBF49, 0x007C5EE4]))
            self.assertEqual(uc.reg_read(UC_X86_REG_FPCW), 0x027F)
            uc.reg_write(UC_X86_REG_FPCW, 0x0E3F)
            uc.mem_write(0x00822D80, struct.pack('<I', 0x0E3F))

        with patch.object(fast_scroll, 'load_image', side_effect=map_fixture), \
                patch.object(fast_scroll, 'run_checked', side_effect=startup) as run:
            fixture = fast_scroll.DragFixture(fast_scroll.inputs('constructor_tooling_regression'))
        run.assert_called_once()
        self.assertEqual(fixture.machine.reg_read(UC_X86_REG_FPCW), 0x0E3F)
        self.assertEqual(fast_scroll.u32(fixture.machine, fast_scroll.DISPLAY), fast_scroll.VTABLE)


@contextmanager
def machine(code, *, region_bytes=None, reads=(), writes=(), sinks=(), transports=(), end=None):
    data = pe_image([(0x1000, 0x200, code, 0x1000, 0x60000020),
                     (0x3000, 0x400, b'\x11' * 32, 0x1000, 0xC0000040)])
    length = len(code) if region_bytes is None else region_bytes
    profile = oracle.ExecutionProfile(
        name='synthetic-test-only', native_sha256=hashlib.sha256(data).hexdigest(),
        regions=((CODE, CODE + length, hashlib.sha256(code[:length]).hexdigest()),),
        entries=((CODE, (end or CODE + len(code),)),),
        reads=((oracle.STACK_BASE, oracle.STACK_SIZE),) + reads,
        writes=((oracle.STACK_BASE, oracle.STACK_SIZE),) + writes,
        fixture_writes=((oracle.STACK_BASE, oracle.STACK_SIZE), (DATA, 32)), sinks=sinks, transports=transports)
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / 'synthetic.exe'
        path.write_bytes(data)
        with patch.dict(os.environ, VERA20K_GAMEMD_EXE=str(path)):
            uc = Uc(UC_ARCH_X86, UC_MODE_32)
            image = oracle.load_image(uc, profile=profile)
            uc.mem_map(oracle.STACK_BASE, oracle.STACK_SIZE)
            uc.reg_write(UC_X86_REG_ESP, oracle.STACK_BASE + 0x1000)
            yield uc, image


class ScopedExecutionTests(unittest.TestCase):
    def setUp(self):
        environment = patch.dict(os.environ)
        environment.start()
        os.environ.pop('VERA20K_NATIVE_FAILURE_DIR', None)
        self.addCleanup(environment.stop)

    def run_scope(self, uc, image, **kwargs):
        return oracle.run_checked(uc, CODE, image.profile.entries[0][1][0], image=image, **kwargs)

    def rejected(self, uc, image, kind, **kwargs):
        with self.assertRaises(oracle.NativeExecutionError) as caught:
            self.run_scope(uc, image, **kwargs)
        report = caught.exception.diagnostics
        self.assertEqual(report['reason'], 'profile_violation')
        self.assertEqual(report['profile_violation']['kind'], kind)
        self.assertEqual(report['expected_native_sha256'], image.profile.native_sha256)
        self.assertEqual(report['profile']['name'], 'synthetic-test-only')
        self.assertIn('trace', report)

    def test_scoped_success_preserves_default_fail_closed_identity(self):
        with machine(b'\xb8\x2a\0\0\0') as (uc, image):
            self.run_scope(uc, image)
            self.assertEqual(uc.reg_read(UC_X86_REG_EAX), 42)
            with self.assertRaisesRegex(oracle.OracleError, 'Unsupported gamemd'):
                oracle.image_bytes()
            with self.assertRaisesRegex(oracle.OracleError, 'Unsupported gamemd'):
                oracle.load_image(Uc(UC_ARCH_X86, UC_MODE_32))

    def test_fresh_call_preserves_scoped_entry_and_fixture_guards(self):
        code = b'\x8b\x44\x24\x04\x40\xc2\x04\x00'
        with machine(code) as (_, image):
            profile = replace(image.profile, entries=((CODE, (oracle.RET_MAGIC,)),))
            self.assertEqual(oracle.call(CODE, stack_args=[41], profile=profile)['eax'], 42)
            with self.assertRaisesRegex(oracle.OracleError, 'Unsupported gamemd'):
                oracle.call(CODE, stack_args=[41])
            with self.assertRaisesRegex(oracle.OracleError, 'undeclared fixture'):
                oracle.call(CODE, profile=profile, writes={DATA + 32: b'\0'})
            with self.assertRaisesRegex(oracle.OracleError, 'cannot replace native'):
                oracle.call(CODE, profile=profile, writes={CODE: b'\xcc'})
            with self.assertRaisesRegex(oracle.OracleError, 'external ST0'):
                oracle.call(CODE, profile=profile, capture_st0=True)

    def test_crc_legacy_cache_cannot_skip_default_identity_gate(self):
        from tools.projectile_oracle import flat_art
        flat_art._legacy_crc.cache_clear()
        self.addCleanup(flat_art._legacy_crc.cache_clear)
        with patch.object(flat_art, 'image_bytes', return_value=b'authenticated'), \
                patch.object(flat_art, 'call', return_value={'eax': 42}) as call:
            self.assertEqual(flat_art.crc('FV'), 42)
            self.assertEqual(flat_art.crc('FV'), 42)
            call.assert_called_once()
        with patch.object(flat_art, 'image_bytes', side_effect=oracle.OracleError('Unsupported gamemd')):
            with self.assertRaisesRegex(oracle.OracleError, 'Unsupported gamemd'):
                flat_art.crc('FV')

    def test_scoped_crc_uses_fresh_qualified_call_on_every_request(self):
        from tools.projectile_oracle import flat_art
        with machine(b'\x90') as (_, image):
            with patch.object(flat_art, 'call', return_value={'eax': 42}) as call:
                self.assertEqual(flat_art.crc('FV', profile=image.profile), 42)
                self.assertEqual(flat_art.crc('FV', profile=image.profile), 42)
            self.assertEqual(call.call_count, 2)
            self.assertTrue(all(row.kwargs['profile'] is image.profile for row in call.call_args_list))

    def test_omitted_or_wrong_image_handle_cannot_run_scoped_machine(self):
        with machine(b'\x90') as (uc, image):
            image._original_bytes(CODE, 1)
            with self.assertRaisesRegex(oracle.OracleError, 'matching image handle'):
                oracle.run_checked(uc, CODE, CODE + 1)
            with self.assertRaisesRegex(oracle.OracleError, 'matching image handle'):
                oracle.run_checked(uc, CODE, CODE + 1, image=replace(image))

    def test_raw_execution_is_blocked_before_native_instruction(self):
        with machine(b'\xb8\x2a\0\0\0') as (uc, image):
            with self.assertRaisesRegex(oracle.OracleError, 'guarded run_checked'):
                uc.emu_start(CODE, CODE + 5)
            self.assertEqual(uc.reg_read(UC_X86_REG_EAX), 0)
            self.run_scope(uc, image)

    def test_instruction_straddling_region_end_is_rejected(self):
        with machine(b'\xb8\x2a\0\0\0', region_bytes=3) as (uc, image):
            # Cached authentic bytes do not grant execution across a region end.
            image._original_bytes(CODE, 5)
            self.rejected(uc, image, 'undeclared_instruction')
            self.assertEqual(uc.reg_read(UC_X86_REG_EAX), 0)

    def test_jump_to_unqualified_instruction_is_rejected(self):
        code = b'\xe9' + struct.pack('<i', SINK - (CODE + 5))
        with machine(code) as (uc, image):
            self.rejected(uc, image, 'undeclared_instruction')

    def test_undeclared_read_and_straddling_data_read_are_rejected(self):
        code = b'\xa1' + struct.pack('<I', DATA)
        for reads in [(), ((DATA, 3),)]:
            with self.subTest(reads=reads), machine(code, reads=reads) as (uc, image):
                self.rejected(uc, image, 'undeclared_read')

    def test_declared_read_is_original_instruction_output(self):
        code = b'\xa1' + struct.pack('<I', DATA)
        with machine(code, reads=((DATA, 4),)) as (uc, image):
            self.run_scope(uc, image)
            self.assertEqual(uc.reg_read(UC_X86_REG_EAX), 0x11111111)

    def test_undeclared_guest_write_is_rejected(self):
        code = b'\xc6\x05' + struct.pack('<I', DATA) + b'\x2a'
        with machine(code) as (uc, image):
            self.rejected(uc, image, 'undeclared_write')

    def test_guest_native_code_write_is_rejected_even_if_range_declared(self):
        code = b'\xc6\x05' + struct.pack('<I', CODE) + b'\x90'
        with machine(code, writes=((CODE, 1),)) as (uc, image):
            self.rejected(uc, image, 'native_code_write')

    def test_fixture_write_cannot_modify_original_code_or_undeclared_data(self):
        with machine(b'\x90') as (uc, image):
            with self.assertRaisesRegex(oracle.OracleError, 'cannot replace native'):
                image.write(CODE, b'\xcc')
            with self.assertRaisesRegex(oracle.OracleError, 'undeclared fixture'):
                image.write(DATA + 32, b'\xcc')
            image.write(DATA, b'\x2a')
            self.assertEqual(bytes(uc.mem_read(DATA, 1)), b'\x2a')

    def test_direct_host_patch_to_qualified_code_is_detected_before_run(self):
        with machine(b'\x90') as (uc, image):
            uc.mem_write(CODE, b'\xcc')
            with self.assertRaisesRegex(oracle.OracleError, 'code changed'):
                self.run_scope(uc, image)

    def test_nonexecuting_endpoint_cannot_write_data(self):
        code = b'\xb8\x2a\0\0\0\xc6\x05' + struct.pack('<I', DATA) + b'\x2a'
        with machine(code, end=CODE + 5, writes=((DATA, 1),)) as (uc, image):
            self.run_scope(uc, image)
            self.assertEqual(bytes(uc.mem_read(DATA, 1)), b'\x11')

    def test_undeclared_entry_or_endpoint_is_rejected(self):
        with machine(b'\x90\x90') as (uc, image):
            for begin, end in [(CODE + 1, CODE + 2), (CODE, CODE + 1)]:
                with self.subTest(begin=begin, end=end), self.assertRaisesRegex(oracle.OracleError, 'entry/endpoint'):
                    oracle.run_checked(uc, begin, end, image=image)

    def test_sink_handler_must_exist_and_redirect_before_instruction(self):
        code = b'\xe8' + struct.pack('<i', SINK - (CODE + 5)) + b'\x90'
        with machine(code, sinks=((SINK, 0),)) as (uc, image):
            self.rejected(uc, image, 'missing_sink')
        with machine(code, sinks=((SINK, 0),)) as (uc, image):
            self.rejected(uc, image, 'sink_abi', sinks={SINK: lambda _: None})
        with machine(code, sinks=((SINK, 0),)) as (uc, image):
            def callback(machine):
                sp = machine.reg_read(UC_X86_REG_ESP)
                target = struct.unpack('<I', machine.mem_read(sp, 4))[0]
                machine.reg_write(UC_X86_REG_ESP, sp + 4)
                machine.reg_write(UC_X86_REG_EIP, target)
                machine.reg_write(UC_X86_REG_EAX, 42)
            self.run_scope(uc, image, sinks={SINK: callback})
            self.assertEqual(uc.reg_read(UC_X86_REG_EAX), 42)
            with self.assertRaisesRegex(oracle.OracleError, 'not original instruction coverage'):
                self.run_scope(uc, image, sinks={SINK: callback}, required_addresses=[SINK])

    def test_sink_cannot_patch_next_native_instruction_during_run(self):
        code = b'\xe8' + struct.pack('<i', SINK - (CODE + 5)) + b'\x90'
        with machine(code, sinks=((SINK, 0),)) as (uc, image):
            self.assertEqual(image._original_bytes(CODE + 5, 1), b'\x90')
            def callback(machine):
                sp = machine.reg_read(UC_X86_REG_ESP)
                target = struct.unpack('<I', machine.mem_read(sp, 4))[0]
                machine.mem_write(CODE + 5, b'\xcc')
                machine.reg_write(UC_X86_REG_ESP, sp + 4)
                machine.reg_write(UC_X86_REG_EIP, target)
            self.rejected(uc, image, 'native_code_changed', sinks={SINK: callback})

    def test_original_byte_cache_retains_file_span_rejections(self):
        with machine(b'\x90') as (_, image):
            with patch.object(oracle, 'file_span', wraps=oracle.file_span) as extract:
                self.assertEqual(image._original_bytes(CODE, 1), b'\x90')
                self.assertEqual(image._original_bytes(CODE, 1), b'\x90')
                self.assertEqual(extract.call_count, 1)
                for _ in range(2):
                    with self.assertRaisesRegex(oracle.OracleError, 'file-backed section'):
                        image._original_bytes(CODE + 1, 1)
                self.assertEqual(extract.call_count, 3)
                self.assertNotIn((CODE + 1, 1), image._original_byte_cache)

    def test_original_byte_cache_is_owned_by_each_image_and_machine(self):
        with machine(b'\x90') as (_, first), machine(b'\x91') as (_, second):
            self.assertIsNot(first._original_byte_cache, second._original_byte_cache)
            self.assertEqual(first._original_bytes(CODE, 1), b'\x90')
            self.assertEqual(second._original_byte_cache, {})
            self.assertEqual(second._original_bytes(CODE, 1), b'\x91')
            self.assertEqual(first._original_bytes(CODE, 1), b'\x90')

    def test_import_transport_is_guarded_before_original_call_and_not_coverage(self):
        code=b'\xff\x15'+struct.pack('<I',DATA)+b'\x40'
        spec=oracle.ImportTransport(CODE,DATA,4)
        with machine(code,reads=((DATA,4),),transports=(spec,))as(uc,image):
            self.rejected(uc,image,'missing_transport')
            def callback(call):
                self.assertEqual(call.arguments,(0,))
                call.return_to_native(41)
            self.run_scope(uc,image,transports={CODE:callback})
            self.assertEqual(uc.reg_read(UC_X86_REG_EAX),42)
            self.assertEqual(uc._vera20k_last_import_transports[0]['original_instruction_executed'],False)
            with self.assertRaisesRegex(oracle.OracleError,'not original instruction coverage'):
                self.run_scope(uc,image,transports={CODE:callback},required_addresses=[CODE])

    def test_import_transport_declarations_reject_wrong_bytes_iat_and_straddles(self):
        code=b'\xff\x15'+struct.pack('<I',DATA)
        cases=((b'\x90'*6,oracle.ImportTransport(CODE,DATA,4),6,'FF15'),
               (code,oracle.ImportTransport(CODE,DATA+4,4),6,'FF15'),
               (code,oracle.ImportTransport(CODE,DATA,4),5,'straddles'),
               (code,oracle.ImportTransport(CODE,DATA,4),6,'read authorization'))
        for payload,spec,length,message in cases:
            reads=()if message=='read authorization'else((DATA,8),)
            with self.subTest(message=message),self.assertRaisesRegex(oracle.OracleError,message):
                with machine(payload,region_bytes=length,reads=reads,transports=(spec,)):pass

    def test_import_transport_rejects_modified_iat_and_bad_callback_abi(self):
        code=b'\xff\x15'+struct.pack('<I',DATA)+b'\x90'
        spec=oracle.ImportTransport(CODE,DATA,4)
        with machine(code,reads=((DATA,4),),transports=(spec,))as(uc,image):
            image._original_bytes(DATA, 4)
            image.write(DATA,b'\x22'*4)
            self.rejected(uc,image,'transport_iat_changed',transports={CODE:lambda call:call.return_to_native(0)})
        for changed in ('none','pc','sp'):
            with self.subTest(changed=changed),machine(code,reads=((DATA,4),),transports=(spec,))as(uc,image):
                def callback(call):
                    if changed=='none':return
                    call.return_to_native(0)
                    call._machine.reg_write(UC_X86_REG_EIP if changed=='pc'else UC_X86_REG_ESP,0)
                self.rejected(uc,image,'transport_abi',transports={CODE:callback})

    def test_import_transport_data_and_stack_access_are_declared(self):
        code=b'\xff\x15'+struct.pack('<I',DATA)+b'\x90'
        spec=oracle.ImportTransport(CODE,DATA,4)
        for operation in ('stack_read','stack_write','data_read','data_write','code_write'):
            with self.subTest(operation=operation),machine(code,reads=((DATA,4),),transports=(spec,))as(uc,image):
                def callback(call):
                    if operation=='stack_read':call.read(call.sp+4,4)
                    elif operation=='stack_write':call.write(call.sp,b'\x00'*4)
                    elif operation=='data_read':call.read(DATA+4,4)
                    elif operation=='data_write':call.write(DATA,b'\x00'*4)
                    else:call.write(CODE,b'\x90')
                    call.return_to_native(0)
                self.rejected(uc,image,'transport_failure',transports={CODE:callback})

    def test_no_argument_import_preserves_stack_and_has_no_implicit_stack_access(self):
        code=b'\xff\x15'+struct.pack('<I',DATA)+b'\xc1\xe8\x04'
        spec=oracle.ImportTransport(CODE,DATA,0)
        with machine(code,reads=((DATA,4),),transports=(spec,))as(uc,image):
            sp=uc.reg_read(UC_X86_REG_ESP)
            def callback(call):
                self.assertEqual(call.arguments,())
                with self.assertRaises(oracle.OracleError):call.read(sp,4)
                call.return_to_native(0xFFFFFFFF)
            self.run_scope(uc,image,transports={CODE:callback})
            self.assertEqual(uc.reg_read(UC_X86_REG_ESP),sp)
            self.assertEqual(uc.reg_read(UC_X86_REG_EAX),0x0FFFFFFF)
        for count in (-4,1,2,3):
            with self.subTest(count=count),self.assertRaisesRegex(oracle.OracleError,'Invalid or duplicate'):
                with machine(code,reads=((DATA,4),),transports=(replace(spec,argument_bytes=count),)):
                    pass

    def test_import_transport_forwards_exact_com_stack_to_original_factory(self):
        factory=CODE+16
        code=b'\xff\x15'+struct.pack('<I',DATA)+b'\x90'+b'\xcc'*9+b'\xb8\x2a\0\0\0\xc2\x10\0'
        spec=oracle.ImportTransport(CODE,DATA,20,stack_writes=((0,20),),forward_entry=factory)
        with machine(code,reads=((DATA,4),),transports=(spec,),end=CODE+7)as(uc,image):
            sp=uc.reg_read(UC_X86_REG_ESP)
            image.write(sp,struct.pack('<5I',1,2,3,4,5))
            self.run_scope(uc,image,transports={CODE:lambda call:call.forward_to_factory()},required_addresses=[factory])
            self.assertEqual(uc.reg_read(UC_X86_REG_EAX),42)
            self.assertEqual(uc.reg_read(UC_X86_REG_ESP),sp+20)
            self.assertEqual(bytes(uc.mem_read(sp,20)),struct.pack('<5I',CODE+6,0,2,4,5))

    def test_prior_hook_cannot_mutate_transport_pc_or_stack_before_guard(self):
        from unicorn import UC_HOOK_CODE
        code=b'\xff\x15'+struct.pack('<I',DATA)+b'\x90'
        spec=oracle.ImportTransport(CODE,DATA,4)
        for reg in (UC_X86_REG_EIP,UC_X86_REG_ESP):
            with self.subTest(reg=reg),machine(code,reads=((DATA,4),),transports=(spec,))as(uc,image):
                uc.hook_add(UC_HOOK_CODE,lambda machine,a,n,d:machine.reg_write(reg,0)if a==CODE else None)
                self.rejected(uc,image,'prehook_control_mutation',transports={CODE:lambda call:call.return_to_native(0)})

    def test_profile_identity_and_regions_are_immutable_and_checked(self):
        with machine(b'\x90') as (_uc, image):
            with self.assertRaises(FrozenInstanceError):
                image.profile.name = 'changed'
            with self.assertRaisesRegex(oracle.OracleError, 'unsupported executable'):
                oracle.load_image(Uc(UC_ARCH_X86, UC_MODE_32), profile=replace(image.profile, native_sha256='0' * 64))
            with self.assertRaisesRegex(oracle.OracleError, 'region mismatch'):
                oracle.load_image(Uc(UC_ARCH_X86, UC_MODE_32), profile=replace(image.profile, regions=((CODE, CODE + 1, '0' * 64),)))
