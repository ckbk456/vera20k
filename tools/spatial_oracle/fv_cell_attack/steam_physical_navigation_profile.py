"""Scoped physical-map prerequisites for the selected ordinary FV chain.

Theater reader seams are independently runnable. Cell/TMP/graph execution is
still a separate qualification obligation; this declaration does not enroll it.
No region is discovered or enrolled from a running failure or CLI input.
"""
from pathlib import Path
import os

from tools.native_oracle import ExecutionProfile, finish_vectors, provenance, load_image, RET_MAGIC
from tools.rules_oracle.theater_general_reader import NATIVE_ASCII_PRINTF_REGIONS, NATIVE_ASCII_PRINTF_READS
from tools.spatial_oracle.fv_cell_attack.steam_movement_profile import (
    STEAM_CONSTRUCTOR_KEYS_PROFILE as PARENT, STEAM_SCENARIO_PROFILE,
    constructor_inputs, NATIVE_SCENARIO_BYTES,
)

# Original theater scalar block, ordinal publication, count/name caller seams,
# and bounded original sprintf/ASCII integer/string formatting machinery.
THEATER_REGIONS = (
    (0x545535, 0x545C3F, '731c8523848c3a43bf03fd79288d326afef03f1261080fd1481a11dd031360f1'),
    (0x545CEF, 0x545FA3, 'e9abf9b4e3e2c165a41d0faab149945f34e64d302471773d09ebd8c782a508c2'),
    (0x545FA3, 0x545FE5, '71dad8320753a98261f9eabdc404227914857b4162d608969c3dca50cc2df9ae'),
    (0x545FE5, 0x54609C, 'ec550d9e2c9371b13739a9d5e5185b32a0682f86a9e0818229a334d8bece694d'),
    (0x54609C, 0x5460EA, '7cf8f828a97e8320a309bd847284e437c2cc3ae2809791833ce612db2dc82404'),
    (0x5462B3, 0x54637B, '8e69910f0c2f8595a87b7752cf364ecd872b1211bffe6f92323dcc5cd09d176f'),

)
# All original role stores in the two selected theater blocks; no broad BSS.
THEATER_DATA = (
    (0xAA0738,20), (0xAA0E18,20), (0xAA0E38,4), (0xAA101C,16),
    (0xAA1050,12), (0xAA1090,40), (0xAA1130,8), (0xAA1540,4),
    (0xAA1548,4), (0xABAD1C,24), (0xABB104,16), (0xABBEBC,16),
    (0xABC1D0,12), (0xABC1E8,4), (0xABC1F8,4), (0xABC2B0,12),
    (0xABC2C8,8), (0x24000000,0x2000000),
)
THEATER_ENTRIES = (
    (0x545535,(0x545C3F,)), (0x545CEF,(0x545FA3,)),
    (0x545FA3,(0x545FE5,0x546C23)), (0x545FE5,(0x54609C,)),
    (0x54609C,(0x5460EA,)), (0x5462B3,(0x54637B,)),
)
STEAM_PHYSICAL_THEATER_PROFILE = ExecutionProfile(
    name='steam-15918130-fv-physical-theater-v1',
    native_sha256=PARENT.native_sha256,
    regions=PARENT.regions+THEATER_REGIONS+NATIVE_ASCII_PRINTF_REGIONS,
    entries=PARENT.entries+THEATER_ENTRIES,
    reads=PARENT.reads+THEATER_DATA+((0x8291A4,0x61C),(0x826278,8))+NATIVE_ASCII_PRINTF_READS,
    writes=PARENT.writes+THEATER_DATA,
    fixture_writes=PARENT.fixture_writes+THEATER_DATA,
    sinks=PARENT.sinks,transports=PARENT.transports,
)

# Original Map/Theater lookup, selected Init_Theater suffix-pointer seams and
# all eleven TileSet property reads/stores. The static packet is
# physical-theater-property-suffix-enrollment-discovery.json; these are literal
# reviewed declarations, not profiles assembled by observing runtime failures.
THEATER_PROPERTY_REGIONS = (
    (0x475870,0x4758BD,'b054e28e3741b38c416948dea5337eaf0f264c1feb053734682b31a87247bbb9'),
    (0x48DBE0,0x48DC13,'f6262a6f7398d83d222712165b6318699655b6a7f48e5cddfe8796b01c798704'),
    (0x5349D7,0x5349E9,'50f3298a361cb78f141672f512ef03e015fbbc9f16c33d802dd968131d601062'),
    (0x534A05,0x534A0F,'4f77e5e5723fc6824bd4675192ca985119915d30c639a77c99baeb1f00fcdeba'),
    (0x5460EA,0x546254,'ac39605ba7d57abe97ae5e46cdb526e0d6fad195f5b05e162c437dd731d15328'),
    (0x54641F,0x5464BB,'3fae5a065f4414114073643ca2f6166d987828b6896e1c98cbb6f4e90161975c'),
    (0x687631,0x68764F,'9a6fdac8daca837825ea16ace8fe05918307fb5c63505f606bfad070151f7ba4'),
)
STEAM_PHYSICAL_THEATER_PROPERTIES_PROFILE = ExecutionProfile(
    name='steam-15918130-fv-physical-theater-properties-v1',
    native_sha256=PARENT.native_sha256,
    regions=STEAM_PHYSICAL_THEATER_PROFILE.regions+THEATER_PROPERTY_REGIONS,
    entries=STEAM_PHYSICAL_THEATER_PROFILE.entries+
        ((0x5349D7,(0x5349E9,)),(0x534A05,(0x534A0F,)),
         (0x5460EA,(0x546254,)),(0x54641F,(0x5464BB,)),(0x687631,(0x68764F,))),
    reads=STEAM_PHYSICAL_THEATER_PROFILE.reads+
        ((0x7E1B78,6*112),(0x818658,8),(0x81FFF0,4),(0x889F64,1),(0xAA102C,20)),
    writes=STEAM_PHYSICAL_THEATER_PROFILE.writes+((0xAA102C,20),),
    fixture_writes=STEAM_PHYSICAL_THEATER_PROFILE.fixture_writes,
    sinks=PARENT.sinks,transports=PARENT.transports,
)

