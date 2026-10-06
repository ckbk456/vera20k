"""Immutable physical asset IO for the retained Steam live-reader VM.

Archive registration/Windows IO are supplied boundaries, never native execution.
Native filename formation, SHP readers and VXL/HVA parsing remain native owners.
The shared stock MIX decoder owns indexes; this owner retains source extents,
first registered winners and bounded read-only handles, without extracting files.
"""
from dataclasses import dataclass
from pathlib import Path
import hashlib
import struct

from tools.sidebar_oracle.stock import mix_hash, mix_index

THEATER_TABLE_ADDRESS=0x7E1B78
THEATER_RECORD_BYTES=112
THEATER_TABLE_BYTES=6*THEATER_RECORD_BYTES
THEATER_TABLE_SHA256='2881748ca63cb213fff046915e5a0e994ffc76b8135822a9b984da56ff7b6a93'
THEATER_INIT_BEGIN,THEATER_INIT_END=0x5349C0,0x534DD2
THEATER_INIT_SHA256='68de0c2b9de7bab294a8d5e2c533b81b570f201479aa08c50efefbd73d558d91'


def filename(value):
    """Native resource basenames only, without host path traversal or aliases."""
    if not value or not value.isascii() or any(c in value for c in '/\\\x00:'):
        raise ValueError('Physical live asset request must be an ASCII basename')
    return value.upper()


@dataclass(frozen=True)
class Span:
    path: Path
    offset: int
    size: int
    source: str
    identity: tuple

    @classmethod
    def disk(cls, path):
        path=Path(path).resolve();info=path.stat()
        return cls(path,0,info.st_size,path.name,(info.st_dev,info.st_ino,info.st_size,info.st_mtime_ns,info.st_ctime_ns))

    def read(self, offset=0, count=None):
        count=self.size-offset if count is None else count
        if offset<0 or count<0 or offset+count>self.size:
            raise ValueError('Physical asset read exceeds its immutable source extent')
        info=self.path.stat()
        if (info.st_dev,info.st_ino,info.st_size,info.st_mtime_ns,info.st_ctime_ns)!=self.identity:
            raise ValueError('Frozen physical archive changed: '+self.source)
        with self.path.open('rb')as stream:
            stream.seek(self.offset+offset);blob=stream.read(count)
        if len(blob)!=count:raise ValueError('Short physical asset read: '+self.source)
        return blob

    def child(self,offset,count,name):
        if offset<0 or count<0 or offset+count>self.size:
            raise ValueError('Nested archive member exceeds parent extent')
        return Span(self.path,self.offset+offset,count,self.source+' -> '+name,self.identity)


