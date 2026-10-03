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

CODE = oracle.IMAGE_BASE + 0x1000
DATA = oracle.IMAGE_BASE + 0x3000
SINK = CODE + 0x100


class LegacyConstructorTests(unittest.TestCase):
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
def machine(code, *, region_bytes=None, reads=(), writes=(), sinks=(), end=None):
    data = pe_image([(0x1000, 0x200, code, 0x1000, 0x60000020),
                     (0x3000, 0x400, b'\x11' * 32, 0x1000, 0xC0000040)])
    length = len(code) if region_bytes is None else region_bytes
    profile = oracle.ExecutionProfile(
        name='synthetic-test-only', native_sha256=hashlib.sha256(data).hexdigest(),
        regions=((CODE, CODE + length, hashlib.sha256(code[:length]).hexdigest()),),
        entries=((CODE, (end or CODE + len(code),)),),
        reads=((oracle.STACK_BASE, oracle.STACK_SIZE),) + reads,
        writes=((oracle.STACK_BASE, oracle.STACK_SIZE),) + writes,
        fixture_writes=((oracle.STACK_BASE, oracle.STACK_SIZE), (DATA, 32)), sinks=sinks)
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

    def test_omitted_or_wrong_image_handle_cannot_run_scoped_machine(self):
        with machine(b'\x90') as (uc, image):
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
            def callback(machine):
                sp = machine.reg_read(UC_X86_REG_ESP)
                target = struct.unpack('<I', machine.mem_read(sp, 4))[0]
                machine.mem_write(CODE + 5, b'\xcc')
                machine.reg_write(UC_X86_REG_ESP, sp + 4)
                machine.reg_write(UC_X86_REG_EIP, target)
            self.rejected(uc, image, 'native_code_changed', sinks={SINK: callback})

    def test_profile_identity_and_regions_are_immutable_and_checked(self):
        with machine(b'\x90') as (_uc, image):
            with self.assertRaises(FrozenInstanceError):
                image.profile.name = 'changed'
            with self.assertRaisesRegex(oracle.OracleError, 'unsupported executable'):
                oracle.load_image(Uc(UC_ARCH_X86, UC_MODE_32), profile=replace(image.profile, native_sha256='0' * 64))
            with self.assertRaisesRegex(oracle.OracleError, 'region mismatch'):
                oracle.load_image(Uc(UC_ARCH_X86, UC_MODE_32), profile=replace(image.profile, regions=((CODE, CODE + 1, '0' * 64),)))
