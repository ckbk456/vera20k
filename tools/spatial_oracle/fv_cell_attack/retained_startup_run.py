"""Own one source-frozen native startup run and retain failure/result evidence.

Run after sourcing environment.sh; choose a unique --run-name. Preparation
does not execute gamemd. Execution refuses existing outputs and equivalent
processes, investigates at900s, and waits for the same child to finish.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import signal
import subprocess
import sys
import time

ROOT=Path(__file__).resolve().parents[3]
MODULE='tools.spatial_oracle.fv_cell_attack.steam_movement_profile'
LIVE_MODULE='tools.spatial_oracle.fv_cell_attack.steam_live_types'
TAIL_MODULE='tools.spatial_oracle.fv_cell_attack.steam_rules_process_tail'

def digest(path):
    with path.open('rb')as source:return hashlib.file_digest(source,'sha256').hexdigest()

def write_new(path,value):
    with path.open('x',encoding='utf-8')as output:output.write(json.dumps(value,indent=2)+'\n')

def diagnostic(pid,started):
    result=dict(pid=pid,elapsed_seconds=time.monotonic()-started)
    try:
        directory=Path('/proc')/str(pid)
        fields=(directory/'stat').read_text().rsplit(')',1)[1].split()
        result.update(state=fields[0],parent_pid=int(fields[1]),user_cpu_ticks=int(fields[11]),
            system_cpu_ticks=int(fields[12]),rss_pages=int(fields[21]),cwd=os.readlink(directory/'cwd'))
        status=dict(line.split(':',1)for line in(directory/'status').read_text().splitlines()if ':'in line)
        result['memory']={key:status.get(key,'').strip()for key in('VmRSS','VmHWM','Threads')}
    except(OSError,ValueError,IndexError)as error:result['inspection_error']=str(error)
    return result

def live_equivalent():
    matches=[]
    for directory in Path('/proc').iterdir():
        if not directory.name.isdigit():continue
        try:
            parts=(directory/'cmdline').read_bytes().split(b'\0')
            if (MODULE.encode()in parts or LIVE_MODULE.encode()in parts or TAIL_MODULE.encode()in parts or any(part.endswith(b'steam_movement_profile.py')for part in parts))and Path(os.readlink(directory/'cwd')).resolve()==ROOT:
                matches.append(int(directory.name))
        except OSError:continue
    return matches

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run-name',required=True)
    parser.add_argument('--scope',choices=('prereaders','live-types','rules-tail'),default='prereaders')
    operation=parser.add_mutually_exclusive_group(required=True)
    operation.add_argument('--prepare-only',action='store_true')
    operation.add_argument('--execute',action='store_true')
    args=parser.parse_args()
    prefix='ordered-'+args.scope+'-'
    if not args.run_name.startswith(prefix)or not re.fullmatch(r'[a-z0-9-]+',args.run_name):
        raise ValueError('Use a unique '+prefix+' run name')
    os.chdir(ROOT)
    folder=ROOT/'.local/fv-movement-validation'/args.run_name
    target=ROOT/'tools/spatial_oracle/fv_cell_attack'/('steam_movement_'+args.run_name.replace('-','_')+'.json')
    if args.scope in ('live-types','rules-tail'):target=folder/'full.json'
    outputs=(target,target.with_suffix('.meta.json'),target.with_name(target.stem+'_reader.json'),target.with_name(target.stem+'_reader.meta.json'))
    if folder.exists()or any(path.exists()for path in outputs):raise ValueError('Owned run/output already exists; preserve it and inspect before a new run')
    if matches:=live_equivalent():raise ValueError('Equivalent native process exists: '+str(matches))
    command=([sys.executable,'-m',MODULE,'--retained-prereaders-only']if args.scope=='prereaders'else
        [sys.executable,'-m',LIVE_MODULE if args.scope=='live-types'else TAIL_MODULE])+['--write','--output',str(target)]
    # Reuse the earlier explicit producer/observer inventory, while freezing
    # current identities and all current tools. The historical freeze stays
    # immutable; it supplies paths, never source identities or native results.
    prior=ROOT/'.local/fv-movement-validation/retained-dialog-fourth-vm-freeze.json'
    if args.scope=='prereaders':
        inventory=json.loads(prior.read_text())
        paths={Path(name)if Path(name).is_absolute()else ROOT/name for name in inventory['producer_sha256']}
        paths.update(ROOT/name for name in inventory['independent_rust_observer_schema_reference_sha256'])
        paths.add(prior)
    else:
        paths={ROOT/name for name in('src/rules/native_processing.rs','src/rules/object_type.rs',
            'src/assets/asset_manager.rs','src/assets/mix_archive.rs')}
        paths.update(path for path in Path(os.environ['VERA20K_FV_MOVEMENT_ASSETS']).iterdir()if path.is_file())
    paths.update(path for path in(ROOT/'tools').rglob('*')if path.is_file()and '__pycache__'not in path.parts)
    paths.update((Path(os.environ['VERA20K_GAMEMD_EXE']),ROOT/'tools/tests/test_fv_rules_prereaders.py'))
    if args.scope in ('live-types','rules-tail'):
        paths.update(path for path in Path(os.environ['VERA20K_GAMEMD_EXE']).parent.iterdir()if path.is_file())
        from tools.projectile_oracle.bridge_render_inputs_palette import PALETTE_ASSETS
        from tools.spatial_oracle.fv_cell_attack.steam_movement_profile import color_palette_root
        paths.update(color_palette_root()/name for name in PALETTE_ASSETS)
    missing=[str(path)for path in paths if not path.is_file()]
    if missing:raise ValueError('Missing frozen input: '+str(missing))
    if args.prepare_only:
        print(json.dumps(dict(command=command,producer_count=len(paths),equivalent_processes=[],outputs_absent=True),indent=2));return
    before={str(path):digest(path)for path in sorted(paths)}
    folder.mkdir(parents=True)
    environment=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',VERA20K_NATIVE_EXECUTION_DIR=str(folder/'executions'),
        VERA20K_NATIVE_FAILURE_DIR=str(folder/'failures'))
    freeze=folder/'freeze.json';log=folder/'stdout.log'
    write_new(freeze,dict(command=command,cwd=str(ROOT),head=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),
        producer_sha256=before,environment={key:environment[key]for key in('VERA20K_GAMEMD_EXE','VERA20K_FV_MOVEMENT_ASSETS',
            'VERA20K_NATIVE_EXECUTION_DIR','VERA20K_NATIVE_FAILURE_DIR','PYTHONDONTWRITEBYTECODE')},
        outputs=[str(path)for path in outputs],profile=('steam-15918130-fv-ordered-rules-prereaders-v1'if args.scope=='prereaders'else
            'steam-15918130-fv-ordered-live-types-v1'if args.scope=='live-types'else
            'steam-15918130-fv-ordered-rules-process-tail-v1'),
        scope=('Selected ordered cold CRT and retained original Process prefix through668EED; no gameplay parity'if args.scope=='prereaders'else
            'Selected ordered Bullet/Sound cold CRT and original retained live type pass to668EF5; supplied physical IO/CSF/device priors; no gameplay parity'if args.scope=='live-types'else
            'Selected ordered CRT including Tiberium before Scenario and original retained root Rules.Process through actual RET4; supplied IO/device priors, stock absent command-bar; no Session/House/gameplay parity')))
    started=time.monotonic();child=None;interrupted=None
    def signal_handler(number,frame):raise KeyboardInterrupt('Owned runner signal '+str(number))
    signal.signal(signal.SIGTERM,signal_handler)
    try:
        with log.open('x')as output:
            child=subprocess.Popen(command,cwd=ROOT,env=environment,stdout=output,stderr=subprocess.STDOUT,start_new_session=True)
            print('OWNED CHILD',child.pid,'FREEZE',digest(freeze),flush=True)
            initial=diagnostic(child.pid,started)
            try:code=child.wait(timeout=900)
            except subprocess.TimeoutExpired:
                details=dict(initial=initial,current=diagnostic(child.pid,started),policy='Investigate exact owned process; continue original child')
                write_new(folder/'threshold-900s.json',details);print('THRESHOLD',json.dumps(details),flush=True)
                code=child.wait()
    except BaseException as error:
        interrupted=type(error).__name__+': '+str(error)
        if child is not None and child.poll()is None:
            os.killpg(child.pid,signal.SIGTERM)
            try:child.wait(timeout=30)
            except subprocess.TimeoutExpired:os.killpg(child.pid,signal.SIGKILL);child.wait()
        code=child.returncode if child is not None else None
    changed={name:dict(before=value,after=digest(Path(name))if Path(name).is_file()else'<missing>')
        for name,value in before.items()if not Path(name).is_file()or digest(Path(name))!=value}
    saved={str(path):dict(bytes=path.stat().st_size,sha256=digest(path))for path in outputs if path.is_file()}
    executions=list((folder/'executions').glob('*.json'))
    binding=False;error=None
    if code==0 and len(saved)==4 and len(executions)==1:
        try:
            from tools.native_oracle import _canonical
            payload,meta,reader,reader_meta=(json.loads(path.read_text())for path in outputs)
            raw=json.loads(executions[0].read_text())
            binding=(raw['semantic_payload_sha256']==meta['payload_sha256']==reader['semantic_payload_sha256']==hashlib.sha256(_canonical(payload)).hexdigest()
                and reader_meta['payload_sha256']==hashlib.sha256(_canonical(reader)).hexdigest()
                and raw['raw_receipt_sha256']==hashlib.sha256(_canonical(raw['raw_receipt'])).hexdigest()
                and raw['native_identity']['native_sha256']==meta['native_sha256']==reader['native_sha256']==reader_meta['native_sha256']
                and raw['source_normalized_lf_sha256']==meta['source_normalized_lf_sha256']==reader['source_normalized_lf_sha256']==reader_meta['source_normalized_lf_sha256'])
        except(OSError,ValueError,KeyError)as failure:error=str(failure)
    result=dict(exit_code=code,child_pid=child.pid if child is not None else None,elapsed_seconds=time.monotonic()-started,
        producer_count=len(before),producer_unchanged=not changed,changed_producers=changed,interrupted=interrupted,
        outputs=saved,raw_executions={str(path):digest(path)for path in executions},output_binding_valid=binding,binding_error=error,
        freeze_sha256=digest(freeze),log_sha256=digest(log)if log.exists()else None)
    write_new(folder/'result.json',result);print('RESULT',json.dumps(result),flush=True)
    if log.exists():print(log.read_text()[-8000:],flush=True)
    sys.exit(0 if code==0 and binding and not changed and not interrupted else 1)

if __name__=='__main__':main()