class PhysicalAssets:
    """Frozen named retail stack, first CRC winner; separate buffer/file reads.

    Matches the already established AssetManager core named-registration route.
    Media/theater/side/scenario registrations are explicit caller parameters;
    no arbitrary recursive archive scan or silent optional-theater selection.
    Loose readable files precede registered archives for read-only file opens.
    LoadFileFromMIX byte buffers are process-sticky by native CRC, with immutable
    aliases sharing the same selected bytes, independent of raw file opens.
    """
    def __init__(self, root, *, media_index=2, extra_archives=()):
        self.root=Path(root).resolve();self.loose={}
        for path in sorted(self.root.iterdir()):
            if not path.is_file():continue
            name=filename(path.name)
            if name in self.loose:raise ValueError('Ambiguous case-insensitive loose filename: '+name)
            self.loose[name]=Span.disk(path)
        self.archives=[];self.winners={};self.buffers={};self.requests=[];self.theater_registration=None
        for name in ('langmd.mix','language.mix'):self.mount(name)
        for index in reversed(range(100)):self.mount(f'expandmd{index:02}.mix')
        for name in ('ra2md.mix','ra2.mix','cachemd.mix','cache.mix','localmd.mix','local.mix'):
            self.mount(name,required=True)
        if not self.mount('audiomd.mix'):self.mount('audio.mix')
        # Freeze independent raw-read-first audio pair before bulk mounts.
        self.audio_pair={name:self.resolve(name)for name in ('audio.idx','audio.bag')}
        for name,required in (('conqmd.mix',True),('genermd.mix',False),('generic.mix',False),
                              ('isogenmd.mix',False),('isogen.mix',False),('conquer.mix',True),
                              ('cameomd.mix',True),('cameo.mix',True)):
            self.mount(name,required=required)
        if not 0<=media_index<=98:raise ValueError('Bounded numbered media index required')
        self.mount(f'mapsmd{media_index+1:02}.mix',required=True)
        self.mount(f'maps{media_index+1:02}.mix')
        self.mount('multimd.mix',required=True)
        if not self.mount('thememd.mix'):self.mount('theme.mix')
        if not self.mount(f'movmd{media_index+1:02}.mix'):
            self.mount(f'movies{media_index+1:02}.mix',required=True)
        for name in extra_archives:self.mount(name,required=True)

    def resolve(self,name):
        name=filename(name)
        return self.loose.get(name)or self.winners.get(mix_hash(name))

    def mount(self,name,*,required=False):
        name=filename(name)
        if any(row['name']==name for row in self.archives):return True
        span=self.resolve(name)
        if span is None:
            if required:raise ValueError('Missing required named retail archive: '+name)
            return False
        if ' -> CRC:' in span.source:
            span=Span(span.path,span.offset,span.size,span.source.rsplit(' -> CRC:',1)[0]+' -> '+name,span.identity)
        entries,index=mix_index(span.read,span.size)
        row=dict(name=name,source=span.source,bytes=span.size,
                 index_sha256=hashlib.sha256(index).hexdigest(),entries=len(entries))
        self.archives.append(row)
        for key,(offset,size)in entries.items():
            self.winners.setdefault(key,span.child(offset,size,f'CRC:{key:08X}'))
        return True

    def read(self,name,*,buffer=True):
        name=filename(name);key=mix_hash(name)
        if buffer and key in self.buffers:
            blob,source=self.buffers[key]
            self.requests.append(dict(name=name,crc=key,cached=True,**source))
            return blob,source
        span=self.resolve(name)
        if span is None:
            blob=None;source=dict(source=None,bytes=0,sha256=None,missing=True)
        else:
            blob=span.read();source=dict(source=span.source,bytes=len(blob),
                  sha256=hashlib.sha256(blob).hexdigest(),missing=False)
        self.requests.append(dict(name=name,crc=key,cached=False,**source))
        # Native missing LoadFileFromMIX requests are not cached successes.
        if buffer and blob is not None:self.buffers[key]=(blob,source)
        return blob,source

    def register_theater(self,native_index,original_record):
        """Supply the reviewed InitTheater named mounts on this existing owner.

        The attached-VM helper authenticates the record and native index. No
        cache is invalidated, earlier CRC winners are retained, and a theater
        switch requires a different cold owner rather than simulated unloads.
        """
        if type(native_index)is not int or not 0<=native_index<6:
            raise ValueError('Original native theater index must select one of six records')
        record=bytes(original_record)
        if len(record)!=THEATER_RECORD_BYTES:raise ValueError('Original theater record extent required')
        def text(offset,size):
            field=record[offset:offset+size]
            if b'\0'not in field:raise ValueError('Unterminated original theater archive field')
            value=field.split(b'\0',1)[0].decode('ascii')
            if not value or not all(c.isascii()and(c.isalnum()or c=='_')for c in value):
                raise ValueError('Invalid original theater archive field')
            return value
        label=text(0,16);long=text(0x30,10);iso_long=text(0x3A,10)
        iso_short=text(0x44,10);short=text(0x4E,4)
        fingerprint=hashlib.sha256(record).hexdigest()
        if self.theater_registration is not None:
            if (self.theater_registration['native_index'],self.theater_registration['record_sha256'])!=(native_index,fingerprint):
                raise ValueError('Physical theater registration cannot switch its cold owner')
            return self.theater_registration
        names=(([long+'MD.MIX']if native_index==1 else[])+
               [long+'.MIX',short+'.MIX',iso_short+'MD.MIX',iso_long+'.MIX'])
        rows=[]
        for name in names:
            already=any(row['name']==filename(name)for row in self.archives)
            present=self.mount(name)
            mounted=next((row for row in self.archives if row['name']==filename(name)),None)
            rows.append(dict(name=filename(name),present=present,already_registered=already,
                             **({k:mounted[k]for k in('source','bytes','index_sha256','entries')}if mounted else{})))
        self.theater_registration=dict(native_index=native_index,name=label,record_sha256=fingerprint,
            archive_order=[filename(name)for name in names],mounts=rows,
            original_entry=THEATER_INIT_BEGIN,original_body_sha256=THEATER_INIT_SHA256,
            boundary='Supplied original InitTheater named archive registration; native archive construction, theater initialization and unloads are not executed')
        return self.theater_registration

    def manifest(self):
        result=dict(boundary='Supplied named archive registration and immutable physical byte IO; original MIX traversal is not executed',
                    root=str(self.root),archives=self.archives,requests=self.requests,
                    frozen_files={name:dict(path=str(span.path),identity=list(span.identity))for name,span in self.loose.items()},
                    audio_pair={name:span.source if span else None for name,span in self.audio_pair.items()})
        if self.theater_registration is not None:result['theater_registration']=self.theater_registration
        return result

    def attach(self,owner):
        if owner.asset_source is not None:raise ValueError('Physical asset supplier already attached')
        # Preexisting palette cache values must agree with this physical winner.
        for name,blob in owner.assets.items():
            actual,source=self.read(name)
            if actual!=blob:raise ValueError('Existing physical asset disagrees with frozen winner: '+name)
        owner.asset_source=self
        return self.manifest()


