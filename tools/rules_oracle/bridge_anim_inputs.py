"""Original AnimType ART reader independently establishes bridge oracle inputs.

Set VERA20K_BRIDGE_ANIM_ASSETS to a directory containing extracted ARTMD.INI
and the 23 physical SHPs named in bridge_anim_inputs.md. Run with PYTHONPATH=.
and VERA20K_GAMEMD_EXE; --write records and --check reproduces native results.
No VERA scalar/parser output initializes native AnimType fields. Both existing
production-export input fixtures are asserted against the native results.
"""
import json,struct,hashlib,os
from pathlib import Path
from tools.rules_oracle.bridge_anim_lists import Lists,HEAP
from tools.projectile_oracle.flat_art import crc
from tools.spatial_oracle.building_body_rules import INI,SP,dwords
from tools.native_oracle import run_checked,RET_MAGIC,NATIVE_SHA256,finish_vectors,provenance
from tools.spatial_oracle.fv_cell_attack.steam_live_reader_helpers_scope import LIVE_READER_WS_PRINTF_CALLS
from unicorn.x86_const import *
DEFAULT_ASSETS=Path(os.environ.get('CARGO_TARGET_DIR','target'))/'asset/bridge-anim-inputs/extract'
ROOT=Path(os.environ.get('VERA20K_BRIDGE_ANIM_ASSETS',str(DEFAULT_ASSETS)))
HERE=Path(__file__).resolve().parent
NAMES=[f'DBRIS{i}LG' for i in range(1,10)]+['DBRS10LG']+[f'DBRIS{i}SM' for i in range(1,5)]+['D','TWLT026','TWLT036','TWLT050','TWLT070','WAKE1','H2O_EXP1','H2O_EXP2','H2O_EXP3','SMOKEY2']
SCALARS={'start':0x2b4,'loop_start':0x2b8,'loop_end':0x2bc,'end':0x2c0,'loop_count':0x2c4,'rate':0x2b0,'damage_radius':0x334,'trailer_seperation':0x30c}
DOUBLES={'damage_f64_bits':0x2a8,'elasticity_f64_bits':0x310,'min_z_vel_f64_bits':0x318,'max_z_vel_f64_bits':0x320,'max_xy_vel_f64_bits':0x328}
BOOLS={'bouncer':0x35a,'normalized':0x362,'scorch':0x36b,'crater':0x36d,'shadow':0x372}
REFS={'bounce_anim':0x300,'expire_anim':0x304,'trailer_anim':0x308,'warhead':0x330}
def physical_sections(raw,*,names=NAMES,empty_section_reopen=False):
 # Cache preparation supplies either selected unique sections, or the complete
 # unique physical root when names=None; it never interprets type/scalar values.
 # It supplies physical lexical strings, never parses scalar/type values.
 # Original INIClass525A60 file loading/archive selection are not executed.
 result={};current=None
 for line in raw.splitlines():
  line=line.strip(bytes(range(33)))
  if line.startswith(b'[') and b']' in line:
   name=line[1:line.index(b']')].decode('latin1');current={}
   if names is None or name in names:
    # Existing supplier omits empty sections. The explicit full-ART boundary
    # may reopen an earlier empty occurrence; nonempty duplicates still fail.
    # This does not claim physical native INI loader/section reuse parity.
    if name in result and empty_section_reopen and not result[name]:del result[name]
    assert name not in result,name;result[name]=current
   else:current=None
   continue
  if current is None:continue
  line=line.split(b';',1)[0].strip(bytes(range(33)))
  if b'=' not in line:continue
  k,v=(x.strip(bytes(range(33))) for x in line.split(b'=',1))
  if k and v:
   k=k.decode('latin1');assert k not in current,('duplicate-key',k);current[k]=v.decode('latin1')
 return {n:v for n,v in result.items() if v}
