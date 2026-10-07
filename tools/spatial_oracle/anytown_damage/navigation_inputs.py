"""Native original input readers for the bounded Anytown navigation composition."""
from pathlib import Path
import os,struct,hashlib,json
HERE=Path(__file__).resolve().parent
from . import next_family_native as identity
from .inputs import ASSETS
from tools.spatial_oracle.shrapnel_repair.map_facts import decode_cells
from tools.sidebar_oracle.stock import mix,mix_hash
from tools.spatial_oracle.shrapnel_repair import retail_inputs as ri
from tools.projectile_oracle.bridge_render_inputs import lexical
from tools.rules_oracle.bridge_landing_inputs import Landing
from tools.native_oracle import finish_vectors,provenance,run_checked
from unicorn import UC_HOOK_MEM_READ
from unicorn.x86_const import *
sha=lambda raw:hashlib.sha256(raw).hexdigest()
MAPFILE=ASSETS/'XMP03T4.MAP'

def map_inputs(map_file=None):
 raw=Path(map_file or MAPFILE).read_bytes();sections,cells=decode_cells(raw)
 return raw,sections,cells

def extract_tiles(t, *, theater_archive='isotemp.mix', theater_override='isotemmd.mix', tile_suffix='tem', disjoint_theater_additions=False, theater_primary=None, theater_short=None, theater_extra=None):
 root=Path(os.environ['RA2_DIR']);archive=(root/'ra2.mix').read_bytes();iso=mix(archive)[mix_hash(theater_archive)];members=mix(iso);rows=[];data={}
 for i,name in t['tiles'].items():
  entry=mix_hash(name);raw=members.get(entry)
  if raw is not None:data[i]=raw
  rows.append(dict(tile=i,file=name,entry=f'{entry:08X}',bytes=len(raw) if raw else 0,sha256=sha(raw) if raw else None))
 wanted={mix_hash(name) for name in t['tiles'].values()};yr=(root/'ra2md.mix').read_bytes();outer=mix(yr);checks=[]
 # Init_Theater5349C0 registers the long/short theater archives as well as
 # isometric archives. Wood bridge TMPs reside in TEMPERAT.MIX/SNOW.MIX.
 # Do not infer precedence: fail on queried-name overlap and prove each
 # additional physical winner is unique across the registered archives.
 defaults={'tem':('temperat.mix','tem.mix',()),'sno':('snow.mix','sno.mix',('snowmd.mix',))}
 primary,short,extra=defaults[tile_suffix]
 primary=theater_primary or primary;short=theater_short or short
 extra=extra if theater_extra is None else tuple(theater_extra)
 theater_checks=[];selected=set(members)&wanted
 for name in (*extra,primary,short):
  found=[(source,payload) for source,container in [('ra2.mix',mix(archive)),('ra2md.mix',outer)] if (payload:=container.get(mix_hash(name))) is not None]
  assert len(found)<=1,('ambiguous theater archive container',name)
  if not found:theater_checks.append(dict(archive=name,absent=True));continue
  source,payload=found[0];entries=mix(payload);hits=sorted(set(entries)&wanted)
  assert not (set(hits)&selected),('ambiguous registered primary TMP',name)
  for row in rows:
   entry=int(row['entry'],16)
   if entry in hits:
    blob=entries[entry];data[row['tile']]=blob
    row.update(bytes=len(blob),sha256=sha(blob),source=source+'/'+name)
  selected.update(hits)
  theater_checks.append(dict(archive=source+'/'+name,sha256=sha(payload),unique_primary_hits=hits))
 for name in (theater_override,'isogenmd.mix','genermd.mix','localmd.mix','cachemd.mix'):
  raw=outer[mix_hash(name)];entries=mix(raw);hits=sorted(set(entries)&wanted)
  if disjoint_theater_additions and name==theater_override:
   # The stock SNOW additions have no base-name overlap. This admits unique
   # physical files without claiming to execute the native archive resolver.
   assert not (set(hits)&selected),('ambiguous TMP winner',name)
   for row in rows:
    entry=int(row['entry'],16)
    if entry in hits:
     blob=entries[entry];data[row['tile']]=blob
     row.update(bytes=len(blob),sha256=sha(blob),source='ra2md.mix/'+name)
  else:assert not hits,(name,hits)
  checks.append(dict(archive='ra2md.mix/'+name,sha256=sha(raw),**{f'primary_{tile_suffix}_name_hits':hits}))
 for name in ('expandmd01.mix','langmd.mix','language.mix'):
  raw=(root/name).read_bytes();hits=sorted(set(mix(raw))&wanted);assert not hits,(name,hits);checks.append(dict(archive=name,sha256=sha(raw),**{f'primary_{tile_suffix}_name_hits':hits}))
 loose={p.name.upper() for p in root.iterdir() if p.is_file()}&{n.upper() for n in t['tiles'].values()};assert not loose,loose
 return data,dict(archive='ra2.mix/'+theater_archive,outer_sha256=sha(archive),inner_sha256=sha(iso),members=rows,registered_theater_checks=theater_checks,selected_override_checks=checks,**{f'loose_primary_{tile_suffix}_hits':sorted(loose)})