def initialize_live_theater_assets(owner,assets):
    """Register physical theater sources selected by the same VM's native Map read."""
    from tools.native_oracle import file_span
    from tools.spatial_oracle.fv_cell_attack.steam_bullet_startup_scope import STEAM_NATIVE_SHA256
    if not isinstance(assets,PhysicalAssets)or owner.asset_source is not assets:
        raise ValueError('Existing attached physical asset owner required for theater registration')
    image=owner.image
    if image is None or image.machine is not owner.u or image.profile.native_sha256!=STEAM_NATIVE_SHA256:
        raise ValueError('Authenticated original Steam owner required for theater registration')
    if hashlib.sha256(image.data).hexdigest()!=STEAM_NATIVE_SHA256:
        raise ValueError('Original Steam theater source image changed')
    image.verify_code()
    body=file_span(image.data,THEATER_INIT_BEGIN,THEATER_INIT_END-THEATER_INIT_BEGIN)[1]
    table=file_span(image.data,THEATER_TABLE_ADDRESS,THEATER_TABLE_BYTES)[1]
    if (hashlib.sha256(body).hexdigest()!=THEATER_INIT_SHA256 or
        hashlib.sha256(table).hexdigest()!=THEATER_TABLE_SHA256 or
        file_span(image.data,0x827D64,7)[1]!=b'%s.MIX\0'or
        file_span(image.data,0x827D58,9)[1]!=b'%sMD.MIX\0'):
        raise ValueError('Original InitTheater archive name/order proof changed')
    if bytes(owner.u.mem_read(THEATER_TABLE_ADDRESS,THEATER_TABLE_BYTES))!=table:
        raise ValueError('Mapped original theater table changed')
    scene=owner.read32(0xA8B230)
    if not scene:raise ValueError('Native Scenario owner required before theater registration')
    index=owner.read32(scene+0x1258)
    if not 0<=index<6:raise ValueError('Native Map/Theater prerequisite required before archive registration')
    return assets.register_theater(index,table[index*THEATER_RECORD_BYTES:(index+1)*THEATER_RECORD_BYTES])