# Actual Overlay/Tiberium registries, named constructors, the selected physical
# Overlay seams (including its Tiberium post-read), and original land reads.
# Reviewed original roots/ranges are retained in physical-{retail-input,
# overlay-constructor,cold-registry,overlay-fields}-* discovery receipts.
# Image721C55's six-way table selects original registered Overlay pointers;
# it does not authorize the omitted ObjectType SHP/archive reader.
PHYSICAL_INPUT_REGIONS = (
    (0x4068F0,0x40691A,'432cef6e6e896601d640d904aceea20a89b8f6cae3c7d02815479cbf21d9bd63'),
    (0x42D470,0x42D486,'f587c5ef77c25ad468d958d7b4fb0b689d67b427e960eeae90dca882f0f36fbe'),
    (0x465D80,0x465D83,'58367ffa2a0179375018fa0f5c26da24391e42ebe0ed8fdda35a21fc7bdc396f'),
    (0x474B50,0x474C1F,'7e149d7b8c8f00a69075a7817852aee0a2a047dbf0305b88bee9f4ddb92a13cf'),
    (0x4754B0,0x47550F,'98a804e1432cc567a719f7a0b620bee4ce71b276d7175d1743603ce691e9c714'),
    (0x48DF80,0x48DFCB,'3fbb40b7f920f92adda8c0acbec3b1ba7afb80dc4a80f26f2598fa4663489c8f'),
    (0x48DFD0,0x48DFE3,'c58efa4261edb864f9c1f18256bb4c66c92685aef2de7839cc2f776a54c8dc66'),
    (0x4E71E0,0x4E721D,'1632b1e399c9df07ad893aaffc72e429eb96a1e3279eae9153debaf3f7ece0fc'),
    (0x4E72E0,0x4E731D,'7538a29e8f73ad80c1c1d96e571b3e696df220af7bf48893fd034c2e2baf62cb'),
    (0x4E8C60,0x4E8C8A,'cee3614be8cc3487981e654512c2b1258d2a37748e0212265f61a1813f0aef1e'),
    (0x4ED2C0,0x4ED370,'e2896f8878455b39bb7a1834178877bea015f3331fb5428c62f3f8f6afb1b645'),
    (0x526960,0x526A21,'2f0948d96f67eed5a2b5d3a57a1a7ef93e8eaf2e59a1efe7e1318164cb983941'),
    (0x526CC0,0x526D8D,'73c6bd3f5433fecc285b21f69f3318960b0a64b86f590ab077dac71fd4f6d486'),
    (0x52B430,0x52B4C5,'45e46388dc26e87408267eed8da45d32f3b674fa982f2a204c3ded75888038aa'),
    (0x52B600,0x52B61B,'b4be17007c7a21c076634259b8a92af8be05edf2bc1bf564fc6a09cd1ca7ac20'),
    (0x5FE250,0x5FE3B4,'d48a6052bc4f21c99fe8ad8674d470475f42e73a85efd79e0785d19f91565dbc'),
    (0x5FE798,0x5FE8A6,'d658bd0b98bbd9dc45bfc0b750684c75c02896efd6705c3ccd6238ece8bb4562'),
    (0x5FE8C9,0x5FE8F1,'149e9e8eb74bb1ba1bde9adc1ea6333e5af16db3d14b6e8b3930a28fb97efd49'),
    (0x5FE933,0x5FEA09,'3891ba6e49324af16b2243892333b94ae7ef7eb4496a27d03b7f463fe8ec2fbd'),
    (0x5FEA0A,0x5FEA10,'0cfd575f0cb8678ca686e74f932a95a3c133f925206679e13213c9131b286e23'),
    (0x5FEC70,0x5FECF3,'a7ecec49ff39a31c4f129f57b50aa4c7fc358004203728565f322b36b2a97862'),
    (0x665F3B,0x665F41,'3fa5913f9a7a060b169746696eee77b5fb2b07c7ca278dbcc49acc2bdb7d3f82'),
    (0x666DF8,0x666E02,'04f9693a90a571f0f383872cb7b63faa93c102cd86f9158dd79de14665553a1f'),
    (0x668CE3,0x668D34,'8015b2e470b9d515709b66efa6d21f4438219297ae5f2a8d88e5dc2d5e74f1ec'),
    (0x66F1CB,0x66F1EC,'e1a9d5974f717adfe94540cf7971342b09fe4f643a4d37786c981dffc5d9660d'),
    (0x671DD2,0x671DF1,'0b88ab71eb16e0e5f572179b4c3f673e84aef43ce7785b711521a93405383720'),
    (0x674000,0x674238,'c3987b278e62fbc833cbb68ac9811301ed879344e1cab226a1420940b068218d'),
    (0x71D580,0x71DA7D,'42cc1f0f8767e340e94293a8344e43230605ff2385f0aef19cfcf01d7ca6c43d'),
    (0x721640,0x72167D,'e6d0a3e4de5debb5c2afb6dc43ff857f9afdbc04d3c17a9aa152174e15ef02a0'),
    (0x7216C0,0x72187E,'3c352c498af301fa2aca6fee238ad654f4a728c22f87a2686915dc0bbf5626ce'),
    (0x721AFA,0x721B12,'6d7972f56f25e57a0f480d7aa33df3f6ad18d997d268e435f8a16f297493c8d4'),
    (0x721C3F,0x721C5C,'e6ffb72315e5c4d8bf19aba5022f9ae8accc60df725337f6eff3ef47dd062ff1'),
    (0x721C5C,0x721C7B,'00bdb26948e5d7efb77152ea2e31ad75a0da189988c250a0eb8288c49857f3ea'),
    (0x721C88,0x721CDC,'bbed4dc4541125cbb821be1c466f1c160e77f4ec752b3236ae4cba172f42c0fb'),
    (0x723730,0x72375A,'89a1076876717e0c7c8617d06f08311fd3ac90792cbe474abf5d5291fcc6595c'),
    (0x723910,0x7239C0,'c13d7d0be3b737f4f12d45efcb1c898eb642fd655118676298a5bd89e6b1570a'),
)
# 71D580's final original REP STOSD at71DA73 clears140 DWORDs atB0EF00
# throughB0F12C. Together with its earlier coordinate tables the exact extent
# isB0EDC0..B0F130. Selected maps have no Terrain entries: leave this BSS
# undeclared/uninitialized, so a future unexpected consumer fails closed.
PHYSICAL_INPUT_DATA=((0xA83D80,24),(0xA8E318,24),(0xB0F4E8,24),
                     (0x89EA40,12*36))
PHYSICAL_INPUT_READ_ONLY=(
    (0x7EA164,28),(0x7EA1E4,28),(0x7F56BC,28),(0x7F0C9C,4),(0x7F0CD0,4),
    (0x817278,12),(0x817474,12),(0x817694,8),(0x8184A8,12),
    (0x8189B0,16),(0x819420,8),(0x81AC58,8),(0x81BAE8,8),
    (0x81BB18,8),(0x81DA28,48),(0x81DBA0,0x84),
    (0x832B78,8),(0x8334D0,0xBC),(0x839D68,48),(0x839DA8,13),
    (0x83B42C,24),(0x83C8CC,24),(0x83D4B4,12),(0x8448EC,8),
    (0x721CF8,24),
)

# Full Rules tail adds only the gaps in the existing Tiberium owner. Its live
# parent already inherits PHYSICAL_INPUT_REGIONS/DATA/READ_ONLY: cold721640,
# ctor7216C0, selected Value/Image bodies, B0F4E8 and the six-way Image table
# remain those original declarations. Existing physical profiles below do not
# consume these additions. See steam_physical_navigation_profile.md for proof.
RULES_TIBERIUM_REGIONS=(
    (0x721A50,0x721AFA,'6d5183de7c54f6fa6e02fe89cf79ac94d71273293c2a4752a0fa55bbef1a3d89'),
    (0x721B12,0x721C3F,'ef88c42a22de53b33367befac15aef8a5b75d4715578cb1d3b1ed73fd3cf14a4'),
    (0x721C7B,0x721C88,'b5902c20b349b25dffece689edb470d48874cc646a13a51544b8e5189312120d'),
    (0x721CDC,0x721CF6,'794eca6091bac2c13e01601d445e019bf1e65b9810ef4940e6753298c5d5997b'),
    (0x721D10,0x721DBA,'89cd46d5fad87ef8006dea6e40fe7db90da2c52e63299b5eaa589843ff0e71ef'),
)
RULES_TIBERIUM_READ_ONLY=(
    (0x7F578C,4),  # Actual721D9F primaryVT7F5728+64 ->721A50 ReadINI.
    (0x8448E4,7),  # Debris
    (0x8448F4,17),  # GrowthPercentage
    (0x844908,7),  # Growth
    (0x844910,17),  # SpreadPercentage
    (0x844924,7),  # Spread
    (0x84492C,10),  # Tiberiums
)
# Registry, Abstract vector, root globals and native heap belong to the live
# parent. No fixture registry/header/index or new mutable BSS is introduced.
RULES_TIBERIUM_NATIVE_DATA=()
RULES_TIBERIUM_ENTRIES=((0x721A50,(RET_MAGIC,)),(0x721D10,(RET_MAGIC,)))

STEAM_PHYSICAL_INPUTS_PROFILE=ExecutionProfile(
    name='steam-15918130-fv-physical-inputs-v1',native_sha256=PARENT.native_sha256,
    regions=STEAM_PHYSICAL_THEATER_PROPERTIES_PROFILE.regions+PHYSICAL_INPUT_REGIONS,
    entries=STEAM_PHYSICAL_THEATER_PROPERTIES_PROFILE.entries+
        tuple((a,(RET_MAGIC,))for a in (0x4E71E0,0x4E72E0,0x526810,0x5276D0,0x5295F0,
                                      0x528A10,0x674000,0x71D580,0x721640,0x7216C0))+
        ((0x5FE798,(0x5FE8A6,)),(0x5FE8C9,(0x5FE8F1,)),
         (0x5FE933,(0x5FEA09,)),(0x5FEA0A,(0x5FEA10,)),
         (0x665F3B,(0x665F41,)),(0x666DF8,(0x666E02,)),
         (0x668CE3,(0x668D34,)),(0x66F1CB,(0x66F1EC,)),
         (0x671DD2,(0x671DF1,)),(0x721AFA,(0x721B12,)),
         (0x721C3F,(0x721C7B,0x721CDC))),
    reads=STEAM_PHYSICAL_THEATER_PROPERTIES_PROFILE.reads+PHYSICAL_INPUT_DATA+PHYSICAL_INPUT_READ_ONLY,
    writes=STEAM_PHYSICAL_THEATER_PROPERTIES_PROFILE.writes+PHYSICAL_INPUT_DATA,
    fixture_writes=STEAM_PHYSICAL_THEATER_PROPERTIES_PROFILE.fixture_writes+PHYSICAL_INPUT_DATA,
    sinks=PARENT.sinks,transports=PARENT.transports,
)