class Inputs(ri.Rules):
 def __init__(self,t,*,map_file=None,theater_file='TEMPERATMD.INI',damage_overlays=range(205,233),owner=None,root=None,profile=None,full_rules_constructor=False,rules_pointer=None,retained_type_registries=False):
  self.map_file=Path(map_file or MAPFILE);self.theater_file=theater_file;self.damage_overlays=tuple(damage_overlays)
  self.shared_owner=owner
  super().__init__(root=root,profile=profile,owner=owner,full_rules_constructor=full_rules_constructor,rules_pointer=rules_pointer,retained_type_registries=retained_type_registries);self.receipts=[];raw,sections,cells=map_inputs(self.map_file);self.physical=cells;self.map_sections=sections
  # 71D580 produces occupation-coordinate templates for TerrainType creation;
  # it has no registry/ID/RNG effects. The shared selected clear-map route has
  # no Terrain names and must not prepare unused legacy terrain inputs.
  if owner is None or sections.get('Terrain'):self.invoke(0x71D580,0)
  if owner is None:self.fixture_write(0xA8B230,ri.dwords(self.alloc(0x1300)))
  if retained_type_registries:
   if self.read32(0x8871E0)!=self.rules:raise ValueError('Retained physical Rules binding changed')
  else:self.fixture_write(0x8871E0,ri.dwords(self.rules))
  if not self.full_rules_constructor:self.block(0x666DF8,0x666E02,{UC_X86_REG_ESI:self.rules})
  names=sorted({v for k,v,line in sections.get('Terrain',())});self.terrain_ptrs={}
  if retained_type_registries:
   # This selected retained map has no Terrain rows. A terrain placement path
   # needs its own native lookup/admission evidence, never a host name guess.
   if names:raise ValueError('Retained physical adoption currently requires no map Terrain records')
   terrainsec,_=lexical((self.root/'RULESMD.INI').read_bytes(),{'TerrainTypes'})
   self.adopt_type_registry(0xA8E318,list(terrainsec['TerrainTypes'].values()),'TerrainTypes')
  elif owner is None:self.fixture_write(0xA8E318,ri.dwords(0x7EB6D4,self.alloc(1024*4),1024,1,0,10))
  else:self.invoke(0x4E72E0,0)  # actual TerrainType registry cold owner
  for name in names:
   p=self.alloc(0x400);self.invoke(0x71DA80,p,(self.cstring(name),));self.terrain_ptrs[name]=p
  art,_=lexical((self.root/'ARTMD.INI').read_bytes(),set(names));self.make_ini(art);art_ini=bytes(self.u.mem_read(ri.INI,0x40))
  self.building_ptrs={}
  for n in sorted({v.split(',')[1] for k,v,line in sections.get('Structures',())}):
   p=self.alloc(0x1800);self.block(0x45E145,0x45E151,{UC_X86_REG_ESI:p,UC_X86_REG_EBX:0});self.building_ptrs[n]=p
  tibsec,_=lexical((self.root/'RULESMD.INI').read_bytes(),{'Tiberiums'});self.tiberium_ptrs={}
  if retained_type_registries:
   rows=self.adopt_type_registry(0xB0F4E8,list(tibsec['Tiberiums'].values()),'Tiberiums')
   self.tiberium_ptrs={row['name']:row['pointer']for row in rows}
  else:
   if owner is None:self.fixture_write(0xB0F4E8,ri.dwords(0x7EB6D4,self.alloc(256),64,1,0,10))
   else:self.invoke(0x721640,0)  # actual TiberiumType registry cold owner
   for name in tibsec['Tiberiums'].values():
    p=self.alloc(0x200);self.invoke(0x7216C0,p,(self.cstring(name),));self.tiberium_ptrs[name]=p
  self.mtnk=None
  if owner is None:
   self.fixture_write(0xA83CE0,ri.dwords(0x7EB6D4,self.alloc(1024),256,1,0,10));self.mtnk=self.alloc(0xF00);self.invoke(0x7470D0,self.mtnk,(self.cstring('MTNK'),))
  self.terrain_layers=[]
  for name,path in [('RULESMD.INI',self.root/'RULESMD.INI'),('LANGRULE.INI',self.root/'LANGRULE.INI'),('MPBattleMD.ini',self.root/'MPBattleMD.ini'),(self.map_file.name,self.map_file)]:
   if not path.exists():assert name=='LANGRULE.INI';self.receipts.append(dict(file=name,absent=True));continue
   raw=path.read_bytes();lex,_=lexical(raw,set(self.names.values())|set(self.land_names)|{'General'}|set(names)|set(self.tiberium_ptrs)|{'MTNK'}|{v.split(',')[1] for k,v,line in sections.get('Structures',())});self.make_ini(lex)
   rules_ini=self.alloc(0x40);self.fixture_write(rules_ini,bytes(self.u.mem_read(ri.INI,0x40)));self.fixture_write(ri.INI,art_ini)
   self.invoke(0x674000,0,(rules_ini,))
   if 'General' in lex:
    self.block(0x66F1CB,0x66F1EC,{UC_X86_REG_ESI:self.rules,UC_X86_REG_EDI:rules_ini})
    self.block(0x671DD2,0x671DF1,{UC_X86_REG_ESI:self.rules,UC_X86_REG_EDI:rules_ini})
   overlays=[]
   for n,p in self.building_ptrs.items():
    if n in lex:self.block(0x460AA0,0x460AE0,{UC_X86_REG_EBP:p,UC_X86_REG_ESI:rules_ini,UC_X86_REG_EBX:self.cstring(n),UC_X86_REG_EAX:0})
   selected=range(len(self.overlay_ptrs)) if owner is None else sorted({v['overlay'] for v in cells.values()if v['overlay'] is not None}|set(self.damage_overlays))
   for i in selected:
    p=self.overlay_ptrs[i]
    if owner is None:
     if self.invoke(0x5FE770,p,(rules_ini,))&255:overlays.append(i)
    elif self.invoke(0x526810,rules_ini,(p+0x24,)):
     self.read_overlay_cell_fields(p,rules_ini,physical_post_read=True);overlays.append(i)
   for n,p in self.tiberium_ptrs.items():
    if not self.invoke(0x526810,rules_ini,(p+0x24,)):continue
    self.block(0x721AFA,0x721B12,{UC_X86_REG_EAX:self.read32(p+0xB8),UC_X86_REG_ECX:rules_ini,UC_X86_REG_EBX:rules_ini,UC_X86_REG_ESI:p,UC_X86_REG_EDI:p+0x24})
    self.u.reg_write(UC_X86_REG_ESP,ri.SP);self.u.reg_write(UC_X86_REG_EBX,rules_ini);self.u.reg_write(UC_X86_REG_ESI,p);self.u.reg_write(UC_X86_REG_EDI,p+0x24);self.run_native(0x721C3F,(0x721C7B,0x721CDC),count=100000)
   if self.mtnk is not None and 'MTNK' in lex:
    p=self.mtnk;self.block(0x5F94B3,0x5F9516,{UC_X86_REG_EBX:p,UC_X86_REG_ESI:rules_ini,UC_X86_REG_EBP:p+0x24,UC_X86_REG_EAX:self.u.mem_read(p+0x231,1)[0]})
    # Original 712452..712473 reads ThreatAvoidanceCoefficient with the
    # retained Type+2F0 double as default; Foot Unlimbo copies it to Foot+530.
    for a,b in [(0x7121D1,0x7121EB),(0x712270,0x71228A),(0x7122BE,0x7122D8),(0x712452,0x712473),(0x714CC8,0x714CE9)]:self.block(a,b,{UC_X86_REG_EBP:p,UC_X86_REG_ESI:rules_ini,UC_X86_REG_EDI:rules_ini,UC_X86_REG_EBX:p+0x24})
    # Original MovementZone reader loads the INI argument from its retained
    # outer frame after two pushes. Keep its native default/store+5B4 owner.
    self.fixture_write(ri.SP+0x380,ri.dwords(rules_ini));self.block(0x71605E,0x716090,{UC_X86_REG_EBP:p,UC_X86_REG_EBX:p+0x24})
   if self.mtnk is not None:self.block(0x7476D3,0x747711,{UC_X86_REG_EDI:self.mtnk,UC_X86_REG_EBX:rules_ini,UC_X86_REG_EBP:self.mtnk+0x24})
   terrain=[]
   for n,p in self.terrain_ptrs.items():
    if self.invoke(0x71DEA0,p,(rules_ini,))&255:terrain.append(n)
   receipt=dict(file=name,sha256=sha(raw),bytes=len(raw),overlay_admitted=overlays,terrain_admitted=terrain)
   if owner is not None:receipt['overlay_scope']='Selected physical overlay Cell keys and native Tiberium post-read; full ObjectType image/ART reader excluded'
   self.receipts.append(receipt)
  assert all(self.string(p+0x1F8)==n for n,p in self.terrain_ptrs.items()), 'ART alias cache requires expansion'
  self.theater=t
  allnames={f'TileSet{i:04d}' for i in range(300)}
  raw=(self.root/self.theater_file).read_bytes();baselex,_=lexical(raw,allnames);allnames|={v.get('SetName','No Name') for v in baselex.values()};full,_=lexical(raw,allnames);self.make_ini(full);self.tile_properties=[]
  used_tiles={cell['tile'] for cell in cells.values()}
  for row in t['sets']:
   sec=f"TileSet{row['ordinal']:04d}";sn=self.cstring(sec);lex=full[sec];setname=lex.get('SetName','No Name');shadow=self.invoke(0x5295F0,ri.INI,(sn,self.cstring('ShadowCaster'),0))&255;count=self.invoke(0x5276D0,ri.INI,(sn,self.cstring('ShadowTiles'),0)) if shadow else 0
   last=self.invoke(0x5276D0,ri.INI,(sn,self.cstring('LastTilesInSet'),-1));assert last in (0xFFFFFFFF,row['count'])
   animations={}
   for j in range(row['count']):
    if owner is not None and row['base']+j not in used_tiles:continue
    key=f'Tile{j+1:02d}Anim';buffer=self.alloc(128);length=self.invoke(0x528A10,ri.INI,(self.cstring(setname),self.cstring(key),self.cstring(''),buffer,128))
    if length:
     aname=self.string(buffer);ap=self.invoke(0x428B80,self.cstring(aname));index=self.invoke(self.read32(self.read32(ap)+0x40),ap);values={}
     for suffix,default in [('XOffset',0),('YOffset',0),('AttachesTo',-1),('ZAdjust',0)]:
      value=self.invoke(0x5276D0,ri.INI,(self.cstring(setname),self.cstring(f'Tile{j+1:02d}{suffix}'),default));values[suffix]=struct.unpack('<i',ri.dwords(value))[0]
     animations[j]=dict(name=aname,index=index,values=values)
   properties=dict(ordinal=row['ordinal'],base=row['base'],count=row['count'],setname=setname,shadow=shadow,shadow_tiles=count,last_tiles_in_set=last,animations=animations)
   if owner is not None:
    properties['native_property_frame_hex']=row['native_property_frame_hex']
   self.tile_properties.append(properties)
  assert all(not self.u.mem_read(p+0x16BF,1)[0] and not self.u.mem_read(p+0x16C0,1)[0] for p in self.building_ptrs.values())
 @classmethod
 def on_existing_owner(cls,owner,t,*,map_file,theater_file='TEMPERATMD.INI',damage_overlays=(),root=None,full_rules_constructor=False,rules_pointer=None,retained_type_registries=False):
  """Read physical map prerequisites while retaining the Reader VM/allocator.

  The constructor's existing FV type registry and Scenario receiver survive.
  This does not construct a second MTNK or overwrite existing UnitType state.
  """
  if owner.image is None:raise ValueError('Shared physical inputs require an explicit scoped image')
  return cls(t,map_file=map_file,theater_file=theater_file,damage_overlays=damage_overlays,owner=owner,root=root or Path(map_file).parent,full_rules_constructor=full_rules_constructor,rules_pointer=rules_pointer,retained_type_registries=retained_type_registries)
 def guard_dropship_timer(self,*,omitted_reset_timer=True):
  """Fail on a selected consumer of the omitted Scenario Reset timer.

  Reset6838B1..6838CD initializes Scenario+34C0/+34C4/+34C8 before
  its Lighting stores. Its middle word copies an uninitialized Reset local,
  not the6C8C40 clock result. This isolated Lighting owner does not execute
  full Reset or supply that timer. The read-only guard survives subsequent
  House/Unit calls on the same VM and rejects any reached dependency.
  With omitted_reset_timer=False the caller has already executed original
  Scenario initialization; the same guard bounds this path to no Dropships.
  """
  if self.shared_owner is None:raise ValueError('Scoped timer boundary requires the existing VM owner')
  owner=self.shared_owner;scenario=self.read32(0xA8B230);start=scenario+0x34C0
  state=getattr(owner,'_physical_dropship_timer_boundary',None)
  if state is not None:
   if state['address']!=start:raise ValueError('Scenario changed under retained timer boundary')
   if bool(state['omitted_native_stores'])!=omitted_reset_timer:raise ValueError('Scenario timer initialization policy changed')
   return state
  state=dict(address=start,bytes=12,initial_hex=bytes(self.u.mem_read(start,12)).hex(),
             native_reads=0,omitted_native_stores=['0x6838bc','0x6838c7','0x6838ca'] if omitted_reset_timer else [])
  def reject_read(uc,access,address,size,value,data):
   if address<start+12 and address+size>start:
    state['native_reads']+=1
    raise RuntimeError(f'Excluded Scenario Dropship timer consumer at {address:#x}, PC={uc.reg_read(UC_X86_REG_EIP):#x}')
  # Include nearby starts so an original scalar/x87 read overlapping the
  # timer cannot evade the assertion by beginning before its first byte.
  owner._physical_dropship_timer_hook=self.u.hook_add(UC_HOOK_MEM_READ,reject_read,begin=start-64,end=start+11)
  owner._physical_dropship_timer_boundary=state
  return state
 def read_map_lighting(self,*,initialize_defaults=True):
  """Original Scenario defaults and twelve map Lighting reads on this VM.

  Original6838C2..6838C7 produces100, then6838CD..68396D stores defaults;
  68A817..68AAE6 executes normal
  and Ion reads with native float/default/ftol semantics. Full Scenario
  construction, transitions and palette initialization remain outside this
  isolated map prerequisite. The same Scenario and RNG receiver survives.
  initialize_defaults=False retains defaults from the caller's executed
  Scenario constructor/Reset; this reader never reconstructs that state.
  """
  if self.shared_owner is None:raise ValueError('Scoped lighting requires a shared physical owner')
  scenario=self.read32(0xA8B230)
  boundary=self.guard_dropship_timer(omitted_reset_timer=initialize_defaults)
  raw=Path(self.map_file).read_bytes();basic,_=lexical(raw,{'Basic'})
  if any(key.casefold()=='startingdropships' for key in basic.get('Basic',{})):
   raise ValueError('Selected Lighting boundary excludes authored StartingDropships')
  if initialize_defaults:
   self.block(0x6838C2,0x6838C7,{UC_X86_REG_EBP:scenario,UC_X86_REG_EBX:0})
   # Retain actual EAX100 from the preceding original MOV. Only the unrelated
   # timer stores are omitted; the native StartingDropships zero store remains.
   self.block(0x6838CD,0x68396D,{UC_X86_REG_EBP:scenario,UC_X86_REG_EBX:0})
  assert self.read32(scenario+0x34D0)==0
  assert bytes(self.u.mem_read(boundary['address'],12)).hex()==boundary['initial_hex']
  raw=Path(self.map_file).read_bytes();sections,_=lexical(raw,{'Lighting'})
  self.make_ini(sections)
  self.block(0x68A817,0x68AAE6,{UC_X86_REG_ESI:scenario,UC_X86_REG_EDI:ri.INI})
  return dict(file=Path(self.map_file).name,sha256=sha(raw),
              default_entry='0x6838c2' if initialize_defaults else None,reader_entry='0x68a817',
              default_store_entry='0x6838cd' if initialize_defaults else None,starting_dropships=0,
              starting_dropships_key_absent=True,dropship_timer_boundary=dict(boundary),
              fields_3528_355c=list(struct.unpack('<14i',self.u.mem_read(scenario+0x3528,56))),
              palette_initialized=bool(self.read32(0x887308)))
 def read_map_theater(self,map_file=None,*,ini_pointer=None):
  # Full_Init687631..68764F executes the exact Map/Theater read, original
  # 475870 -> 528A10 -> 48DBE0 lookup and Scenario+1258 store. The surrounding
  # Scenario allocation and lexical INI cache remain declared host boundaries.
  source=Path(map_file or self.map_file);raw=source.read_bytes()
  if ini_pointer is None:
   # Historical isolated callers retain their default receiver and supplier.
   lex,_=lexical(raw,{'Map'});pointer=ri.INI;self.make_ini(lex)
  else:
   # Live startup retains ART/root Rules. Prepare only a distinct Map cache;
   # original INI/type/scalar readers remain the result authority. Reject
   # duplicate physical sections/keys rather than select a host winner.
   from tools.rules_oracle.bridge_anim_inputs import physical_sections
   if ini_pointer==ri.INI:raise ValueError('Explicit Map receiver must be distinct from global ART')
   lex=physical_sections(raw,names=('Map',));pointer=ini_pointer;self.make_ini(lex,pointer=pointer)
  scenario=self.read32(0xA8B230);before=self.read32(scenario+0x1258)
  self.u.reg_write(UC_X86_REG_ESP,ri.SP);self.u.reg_write(UC_X86_REG_EBP,pointer);self.u.reg_write(UC_X86_REG_EBX,0)
  options={}if ini_pointer is None else dict(context=dict(case='physical-map-theater-prerequisite',source=str(source),map_sha256=sha(raw),ini_pointer=pointer))
  self.run_native(0x687631,0x68764F,count=6000000,**options)
  result=dict(map_sha256=sha(raw),section='Map',key='Theater',default=0,
              source_value=lex.get('Map',{}).get('Theater'),before=before,
              value=self.read32(scenario+0x1258),reader='0x475870',
              lookup='0x48DBE0',caller='0x687631..0x68764F',field='Scenario+0x1258')
  if ini_pointer is not None:result.update(source=str(source),ini_pointer=pointer,ini_allocation_bytes=0x58,
      native_entry=0x687631,native_end=0x68764F,
      supplier_boundary='Unique physical Map-only lexical cache; no map Rules layering or native file-loader claim.')
  return result
 def snapshot(self):
  used=sorted({c['overlay'] for c in self.physical.values() if c['overlay'] is not None}|set(self.damage_overlays))
  terrains={}
  for n,p in self.terrain_ptrs.items():
   row=Landing.terrainstate(self,p);f=self.read32(p+0x2B8);cells=[]
   for i in range(10):
    pair=list(struct.unpack('<hh',self.u.mem_read(f+i*4,4)))
    if pair==[32767,32767]:break
    cells.append(pair)
   else:raise AssertionError(('unterminated Terrain occupy list',n))
   row.update(image=self.string(p+0x1F8),occupy_list=cells,map_occupied=self.u.mem_read(p+0x235,1)[0]);terrains[n]=row
  result=dict(art_sha256=sha((self.root/'ARTMD.INI').read_bytes()),bootstrap_layers=[dict(file=v['file'],absent=v.get('absent',False),sha256=v.get('sha256'),sections=sorted(v.get('sections',{}))) for v in self.layers],mtnk=dict(strength=self.read32(self.mtnk+0xA0),speed_type=self.read32(self.mtnk+0x67C),movement_zone=self.read32(self.mtnk+0x5B4),crusher=self.u.mem_read(self.mtnk+0xD28,1)[0]) if self.mtnk is not None else None,tiberiums={n:dict(index=self.read32(p+0x98),value=self.read32(p+0xB8),base_overlay=self.read32(self.read32(p+0xE0)+0x294),images=self.read32(p+0xE8),extra=self.read32(p+0xEC)) for n,p in self.tiberium_ptrs.items()},building_zone_gate_bytes={n:bytes(self.u.mem_read(p+0x16BF,2)).hex() for n,p in self.building_ptrs.items()},tile_properties=self.tile_properties,layers=self.receipts,cliff=self.u.mem_read(self.rules+0x664,1)[0],land_table_hex=bytes(self.u.mem_read(0x89EA40,432)).hex(),overlays=[dict(index=i,name=self.names[i],land=self.read32(self.overlay_ptrs[i]+0x298),crushable=self.u.mem_read(self.overlay_ptrs[i]+0x22D,1)[0],wall=self.u.mem_read(self.overlay_ptrs[i]+0x2A8,1)[0],tiberium=self.u.mem_read(self.overlay_ptrs[i]+0x2A9,1)[0],no_use_tile_land=self.u.mem_read(self.overlay_ptrs[i]+0x2AC,1)[0],rubble=self.u.mem_read(self.overlay_ptrs[i]+0x2B4,1)[0],rock=self.u.mem_read(self.overlay_ptrs[i]+0x2B5,1)[0]) for i in used],terrains=terrains)
  if self.retained_type_registries:result['registry_adoption']=self.registry_adoption
  return result