class ReadOnlyFiles:
    """Host Win32 read-only data transport; original guest File bodies execute."""
    def __init__(self,assets):
        self.assets=assets;self.handles={};self.serial=0;self.last_error=0;self.events=[]

    def open(self,name,access,share,security,disposition,flags,template):
        if (access,share,security,disposition,flags,template)not in (
                (0x80000000,1,0,3,0x80,0),(0x80000000,3,0,3,0x08000080,0)):
            raise ValueError('Unexpected native read-only CreateFile arguments')
        blob,source=self.assets.read(name,buffer=False)
        if blob is None:
            self.last_error=2;self.events.append(dict(api='CreateFileA',name=name,handle=0xFFFFFFFF,**source));return 0xFFFFFFFF
        self.serial+=1;handle=0x41000000+self.serial
        self.handles[handle]=dict(data=blob,position=0,source=source)
        self.last_error=0;self.events.append(dict(api='CreateFileA',name=name,handle=handle,**source));return handle

    def read(self,handle,count):
        row=self.handles[handle]
        if count<0:raise ValueError('Negative ReadFile request')
        start=row['position'];end=min(start+count,len(row['data']))
        row['position']=end;self.last_error=0
        blob=row['data'][start:end]
        self.events.append(dict(api='ReadFile',handle=handle,offset=start,requested=count,bytes=len(blob)))
        return blob

    def seek(self,handle,distance,high,origin):
        if high or origin not in (0,1,2):raise ValueError('Unreviewed native file seek')
        distance=struct.unpack('<i',struct.pack('<I',distance))[0]
        row=self.handles[handle];base=(0,row['position'],len(row['data']))[origin]
        position=base+distance
        if not 0<=position<=len(row['data']):raise ValueError('Native seek exceeds authenticated asset bytes')
        row['position']=position;self.last_error=0
        self.events.append(dict(api='SetFilePointer',handle=handle,distance=distance,origin=origin,position=position));return position

    def close(self,handle):
        if handle not in self.handles:raise ValueError('Closing an unowned asset handle')
        del self.handles[handle];self.last_error=0
        self.events.append(dict(api='CloseHandle',handle=handle));return 1

    def transport(self,call):
        iat=call.spec.iat;args=call.arguments
        if iat==0x7E11BC:
            pointer,*rest=args;characters=[]
            for offset in range(260):
                byte=call.read(pointer+offset,1)[0]
                if not byte:break
                characters.append(byte)
            else:raise ValueError('Native filename exceeds bounded basename transport')
            value=self.open(bytes(characters).decode('ascii'),*rest)
        elif iat==0x7E111C:
            handle,destination,count,result,overlapped=args
            if overlapped:raise ValueError('Asynchronous native file reads are not enrolled')
            if result!=call.sp+0x24:raise ValueError('Original RawFile ReadFile count receiver changed')
            blob=self.read(handle,count)
            if blob:call.write(destination,blob)
            call.write(result,struct.pack('<I',len(blob)));value=1
        elif iat==0x7E11C0:value=self.seek(*args)
        elif iat==0x7E11E0:value=self.close(*args)
        elif iat==0x7E1120:
            handle,high=args
            if high:raise ValueError('Unreviewed high-word native GetFileSize')
            value=len(self.handles[handle]['data'])
            self.events.append(dict(api='GetFileSize',handle=handle,bytes=value))
        else:raise ValueError('Unsupported original asset file import')
        call.return_to_native(value)

    def attach(self,owner):
        from tools.spatial_oracle.fv_cell_attack.steam_live_asset_scope import TRANSPORTS
        sites={spec.site:spec for spec in owner.image.profile.transports}
        for spec in TRANSPORTS:
            if sites.get(spec.site)!=spec:raise ValueError('Asset file API is absent from the frozen native profile')
            if spec.site in owner.transports:raise ValueError('Asset file API already owned')
        for spec in TRANSPORTS:owner.transports[spec.site]=self.transport
        owner.live_asset_files=self


def prepare_csf(owner,assets):
    """Prepare full physical lexical CSF cache for original734E60 lookup.

    This explicitly supplies decoded immutable CSF records, not native CSF file
    parsing. Native lookups, missing-key allocation and consumer fields execute.
    The original qsort/bsearch comparator7C8D20 uses case-insensitive ASCII keys;
    Records must sort by the comparator's ASCII lowercase fold, not uppercase
    byte order: punctuation sorts differently relative to uppercase letters.
    Stored uppercase keys retain source-owned value ordinals in +24.
    """
    from tools.storage_oracle.keyboard_bindings import parse_csf
    if any(owner.u.mem_read(0xB1CF6C,0x14)):
        raise ValueError('CSF cache already initialized; never replace retained state')
    blob,source=assets.read('RA2MD.CSF',buffer=False)
    if blob is None:raise ValueError('Physical active-YR CSF is required before live readers')
    entries,digest,physical_extras=parse_csf(blob,include_extras=True)
    names=sorted(entries,key=str.lower)
    if any(not key.isascii()or len(key.encode('ascii'))>=36 for key in names):
        raise ValueError('CSF keys exceed original native cached record extent')
    records=owner.alloc(len(names)*0x28);values=owner.alloc(len(names)*4);extras=owner.alloc(len(names)*4)
    ordinals={name:index for index,name in enumerate(entries)}
    for record_index,name in enumerate(names):
        owner.fixture_write(records+record_index*0x28,name.encode('ascii')+b'\0')
        owner.fixture_write(records+record_index*0x28+0x24,struct.pack('<I',ordinals[name]))
    for ordinal,name in enumerate(entries):
        value=(entries[name]+'\0').encode('utf-16-le');pointer=owner.alloc(len(value))
        owner.fixture_write(pointer,value)
        owner.fixture_write(values+ordinal*4,struct.pack('<I',pointer))
        extra=physical_extras[name];extra_pointer=0
        if extra is not None:
            extra_pointer=owner.alloc(len(extra)+1);owner.fixture_write(extra_pointer,extra+b'\0')
        owner.fixture_write(extras+ordinal*4,struct.pack('<I',extra_pointer))
    owner.fixture_write(0xB1CF6C,struct.pack('<I',len(names)))
    owner.fixture_write(0xB1CF74,struct.pack('<III',records,values,extras))
    from tools.spatial_oracle.fv_cell_attack.steam_live_formatter_scope import (
        FORMATTER_TRANSPORTS,FORMATTER_INTERLOCKED_CALLS,FORMATTER_INTERLOCKED_ARGUMENT)
    from tools.spatial_oracle.anytown_damage.mission import interlocked_update
    sites={spec.site:spec for spec in owner.image.profile.transports}
    deltas={site:delta for site,iat,size,register,delta in FORMATTER_INTERLOCKED_CALLS}
    def atomic_reader_count(call):
        if call.arguments!=(FORMATTER_INTERLOCKED_ARGUMENT,):
            raise ValueError('Native formatter atomic call changed its original DWORD receiver')
        call.return_to_native(interlocked_update(call.read,call.write,
            FORMATTER_INTERLOCKED_ARGUMENT,deltas[call.spec.site]))
    for spec in FORMATTER_TRANSPORTS:
        if sites.get(spec.site)!=spec or spec.site in owner.transports:
            raise ValueError('Native formatter import is absent or already owned')
        owner.transports[spec.site]=atomic_reader_count
    return dict(physical_source=source,source_sha256=digest,entries=len(names),
                boundary='Supplied full decoded physical CSF cache; native734E60 lookups execute; physical nativeCSF parser is excluded')


