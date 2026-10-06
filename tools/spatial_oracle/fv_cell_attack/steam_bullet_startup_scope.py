"""Authenticated Bullet registry CRT declaration for a new fresh startup scope.

Original table slot 813280 (index 1184) calls 4E75E0 before Mission/Dummy/
Scenario. The shared ordered CRT owner executes it; this module supplies no
registry bytes, invokes no callback and never repairs a retained VM. Historical
selected startup profiles do not enroll it.
"""
from dataclasses import replace

from tools.native_oracle import RET_MAGIC


STEAM_NATIVE_SHA256='3e81a61775d2745d1dabe397325ef663cd994ffc194da4e998e3bf5d2d308600'
BULLET_COLD_PROFILE_NAME='steam-15918130-fv-ordered-bullet-crt-v1'
BULLET_COLD_ENTRY=0x4E75E0
BULLET_COLD_TABLE_INDEX=1184
BULLET_COLD_TABLE_SLOT=0x813280
BULLET_REGISTRY=0xA83C80
BULLET_REGISTRY_BYTES=24
BULLET_REGISTRY_VTABLE=0x7EA364
BULLET_EXIT_CALLBACK=0x4E7620
BULLET_COLD_REGION=(0x4E75E0,0x4E761D,
    'b7860475aef8be3415f4926d30c41b41dfd5c143e315d592202bfd3837c32fac')


def extend_ordered_startup_profile(profile,*,name=BULLET_COLD_PROFILE_NAME):
    """Declare the literal callback and native-only 24-byte registry writes.

    Select the returned profile before constructing the single fresh VM. Only
    the existing Steam ordered startup/prereader owners are eligible; transport,
    allocator and fixture grants are inherited without widening them.
    """
    if profile.native_sha256!=STEAM_NATIVE_SHA256 or profile.name not in (
            'steam-15918130-fv-selected-cold-crt-v1',
            'steam-15918130-fv-ordered-rules-prereaders-v1'):
        raise ValueError('Bullet CRT declaration requires authenticated ordered startup')
    if any(start<=BULLET_COLD_ENTRY<end for start,end,_ in profile.regions):
        raise ValueError('Bullet CRT declaration must not be enrolled twice')
    data=((BULLET_REGISTRY,BULLET_REGISTRY_BYTES),)
    return replace(profile,name=name,regions=profile.regions+(BULLET_COLD_REGION,),
        entries=profile.entries+((BULLET_COLD_ENTRY,(RET_MAGIC,)),),
        reads=profile.reads+data,writes=profile.writes+data)


def generate_ordered_bullet_startup():
    """Execute the existing fresh startup owner with the new literal grant."""
    from tools.spatial_oracle.fv_cell_attack import steam_movement_profile as driver
    owner,selected,receipt=driver.constructor_inputs(
        profile=extend_ordered_startup_profile(driver.ordered_startup_profile()),
        heap_bytes=0x2000000,initial_counter=None,scenario_bytes=driver.NATIVE_SCENARIO_BYTES,
        native_scenario=True,construct_selected_type=False,initialize_options=True,
        initialize_physical=True,ordered_cold_startup=True)
    if selected is not None or receipt['scenario_counter_before']!=1_000_000:
        raise ValueError('Bullet startup must precede fresh Scenario and type discovery')
    return dict(schema_version=1,constructor=receipt,
        bullet_registry_address=BULLET_REGISTRY,
        bullet_registry_hex=bytes(owner.u.mem_read(BULLET_REGISTRY,BULLET_REGISTRY_BYTES)).hex(),
        bullet_exit_registration_count=owner.exit_registrations.count(BULLET_EXIT_CALLBACK),
        excluded=['Full CRT/Windows startup, Rules/live type readers, assets, House, placement and movement parity.'])


def ordered_bullet_startup_metadata():
    from unicorn import Uc,UC_ARCH_X86,UC_MODE_32
    from tools.native_oracle import load_image,provenance
    from tools.spatial_oracle.fv_cell_attack import steam_movement_profile as driver
    image=load_image(Uc(UC_ARCH_X86,UC_MODE_32),
        profile=extend_ordered_startup_profile(driver.ordered_startup_profile()))
    return provenance(image=image,scope='Original selected cold CRT plus Bullet index1184 before Scenario',
        entry_points={'bullet_static':BULLET_COLD_ENTRY,'mission_static':0x4E7CF0,
            'dummy_static':0x565060,'scenario_ctor':0x6832C0},
        assumptions=['Original authenticated ascending CRT table binds callback order; omitted callbacks remain excluded.',
            'The same fresh VM retains native-only Bullet registry writes and original destructor registration.',
            'No Rules/live type/assets/placement/movement parity claim.'],
        substitutions=['Existing bounded allocator/CRT exit/TLS and explicit fresh zero-BSS/string priors.',
            'Native Scenario clock transport supplies six zero DWORD values; Windows startup is not executed.'])


def main(argv=None):
    from pathlib import Path
    from tools.native_oracle import finish_vectors
    here=Path(__file__).resolve();repo=here.parents[3]
    sources={leaf:repo/leaf for leaf in (
        'tools/native_oracle.py','tools/rules_oracle/bridge_anim_inputs.py',
        'tools/rules_oracle/bridge_anim_lists.py',
        'tools/spatial_oracle/fv_cell_attack/steam_movement_profile.py',
        'tools/spatial_oracle/fv_cell_attack/steam_bullet_startup_scope.py',
        'tools/spatial_oracle/fv_cell_attack/steam_physical_navigation_profile.py',
        'tools/spatial_oracle/anytown_damage/navigation.py',
        'tools/spatial_oracle/anytown_damage/mission.py',
        'tools/spatial_oracle/shrapnel_repair/shrapnel_repair.py',
        'tools/spatial_oracle/locomotor_force_track.py',
        'tools/spatial_oracle/mapgen_range.py','tools/input_oracle/fast_scroll.py',
        'tools/spatial_oracle/building_body_rules.py',
        'tools/spatial_oracle/locomotor_track_cursor.py','tools/spatial_oracle/map_queries.py',
        'tools/spatial_oracle/track_speed_native.py','tools/spatial_oracle/track_destination.py',
        'tools/spatial_oracle/track_outer_continuation.py')}
    finish_vectors(generate_ordered_bullet_startup,here.with_name('steam_movement_ordered_bullet_startup.json'),
        provenance=ordered_bullet_startup_metadata,argv=argv,description=__doc__,source_paths=sources)


if __name__=='__main__':main()