# Original Map/Cell/TMP input producer for the separately authored clear map.
# Literal roots/spans were reviewed in physical-cell-prefix-closure-static,
# physical-prefix-actual-empty-registry-static and physical-scenario-lighting-
# reader-static receipts. No profile is assembled from observed execution.
# Dormant waterfall/animation/shadow branches and full palette initialization
# remain fail-closed outside this selected Tile0/overlayFF/ShadowCasterfalse path.
CELL_PREFIX_REGIONS = (
    (0x421B60,0x421C81,'7be2d34557a7b156778538acb80c33b82c572831d0b66b21979cb3733ee74925'),
    (0x40AFA0,0x40AFB6,'24d68f0ef1029c864de26a653af2bce0754a2a85b4ce27ed70b2ba197a2d4ac1'),
    (0x42A6D0,0x42A8FA,'843a211b886f65e2fabae5e0a1a787da9473781abdcb3183d4899eced6d7c151'),
    (0x42AC00,0x42ACED,'9494f21cfd51685f393b03aa1f49644f42cf6f44942a5ec7e03d7814c60558b9'),
    (0x42D510,0x42D539,'8fa89860230552cb905c14a11c3fa3197f15baab8088341cb503569835fe934a'),
    (0x42D540,0x42D56A,'480571baece26ea08460228641b466b64b7db3ecb06bdae72a8e278461a3d843'),
    (0x42DC50,0x42DC9A,'0f3f49e83b57250a9be2987895a3f8123a2015af913286d7ae1aa72620f9882b'),
    (0x42F420,0x42F44A,'27cbb548042a5011cf111624a403c704ec6c2a9245eb82b97cdf14dc8b28e510'),
    (0x42F860,0x42F92A,'bf3e18e8c6d3705ed7095d3090f6699b00210a690fab9979a95cbecba8f15018'),
    (0x42FCB0,0x42FD22,'058a578a361b1b87f513fb8c7ec289edfcb98e29c8464488cd37a5a4df59c431'),
    (0x47B150,0x47B178,'9ca05a2be02dc492ce611745a788ad56c65b3cca7ace547bbf7b5a4dff2773c7'),
    (0x47B180,0x47B193,'621e22aceda6c1515390964e8cc99d8f781ba66f814d138c00dda8e285daa1c3'),
    (0x47B1A0,0x47B1B3,'da64ad6fd8c756db16ea3adb1d42d88b3d6ebf57151aad911503e8795dd27ea8'),
    (0x47B1C0,0x47B1D3,'0999acfb8c5744d67c3205d186530f0037b6024bd7128d35fe4864ad2ac7a34c'),
    (0x47B1E0,0x47B1F3,'7e39a75b64dd93406292fff0b5945e23af40dbd94fd22b94c37ea3bd7d0a4eb2'),
    (0x47B200,0x47B213,'7464d81e5c2d094dc9b83df336243eefb2946a7dbb88ef7ecb3dff48828ec8b5'),
    (0x47B220,0x47B251,'fc81fb486f513d6eefd711068b697f25a6701d0acd107741820321a03deddd02'),
    (0x47B260,0x47B281,'959d9f7f4e8f33e095b57c5d2c5651a2064d54b8b6943f05c4d7ddad47e9bad4'),
    (0x47B290,0x47B2BC,'d985373956ef0541daba43ebe414a047d633e1e6122269598a973803429c395b'),
    (0x47B2C0,0x47B2E7,'09c1187cb3c0634d045b9aa49a21804ef957e5c3d30a3309fac360653f43d67d'),
    (0x47B2F0,0x47B2FF,'c2a6bfdfd8584bd133719d80916ccf5add31e5007564f6678d02a6e58b22f058'),
    (0x47B300,0x47B312,'9f18fca2223758dab3df1fd53b2230e063224812bb99608ffc70f8b0facb5eb2'),
    (0x47B320,0x47B33A,'7e08dc08bc97d3d1ff28207ea4b1fc9caf083210a0df5b54048efe479f799deb'),
    (0x47BBF0,0x47BDA8,'abc5f47c9d770dd4341ba5167e5841f4c347d59a13d9b810edfd696506553c99'),
    (0x47CA80,0x47D20A,'ab47d106d96bcbd53ce5a112542be824192a8c6e0cd9e4bd8613565b86e04ab0'),
    (0x47D2B0,0x47DD64,'515282c905f975ec44e8ccbac28c898f5163b72eebc04541183e4a87877eac06'),
    (0x483C80,0x483E29,'fe7d7a78e5b24725d0477cfbb4807298f93c94fe4f8f8dd86bdb273188bb3387'),
    (0x483E30,0x484041,'e0c5c9f644e5ef04cc034ccd008aa4ec63b612dcb653fed10f19165147f838d2'),
    (0x484180,0x484678,'a9a2285793906cb12b173be91110896124c69c47123cbd4c4bdc5751366c8e35'),
    (0x485020,0x485053,'1e27a9fc9c4245cc91bb794bbe713b10ca7db3d960617af9adb2bf4fb948338c'),
    (0x49F2F0,0x49F39C,'ab85906af665f42b5c85a90d7dd969c6a9d743362a691883cd3aa73c337173ac'),
    (0x49F3A0,0x49F414,'b1963497a98839ab820d963a9d81d90c483de43017c38320223d18a30ec6fd3e'),
    (0x4E6A60,0x4E6A9D,'c0c182169a0699585e0a7c79f25600de6461c25298d2f08407826507632d0869'),
    (0x4E6D60,0x4E6D9D,'cb8a1c9cb6bf2d4c46df1cb926dbb62e5272ee0f89aad91cbb64f3d8df5b1f34'),
    (0x4E74E0,0x4E751D,'e9179bc8dc5523c30940341e684cda0507a7110f8ccaa1cb52f1d80fafb5707a'),
    (0x4E76E0,0x4E771D,'039655c722b36671f9a3ff87c2b42d12691f0fe8777c67cdea593a726143772e'),
    (0x4E9020,0x4E904A,'31d4d54426557d1f122d4f9a0f757a46c5e53e1d916009482416058f609d205a'),
    (0x4EEA80,0x4EEB30,'3af1a1ea9e830a28438b6921ed487eda3ffc85fcf0e4553fbf014c8a30cfdde5'),
    (0x4F4220,0x4F4238,'3cabebfe45691204f23c2a373851091e3c603acc675565b033d9617ba9ae33e2'),
    (0x4F42A0,0x4F42AB,'cd56aea250c31ec9d716997caaa854680cccef5b2c54ea58dff33ddd249188a0'),
    (0x53A100,0x53A106,'0df1bda41367c95520601de539061753e7e14c44b23968196cfe32bdfd370941'),
    (0x53A110,0x53A11F,'72243a7a806855d73e41c662229fd93036bef1086da194736e7df04ce93854fc'),
    (0x53B400,0x53B40B,'d55b1dcc81533efa41fe4ed8998fe4ca654655df91119a0e944f639a119c58cb'),
    (0x5447C0,0x5449FD,'44e3add8df32e28a1ea19a37dc512a43b10c46743ac7b95470ff93bd6ac1d054'),
    (0x544BE0,0x544C18,'eca9364704400542cc58c1e6131a1cc0ef6caf484f6a246bafeb4f59cd27f20d'),
    (0x544C20,0x544C73,'523351cb12404dcbeebd37d0c78accaa2280cda4b295daffcae1803cc2868d9a'),
    (0x544C80,0x544CAB,'a15ab05b1dea37bcbda868b9a6a3178d25c1b6611d0f97bce7d8811ccf342333'),
    (0x544CB0,0x544CD6,'ac0c5d45d78f174c2283da57b322b78600591e9c4aa11f51a9e75365106447a5'),
    (0x544E70,0x544FE1,'509fddecf00581ff52b48c3f02ae6268b7dad8427df5d381e58bc38fc068d2e9'),
    (0x547150,0x5471A5,'eed1b7763d6f82d2d4e35ff0af7b35b1ac11c90e8ff39bede754e1da01dcfbcf'),
    (0x5471B0,0x5471E1,'2f34d2292d6064e23b126e13bd55d162f62dbd708c7fdce8837b053f9021031a'),
    (0x554640,0x55467D,'4d0dcf83fce708c672e42e894cb242cf1cb5cbff5807b58e523d8819fca630bf'),
    (0x5558E0,0x555ABA,'86958a6b4537c608a3471e259e0ef6c97df619d5dfcf068b427cb4c18efb408d'),
    (0x565090,0x565184,'3ee75d9faf2546a0b15474b939b6ea634b6c6aeb96f955d50c172d3fd496f1ae'),
    (0x5657A0,0x5657D8,'bdb90075c58df4b3aecb81d54cfdc37b3259ad9da64d01c216e4ec634ae5a7b8'),
    (0x565800,0x5659ED,'b1cd9306df95c32a5190e7e2756c6ec26ef170c6aeeecaeba2b3f11579a3d184'),
    (0x565AA0,0x565AFE,'81ebfb337d36437296efaeb1a66aa1f52e2ec83b8412cbe5de93a17e94c111a9'),
    (0x567110,0x5671E9,'c36ed3e1a070ed8b5c2b1b61f15054e342e3b0bfa8790884e4e595476d0d388b'),
    (0x567230,0x5672D3,'d24907d262029b4c5eb0b1729cad8e7551eb93e4284feda14c811c4cbccc0d26'),
    (0x568BB0,0x568E39,'fd0d6b47b41a87610b5ab830e0fbe17fe130c16c3b120cc4bb2cfb1e7ab55883'),
    (0x56D3F0,0x56D426,'226651300930972ccc0ff20a26be3337e498166fb2d3b1b2443ccfcfe6214eab'),
    (0x578290,0x578342,'243fef03ecb3f0f20a8bf67b35f88d10e852f80bf4eec95f260f0af4bb45d3fb'),
    (0x578460,0x578537,'4d6c54da19576f69b0f549300f7d628a3cde8403ea016159c2eaee865a50c15b'),
    (0x588D60,0x588DD8,'868780020889fc3165dc8bdad926c530f5201df73244431e37f49352eac7d445'),
    (0x588F60,0x588F8A,'3585ec6f393a63312617b3cbb2880ce1724ff387547f0febc2c26cf864470525'),
    (0x588FD0,0x588FFA,'6a9dbc3eb274421d15549f5c7b1667e5c7c0954946722ba7c1a8df456e495804'),
    (0x589CE0,0x589D8E,'4b7f880b8fbce9205c112bc9a08216f0b228bfbf7943d9151bdf32d3900dc79c'),
    (0x589D90,0x589DB7,'ea6f38c14ba77f529d4d98e8426ba741dc765dfae84c5128e21cf2540e6e4125'),
    (0x58ADB0,0x58AE5E,'28361b3a2262eef428437b6a136073b0d38620118aa35cce5c26f45b7c60fa24'),
    (0x58AE60,0x58AF72,'cf0b8a77b5d4c90d35e45b2405dd8feaaa21bfbe97d0ba71b664b8f64bdde73d'),
    (0x58AFF0,0x58B062,'de657674db96e3d3c76c4162143e415707360de0ff295800b39a17695c75f4c7'),
    (0x58B070,0x58B104,'812c0d14cc317fc0f18a6df8571b1408f407349efe2bc2e29b37a5c7f18d0c1c'),
    # Original485020 and47D2B0 call this owner. OverlayFFFFFFFF branches
    # directly to the original -1 return without touching either registry.
    # Nonabsent paths remain bounded by existing input declarations; the
    # unmatched-ore logger4068E0 stays undeclared/fail-closed.
    (0x5FDD20,0x5FDDDE,'edf5348132a35eb58ca33b1d0998e5380047f60139c5f8dca3f62ac8afcb4709'),
    (0x65C6D0,0x65C77A,'60889d008c03c4b02b53ccaa67109bd2997602bdfcaba8e31003ad168bd0df1b'),
    (0x6838C2,0x6838C7,'685d1dc1d4261c409bcea48643b574555b071c73d24ad5cbf99776723f09eda5'),
    (0x6838CD,0x68396D,'ac5fae57f958fa7013ba372029178c0b8d1f5de49041fbf7ac9750f84138d5b9'),
    (0x68A817,0x68AAE6,'6a109967e3b611c332d56ff1c802d863bcde9962ad7a2388dd5a39f32f5c9345'),
)

