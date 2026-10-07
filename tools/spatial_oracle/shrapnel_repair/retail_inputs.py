"""Original scalar/type readers over declared physical lexical INI caches."""
from pathlib import Path
import hashlib,os,struct
from unicorn.x86_const import *
from tools.rules_oracle.bridge_anim_inputs import Reader
from tools.rules_oracle.bridge_child_sound import Sound
from tools.rules_oracle import theater_general_reader
from tools.rules_oracle.theater_general_reader import TheaterReader,general_text
from tools.projectile_oracle.bridge_render_inputs import lexical
from tools.spatial_oracle.building_body_rules import INI,SP,dwords
from tools.native_oracle import run_checked
HERE=Path(__file__).resolve().parent
ASSETS=Path(os.environ.get('VERA20K_SHRAPNEL_INPUTS', 'target/shrapnel-native-inputs/extract'))

class Rules(Sound):
 hook=Reader.hook
 def __init__(self,*,root=None,profile=None,owner=None,full_rules_constructor=False,rules_pointer=None,retained_type_registries=False):
  if rules_pointer is not None and owner is None:raise ValueError('Retained Rules requires its existing VM owner')
  if retained_type_registries and (owner is None or rules_pointer is None):
   raise ValueError('Retained type registries require their existing VM and initialized Rules receiver')
  self.retained_type_registries=retained_type_registries
  self.registry_adoption=[]
  self.root=Path(root or ASSETS)
  raw=(self.root/'RULESMD.INI').read_bytes();sec,_=lexical(raw,{'OverlayTypes'})
  if owner is None:Reader.__init__(self,self.root,sec,profile=profile)
  else:
   self.owner=owner;self.u=owner.u;self.image=owner.image
   for name in ('fixture_write','run_native','alloc','invoke','read32','string','cstring','make_ini'):
    setattr(self,name,getattr(owner,name))
   owner.assets.update({p.name.upper():p.read_bytes() for p in self.root.iterdir() if p.is_file()})
   self.assets=owner.assets;self.asset_loaded=owner.asset_loaded
   self.sinks=owner.sinks;self.transports=owner.transports;self.transport_events=owner.transport_events
   self.make_ini(sec)
  if retained_type_registries:
   rows=self.adopt_type_registry(0xA83D80,list(sec['OverlayTypes'].values()),'OverlayTypes')
   self.overlay_ptrs=[row['pointer']for row in rows]
  else:
   if owner is None:self.fixture_write(0xA83D80,dwords(0x7EB6D4,self.alloc(256*4),256,1,0,10))
   else:self.invoke(0x4E71E0,0)  # actual OverlayType registry cold owner
   self.block(0x668CE3,0x668D34,{UC_X86_REG_ESI:INI})
   self.overlay_ptrs=[self.read32(self.read32(0xA83D84)+i*4) for i in range(self.read32(0xA83D90))]
  assert len(self.overlay_ptrs)==250
  self.names={i:self.string(p+0x24) for i,p in enumerate(self.overlay_ptrs)}
  self.full_rules_constructor=full_rules_constructor or rules_pointer is not None
  if rules_pointer is not None:
   # Keep the original constructor and prior layer state on this receiver.
   self.rules=rules_pointer
   if self.read32(0x8871E0)!=self.rules:raise ValueError('Retained Rules must already be initialized and bound on this VM')
  else:
   self.rules=self.alloc(0x2000)
   if full_rules_constructor:
    from tools.rules_oracle.weapon_speed_order import construct_rules
    construct_rules(owner or self,pointer=self.rules)
   else:self.block(0x665F3B,0x665F41,{UC_X86_REG_ESI:self.rules,UC_X86_REG_EBX:0})
  self.ctor_cliff=self.u.mem_read(self.rules+0x664,1)[0]
  self.land_names=[self.string(self.read32(0x839D68+i*4)) for i in range(12)]
  self.layers=[]
  # The shared physical owner reads its map-used overlays below. Bridge-only
  # DamageAnim inputs belong to the legacy bridge chain and must not construct
  # unrelated animation types on this retained FV VM.
  bridge_indices=range(74,102) if owner is None else ()
  wanted={self.names[i] for i in bridge_indices}|set(self.land_names)|{'General'}
  map_path=self.map_file if owner is not None else self.root/'XShrapnel.MAP'
  # Inputs owns the single physical layer sequence on a shared VM. Replaying
  # this bridge bootstrap first would duplicate native land/key read order.
  paths=(self.root/'RULESMD.INI',self.root/'LANGRULE.INI',self.root/'MPBattleMD.ini',map_path) if owner is None else ()
  for p in paths:
   name=p.name
   if not p.exists():assert name=='LANGRULE.INI';self.layers.append(dict(file=name,absent=True));continue
   raw=p.read_bytes();sections,lines=lexical(raw,wanted);self.make_ini(sections)
   self.invoke(0x674000,0,(INI,))
   if 'General' in sections:self.block(0x66F1CB,0x66F1EC,{UC_X86_REG_ESI:self.rules,UC_X86_REG_EDI:INI})
   for index in bridge_indices:
    if self.names[index] not in sections:continue
    ptr=self.overlay_ptrs[index]
    self.read_overlay_cell_fields(ptr,INI)
   self.layers.append(dict(file=name,sha256=hashlib.sha256(raw).hexdigest(),cliff=self.u.mem_read(self.rules+0x664,1)[0],sections=sections,source_lines=lines))
 def adopt_type_registry(self,address,expected_names,category):
  """Observe the caller's native typed vector without reconstructing it.

  This host binding is not a native factory or initialization proof. The joined
  producer must retain its executed master/factory receipt; exact header/name
  checks reject a missing or incompatible prior rather than create late types.
  """
  if not self.retained_type_registries:raise ValueError('Type registry adoption was not selected')
  header=bytes(self.u.mem_read(address,24));vtable,data,capacity,flags,count,growth=struct.unpack('<6I',header)
  if not vtable or count>capacity or (count and not data):
   raise ValueError('Retained typed vector is not initialized: '+category)
  rows=[dict(index=i,pointer=self.read32(data+i*4))for i in range(count)]
  if any(not row['pointer']for row in rows):raise ValueError('NULL retained type: '+category)
  for row in rows:row['name']=self.string(row['pointer']+0x24)
  if expected_names is not None and [row['name']for row in rows]!=expected_names:
   raise ValueError('Retained type order/names do not match the selected retail input: '+category)
  self.registry_adoption.append(dict(category=category,address=address,header_hex=header.hex(),rows=rows))
  return rows
 def block(self,a,b,regs):
  self.u.reg_write(UC_X86_REG_ESP,SP)
  for k,v in regs.items():self.u.reg_write(k,v)
  # Actual250-name registration performs the original retained-array searches.
  # Its guarded shared execution needs a longer wall budget than scalar seams;
  # the legacy caller retains its runner default and all instruction limits.
  options=dict(count=6000000)
  if getattr(self,'owner',None) is not None and (a,b)==(0x668CE3,0x668D34):options['timeout_us']=60000000
  self.run_native(a,b,**options)
 def read_overlay_cell_fields(self,pointer,ini,*,physical_post_read=False):
  """Original Overlay cell-key seams, retaining native defaults and stores.

  Physical clear-map inputs also require the native Tiberium Armor/Land
  post-read and the final Rubble store across the unrelated saved-EDI pop.
  ObjectType image/ART reads are a separate input mechanism; they are not
  substituted here and this does not claim the complete Overlay reader.
  """
  self.block(0x5FE798,0x5FE8A6,{UC_X86_REG_ESI:pointer,UC_X86_REG_EBX:ini})
  if physical_post_read:self.block(0x5FE8C9,0x5FE8F1,{UC_X86_REG_ESI:pointer})
  self.block(0x5FE933,0x5FEA09,{UC_X86_REG_ESI:pointer,UC_X86_REG_EBX:ini,UC_X86_REG_EDI:pointer+0x24})
  if physical_post_read:self.block(0x5FEA0A,0x5FEA10,{UC_X86_REG_ESI:pointer})
 def snapshot(self):
  return dict(constructor_cliff=self.ctor_cliff,cliff=self.u.mem_read(self.rules+0x664,1)[0],overlays=[dict(index=i,name=self.names[i],land=self.read32(p+0x298),no_use_tile_land=self.u.mem_read(p+0x2AC,1)[0],tiberium=self.u.mem_read(p+0x2A9,1)[0],wall=self.u.mem_read(p+0x2A8,1)[0]) for i,p in enumerate(self.overlay_ptrs) if 74<=i<=101],land_table_hex=bytes(self.u.mem_read(0x89EA40,12*36)).hex(),layers=self.layers)

