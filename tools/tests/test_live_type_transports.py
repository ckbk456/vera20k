"""Bounded USER32 data/ABI controls; no Windows execution or gameplay parity."""
import struct
import unittest
from unittest.mock import patch

from unicorn.x86_const import UC_X86_REG_EAX,UC_X86_REG_ESP
from tools import native_oracle as oracle
from tools.rules_oracle import bridge_anim_inputs as bridge
from tools.spatial_oracle.fv_cell_attack.steam_live_reader_helpers_scope import LIVE_READER_WS_PRINTF_CALLS
from tools.tests.test_native_scope import CODE,DATA,machine


class OccupancyKeyTransportTests(unittest.TestCase):
    def execute(self,original,index=1,mutation=None):
        row=dict(original,site=CODE,iat=DATA,format_address=DATA+4)
        spec=oracle.ImportTransport(CODE,DATA,0,stack_reads=row['stack_reads'],stack_writes=row['stack_writes'])
        with machine(b'\xff\x15'+struct.pack('<I',DATA)+b'\x90',reads=((DATA,32),),transports=(spec,))as(uc,image):
            sp=uc.reg_read(UC_X86_REG_ESP);destination=sp+row['destination_sp_offset']
            image.write(DATA+4,row['format_bytes'])
            args=[destination,DATA+4,index]
            if mutation=='destination':args[0]+=1
            if mutation=='format_pointer':args[1]+=1
            if mutation=='format_bytes':image.write(DATA+4,b'X')
            image.write(sp,struct.pack('<III',*args))
            owner=bridge.Reader.__new__(bridge.Reader);owner.transport_events=[]
            with patch.object(bridge,'LIVE_READER_WS_PRINTF_CALLS',(row,)):
                if mutation or not 1<=index<=8:
                    with self.assertRaises(oracle.NativeExecutionError)as caught:
                        oracle.run_checked(uc,CODE,CODE+7,image=image,transports={CODE:owner.import_transport})
                    self.assertEqual(caught.exception.diagnostics['profile_violation']['kind'],'transport_failure')
                    self.assertEqual(bytes(uc.mem_read(destination,row['stack_writes'][0][1])),bytes(row['stack_writes'][0][1]))
                    self.assertEqual(owner.transport_events,[])
                else:
                    oracle.run_checked(uc,CODE,CODE+7,image=image,transports={CODE:owner.import_transport})
                    prefix='AddOccupy'if original['site']==0x461442 else'RemoveOccupy'
                    expected=(prefix+str(index)).encode()+b'\0'
                    self.assertEqual(bytes(uc.mem_read(destination,len(expected))),expected)
                    self.assertEqual(uc.reg_read(UC_X86_REG_EAX),len(expected)-1)
                    self.assertEqual(uc.reg_read(UC_X86_REG_ESP),sp) # Original caller owns cdecl cleanup.

    def test_both_original_patterns_cover_every_original_loop_index(self):
        for row in LIVE_READER_WS_PRINTF_CALLS:
            for index in range(1,9):
                with self.subTest(site=row['site'],index=index):self.execute(row,index)

    def test_unreviewed_integer_domain_is_rejected_without_writing(self):
        for index in (0,9,0xFFFFFFFF):
            with self.subTest(index=index):self.execute(LIVE_READER_WS_PRINTF_CALLS[0],index)

    def test_changed_destination_or_format_is_rejected_without_writing(self):
        for mutation in ('destination','format_pointer','format_bytes'):
            with self.subTest(mutation=mutation):self.execute(LIVE_READER_WS_PRINTF_CALLS[1],mutation=mutation)


if __name__=='__main__':unittest.main()