CELL_PREFIX_DATA = (
    # Actual565090 initializes256 stride16 entries fromMap+164, followed by
    # the retained auxiliary vector115C..1173. Init/normalization/selected
    # Recalc consumers stay inside this same receiver; see the reviewed
    # physical-map-receiver-bounds-handoff static packet. Legacy profiles
    # retain their historical200B fixture extent.
    (0x87F7E8,0x1174),
    (0x40000000,4560*0x200), (0x44480000,838*0x400),
    # Original42A8BF clears three retained tail DWORDsC74/C78/C7C after
    # its three250-DWORD scratch arrays; original42AC00 stays withinC80.
    (0x48000000,1872), (0x87E8B8,0xC80),
    (0x886B88,0x3F4), (0xABE890,0x3F4),
    (0x89A304,32), (0x89C2DC,4), (0x89E720,0xA4),
    (0x89F688,32), (0x89F6D8,64), (0xA8EF54,4),
    (0xA8ED28,24), (0xA8E988,24), (0xA8E9A8,24), (0xABCA10,24),
)
CELL_PREFIX_READ_ONLY = (
    # Native544C09 indexes8288E4 by signedTMP block+29. The authenticated
    # Clear01.TEM block has index13: only its immutable land0 DWORD is read.
    # physical-selected-tmp-land-table-static pins bytes/hash/caller/input;
    # every other index remains undeclared on this selected Tile0 control.
    (0x828918,4),
    (0x8129FC,52), (0x839644,16), (0x839694,16),
    (0x7E4EA8,16), (0x7E3808,8), (0x7E3818,8),
    (0x7E2AC0,8), (0x7E4658,8), (0x7F0E78,4), (0x7ED088,8),
    (0x7E37CC,28), (0x7E3890,28), (0x7E38D0,28),
    (0x7ED404,92), (0x7ED480,28), (0x7ED4A0,28),
    (0x7ED4E0,28), (0x7ED520,28), (0x7ED540,28),
    (0x7EA3E4,28), (0x7ECC48+0x9C,4),
    (0x887308,4), (0xA9FAB4,1), (0xA9FABC,8),
    (0x82BF94,8), (0x82BF88,9), (0x820538,4), (0x82053C,6),
    (0x8207DC,5), (0x81DB84,7), (0x81B0D4,6),
    (0x82BF5C,11), (0x82BF54,7), (0x82BF48,9),
    (0x82BF40,8), (0x82BF34,10), (0x82BF28,9),
)
STEAM_PHYSICAL_CELLS_PROFILE=ExecutionProfile(
    name='steam-15918130-fv-clear-physical-cells-v1',native_sha256=PARENT.native_sha256,
    # Compose the qualified original initializer, not another Scene owner.
    # Identical trusted spans already present (notably Seed) appear once.
    regions=STEAM_PHYSICAL_INPUTS_PROFILE.regions+CELL_PREFIX_REGIONS+
        tuple(r for r in STEAM_SCENARIO_PROFILE.regions
              if r not in STEAM_PHYSICAL_INPUTS_PROFILE.regions+CELL_PREFIX_REGIONS),
    entries=STEAM_PHYSICAL_INPUTS_PROFILE.entries+
        tuple((a,(RET_MAGIC,))for a in (
            0x565090,0x565800,0x47BBF0,0x5447C0,0x65C6D0,
            0x40AFA0,0x49F2F0,0x49F3A0,0x4E6D60,0x4E74E0,
            0x554640,0x4E76E0,0x4E6A60,
            0x47B150,0x47B180,0x47B1A0,0x47B1C0,0x47B1E0,
            0x47B200,0x47B220,0x47B260,0x47B290,0x47B2C0,
            0x47B2F0,0x47B300,0x47B320))+
        ((0x567110,(0x5671E9,)),(0x567230,(0x5672D3,)),
         (0x6838C2,(0x6838C7,)),(0x6838CD,(0x68396D,)),
         (0x68A817,(0x68AAE6,)),(0x6832C0,(RET_MAGIC,))),
    reads=STEAM_PHYSICAL_INPUTS_PROFILE.reads+CELL_PREFIX_DATA+CELL_PREFIX_READ_ONLY+
        tuple(r for r in STEAM_SCENARIO_PROFILE.reads
              if r not in STEAM_PHYSICAL_INPUTS_PROFILE.reads+CELL_PREFIX_DATA+CELL_PREFIX_READ_ONLY),
    writes=STEAM_PHYSICAL_INPUTS_PROFILE.writes+CELL_PREFIX_DATA+
        tuple(r for r in STEAM_SCENARIO_PROFILE.writes
              if r not in STEAM_PHYSICAL_INPUTS_PROFILE.writes+CELL_PREFIX_DATA),
    fixture_writes=STEAM_PHYSICAL_INPUTS_PROFILE.fixture_writes+CELL_PREFIX_DATA+
        tuple(r for r in STEAM_SCENARIO_PROFILE.fixture_writes
              if r not in STEAM_PHYSICAL_INPUTS_PROFILE.fixture_writes+CELL_PREFIX_DATA),
    sinks=STEAM_SCENARIO_PROFILE.sinks,transports=STEAM_SCENARIO_PROFILE.transports,
)

