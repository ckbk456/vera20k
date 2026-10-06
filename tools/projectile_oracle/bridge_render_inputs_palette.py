"""Original selected Init_Game palette loads, expansion and full Convert constructors.
Archive IO, an RGB565 BSurface and its initialized format globals are supplied.
"""
import importlib.util,json,struct,hashlib,argparse
from pathlib import Path
from unicorn import UC_HOOK_CODE
from unicorn.x86_const import *
from tools.native_oracle import run_checked,NATIVE_SHA256,RET_MAGIC
from tools.spatial_oracle.building_body_rules import SP,dwords
from tools.projectile_oracle import bridge_render_inputs as module

class PaletteReader(module.BulletReader):
 def __init__(self,art):
  super().__init__(art);self.u.mem_map(0x24400000,0x3c00000)
 def alloc(self,n):
  out=self.cursor;self.cursor+=(n+15)&~15;assert self.cursor<0x28000000;return out
 def hook(self,u,p,n,d):
  if p==0x7c8e17:
   self.ret(self.alloc(self.read32(u.reg_read(UC_X86_REG_ESP)+4)));return
  super().hook(u,p,n,d)

PALETTE_INPUT_REGIONS=(
 (0x52BBD7,0x52BCBB,'eb31c91111b9024c4a1deea0652075d93bd441e8e1c77995b7fe22f7d2e64539'),
 (0x4355B0,0x4355C9,'b7d215e1d08a46db2474d52c3b3155f5af849cca78017d6a23dd85e3701a994c'),
 # Aligned, forward, nonoverlapping768-byte copy only. The actual original
 # table[0] lands at7CA1E8; other memcpy dispatches remain fail-closed.
 (0x7CA090,0x7CA0CC,'e7ce8d917e3a48b3c8a198facd42829d77db528b4764f8454f88743ad3da8bd7'),
 (0x7CA1E8,0x7CA1EF,'42af23f2392dc1efe1fd06612d07b84d932d0880aee40478b800b90322e3b5d0'),
 (0x48E680,0x48E697,'2d56020327bd9900410b5bbf76b317e28c61f670841b444a48ace4189901f08e'),
 (0x48E6A0,0x48E6DD,'3289cc2e30e88a0d349d8cf03152232de97a80a070340177555a6c6bd9f1832c'),
 (0x420080,0x4200BD,'03531bbb781592da5511c4324bc903d3ecbbe0c0972cc0eea2cbf1f32cc65d8c'),
 # Actual SurfaceVT7E85D4/+70 identity;411630 is a different legacy service.
 (0x4BAD60,0x4BAD64,'74032ad0e931f3c4730df99da43479f9f5315cc898c7c8614278631cb2c16a62'),
)
PALETTE_INPUT_READS=((0x8260C8,13),(0x8260D8,12),(0x7CA1D8,4),(0x7E8644,4))
PALETTE_INPUT_DATA=((0x885780,0x300),(0x886380,0x300),(0x887308,4),
 (0x89ECE8,16),(0x89ECF8,24),(0x88A080,24),(0x8A0DD0,28),
 (0x84E860,3),(0x829D20,4))
PALETTE_ASSETS={
 'UNITSNO.PAL':'c5281f05b0039fb8edb6a91dd61c6493d2de9fc90ab3a9acb442a5e203260f7f',
 'TEMPERAT.PAL':'5903b69868b84f494cfbb4e7100398015ef9775b37726019a0d7b5fb6cb33b55',
}

