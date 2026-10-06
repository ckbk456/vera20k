"""Continue the retained original live type caller without rebuilding its state.

This owner records original dispatch, native discoveries and physical requests.
An enrolled root is not a complete asset/helper closure: undeclared execution
still fails closed and partial observations are never a successful corpus.
"""
from dataclasses import replace
import json
from pathlib import Path

from tools.native_oracle import NativeExecutionError, RET_MAGIC

PROFILE_NAME='steam-15918130-fv-ordered-live-types-v1'
LIVE_HEAP_BYTES=0x08000000
BEGIN=0x668EED
END=0x668EF5


def live_types_profile():
    from tools.spatial_oracle.fv_cell_attack.steam_movement_profile import rules_prereader_profile
    from tools.spatial_oracle.fv_cell_attack.steam_bullet_startup_scope import extend_ordered_startup_profile
    from tools.spatial_oracle.fv_cell_attack.steam_live_types_scope import (
        LIVE_REGIONS, LIVE_READ_ONLY, LIVE_NATIVE_DATA, LIVE_READERS)
    from tools.spatial_oracle.fv_cell_attack.steam_live_asset_scope import (
        LIVE_ASSET_REGIONS,READ_ONLY,NATIVE_DATA,FIXTURE_DATA,SINKS,TRANSPORTS)
    from tools.spatial_oracle.fv_cell_attack.steam_live_catalog_scope import (
        CATALOG_REGIONS,CATALOG_READ_ONLY,CATALOG_NATIVE_DATA,CATALOG_ENTRIES)
    profile=extend_ordered_startup_profile(rules_prereader_profile(),name=PROFILE_NAME)
    transports={spec.site:spec for spec in profile.transports}
    for spec in TRANSPORTS:
        old=transports.get(spec.site)
        if old is not None and(old.iat!=spec.iat or old.argument_bytes!=spec.argument_bytes):
            raise ValueError('Live file transport changes the original import ABI')
        transports[spec.site]=spec
    heap=((0x24000000,LIVE_HEAP_BYTES),)
    return replace(profile,regions=profile.regions+LIVE_REGIONS+LIVE_ASSET_REGIONS+CATALOG_REGIONS,
        entries=profile.entries+((BEGIN,(END,)),)+tuple((row['entry'],(RET_MAGIC,))for row in LIVE_READERS)+
            tuple((entry,(RET_MAGIC,))for entry in(0x750300,0x403ED0,0x7510D0,0x734E60))+CATALOG_ENTRIES,
        reads=profile.reads+LIVE_READ_ONLY+LIVE_NATIVE_DATA+READ_ONLY+NATIVE_DATA+FIXTURE_DATA+CATALOG_READ_ONLY+CATALOG_NATIVE_DATA+heap,
        writes=profile.writes+LIVE_NATIVE_DATA+NATIVE_DATA+FIXTURE_DATA+CATALOG_NATIVE_DATA+heap,
        fixture_writes=profile.fixture_writes+FIXTURE_DATA+heap,
        sinks=profile.sinks+SINKS,transports=tuple(transports.values()))


def registry_snapshot(m):
    from tools.spatial_oracle.fv_cell_attack.steam_movement_profile import TYPED_MASTER_FAMILIES
    families=[(name,registry,size,vt)for name,_,_,size,_,registry,vt in TYPED_MASTER_FAMILIES]
    families.extend((('Weapon',0x887568,0x160,0x7E1ED4),('Bullet',0xA83C80,0x2F8,0x7EA364)))
    result=[]
    for name,registry,size,vt in families:
        if m.read32(registry)!=vt:raise ValueError('Live types require the original cold registry: '+name)
        array=m.read32(registry+4);count=m.read32(registry+16)
        capacity=m.read32(registry+8)
        if count>capacity or(capacity and not(0x24000000<=array and array+capacity*4<=m.heap_end)):
            raise ValueError('Invalid retained registry: '+name)
        members=[]
        for index in range(count):
            pointer=m.read32(array+index*4)
            if not (0x24000000<=pointer and pointer+size<=m.heap_end):
                raise ValueError('Type pointer outside original allocator')
            members.append(dict(index=index,pointer=pointer,name=m.string(pointer+0x24),
                native_id=m.read32(pointer+0x10),vtable=m.read32(pointer),
                full_type_hex=bytes(m.u.mem_read(pointer,size)).hex()))
        result.append(dict(family=name,registry=registry,header_hex=bytes(m.u.mem_read(registry,24)).hex(),members=members))
    return result