# Original567110 performs Recalc, derives Bridge records by traversing actual
# Cells, then builds connectivity, three hierarchy levels and Pathfinder scratch.
# Reviewed spans come from the existing physical-{cell-graph,clear-leaf,vector-
# leaf,graph-caller,cold-bridge,cell-null-init,map-vector-methods}-* packets and
# physical-nested-edge-grow-static. These are literal code declarations, not
# runtime discovery. Actual final vtables select every +8/+C vector method.
GRAPH_REGIONS = (
    (0x40B070,0x40B113,'bcb6471ead6d1089ea881e3bbbc261420a8c8a9b51d4c1e3389fab23f7ab96a1'),
    (0x40B270,0x40B297,'7d6bb0a4e525b91e86c8598406b230afa8ad5530984ddeff95bec195085140af'),
    (0x429780,0x429827,'a0e65241a71616ac21623bd2f24acc38f41580c3b17429fe7af0c3d2d304fad7'),
    (0x42B1C0,0x42B1E5,'0d84d1af7bf473c2f786d8c76ca20e5887ea63a265891cdc27a214ca43856e7e'),
    (0x42C1C0,0x42C286,'ee99d982ca60360144ea5a09b0cf96a04db0e5e431bc3ad8d412c6844206dfcf'),
    (0x481810,0x481866,'fcf004ddbe8413b19c5521c4bbfaba8db5f93fd0ef177554ddbd71735c173939'),
    (0x484AB0,0x484ADB,'c200bd519e93e48a6b677c2f8ead1951a92d757d5b1f59cef567f1fdf348a511'),
    (0x484F20,0x484F46,'5ae34af99f8d3d9b94bb4454841ac990d2ffdd6a505b1dcb291f8deb46c00950'),
    (0x486750,0x48676F,'4e7dbf9751c9aebfa41e44ce313703a41f663322ee8e201088386ac21d7a8679'),
    (0x486770,0x48678F,'1c866bb549f630f9fcddd75d96a319a76f839359e2b53cd5c83f2e527b9e415f'),
    (0x567110,0x567229,'4e1787963a67bd5911a7cde8c6b0039d538606b04a6a173c3efcbcf3d3aba8fb'),
    (0x56C510,0x56CB7E,'c054495a47994883c2ff7a7f654791fbd205fab54234ecc5cbaf9f49428015cf'),
    (0x56CB90,0x56D0FA,'5597952eb138a262cc5363a0bd2a79395aefa4e4dbcfd2f080e8ca526d3ed99f'),
    (0x56D430,0x56D453,'f9115256dd47c60ab69fc1a1c47d0665a54cd82cfd6765a95c876ffc310682d4'),
    (0x56D6E0,0x56DA04,'12c8a62f1bc0bba36baa4991be9fe2a5f163011ed173a98013f18224782233c1'),
    (0x581F90,0x58249A,'3ba405242cb4d6d49abe70dc2fee3193b39139e58542ab0f6c8645326784c9c4'),
    (0x5824A0,0x582D28,'b2958236db73d943fbf83a4c6c038b4199cbbc78d98375e0b1f7347181d6159c'),
    (0x582D70,0x583174,'2eac9d06dd143cec7abedbd55a3d9469548f321590f98c729ab487b815ffef47'),
    (0x588C90,0x588CBA,'3e41061d15290b17536d5c9976a65c192dfd0a84e058a0fd365eb1523a582095'),
    (0x588CE0,0x588D0A,'7c8ca9f0c1a6e3a7bedff1bafe3797999f4537d1dea66d28554c16f907f15e30'),
    (0x588F00,0x588F2A,'dbc14b417473b2e942424350e97a91ee039019c7431ba11512d6cd0b50bb21be'),
    (0x589100,0x589190,'e204e24fdbbef2a2ee846107e0c4e4612bfd59c1bed2c72074d66908378c8226'),
    (0x589190,0x58928A,'6e9fe4feb187d9ee7f7f0cb762c9a1901999d973089e7a0955dce3847192a58a'),
    (0x589550,0x58967A,'c607e2e4ddc74cb8506379e7d110dd37cec43c69384563eaf5acbee3c9ac51a8'),
    (0x589680,0x58969E,'dd0a091958cccc5dc32e123d58c1c7865bb10f80bc28f0d8e2063e03aaae7ee1'),
    (0x589A60,0x589BC8,'e3a343d9f4f02ba80ae8b01d47da9e72467849c919e4072bc224c5e1ea6aaf66'),
    (0x589BD0,0x589C08,'f0cb33967182f75e3bf4600db9bcba6a4895f544f0fd1823c8f2adcdace13b37'),
    (0x589E20,0x589EA9,'e3c0a0a6d43d8c4c407a7c700a428a213f8bc4c88bb7b122c74acdda56c69a7f'),
    (0x58A030,0x58A0E0,'aca9d9ac7617d0fc71d81b4de4fd218a1d33acc56fdbc9c96271e7eadfa1b61b'),
    (0x58A150,0x58A226,'776584a301a2b793dc0f0cd815963c646b945802aabcc129898d76ddaade3c05'),
    (0x58A2A0,0x58A397,'c18ae2d3a9f8d7ba7ae83227768e11e204e6b4f7b33dea9727e20e5dc660b60f'),
    (0x58A500,0x58A5AD,'92f28199d63755e7d7d738ec5ddb45ece180590e44b1a0f9e9a144874b444e17'),
    (0x58A7B0,0x58A7D7,'ac129d5b58f0c051108ab409cc910185ee341429b4083c00ce7381b2e727cbca'),
    (0x58ABD0,0x58AC69,'a70fc66e7a5061bb5580d61cfa6fca4d0537ae53b686f99d1538f04c7a5b43f7'),
    (0x58AC70,0x58AD03,'985ba4ca6ed3074517c60d298d58ba7e2cd6bb41cc49ec687e73203dd2e851d5'),
    (0x58AF80,0x58AFE1,'2ae5001b588233306c5063b121c70b812017580baa026fb5c986260aff528a5e'),
)
STEAM_PHYSICAL_GRAPHS_PROFILE=ExecutionProfile(
    name='steam-15918130-fv-clear-physical-graphs-v1',native_sha256=PARENT.native_sha256,
    # Replace the paused prefix span/boundary. The full route enters567110
    # once; it never re-enters or overwrites a retained caller frame.
    regions=tuple(r for r in STEAM_PHYSICAL_CELLS_PROFILE.regions if r[0]!=0x567110)+GRAPH_REGIONS,
    entries=tuple(r for r in STEAM_PHYSICAL_CELLS_PROFILE.entries if r[0]!=0x567110)+((0x567110,(RET_MAGIC,)),),
    # Original56C997..56CB01 visits13 rows of8 immutable movement-class
    # DWORDs;56C9E0 reads row[class]. See physical-connectivity-movement-
    # matrix-static. No resulting connectivity IDs or row values are supplied.
    reads=STEAM_PHYSICAL_CELLS_PROFILE.reads+((0x82A594,0x1A0),(0xABDE8C,4),
        (0x7ED4C8,8),(0x7ED588,8),(0x7ED5A8,8)),
    writes=STEAM_PHYSICAL_CELLS_PROFILE.writes+((0xABDE8C,4),),
    fixture_writes=STEAM_PHYSICAL_CELLS_PROFILE.fixture_writes,
    sinks=STEAM_PHYSICAL_CELLS_PROFILE.sinks,transports=STEAM_PHYSICAL_CELLS_PROFILE.transports,
)


# Original selected GameFile/RawFile Win32 read-only route, first theater
# palette/cache producer and cold defaultCell. See physical-tile-palette-
# gamefile-closure-static and physical-dummy-crt-native-boundary-static.
TILE_PALETTE_REGIONS=(
    (0x401940,0x401944,'38058506e8e859d5be73a33baa621352c08ea01f2224ee170173253757193941'),
    (0x40C1B0,0x40C1ED,'94ae6ce9f85fd1036964bbe6c51b5cb5f77b9dc8b958964ebf31239bc42ffe58'),
    (0x40C410,0x40C4C0,'26ada428d47808a491eb6de7fbd61af7fbeb79a7e5e820425f027df35b58672a'),
    (0x431B20,0x431B7F,'c9d9001ecb97e0d6ed397773b9d478a9c4c7d0e0dcacc1fa5c1206db8f22ac71'),
    (0x431E80,0x431F03,'bd84b39be4bee295b92bc2cbb7c1d258b7a9adf92d11c2f7e5bfbef8081423da'),
    (0x431F10,0x431F26,'faa0829e2cfa7306cb5cce41a5597fe3c401bb4270a7a2252ac61fc5cf210888'),
    (0x431F30,0x431F4D,'b8ce3fb5f9368e3e6c04182664c9e5a473c5fbbc97f9701df3952706519e146b'),
    (0x431F70,0x432050,'52d9c4eb5d9fcdf76785d2b7310ce3ad3db2cff366dd5a0b8332e6d56623f6e1'),
    (0x4322A0,0x4324AD,'cfe51ec6540ef350a5b56ee4d79f95d5f13173946d8ac5c64ac36ea68913a694'),
    (0x4325C0,0x43260E,'85fbcc2e6a6e388462d36b19c4b2493aa88bf61aa80fe845f80448c03a13a715'),
    (0x43AD00,0x43AD31,'c9a38aa7ce627ccf66d97e461db61c5c22390f01f7920c1773ec54f93e2aa2d1'),
    (0x4739F0,0x473A2A,'1b1defc95075f6802e9ff31c7f3c00a1c0d760b2e6d2bee5f50e385f188024b0'),
    (0x473B10,0x473B9E,'0f009fae8a21ad4dd37bf89b6758488c87103f916fb4844fb4b6c3cb211a65dc'),
    (0x473C50,0x473CC3,'57cae47ab20f5b9619d85f3a3c5e3522ecdd27e1640fae98e48b6812dd84e493'),
    (0x473CD0,0x473CDF,'e933988f6e71f6ca3e39016b34741d5bdd7fc83ad7ed417bdc96a7d9f2aecedf'),
    (0x473CE0,0x473D03,'21329c7a8cef9bc29dc582b2b61f134767483191562a8345c24f8e148e0d3324'),
    (0x473D10,0x473E4E,'58487aca24b96a95377fea843cb0deb31f988c98c101a1d665ed2a1d1fe25b26'),
    (0x47AA30,0x47AA46,'87472ec0349e29562d13418a0dcd2b0fab6d85aee74340a3b777738cc9dbd8bd'),
    (0x47AAB0,0x47AABD,'a88fc9e952de7dbabec520e20d5f61d40b9e4a169793fa7117eb48e3a8073e92'),
    (0x47AE10,0x47AF04,'9cc67877e17b925242ae8a4422e6fd1c8d57489e3468fa9bd4065f8d112f19a7'),
    (0x545000,0x54514A,'a2d8b37ed9c6fb9aaf05e3323fb90bb4144f0704134bd2a0e749f08becfee641'),
    (0x54547F,0x5454EB,'039c5b848786b7f78fbc5b14523f3238af14e5cf33d00051a9f67e203e355a20'),
    (0x555AC0,0x555B82,'1bbbd7be2894be170ba21a2b3492bbe526d542c061642a2df517d73d1dd9004b'),
    (0x565060,0x565076,'bdf65e0cf5e3e3a7c7be69182e50dd55e330010ae6ea7a928ac739a29fbddbca'),
    (0x578350,0x578383,'8321b1ab359094b71f1a488b2255d94631b927daeb935e35236a3492091176fa'),
    (0x5B4430,0x5B458C,'36634011b3722c2879400f246a525d70234a9f9d85d35e6ff0c2e1bb516aa91a'),
    (0x65CAC0,0x65CB2F,'09ee9e3fd242f5e2c4f4a10230c6af04a07ca12d98ea6982b1013a8462d1ddde'),
    (0x65CB50,0x65CBEB,'3a482b16a52badab162bff0cea670cc1794384e96d3a1a3e640c85999678915b'),
    (0x65CBF0,0x65CC9B,'14cd6fc6385f588fab3fc2bd088cbe90791b4b005a7cbc3c94f73d6ac4988cc4'),
    (0x65CCA0,0x65CCD8,'0050a6a7e39b8b12d614a94a9be0a688a88ce46db0061523776f89b58ef21b90'),
    (0x65CCE0,0x65CDCE,'ea4ac45bcd65e38eb3406160358e01b6170967d2ea04037b4c80e622d6e28d12'),
    (0x65CF00,0x65D0CB,'0cd80195e23024ffa567eee82a39e1796234c8fc25b150aaf86d033477311e94'),
)
TILE_PALETTE_DATA=((0x87F698,24),(0xABBED0,768),(0xB04BEC,1))
TILE_PALETTE_READS=((0x89E410,4),(0xABEFE0,4),(0x7E16B0,68),
    (0x7E1668,68),(0x7E3A2C,68),(0x7E186C,20),(0x8295F4,10),
    (0x7E1BC6,4),(0x813AAC,4),(0x7E11BC,4),(0x7E11E0,4),
    (0x7E111C,4),(0x7E11C0,4))