def initialize_tile_palette(m,*,theater,palette_root):
 """Original selected theater palette file/read/expansion and cache producer.

 Steam supplies this member in ra2.mix/cache.mix. This witness exposes those
 unchanged bytes as one virtual loose file at the Win32 boundary; native
 GameFile/RawFile state, filename, availability, open/read/seek/close execute.
 It does not reproduce archive registration, precedence or the whole545150
 loader. The selected empty-Map placement of545000 still requires joined
 execution evidence; full launch ordering is not claimed.
 """
 if m.image is None or theater!=0 or not m.read32(0x887308):
  raise ValueError('Selected tile palette requires checked temperate state and the retained nonNULL Surface')
 if m.read32(0xA8ED38) or m.read32(0x87F6A8):
  raise ValueError('Selected tile palette must precede Tile construction and populated tile palette cache')
 if m.read32(0x89E410) or m.read32(0xABEFE0):
  raise ValueError('Virtual loose-file control excludes populated search paths/MIX registries; never reset them')
 raw=(Path(palette_root)/'ISOTEM.PAL').read_bytes()
 digest='5d6e40fcd11a592a31494c635d93c21796cfe86a2743f0258b1f7d0aff850795'
 if len(raw)!=768 or hashlib.sha256(raw).hexdigest()!=digest:
  raise ValueError('Authenticated Steam ISOTEM.PAL identity mismatch')
 scene=m.read32(0xA8B230);surface=m.read32(0x887308);counter=m.read32(scene+0x214)
 rngs={'main':0x886B88,'scenario':scene+0x218,'mapgen':0xABE890}
 rng_before={name:bytes(m.u.mem_read(p,0x3F4))for name,p in rngs.items()}
 allocations=len(m.allocation_events);events=[];handles={};next_handle=0x5100
 specs={spec.site:spec for spec in m.image.profile.transports}
 sites=(0x65CC59,0x65CC6F,0x65CBBB,0x65CCB0,0x65CD5D,0x65D0A5)
 if any(site not in specs or site in m.transports for site in sites):
  raise ValueError('Tile palette requires its declared unoccupied Win32 file transport sites')
 def file_transport(call):
  nonlocal next_handle
  args=call.arguments;site=call.spec.site
  if site in (0x65CC59,0x65CBBB):
   name,access,sharing,security,creation,attributes,template=args
   physical=call.read(name,64).split(b'\0')[0].decode('latin1')
   expected=(0x80000000,1,0,3,0x80,0)if site==0x65CC59 else(0x80000000,3,0,3,0x8000080,0)
   if physical.upper()!='ISOTEM.PAL' or tuple(args[1:])!=expected:
    raise ValueError('Native file request exceeds the selected authenticated read-only loose file')
   handle=next_handle;next_handle+=1;handles[handle]=0
   events.append(dict(site=site,api='CreateFileA',name=physical,arguments=list(args[1:]),handle=handle))
   call.return_to_native(handle);return
  if site in (0x65CC6F,0x65CCB0):
   handle,=args
   if handle not in handles:raise ValueError('CloseHandle requires an owned palette handle')
   events.append(dict(site=site,api='CloseHandle',handle=handle,position=handles.pop(handle)))
   call.return_to_native(1);return
  if site==0x65CD5D:
   handle,dest,count,read_count,overlapped=args
   if handle not in handles or dest!=0xABBED0 or count!=768 or overlapped or read_count!=call.sp+0x24:
    raise ValueError('ReadFile exceeds the reviewed768-byte palette request/stack result')
   position=handles[handle];blob=raw[position:position+count]
   call.write(dest,blob);call.write(read_count,dwords(len(blob)));handles[handle]+=len(blob)
   events.append(dict(site=site,api='ReadFile',handle=handle,destination=dest,requested=count,
    bytes=len(blob),position=position,sha256=hashlib.sha256(blob).hexdigest()))
   call.return_to_native(1);return
  if site==0x65D0A5:
   handle,distance,high,origin=args
   if handle not in handles or high or origin not in(0,1,2):raise ValueError('Unsupported palette file seek')
   distance=struct.unpack('<i',dwords(distance))[0]
   position=(0,handles[handle],len(raw))[origin]+distance
   if not 0<=position<=len(raw):raise ValueError('Palette seek exceeds authenticated bytes')
   handles[handle]=position;events.append(dict(site=site,api='SetFilePointer',handle=handle,distance=distance,origin=origin,position=position))
   call.return_to_native(position);return
  raise ValueError('Unsupported tile palette file transport')
 calls={};lighting_args=[]
 def observe(u,p,n,d):
  if p in(0x4739F0,0x473C50,0x473B10,0x545000,0x555DA0,0x48EBF0,0x40C410):calls[hex(p)]=calls.get(hex(p),0)+1
  if p==0x555DA0:
   sp=u.reg_read(UC_X86_REG_ESP);args=list(struct.unpack('<9I',u.mem_read(sp+4,36)))
   if args!=[0xABBED0,0x885780,surface,1000,1000,1000,0,0,53]:
    raise ValueError('Original first theater LightingConvert arguments changed')
   lighting_args.append(args)
 hook=None
 try:
  for site in sites:m.transports[site]=file_transport
  if not any(m.u.mem_read(0x87F698,24)):m.invoke(0x40C1B0,0)
  elif m.read32(0x87F698)!=0x7E186C:raise ValueError('Tile palette cache must retain its original native vector')
  before_cache=bytes(m.u.mem_read(0x87F698,24)).hex()
  hook=m.u.hook_add(UC_HOOK_CODE,observe)
  m.u.reg_write(UC_X86_REG_ESP,SP);m.u.reg_write(UC_X86_REG_ESI,0);m.u.reg_write(UC_X86_REG_EBP,0)
  m.run_native(0x54547F,0x5454EB,count=2_000_000,
   required_addresses=(0x545493,0x4739F0,0x473C50,0x473B10,0x5454E0),
   context=dict(case='physical-temperate-tile-palette',physical_sha256=digest,virtual_loose_file=True))
  assert m.u.reg_read(UC_X86_REG_ESP)==SP and not handles
  assert m.string(SP+0x6B0)=='ISOTEM.PAL' and m.read32(SP+0x3A8+0x14)==0xFFFFFFFF
  file_hex=bytes(m.u.mem_read(SP+0x3A8,0x6C)).hex()
  m.fixture_write(SP,dwords(RET_MAGIC));m.u.reg_write(UC_X86_REG_ESP,SP);m.u.reg_write(UC_X86_REG_ECX,0)
  m.run_native(0x545000,RET_MAGIC,count=30_000_000,timeout_us=60_000_000,
   required_addresses=(0x555DA0,0x48EBF0,0x40C410,0x483E30,0x578350),
   context=dict(case='physical-first-tile-lighting-cache',surface=surface))
 finally:
  if hook is not None:m.u.hook_del(hook)
  for site in sites:m.transports.pop(site,None)
 assert m.read32(scene+0x214)==counter and m.read32(0x887308)==surface
 assert all(bytes(m.u.mem_read(p,0x3F4))==rng_before[name]for name,p in rngs.items())
 assert m.read32(0x87F6A8)==1 and len(lighting_args)==1
 pointer=m.read32(m.read32(0x87F69C))
 m.tile_palette_initialization=dict(theater=theater,filename='ISOTEM.PAL',source_sha256=digest,
  source_bytes=768,source_archive='Steam ra2.mix/cache.mix',native_file_hex=file_hex,events=events,
  expanded_hex=bytes(m.u.mem_read(0xABBED0,768)).hex(),
  expanded_sha256=hashlib.sha256(bytes(m.u.mem_read(0xABBED0,768))).hexdigest(),
  cache_before_hex=before_cache,cache_after_hex=bytes(m.u.mem_read(0x87F698,24)).hex(),
  first_lighting_pointer=pointer,first_lighting_hex=bytes(m.u.mem_read(pointer,0x1B4)).hex(),
  lighting_arguments=lighting_args,calls=calls,allocations=list(m.allocation_events[allocations:]),
  retained_surface=surface,scenario_counter=counter,detail=m.read32(0xA8EB78),
  rng_before={name:v.hex()for name,v in rng_before.items()},
  rng_after={name:bytes(m.u.mem_read(p,0x3F4)).hex()for name,p in rngs.items()},
  boundaries=['Authenticated Steam MIX member is exposed as a virtual loose file at Win32 APIs; archive registration/precedence are not executed.',
   'Selected545150 filename/file/read/expansion seam and full545000 execute; earlier theater loader and outer File destructor are excluded.',
   'Retained declared RGB565/plainCPU Surface service is preserved; no rendered/device parity claim.'])
 return m.tile_palette_initialization