def continue_live_types(m,rules,reader_ini,receipt):
    from unicorn import UC_HOOK_CODE
    from unicorn.x86_const import (UC_X86_REG_EIP,UC_X86_REG_EDI,UC_X86_REG_ESI,
        UC_X86_REG_ESP,UC_X86_REG_ECX)
    from tools.spatial_oracle.fv_cell_attack.steam_movement_profile import TYPED_MASTER_FAMILIES
    from tools.spatial_oracle.fv_cell_attack.steam_live_types_scope import LIVE_READERS
    if m.image is None or m.image.profile.name!=PROFILE_NAME:
        raise ValueError('Live types require their complete profile at fresh VM creation')
    if 'retained_live_types'in receipt:raise ValueError('Live types cannot restart a retained caller')
    prior=receipt.get('retained_prereaders')
    if prior is None or prior['end']!=BEGIN or not all(prior['checks'].values()):
        raise ValueError('Live types require the executed retained Rules prereaders')
    sp=m.u.reg_read(UC_X86_REG_ESP)
    if (m.u.reg_read(UC_X86_REG_EIP),m.u.reg_read(UC_X86_REG_EDI),m.u.reg_read(UC_X86_REG_ESI),sp)!=(
            BEGIN,rules,reader_ini,prior['actual_after_esp']):
        raise ValueError('Live types require the actual original Rules/INI/stack caller')
    scene=m.read32(0xA8B230);surface=m.read32(0x887308)
    frame=bytes(m.u.mem_read(sp,receipt['original_prefix_frame_bytes']-4)).hex()
    caches_before={name:m.ini_cache_snapshot(address)for name,address in(('rules',reader_ini),('art',0x887180))}
    rng_addresses={'main':0x886B88,'scenario':scene+0x218,'mapgen':0xABE890}
    rng_before={name:bytes(m.u.mem_read(address,0x3F4)).hex()for name,address in rng_addresses.items()}
    before=registry_snapshot(m);allocation_mark=len(m.allocation_events);cursor=m.cursor
    counter=m.read32(scene+0x214);requests=len(m.asset_loaded)
    readers={row['entry']:row for row in LIVE_READERS}
    constructors_by_entry={ctor:family for family,_,ctor,_,_,_,_ in TYPED_MASTER_FAMILIES}
    constructors_by_entry.update({0x771C70:'Weapon',0x46BBC0:'Bullet'})
    calls=[];constructors=[];mission=[];postpasses=[];rng_calls=[];post_membership={}
    def observe(uc,pc,size,data):
        entry_sp=uc.reg_read(UC_X86_REG_ESP)
        if pc in readers:
            row=readers[pc];pointer=uc.reg_read(UC_X86_REG_ECX)
            array=m.read32(row['registry']+4);count=m.read32(row['registry']+16)
            indices=[index for index in range(count)if m.read32(array+index*4)==pointer]
            calls.append(dict(family=row['family'],entry=pc,caller=m.read32(entry_sp),
                pointer=pointer,ini=m.read32(entry_sp+4),name=m.string(pointer+0x24),
                counter=m.read32(scene+0x214),registry_count=count,registry_indices=indices))
        for meta in LIVE_READERS:
            if pc==meta['caller']:
                call=next((row for row in reversed(calls)if row['entry']==meta['entry']and'registry_count_after_return'not in row),None)
                if call is None:raise ValueError('Live reader returned without its observed original entry')
                call['registry_count_after_return']=m.read32(meta['registry']+16)
        if pc in constructors_by_entry:
            constructors.append(dict(family=constructors_by_entry[pc],entry=pc,caller=m.read32(entry_sp),
                pointer=uc.reg_read(UC_X86_REG_ECX),name=m.string(m.read32(entry_sp+4)),
                counter_before=m.read32(scene+0x214)))
        if pc==0x5B3760:
            pointer=uc.reg_read(UC_X86_REG_ECX)
            mission.append(dict(pointer=pointer,index=m.read32(pointer),ini=m.read32(entry_sp+4),caller=m.read32(entry_sp)))
        if pc in(0x7729F0,0x465CB0):
            family='Weapon'if pc==0x7729F0 else'Building'
            if family not in post_membership:
                meta=next(row for row in LIVE_READERS if row['family']==family)
                array=m.read32(meta['registry']+4);count=m.read32(meta['registry']+16)
                post_membership[family]=[m.read32(array+index*4)for index in range(count)]
            postpasses.append(dict(entry=pc,pointer=uc.reg_read(UC_X86_REG_ECX),caller=m.read32(entry_sp)))
        if pc==0x65C780:rng_calls.append(dict(entry=pc,receiver=uc.reg_read(UC_X86_REG_ECX),caller=m.read32(entry_sp)))
    watched=set(readers)|set(constructors_by_entry)|{row['caller']for row in LIVE_READERS}|{0x5B3760,0x7729F0,0x465CB0,0x65C780}
    hooks=[m.u.hook_add(UC_HOOK_CODE,observe,begin=pc,end=pc)for pc in sorted(watched)]
    try:
        m.run_native(BEGIN,END,count=200_000_000,timeout_us=1_200_000_000,
            required_addresses=(0x679A10,0x5B3760),context=dict(case='retained-original-live-type-pass',
                rules_ini=reader_ini,art_ini=0x887180,cache_rebuilt=False))
        after=registry_snapshot(m)
        for row in constructors:row['native_id_after']=m.read32(row['pointer']+0x10)
        caches_after={name:m.ini_cache_snapshot(address)for name,address in(('rules',reader_ini),('art',0x887180))}
        allocations=list(m.allocation_events[allocation_mark:])
        order={row['family']:index for index,row in enumerate(LIVE_READERS)}
        dispatch=[order[row['family']]for row in calls]
        membership_order=all([row['registry_indices']for row in calls if row['family']==meta['family']]==
            [[index]for index in range(sum(row['family']==meta['family']for row in calls))]for meta in LIVE_READERS)
        from tools.spatial_oracle.fv_cell_attack.steam_live_types_scope import LIVE_POSTPASSES,LIVE_MISSION
        expected_post=[]
        for family,entry,caller in LIVE_POSTPASSES:
            # Bullet/Warhead readers may append Weapons after the Weapon body
            # loop. The original postpass sees the then-current membership.
            expected_post.extend((entry,pointer,caller)for pointer in post_membership.get(family,()))
        live_coverage=all(not(rows:=[row for row in calls if row['family']==meta['family']])or
            rows[-1].get('registry_count_after_return')==len(rows)for meta in LIVE_READERS)
        checks=dict(original_stack=m.u.reg_read(UC_X86_REG_ESP)==sp,
            remaining_frame=bytes(m.u.mem_read(sp,len(bytes.fromhex(frame)))).hex()==frame,
            scene_rules_surface=(m.read32(0xA8B230),m.read32(0x8871E0),m.read32(0x887308))==(scene,rules,surface),
            lexical_bytes=all(caches_after[name]['immutable_sha256']==caches_before[name]['immutable_sha256']for name in caches_before),
            separate_receivers=reader_ini!=0x887180 and all(row['ini']==(0x887180 if row['family']=='Anim'else reader_ini)for row in calls),
            reader_order=dispatch==sorted(dispatch),
            original_member_order=membership_order,
            active_loop_coverage=live_coverage,
            original_reader_calls=all(row['caller']==readers[row['entry']]['caller']for row in calls),
            original_postpasses=[(row['entry'],row['pointer'],row['caller'])for row in postpasses]==expected_post,
            mission_order=[row['index']for row in mission]==list(range(32)),
            mission_receivers=all(row['pointer']==0xA8E3A8+index*0x20 and row['ini']==reader_ini and row['caller']==LIVE_MISSION['caller']for index,row in enumerate(mission)),
            constructor_ids=all(row['counter_before']==counter+index and row['native_id_after']==counter+index+1 for index,row in enumerate(constructors)),
            counter_chronology=m.read32(scene+0x214)==counter+len(constructors),
            native_allocation_extents=all(row['size']>0 and cursor<=row['pointer'] and row['pointer']+row['size']<=m.heap_end
                and(index==0 or allocations[index-1]['pointer']+allocations[index-1]['size']<=row['pointer'])for index,row in enumerate(allocations)))
        if not all(checks.values()):raise ValueError('Live type boundary checks failed: '+str(checks))
        receipt['retained_live_types']=dict(begin=BEGIN,end=END,calls=calls,constructors=constructors,
            missions=mission,postpasses=postpasses,postpass_membership=post_membership,checks=checks,actual_after_esp=m.u.reg_read(UC_X86_REG_ESP),
            registry_before=before,registry_after=after,counter_before=counter,counter_after=m.read32(scene+0x214),
            allocations=allocations,allocator_cursor_before=cursor,allocator_cursor_after=m.cursor,
            lexical_cache_before=caches_before,lexical_cache_after=caches_after,
            rng_before=rng_before,rng_after={name:bytes(m.u.mem_read(address,0x3F4)).hex()for name,address in rng_addresses.items()},
            rng_calls=rng_calls,rng_unchanged=all(bytes(m.u.mem_read(address,0x3F4)).hex()==rng_before[name]for name,address in rng_addresses.items()),
            asset_requests=m.asset_loaded[requests:],boundary='Original type bodies under supplied lexical/physical asset IO and startup priors; later Process/Session/House/placement/movement excluded.')
    except Exception as error:
        if isinstance(error,NativeExecutionError):
            error.diagnostics['live_type_progress']=dict(calls=calls,constructors=constructors,
                missions=mission,postpasses=postpasses,asset_requests=m.asset_loaded[requests:],
                counter_before=counter,counter_current=m.read32(scene+0x214),allocator_cursor=m.cursor,
                status='Partial original dispatch only; no successful live-type or retail parity claim')
            if error.report_path is not None:Path(error.report_path).write_text(json.dumps(error.diagnostics,indent=2)+'\n')
        raise
    finally:
        for hook in hooks:m.u.hook_del(hook)