def prepare_sound(owner,assets):
    """Execute original disabled-output factory and full physical SoundList.

    Requires original ordered CRT750300 before Scenario, never synthesizes or
    resets the registry. Original403ED0 sets factory ready with null audio index;
    original4064A0 skips sample slots. No selected sound indices are supplied.
    Windows device startup/AudioInit caller and waveform mixing are excluded.
    """
    from tools.rules_oracle.bridge_anim_inputs import physical_sections
    if owner.read32(0xB1D378)!=0x7F68AC or owner.read32(0xB1D38C)!=10:
        raise ValueError('Full sound needs correctly ordered original Sound registry CRT750300')
    if any(owner.read32(a)for a in (0xB1D37C,0xB1D380,0xB1D388,0x87E294,0x87E2A0)):
        raise ValueError('Sound initialization requires original cold empty state')
    blob,source=assets.read('SOUNDMD.INI',buffer=False)
    if blob is None:raise ValueError('Active-YR physical SOUNDMD is required')
    sections=physical_sections(blob,names=None)
    if not sections.get('SoundList'):raise ValueError('Physical SoundList is empty')
    # Original7510D0 walks every physical source-order entry. Repeated names
    # reuse the original case-insensitive registry entry; validate that entire
    # observed result instead of treating an arbitrary successful return as a
    # complete catalog. This supplies no registry objects or indices.
    expected_names=list(dict.fromkeys(name.upper()for name in sections['SoundList'].values()))
    receiver=owner.alloc(0x40);owner.make_ini(sections,pointer=receiver)
    # invoke resetsECX; EDX is the original null-index argument for403ED0.
    from unicorn.x86_const import UC_X86_REG_EDX
    owner.u.reg_write(UC_X86_REG_EDX,0)
    owner.invoke(0x403ED0,0,timeout_us=30_000_000,context=dict(case='original-disabled-output-sound-factory'))
    if owner.read32(0x87E2A0)!=1 or owner.read32(0x87E294)!=0:
        raise ValueError('Original noaudio factory did not establish ready/null-index state')
    # The authentic complete registry performs source-order linear name
    # searches. Its 821 retail entries need a larger bounded instruction/time
    # budget than selected-entry witnesses; no native loop is bypassed.
    owner.invoke(0x7510D0,receiver,timeout_us=900_000_000,count=120_000_000,context=dict(case='full-physical-SOUNDMD-source-order'))
    count=owner.read32(0xB1D388);pointers=owner.read32(0xB1D37C)
    names=[];samples=[]
    for i in range(count):
        voc=owner.read32(pointers+i*4);sound=owner.read32(voc)
        names.append(owner.string(sound+0x6C));samples.append(owner.read32(sound+0x134))
    if [name.upper()for name in names]!=expected_names:
        raise ValueError('Original SoundList result does not match the full physical source order')
    if any(samples):raise ValueError('Native null AudioIndex admitted supplied sample slots')
    return dict(physical_source=source,ini_receiver=receiver,count=count,names=names,
                source_entries=len(sections['SoundList']),unique_source_names=len(expected_names),
                sample_counts=samples,factory_ready=1,audio_index=0,
                boundary='Original noaudio factory403ED0 and fullnative7510D0 definitions; supplied physicalINI lexical cache; Windows AudioInit/device/output excluded')