def initialize(m,*,surface_service=None,palette_root=None,inputs_only=False):
 if surface_service is not None:
  # One owner for legacy and checked retained-VM palette initialization.
  # Original6BDCA0..6BDCC2 requires Surface BPP2. Device construction4BA770
  # and format detection are omitted explicit inputs, not executed DirectDraw.
  if surface_service!='rgb565-plain-cpu' or not inputs_only or m.image is None:
   raise ValueError('Only the checked selected RGB565 palette-input stage is enrolled')
  if m.read32(0x887308):raise ValueError('Palette Surface already initialized; never reset retained service state')
  if palette_root is None:raise ValueError('Selected palette input requires authenticated physical files')
  physical=[]
  for name,digest in PALETTE_ASSETS.items():
   raw=(Path(palette_root)/name).read_bytes()
   if len(raw)!=768 or hashlib.sha256(raw).hexdigest()!=digest:
    raise ValueError('Selected official palette identity mismatch: '+name)
   if name in m.assets and m.assets[name]!=raw:raise ValueError('Conflicting retained physical asset: '+name)
   m.assets[name]=raw;physical.append(dict(name=name,bytes=len(raw),sha256=digest))
  scenario=m.read32(0xA8B230);counter=m.read32(scenario+0x214)
  rng=bytes(m.u.mem_read(scenario+0x218,0x3F4))
  allocation_mark=len(m.allocation_events);exit_mark=len(m.exit_registrations);load_mark=len(m.asset_loaded)
  # Actual CRTslots812B30/812B34/8124E8, empty count/capacity and growth10.
  # No generic vtable or supplied spare cache capacity on the selected route.
  for address,size in ((0x89ECE8,16),(0x89ECF8,24),(0x88A080,24)):
   if any(m.u.mem_read(address,size)):raise ValueError('Palette cold state already initialized')
  for address in (0x48E680,0x48E6A0,0x420080):m.invoke(address,0)
  surface=m.alloc(0x24)
  m.fixture_write(surface,dwords(0x7E85D4));m.fixture_write(surface+0x10,dwords(2))
  if m.invoke(0x4BAD60,surface)!=2:raise ValueError('Selected original Surface getter rejected BPP2 input')
  m.fixture_write(0x887308,dwords(surface))
  # RGB565 is a declared format, not implied by BPP2 (RGB555 also has BPP2).
  shifts=(11,3,0,3,5,2)
  for i,value in enumerate(shifts):m.fixture_write(0x8A0DD0+i*4,dwords(value))
  m.fixture_write(0x8A0DE8,struct.pack('<2H',0x7BEF,0xF7DE))
  m.fixture_write(0x829D20,dwords(2));m.fixture_write(0x84E860,bytes(3))
  copies=[]
  def observe_copy(u,p,n,d):
   if p!=0x7CA090:return
   sp=u.reg_read(UC_X86_REG_ESP);dest,source,count=struct.unpack('<3I',u.mem_read(sp+4,12))
   if count!=768 or dest not in (0x886380,0x885780) or dest%4 or not(dest+count<=source or source+count<=dest):
    raise ValueError('Memcpy inputs exceed reviewed aligned768-byte forward closure')
   if u.reg_read(UC_X86_REG_EFLAGS)&0x400:raise ValueError('Selected forward copy requires original cleared DF prior')
   copies.append(dict(destination=dest,source=source,bytes=count,input_sha256=hashlib.sha256(bytes(u.mem_read(source,count))).hexdigest()))
  hook=m.u.hook_add(UC_HOOK_CODE,observe_copy)
  m.u.reg_write(UC_X86_REG_ESP,SP)
  try:m.run_native(0x52BBD7,0x52BCBB,count=2_000_000,
   required_addresses=(0x52BBE3,0x52BC55,0x7CA090,0x7CA1E8,0x4355B0),
   context=dict(case='literal-color-palette-inputs',surface_service=surface_service))
  finally:m.u.hook_del(hook)
  assert m.u.reg_read(UC_X86_REG_ESP)==SP and len(copies)==2
  assert m.read32(scenario+0x214)==counter and bytes(m.u.mem_read(scenario+0x218,0x3F4))==rng
  m.palette_initialization=dict(surface_pointer=surface,surface_bytes=0x24,surface_vtable=0x7E85D4,
   getter=0x4BAD60,bytes_per_pixel=2,service=surface_service,format=2,shifts=list(shifts),masks=[0x7BEF,0xF7DE],
   cpu_flags_hex=bytes(m.u.mem_read(0x84E860,3)).hex(),physical_assets=physical,
   native_loads=list(m.asset_loaded[load_mark:]),native_copies=copies,
   palettes=[dict(name=name,address=address,expanded_hex=bytes(m.u.mem_read(address,768)).hex(),
    expanded_sha256=hashlib.sha256(bytes(m.u.mem_read(address,768))).hexdigest())
    for name,address in (('UNITSNO.PAL',0x886380),('TEMPERAT.PAL',0x885780))],
   cache_headers={hex(address):bytes(m.u.mem_read(address,24)).hex()for address in (0x89ECF8,0x88A080)},
   allocations=list(m.allocation_events[allocation_mark:]),exit_registrations=list(m.exit_registrations[exit_mark:]),
   scenario_counter=counter,scenario_rng_sha256=hashlib.sha256(rng).hexdigest(),
   boundaries=['Physical archive/fileIO supplies authenticated768-byte assets through existing Reader service; original copy/RGB expansion executes.',
    'Surface/device initialization and RGB565/CPU flags are declared inputs; actual SurfaceVT/getter executes, no DirectDraw/startup parity claim.',
    'Original cold caches execute; no Convert/Color construction, cache teardown or whole retail type-prefix chronology is claimed.'])
  return m
 if inputs_only or palette_root is not None:raise ValueError('Selected palette options require an explicit service input')
 u=m.u;surface=m.alloc(0x40);vtable=m.alloc(0x100)
 u.mem_write(surface,dwords(vtable));u.mem_write(surface+0x10,dwords(2))
 u.mem_write(vtable+0x70,dwords(0x411630));u.mem_write(0x887308,dwords(surface))
 u.mem_write(0x89ecf8,dwords(0x7eb6d4,m.alloc(4096),1024,1,0,10))
 # Native startup's empty DynamicVector registries, supplied with spare capacity.
 # Original intensity420140 populates and subsequently reuses this cache.
 u.mem_write(0x88a080,dwords(0x7eb6d4,m.alloc(4096),1024,1,0,10))
 for addr,value in((0x8a0dd0,11),(0x8a0dd4,3),(0x8a0dd8,0),(0x8a0ddc,3),(0x8a0de0,5),(0x8a0de4,2)):
  u.mem_write(addr,dwords(value))
 u.mem_write(0x8a0de8,struct.pack('<2H',0x7bef,0xf7de))
 u.reg_write(UC_X86_REG_ESP,SP);u.reg_write(UC_X86_REG_EBX,0)
 # Full original calls, not injected Convert fields or shade tables.
 run_checked(u,0x52be61,0x52bfce,count=100000000,timeout_us=120000000,
  required_addresses=(0x52be6d,0x52bf26,0x48e740,0x48ebf0,0x4bbb00))
 assert u.reg_read(UC_X86_REG_ESP)==SP
 return m