def theater():
 raw=(ASSETS/'SNOWMD.INI').read_bytes()
 # The shared reader builds an unused asset cache at construction. Bind it to
 # the same explicit retail directory; restore its module default afterward.
 previous=theater_general_reader.ROOT;theater_general_reader.ROOT=ASSETS
 try:m=TheaterReader()
 finally:theater_general_reader.ROOT=previous
 initial=m.read(general_text(raw));rows=m.reads
 assert m.asset_loaded==[], 'theater scalar witness must not load graphics'
 # The surrounding loader supplies ordinal and cumulative count. Here each
 # physical TilesInSet scalar is parsed by original5276D0; file/TMP admission
 # remains a declared supplied boundary, not a full545150 loader execution.
 sections,_=lexical(raw,{f'TileSet{i:04d}' for i in range(300)})
 r=Rules();r.make_ini(sections);base=0;tiles={};sets=[]
 for ordinal in range(300):
  name=f'TileSet{ordinal:04d}'
  if name not in sections:break
  count=r.invoke(0x5276D0,INI,(r.cstring(name),r.cstring('TilesInSet'),0))
  assert count<1000
  m.project(ordinal,base)
  filename=sections[name]['FileName']
  for j in range(count):tiles[base+j]=filename+str(j+1).zfill(2)+'.sno'
  sets.append(dict(ordinal=ordinal,base=base,count=count,physical=sections[name]));base+=count
 globals_={int(row.get('resolved_global',row['location']),16):m.read32(int(row.get('resolved_global',row['location']),16)) for row in rows}
 return dict(sha256=hashlib.sha256(raw).hexdigest(),general=initial,globals=globals_,sets=sets,tiles=tiles,count=base)
