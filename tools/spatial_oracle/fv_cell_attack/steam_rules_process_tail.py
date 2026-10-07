"""Finish the original retained Rules.Process frame; never reconstruct its ABI.

The selected stock root has no command-bar sections. Original difficulty,
post-type readers, Warhead rereads and Tiberium discovery still execute. Session,
House, placement and gameplay remain later scopes.
"""
from dataclasses import replace
import json
from pathlib import Path

from tools.native_oracle import NativeExecutionError, RET_MAGIC

PROFILE_NAME = 'steam-15918130-fv-ordered-rules-process-tail-v1'
BEGIN = 0x668EF5
TIBERIUM_COLD_ENTRY = 0x721640
TIBERIUM_REGISTRY = 0xB0F4E8
TIBERIUM_COLD_TABLE_INDEX = 3220
TIBERIUM_COLD_TABLE_SLOT = 0x815250
TAIL_INSTRUCTION_LIMIT = 100_000_000
TAIL_TIMEOUT_US = 900_000_000


def rules_process_tail_profile():
    from tools.spatial_oracle.fv_cell_attack.steam_live_types import live_types_profile
    from tools.spatial_oracle.fv_cell_attack.steam_rules_tail_scope import (
        TAIL_REGIONS, TAIL_READ_ONLY, TAIL_NATIVE_DATA, TAIL_ENTRIES)
    from tools.spatial_oracle.fv_cell_attack.steam_physical_navigation_profile import (
        RULES_TIBERIUM_REGIONS, RULES_TIBERIUM_READ_ONLY,
        RULES_TIBERIUM_NATIVE_DATA, RULES_TIBERIUM_ENTRIES)
    parent = live_types_profile()
    def append(prior, extra):
        return prior + tuple(row for row in extra if row not in prior)
    entries = ((BEGIN, (RET_MAGIC,)),) + TAIL_ENTRIES + RULES_TIBERIUM_ENTRIES
    entry_stops = dict(parent.entries)
    entry_stops.update(entries)
    return replace(parent, name=PROFILE_NAME,
        regions=append(parent.regions, TAIL_REGIONS + RULES_TIBERIUM_REGIONS),
        entries=tuple(entry_stops.items()),
        reads=append(parent.reads, TAIL_READ_ONLY + TAIL_NATIVE_DATA +
                     RULES_TIBERIUM_READ_ONLY + RULES_TIBERIUM_NATIVE_DATA),
        writes=append(parent.writes, TAIL_NATIVE_DATA + RULES_TIBERIUM_NATIVE_DATA))


def tiberium_snapshot(m):
    from tools.spatial_oracle.fv_cell_attack.steam_live_types_scope import LIVE_READERS
    registry = TIBERIUM_REGISTRY
    if m.read32(registry) != 0x7F56BC:
        raise ValueError('Tiberium requires its original ordered cold registry')
    array, capacity, count = (m.read32(registry + offset) for offset in (4, 8, 16))
    if count > capacity or (capacity and not (0x24000000 <= array and array + capacity * 4 <= m.heap_end)):
        raise ValueError('Invalid original Tiberium vector')
    members = []
    overlay = next(row for row in LIVE_READERS if row['family'] == 'Overlay')
    overlay_array = m.read32(overlay['registry'] + 4)
    overlay_members = {}
    for index in range(m.read32(overlay['registry'] + 16)):
        pointer = m.read32(overlay_array + index * 4)
        overlay_members[pointer] = dict(index=index, name=m.string(pointer + 0x24))
    for index in range(count):
        pointer = m.read32(array + index * 4)
        if not (0x24000000 <= pointer and pointer + 0x128 <= m.heap_end):
            raise ValueError('Tiberium pointer outside original allocator')
        members.append(dict(index=index, pointer=pointer, name=m.string(pointer + 0x24),
                            native_id=m.read32(pointer + 0x10), native_ordinal=m.read32(pointer + 0x98),
                            image_pointer=m.read32(pointer + 0xE0),
                            image_overlay=overlay_members.get(m.read32(pointer + 0xE0)),
                            image_dimensions=[m.read32(pointer + offset) for offset in (0xE4, 0xE8, 0xEC)],
                            full_type_hex=bytes(m.u.mem_read(pointer, 0x128)).hex()))
    return dict(family='Tiberium', registry=registry,
                header_hex=bytes(m.u.mem_read(registry, 24)).hex(), members=members)