def prepare_eva(owner,assets):
    """Execute the complete original EVAMD DialogList over physical strings.

    Building CaptureEvaEvent resolves through original753250. Its complete
    native source-order catalog must exist before that reader executes; no
    empty registry, selected indices or decoded EVA fields are supplied.
    """
    from tools.rules_oracle.bridge_anim_inputs import physical_sections
    from tools.spatial_oracle.fv_cell_attack.steam_live_catalog_scope import (
        EVA_REGISTRY,EVA_REGISTRY_VTABLE,EVA_CLEAR_ENTRY,EVA_LOAD_ENTRY,EVA_ENTRY_BYTES)
    if owner.read32(EVA_REGISTRY)!=EVA_REGISTRY_VTABLE or owner.read32(EVA_REGISTRY+0x14)!=10:
        raise ValueError('Full EVA needs correctly ordered original registry CRT752210')
    if any(owner.read32(EVA_REGISTRY+offset)for offset in (4,8,0x10)):
        raise ValueError('EVA initialization requires original cold empty state')
    if any(owner.read32(address)for address in (0xB1D4BC,0xB1D4C4,0xB1D4CC)):
        raise ValueError('EVA cold clear cannot replace retained playback or queue state')
    blob,source=assets.read('EVAMD.INI',buffer=False)
    if blob is None:raise ValueError('Active-YR physical EVAMD is required')
    sections=physical_sections(blob,names=None)
    if not sections.get('DialogList'):raise ValueError('Physical EVA DialogList is empty')
    expected_names=list(dict.fromkeys(name.upper()for name in sections['DialogList'].values()))
    receiver=owner.alloc(0x40);owner.make_ini(sections,pointer=receiver)
    owner.invoke(EVA_CLEAR_ENTRY,0,context=dict(case='original-cold-empty-EVA-clear'))
    owner.invoke(EVA_LOAD_ENTRY,receiver,timeout_us=180_000_000,count=30_000_000,
                 context=dict(case='full-physical-EVAMD-source-order'))
    count=owner.read32(EVA_REGISTRY+0x10);pointers=owner.read32(EVA_REGISTRY+4)
    names=[];records=[]
    for index in range(count):
        record=owner.read32(pointers+index*4)
        names.append(owner.string(record))
        records.append(bytes(owner.u.mem_read(record,EVA_ENTRY_BYTES)).hex())
    if [name.upper()for name in names]!=expected_names:
        raise ValueError('Original DialogList result does not match the full physical source order')
    return dict(physical_source=source,ini_receiver=receiver,count=count,names=names,
                source_entries=len(sections['DialogList']),unique_source_names=len(expected_names),
                original_record_hex=records,
                boundary='Original cold clear7531A0 and full753000/752DB0 EVA definitions; supplied physicalINI lexical cache; queue/playback/Windows startup excluded')


def initialize_live_asset_inputs(owner,assets,*,progress=None):
    """Attach the caller's already frozen physical IO and pre-live catalogs."""
    if not isinstance(assets,PhysicalAssets):raise ValueError('A frozen physical asset owner is required')
    assets.attach(owner)
    from tools.spatial_oracle.fv_cell_attack.steam_live_reader_helpers_scope import LIVE_READER_WS_PRINTF_CALLS
    for row in LIVE_READER_WS_PRINTF_CALLS:
        if row['site']in owner.transports:raise ValueError('Occupancy-key Windows transport already owned')
        owner.transports[row['site']]=owner.import_transport
    files=ReadOnlyFiles(assets);files.attach(owner)
    csf=prepare_csf(owner,assets)
    if progress:progress('Physical CSF cache prepared; original full Sound loader starting')
    sound=prepare_sound(owner,assets)
    if progress:progress('Original Sound loader finished; original full EVA loader starting')
    eva=prepare_eva(owner,assets)
    if progress:progress('Original EVA loader finished')
    return dict(assets=assets.manifest(),csf=csf,sound=sound,eva=eva,
                limitations=['Host archive registration/file IO and decoded CSF cache are supplied boundaries',
                             'Fullnative Windows startup/device lifecycle and audio waveform output are excluded'])
