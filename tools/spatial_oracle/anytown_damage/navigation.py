"""Original full Anytown navigation graphs, deriving Cell inputs through original readers/Recalc."""
from .navigation_inputs import *
from .navigation_publication import finish_vectors
from .anytown_geometry import Geometry,inputs as crop_inputs,sr
from tools.spatial_oracle.shrapnel_repair.zone_composition import ConnectivityRepair,BASE,PLANE
from tools.spatial_oracle.shrapnel_repair.hierarchy_composition import HierarchyRepair
from tools.spatial_oracle.bridge_rim import TABLE,CELLS,DUMMY,MAP,COORD
from tools.native_oracle import run_checked,RET_MAGIC,STACK_BASE,STACK_SIZE
from tools.spatial_oracle.map_queries import packed,dwords,normalize
from collections import Counter
from unicorn import UC_HOOK_CODE
import copy

class Navigation(Geometry):
 allocate=ConnectivityRepair.allocate
 nav_snapshot=ConnectivityRepair.nav_snapshot
 graph_snapshot=HierarchyRepair.graph_snapshot
 dummy_snapshot=HierarchyRepair.dummy_snapshot
 @staticmethod
 def initialize_dummy_crt(owner):
  """Original13 Cell CRT owners then813AAC/565060 before Scenario publication.

  This is distinct from the later5670E7..5670F2 Resize reconstruction on the
  same fixed address. Cell47BC66/47BD8F passes receiver+4 to410230; its
  callee+0x0C store assigns Cell+0x10 coldID0. No late counter
  reset or copy of a donor Cell establishes this initialization.
  """
  if owner.image is None or owner.read32(0xA8B230):
   raise ValueError('Cold default Cell must precede publication on its checked VM')
  if getattr(owner,'physical_dummy_startup',None) is not None or any(owner.u.mem_read(DUMMY,0x148)):
   raise ValueError('Cold default Cell already initialized; never reconstruct it as startup')
  if owner.read32(0x813AAC)!=0x565060:raise ValueError('Original default Cell CRT slot changed')
  before={name:bytes(owner.u.mem_read(p,0x3F4))for name,p in(('main',0x886B88),('mapgen',0xABE890))}
  # Reuse the one Cell CRT execution owner. Palette545000 reads the default
  # Cell height, so the13 original producers must precede its constructor,
  # rather than being reset later when the physical map adopts this VM.
  cell_startup=getattr(owner,'physical_cell_startup',None)
  table=bytes(owner.u.mem_read(0x8129FC,52)).hex()
  if cell_startup is None:
   static_before=bytes(owner.u.mem_read(0x89E720,0xA4)).hex()
   cell_startup=sr.initialize_cell_crt(owner,include_null_cell=True)
   cell_startup.update(executed=True,unpublished_scenario=True,table_hex=table,
      static_globals_address=0x89E720,static_globals_bytes=0xA4,
      static_globals_before_hex=static_before,
      static_globals_after_hex=bytes(owner.u.mem_read(0x89E720,0xA4)).hex())
   owner.physical_cell_startup=cell_startup
  elif not(cell_startup.get('executed')and cell_startup.get('unpublished_scenario')and
           cell_startup.get('table_hex')==table):
   raise ValueError('Cold default Cell requires an executed original Cell CRT receipt on its retained VM')
  mark=len(owner.exit_registrations);owner.invoke(0x565060,0)
  assert owner.read32(0xA8B230)==0 and owner.read32(DUMMY+0x10)==0
  assert owner.exit_registrations[mark:]==[0x565080]
  assert all(bytes(owner.u.mem_read(p,0x3F4))==before[name]for name,p in(('main',0x886B88),('mapgen',0xABE890)))
  owner.physical_dummy_startup=dict(entry=0x565060,crt_slot=0x813AAC,constructor=0x47BBF0,
   pointer=DUMMY,executed=True,unpublished_scenario=True,native_id=0,native_id_offset=0x10,abstract_id_receiver_offset=4,
   native_hex=bytes(owner.u.mem_read(DUMMY,0x148)).hex(),exit_registration=0x565080,
   cell_startup=cell_startup,
   rng_before={name:v.hex()for name,v in before.items()},
   rng_after={name:bytes(owner.u.mem_read(p,0x3F4)).hex()for name,p in(('main',0x886B88),('mapgen',0xABE890))})
  return owner.physical_dummy_startup
 @classmethod
 def on_existing_map(cls,owner,*,size,class_height_plane):
  """Join native graphs to an existing VM and declared admitted map prior.

  Cell membership, dimensions and the class/height bytes are caller inputs,
  not answers to a path query. Original connectivity/hierarchy and all later
  pathfinding execute. The existing runtime owns every allocation and hook.
  """
  from types import MethodType
  m=cls.__new__(cls);m.owner=None;m.uc=owner.u;m.case=dict(size=list(size))
  m.width=sum(size);m.side=m.width+1
  assert list(struct.unpack('<2i',m.uc.mem_read(MAP+0xF4,8)))==list(size)
  assert len(class_height_plane)==m.side*m.side*4
  m.allocate=owner.allocate;m.call=MethodType(ConnectivityRepair.call,m)
  m.uc.mem_map(0x44000000,0x800000)
  m.uc.mem_write(BASE,class_height_plane)
  m.uc.mem_write(MAP+0x68,dwords(BASE,m.side*m.side,PLANE))
  return m
 @staticmethod
 def setup_pathfinder(call):
  """Original shared workspace producer; call transport owns execution budget.

  42A6D0 constructs the global, 42AC00 sizes its map arrays, and 42C1C0
  derives scratch from retained native hierarchy. No query result is supplied.
  """
  call(0x49F3A0,this=0)
  call(0x42A6D0,this=0x87E8B8)
  call(0x42AC00,this=0x87E8B8,args=(MAP+0xEC,))
  call(0x42C1C0,this=0x87E8B8)
 def __init__(self,r,t,tiles,*,case=None,create_actor=True,actor_coord=(87,53),actor_height=4,admission_cells=None,stages=None,scenario_theater=None,cell_inputs_only=False,rng_seed=0):
  self.owner=None
  self._bootstrap(r,t,tiles,case=case,create_actor=create_actor,actor_coord=actor_coord,actor_height=actor_height,admission_cells=admission_cells,stages=stages,scenario_theater=scenario_theater,cell_inputs_only=cell_inputs_only,rng_seed=rng_seed)
 @classmethod
 def on_physical_map(cls,owner,t,tiles,*,case,map_file,inputs=None,create_actor=False,scenario_theater=None,cell_inputs_only=False,rng_seed=0,scenario_initialization=None,full_graph_timeout_us=60000000):
  """Retain original physical Cell/TMP/graph algorithms on one Reader VM.

  The existing owner retains the allocator, scoped image, import transports and
  sink lifetime. No guest heap, registries, scenario or code is donor-copied.
  An executed Scenario initialization receipt retains its original defaults.
  A per-stream seed dictionary can retain its RNG while
  executing original Seed for separately declared Main/MapGen inputs.
  """
  if owner.image is None:raise ValueError('Physical shared map requires an explicit scoped image')
  if create_actor:raise ValueError('Shared physical map does not construct a second actor')
  if full_graph_timeout_us not in (60000000,300000000):raise ValueError('Unsupported physical graph execution budget')
  r=owner if inputs is None else inputs
  if r.u is not owner.u or r.image is not owner.image:raise ValueError('Physical inputs must retain the same VM and scoped image')
  if Path(r.map_file).resolve()!=Path(map_file).resolve():raise ValueError('Physical inputs must name the selected map')
  initialize_lighting_defaults=scenario_initialization is None
  if scenario_initialization is not None:
   from tools.spatial_oracle.fv_cell_attack.steam_movement_profile import NATIVE_SCENARIO_BYTES
   if not (scenario_initialization['executed'] and scenario_initialization['ctor']==0x6832C0
           and scenario_initialization['reset']==0x683610
           and scenario_initialization['allocation_pointer']==owner.read32(0xA8B230)
           and scenario_initialization['allocation_bytes']==NATIVE_SCENARIO_BYTES
           and scenario_initialization['unpublished_during_ctor']):
    raise ValueError('Physical defaults require the same executed original Scenario receiver')
  m=cls.__new__(cls);m.owner=owner;m.uc=m.u=owner.u;m.image=owner.image
  m.full_graph_timeout_us=full_graph_timeout_us
  r.guard_dropship_timer(omitted_reset_timer=initialize_lighting_defaults)  # retained across Map/Cell and later joined Unit calls
  m.allocate=owner.alloc;m.map_file=Path(map_file);m.phase='measure';m.trace=[];m.events=m.trace
  m.pending={};m.reached={};m.writes=[];m.stage='physical_navigation'
  from tools.spatial_oracle.bridge_rim import FAMILIES
  m.family=FAMILIES['high'];m.bootstrap={};m.cell_startup={}
  m.code_hash=sha(bytes(m.u.mem_read(0x401000,0x3E0000)))
  for base,size in ((CELLS,0x2000000),(0x44000000,0x800000),(0x48000000,0x8000000)):
   m.u.mem_map(base,size)
  m.u.hook_add(UC_HOOK_CODE,m.observe)
  m._bootstrap(r,t,tiles,case=case,create_actor=False,scenario_theater=scenario_theater,cell_inputs_only=cell_inputs_only,rng_seed=rng_seed,initialize_lighting_defaults=initialize_lighting_defaults)
  return m
 def fixture_write(self,address,blob):
  if self.owner is None:self.uc.mem_write(address,blob)
  else:self.owner.fixture_write(address,blob)
 def call(self,address,this=MAP,args=(),count=30000000,timeout_us=60000000):
  if self.owner is None:return ConnectivityRepair.call(self,address,this,args,count)
  from tools.spatial_oracle.building_body_rules import SP
  self.fixture_write(SP,dwords(RET_MAGIC,*args));self.uc.reg_write(UC_X86_REG_ESP,SP);self.uc.reg_write(UC_X86_REG_ECX,this)
  self.owner.run_native(address,RET_MAGIC,count=count,timeout_us=timeout_us,context=dict(case='physical_navigation',activity=self.activity))
  return self.uc.reg_read(UC_X86_REG_EAX)
 def physical_constructor_state(self):
  """Observe retained constructor ID/RNG state; never supplies native input."""
  scenario=self.owner.read32(0xA8B230)
  return dict(scenario_counter=self.owner.read32(scenario+0x214),
              rng={name:sr.rng_state(self.uc,pointer)for name,pointer in self.rngs.items()})
 def _bootstrap(self,r,t,tiles,*,case=None,create_actor=True,actor_coord=(87,53),actor_height=4,admission_cells=None,stages=None,scenario_theater=None,cell_inputs_only=False,rng_seed=0,initialize_lighting_defaults=True):
  self.create_actor=create_actor;self.actor_coord=actor_coord;self.actor_height=actor_height
  self.admission_cells=admission_cells if admission_cells is not None else [(87,53),(86,54),(87,54),(88,54),(87,55),(85,54),(89,54)]
  self.stages=stages;self.tile_count=t['count']
  case=copy.deepcopy(case) if case is not None else crop_inputs(t);raw,sections,physical=map_inputs(r.map_file);case['cells']=[[*c,p['tile'],p['subtile'],0,p['overlay'],p['frame'],None,p['level'],0] for c,p in sorted(physical.items(),key=lambda kv:(kv[0][1],kv[0][0]))];case['supplied_cells']=[];case['boundary']='Physical full-diamond tile/subtile/level/ice/overlay/frame supplied from MAP bytes; original Cell constructor and Recalc derive runtime land/slope/class. Actual native scenario/file loader, actor command dispatch and projectile admission excluded.'
  if self.owner is None:case['local_size']=normalize(case['size'],case['local_size'])['normalized']
  self.activity='bootstrap';self.counters=Counter();self.illegal=[];self.range_pending=[];self.used_tile_heads=set();self.tile_image_getter=None
  self.native_final_init_started=False
  if self.owner is None:super().__init__(case)
  else:
   self.case=case
   from tools.spatial_oracle.bridge_rim import OriginalRim
   self.rngs={'main':0x886B88,'scenario':r.read32(0xA8B230)+0x218,'mapgen':0xABE890}
   self.construction_history={'map':dict(before=self.physical_constructor_state())}
   # Original Map constructor and Init create the retained typed vectors and
   # cell pointer table using the existing guest allocator. Authored fields
   # below populate this actual table; graph headers are never manufactured.
   self.call(0x565090)
   self.call(0x565800)
   self.construction_history['map']['after']=self.physical_constructor_state()
   self.cell_table_address=r.read32(MAP+0x13C)
   assert self.cell_table_address and r.read32(MAP+0x140)==0x40000
   OriginalRim.prepare_map(self,case)
   self.normalization=normalize(case['size'],case['local_size'],owner=self.owner,map_pointer=MAP)
   case['local_size']=self.normalization['normalized']
   # Isolated physical setup precedes Unit construction. Original Seed fills
   # each actual retained receiver; caller seed0 is not full load chronology.
   if isinstance(rng_seed,dict):
    if set(rng_seed)!=set(self.rngs):raise ValueError('Native seed policy must name all three retained streams')
    self.seed_inputs=dict(rng_seed)
   else:self.seed_inputs={name:rng_seed for name in self.rngs}
   # None preserves a caller's already-initialized map/House/Unit chronology.
   # The isolated control defaults to original Seed0 before all map work.
   if any(seed is not None and (not isinstance(seed,int) or not 0<=seed<=0xFFFFFFFF)
          for seed in self.seed_inputs.values()):raise ValueError('Native seed must be a u32 or None')
   for name,pointer in self.rngs.items():
    seed=self.seed_inputs[name]
    if seed is not None:self.call(0x65C6D0,this=pointer,args=(seed,))
   self.construction_history['seed']=dict(input=dict(self.seed_inputs) if isinstance(rng_seed,dict) else rng_seed,
                                          after=self.physical_constructor_state())
   if getattr(r,'retained_type_registries',False):
    cold=getattr(r,'physical_cell_startup',None)
    if not(cold and cold.get('executed')and cold.get('unpublished_scenario')and
           cold.get('table_hex')==bytes(u.mem_read(0x8129FC,52)).hex()):
     raise ValueError('Retained physical map requires its original pre-Scenario Cell CRT receipt')
    # This is an observation of retained native fields, never a copied Cell
    # prior or a second execution of cold initializers after Rules readers.
    self.cell_startup=dict(cold,adopted=True,
       retained_static_globals_hex=bytes(u.mem_read(0x89E720,0xA4)).hex())
   else:self.cell_startup=sr.initialize_cell_crt(self,include_null_cell=True)
   self.call(0x49F2F0,this=0)  # original eight neighbor-coordinate table
   self.call(0x49F3A0,this=0)  # original world-coordinate direction table
   self.call(0x40AFA0,this=0)  # actual global Pathfinder cold constructor
   if getattr(r,'retained_type_registries',False):
    # The same pre-Scenario CRT Cell is used by original545000. The later
    # selected Resize projection still reconstructs it after all real Cells.
    cold=getattr(self.owner,'physical_dummy_startup',None)
    if not cold or not(cold['executed']and cold['pointer']==DUMMY and cold['native_id']==0):
     raise ValueError('Retained physical palette requires the original pre-Scenario default Cell')
    from tools.projectile_oracle.bridge_render_inputs_palette import initialize_tile_palette
    self.construction_history['tile_palette']=initialize_tile_palette(self.owner,
       theater=scenario_theater['value'],palette_root=Path(os.environ.get('VERA20K_FV_TILE_PALETTES',
        '.local/fv-movement-validation/tile-palette/extract')))
   # Original568BB0 visits the Anim instance vector before its Cell pass.
   # Execute the actual empty registry owners, not image-zero headers.
   assert r.read32(0xA8E9B8)==0
   self.call(0x4E6D60,this=0)  # actual empty Anim instance collection
   if getattr(r,'retained_type_registries',False):
    # 4E74E0 owns AnimType, not Anim instances. Typed master startup already
    # constructed this populated vector; never erase its original members.
    r.adopt_type_registry(0x8B4150,None,'AnimTypes')
   else:
    assert r.read32(0x8B4160)==0
    self.call(0x4E74E0,this=0)
   self.call(0x554640,this=0)  # actual empty LightSource collection
   self.construction_history['lighting']=dict(before=self.physical_constructor_state())
   self.scenario_lighting=r.read_map_lighting(initialize_defaults=initialize_lighting_defaults)
   self.construction_history['lighting']['after']=self.physical_constructor_state()
   assert self.construction_history['lighting']['before']==self.construction_history['lighting']['after']
   self.fixture_write(MAP+0x124,dwords(1,1,sum(case['size'])-1,sum(case['size'])-1))
  u=self.uc;self.width=sum(case['size']);self.side=self.width+1;self.physical=physical
  if scenario_theater is not None:
   if self.owner is None:self.fixture_write(sr.u32(u,0xA8B230)+0x1258,dwords(scenario_theater['value']))
   else:assert sr.i32(u,sr.u32(u,0xA8B230)+0x1258)==scenario_theater['value']
  if self.owner is None:
   u.mem_map(0x24000000,0x400000);self.fixture_write(0x24000000,bytes(r.u.mem_read(0x24000000,0x400000)))
   u.mem_map(0x44000000,0x800000);u.mem_map(0x48000000,0x8000000)
   for a,n in [(0xA83D80,24),(0xA8E318,24),(0x8B4150,24),(0xB0F4E8,24),(0xB0EDC0,0x1000),(0x89EA40,12*36)]:self.fixture_write(a,bytes(r.u.mem_read(a,n)))
  if self.owner is not None and getattr(r,'retained_type_registries',False):
   assert r.read32(0x8871E0)==r.rules
  else:self.fixture_write(0x8871E0,dwords(r.rules))
  if self.owner is None:
   self.fixture_write(MAP+0x68,dwords(BASE,self.side*self.side,PLANE));self.fixture_write(BASE,b'\x07\x00\x00\x00'*(self.side*self.side))
  self.activity='cell_ctor'
  if self.owner is not None:self.construction_history['cells']=dict(before=self.physical_constructor_state())
  for c,p in self.ptrs.items():
   self.call(0x47BBF0,this=p,count=2000);v=physical[c];self.fixture_write(p+0x24,packed(*c));self.fixture_write(p+0x38,dwords(v['tile']));self.fixture_write(p+0x44,dwords(v['overlay'] if v['overlay'] is not None else -1));self.fixture_write(p+0x11A,bytes([v['subtile'],v['level']]));self.fixture_write(p+0x11E,bytes([v['frame']]));self.fixture_write(p+0x119,bytes([v['ice']]))
  self.call(0x47BBF0,this=DUMMY,count=2000)
  if self.owner is not None:
   # Original47BD90 ->410230 ->68BCB0 increments the Scenario ID cursor.
   # Existing Rustnative_identity::resize_constructor_count owns the matching
   # physical-cell plus retained-dummy count; no tile contribution is assumed.
   self.construction_history['cells'].update(after=self.physical_constructor_state(),
      physical_count=len(self.ptrs),dummy_count=1,
      physical_native_ids=[self.owner.read32(p+0x10)for p in self.ptrs.values()],
      dummy_native_id=self.owner.read32(DUMMY+0x10))
   # Preserve reached constructor observations in the owned raw log even if
   # a later Tile/TMP/graph prerequisite fails before the final artifact.
   print(json.dumps(dict(stage='physical_cell_constructors',
      lighting=self.scenario_lighting,
      construction_history={k:v for k,v in self.construction_history.items()if k!='tiles'})),flush=True)
  self.tile_image_getter=sr.u32(u,0x7ECC48+0x9C)
  self.activity='tile_ctor'
  if self.owner is not None:self.construction_history['tiles']=dict(before=self.physical_constructor_state())
  if self.owner is None:self.fixture_write(0xA8ED28,dwords(0x7EB6D4,0x44000000,t['count'],1,0,10))
  else:self.call(0x4E76E0,this=0)  # actual IsoTileType registry cold owner
  # The shared VM already contains FV in the original Abstract/ObjectType
  # registry. Retain its original header and growth owner for appended tiles.
  if self.owner is None:self.fixture_write(0xB0F670,dwords(0x7EB6D4,self.allocate(4096*4),4096,1,0,10))
  for a,v in t['globals'].items():self.fixture_write(a,dwords(v))
  data=0x48000000
  shadow_bases=[v['base'] for v in r.tile_properties if v['shadow']]
  assert len(shadow_bases)<=5
  if self.owner is None:self.fixture_write(0xAA102C,dwords(*(shadow_bases+[0]*(5-len(shadow_bases)))))
  self.tile_properties={v['base']+j:v for v in r.tile_properties for j in range(v['count'])}
  for i,name in t['tiles'].items():
   p=0x44480000+i*0x400
   if self.owner is None:
    name_pointer=COORD+0x100;self.fixture_write(name_pointer,name[:-4].encode('ascii')+b'\0')
   else:name_pointer=self.owner.cstring(name[:-4])
   # Four actual registry grows copy their retained capacities through six
   # native instructions/pointer.838 heads can exceed the legacy10k cap;
   # checked shared execution retains its60s limit and exact code/data scope.
   self.call(0x5447C0,this=p,args=(i,-65,0,name_pointer,0),count=10000 if self.owner is None else 100000)
   properties=self.tile_properties[i]
   if self.owner is None:self.fixture_write(p+0x2E1,bytes([int(bool(properties['shadow'] and properties['shadow_tiles']))]))
   else:
    from tools.rules_oracle.theater_general_reader import TheaterReader
    TheaterReader.publish_tile_properties(self.owner,p,properties['native_property_frame_hex'])
   anim=properties['animations'].get(i-properties['base'])
   if anim:self.fixture_write(p+0x2C8,dwords(anim['index'],anim['values']['XOffset'],anim['values']['YOffset'],anim['values']['AttachesTo'],anim['values']['ZAdjust']))
   raw=tiles.get(i)
   if raw:
    tmp=bytearray(raw);w,h=struct.unpack_from('<II',tmp)
    for j in range(w*h):
     off=struct.unpack_from('<I',tmp,16+j*4)[0]
     if off:struct.pack_into('<I',tmp,16+j*4,data+off)
    self.fixture_write(data,bytes(tmp));self.fixture_write(p+0xA4,dwords(data));self.fixture_write(p+0x2E4,dwords(w&255,h&255));data+=(len(tmp)+15)&~15
  assert sr.u32(u,0xA8ED38)==t['count']
  if self.owner is not None:
   self.construction_history['tiles'].update(after=self.physical_constructor_state(),
      count=t['count'],native_ids=[self.owner.read32(0x44480000+i*0x400+0x10)for i in range(t['count'])])
   # One retained observation per constructor group, including failure logs.
   # Do not emit timing/name lines for each head or supply any native state.
   print(json.dumps(dict(stage='physical_tile_constructors',history=self.construction_history['tiles'])),flush=True)
  print('native cells and tile heads ready',flush=True)
  self.activity='initial_recalc';self.sweeps=[];self.trace.clear();self.writes.clear()
  cell_rng_before={k:sr.rng_state(u,p) for k,p in self.rngs.items()}
  self.cell_inputs_rng=dict(before=cell_rng_before)
  if self.owner is None:self.sweep()
  if cell_inputs_only:
   # Reuse the authentic Cell/type/TMP input producer without executing later
   # Terrain placement, graph construction or actor setup. No native return is
   # substituted to impose this fixture boundary.
   if self.owner is not None:
    # Original567110 allocates the class/height planes, sizes Pathfinder and
    # calls original568BB0. Stop before its bridge-record/graph suffix.
    from tools.spatial_oracle.building_body_rules import SP
    self.native_final_init_started=True
    self.fixture_write(SP,dwords(RET_MAGIC));u.reg_write(UC_X86_REG_ESP,SP);u.reg_write(UC_X86_REG_ECX,MAP)
    self.owner.run_native(0x567110,0x5671E9,count=80000000,timeout_us=60000000)
    self.final_tiberium_value=u.reg_read(UC_X86_REG_EAX)
   self.cell_inputs_rng=dict(before=cell_rng_before,after={k:sr.rng_state(u,p) for k,p in self.rngs.items()})
   self.initial_cells=self.cell_plane();self.trace.clear();self.writes.clear();self.pending.clear();self.reached={};self.activity='cell_inputs'
   return
  self.activity='terrain_place';self.terrain_placement=[]
  if self.owner is None:self.fixture_write(0xA8E988,dwords(0x7EB6D4,self.allocate(1024*4),1024,1,0,10))
  else:self.call(0x4E6A60,this=0)  # actual Terrain instance registry cold owner
  for key,name,line in sections.get('Terrain',()):
   p=self.allocate(0xE0);q=r.terrain_ptrs[name];coord=(int(key)%1000,int(key)//1000);self.call(0x71BB90,this=p,args=(q,0xB0ECF0),count=100000)
   self.fixture_write(COORD,packed(*coord));self.fixture_write(COORD+16,dwords(coord[0]*256+128,coord[1]*256+128,0));self.call(0x71E0D0,this=q,args=(COORD+32,COORD+16));self.call(0x5F6940,this=p,args=(COORD+32,))
   # Direct original Place_Down after constructor and coordinate callback. Display/Logic reveal excluded.
   self.call(0x5683C0,args=(COORD,p),count=300000)
   self.terrain_placement.append(dict(key=key,name=name,coord=list(coord),native_xyz=list(struct.unpack('<3i',u.mem_read(p+0x9C,12)))))
  print('native terrain placements ready',flush=True)
  self.activity='final_recalc'
  if self.owner is None:self.final_tiberium_value=self.call(0x568BB0,args=(0,),count=80000000)
  else:self.finish_graphs()
  print('native cell planes established',dict(self.counters),flush=True)
  self.initial_cells=self.cell_plane();self.trace.clear();self.writes.clear();self.pending.clear();self.reached={}
  if self.owner is None:self.finish_graphs()
  self.actor_constructor_before={k:sr.rng_state(u,p) for k,p in self.rngs.items()};self.trace.clear()
  if self.create_actor:self.build_actor(r.mtnk)
  self.actor_constructor=dict(before_rng=self.actor_constructor_before,after_rng={k:sr.rng_state(u,p) for k,p in self.rngs.items()},trace=list(self.trace));self.initial=self.state();print('native hierarchy established',[len(x['records']) for x in self.initial['graphs']],flush=True)
  self.activity='bridge'
 def finish_graphs(self,*,compute_bridge_records=False):
  """Build original graphs over this VM's already-constructed Cell state.

  The shared route executes567110 once over actual constructor-owned vectors,
  including original Bridge-record production. A paused prefix is not resumed
  by re-entering that caller. Legacy supplied-header controls remain separate.
  """
  if self.owner is not None:
   if self.native_final_init_started:
    raise ValueError('Original567110 already entered; a retained prefix frame cannot be re-entered')
   self.native_final_init_started=True
   self.activity='native_graph_construction'
   self.construction_history['graphs']=dict(before=self.physical_constructor_state())
   self.call(0x567110,count=180000000,timeout_us=self.full_graph_timeout_us)
   self.construction_history['graphs']['after']=self.physical_constructor_state()
   header=struct.unpack('<6I',self.uc.mem_read(MAP+0x50,24))
   self.bridge_record_production=dict(entry='0x56d6e0',count=header[4],capacity=header[2])
   return
  u=self.uc;case=self.case
  self.activity='connectivity';self.fixture_write(MAP+0x18,bytes(13*4))
  if compute_bridge_records:
   from tools.spatial_oracle.bridge_records import compute_on_map
   self.bridge_record_production=compute_on_map(self)
  else:self.fixture_write(MAP+0x54,dwords(0,0,1,0,10))
  for address in (0x49F0E0,0x49F190,0x49F2F0,0x49F2D0,0x49F280):self.call(address,count=10000)
  root=self.allocate(16);buckets=self.allocate(256*24);template=self.allocate(24);self.call(0x58AFF0,this=template,args=(0,0),count=1000);self.fixture_write(template,dwords(0x7ED540));self.fixture_write(template+16,dwords(0,20));self.fixture_write(buckets,bytes(u.mem_read(template,24))*256);self.fixture_write(root,dwords(buckets,0x56CB80,256,20));self.fixture_write(MAP+0x14,dwords(root));self.call(0x56C510,count=60000000)
  print('native base graph established',self.nav_snapshot()['zone_count'],flush=True)
  self.activity='hierarchy';self.fixture_write(0x87E8B8+0x40,bytes(9*4));template=self.allocate(24);self.call(0x58B070,this=template,args=(0,0),count=1000);self.fixture_write(template,dwords(0x7ED520));self.fixture_write(template+16,dwords(0,20));bucket_template=bytes(u.mem_read(template,24));w,h=case['size']
  for level in range(3):
   header=MAP+0x8C+level*24;self.call(0x58AE60,this=header,args=(0,0),count=1000);self.fixture_write(header,dwords(0x7ED4A0));self.fixture_write(header+16,dwords(0,w*h*4//(1<<(2*(level+1)))));buckets=self.allocate(256*24);root=self.allocate(16);self.fixture_write(root,dwords(buckets,0x56CB80,256,20));self.fixture_write(MAP+0x80+level*4,dwords(root));self.fixture_write(buckets,bucket_template*256)
  for level in (2,1,0):self.call(0x581F90,args=(level,),count=80000000)
  self.call(0x42C1C0,this=0x87E8B8,count=10000000)
 def sweep(self):
  self.call(0x578350);coords=[]
  while True:
   p=self.call(0x578290)
   if not p:break
   coords.append(self.coord(p));self.call(0x47D2B0,this=p,args=(-1,),count=100000)
  assert {tuple(c) for c in coords}==set(self.ptrs),(len(coords),len(self.ptrs))
  self.sweeps.append(dict(activity=self.activity,count=len(coords),order_sha256=sha(b''.join(packed(*c) for c in coords))))
 def cell_plane(self):
  u=self.uc
  return [dict(coord=list(c),tile=sr.i32(u,p+0x38),subtile=u.mem_read(p+0x11A,1)[0],level=u.mem_read(p+0x11B,1)[0],slope=u.mem_read(p+0x11C,1)[0],land=sr.i32(u,p+0xEC),zone_type=sr.i32(u,p+0x4C),flags=sr.u32(u,p+0x140),occupation=u.mem_read(p+0x124,1)[0],has_ground_object=bool(sr.u32(u,p+0xE4))) for c,p in self.ptrs.items()]
 def build_actor(self,typ):
  u=self.uc;self.actor=self.allocate(0x800);self.drive=self.allocate(0x100);house=self.allocate(0x17000);self.fixture_write(0xB0F720,dwords(0x7EB6D4,self.allocate(4096),1024,1,0,10));sp=STACK_BASE+STACK_SIZE-0x1000;self.fixture_write(sp,dwords(RET_MAGIC,typ,0));u.reg_write(UC_X86_REG_ESP,sp);u.reg_write(UC_X86_REG_ECX,self.actor);run_checked(u,0x7353C0,0x7354CE,count=300000)
  self.call(0x4AF540,this=self.drive);self.fixture_write(self.drive+0xC,dwords(self.actor));self.fixture_write(self.drive+0x14,dwords(1));self.fixture_write(self.actor+0x674,dwords(self.drive+4));self.fixture_write(self.actor+0x21C,dwords(house));self.fixture_write(self.actor+0x6C,dwords(sr.u32(u,typ+0xA0)));self.fixture_write(self.actor+0x90,b'\x01');self.fixture_write(self.actor+0x81,b'\0');self.fixture_write(self.actor+0xAC,dwords(5));self.fixture_write(self.actor+0xB4,dwords(-1));self.fixture_write(self.actor+0x3D5,b'\1');self.fixture_write(self.actor+0x6D8,dwords(-1));self.fixture_write(self.actor+0x338,dwords(-1));self.fixture_write(self.actor+0x684,b'\xff');self.fixture_write(self.actor+0x9C,dwords(self.actor_coord[0]*256+128,self.actor_coord[1]*256+128,self.actor_height*sr.i32(u,0x89E7C0)));self.fixture_write(self.actor+0x55C,packed(*self.actor_coord));self.call(0x4AF4A0,this=0)
 def movement_admissions(self):
  result=[];u=self.uc;before={k:sr.rng_state(u,p) for k,p in self.rngs.items()};fn=sr.u32(u,sr.u32(u,self.actor)+0x1AC);assert fn==0x73F0A0
  for c in self.admission_cells:
   p=self.ptrs[c];value=self.call(fn,this=self.actor,args=(p,4,self.actor_height,0,1),count=300000);result.append(dict(candidate=list(c),direction=4,height=self.actor_height,previous_cell=None,arg5=1,land=sr.i32(u,p+0xEC),class_result=value))
  assert before=={k:sr.rng_state(u,p) for k,p in self.rngs.items()}
  return result
 def state(self):return dict(rng={k:sr.rng_state(self.uc,p) for k,p in self.rngs.items()},movement_admissions=self.movement_admissions() if self.create_actor else [],navigation=self.nav_snapshot(),graphs=self.graph_snapshot(),dummy=self.dummy_snapshot(),cells=self.cell_plane())
 def observe(self,u,a,n,d):
  if self.owner is not None:return self.observe_physical(u,a,n,d)
  if self.phase!='measure':return super().observe(u,a,n,d)
  if self.range_pending and a==self.range_pending[-1][0]:
   _,row=self.range_pending.pop();row['result']=u.reg_read(UC_X86_REG_EAX)
  if a==self.tile_image_getter:
   p=u.reg_read(UC_X86_REG_ECX)
   if 0x44480000<=p<0x44480000+self.tile_count*0x400:
    index=(p-0x44480000)//0x400;self.used_tile_heads.add(index);assert sr.u32(u,p+0xA4),('reached primary TMP absent',index)
  if a==0x65C7E0:
   sp=u.reg_read(UC_X86_REG_ESP);this=u.reg_read(UC_X86_REG_ECX);stream=next(k for k,p in self.rngs.items() if p==this);row=dict(kind='range_request',stream=stream,minimum=sr.i32(u,sp+4),maximum=sr.i32(u,sp+8));self.trace.append(row);self.range_pending.append((sr.u32(u,sp),row));self.counters[f'{self.activity}:{stream}:range_requests']+=1
  if a==0x65C84B:self.counters[f'{self.activity}:ranged_raw_draws']+=1
  if a==0x65C780:
   stream=next(k for k,p in self.rngs.items() if p==u.reg_read(UC_X86_REG_ECX));self.counters[f'{self.activity}:{stream}:next_draws']+=1
  if a in (0x47D2B0,0x47CA80,0x483C80,0x5FDD20,0x547370,0x71C110,0x47E8A0):
   self.counters[f'{self.activity}:{a:08X}']+=1
   if a==0x47D2B0:return
  if a==0x421EA0:
   sp=u.reg_read(UC_X86_REG_ESP);self.counters[f'{self.activity}:animation_constructor_boundary']+=1;self.ret(28,u.reg_read(UC_X86_REG_ECX));return
  if a in (0x547020,0x727FD0):raise AssertionError(('uncovered dependency',self.activity,hex(a)))
  if a in (0x56C510,0x586990,0x584550,0x581F90,0x5824A0,0x42C1C0,0x578460,0x56CB90,0x56C6CB):
   self.counters[f'{self.activity}:{a:08X}']+=1
   if self.activity=='bridge':
    sp=u.reg_read(UC_X86_REG_ESP)
    if a==0x56C510:self.event('connectivity')
    elif a==0x586990:
     v=sr.u32(u,sp+4);data=sr.u32(u,v+4);count=sr.u32(u,v+16);self.event('hierarchy_batch',cells=[list(struct.unpack('<hh',u.mem_read(data+i*4,4)))for i in range(count)])
    elif a==0x584550:self.event('hierarchy_patch',coord=list(struct.unpack('<hh',u.mem_read(sr.u32(u,sp+4),4))))
    elif a==0x42C1C0:self.event('pathfinder_scratch_refresh')
    elif a==0x578460 and sr.u32(u,sp) in (0x5869BA,0x586A5B):self.event('hierarchy_cell_pass',pass_number=1 if sr.u32(u,sp)==0x5869BA else 2,coord=list(struct.unpack('<hh',u.mem_read(sr.u32(u,sp+4),4))))
   return
  if a==0x7C978A:self.ret(eax=0);return
  if a in (0x586360,0x5865E0):self.counters[f'{self.activity}:shroud_boundary']+=1;self.ret(4,1);return
  if a==0x7D140B:self.ret(eax=0x447F0000);return
  if a==0x4068E0:raise AssertionError(('native warning reached',self.activity,hex(a)))
  super().observe(u,a,n,d)
 def observe_physical(self,u,a,n,d):
  """Observer only: guarded runner owns every OS/presentation substitution."""
  if a==0x5671E9:
   self.final_tiberium_value=u.reg_read(UC_X86_REG_EAX)
   self.cell_inputs_rng['after']={k:sr.rng_state(u,p)for k,p in self.rngs.items()}
   print(json.dumps(dict(stage='physical_recalc',state=self.physical_constructor_state(),
                        native_reached=dict(self.counters),final_tiberium_value=self.final_tiberium_value)),flush=True)
  if a==self.tile_image_getter:
   p=u.reg_read(UC_X86_REG_ECX)
   if 0x44480000<=p<0x44480000+self.tile_count*0x400:
    index=(p-0x44480000)//0x400;self.used_tile_heads.add(index)
    assert sr.u32(u,p+0xA4),('reached primary TMP absent',index)
  if a in (0x47D2B0,0x47CA80,0x483C80,0x5447C0,0x547370,0x5FDD20,0x567110,0x56D6E0,0x56C510,0x581F90,0x42C1C0,0x578460):
   self.counters[f'{self.activity}:{a:08X}']+=1
  if a in (0x421EA0,0x547020,0x727FD0,0x4068E0):
   raise AssertionError(('uncovered physical dependency',self.activity,hex(a)))
 def write(self,u,access,a,n,v,d):
  if self.activity=='bridge':return super().write(u,access,a,n,v,d)
  assert not 0x401000<=a<0x7E1000
 def run(self):
  stages=[]
  for name,fn,c in (self.stages if self.stages is not None else [('first_damage',0x57CCF0,self.case['impact']),('collapse',0x57CCF0,self.case['impact']),('repair',0x573540,self.case['start'])]):
   counts0=self.counters.copy();self.trace.clear();self.pending.clear();rng0={k:sr.rng_state(self.uc,p) for k,p in self.rngs.items()};self.uc.mem_write(COORD,packed(*c));answer=self.call(fn,args=(COORD,),count=80000000)
   stages.append(dict(name=name,returned_low_byte=answer&255,trace=list(self.trace),rng_before=rng0,rng_after={k:sr.rng_state(self.uc,p) for k,p in self.rngs.items()},state=self.state(),native_reached_delta=dict(self.counters-counts0)));assert not self.pending and not self.range_pending;assert sha(bytes(self.uc.mem_read(0x401000,0x3E0000)))==self.code_hash;print(name,'done',flush=True)
  return stages

def generate():
 t=identity.theater();r=Inputs(t);tiles,assets=extract_tiles(t);m=Navigation(r,t,tiles)
 assert not m.range_pending
 assert sha(bytes(m.uc.mem_read(0x401000,0x3E0000)))==m.code_hash
 return dict(schema=1,readers=r.snapshot(),theater=t,assets=assets,text_sha256=m.code_hash,case=m.case,sweeps=m.sweeps,terrain_placement=m.terrain_placement,final_tiberium_value=m.final_tiberium_value,fpcw=m.uc.reg_read(UC_X86_REG_FPCW),bootstrap=m.bootstrap,cell_startup=m.cell_startup,actor_constructor=m.actor_constructor,initial=m.initial,stages=m.run(),native_reached=dict(m.counters),reached_primary_tmp_heads=sorted(m.used_tile_heads))
if __name__=='__main__':finish_vectors(generate,HERE/'navigation.json.gz',provenance=lambda:provenance(scope=__doc__,assumptions=['Physical XMP03T4.MAP diamond fields, original scalar/type readers and relocated physical TEMPERATMD primary TMP bytes; original Cell constructors and Recalc derive all class/height inputs. No VERA planes or IDs supplied.','Original Terrain constructors and direct Place_Down follow physical source order; full Unlimbo, loaded world object arrays and scenario timing are excluded. Ordinary building class gates are independently native-read false; ordinary mobile RTTIs are ignored by483C80.','Actual568BB0 final initialization,56C510 and581F90(2,1,0), then original57CCF0 twice and573540 repair execute. Graph header final-vtable/growth caller stores are supplied as in the established hierarchy harness.','Main, Scenario and MapGen begin with original seeded0 complete states; the original Unit constructor prefix advances Scenario once, recorded separately. No full native scenario load/RNG claim.'],substitutions=['Successful bounded malloc/free, CRT atexit registration and TLS. Physical archive and lexical INI cache preparation remain host-side.','Waterfall Anim421EA0 returns original allocated receiver and records caller-side state; animation registration/playback/lifetime and its hidden RNG are excluded from initialization. Shroud query returns hidden; Terrain discovery does not supply graph state.','Screen/radar/dirty-rectangle sinks inherited from the frozen geometry harness. Dynamic mobiles and ordinary buildings are omitted only from class-neutral membership; this is not a full actor/world loading comparison.'],entry_points={'cell_ctor':0x47BBF0,'terrain_ctor':0x71BB90,'terrain_place':0x5683C0,'recalc':0x47D2B0,'zone':0x483C80,'final_init':0x568BB0,'connectivity':0x56C510,'hierarchy':0x581F90,'batch':0x586990,'damage':0x57CCF0,'repair':0x573540,'unit_can_enter':0x73F0A0}))