def continue_rules_process_tail(m, rules, reader_ini, receipt, *, progress=None):
    from unicorn import UC_HOOK_CODE
    from unicorn.x86_const import (UC_X86_REG_EIP, UC_X86_REG_ESP, UC_X86_REG_EDI,
        UC_X86_REG_ESI, UC_X86_REG_ECX, UC_X86_REG_EDX, UC_X86_REG_EBP, UC_X86_REG_EBX)
    from tools.spatial_oracle.fv_cell_attack.steam_live_types import registry_snapshot
    from tools.spatial_oracle.fv_cell_attack.steam_live_types_scope import LIVE_READERS
    from tools.spatial_oracle.fv_cell_attack.steam_movement_profile import TYPED_MASTER_FAMILIES
    from tools.spatial_oracle.fv_cell_attack.steam_rules_tail_scope import TAIL_READERS
    if m.image is None or m.image.profile.name != PROFILE_NAME:
        raise ValueError('Rules tail requires its complete profile at fresh VM creation')
    if 'retained_rules_process_tail' in receipt:
        raise ValueError('Rules tail cannot restart its retained original caller')
    prior = receipt.get('retained_live_types')
    if prior is None or prior['end'] != BEGIN or not all(prior['checks'].values()):
        raise ValueError('Rules tail requires completed retained live readers')
    sp = m.u.reg_read(UC_X86_REG_ESP)
    if (m.u.reg_read(UC_X86_REG_EIP), m.u.reg_read(UC_X86_REG_EDI),
            m.u.reg_read(UC_X86_REG_ESI), sp) != (BEGIN, rules, reader_ini, prior['actual_after_esp']):
        raise ValueError('Rules tail requires the actual Rules/INI/stack caller')
    if m.read32(sp + 0x3C) != RET_MAGIC:
        raise ValueError('Rules tail lost the original Process return sentinel')
    scene, surface = m.read32(0xA8B230), m.read32(0x887308)
    mode = m.read32(0xA8B238)
    if mode != 0:
        raise ValueError('Rules tail currently qualifies the unchanged cold mode-zero prior only')
    caches_before = {name:m.ini_cache_snapshot(address) for name,address in
                     (('rules', reader_ini), ('art', 0x887180))}
    sections = {row['name']:row for row in caches_before['rules']['sections']}
    if any(name in sections for name in ('AdvancedCommandBar', 'MultiplayerAdvancedCommandBar')):
        raise ValueError('Populated command-bar sections are outside the qualified Rules tail scope')
    rng_addresses = {'main':0x886B88, 'scenario':scene + 0x218, 'mapgen':0xABE890}
    rng_before = {name:bytes(m.u.mem_read(address, 0x3F4)).hex() for name,address in rng_addresses.items()}
    before = registry_snapshot(m)
    tib_before = tiberium_snapshot(m)
    counter, cursor = m.read32(scene + 0x214), m.cursor
    allocation_mark, request_mark = len(m.allocation_events), len(m.asset_loaded)
    saved_registers = {name:m.read32(sp + offset) for name,offset in
                       (('edi', 0), ('esi', 4), ('ebp', 8), ('ebx', 12))}
    frame = bytes(m.u.mem_read(sp, 0x44)).hex()
    top_level = tuple((row['entry'], row['caller'], row['physicalsection']) for row in TAIL_READERS)
    readers = {(entry, caller):section for entry,caller,section in top_level}
    ctor_entries = {ctor:family for family,_,ctor,_,_,_,_ in TYPED_MASTER_FAMILIES}
    ctor_entries.update({0x771C70:'Weapon', 0x46BBC0:'Bullet'})
    warhead = next(row for row in LIVE_READERS if row['family'] == 'Warhead')
    calls, constructors, tib_calls, tib_constructors, warhead_calls, rng_calls, epilogues = [], [], [], [], [], [], []
    warhead_membership = None
    def observe(uc, pc, size, data):
        nonlocal warhead_membership
        entry_sp = uc.reg_read(UC_X86_REG_ESP)
        caller = m.read32(entry_sp)
        if pc == 0x668FA2:
            epilogues.append(dict(entry=pc, opcode_hex=bytes(uc.mem_read(pc, size)).hex(),
                                  esp=entry_sp, return_address=caller))
        if (pc, caller) in readers:
            section = readers[(pc, caller)]
            calls.append(dict(entry=pc, caller=caller, section=section,
                ecx=uc.reg_read(UC_X86_REG_ECX), edx=uc.reg_read(UC_X86_REG_EDX),
                argument=m.read32(entry_sp + 4), second_argument=m.read32(entry_sp + 8), entry_esp=entry_sp))
            if progress:progress('Original Rules tail reader ' + section)
        if pc in ctor_entries:
            pointer = uc.reg_read(UC_X86_REG_ECX)
            constructors.append(dict(entry=pc, family=ctor_entries[pc], pointer=pointer,
                caller=caller, name=m.string(m.read32(entry_sp + 4)),
                counter_before=m.read32(scene + 0x214)))
        if pc == 0x7216C0:
            tib_constructors.append(dict(entry=pc, pointer=uc.reg_read(UC_X86_REG_ECX),
                caller=caller, name=m.string(m.read32(entry_sp + 4)), counter_before=m.read32(scene + 0x214)))
        if pc == 0x721A50:
            tib_calls.append(dict(entry=pc, caller=caller, pointer=uc.reg_read(UC_X86_REG_ECX),
                                  ini=m.read32(entry_sp + 4)))
        if pc == warhead['entry'] and caller == 0x6691AD:
            pointer = uc.reg_read(UC_X86_REG_ECX)
            array, count = m.read32(warhead['registry'] + 4), m.read32(warhead['registry'] + 16)
            if warhead_membership is None:
                warhead_membership = [m.read32(array + index * 4) for index in range(count)]
            warhead_calls.append(dict(entry=pc, caller=caller, pointer=pointer,
                ini=m.read32(entry_sp + 4), registry_indices=[index for index in range(count)
                    if m.read32(array + index * 4) == pointer]))
        if pc == 0x65C780:
            rng_calls.append(dict(entry=pc, caller=caller, receiver=uc.reg_read(UC_X86_REG_ECX)))
    watched = {entry for entry,_,_ in top_level} | set(ctor_entries) | {
        0x7216C0, 0x721A50, warhead['entry'], 0x65C780, 0x668FA2}
    hooks = [m.u.hook_add(UC_HOOK_CODE, observe, begin=pc, end=pc) for pc in sorted(watched)]
    try:
        m.run_native(BEGIN, RET_MAGIC, count=TAIL_INSTRUCTION_LIMIT, timeout_us=TAIL_TIMEOUT_US,
            required_addresses=tuple(dict.fromkeys(entry for entry,_,_ in top_level)),
            context=dict(case='retained-original-Rules-Process-tail', cache_rebuilt=False))
        after, tib_after = registry_snapshot(m), tiberium_snapshot(m)
        warhead_after = next(row for row in after if row['family'] == 'Warhead')
        for row in constructors:row['native_id_after'] = m.read32(row['pointer'] + 0x10)
        for row in tib_constructors:
            row['native_id_after'] = m.read32(row['pointer'] + 0x10)
            row['native_ordinal_after'] = m.read32(row['pointer'] + 0x98)
        caches_after = {name:m.ini_cache_snapshot(address) for name,address in
                       (('rules', reader_ini), ('art', 0x887180))}
        restored = {name:m.u.reg_read(register) for name,register in
                    (('edi', UC_X86_REG_EDI), ('esi', UC_X86_REG_ESI),
                     ('ebp', UC_X86_REG_EBP), ('ebx', UC_X86_REG_EBX))}
        checks = dict(original_return=m.u.reg_read(UC_X86_REG_EIP) == RET_MAGIC,
            original_ret4_instruction=epilogues == [dict(entry=0x668FA2, opcode_hex='c20400',
                esp=sp + 0x3C, return_address=RET_MAGIC)],
            original_ret4_stack=m.u.reg_read(UC_X86_REG_ESP) == sp + 0x44,
            saved_registers=restored == saved_registers,
            scene_rules_surface=(m.read32(0xA8B230), m.read32(0x8871E0), m.read32(0x887308)) == (scene, rules, surface),
            top_level_order=[(row['entry'], row['caller'], row['section']) for row in calls] == list(top_level),
            original_receivers=all(row['ecx'] == (reader_ini if row['section'] in ('Easy', 'Normal', 'Difficult', 'Tiberiums') else rules)
                and (row['section'] in ('Easy', 'Normal', 'Difficult', 'Tiberiums') or row['argument'] == reader_ini) for row in calls),
            difficulty_rows=all(row['edx'] == rules + 0x1538 + index * 0x50 for index,row in enumerate(calls[:3])),
            command_bar_flag=calls[-1]['second_argument'] == 0,
            lexical_bytes=all(caches_after[name]['immutable_sha256'] == caches_before[name]['immutable_sha256'] for name in caches_before),
            constructor_ids=all(row['counter_before'] == counter + index and row['native_id_after'] == counter + index + 1 for index,row in enumerate(constructors)),
            counter_chronology=m.read32(scene + 0x214) == counter + len(constructors),
            warhead_member_order=[row['registry_indices'] for row in warhead_calls] == [[index] for index in range(len(warhead_calls))],
            warhead_ini=all(row['ini'] == reader_ini for row in warhead_calls),
            warhead_loop_coverage=len(warhead_calls) == (len(warhead_after['members']) if 'SpecialWeapons' in sections else 0),
            tiberium_ini=all(row['ini'] == reader_ini and row['caller'] == 0x721DA2 for row in tib_calls),
            tiberium_loop_coverage=len(tib_calls) == sections.get('Tiberiums', {}).get('index_count', 0),
            native_allocation_extents=all(cursor <= row['pointer'] and row['pointer'] + row['size'] <= m.heap_end
                for row in m.allocation_events[allocation_mark:]))
        if not all(checks.values()):raise ValueError('Rules Process tail checks failed: ' + str(checks))
        receipt['retained_rules_process_tail'] = dict(begin=BEGIN, end=RET_MAGIC,
            calls=calls, constructors=constructors, tiberium_constructors=tib_constructors,
            tiberium_reads=tib_calls, warhead_rereads=warhead_calls, warhead_membership_at_loop=warhead_membership,
            registry_before=before, registry_after=after, tiberium_before=tib_before, tiberium_after=tib_after,
            checks=checks, original_frame_before_hex=frame, saved_registers_before=saved_registers,
            native_epilogues=epilogues,
            restored_registers_after=restored, actual_after_esp=m.u.reg_read(UC_X86_REG_ESP),
            lexical_cache_before=caches_before, lexical_cache_after=caches_after,
            counter_before=counter, counter_after=m.read32(scene + 0x214),
            allocations=list(m.allocation_events[allocation_mark:]), allocator_cursor_before=cursor,
            allocator_cursor_after=m.cursor, asset_requests=m.asset_loaded[request_mark:],
            rng_before=rng_before, rng_after={name:bytes(m.u.mem_read(address, 0x3F4)).hex() for name,address in rng_addresses.items()},
            rng_calls=rng_calls, rng_unchanged=all(bytes(m.u.mem_read(address, 0x3F4)).hex() == rng_before[name] for name,address in rng_addresses.items()),
            rules_after_hex=bytes(m.u.mem_read(rules, 0x18C0)).hex(),
            mode=mode, command_bar_boundary='Original mode-zero absent AdvancedCommandBar return; populated command-bar and accepted Session settings excluded.')
        receipt['excluded'][1] = 'Root Rules.Process returned; later Rules layers, accepted Session, House/map placement and paid movement remain excluded.'
    except Exception as error:
        diagnostic = dict(calls=calls, constructors=constructors, tiberium_constructors=tib_constructors,
            tiberium_reads=tib_calls, warhead_rereads=warhead_calls, rng_calls=rng_calls, native_epilogues=epilogues,
            current_counter=m.read32(scene + 0x214), allocator_cursor=m.cursor,
            status='Incomplete native Rules tail; no successful Process receipt')
        if isinstance(error, NativeExecutionError):
            error.diagnostics['rules_process_tail_progress'] = diagnostic
            if error.report_path is not None:Path(error.report_path).write_text(json.dumps(error.diagnostics, indent=2) + '\n')
            raise
        raise NativeExecutionError('Post-native Rules tail validation failed: ' + str(error), diagnostic) from error
    finally:
        for hook in hooks:m.u.hook_del(hook)