# Original FF15 sites only. The buffered/limited-file register-indirect seek
# branches remain undeclared; exact read-only CreateFile and one768-byte ReadFile
# are checked by the existing palette owner before a transport supplies bytes.
from tools.native_oracle import ImportTransport
TILE_PALETTE_TRANSPORTS=(
    ImportTransport(0x65CC59,0x7E11BC,28),
    ImportTransport(0x65CC6F,0x7E11E0,4),
    ImportTransport(0x65CBBB,0x7E11BC,28),
    ImportTransport(0x65CCB0,0x7E11E0,4),
    ImportTransport(0x65CD5D,0x7E111C,20,stack_writes=((0x24,4),)),
    ImportTransport(0x65D0A5,0x7E11C0,16),
)
from tools.spatial_oracle.fv_cell_attack.steam_movement_profile import STEAM_TYPED_MASTER_PROFILE
STEAM_JOINED_PHYSICAL_PROFILE=ExecutionProfile(
    name='steam-15918130-fv-retained-typed-physical-v1',native_sha256=PARENT.native_sha256,
    regions=tuple(dict.fromkeys(STEAM_TYPED_MASTER_PROFILE.regions+STEAM_PHYSICAL_GRAPHS_PROFILE.regions+TILE_PALETTE_REGIONS)),
    entries=tuple(dict.fromkeys(STEAM_TYPED_MASTER_PROFILE.entries+STEAM_PHYSICAL_GRAPHS_PROFILE.entries+
        ((0x54547F,(0x5454EB,)),)+tuple((a,(RET_MAGIC,))for a in(0x40C1B0,0x545000,0x565060)))),
    reads=tuple(dict.fromkeys(STEAM_TYPED_MASTER_PROFILE.reads+STEAM_PHYSICAL_GRAPHS_PROFILE.reads+
        TILE_PALETTE_DATA+TILE_PALETTE_READS+((0x24000000,0x2000000),))),
    writes=tuple(dict.fromkeys(STEAM_TYPED_MASTER_PROFILE.writes+STEAM_PHYSICAL_GRAPHS_PROFILE.writes+
        TILE_PALETTE_DATA+((0x24000000,0x2000000),))),
    fixture_writes=tuple(dict.fromkeys(STEAM_TYPED_MASTER_PROFILE.fixture_writes+STEAM_PHYSICAL_GRAPHS_PROFILE.fixture_writes+
        ((0x24000000,0x2000000),))),
    sinks=tuple(dict.fromkeys(STEAM_TYPED_MASTER_PROFILE.sinks+STEAM_PHYSICAL_GRAPHS_PROFILE.sinks)),
    transports=tuple(dict.fromkeys(STEAM_TYPED_MASTER_PROFILE.transports+STEAM_PHYSICAL_GRAPHS_PROFILE.transports+TILE_PALETTE_TRANSPORTS)),
)


def theater_inputs(owner, root, *, filename='TEMPERATMD.INI', suffix='tem', map_file=None, include_properties=False):
    """Extend the existing theater owner on the same Reader VM/allocator."""
    from tools.rules_oracle.theater_general_reader import TheaterReader, general_text
    binding=None
    if map_file is not None:
        from tools.spatial_oracle.anytown_damage.navigation_inputs import Inputs
        binding=Inputs.read_map_theater(owner,map_file)
        binding['filename_suffix']=TheaterReader.scenario_suffix(owner)
        suffix=binding['filename_suffix']['suffix']
    raw=(Path(root)/filename).read_bytes()
    reader=TheaterReader(owner=owner)
    general=reader.read(general_text(raw))
    result=reader.read_sets(raw,suffix=suffix,include_properties=include_properties)
    result.update(general=general,source_file=filename,
                  exclusions=['Physical native INI/archive loader and precedence',
                              'Scenario theater-to-suffix binding',
                              'Full tile construction/TMP/Cell/Recalc/navigation'])
    if binding is not None:
        result['scenario_theater']=binding
        result['exclusions'].remove('Scenario theater-to-suffix binding')
    if include_properties:
        result['property_read_boundary']='Original eleven-key reader frame retained; actual head construction/publication belongs to physical map setup'
    return result


def generate_theater():
    root=Path(os.environ['VERA20K_FV_MOVEMENT_ASSETS'])
    owner,typ,ctor=constructor_inputs(profile=STEAM_PHYSICAL_THEATER_PROFILE,heap_bytes=0x2000000)
    return dict(schema_version=1,constructor=ctor,
                theater=theater_inputs(owner,root),
                retained_type_name=owner.string(typ+0x24),
                retained_scenario_pointer=owner.read32(0xA8B230))


def generate_theater_properties():
    root=Path(os.environ['VERA20K_FV_MOVEMENT_ASSETS'])
    owner,typ,ctor=constructor_inputs(profile=STEAM_PHYSICAL_THEATER_PROPERTIES_PROFILE,heap_bytes=0x2000000)
    return dict(schema_version=1,constructor=ctor,
                theater=theater_inputs(owner,root,map_file=root/'dragon-cadence.map',include_properties=True),
                retained_type_name=owner.string(typ+0x24),
                retained_scenario_pointer=owner.read32(0xA8B230))


def physical_inputs(*,map_file=None,profile=None,scenario_bytes=0x1300,native_scenario=False,native_state=None):
    """Read physical inputs on the existing constructor or typed-startup VM.

    native_state is the startup owner's (VM, selected FV, Rules, receipt).
    Adoption never reruns constructors, cold registries or a native ID/RNG
    reset. Its retained Tiberium vector must already exist: original668F65
    calls721D10 late in Rules Process, not in the typed master prefix. The
    caller retains that producer evidence; observing a vector is not proof
    of the complete Process/launch. Fresh historical defaults are unchanged.
    """
    from tools.spatial_oracle.anytown_damage.navigation_inputs import Inputs
    root=Path(os.environ['VERA20K_FV_MOVEMENT_ASSETS'])
    map_file=Path(map_file) if map_file is not None else root/'dragon-cadence.map'
    adopted=native_state is not None
    if not adopted:
        owner,typ,ctor=constructor_inputs(profile=STEAM_PHYSICAL_INPUTS_PROFILE if profile is None else profile,
            heap_bytes=0x2000000,scenario_bytes=scenario_bytes,native_scenario=native_scenario,
            initial_counter=None if native_scenario else 31)
        rules=None
    else:
        if profile is not None:raise ValueError('Retained physical owner cannot replace its execution profile')
        owner,typ,rules,receipt=native_state
        if owner.image is None or owner.image.profile.native_sha256!=PARENT.native_sha256:
            raise ValueError('Retained physical inputs require the authenticated Steam VM')
        if not typ or owner.string(typ+0x24)!='FV' or owner.read32(0x8871E0)!=rules or not rules:
            raise ValueError('Retained physical inputs require the original selected FV and Rules receiver')
        if not owner.read32(0x887308):raise ValueError('Retained physical inputs require the original nonNULL Surface')
        if owner.heap_end!=0x26000000:
            raise ValueError('Create the joined VM with the reviewed32MiB allocator; never replace or copy its heap')
        if not owner.read32(0xB0F4E8) or owner.read32(0xB0F4F8)!=4:
            raise ValueError('Original four Tiberium types must precede physical adoption; no late host construction')
        ctor=receipt['setup']
        scenario=owner.read32(0xA8B230)
        allocation=ctor['scenario_allocation']
        if allocation['pointer']!=scenario or allocation['bytes']!=NATIVE_SCENARIO_BYTES:
            raise ValueError('Retained physical inputs require their original full Scenario allocation')
        registries=(0xA83D80,0xA8E318,0x8B4150,0xB0F4E8)
        before_headers={a:bytes(owner.u.mem_read(a,24))for a in registries}
        rngs={'main':0x886B88,'scenario':scenario+0x218,'mapgen':0xABE890}
        before_rng={name:bytes(owner.u.mem_read(a,0x3F4))for name,a in rngs.items()}
        before_counter=owner.read32(scenario+0x214);before_cursor=owner.cursor
        surface=owner.read32(0x887308)
    t=theater_inputs(owner,root,map_file=map_file,include_properties=True)
    inputs=Inputs.on_existing_owner(owner,t,map_file=map_file,root=root,
        rules_pointer=rules,retained_type_registries=adopted)
    if adopted:
        assert owner.read32(0x8871E0)==rules and owner.read32(0xA8B230)==scenario
        assert owner.read32(0x887308)==surface and owner.read32(scenario+0x214)==before_counter
        assert owner.cursor>=before_cursor
        assert all(bytes(owner.u.mem_read(a,24))==before_headers[a]for a in registries)
        assert all(bytes(owner.u.mem_read(a,0x3F4))==before_rng[name]for name,a in rngs.items())
        inputs.retained_startup=receipt
        inputs.retained_physical_adoption=dict(rules=rules,selected_fv=typ,scenario=scenario,surface=surface,
            allocator_before=before_cursor,allocator_after=owner.cursor,allocator_end=owner.heap_end,
            scenario_counter=before_counter,registry_headers={hex(a):v.hex()for a,v in before_headers.items()},
            rng_before={name:v.hex()for name,v in before_rng.items()},
            rng_after={name:bytes(owner.u.mem_read(a,0x3F4)).hex()for name,a in rngs.items()},
            boundary='Existing selected physical field readers execute; caller startup receipt is retained, full Rules Process/launch not claimed.')
    return owner,typ,ctor,t,inputs


