"""Original RulesClass bridge animation vectors: constructors and ReadGeneral.

Run from the repository root with PYTHONPATH=. and VERA20K_GAMEMD_EXE set:
  python tools/rules_oracle/bridge_anim_lists.py --check

INI lookup indexes are supplied; the original ReadString, strtok, AnimType
factory/constructors and vector copy execute. This does not execute physical INI
loading, ART loading or animation playback. Rust consumers compare the retained
lists through RulesLayerStack and RuleSet in native_processing_tests.rs.
"""
import json, struct
from pathlib import Path
from unicorn import UC_HOOK_CODE
from unicorn.x86_const import *
from tools.native_oracle import run_checked, finish_vectors, provenance
from tools.spatial_oracle.building_body_rules import Fixture, TYPE, INI, SP, dwords
HEAP=0x24000000
KEYS={'MetallicDebris':(0x83CEF0,0x66DA90,0x66DB93,0x13C), 'BridgeExplosions':(0x83CEDC,0x66DB93,0x66DC96,0x158)}
class Lists:
 def __init__(self,*,profile=None,heap_bytes=0x400000,native_registry_startup=False):
  live_heap=profile is not None and profile.name in (
   'steam-15918130-fv-ordered-live-types-v1',
   'steam-15918130-fv-ordered-rules-process-tail-v1') and heap_bytes==0x08000000
  if (not live_heap and not 0x20000<=heap_bytes<=0x2000000)or heap_bytes%0x1000:
   raise ValueError('Reader heap requires historical128KiB..32MiB or the exact128MiB live asset profile')
  self.f=Fixture(profile=profile);self.u=self.f.u;self.image=self.f.image
  self.u.mem_map(HEAP,heap_bytes);self.heap_end=HEAP+heap_bytes;self.cursor=HEAP+0x10000
  self.events=[];self.read_result=None;self.allocation_events=[];self.exit_registrations=[]
  if self.image is None:self.u.hook_add(UC_HOOK_CODE,self.hook)
  self.transports={}
  self.sinks={} if self.image is None else {a:(lambda u,a=a:self.hook(u,a,0,None))for a,_ in profile.sinks}
  if native_registry_startup and self.image is None:
   raise ValueError('Native registry startup requires a checked original image')
  # Historical isolated readers supply these empty registries with spare
  # capacity. A joined startup preserves original zero BSS instead: its actual
  # CRT constructors own the headers before any Type can register. Never
  # replace a populated retained registry to enter that route.
  if not native_registry_startup:
   for address,items in ((0x8B4150,HEAP+0x1000),(0xB0F670,HEAP+0x4000)):
    self.fixture_write(address,dwords(0x7EB6D4,items,1024,1,0,10))
  self.u.reg_write(UC_X86_REG_ESP,SP);self.u.reg_write(UC_X86_REG_ESI,TYPE)
  self.u.reg_write(UC_X86_REG_EBX,0);self.u.reg_write(UC_X86_REG_EDI,10)
  self.run_native(0x665827,0x66585F)
  self.initial={k:self.state(k) for k in KEYS}
 def fixture_write(self,address,blob):self.f.fixture_write(address,blob)
 def run_native(self,begin,end,**kwargs):return self.f.run_native(begin,end,sinks=self.sinks,transports=self.transports,**kwargs)
 def read32(self,p):return struct.unpack('<I',self.u.mem_read(p,4))[0]
 def alloc(self,n):
  if n<0:raise ValueError('Negative reader allocation')
  out=self.cursor;self.cursor+=(n+15)&~15
  assert self.cursor<self.heap_end,('Reader heap exhausted',n,hex(self.cursor),hex(self.heap_end))
  return out
 def string(self,p):return bytes(self.u.mem_read(p,512)).split(b'\0')[0].decode('latin1')
 def ret(self,eax,cleanup=0):
  sp=self.u.reg_read(UC_X86_REG_ESP);ret=self.read32(sp)
  self.u.reg_write(UC_X86_REG_EAX,eax);self.u.reg_write(UC_X86_REG_ESP,sp+4+cleanup);self.u.reg_write(UC_X86_REG_EIP,ret)
 def hook(self,u,p,n,user):
  if p==0x7C8E17 or (p==0x7C9430 and self.image is not None):
   # Selected original strdup7D5408 calls CRTmalloc7C9430 directly. Reuse
   # the one supplied heap/positive cdecl allocation boundary; execute its
   # original strlen/string copy. Zero-size/error/platform heap paths are
   # not enrolled by that selected consumer.
   size=self.read32(u.reg_read(UC_X86_REG_ESP)+4)
   if p==0x7C9430 and not size:raise ValueError('Selected CRTmalloc requires positive requested bytes')
   result=self.alloc(size)
   if self.image is not None:
    event=dict(size=size,pointer=result,initial_hex=bytes(u.mem_read(result,size)).hex())
    if p==0x7C9430:event.update(source=p,abi='cdecl',end=result+size)
    self.allocation_events.append(event)
   self.ret(result)
  elif p==0x7C978A and self.image is not None:
   self.exit_registrations.append(self.read32(u.reg_read(UC_X86_REG_ESP)+4));self.ret(0)
  elif p==0x7C93E8 and self.image is not None:
   # Original RawFile65CA4C frees its native strdup storage; Shape69E985
   # frees an original allocated physical buffer. This is the same supplied
   # heap/delete boundary, with ownership checked before a CRTfree return.
   pointer=self.read32(u.reg_read(UC_X86_REG_ESP)+4)
   if pointer and not any(row['pointer']==pointer for row in self.allocation_events):
    raise ValueError('CRTfree pointer is not a retained native allocation')
   if not hasattr(self,'free_events'):self.free_events=[]
   self.free_events.append(dict(source=p,pointer=pointer,storage_retained=True))
   self.ret(0)
  elif p==0x7C8B3D:self.ret(0)
  elif p==0x7D140B:self.ret(HEAP+0x8000)
  elif p==0x428B80:self.events.append(self.string(u.reg_read(UC_X86_REG_ECX)))
  elif p in (0x66DAB2,0x66DBB5):self.read_result={'length':u.reg_read(UC_X86_REG_EAX),'value':self.string(SP+0x50)}
 def state(self,key):
  off=KEYS[key][3];p=self.read32(TYPE+off+4);n=self.read32(TYPE+off+16)
  return {'data_is_null':p==0,'count':n,'names':[self.string(self.read32(p+i*4)+0x24) for i in range(n)]}
 def read(self,key,raw):
  p,begin,end,off=KEYS[key];self.f.ini(p,raw);self.f.write(INI+4,0x826278)
  self.u.reg_write(UC_X86_REG_ESP,SP);self.u.reg_write(UC_X86_REG_ESI,TYPE);self.u.reg_write(UC_X86_REG_EDI,INI)
  self.events=[];self.read_result=None
  self.run_native(begin,end,count=2000000,required_addresses=(0x528A10,))
  assert self.u.reg_read(UC_X86_REG_ESP)==SP
  return {'key':key,'raw':raw,'native_read_string':self.read_result,'find_or_allocate_inputs':list(self.events),'result':self.state(key)}