def metadata():
    from unicorn import Uc, UC_ARCH_X86, UC_MODE_32
    from tools.native_oracle import load_image, provenance
    image = load_image(Uc(UC_ARCH_X86, UC_MODE_32), profile=rules_process_tail_profile())
    return provenance(image=image, scope='Original ordered CRT and retained root Rules.Process through actual RET4',
        entry_points=dict(tiberium_crt=TIBERIUM_COLD_ENTRY, tail=BEGIN, tiberium_all=0x721D10, return_sentinel=RET_MAGIC),
        assumptions=['Original selected CRT includes Tiberium index3220 before Scenario; historical live-type mode unchanged.',
            'Same retained Rules/ART objects, physical root cache, native registry membership and Process frame through return.',
            'Root difficulty and all post-type readers execute; late constructors and Warhead rereads preserve native chronology.',
            'Only unchanged cold mode-zero command-bar absent-section return is qualified; no accepted Session/House/placement or gameplay parity.'],
        substitutions=['Inherited authenticated lexical/CSF/physical IO, bounded heap/CRT/TLS, null audio output and RGB565 Surface/clock priors.'])


def main():
    from tools.spatial_oracle.fv_cell_attack.steam_live_types import main as live_main
    return live_main(rules_process_tail=True)


if __name__ == '__main__':main()