def metadata():
    from unicorn import Uc,UC_ARCH_X86,UC_MODE_32
    from tools.native_oracle import load_image,provenance
    image=load_image(Uc(UC_ARCH_X86,UC_MODE_32),profile=live_types_profile())
    return provenance(image=image,scope='Original selected Bullet/Sound CRT, retained Rules prerequisites and live type caller668EED→668EF5',
        entry_points=dict(live_caller=BEGIN,live_pass=0x679A10,boundary=END),
        assumptions=['One fresh original-order selected CRT VM; original Scenario and retained Rules/ART objects.',
            'Physical unique lexical Rules/ART receivers; complete resident type loop rather than selected FV body.',
            'Explicit128MiB bounded heap for resident native parsers and immutable physical assets; historical32MiB profiles unchanged.',
            'Full physical decoded CSF cache is supplied before native type readers; original lookups execute.',
            'Original disabled-output sound factory and full SoundList execute before entering retained Process.',
            'Declarations alone establish no numeric, gameplay or complete Windows startup parity.'],
        substitutions=['Existing checked heap/CRT retirement/TLS/clock/RGB565 Surface boundaries.',
            'Frozen named archive registration and physical byte/file IO; original MIX traversal remains excluded.',
            'No Windows audio devices or waveform output; original null-index factory and definition/sample-skip branches execute.'])