def initialize_named_colors(m,rules,layers):
 """Original physical Colors read on the retained palette/Rules/Scenario VM.

 No rendering callback replaces the named constructor, shades, blitters or
 intensity cache. Layer caches supply lexical strings in physical source order.
 """
 from collections import Counter
 from tools.rules_oracle.bridge_anim_inputs import physical_sections
 from tools.spatial_oracle.building_body_rules import INI
 if m.image is None or m.read32(0x8871E0)!=rules or not m.read32(0x887308):
  raise ValueError('Named Colors requires retained original Rules and initialized Surface')
 if any(m.u.mem_read(0xB054D0,24)) or m.read32(0xAC48F0):
  raise ValueError('Named Colors cold state must be original fresh BSS; never reset retained caches')
 m.invoke(0x68C330,0)
 scene=m.read32(0xA8B230);counter=m.read32(scene+0x214);rng=bytes(m.u.mem_read(scene+0x218,0x3F4))
 surface=m.read32(0x887308);allocation_mark=len(m.allocation_events)
 observed=Counter();converters=[];current={}
 def observe(u,pc,n,d):
  if pc in (0x66D3A0,0x626AB0,0x68C9C0,0x68C710,0x48E740,0x48EBF0,0x420140,0x7D5408,0x7C9430,0x7DE200,0x7DE440):
   observed[hex(pc)]+=1
  if pc==0x555DA0:
   sp=u.reg_read(UC_X86_REG_ESP);args=list(struct.unpack('<9I',u.mem_read(sp+4,36)))
   assert args[6]==0,('Original named constructor must not delay blitters',args)
   converters.append(dict(pointer=u.reg_read(UC_X86_REG_ECX),arguments=args,layer=current['file']))
 hook=m.u.hook_add(UC_HOOK_CODE,observe);rows=[]
 try:
  for file in layers:
   path=Path(file)
   if not path.is_file():
    if path.name.upper()!='LANGRULE.INI':raise ValueError('Required Colors layer missing: '+str(path))
    rows.append(dict(file=str(path),absent=True));continue
   raw=path.read_bytes();sections=physical_sections(raw,names=('Colors',))
   if any(not name.isascii() or len(name)>255 for name in sections.get('Colors',{})):
    raise ValueError('Physical color names exceed selected ASCII name-cache bound')
   m.make_ini(sections);current['file']=str(path);before=m.read32(0xB054E0)
   mark=len(converters);counts=dict(observed)
   # Same original Reader invocation ABI, with a loop-derived budget: at most
   # 42 retail converters x53 rows x255 entries plus two65536-entry intensity
   # fills.100M instructions covers that body;600s includes Python guards.
   # Larger/different inputs retain the explicit finite budget and fail closed.
   from tools.native_oracle import RET_MAGIC
   m.fixture_write(SP,dwords(RET_MAGIC,INI));m.u.reg_write(UC_X86_REG_ESP,SP);m.u.reg_write(UC_X86_REG_ECX,rules)
   m.run_native(0x66D3A0,RET_MAGIC,count=100_000_000,timeout_us=600_000_000,
    required_addresses=(0x66D3A0,)+( (0x626AB0,0x68C710,0x48E740,0x48EBF0,0x7DE200,0x7DE440)if sections else () ),
    context=dict(case='original-physical-colors-full-convert',file=str(path),lexical_names=list(sections.get('Colors',{}))))
   assert m.u.reg_read(UC_X86_REG_ESP)==SP+8
   assert m.read32(0x887308)==surface and m.read32(scene+0x214)==counter
   assert bytes(m.u.mem_read(scene+0x218,0x3F4))==rng
   rows.append(dict(file=str(path),sha256=hashlib.sha256(raw).hexdigest(),lexical_colors=sections.get('Colors',{}),
    native_return=m.u.reg_read(UC_X86_REG_EAX)&255,registry_count_before=before,registry_count_after=m.read32(0xB054E0),
    converter_calls=converters[mark:],calls={a:n-counts.get(a,0)for a,n in observed.items()if n!=counts.get(a,0)}))
 finally:m.u.hook_del(hook)
 data=m.read32(0xB054D4);count=m.read32(0xB054E0);colors=[]
 for i in range(count):
  p=m.read32(data+i*4);convert=m.read32(p+0x30C)
  assert convert and m.read32(convert+4)==2
  table=m.read32(convert+0x170);shades=m.read32(convert+0x16C);shade_bytes=bytes(m.u.mem_read(table,shades*512))
  colors.append(dict(index=i,pointer=p,ordinal=m.read32(p),name=m.string(m.read32(p+0x304)),
   hsv_hex=bytes(m.u.mem_read(p+0x308,3)).hex(),shade_count=shades,
   palette_sha256=hashlib.sha256(bytes(m.u.mem_read(p+4,768))).hexdigest(),
   color_hex=bytes(m.u.mem_read(p,0x33C)).hex(),convert_pointer=convert,
   convert_hex=bytes(m.u.mem_read(convert,0x1B4)).hex(),shade_table_sha256=hashlib.sha256(shade_bytes).hexdigest(),
   shade_table_hex=shade_bytes.hex(),plain_vtable=m.read32(m.read32(convert+0x88)),rle_vtable=m.read32(m.read32(convert+0x8C))))
 allocations=list(m.allocation_events[allocation_mark:]);previous_end=0
 for event in allocations:
  assert event['size']>0 and previous_end<=event['pointer'] and event['pointer']+event['size']<=m.heap_end
  previous_end=event['pointer']+event['size']
 intensity_data=m.read32(0x88A084);intensity_count=m.read32(0x88A090);intensities=[]
 for i in range(intensity_count):
  p=m.read32(intensity_data+i*4)
  intensities.append(dict(pointer=p,shade_count=m.read32(p+0x20000),refcount=m.read32(p+0x20004),
   table_sha256=hashlib.sha256(bytes(m.u.mem_read(p,0x20000))).hexdigest()))
 return dict(layers=rows,colors=colors,registry_hex=bytes(m.u.mem_read(0xB054D0,24)).hex(),
  hsv_cache_pointer=m.read32(0xAC48F0),convert_registry_hex=bytes(m.u.mem_read(0x89ECF8,24)).hex(),
  intensity_registry_hex=bytes(m.u.mem_read(0x88A080,24)).hex(),intensities=intensities,
  calls=dict(observed),allocations=allocations,allocator_end=m.heap_end,allocator_cursor=m.cursor,
  scenario_counter=counter,scenario_rng_sha256=hashlib.sha256(rng).hexdigest(),
  boundaries=['Full original named Color/Convert/Blitter/shade/intensity construction; no pixel draw or DirectDraw startup claim.',
   'Physical unique lexical caches plus existing allocator/TLS and RGB565/plainCPU/Session BSS inputs are supplied; unsupported input branches fail closed.',
   'No full retail type-prefix/House/SuperWeapon/Unit construction history or gameplay parity claim.'])

def generate():
 m=initialize(PaletteReader({}));u=m.u;rows=[]
 for name,global_address in [('anim.pal',0x87f6c0),('palette.pal',0x87f6c4)]:
  p=m.read32(global_address);table=m.read32(p+0x170);count=m.read32(p+0x16c)
  rows.append(dict(name=name,global_address=hex(global_address),bytes_per_pixel=m.read32(p+4),shade_count=count,
   middle_row=(m.read32(p+0x174)-table)//512,mask_half=m.read32(p+0x180),mask_quarter=m.read32(p+0x184),
   table_sha256=hashlib.sha256(bytes(u.mem_read(table,count*512))).hexdigest(),
   body_plain_vtable=hex(m.read32(m.read32(p+0x88))),body_rle_vtable=hex(m.read32(m.read32(p+0x8c))),
   convert_fields=[hex(m.read32(p+i)) for i in range(0,0x170,4)]))
 return dict(native_sha256=NATIVE_SHA256,loads=m.asset_loaded,rows=rows)

if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--check',type=Path);args=a.parse_args();result=generate()
 if args.check:assert result==json.loads(args.check.read_text());print('PASS original palette startup and full Convert construction')
 else:print(json.dumps(result,indent=2))