def generate_physical_inputs():
    owner,typ,ctor,t,inputs=physical_inputs()
    return dict(schema_version=1,constructor=ctor,theater=t,
                physical_inputs=inputs.snapshot(),
                retained_type_name=owner.string(typ+0x24),
                retained_scenario_pointer=owner.read32(0xA8B230),
                overlay_registry_count=owner.read32(0xA83D90),
                tiberium_registry_count=owner.read32(0xB0F4F8),
                original_object_type_registry_count=owner.read32(0xB0F680))


def physical_cells(*,map_file,rng_seed=0,build_graphs=False,native_state=None):
    """Run the existing native physical owner on explicitly selected clear bytes."""
    from tools.spatial_oracle.anytown_damage.navigation import Navigation
    from tools.spatial_oracle.anytown_damage.navigation_inputs import map_inputs,sha
    from tools.spatial_oracle.bridge_rim import GLOBALS
    adopted=native_state is not None
    if adopted and rng_seed is not None:
        raise ValueError('Retained physical map requires rng_seed=None to preserve all three original streams')
    if adopted:
        cold=getattr(native_state[0],'physical_dummy_startup',None)
        if not cold or not(cold['executed']and cold['entry']==0x565060
                and cold['native_id']==0 and cold['native_id_offset']==0x10
                and cold['unpublished_scenario']):
            raise ValueError('Retained physical map requires its executed original pre-Scenario default Cell')
    profile=None if adopted else(STEAM_PHYSICAL_GRAPHS_PROFILE if build_graphs else STEAM_PHYSICAL_CELLS_PROFILE)
    owner,typ,ctor,t,inputs=physical_inputs(map_file=map_file,profile=profile,
        scenario_bytes=NATIVE_SCENARIO_BYTES,native_scenario=True,native_state=native_state)
    # Original startup52BA78 allocates0x3740 before6832C0. The historical
    # constructor-only buffer0x1300 does not own Lighting/Dropship fields and
    # cannot be used for this physical path. Extent is independent of the
    # executed initialization receipt recorded by the constructor.
    allocation=ctor['scenario_allocation']
    scenario=owner.read32(0xA8B230)
    assert allocation['pointer']==scenario and allocation['bytes']==NATIVE_SCENARIO_BYTES
    assert allocation['end']==scenario+NATIVE_SCENARIO_BYTES and typ>=allocation['end']
    assert scenario+0x355C+4<=allocation['end']
    initialization=ctor['scenario_initialization']
    # Original SceneCtor seeded its stream before FV/type construction. Keep
    # that state; Main/MapGen remain separately declared isolated Seed inputs.
    seeds=dict(main=None,scenario=None,mapgen=None) if adopted else dict(main=rng_seed,scenario=None,mapgen=rng_seed)
    raw,sections,cells=map_inputs(map_file)
    assert len(cells)==4560 and t['count']==838
    assert all(v['tile']==0 and v['subtile']==0 and v['level']==0 and
               v['ice']==0 and v['overlay'] is None and v['frame']==0 for v in cells.values())
    assert not sections.get('Terrain') and not sections.get('Structures')
    fields={k:v for k,v,line in sections['Map']}
    size=[int(v)for v in fields['Size'].split(',')[2:]]
    assert size==[48,48]
    case=dict(size=size,local_size=[int(v)for v in fields['LocalSize'].split(',')],
              bridge_base=t['globals'][0xAA0E28],wood_base=t['globals'][0xABAD1C],
              rim_keys={k:t['globals'][a]for k,a in GLOBALS.items()},
              map_sha256=sha(raw))
    # Native Scenario-to-filename selection was independently executed above.
    # This bounded host file binding supplies the original TMP byte layout;
    # original Tile getters/Recalc execute, archive precedence remains excluded.
    assert t['tiles'][0].upper()=='CLEAR01.TEM'
    tmp=Path(os.environ['VERA20K_FV_MOVEMENT_ASSETS'])/'Clear01.tem'
    blob=tmp.read_bytes()
    assert len(blob)==1872 and sha(blob)=='d90df76d78fd9a3e23834c5a728cef666dbdf65b212dd3a66c29b456cbd51ed2'
    surface=owner.read32(0x887308)
    assert (surface!=0) if adopted else(surface==0)  # retained or isolated presentation boundary
    native=Navigation.on_physical_map(owner,t,{0:blob},case=case,map_file=map_file,
             inputs=inputs,scenario_theater=t['scenario_theater'],
             cell_inputs_only=not build_graphs,rng_seed=seeds,scenario_initialization=initialization,
             # Ninth60s run reached physical slot2735/4560 during actual
             # lighting/Recalc (return568CBE). The full selected pass plus
             # graphs needs a bounded longer call, without skipping work.
             full_graph_timeout_us=300000000 if build_graphs else 60000000)
    assert owner.read32(0x887308)==surface
    return owner,typ,ctor,t,inputs,native,dict(filename=t['tiles'][0],bytes=len(blob),sha256=sha(blob))


def generate_physical_cells(*,map_file,build_graphs=False,native_state=None):
    adopted=native_state is not None
    owner,typ,ctor,t,inputs,native,tmp=physical_cells(map_file=map_file,build_graphs=build_graphs,
        native_state=native_state,rng_seed=None if adopted else 0)
    assert native.used_tile_heads=={0}
    assert(owner.read32(0x887308)!=0)if adopted else(owner.read32(0x887308)==0)
    result=dict(schema_version=1,constructor=ctor,theater=t,physical_inputs=inputs.snapshot(),
                map_file=str(Path(map_file).resolve()),map_sha256=native.case['map_sha256'],
                normalization=native.normalization,
                construction_history=native.construction_history,
                primary_tmp=tmp,cell_startup=native.cell_startup,
                native_cells=native.initial_cells,scenario_lighting=native.scenario_lighting,
                cell_inputs_rng=native.cell_inputs_rng,
                native_reached=dict(native.counters),reached_primary_tmp_heads=sorted(native.used_tile_heads),
                native_map_vtable=owner.read32(0x87F7E8),
                native_cell_table_pointer=owner.read32(0x87F7E8+0x13C),
                native_isotile_count=owner.read32(0xA8ED38),
                original_object_type_registry_count=owner.read32(0xB0F680),
                retained_type_name=owner.string(typ+0x24),
                retained_scenario_pointer=owner.read32(0xA8B230),
                final_tiberium_value=native.final_tiberium_value,
                exclusions=['Full native scenario/file/archive loader chronology',
                            'Palette initialization/rendering: original544E70 takes the declared NULL presentation branch',
                            'Connectivity/hierarchy suffix after5671E9 and Unit construction/admission'])
    if adopted:
        result.update(retained_startup=inputs.retained_startup,
            retained_physical_adoption=inputs.retained_physical_adoption,
            cold_default_cell=owner.physical_dummy_startup,
            tile_palette_initialization=owner.tile_palette_initialization)
        result['exclusions'][1]='Authenticated virtual loose-file palette service; archive precedence and rendered/device parity excluded'
    if build_graphs:
        # observe_physical uses the original address formatted as :08X.
        assert native.counters['native_graph_construction:00567110']==1
        assert native.counters['native_graph_construction:0056D6E0']==1
        assert native.counters['native_graph_construction:0056C510']==1
        assert native.counters['native_graph_construction:00581F90']==3
        assert native.counters['native_graph_construction:0042C1C0']==1
        result.update(bridge_record_production=native.bridge_record_production,
                      navigation=native.nav_snapshot(),graphs=native.graph_snapshot(),
                      dummy=native.dummy_snapshot())
        result['exclusions'][-1]='Unit construction/admission and live world lifecycle'
    return result