def main():
    import os,sys
    from functools import partial
    from tools.native_oracle import finish_vectors
    from tools.spatial_oracle.fv_cell_attack.steam_movement_profile import (
        color_palette_root,generate_typed_master,retained_dialog_companion_argv,retained_dialog_reader_vectors)
    from tools.projectile_oracle.bridge_render_inputs_palette import PALETTE_ASSETS
    root=Path(__file__).resolve().parents[3]
    argv=sys.argv[1:]
    if not any(arg=='--output'or arg.startswith('--output=')for arg in argv):
        raise ValueError('Live native corpus requires a separate explicit --output; keep full retail lexical/asset data local')
    # Bind source owners, including late native helper imports, without importing
    # the unrelated gameplay fixtures solely to discover them. The owned wrapper
    # separately freezes complete current producer and physical file inventories.
    paths={str(path.relative_to(root)):path for path in(root/'tools').rglob('*.py')if'__pycache__'not in path.parts}
    physical=Path(os.environ['VERA20K_FV_MOVEMENT_ASSETS'])
    paths.update({name:physical/leaf for name,leaf in(('physical_rules_root','RULESMD.INI'),('physical_art_root','ARTMD.INI'))})
    paths.update({'physical_'+name:color_palette_root()/name for name in PALETTE_ASSETS})
    captured={}
    generator=partial(generate_typed_master,retained_startup=True,retained_dialog=True,
        ordered_cold_startup=True,retained_prereaders=True,retained_live_types=True,
        execution_source_paths=paths,reference_capture=captured)
    default=root/'.local/fv-movement-validation/live-types/full.json'
    finish_vectors(generator,default,provenance=metadata,argv=argv,source_paths=paths,description=__doc__)
    companion_argv,companion_path=retained_dialog_companion_argv(argv,default)
    finish_vectors(partial(retained_dialog_reader_vectors,captured['reader'],source_paths=paths),
        companion_path,provenance=metadata,argv=companion_argv,source_paths=paths)


if __name__=='__main__':main()
