"""Guard the original RawFile CALL EBP import boundary, never a general jump."""
import struct
import unittest
from dataclasses import replace

from unicorn.x86_const import UC_X86_REG_EAX, UC_X86_REG_EBP, UC_X86_REG_EIP, UC_X86_REG_ESP

from tools import native_oracle as oracle
from tools.tests.test_native_scope import CODE, DATA, machine


class EbpTransportTests(unittest.TestCase):
    def spec(self):
        return oracle.EbpImportTransport(CODE,DATA,4)

    def run_scope(self,uc,image,**kwargs):
        return oracle.run_checked(uc,CODE,CODE+3,image=image,**kwargs)

    def rejected(self,uc,image,kind,**kwargs):
        with self.assertRaises(oracle.NativeExecutionError)as error:self.run_scope(uc,image,**kwargs)
        self.assertEqual(error.exception.diagnostics['profile_violation']['kind'],kind)

    def test_exact_original_register_import_redirect_and_argument_cleanup(self):
        with machine(b'\xff\xd5\x40',reads=((DATA,4),),transports=(self.spec(),))as(uc,image):
            uc.reg_write(UC_X86_REG_EBP,struct.unpack('<I',oracle.file_span(image.data,DATA,4)[1])[0])
            sp=uc.reg_read(UC_X86_REG_ESP)
            def callback(call):
                self.assertEqual(call.arguments,(0,))
                call.return_to_native(41)
            self.run_scope(uc,image,transports={CODE:callback})
            self.assertEqual(uc.reg_read(UC_X86_REG_EAX),42)
            self.assertEqual(uc.reg_read(UC_X86_REG_ESP),sp+4)
            event,=uc._vera20k_last_import_transports
            self.assertFalse(event['original_instruction_executed'])
            self.assertEqual(event['redirect'],CODE+2)

    def test_wrong_register_target_is_rejected_before_callback(self):
        with machine(b'\xff\xd5\x90',reads=((DATA,4),),transports=(self.spec(),))as(uc,image):
            uc.reg_write(UC_X86_REG_EBP,0xDEADBEEF)
            self.rejected(uc,image,'transport_register_target',transports={CODE:lambda call:self.fail('must not run')})

    def test_modified_iat_is_rejected(self):
        with machine(b'\xff\xd5\x90',reads=((DATA,4),),transports=(self.spec(),))as(uc,image):
            image.write(DATA,b'\x22'*4)
            self.rejected(uc,image,'transport_iat_changed',transports={CODE:lambda call:self.fail('must not run')})

    def test_only_call_ebp_bytes_and_whole_site_can_be_declared(self):
        for code,length,message in ((b'\xff\xd0\x90',3,'CALL EBP'),(b'\xff\xd5\x90',1,'straddles')):
            with self.subTest(code=code),self.assertRaisesRegex(oracle.OracleError,message):
                with machine(code,region_bytes=length,reads=((DATA,4),),transports=(self.spec(),)):pass

    def test_callback_cannot_return_with_legacy_six_byte_pc_or_omit_cleanup(self):
        for changed in ('pc','sp'):
            with self.subTest(changed=changed),machine(b'\xff\xd5\x90',reads=((DATA,4),),transports=(self.spec(),))as(uc,image):
                uc.reg_write(UC_X86_REG_EBP,struct.unpack('<I',oracle.file_span(image.data,DATA,4)[1])[0])
                def callback(call):
                    call.return_to_native(0)
                    uc.reg_write(UC_X86_REG_EIP if changed=='pc'else UC_X86_REG_ESP,CODE+6 if changed=='pc'else call.sp)
                self.rejected(uc,image,'transport_abi',transports={CODE:callback})

    def test_register_import_cannot_forward_to_native_com_factory(self):
        spec=replace(self.spec(),argument_bytes=20,stack_writes=((0,20),),forward_entry=CODE+2)
        with self.assertRaisesRegex(oracle.OracleError,'cannot forward'):
            with machine(b'\xff\xd5\x90',reads=((DATA,4),),transports=(spec,)):pass


if __name__=='__main__':unittest.main()