def ascii_utf16(value,capacity):
 # The existing physical Mission OS boundary, limited to ASCII CP_ACP input.
 # -1 includes NULL and returned UTF16 code-unit count includes NULL:
 # https://learn.microsoft.com/en-us/windows/win32/api/stringapiset/nf-stringapiset-multibytetowidechar
 assert value.isascii();raw=(value+'\0').encode('utf-16-le');assert len(raw)//2<=capacity
 return raw

def clsid_bytes(value):
 # Host OS transport, not original Windows code execution. GUID memory layout:
 # https://learn.microsoft.com/en-us/windows/win32/api/guiddef/ns-guiddef-guid
 # https://learn.microsoft.com/en-us/windows/win32/api/combaseapi/nf-combaseapi-clsidfromstring
 import uuid
 return uuid.UUID(value).bytes_le

class Reader(Lists):
 def __init__(self,root,sections,*,profile=None,heap_bytes=0x400000,native_registry_startup=False):
  self.assets={p.name.upper():p.read_bytes() for p in root.glob('*')};self.asset_loaded=[];self.asset_ptr={};self.sound_names=[]
  self.asset_source=None
  super().__init__(profile=profile,heap_bytes=heap_bytes,native_registry_startup=native_registry_startup)
  # Retail startup installs the CRT floating scanner before ReadDouble5283D0.
  self.invoke(0x7C8F5E,0)
  self.make_ini(sections)
  self.transport_events=[]
  if self.image is not None:
   self.transports={spec.site:self.import_transport for spec in profile.transports if spec.site in (0x527AF9,0x527B0C)}
 def cstring(self,s):
  raw=s.encode('latin1')+b'\0';ptr=self.alloc(len(raw));self.fixture_write(ptr,raw);return ptr
 def invoke(self,addr,obj,args=(),*,timeout_us=10_000_000,context=None,preserve_context=False,stack_pointer=SP,count=2000000):
  # Observation inside a retained original caller uses a reviewed disjoint
  # stack and the complete Unicorn CPU context (flags/x87 included). Guest
  # memory is never restored/copied. Historical calls retain their old ABI.
  if preserve_context and stack_pointer==SP:
   raise ValueError('Retained observational invocation needs a reviewed disjoint stack')
  saved=self.u.context_save()if preserve_context else None
  try:
   self.fixture_write(stack_pointer,dwords(RET_MAGIC,*args));self.u.reg_write(UC_X86_REG_ESP,stack_pointer);self.u.reg_write(UC_X86_REG_ECX,obj)
   self.run_native(addr,RET_MAGIC,count=count,timeout_us=timeout_us,context=context)
   result=self.u.reg_read(UC_X86_REG_EAX)
  finally:
   if saved is not None:self.u.context_restore(saved)
  return result
 def make_ini(self,sections,*,pointer=INI):
  # Separate root Rules and global ART receivers share this lexical-cache
  # owner. Callers establish both before entering a retained original frame.
  # Default callers retain the historical887180 receiver/reload semantics.
  if self.image is not None:
   # Immutable scoped image/profile identity owns this derived lexical index.
   # Repeated keys across Rules/ART/SOUND reuse one existing native CRC result;
   # scalar parsing and guest INI caches remain original native authorities.
   if hasattr(self,'_lexical_crc_image')and self._lexical_crc_image is not self.image:
    raise ValueError('Lexical CRC cache cannot move to another native image')
   if self.image.machine is not self.u:
    raise ValueError('Lexical CRC cache requires its original owner machine')
   self.image.verify_code()
   if not hasattr(self,'_lexical_crc_image'):
    self._lexical_crc_image=self.image;self._lexical_crc_values={}
  def lexical_crc(text):
   if self.image is None:return crc(text)
   if text not in self._lexical_crc_values:
    self._lexical_crc_values[text]=crc(text,profile=self.image.profile)
   return self._lexical_crc_values[text]
  u=self.u;self.fixture_write(pointer,bytes(0x40));rows=[];layouts=[]
  # Original ReadInt527818/52781B and ReadString528B73/528B76 write
  # receiver+8/+4. Original5268A1/5277EA write the CRC-index cache+38.
  # All other receiver words remain covered by immutable-byte fingerprints.
  regions=[(pointer,4),(pointer+0xC,0x2C),(pointer+0x3C,4)]
  for name,keys in sections.items():
   sec=self.alloc(0x44);name_ptr=self.cstring(name)
   self.fixture_write(sec+0xc,dwords(name_ptr));entries=[]
   regions.extend(((name_ptr,len(name.encode('latin1'))+1),(sec,0x3C),(sec+0x40,4)))
   # Original52ACE0 intrusive list: embedded head/tail, distinct from
   # the CRC index. Original526CC0 walks source order from section+18.
   # See physical-ini-intrusive-entry-discovery.json; physical loading remains
   # a supplied lexical cache, not an executed parser/retirement claim.
   head,tail=sec+0x14,sec+0x20
   self.fixture_write(sec+0x10,dwords(0x7EB744,0x7E1B0C,tail,0,0x7E1B0C,0,head))
   previous=head
   for key,value in keys.items():
    entry=self.alloc(0x28);self.fixture_write(entry,dwords(0x7EB734,tail,previous))
    self.fixture_write(previous+4,dwords(entry));self.fixture_write(tail+8,dwords(entry));previous=entry
    key_ptr=self.cstring(key);value_ptr=self.cstring(value)
    self.fixture_write(entry+0xc,dwords(key_ptr,value_ptr));entries.append((lexical_crc(key),entry))
    regions.extend(((entry,0x28),(key_ptr,len(key.encode('latin1'))+1),(value_ptr,len(value.encode('latin1'))+1)))
   items=self.alloc(len(entries)*8)
   for i,(key,entry_pointer) in enumerate(sorted(entries,key=lambda x:struct.unpack('<i',dwords(x[0]))[0])):self.fixture_write(items+i*8,dwords(key,entry_pointer))
   self.fixture_write(sec+0x2c,dwords(items,len(entries),len(entries),1,0));rows.append((lexical_crc(name),sec))
   if entries:regions.append((items,len(entries)*8))
   layouts.append(dict(pointer=sec,name=name,index_pointer=items,index_count=len(entries)))
  items=self.alloc(len(rows)*8)
  for i,(key,entry_pointer) in enumerate(sorted(rows,key=lambda x:struct.unpack('<i',dwords(x[0]))[0])):self.fixture_write(items+i*8,dwords(key,entry_pointer))
  self.fixture_write(pointer+0x28,dwords(items,len(rows),len(rows),1,0))
  if rows:regions.append((items,len(rows)*8))
  # Derived extents belong to this preparer, including existing callers which
  # borrow make_ini without constructing Reader. Repreparing a receiver replaces
  # its layout; guest memory remains authoritative and native reads own caches.
  if not hasattr(self,'_ini_cache_layouts'):self._ini_cache_layouts={}
  self._ini_cache_layouts[pointer]=dict(regions=tuple(regions),sections=layouts,index_pointer=items,index_count=len(rows))
  return pointer
 def ini_cache_snapshot(self,pointer=INI):
  """Observe prepared immutable bytes and independently owned native caches.

  Native last-section arguments are borrowed caller pointers. The section
  cache and CRC-index cache may name different sections after find-only
  queries; validate membership independently. A continuing caller can impose
  stronger literal/section coherence where its executed body establishes it.
  Original52775D stores the section key-index cache at section+3C. Hits cache
  actual eight-byte index rows; a miss may retain the prior valid row.
  """
  layout=self._ini_cache_layouts[pointer]
  argument,section,index=(self.read32(pointer+offset)for offset in (4,8,0x38))
  def member(value,start,count):return value==0 or start<=value<start+count*8 and (value-start)%8==0
  if bool(argument)!=bool(section)or section and section not in {row['pointer']for row in layout['sections']}:
   raise ValueError('Native INI last-section cache has no owned section')
  if argument:
   # Addressability only: the native cache borrows an argument, rather than
   # requiring it to be an allocation owned by this lexical receiver.
   self.u.mem_read(argument,1)
  if not member(index,layout['index_pointer'],layout['index_count']):
   raise ValueError('Native INI section-index cache points outside its own index')
  caches=[]
  for row in layout['sections']:
   entry=self.read32(row['pointer']+0x3C)
   if not member(entry,row['index_pointer'],row['index_count']):
    raise ValueError('Native INI key-index cache points outside its own section index')
   caches.append(dict(row,cache_entry_pointer=entry,header_hex=bytes(self.u.mem_read(row['pointer'],0x44)).hex()))
  digest=hashlib.sha256()
  for address,size in layout['regions']:
   digest.update(struct.pack('<II',address,size));digest.update(bytes(self.u.mem_read(address,size)))
  return dict(receiver=pointer,header_hex=bytes(self.u.mem_read(pointer,0x40)).hex(),
      immutable_sha256=digest.hexdigest(),immutable_regions=len(layout['regions']),
      immutable_bytes=sum(size for _,size in layout['regions']),
      index_pointer=layout['index_pointer'],index_count=layout['index_count'],
      last_section_argument_pointer=argument,last_section_pointer=section,
      section_index_cache_pointer=index,sections=caches,cache_pointer_membership_valid=True)
 def import_transport(self,call):
  for row in LIVE_READER_WS_PRINTF_CALLS:
   if call.spec.site!=row['site']:continue
   destination,pattern,index=struct.unpack('<III',call.read(call.sp,row['argument_bytes']))
   if (destination!=call.sp+row['destination_sp_offset']or pattern!=row['format_address']or
       not row['index_min']<=index<=row['index_max']):
    raise ValueError('Original bounded occupancy-key wsprintf arguments changed')
   if call.read(pattern,len(row['format_bytes']))!=row['format_bytes']:
    raise ValueError('Original occupancy-key wsprintf format bytes changed')
   # Supplied USER32 API: only original Add/RemoveOccupy%d with indices1..8.
   # Signed decimal, NUL/count and cdecl contract:
   # https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-wsprintfa
   output=row['prefix_bytes']+bytes((ord('0')+index,))+b'\0'
   call.write(destination,output);call.return_to_native(len(output)-1)
   self.transport_events.append(dict(kind='OS_occupancy_key_wsprintfA',site=call.spec.site,
       index=index,output_hex=output.hex(),return_characters=len(output)-1));return
  if call.spec.site==0x527AF9:
   codepage,flags,source,length,dest,capacity=call.arguments
   assert (codepage,flags,length,capacity)==(0,1,0xffffffff,128)
   assert source==call.sp+0x50 and dest==call.sp+0xD0
   raw=call.read(source,128);assert b'\0'in raw
   value=raw.split(b'\0')[0].decode('ascii');converted=ascii_utf16(value,capacity)
   call.write(dest,converted);call.return_to_native(len(converted)//2)
   self.transport_events.append(dict(kind='OS_ascii_to_utf16',value=value,output_hex=converted.hex(),return_code_units=len(converted)//2));return
  if call.spec.site==0x527B0C:
   source,dest=call.arguments
   assert source==call.sp+0xC0 and dest==call.sp+0x20
   raw=call.read(source,256);units=struct.unpack('<128H',raw);assert 0 in units
   value=''.join(chr(v)for v in units[:units.index(0)])
   assert len(value)==38 and value[0]=='{'and value[-1]=='}'
   converted=clsid_bytes(value);call.write(dest,converted);call.return_to_native(0)
   self.transport_events.append(dict(kind='OS_CLSIDFromString',value=value,bytes=converted.hex(),hresult=0));return
  raise ValueError('Unsupported original import transport site')
 def hook(self,u,p,n,d):
  if p==0x5B40B0:
   name=self.string(u.reg_read(UC_X86_REG_ECX));raw=self.assets.get(name.upper());pointer=0
   source=None
   if self.asset_source is not None:
    raw,source=self.asset_source.read(name)
    if name.upper() in self.assets and self.assets[name.upper()]!=raw:
     raise ValueError('Conflicting retained physical asset supplier: '+name)
   if raw:
    cache_key=name.upper()
    if self.asset_source is not None:
     from tools.sidebar_oracle.stock import mix_hash
     cache_key=('native-crc',mix_hash(name))
    if cache_key not in self.asset_ptr:
     pointer=self.alloc(len(raw));self.fixture_write(pointer,raw);self.asset_ptr[cache_key]=pointer
    pointer=self.asset_ptr[cache_key]
   event=dict(name=name,bytes=len(raw) if raw else 0,sha256=hashlib.sha256(raw).hexdigest() if raw else None,header8_hex=raw[:8].hex() if raw else None)
   if source is not None:event['physical_source']=source
   self.asset_loaded.append(event);self.ret(pointer,0);return
  super().hook(u,p,n,d)
 def result(self,name,ptr,admitted):
  u=self.u
  out={'name':name,'art_body_read':bool(admitted&255)}
  out.update({k:struct.unpack('<i',u.mem_read(ptr+v,4))[0] for k,v in SCALARS.items()})
  out.update({k:struct.unpack('<Q',u.mem_read(ptr+v,8))[0] for k,v in DOUBLES.items()})
  out.update({k:bool(u.mem_read(ptr+v,1)[0]) for k,v in BOOLS.items()})
  out.update({k:self.string(self.read32(ptr+v)+0x24) if self.read32(ptr+v) else None for k,v in REFS.items()})
  image=self.read32(ptr+0xa4);out.update(image=self.string(ptr+0x1f8),raw_shp_frame_count=struct.unpack('<h',u.mem_read(image+6,2))[0] if image else 0,middle=struct.unpack('<i',u.mem_read(ptr+0x298,4))[0],random_rate=list(struct.unpack('<2i',u.mem_read(ptr+0x2e4,8))),report_index=struct.unpack('<i',u.mem_read(ptr+0x2f8,4))[0])
  return out

def read_types(root,sections,names):
 m=Reader(root,sections);types={}
 for name in names:
  ptr=m.alloc(0x400);m.invoke(0x427530,ptr,(m.cstring(name),));types[name]=ptr
 rows=[]
 for name,ptr in types.items():
  mark=len(m.asset_loaded);admitted=m.invoke(0x427D00,ptr,(INI,))
  row=m.result(name,ptr,admitted)
  row['asset_loads']=m.asset_loaded[mark:]
  row['physical_art_keys']=sections.get(name)
  rows.append(row)
 return rows

# These are the actual fields supplied by producer/flight harnesses. No expected
# field is read before the independent native constructor/ART call above.
EXPORTED_FIELDS=list(SCALARS)+[x for x in DOUBLES if x!='max_z_vel_f64_bits']+[
 'art_body_read','bouncer','scorch','crater','expire_anim','trailer_anim',
 'bounce_anim','warhead','raw_shp_frame_count']

def assert_production_exports(native_rows):
 native={r['name']:r for r in native_rows};checks=[]
 for filename,count in [('bridge-retail-anim-inputs.json',19),
                         ('bridge_debris_flight.inputs.json',24)]:
  path=HERE.parent/'spatial_oracle'/filename
  rows=json.loads(path.read_text())['rows'];assert len(rows)==count
  compared=[]
  for row in rows:
   name=row['name'];expected=native[name]
   if row.get('missing_runtime_config'):
    # Historical export exposes the production defect fixed by this chain:
    # registered D was missing a runtime config. Native remains constructor-only.
    assert name=='D' and not expected['art_body_read']
    assert expected['raw_shp_frame_count']==0 and expected['asset_loads']==[]
    continue
   for field in EXPORTED_FIELDS:
    assert row[field]==expected[field],(filename,name,field,row[field],expected[field])
   assert (row['random_rate'] or [0,0])==expected['random_rate'],(filename,name,'random_rate')
   normalized='normalized: true' in row['full_config_debug']
   assert normalized==expected['normalized'],(filename,name,'normalized')
   compared.append(name)
  checks.append(dict(fixture=filename,compared=compared,
                    historical_missing_config=['D'],fields=EXPORTED_FIELDS+['random_rate','normalized']))
 return checks

def generate():
 raw=(ROOT/'ARTMD.INI').read_bytes();sections=physical_sections(raw)
 assert set(sections)==set(NAMES)-{'D'},sorted(sections)
 rows=read_types(ROOT,sections,NAMES)
 checks=assert_production_exports(rows)
 # Distinguish +36B Scorch from +36D Crater independently; the selected retail
 # rows set both identically and cannot detect an accidentally swapped injector.
 controls=[]
 for scorch,crater in [('yes','no'),('no','yes')]:
  controls.extend(read_types(ROOT,{'DBRIS1LG':{'Scorch':scorch,'Crater':crater}},['DBRIS1LG']))
 assert [(r['scorch'],r['crater']) for r in controls]==[(True,False),(False,True)]
 return dict(schema_version=1,native_sha256=NATIVE_SHA256,
             art_sha256=hashlib.sha256(raw).hexdigest(),art_bytes=len(raw),
             rows=rows,asymmetric_flag_controls=controls,production_export_checks=checks)

def metadata():
 return provenance(
  scope='24 independently initialized original AnimType ART readers/image-header consumers plus two asymmetric Scorch/Crater controls; bridge producer/flight input prerequisites',
  assumptions=[
   'Selected exact-case physical ARTMD sections/keys are unique; a bounded lexical extraction prepares original signed-CRC INI caches. Full INIClass525A60 physical loader and MIX precedence are outside this run. All scalar values/defaults/references/rate postprocessing come from original ctor427530 and ReadINI427D00, not VERA exports.',
   'ARTMD and 23 full SHP files are extracted retail bytes. Output pins ART SHA256 and each loaded SHP SHA256, length and first eight bytes. Original filename formation and image metadata427B50 execute; archive IO returns the corresponding unchanged physical bytes.',
   'Fresh original AnimType registry preallocates all24 types in native pool/list order, with empty sound registry. Original missing D section returns false and retains constructor values. HE FindOrAllocate and its original ctor execute; this does not establish Warhead rules fields.',
   'Report/StartSound stay -1 in the empty sound registry, matching the declared silent producer/flight boundary; sound binding/playback is not claimed.',
   'The completed native rows assert every injected ART field against both saved production-export fixtures; historical missing D is explicitly identified instead of certified as correct production behavior. Current production Rust comparisons cover corrected D separately.',
   'PC53/chop FPCW0E7F; original CRT floating scanner initializer7C8F5E executes before native ReadDouble. Native uint64 payloads retain exact binary64 bits.'],
  substitutions=[
   'operator_new7C8E17 returns bump storage; operator_delete7C8B3D is no-op; CRT TLS accessor7D140B returns per-thread storage.',
   'LoadFileFromMIX5B40B0 returns exact full bytes for the original requested retail filename; no SHP header is manufactured.'],
  entry_points={'anim_type_ctor':0x427530,'anim_type_read_art':0x427D00,
   'object_type_read':0x5F92E0,'image_load_and_metadata':0x427B50,
   'read_double':0x5283D0,'read_integer':0x5276D0,'read_bool':0x5295F0,
   'read_minmax':0x529880,'float_scanner_init':0x7C8F5E})

if __name__=='__main__':
 finish_vectors(generate,Path(__file__).with_suffix('.json'),provenance=metadata)