def physical_cells_metadata(*,build_graphs=False):
    from unicorn import Uc,UC_ARCH_X86,UC_MODE_32
    profile=STEAM_PHYSICAL_GRAPHS_PROFILE if build_graphs else STEAM_PHYSICAL_CELLS_PROFILE
    image=load_image(Uc(UC_ARCH_X86,UC_MODE_32),profile=profile)
    return provenance(image=image,scope='Original physical clear-map Cell/TMP/Recalc producer on one retained FV type VM',
        assumptions=['Explicitly selected authored48x48 clear map supplies4560 Tile0/subtile0/height0/overlayFF records; native constructors derive Cell state.',
                     'Original Map constructor/Init allocate the genuine Cell pointer table and typed graph headers on the same32MiB allocator.',
                     'All838 actual IsoTile heads retain original ordinal/name constructors and property publication; only reached native Clear01.TEM payload is bound.',
                     'Original6832C0 Scenario constructor/full selected683610 Reset execute before A8B230 publication and isolated namedFV type; actual0x3740 allocation remains disjoint from subsequent types/inputs.',
                     'Original13 Cell CRT initializers, Pathfinder cold constructor and neighbor/direction tables precede Cells; Main/MapGen receive explicit original Seed0 controls while Scenario retains its constructor-seeded state.',
                     'The executed Scenario Reset supplies Lighting defaults; all twelve original map Lighting reads precede483E30/484180 gathering/finalization without repeating defaults or resetting retained state.',
                     ('Original567110 executes once: allocates class/height planes, runs568BB0/Recalc, derives Bridge records through56D6E0, builds56C510 connectivity and581F90 levels2/1/0, then42C1C0 scratch; no copied graph IDs/edges or supplied empty Bridge result.' if build_graphs else
                      'Original567110 prefix allocates class/height planes and executes568BB0/Recalc; connectivity/hierarchy suffix remains unexecuted.'),
                     ('Selected full567110 call has300s timeout and unchanged180M instruction cap; other shared calls/legacy defaults remain60s.' if build_graphs else
                      'Selected prefix call retains60s timeout and80M instruction cap.')],
        substitutions=['Host lexical INI cache, authored Map membership and existing physical TMP pointer relocation are declared file-binding boundaries.',
                       'Fresh aligned zero-filled Scenario allocation, observed incoming stack, zero-BSS mode0/frame and empty runtime strings remain explicit inputs; native6832C0/683610 derives state. Mode5 localization/nonzero incoming slot callbacks and whole startup/type-prefix/load chronology remain excluded.',
                       'Existing ThrottleServices supplies six DWORD zero inputs to WINMM timeGetTime; original6C8C40 SHR4 executes. Non-EAX register preservation and incoming stack are declared ABI inputs, so observed Reset timer words are not universal native constants or Windows clock parity.',
                       'The selected map has no StartingDropships key, original Reset stores count0, and a retained read-only guard rejects every reached Dropship timer consumer. Timer bytes are native-initialized and preserved; Dropship startup/timer lifecycle is excluded. Any authored key or reached timer read reopens this prerequisite.',
                       'Presentation palette system is uninitialized: original544E70 returnsNULL for every Cell lighting refresh. Scalar lighting executes; palette creation/rendering are excluded. Navigation land/class/height consumers do not read Cell+34 palette pointer on this selected path; revisit on any joined Unit palette consumer.',
                       'Selected empty world has no active superweapon lighting effects; no full controller or live scenario lifecycle is claimed.',
                       'Checked CRT heap/exit-registration transports are inherited from the constructor owner; no gameplay return or Recalc result is substituted.'],
        entry_points={'map_constructor':0x565090,'map_init':0x565800,'cell_ctor':0x47BBF0,
                      'tile_ctor':0x5447C0,'tmp_getter':0x544CB0,'recalc':0x47D2B0,
                      'scenario_constructor':0x6832C0,'scenario_reset':0x683610,'lighting_read':0x68A817,
                      'cell_lighting':0x483E30,'final_init':0x567110})


def physical_inputs_metadata():
    from unicorn import Uc,UC_ARCH_X86,UC_MODE_32
    image=load_image(Uc(UC_ARCH_X86,UC_MODE_32),profile=STEAM_PHYSICAL_INPUTS_PROFILE)
    return provenance(image=image,scope='Selected original physical Overlay/Tiberium/land inputs on the retained FV type VM',
        assumptions=['One existing Reader VM and one32MiB guest allocator retain the actual FV type and Scenario.',
                     'Actual Overlay250 named constructors and Tiberium4 named constructors append to original cold typed registries.',
                     'The single physical layered pass executes original selected Overlay Cell-key seams including Tiberium Armor/Land post-read.',
                     'Original Tiberium Value/Image reads and six-way switch retain actual registered Overlay pointers; original land speed/default/clamp/store code executes.',
                     'Selected authored maps have no Terrain records; unused71D580 occupation templates remain uninitialized and outside declared data access.',
                     'Map bytes supply authored membership/tile/overlay coordinates; original Cell/TMP/Recalc/connectivity/hierarchy are not executed by this input milestone.'],
        substitutions=['Existing checked CRT allocation/exit-registration and exact physical lexical INI-cache boundaries.',
                       'Full Rules/ObjectType image/ART/archive loading and actual native scenario/file load chronology remain outside the selected inputs.',
                       'Only map-used tile animation keys are examined; unused physical tile ordinal heads remain an explicit later construction obligation.'],
        entry_points={'overlay_names':0x668CE3,'overlay_constructor':0x5FE250,
                      'overlay_cell_keys':0x5FE798,'overlay_tiberium_post':0x5FE8C9,
                      'tiberium_constructor':0x7216C0,'tiberium_image':0x721C3F,
                      'land':0x674000})


def theater_properties_metadata():
    from unicorn import Uc,UC_ARCH_X86,UC_MODE_32
    image=load_image(Uc(UC_ARCH_X86,UC_MODE_32),profile=STEAM_PHYSICAL_THEATER_PROPERTIES_PROFILE)
    return provenance(image=image,scope='Original Scenario theater lookup/suffix pointer and physical TileSet property reader seams on the retained FV VM',
        assumptions=['Original constructor/type/CRT inputs precede the selected authored Map/Theater read in one checked VM.',
                     'Original Map/Theater parser/lookup and original Init_Theater index/pointer stores determine the filename suffix.',
                     'Original eleven TileSet key reads retain their unchanged output frame; shadow publication starts with explicit outer caller count0.',
                     'Original ordinal/cumulative-base seams are explicit inputs; no full native scenario/file loader chronology is claimed.'],
        substitutions=['Existing bounded heap/CRT/ASCII GUID setup boundaries inherited from the type owner.',
                       'Physical INI lookup indexes are supplied by the existing owner; archive/render I/O is excluded.'],
        entry_points={'map_theater':0x687631,'theater_lookup':0x48DBE0,'suffix_index':0x5349D7,
                      'suffix_pointer':0x534A05,'properties':0x5460EA,'head_property_store':0x54641F})


def theater_metadata():
    from unicorn import Uc,UC_ARCH_X86,UC_MODE_32
    image=load_image(Uc(UC_ARCH_X86,UC_MODE_32),profile=STEAM_PHYSICAL_THEATER_PROFILE)
    return provenance(image=image,scope='Selected original physical theater scalar/count/name seams on the existing FV type VM',
        assumptions=['Original FV type/CRT precedes this isolated theater input; no Unit instance is constructed.',
                     'Physical exact-case records prepare native sorted lookup indexes; original readers/sprintf execute.',
                     'Ordinal and cumulative base are explicit caller seams; no full native theater/scenario loader claim.'],
        substitutions=['Existing bounded heap/CRT/ASCII GUID setup boundaries inherited from the type owner.',
                       'The temperate suffix is supplied; native Scenario-to-filename suffix selection remains open.'],
        entry_points={'general':0x545535,'ordinal':0x545CEF,'count':0x545FA3,'names':0x54609C,'filename':0x5462B3})


if __name__=='__main__':
    import sys
    if '--physical-cells-only' in sys.argv or '--physical-graphs-only' in sys.argv:
        build_graphs='--physical-graphs-only' in sys.argv
        sys.argv.remove('--physical-graphs-only' if build_graphs else '--physical-cells-only')
        if '--map-file' not in sys.argv:raise SystemExit('Physical Cells require an explicit --map-file')
        index=sys.argv.index('--map-file')
        if index+1>=len(sys.argv):raise SystemExit('--map-file requires a path')
        selected_map=Path(sys.argv[index+1]);del sys.argv[index:index+2]
        name='steam_physical_graphs.json' if build_graphs else 'steam_physical_cells.json'
        finish_vectors(lambda:generate_physical_cells(map_file=selected_map,build_graphs=build_graphs),
                       Path(__file__).with_name(name),
                       provenance=lambda:physical_cells_metadata(build_graphs=build_graphs))
    elif '--physical-inputs-only' in sys.argv:
        sys.argv.remove('--physical-inputs-only')
        finish_vectors(generate_physical_inputs,Path(__file__).with_name('steam_physical_inputs.json'),provenance=physical_inputs_metadata)
    elif '--properties-only' in sys.argv:
        sys.argv.remove('--properties-only')
        finish_vectors(generate_theater_properties,Path(__file__).with_name('steam_physical_theater_properties.json'),provenance=theater_properties_metadata)
    else:
        finish_vectors(generate_theater,Path(__file__).with_name('steam_physical_theater.json'),provenance=theater_metadata)