def generate():
 s=Lists();rows=[]
 for key in KEYS:
  for raw in ['ONE,TWO',None,'','   ', ',,,',
              'ONE, none,NONE,<none>,TWO,ONE',
              'abcdefghijklmnopqrstuvwxyz1234,abcdefghijklmnopqrstuvwxyz1234',
              'MixedCase,mIXEDcASE, MIXEDCASE , ,ONE',
              'none,<none>']:
   rows.append(s.read(key,raw))
 inputs=json.loads(Path(__file__).with_name('bridge_anim_list_inputs.json').read_text())
 for layer in inputs:
  if layer.get('absent'):continue
  for key in KEYS:rows.append({'file':layer['file'],**s.read(key,layer[key])})
 return {'constructor':s.initial,'rows':rows}


if __name__=='__main__':
 finish_vectors(generate,Path(__file__).with_suffix('.json'),provenance=lambda:provenance(
  scope='Original Rules two vector constructors and complete MetallicDebris/BridgeExplosions ReadGeneral blocks',
  assumptions=[
   'Supplied cached INI indexes. Retail input strings exported by production AssetManager and IniFile from RULESMD.INI, optional LANGRULE.INI, MPBattleMD.ini and Hills.mmx; no native physical INI load.',
   'Fresh AnimType registry with spare capacity, full original FindOrAllocate and constructors, original vector storage/copy routines. No AnimType ART read or game production claim.',
   'Rows execute sequentially in one RulesClass and AnimType registry; missing/empty/whitespace reads retain vectors while comma-only input replaces with empty.'],
  substitutions=[
   'operator_new returns bump storage; operator_delete is a no-op; CRT TLS accessor returns supplied per-thread storage for original strtok'],
  entry_points={'constructor':0x665827,'metallic_list':0x66DA90,'explosion_list':0x66DB93,
                'read_string':0x528A10,'strtok':0x7C9CC2,'find_or_allocate':0x428B80,'anim_type_ctor':0x427530}))
