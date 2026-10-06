"""Literal original Steam live type reader enrollment.

Native SHA256: 3e81a61775d2745d1dabe397325ef663cd994ffc194da4e998e3bf5d2d308600.
This module is declarative only: no discovery, execution, fixture mutation,
file transport or profile creation. Original helper scopes remain inherited.
Asset/service leaves have a separate owner; undeclared transfers fail closed.
See steam_live_types_scope.md for receiver review and qualification limits.
"""

LIVE_REGIONS = (
    # Original Process caller, stop before difficulty readers.
    (0x668EED, 0x668EF5, "e53c06c2987864bbd074305c5e4f42472841d7db14384c4f1a3f6d73d8bbf84e"),
    # Original live loop, counts reread within each active family.
    (0x679A10, 0x679CB7, "602648590ed85cd363f8ac604d5f75b49fbc4f0d09de12c12627e0a4b1bff9ab"),
    # Abstract Name/UIName, inherited incoming INI.
    (0x410A60, 0x410B8B, "302413ea9928adf0e7e11198ea9b7e8155af973b809a60743a3c3dd1144bbaaf"),
    # Object incoming INI Image then global ART.
    (0x5F92D0, 0x5F96AA, "0e03c5a69e81efb82686a57a1087cb7aef51d862cd53ed7e2e84bfd9dc14ea8c"),
    # Techno gameplay Rules and visual global ART.
    (0x712170, 0x716141, "d36fd601a401741ee981a29eac09fa14923f47967de7c3453134a6933348a6b4"),
    # Bullet find-or-create, original constructor allocation2F8.
    (0x46C790, 0x46C813, "f8dc6166a3c069733bf55ad84fc9fd67d58f53ec7c6836e815170836e1815bf8"),
    # Bullet primary constructor and registry insertion.
    (0x46BBC0, 0x46BDDE, "d282ea75362a7f10ea24dcd932b92c4732f3bb25b909d5b2aa2a8ceb31730fdd"),
    # Weapon postpass.
    (0x7729F0, 0x772A4D, "62546dd784a0da0f16a576d392ace01674f29c7cbbdd4a74d2a7d79d4e104760"),
    # Building original RET postpass.
    (0x465CB0, 0x465CB1, "ae3f4619b0413d70d3004b9131c3752153074e45725be13b9a148978895e359e"),
    # MissionControl original indexed reader.
    (0x5B3760, 0x5B390C, "7bf7c3e75182871be6ff9d47096b4d8f2895311cfc92cc12c5e22d8a94793496"),
    # Weapon postpass original Rules scalar.
    (0x48AB90, 0x48ABB9, "a14a78c4178a85ba198aec0a7565c2594d8e69fd9b7d2dcdcf02d945551ded52"),
    # Weapon postpass original FPU multiply.
    (0x48ACF0, 0x48AD02, "580d05f16cd907eb01f3e759a28a6d5538ef39a977d7070c2df17c885e10e931"),
    # Country original concrete primary +64 reader.
    (0x511850, 0x512165, "07e86e289f87ac364efa37913905da93e9704944f5682f6bb62d8e48a9a8afc8"),
    # SuperWeapon original concrete primary +64 reader.
    (0x6CEA20, 0x6CEE5D, "2208040e5017bf63f2a83062894ab2d1d53dadbaf344803551f64ded3971c2e3"),
    # Anim original concrete primary +64 reader.
    (0x427D00, 0x4287F6, "be7c6ebc541ac8cffd92337a610dd6ebd281770ef3b250d8744097bf9b25c71d"),
    # Building original concrete primary +64 reader.
    (0x45FE50, 0x464A63, "5388a9be97085cd1b22413d3bf0c7576699523f02ae1fb42a4761edb2f9d1504"),
    # Aircraft original concrete primary +64 reader.
    (0x41CC20, 0x41CDA4, "d48e74b0c45ad0f5a0513262b0ddaa8b491aece11bb3c2513255da9339dfac4e"),
    # Unit original concrete primary +64 reader.
    (0x747620, 0x747EAC, "8ca2bf5a74eff90995e635834a6f5a22ea50359b36873fa82e2f4579131c05ab"),
    # Infantry original concrete primary +64 reader.
    (0x5240A0, 0x52475D, "2550e53107e69aef4523b16f12af93a2d41a750b3ad822391b256ebe2416eea3"),
    # Weapon original concrete primary +64 reader.
    (0x772080, 0x7729E5, "6d56033c1ed4af71b2afcc3dd3f8cfae7aade05bfd976b1b9a490c9bd31fc17b"),
    # Bullet original concrete primary +64 reader.
    (0x46BEE0, 0x46C436, "25e95a2465754739c403511705e6a2e07d4aadbf700882a33c86a3f5de68bae4"),
    # Warhead original concrete primary +64 reader.
    (0x75D3A0, 0x75DEBE, "951e720f8b8dbcac4bfb95d4a2a81f7a9124d2ced148dfb61115ded68ae54c23"),
    # Terrain original concrete primary +64 reader.
    (0x71DEA0, 0x71E0C1, "64cd01f3da70006f2d5b428133cd9c61c6f499b33efe3a2a949ede927c11bee5"),
    # Smudge original concrete primary +64 reader.
    (0x6B56D0, 0x6B57E7, "a5785429a45e6a1a7f0253b385a5b35a1222bb509ae0d332ff34bf8693bef541"),
    # Overlay original concrete primary +64 reader.
    (0x5FE770, 0x5FEA2B, "236b449291a80c05c4b484e3b2142c58615e8a3f913d53cb2fe1d0a0d9d9663d"),
    # Particle original concrete primary +64 reader.
    (0x644F50, 0x645423, "c9be91a92641d78b344fda0f8bf7837afbc5e39392f42ecd1ea53c33fdc08218"),
    # ParticleSystem original concrete primary +64 reader.
    (0x6442D0, 0x64462B, "c8282738b2b00dc7cf63940825f90158ae5d00ea1f0759365abed397c504e4af"),
    # VoxelAnim original concrete primary +64 reader.
    (0x74B050, 0x74B61D, "a01c00083385027fe2601dc98ed99a72347188c66111a1fa6b2f2583488e819f"),
    # Speed clamped0..100 to native integer scale.
    (0x474810, 0x474866, "fe814b0a3a18fb0d4837bb54dac07a04a38eb235cddea12071bcd26586b5e487"),
    # Pip original eleven name/value records, including person colors.
    (0x4748A0, 0x47490A, "c8d4d08a963409378064862b075b3c65c9a6ab5e2c12006c7dc535ac2df04986"),
    # PipScale original five name/value records.
    (0x474940, 0x4749B0, "32450762b7c4ad74cca7cedc43d19acef656e5dc9fc9c7cf53792bd8a148554e"),
    # Category original name lookup.
    (0x4749E0, 0x474A18, "8a692730dc65a4f1f1220e81ae5a7efc399eae3a4294f78b8ec8db0bc9fd0597"),
    # Foundation original22 name/value records.
    (0x474DA0, 0x474E07, "854d6ddef79dc71b1d118d8dadaf6ccbc3f1302312c01f49cad9f995b0a6943b"),
    # Action original73 name slots, read by SuperWeapon.
    (0x474EE0, 0x474F42, "fa48f761cdb9a319a3d09adefde962dfef93cff2bde760b07c48da44c351e208"),
    # SuperWeapon index name and existing lookup.
    (0x474F50, 0x474F99, "0a995d4c078d52bc6692ae6366ec6d69273adc66d1ecffe00aaee0c4b97dd2ce"),
    # EVA name lookup used by original Building CaptureEvaEvent.
    (0x474FA0, 0x474FE9, "5d3f9db53b578569e1f18ca8977f8636da1de914aadc3ebea1c22f311a844213"),
    # AI trigger condition name lookup.
    (0x474FF0, 0x475028, "677db1e8b38fef59b7fcfa75b15aeb555096caaed305448491be9b515dda2adf"),
    # Building name lookup.
    (0x475060, 0x475098, "5e116a3d245fbf73b0a008fa5e67a55505c03acef2fa5a6b0231336f77853584"),
    # House bitset native token order.
    (0x4750D0, 0x475143, "380881a230e1c557543c288e79fa79c1df7abdb27e92d4ae3233b458ecfb1bf2"),
    # Armor ReadString wrapper with original default-name lookup.
    (0x4753F0, 0x475433, "8455e66cab0f152ebbca5889fc6b97f9dbaf05db0d560c5e09c99cb5627b129a"),
    # Script type native lookup.
    (0x4756F0, 0x475792, "476867c7537874c99acdf9b70a90090f7155a3b466975414c4e507eb7429978b"),
    # Three integer tuple.
    (0x476340, 0x47641E, "5242cf1c1245dab3dcc78fdbfb53505e3d7803bec850d8e07907fc694a12332c"),
    # Three binary64 tuple.
    (0x476420, 0x4764EE, "58314f2ab67ae85add039c4e5b22dc6f6c4b520a13acc9bd8a5d07e4fd082f92"),
    # Color tuple vector.
    (0x476B20, 0x476D76, "ffafd9eb9a2d5d1e80642fdfbcb08215fad9881d27d673ac75c36417aff7bd18"),
    # Techno type resolver existing four factories.
    (0x476EB0, 0x476F6A, "c4159da3b3b35a8a5cb88c80639a3d26c4642f4ffddaa9247b0ed9b6aa52abf5"),
    # Layer original ReadString wrapper and enum parser.
    (0x477050, 0x4770AF, "bc3a9685cb3bd36a56d5a8fd633133180beb72dd8141bddd4f278c720e56b3f4"),
    # Target restriction three-name enum.
    (0x477590, 0x47763A, "cb7b730774ae026bd00193daeff3c357955df5ff84a4519c1fdb49aa6699534e"),
    # Warhead affect-type native18 flags.
    (0x477640, 0x477735, "76e76c1c6fd694e70414ae0b4f6ec34e5fcaab2ed7771088ed7041ecfa7a22ce"),
    # Temporary color vector clear.
    (0x478440, 0x478467, "d41af57306c23f30ca8bbeb23df9bceb0fd8237cf4551821e8ec9df9c4376111"),
    # Temporary color vector copy.
    (0x4788E0, 0x478983, "0293280d75460d0025ca4d3d33e35e1a53eacdedee7c59e65b8825148aa6d4a0"),
    # Country Infantry temporary vector constructor.
    (0x512DC0, 0x512E1D, "266b125c5093e8259e1f1a5a72bbd2784e5993130ae919c0498cfb78ce9356c8"),
    # Country Infantry vector push.
    (0x512F20, 0x512F70, "30af68b9c6a673326067624c6aebf06e6d7145fa754b7738b9265393be87482f"),
    # Country Aircraft temporary vector constructor.
    (0x513560, 0x5135BD, "3f41068d7c0b2fe075250d5ea302c5f739d078c6dc611fdc23a9eb7a1c9b9d20"),
    # Country Aircraft temporary vector copy.
    (0x5137D0, 0x513858, "fe73f2bc68e87c680963ec99981962473711c5cc0db27bec176823bf9961c742"),
    # Country Infantry temporary vector copy.
    (0x513860, 0x5138E8, "d7d683bdf982c790d5aeb07ac4a98674a539854c05e19d2a9dc73fc66514a347"),
    # Infantry sound vector copy.
    (0x524F20, 0x524FA4, "1fab88a9686104283be696e22333301c6f97a536c5364d67ee9d3b02311303c5"),
    # Sound list original token loop.
    (0x525430, 0x5255E7, "827a2e0fbb1e9d9d432eda90520200c77ffdc1b2f96c4fa8850125af7e599223"),
    # Point2D reader used by Anim/Building.
    (0x529880, 0x529A25, "e39594e9470481de5b95b823a8f51d020a0dc6d1ffe257c8f018eacd71e56304"),
    # Point3D reader used by Techno/Unit/Building.
    (0x529CA0, 0x529E66, "451bebd4f8827d5a67bb556ab7154a2adc35ac40e27053b6d707258adea758b7"),
    # Particle find-or-create.
    (0x645430, 0x6454BF, "eba07dce5afa4a279637e090be15fea3f867540381bc2e0f4a35a5e9b4635e80"),
    # ParticleSystem find-or-create.
    (0x644630, 0x6446D1, "dead128f5e6a7eb7b4498eb32cadcdab002e83c3a2b9bd87fc7cd7edc782bed3"),
    # Color derived vector constructor.
    (0x645A70, 0x645B04, "b0eb53ee5627393f615bdcf9745c8ee8ce54a9e81e175f5db82d517ecb282c33"),
    # VoxelAnim find-or-create.
    (0x74BB20, 0x74BBA0, "6c0e504cf55b872b5e926396f0914c276458eed618f3ff66e8d99c221b906d98"),
    # Warhead VoxelAnim vector copy.
    (0x75E6B0, 0x75E738, "6a58d3ef9990182ef229b79f52c53a1aefe106a4e0843eade81ede9a23c618ac"),
    # Techno temporary vector clear.
    (0x45A270, 0x45A297, "3978798d7bd42b3a2366ddc49fe9a7f26247e0d926cf73c6c3462bd7e94661db"),
    # Building find-or-create.
    (0x466000, 0x466080, "958b955d323b9a3e13eb3d1abfff7fff4fcd803bbe22bae8b93c929dedf56c16"),
    # Anim find-or-create.
    (0x428F70, 0x428FF0, "35ea2ab4da4d1ef60985c757f11c05ba3d2e25a316f979898c7e89e2f428da5e"),
    # AI trigger enum formatter.
    (0x40DCB0, 0x40DCD4, "d5fb11f66187527728fd823638a4744d9319850da8dd8bb143c04a83f3387afa"),
    # AI trigger enum parser.
    (0x40DCE0, 0x40DD19, "a4528583a5800b5acfc266ca8c0520d9170ef9f25d660894a0b1e37b179f03c4"),
    # Aircraft name find existing registry.
    (0x41CAA0, 0x41CAE1, "fb46943f493298276b90a5fe3cde04d62f1ee35eba1d5fb538b8338b7f74ca9f"),
    # Building enum formatter.
    (0x45DD20, 0x45DD44, "62a850a2c2ad1129ba2aaf10514acab6e62635f62ca60d6dd1533443ff3b1b62"),
    # Building enum parser.
    (0x45DD50, 0x45DD89, "36b54cd3072daec80d4feb743e39bbc69ad4b0f9543defc97f1145173aac659b"),
    # Category enum formatter.
    (0x473960, 0x473973, "da075a82376572b5345f7d79110503ead2f28c07ae4fac2bbde702edbd1eb9af"),
    # Category enum aliases parser.
    (0x473980, 0x4739CA, "d066985b4ab374832e4b20b72d5608a10a5c41f904730f71db6919b40e816f59"),
    # Named ColorScheme original name parser.
    (0x474A90, 0x474B1A, "96dc7d828887a3f449353f4027378e9ed379fcd38dfc14106cd3112e01245b0c"),
    # Temporary color vector copy constructor.
    (0x478220, 0x4782D5, "9bb22f71bdf45da567aadef58afecc355650bad544d4c28083164de21117ead1"),
    # Country lookup to native House bit.
    (0x48DEB0, 0x48DECC, "c258651882530e4c8e3f74bf4b589ccd4185366f9bed5d62dee95de53d54506b"),
    # Layer enum parser.
    (0x48E050, 0x48E089, "cb1e18466000f670443483dd87c1c33b81a79edaec8412f1531d29f5c05368f7"),
    # Layer enum formatter.
    (0x48E090, 0x48E0A3, "99e10019077c0413be29a88276ea84f746d335ecef1c0f89147039328c803115"),
    # Infantry name find existing registry.
    (0x523C90, 0x523CF1, "b47b000b5c789046d56994268f0d45ea702a4586d8e9b6a29854e9217669663e"),
    # CRC temporary header constructor.
    (0x52AEC0, 0x52AED3, "28df2a2e8fad58e026018531dac4dac516e38500013a84903f827853c83f55c6"),
    # INI key index original sorted lookup.
    (0x52B210, 0x52B2A5, "565957759ec1e4b79e643527320a0c513ad45ea1936c8f169ad23d5d588275e5"),
    # SuperWeapon name find existing registry.
    (0x6CEE60, 0x6CEEA1, "400dba34045cae4538d6f9d72595fa8b6d05cb6aaba24d977dd3359ae86d35d5"),
    # Warhead affect-type original18 name parser.
    (0x74FEF0, 0x74FF25, "65f238866e4ae608613e6e82b0592f6cfe3df352601359922b1210e25447414d"),
    # Armor original eleven-name parser; pointer bound7E523C.
    (0x772A50, 0x772A88, "63f05fe6a8dbc4e97ee3befe164bdfc9a86958e71f92d488be21d1cbc8860fd9"),
    # Bullet native derived pointer vector resize.
    (0x4EE5C0, 0x4EE670, "95cc7a9f6b8c01c5429fca069cb2462dd2494757c515f10b48851874a6eef734"),
    # Bullet native derived pointer vector clear.
    (0x4E8F60, 0x4E8F8A, "ea5cdaaa86709ea1d9393acd015522f2cc4e31b9061e4044c91a43bafe463c5c"),
    # Color native derived vector clear.
    (0x477900, 0x47792A, "b1c9b4d16b98b8c6b8bd8dd6c6bf5b8b7020aca3989a1c56a4243ef546506b44"),
    # Country original concrete class-kind leaf.
    (0x512710, 0x512716, "de007fbe046756dbb8aa3cdc727082f435e259d016267520350998706d517385"),
    # SuperWeapon original concrete class-kind leaf.
    (0x6CE8F0, 0x6CE8F6, "6e7ad2e0613c7b35767a2892528cb56d04e6c29c6569027d24dd57c372d07617"),
    # Anim original concrete class-kind leaf.
    (0x428E50, 0x428E56, "21faa16607cb70438711aab3fa582829af50aa15d5946524996fc7aa8a8e4e6d"),
    # Building original concrete class-kind leaf.
    (0x465D90, 0x465D96, "7500687ab6484f894dd29beddc484e671de6539e4faf19ef80805cfd49e55624"),
    # Aircraft original concrete class-kind leaf.
    (0x41CFB0, 0x41CFB6, "7adb2a5467d3718ab3b55c6851599af573d4fbeadcd90dd961cfd69d4f94cc9f"),
    # Infantry original concrete class-kind leaf.
    (0x524D40, 0x524D46, "75f533bd3e59de2588c8f1901e45a3eea6688bc16b7ecaf3dcaf4d49cf4f3d49"),
    # Weapon original concrete class-kind leaf.
    (0x7730E0, 0x7730E6, "b51b8cf9800e04adbbe8029b6676afea560b47b232d98106af7ac15ac5215144"),
    # Bullet original concrete class-kind leaf.
    (0x46C850, 0x46C856, "491fd347216c9bbae36837ea422dc8d4d5bd6a8c889ee1b18a90650dd7dbb1b6"),
    # Warhead original concrete class-kind leaf.
    (0x75E500, 0x75E506, "7014eb9e06dadd63d0b87144bce8629f02ed2856e23551faca425005c46accbe"),
    # Terrain original concrete class-kind leaf.
    (0x71E330, 0x71E336, "b3aead4a2f2b71b81ff91e2e550dd830b445948d7fff71521516b86bb840e8df"),
    # Smudge original concrete class-kind leaf.
    (0x6B6130, 0x6B6136, "c1ff6f09e9a650308b4724bdf5e9b2778c80630e91ea5a47ac6e32ba695875cd"),
    # Overlay original concrete class-kind leaf.
    (0x5FEF00, 0x5FEF06, "e4f9f7041b372cb8bd7dda73eb33390a3fb3a11ea2164b2b6a465b11b2ea2188"),
    # Particle original concrete class-kind leaf.
    (0x645920, 0x645926, "7f32f9318a0651d8bad36d2c6c7c4d1f1e1f6cdd55569441515ed9d2eb076e14"),
    # ParticleSystem original concrete class-kind leaf.
    (0x644930, 0x644936, "49284e5a57f3a3975d45904142e135f007e997b81a88671e86fdbff4313ea7e3"),
    # VoxelAnim original concrete class-kind leaf.
    (0x74B9F0, 0x74B9F6, "11db5348e275fb704be582e8005ee7d604f7f17b154d6cc644d240eef29d456a"),
)

LIVE_READ_ONLY = (
    (0x7E2894, 4),  # Aircraft +2C
    (0x7E28CC, 4),  # Aircraft +64
    (0x7E3634, 4),  # Anim +2C
    (0x7E366C, 4),  # Anim +64
    (0x7E3860, 8),  # Building FPU rounding bias
    (0x7E4430, 4),  # Concrete vector0x7e4424 0xc
    (0x7E459C, 4),  # Building +2C
    (0x7E45D4, 4),  # Building +64
    (0x7E4974, 4),  # Bullet +2C
    (0x7E49AC, 4),  # Bullet +64
    (0x7E4C50, 292),  # Action73 enum-name slots; native end7E4D74
    (0x7E5168, 4),  # Techno FPU scalar
    (0x7E5190, 8),  # Weapon postpass FPU multiplier
    (0x7E5210, 44),  # Armor eleven name pointers; native end7E523C
    (0x7EA36C, 4),  # Concrete vector0x7ea364 0x8
    (0x7EA370, 4),  # Concrete vector0x7ea364 0xc
    (0x7EAB84, 4),  # Country +2C
    (0x7EABBC, 4),  # Country +64
    (0x7EB63C, 4),  # Infantry +2C
    (0x7EB674, 4),  # Infantry +64
    (0x7EF62C, 4),  # Overlay +2C
    (0x7EF664, 4),  # Overlay +64
    (0x7F00D4, 4),  # ParticleSystem +2C
    (0x7F010C, 4),  # ParticleSystem +64
    (0x7F01B4, 4),  # Particle +2C
    (0x7F01EC, 4),  # Particle +64
    (0x7F0234, 4),  # Concrete vector0x7f022c 0x8
    (0x7F0238, 4),  # Concrete vector0x7f022c 0xc
    (0x7F0DD4, 4),  # Concrete vector0x7f0dcc 0x8
    (0x7F0DD8, 4),  # Concrete vector0x7f0dcc 0xc
    (0x7F3554, 4),  # Smudge +2C
    (0x7F358C, 4),  # Smudge +64
    (0x7F40BC, 4),  # SuperWeapon +2C
    (0x7F40F4, 4),  # SuperWeapon +64
    (0x7F4100, 4),  # SuperWeapon FPU scalar
    (0x7F4FB8, 8),  # Techno FPU scalar
    (0x7F5484, 4),  # Terrain +2C
    (0x7F54BC, 4),  # Terrain +64
    (0x7F6B5C, 4),  # Warhead +2C
    (0x7F6B94, 4),  # Warhead +64
    (0x7F73E4, 4),  # Weapon +2C
    (0x7F741C, 4),  # Weapon +64
    (0x816CAC, 128),  # 32 MissionControl section pointers
    (0x816D2C, 17),  # Spyplane Overfly
    (0x816D40, 18),  # Spyplane Approach
    (0x816D54, 12),  # Attack Move
    (0x816D60, 5),  # Wait
    (0x816D68, 17),  # Paradrop Overfly
    (0x816D7C, 18),  # Paradrop Approach
    (0x816D90, 7),  # Patrol
    (0x816D98, 5),  # Open
    (0x816DA0, 9),  # Harmless
    (0x816DAC, 8),  # Missile
    (0x816DB4, 7),  # Rescue
    (0x816DBC, 7),  # Repair
    (0x816DC4, 8),  # Selling
    (0x816DCC, 13),  # Construction
    (0x816DDC, 9),  # Sabotage
    (0x816DE8, 7),  # Unload
    (0x816DF0, 5),  # Hunt
    (0x816DF8, 7),  # Ambush
    (0x816E00, 5),  # Stop
    (0x816E08, 7),  # Return
    (0x816E10, 11),  # Area Guard
    (0x816E1C, 8),  # Harvest
    (0x816E24, 6),  # Eaten
    (0x816E2C, 8),  # Capture
    (0x816E34, 6),  # Enter
    (0x816E3C, 7),  # Sticky
    (0x816E44, 6),  # Guard
    (0x816E4C, 8),  # Retreat
    (0x816E54, 6),  # QMove
    (0x816E5C, 5),  # Move
    (0x816E64, 7),  # Attack
    (0x816E6C, 6),  # Sleep
    (0x816EE0, 592),  # AI trigger74 name/value records
    (0x817130, 8),  # Unknown
    (0x817134, 4),  # own
    (0x817138, 10),  # DiskLaser
    (0x817144, 13),  # SlaveManager
    (0x817154, 10),  # Airstrike
    (0x817160, 8),  # RadSite
    (0x817174, 5),  # Bomb
    (0x817188, 15),  # CaptureManager
    (0x817198, 13),  # SpawnManager
    (0x8171A8, 9),  # NavyType
    (0x8171B4, 16),  # VeinholeMonster
    (0x8171C4, 11),  # AlphaShape
    (0x8171D0, 13),  # FoggedObject
    (0x8171E0, 7),  # Neuron
    (0x8171E8, 14),  # AITriggerType
    (0x8171F8, 10),  # AITrigger
    (0x817204, 12),  # SuperWeapon
    (0x817210, 12),  # TacticalMap
    (0x81721C, 8),  # EMPulse
    (0x817224, 12),  # LightSource
    (0x817230, 5),  # Tube
    (0x817238, 9),  # Abstract
    (0x817244, 9),  # Waypoint
    (0x817250, 12),  # WarheadType
    (0x81725C, 11),  # WeaponType
    (0x817268, 6),  # Event
    (0x817270, 7),  # Action
    (0x817284, 8),  # TagType
    (0x81728C, 4),  # Tag
    (0x817290, 5),  # Wave
    (0x817298, 14),  # VoxelAnimType
    (0x8172A8, 10),  # VoxelAnim
    (0x8172B4, 9),  # UnitType
    (0x8172C0, 12),  # TriggerType
    (0x8172CC, 8),  # Trigger
    (0x8172D4, 12),  # TerrainType
    (0x8172E0, 8),  # Terrain
    (0x8172E8, 9),  # TeamType
    (0x8172F4, 5),  # Team
    (0x8172FC, 10),  # TaskForce
    (0x817308, 16),  # SuperWeaponType
    (0x817318, 8),  # Special
    (0x817320, 11),  # SmudgeType
    (0x81732C, 7),  # Smudge
    (0x817334, 5),  # Side
    (0x81733C, 11),  # ScriptType
    (0x817348, 7),  # Script
    (0x817350, 19),  # ParticleSystemType
    (0x817364, 15),  # ParticleSystem
    (0x817374, 13),  # ParticleType
    (0x817384, 9),  # Particle
    (0x817390, 12),  # OverlayType
    (0x81739C, 8),  # Overlay
    (0x8173A4, 6),  # Light
    (0x8173AC, 12),  # IsotileType
    (0x8173B8, 8),  # Isotile
    (0x8173C0, 13),  # InfantryType
    (0x8173DC, 10),  # HouseType
    (0x8173E8, 6),  # House
    (0x8173F0, 8),  # Factory
    (0x8173F8, 5),  # Cell
    (0x817400, 9),  # Campaign
    (0x81740C, 11),  # BulletType
    (0x817418, 7),  # Bullet
    (0x817420, 13),  # BuildingType
    (0x817430, 9),  # Building
    (0x81743C, 9),  # AnimType
    (0x817448, 5),  # Anim
    (0x817450, 13),  # AircraftType
    (0x81758C, 4),  # Air
    (0x817830, 25),  # D:\ra2mdpost\AbsType.cpp
    (0x81784C, 7),  # UIName
    (0x817854, 5),  # Name
    (0x817F64, 8),  # None default; strncpy7C9266 reads original NUL padding DWORD
    (0x817FF0, 8),  # FlyBack
    (0x817FF8, 6),  # FlyBy
    (0x818000, 11),  # SpawnDelay
    (0x81800C, 8),  # Trailer
    (0x818014, 12),  # CustomRotor
    (0x818020, 7),  # Rotors
    (0x818028, 9),  # Carryall
    (0x818034, 8),  # Fighter
    (0x81803C, 13),  # AirportBound
    (0x81804C, 9),  # Landable
    (0x818164, 9),  # Civilian
    (0x81834C, 5),  # .SHP
    (0x818354, 11),  # RandomRate
    (0x818360, 13),  # NumParticles
    (0x818370, 15),  # SpawnsParticle
    (0x818380, 15),  # UseNormalLight
    (0x818390, 20),  # ShouldUseCellDrawer
    (0x8183A4, 6),  # Tiled
    (0x8183AC, 8),  # Bouncer
    (0x8183BC, 13),  # DamageRadius
    (0x8183CC, 18),  # TrailerSeperation
    (0x8183E0, 12),  # TrailerAnim
    (0x8183EC, 11),  # ExpireAnim
    (0x8183F8, 11),  # BounceAnim
    (0x818404, 10),  # StopSound
    (0x818410, 7),  # Report
    (0x818418, 11),  # StartSound
    (0x818424, 8),  # ZAdjust
    (0x81842C, 12),  # YDrawOffset
    (0x818438, 14),  # RunningFrames
    (0x818448, 13),  # IsFlamingGuy
    (0x818458, 16),  # ShouldFogRemove
    (0x818468, 19),  # IsAnimatedTiberium
    (0x81847C, 18),  # TiberiumSpawnType
    (0x818490, 21),  # TiberiumSpreadRadius
    (0x8184B0, 9),  # IsMeteor
    (0x8184BC, 11),  # SpawnCount
    (0x8184D0, 13),  # MakeInfantry
    (0x8184E0, 8),  # MinZVel
    (0x8184E8, 9),  # MaxXYVel
    (0x8184F4, 11),  # Elasticity
    (0x818500, 12),  # YSortAdjust
    (0x81850C, 12),  # HideIfNoOre
    (0x818518, 11),  # IsTiberium
    (0x818524, 13),  # Translucency
    (0x818534, 16),  # RandomLoopDelay
    (0x818544, 24),  # TranslucencyDetailLevel
    (0x81855C, 12),  # DetailLevel
    (0x818568, 5),  # Next
    (0x818570, 10),  # LoopCount
    (0x81857C, 8),  # LoopEnd
    (0x818584, 10),  # LoopStart
    (0x818590, 4),  # End
    (0x818594, 6),  # Start
    (0x81859C, 7),  # Damage
    (0x8185A4, 5),  # Rate
    (0x8185AC, 22),  # TiberiumChainReaction
    (0x8185C4, 11),  # PsiWarning
    (0x8185D0, 8),  # Reverse
    (0x8185D8, 9),  # PingPong
    (0x8185E4, 16),  # ForceBigCraters
    (0x8185F4, 7),  # Crater
    (0x8185FC, 7),  # Scorch
    (0x818604, 12),  # Translucent
    (0x818610, 11),  # Normalized
    (0x81861C, 7),  # Flamer
    (0x818624, 5),  # Flat
    (0x81862C, 12),  # DoubleThick
    (0x818638, 11),  # AltPalette
    (0x818644, 6),  # Layer
    (0x81864C, 11),  # NewTheater
    (0x818660, 7),  # Shadow
    (0x819288, 48),  # Building six name/value records
    (0x819368, 7),  # Combat
    (0x819370, 15),  # Infrastructure
    (0x819380, 9),  # Resource
    (0x81938C, 6),  # Power
    (0x819394, 5),  # Tech
    (0x81939C, 9),  # DontCare
    (0x819490, 14),  # DeployingAnim
    (0x8194AC, 5),  # .VXL
    (0x8194B4, 16),  # DockingOffset%d
    (0x8194C4, 14),  # NumberOfDocks
    (0x8194D4, 17),  # PowerUp%01dYSort
    (0x8194E8, 17),  # PowerUp%01dLocZZ
    (0x8194FC, 17),  # PowerUp%01dLocYY
    (0x819510, 17),  # PowerUp%01dLocXX
    (0x819524, 23),  # PowerUp%01dDamagedAnim
    (0x81953C, 16),  # PowerUp%01dAnim
    (0x81954C, 9),  # Upgrades
    (0x819558, 29),  # VoxelBarrelOffsetToBarrelEnd
    (0x819578, 38),  # VoxelBarrelOffsetToBuildingPivotPoint
    (0x8195A0, 36),  # VoxelBarrelOffsetToRotatePivotPoint
    (0x8195C4, 35),  # VoxelBarrelOffsetToPitchPivotPoint
    (0x8195E8, 16),  # VoxelBarrelFile
    (0x8195F8, 18),  # BarrelAnimIsVoxel
    (0x81960C, 18),  # TurretAnimIsVoxel
    (0x819620, 16),  # TurretAnimYSort
    (0x819630, 18),  # TurretAnimZAdjust
    (0x819644, 12),  # TurretAnimY
    (0x819650, 12),  # TurretAnimX
    (0x81965C, 21),  # TurretAnimGarrisoned
    (0x819674, 18),  # TurretAnimDamaged
    (0x819688, 11),  # TurretAnim
    (0x819694, 23),  # PreProductionAnimYSort
    (0x8196AC, 25),  # PreProductionAnimZAdjust
    (0x8196C8, 19),  # PreProductionAnimY
    (0x8196DC, 19),  # PreProductionAnimX
    (0x8196F0, 28),  # PreProductionAnimGarrisoned
    (0x81970C, 25),  # PreProductionAnimDamaged
    (0x819728, 18),  # PreProductionAnim
    (0x81973C, 23),  # IdleAnimPoweredSpecial
    (0x819754, 22),  # IdleAnimPoweredEffect
    (0x81976C, 21),  # IdleAnimPoweredLight
    (0x819784, 16),  # IdleAnimPowered
    (0x819794, 14),  # IdleAnimYSort
    (0x8197A4, 16),  # IdleAnimZAdjust
    (0x8197B4, 10),  # IdleAnimY
    (0x8197C0, 10),  # IdleAnimX
    (0x8197CC, 19),  # IdleAnimGarrisoned
    (0x8197E0, 16),  # IdleAnimDamaged
    (0x8197F0, 9),  # IdleAnim
    (0x8197FC, 20),  # ProductionAnimYSort
    (0x819810, 22),  # ProductionAnimZAdjust
    (0x819828, 16),  # ProductionAnimY
    (0x819838, 16),  # ProductionAnimX
    (0x819848, 25),  # ProductionAnimGarrisoned
    (0x819864, 22),  # ProductionAnimDamaged
    (0x81987C, 15),  # ProductionAnim
    (0x81988C, 28),  # SuperLowPowerPoweredSpecial
    (0x8198A8, 27),  # SuperLowPowerPoweredEffect
    (0x8198C4, 26),  # SuperLowPowerPoweredLight
    (0x8198E0, 21),  # SuperLowPowerPowered
    (0x8198F8, 19),  # SuperLowPowerYSort
    (0x81990C, 21),  # SuperLowPowerZAdjust
    (0x819924, 15),  # SuperLowPowerY
    (0x819934, 15),  # SuperLowPowerX
    (0x819944, 24),  # SuperLowPowerGarrisoned
    (0x81995C, 21),  # SuperLowPowerDamaged
    (0x819974, 14),  # SuperLowPower
    (0x819984, 23),  # LowPowerPoweredSpecial
    (0x81999C, 22),  # LowPowerPoweredEffect
    (0x8199B4, 21),  # LowPowerPoweredLight
    (0x8199CC, 16),  # LowPowerPowered
    (0x8199DC, 14),  # LowPowerYSort
    (0x8199EC, 16),  # LowPowerZAdjust
    (0x8199FC, 10),  # LowPowerY
    (0x819A08, 10),  # LowPowerX
    (0x819A14, 19),  # LowPowerGarrisoned
    (0x819A28, 16),  # LowPowerDamaged
    (0x819A38, 9),  # LowPower
    (0x819A44, 30),  # SpecialAnimFourPoweredSpecial
    (0x819A64, 29),  # SpecialAnimFourPoweredEffect
    (0x819A84, 28),  # SpecialAnimFourPoweredLight
    (0x819AA0, 23),  # SpecialAnimFourPowered
    (0x819AB8, 21),  # SpecialAnimFourYSort
    (0x819AD0, 23),  # SpecialAnimFourZAdjust
    (0x819AE8, 17),  # SpecialAnimFourY
    (0x819AFC, 17),  # SpecialAnimFourX
    (0x819B10, 26),  # SpecialAnimFourGarrisoned
    (0x819B2C, 23),  # SpecialAnimFourDamaged
    (0x819B44, 16),  # SpecialAnimFour
    (0x819B54, 31),  # SpecialAnimThreePoweredSpecial
    (0x819B74, 30),  # SpecialAnimThreePoweredEffect
    (0x819B94, 29),  # SpecialAnimThreePoweredLight
    (0x819BB4, 24),  # SpecialAnimThreePowered
    (0x819BCC, 22),  # SpecialAnimThreeYSort
    (0x819BE4, 24),  # SpecialAnimThreeZAdjust
    (0x819BFC, 18),  # SpecialAnimThreeY
    (0x819C10, 18),  # SpecialAnimThreeX
    (0x819C24, 27),  # SpecialAnimThreeGarrisoned
    (0x819C40, 24),  # SpecialAnimThreeDamaged
    (0x819C58, 17),  # SpecialAnimThree
    (0x819C6C, 29),  # SpecialAnimTwoPoweredSpecial
    (0x819C8C, 28),  # SpecialAnimTwoPoweredEffect
    (0x819CA8, 27),  # SpecialAnimTwoPoweredLight
    (0x819CC4, 22),  # SpecialAnimTwoPowered
    (0x819CDC, 20),  # SpecialAnimTwoYSort
    (0x819CF0, 22),  # SpecialAnimTwoZAdjust
    (0x819D08, 16),  # SpecialAnimTwoY
    (0x819D18, 16),  # SpecialAnimTwoX
    (0x819D28, 25),  # SpecialAnimTwoGarrisoned
    (0x819D44, 22),  # SpecialAnimTwoDamaged
    (0x819D5C, 15),  # SpecialAnimTwo
    (0x819D6C, 26),  # SpecialAnimPoweredSpecial
    (0x819D88, 25),  # SpecialAnimPoweredEffect
    (0x819DA4, 24),  # SpecialAnimPoweredLight
    (0x819DBC, 19),  # SpecialAnimPowered
    (0x819DD0, 17),  # SpecialAnimYSort
    (0x819DE4, 19),  # SpecialAnimZAdjust
    (0x819DF8, 13),  # SpecialAnimY
    (0x819E08, 13),  # SpecialAnimX
    (0x819E18, 22),  # SpecialAnimGarrisoned
    (0x819E30, 19),  # SpecialAnimDamaged
    (0x819E44, 12),  # SpecialAnim
    (0x819E50, 28),  # SuperAnimFourPoweredSpecial
    (0x819E6C, 27),  # SuperAnimFourPoweredEffect
    (0x819E88, 26),  # SuperAnimFourPoweredLight
    (0x819EA4, 21),  # SuperAnimFourPowered
    (0x819EBC, 19),  # SuperAnimFourYSort
    (0x819ED0, 21),  # SuperAnimFourZAdjust
    (0x819EE8, 15),  # SuperAnimFourY
    (0x819EF8, 15),  # SuperAnimFourX
    (0x819F08, 24),  # SuperAnimFourGarrisoned
    (0x819F20, 21),  # SuperAnimFourDamaged
    (0x819F38, 14),  # SuperAnimFour
    (0x819F48, 29),  # SuperAnimThreePoweredSpecial
    (0x819F68, 28),  # SuperAnimThreePoweredEffect
    (0x819F84, 27),  # SuperAnimThreePoweredLight
    (0x819FA0, 22),  # SuperAnimThreePowered
    (0x819FB8, 20),  # SuperAnimThreeYSort
    (0x819FCC, 22),  # SuperAnimThreeZAdjust
    (0x819FE4, 16),  # SuperAnimThreeY
    (0x819FF4, 16),  # SuperAnimThreeX
    (0x81A004, 25),  # SuperAnimThreeGarrisoned
    (0x81A020, 22),  # SuperAnimThreeDamaged
    (0x81A038, 15),  # SuperAnimThree
    (0x81A048, 27),  # SuperAnimTwoPoweredSpecial
    (0x81A064, 26),  # SuperAnimTwoPoweredEffect
    (0x81A080, 25),  # SuperAnimTwoPoweredLight
    (0x81A09C, 20),  # SuperAnimTwoPowered
    (0x81A0B0, 18),  # SuperAnimTwoYSort
    (0x81A0C4, 20),  # SuperAnimTwoZAdjust
    (0x81A0D8, 14),  # SuperAnimTwoY
    (0x81A0E8, 14),  # SuperAnimTwoX
    (0x81A0F8, 23),  # SuperAnimTwoGarrisoned
    (0x81A110, 20),  # SuperAnimTwoDamaged
    (0x81A124, 13),  # SuperAnimTwo
    (0x81A134, 24),  # SuperAnimPoweredSpecial
    (0x81A14C, 23),  # SuperAnimPoweredEffect
    (0x81A164, 22),  # SuperAnimPoweredLight
    (0x81A17C, 17),  # SuperAnimPowered
    (0x81A190, 15),  # SuperAnimYSort
    (0x81A1A0, 17),  # SuperAnimZAdjust
    (0x81A1B4, 11),  # SuperAnimY
    (0x81A1C0, 11),  # SuperAnimX
    (0x81A1CC, 20),  # SuperAnimGarrisoned
    (0x81A1E0, 17),  # SuperAnimDamaged
    (0x81A1F4, 10),  # SuperAnim
    (0x81A200, 29),  # ActiveAnimFourPoweredSpecial
    (0x81A220, 28),  # ActiveAnimFourPoweredEffect
    (0x81A23C, 27),  # ActiveAnimFourPoweredLight
    (0x81A258, 22),  # ActiveAnimFourPowered
    (0x81A270, 20),  # ActiveAnimFourYSort
    (0x81A284, 22),  # ActiveAnimFourZAdjust
    (0x81A29C, 16),  # ActiveAnimFourY
    (0x81A2AC, 16),  # ActiveAnimFourX
    (0x81A2BC, 25),  # ActiveAnimFourGarrisoned
    (0x81A2D8, 22),  # ActiveAnimFourDamaged
    (0x81A2F0, 15),  # ActiveAnimFour
    (0x81A300, 30),  # ActiveAnimThreePoweredSpecial
    (0x81A320, 29),  # ActiveAnimThreePoweredEffect
    (0x81A340, 28),  # ActiveAnimThreePoweredLight
    (0x81A35C, 23),  # ActiveAnimThreePowered
    (0x81A374, 21),  # ActiveAnimThreeYSort
    (0x81A38C, 23),  # ActiveAnimThreeZAdjust
    (0x81A3A4, 17),  # ActiveAnimThreeY
    (0x81A3B8, 17),  # ActiveAnimThreeX
    (0x81A3CC, 26),  # ActiveAnimThreeGarrisoned
    (0x81A3E8, 23),  # ActiveAnimThreeDamaged
    (0x81A400, 16),  # ActiveAnimThree
    (0x81A410, 28),  # ActiveAnimTwoPoweredSpecial
    (0x81A42C, 27),  # ActiveAnimTwoPoweredEffect
    (0x81A448, 26),  # ActiveAnimTwoPoweredLight
    (0x81A464, 21),  # ActiveAnimTwoPowered
    (0x81A47C, 19),  # ActiveAnimTwoYSort
    (0x81A490, 21),  # ActiveAnimTwoZAdjust
    (0x81A4A8, 15),  # ActiveAnimTwoY
    (0x81A4B8, 15),  # ActiveAnimTwoX
    (0x81A4C8, 24),  # ActiveAnimTwoGarrisoned
    (0x81A4E0, 21),  # ActiveAnimTwoDamaged
    (0x81A4F8, 14),  # ActiveAnimTwo
    (0x81A508, 25),  # ActiveAnimPoweredSpecial
    (0x81A524, 24),  # ActiveAnimPoweredEffect
    (0x81A53C, 23),  # ActiveAnimPoweredLight
    (0x81A554, 18),  # ActiveAnimPowered
    (0x81A568, 16),  # ActiveAnimYSort
    (0x81A578, 18),  # ActiveAnimZAdjust
    (0x81A58C, 12),  # ActiveAnimY
    (0x81A598, 12),  # ActiveAnimX
    (0x81A5A4, 21),  # ActiveAnimGarrisoned
    (0x81A5BC, 18),  # ActiveAnimDamaged
    (0x81A5D0, 11),  # ActiveAnim
    (0x81A5DC, 9),  # AnimAux2
    (0x81A5E8, 9),  # AnimAux1
    (0x81A5F4, 11),  # AnimActive
    (0x81A600, 9),  # AnimIdle
    (0x81A60C, 8),  # Buildup
    (0x81A614, 13),  # QueueingCell
    (0x81A624, 15),  # RemoveOccupy%d
    (0x81A634, 12),  # AddOccupy%d
    (0x81A640, 14),  # CanHideThings
    (0x81A650, 11),  # ExtraLight
    (0x81A65C, 16),  # ZShapePointMove
    (0x81A66C, 14),  # NormalZAdjust
    (0x81A67C, 23),  # SpecialZOverlayZAdjust
    (0x81A694, 17),  # ExtraDamageStage
    (0x81A6A8, 22),  # PrimaryFireDualOffset
    (0x81A6C0, 25),  # SecondaryFirePixelOffset
    (0x81A6DC, 23),  # PrimaryFirePixelOffset
    (0x81A6F4, 11),  # GateStages
    (0x81A700, 15),  # TerrainPalette
    (0x81A710, 12),  # DamagedDoor
    (0x81A71C, 11),  # DoorStages
    (0x81A728, 9),  # MidPoint
    (0x81A734, 11),  # Foundation
    (0x81A740, 10),  # ToOverlay
    (0x81A74C, 17),  # DelayedFireDelay
    (0x81A760, 18),  # IsAnimDelayedFire
    (0x81A774, 11),  # ChargeAnim
    (0x81A780, 11),  # SiloDamage
    (0x81A78C, 11),  # Recoilless
    (0x81A798, 13),  # OccupyHeight
    (0x81A7A8, 7),  # Height
    (0x81A7B0, 11),  # ExtraPower
    (0x81A7BC, 26),  # ConcentricRadialIndicator
    (0x81A7D8, 19),  # IsThreatRatingNode
    (0x81A7EC, 14),  # IsBaseDefense
    (0x81A7FC, 12),  # AIBuildThis
    (0x81A808, 10),  # ExitCoord
    (0x81A814, 18),  # TargetCoordOffset
    (0x81A828, 10),  # Artillary
    (0x81A834, 13),  # ICBMLauncher
    (0x81A844, 14),  # PlaceAnywhere
    (0x81A854, 12),  # LeaveRubble
    (0x81A860, 20),  # CrateBeneathIsMoney
    (0x81A874, 13),  # CrateBeneath
    (0x81A884, 19),  # HasStupidGuardMode
    (0x81A898, 16),  # BridgeRepairHut
    (0x81A8A8, 16),  # PowersUpToLevel
    (0x81A8B8, 17),  # PowersUpBuilding
    (0x81A8CC, 16),  # InvisibleInGame
    (0x81A8DC, 15),  # GateCloseDelay
    (0x81A8EC, 14),  # LightBlueTint
    (0x81A8FC, 15),  # LightGreenTint
    (0x81A90C, 13),  # LightRedTint
    (0x81A91C, 15),  # LightIntensity
    (0x81A92C, 16),  # LightVisibility
    (0x81A93C, 13),  # DeployFacing
    (0x81A94C, 17),  # BarrelStartPitch
    (0x81A960, 23),  # PsychicDetectionRadius
    (0x81A978, 19),  # CloakRadiusInCells
    (0x81A98C, 12),  # SensorArray
    (0x81A998, 15),  # CloakGenerator
    (0x81A9A8, 13),  # SuperWeapon2
    (0x81A9B8, 16),  # ChargedAnimTime
    (0x81A9C8, 9),  # TickTank
    (0x81A9D4, 14),  # EMPulseCannon
    (0x81A9E4, 13),  # YuriBarracks
    (0x81A9F4, 12),  # NODBarracks
    (0x81AA00, 12),  # GDIBarracks
    (0x81AA0C, 7),  # Armory
    (0x81AA14, 9),  # Hospital
    (0x81AA20, 14),  # FirestormWall
    (0x81AA30, 11),  # LaserFence
    (0x81AA3C, 15),  # LaserFencePost
    (0x81AA4C, 15),  # WeaponsFactory
    (0x81AA5C, 9),  # Refinery
    (0x81AA68, 9),  # NukeSilo
    (0x81AA74, 17),  # ConstructionYard
    (0x81AA88, 4),  # SAM
    (0x81AA8C, 5),  # Gate
    (0x81AA94, 11),  # DockUnload
    (0x81AAA0, 10),  # SecretLab
    (0x81AAAC, 15),  # InfantryAbsorb
    (0x81AABC, 11),  # UnitAbsorb
    (0x81AAC8, 9),  # Grinding
    (0x81AAD4, 8),  # Cloning
    (0x81AADC, 7),  # Bunker
    (0x81AAE4, 11),  # UnitReload
    (0x81AAF0, 11),  # UnitRepair
    (0x81AAFC, 16),  # NotWorkingSound
    (0x81AB0C, 13),  # WorkingSound
    (0x81AB1C, 15),  # UnitEnterSound
    (0x81AB2C, 14),  # UnitExitSound
    (0x81AB3C, 16),  # CreateUnitSound
    (0x81AB4C, 12),  # PackupSound
    (0x81AB58, 13),  # BuildupSound
    (0x81AB68, 12),  # TogglePower
    (0x81AB74, 18),  # DefensesCostBonus
    (0x81AB88, 19),  # BuildingsCostBonus
    (0x81AB9C, 18),  # AircraftCostBonus
    (0x81ABB0, 15),  # UnitsCostBonus
    (0x81ABC0, 18),  # InfantryCostBonus
    (0x81ABD4, 15),  # SecretBuilding
    (0x81ABE4, 11),  # SecretUnit
    (0x81AC00, 7),  # IsPlug
    (0x81AC08, 9),  # IsTemple
    (0x81AC14, 9),  # HoverPad
    (0x81AC20, 9),  # FreeUnit
    (0x81AC2C, 13),  # FactoryPlant
    (0x81AC3C, 12),  # OrePurifier
    (0x81AC48, 8),  # Helipad
    (0x81AC50, 7),  # Weeder
    (0x81AC60, 17),  # DamageFireOffset
    (0x81AC74, 12),  # MuzzleFlash
    (0x81AC80, 16),  # ProtectWithWall
    (0x81AC90, 16),  # CaptureEvaEvent
    (0x81ACA0, 14),  # NeedsEngineer
    (0x81ACB0, 21),  # EligibleForDelayKill
    (0x81ACC8, 25),  # EligibileForAllyBuilding
    (0x81ACE4, 11),  # BaseNormal
    (0x81ACF0, 20),  # RefinerySmokeFrames
    (0x81AD04, 18),  # UnitsGainSelfHeal
    (0x81AD18, 21),  # InfantryGainSelfHeal
    (0x81AD30, 17),  # ProduceCashDelay
    (0x81AD44, 18),  # ProduceCashAmount
    (0x81AD58, 19),  # ProduceCashStartup
    (0x81AD6C, 21),  # NumberImpassableRows
    (0x81AD84, 19),  # MaxNumberOccupants
    (0x81AD98, 17),  # ShowOccupantPips
    (0x81ADAC, 14),  # CanOccupyFire
    (0x81ADBC, 14),  # CanBeOccupied
    (0x81ADCC, 16),  # ClickRepairable
    (0x81ADDC, 11),  # Unsellable
    (0x81ADE8, 4),  # Bib
    (0x81ADEC, 16),  # WantsExtraSpace
    (0x81ADFC, 6),  # CanC4
    (0x81AE04, 8),  # Spyable
    (0x81AE0C, 14),  # Overpowerable
    (0x81AE1C, 15),  # PoweredSpecial
    (0x81AE2C, 8),  # Powered
    (0x81AE34, 11),  # Capturable
    (0x81AE40, 9),  # Adjacent
    (0x81AE4C, 11),  # WaterBound
    (0x81AE58, 7),  # SpySat
    (0x81AE60, 6),  # Radar
    (0x81AE68, 25),  # HalfDamageSmokeLocation2
    (0x81AE84, 25),  # HalfDamageSmokeLocation1
    (0x81AEA0, 13),  # HasSpotlight
    (0x81AEB0, 13),  # AntiAirValue
    (0x81AEC0, 15),  # AntiArmorValue
    (0x81AED0, 18),  # AntiInfantryValue
    (0x81AEE4, 9),  # BuildCat
    (0x81AFD0, 12),  # AnimPalette
    (0x81AFDC, 9),  # AnimRate
    (0x81AFE8, 9),  # AnimHigh
    (0x81AFF4, 8),  # AnimLow
    (0x81AFFC, 14),  # FirersPalette
    (0x81B00C, 9),  # Vertical
    (0x81B018, 19),  # DetonationAltitude
    (0x81B02C, 14),  # ShrapnelCount
    (0x81B03C, 15),  # ShrapnelWeapon
    (0x81B04C, 15),  # AirburstWeapon
    (0x81B05C, 8),  # Rotates
    (0x81B064, 9),  # Scalable
    (0x81B070, 8),  # Cluster
    (0x81B078, 9),  # Airburst
    (0x81B084, 7),  # Bouncy
    (0x81B08C, 12),  # Degenerates
    (0x81B098, 3),  # AG
    (0x81B09C, 3),  # AA
    (0x81B0A0, 12),  # FlakScatter
    (0x81B0AC, 11),  # Inaccurate
    (0x81B0B8, 7),  # Ranged
    (0x81B0C0, 10),  # Proximity
    (0x81B0CC, 7),  # Inviso
    (0x81B0DC, 9),  # Dropping
    (0x81B0E8, 9),  # VeryHigh
    (0x81B0F4, 15),  # SubjectToWalls
    (0x81B104, 19),  # SubjectToElevation
    (0x81B118, 16),  # SubjectToCliffs
    (0x81B128, 8),  # Floater
    (0x81B130, 7),  # Arcing
    (0x81B138, 6),  # Color
    (0x81B150, 19),  # CourseLockDuration
    (0x81B168, 4),  # Arm
    (0x81B7C8, 88),  # Category eleven alternate-name pairs; native end81B820
    (0x81B820, 8),  # AirLift
    (0x81B828, 14),  # Air Transport
    (0x81B838, 9),  # AirPower
    (0x81B844, 19),  # Air Combat Support
    (0x81B858, 10),  # Transport
    (0x81B864, 18),  # Transport Vehicle
    (0x81B878, 8),  # Support
    (0x81B880, 22),  # Misc. Support Vehicle
    (0x81B898, 5),  # LRFS
    (0x81B8A0, 22),  # Indirect Fire Support
    (0x81B8B8, 4),  # IFV
    (0x81B8BC, 26),  # Infantry Fighting Vehicle
    (0x81B8D8, 4),  # AFV
    (0x81B8DC, 25),  # Armored Fighting Vehicle
    (0x81B8F8, 6),  # Recon
    (0x81B900, 14),  # Recon Vehicle
    (0x81B910, 4),  # VIP
    (0x81B914, 10),  # VIP/Agent
    (0x81B920, 8),  # Soldier
    (0x81B958, 88),  # Pip eleven name/value records; native end81B9B0
    (0x81B9B0, 40),  # PipScale five name/value records; native end81B9D8
    (0x81B9D8, 176),  # Foundation22 name/value records; native end81BA88
    (0x81BABC, 12),  # Target restriction three names
    (0x81BAC8, 7),  # Strong
    (0x81BB68, 4),  # 0x0
    (0x81BB6C, 4),  # 6x4
    (0x81BB70, 4),  # 3x4
    (0x81BB74, 4),  # 4x4
    (0x81BB78, 4),  # 5x3
    (0x81BB7C, 4),  # 2x5
    (0x81BB80, 4),  # 2x6
    (0x81BB84, 4),  # 1x5
    (0x81BB88, 4),  # 1x4
    (0x81BB8C, 4),  # 4x3
    (0x81BB90, 4),  # 3x1
    (0x81BB94, 4),  # 1x3
    (0x81BB98, 12),  # 3x3Refinery
    (0x81BBA4, 4),  # 4x2
    (0x81BBA8, 4),  # 3x5
    (0x81BBAC, 4),  # 3x3
    (0x81BBB0, 4),  # 3x2
    (0x81BBB4, 4),  # 2x3
    (0x81BBB8, 4),  # 2x2
    (0x81BBBC, 4),  # 1x2
    (0x81BBC0, 4),  # 2x1
    (0x81BBC4, 4),  # 1x1
    (0x81BBD4, 11),  # Passengers
    (0x81BBE8, 13),  # personpurple
    (0x81BBF8, 11),  # personblue
    (0x81BC04, 10),  # personred
    (0x81BC10, 12),  # personwhite
    (0x81BC1C, 13),  # personyellow
    (0x81BC2C, 12),  # persongreen
    (0x81BC38, 5),  # blue
    (0x81BC40, 4),  # red
    (0x81BC44, 6),  # white
    (0x81BC4C, 8),  # yellow Pip default; original strncpy DWORD includes padding
    (0x81BC54, 6),  # green
    (0x81BC5C, 14),  # PsychicReveal
    (0x81BC6C, 14),  # NoForceShield
    (0x81BC7C, 12),  # ForceShield
    (0x81BC88, 17),  # GeneticConverter
    (0x81BC9C, 9),  # SpyPlane
    (0x81BCA8, 17),  # PsychicDominator
    (0x81BCBC, 13),  # AmerParaDrop
    (0x81BCCC, 9),  # Demolish
    (0x81BCD8, 14),  # AttackMoveTar
    (0x81BCE8, 14),  # AttackMoveNav
    (0x81BCF8, 13),  # SelectBeacon
    (0x81BD08, 12),  # PlaceBeacon
    (0x81BD14, 14),  # AttackSupport
    (0x81BD24, 11),  # SelectNode
    (0x81BD30, 11),  # DisarmBomb
    (0x81BD3C, 12),  # DetonateAll
    (0x81BD48, 9),  # Detonate
    (0x81BD54, 11),  # NoIvanBomb
    (0x81BD60, 9),  # IvanBomb
    (0x81BD6C, 11),  # AreaAttack
    (0x81BD78, 15),  # PatrolWaypoint
    (0x81BD88, 14),  # EnterWaypoint
    (0x81BD98, 15),  # AttackWaypoint
    (0x81BDA8, 13),  # DragWaypoint
    (0x81BDB8, 17),  # LoopWaypointPath
    (0x81BDCC, 15),  # SelectWaypoint
    (0x81BDDC, 15),  # FollowWaypoint
    (0x81BDEC, 18),  # EnterWaypointMode
    (0x81BE00, 10),  # TibSunBug
    (0x81BE0C, 14),  # PlaceWaypoint
    (0x81BE1C, 9),  # ParaDrop
    (0x81BE28, 11),  # ChronoWarp
    (0x81BE34, 13),  # ChronoSphere
    (0x81BE44, 15),  # LightningStorm
    (0x81BE54, 12),  # IronCurtain
    (0x81BE60, 14),  # NoEnterTunnel
    (0x81BE70, 12),  # EnterTunnel
    (0x81BE7C, 14),  # NoTogglePower
    (0x81BE8C, 10),  # NoGRepair
    (0x81BE98, 8),  # NoEnter
    (0x81BEA0, 9),  # NoDeploy
    (0x81BEAC, 8),  # GRepair
    (0x81BEB4, 5),  # Heal
    (0x81BEC8, 9),  # DontUse8
    (0x81BED4, 9),  # DontUse7
    (0x81BEE0, 9),  # DontUse6
    (0x81BEEC, 9),  # DontUse5
    (0x81BEF8, 9),  # DontUse4
    (0x81BF04, 5),  # Nuke
    (0x81BF0C, 9),  # DontUse3
    (0x81BF18, 9),  # DontUse2
    (0x81BF24, 5),  # Tote
    (0x81BF2C, 9),  # NoRepair
    (0x81BF38, 7),  # NoSell
    (0x81BF40, 9),  # SellUnit
    (0x81BF4C, 5),  # Sell
    (0x81BF54, 13),  # ToggleSelect
    (0x81BF64, 7),  # Select
    (0x81BF6C, 5),  # Self
    (0x81BF74, 7),  # NoMove
    (0x81C000, 6),  # %d,%d
    (0x81DA78, 20),  # Layer five names; native end81DA8C
    (0x81DB24, 10),  # special_2
    (0x81DB30, 10),  # special_1
    (0x81DB3C, 9),  # concrete
    (0x81DB48, 6),  # steel
    (0x81DB50, 5),  # wood
    (0x81DB58, 6),  # heavy
    (0x81DB60, 7),  # medium
    (0x81DB68, 6),  # light
    (0x81DB70, 6),  # plate
    (0x81DB78, 5),  # flak
    (0x81DB80, 4),  # Top
    (0x81DB8C, 8),  # Surface
    (0x81DB94, 12),  # Underground
    (0x820178, 5),  # Size
    (0x8204FC, 11),  # XXICON.SHP
    (0x820BA0, 8),  # SCATTER
    (0x824254, 8),  # Palette
    (0x824314, 5),  # Type
    (0x825288, 16),  # VeteranAircraft
    (0x825298, 13),  # VeteranUnits
    (0x8252A8, 16),  # VeteranInfantry
    (0x8252B8, 11),  # IncomeMult
    (0x8252C4, 22),  # BuildTimeDefensesMult
    (0x8252DC, 23),  # BuildTimeBuildingsMult
    (0x8252F4, 22),  # BuildTimeAircraftMult
    (0x82530C, 19),  # BuildTimeUnitsMult
    (0x825320, 22),  # BuildTimeInfantryMult
    (0x825338, 18),  # SpeedAircraftMult
    (0x82534C, 15),  # SpeedUnitsMult
    (0x82535C, 18),  # SpeedInfantryMult
    (0x825370, 17),  # CostDefensesMult
    (0x825384, 18),  # CostBuildingsMult
    (0x825398, 17),  # CostAircraftMult
    (0x8253AC, 14),  # CostUnitsMult
    (0x8253BC, 17),  # CostInfantryMult
    (0x8253D0, 18),  # ArmorDefensesMult
    (0x8253E4, 19),  # ArmorBuildingsMult
    (0x8253F8, 18),  # ArmorAircraftMult
    (0x82540C, 15),  # ArmorUnitsMult
    (0x82541C, 18),  # ArmorInfantryMult
    (0x825430, 8),  # SmartAI
    (0x825438, 10),  # WallOwner
    (0x825444, 17),  # MultiplayPassive
    (0x825458, 10),  # Multiplay
    (0x825494, 7),  # Prefix
    (0x82549C, 14),  # ParentCountry
    (0x8254AC, 7),  # Suffix
    (0x825670, 15),  # SecondaryProne
    (0x825680, 14),  # SecondaryFire
    (0x8257B8, 10),  # FireProne
    (0x8257D8, 7),  # FireUp
    (0x8258F4, 7),  # Crawls
    (0x8258FC, 12),  # JumpJetTurn
    (0x825908, 11),  # UseOwnName
    (0x825914, 18),  # DeployedCrushable
    (0x825928, 9),  # Deployer
    (0x825934, 7),  # Doggie
    (0x82593C, 13),  # VehicleThief
    (0x82594C, 6),  # Thief
    (0x825954, 6),  # Agent
    (0x82595C, 14),  # TiberiumProof
    (0x825978, 3),  # C4
    (0x82597C, 12),  # HarvestRate
    (0x825988, 18),  # DetectionDistance
    (0x82599C, 10),  # Assaulter
    (0x8259A8, 9),  # Occupier
    (0x8259B4, 5),  # Ivan
    (0x8259BC, 11),  # Infiltrate
    (0x8259C8, 10),  # Fraidycat
    (0x8259D4, 9),  # Fearless
    (0x8259E0, 16),  # LeaveWaterSound
    (0x8259F0, 16),  # EnterWaterSound
    (0x825A00, 9),  # NotHuman
    (0x825A0C, 7),  # Cyborg
    (0x825A14, 11),  # DeathAnims
    (0x825A2C, 13),  # VoiceComment
    (0x825A3C, 18),  # EliteOccupyWeapon
    (0x825A50, 13),  # OccupyWeapon
    (0x825A60, 10),  # OccupyPip
    (0x825A6C, 4),  # Pip
    (0x82BBE4, 6),  # Width
    (0x82C27C, 7),  # AARate
    (0x82C28C, 10),  # Retaliate
    (0x82C298, 10),  # Paralyzed
    (0x82C2A4, 12),  # Recruitable
    (0x82C2B0, 7),  # Zombie
    (0x82C2B8, 9),  # NoThreat
    (0x832AEC, 6),  # Voxel
    (0x832AF4, 24),  # LineTrailColorDecrement
    (0x832B0C, 15),  # LineTrailColor
    (0x832B1C, 13),  # UseLineTrail
    (0x832B2C, 17),  # IgnoresFirestorm
    (0x832B40, 12),  # RadialColor
    (0x832B4C, 19),  # HasRadialIndicator
    (0x832B60, 14),  # Insignificant
    (0x832B70, 7),  # Immune
    (0x832B84, 12),  # LegalTarget
    (0x832B90, 11),  # Selectable
    (0x832B9C, 15),  # RadarInvisible
    (0x832BAC, 19),  # AlternateArcticArt
    (0x832BC0, 11),  # NoSpawnAlt
    (0x832BCC, 9),  # Bombable
    (0x832BD8, 10),  # Crushable
    (0x832BE4, 13),  # AmbientSound
    (0x832BF4, 11),  # CrushSound
    (0x832C00, 11),  # AlphaImage
    (0x836EF4, 8),  # Railgun
    (0x836EFC, 6),  # Spark
    (0x836F04, 5),  # Fire
    (0x836F0C, 6),  # Smoke
    (0x836F40, 21),  # SpawnSparkPercentage
    (0x836F58, 14),  # OneFrameLight
    (0x836F68, 10),  # LightSize
    (0x836F74, 17),  # SparkSpawnFrames
    (0x836F88, 11),  # LaserColor
    (0x836F94, 6),  # Laser
    (0x836F9C, 32),  # VelocityPerturbationCoefficient
    (0x836FBC, 32),  # MovementPerturbationCoefficient
    (0x836FDC, 32),  # PositionPerturbationCoefficient
    (0x836FFC, 13),  # SpiralRadius
    (0x83700C, 20),  # SpiralDeltaPerCoord
    (0x837020, 18),  # ParticlesPerCoord
    (0x837034, 15),  # SpawnDirection
    (0x837044, 12),  # BehavesLike
    (0x837050, 9),  # Lifetime
    (0x83705C, 24),  # SpawnTranslucencyCutoff
    (0x837074, 12),  # SpawnCutoff
    (0x837080, 9),  # Slowdown
    (0x83708C, 12),  # SpawnRadius
    (0x837098, 12),  # ParticleCap
    (0x8370A4, 12),  # SpawnFrames
    (0x8370B0, 10),  # HoldsWhat
    (0x8370BC, 20),  # Particle five behavior enum names
    (0x8370F0, 13),  # NextParticle
    (0x837100, 17),  # FinalDamageState
    (0x837114, 12),  # StartColor2
    (0x837120, 12),  # StartColor1
    (0x83712C, 19),  # NextParticleOffset
    (0x837140, 15),  # ZVelocityRange
    (0x837150, 13),  # MinZVelocity
    (0x837160, 10),  # YVelocity
    (0x83716C, 10),  # XVelocity
    (0x837178, 11),  # ColorSpeed
    (0x837184, 19),  # Translucent25State
    (0x837198, 19),  # Translucent50State
    (0x8371AC, 15),  # StateAIAdvance
    (0x8371BC, 13),  # StartStateAI
    (0x8371CC, 11),  # EndStateAI
    (0x8371D8, 19),  # DeleteOnStateLimit
    (0x8371EC, 7),  # Radius
    (0x8371F4, 6),  # Deacc
    (0x8371FC, 9),  # Velocity
    (0x837208, 11),  # WindEffect
    (0x837214, 14),  # NumLoopFrames
    (0x837224, 11),  # StartFrame
    (0x837230, 6),  # MaxEC
    (0x837238, 6),  # MaxDC
    (0x837240, 10),  # ColorList
    (0x839E80, 10),  # Radiation
    (0x83A6CC, 16),  # DeactivateSound
    (0x83A6DC, 14),  # ActivateSound
    (0x83A6EC, 21),  # LeaveBioReactorSound
    (0x83A704, 21),  # EnterBioReactorSound
    (0x83A71C, 18),  # LeaveGrinderSound
    (0x83A730, 18),  # EnterGrinderSound
    (0x83A744, 17),  # MindClearedSound
    (0x83A994, 15),  # ChronoOutSound
    (0x83A9A4, 14),  # ChronoInSound
    (0x83A9B4, 13),  # SinkingSound
    (0x83A9C4, 16),  # ImpactLandSound
    (0x83A9D4, 17),  # ImpactWaterSound
    (0x83ADC0, 11),  # TurboBoost
    (0x83B11C, 12),  # DeathWeapon
    (0x840028, 5),  # Burn
    (0x8425C0, 48),  # SuperWeapon twelve typed effect-name slots
    (0x8425F0, 13),  # MultiMissile
    (0x842624, 13),  # SidebarImage
    (0x842634, 13),  # RechargeTime
    (0x842644, 14),  # ManualControl
    (0x842654, 15),  # UseChargeDrain
    (0x842664, 12),  # AuxBuilding
    (0x842670, 13),  # PreDependent
    (0x842680, 15),  # LineMultiplier
    (0x842690, 6),  # Range
    (0x842698, 13),  # SpecialSound
    (0x8426A8, 10),  # ShowTimer
    (0x8426B4, 10),  # PostClick
    (0x8426C0, 9),  # PreClick
    (0x8426CC, 16),  # AIDefendAgainst
    (0x8426DC, 22),  # FlashSidebarTabFrames
    (0x8426F4, 21),  # DisableableFromShell
    (0x84270C, 10),  # IsPowered
    (0x843050, 8),  # Suicide
    (0x8431D8, 18),  # SecondSpawnOffset
    (0x8431EC, 26),  # TurretNotExportedOnGround
    (0x843208, 15),  # AlternateFLH%d
    (0x843218, 22),  # EliteSBarrelThickness
    (0x843230, 19),  # EliteSBarrelLength
    (0x843244, 22),  # EliteSecondaryFireFLH
    (0x84325C, 22),  # ElitePBarrelThickness
    (0x843274, 19),  # ElitePBarrelLength
    (0x843288, 20),  # ElitePrimaryFireFLH
    (0x84329C, 17),  # SBarrelThickness
    (0x8432B0, 14),  # SBarrelLength
    (0x8432C0, 17),  # SecondaryFireFLH
    (0x8432D4, 17),  # PBarrelThickness
    (0x8432E8, 14),  # PBarrelLength
    (0x8432F8, 15),  # PrimaryFireFLH
    (0x843308, 15),  # %sTurretLocked
    (0x843318, 18),  # %sBarrelThickness
    (0x84332C, 15),  # %sBarrelLength
    (0x84333C, 6),  # %sFLH
    (0x843344, 9),  # AltCameo
    (0x843350, 6),  # Cameo
    (0x843358, 19),  # DisableShadowCache
    (0x84336C, 18),  # DisableVoxelCache
    (0x843380, 12),  # ShadowIndex
    (0x84338C, 12),  # VisibleLoad
    (0x843398, 10),  # Remapable
    (0x8433A4, 9),  # RotCount
    (0x8433B0, 13),  # TurretOffset
    (0x843408, 10),  # UseBuffer
    (0x843414, 22),  # IsSelectableCombatant
    (0x84342C, 19),  # SpecialThreatValue
    (0x843440, 26),  # TargetDistanceCoefficient
    (0x84345C, 26),  # TargetStrengthCoefficient
    (0x843478, 31),  # TargetSpecialThreatCoefficient
    (0x843498, 31),  # TargetEffectivenessCoefficient
    (0x8434B8, 27),  # MyEffectivenessCoefficient
    (0x8434D4, 15),  # EliteAbilities
    (0x8434E4, 17),  # VeteranAbilities
    (0x8434F8, 13),  # ZFudgeBridge
    (0x843508, 13),  # ZFudgeTunnel
    (0x843518, 13),  # ZFudgeColumn
    (0x843528, 12),  # ZFudgeCliff
    (0x843540, 17),  # TiltsWhenCrushes
    (0x843604, 25),  # AttackCursorOnFriendlies
    (0x843620, 17),  # AttackFriendlies
    (0x843634, 10),  # Crashable
    (0x843640, 8),  # JumpJet
    (0x843648, 17),  # JumpjetDeviation
    (0x84365C, 17),  # JumpjetNoWobbles
    (0x843670, 15),  # JumpjetWobbles
    (0x843680, 13),  # JumpjetAccel
    (0x843690, 14),  # JumpjetHeight
    (0x8436A0, 13),  # JumpjetCrash
    (0x8436B0, 13),  # JumpjetClimb
    (0x8436C0, 13),  # JumpjetSpeed
    (0x8436D0, 16),  # JumpjetTurnRate
    (0x8436E0, 9),  # NoShadow
    (0x8436EC, 21),  # SuppressionThreshold
    (0x843704, 15),  # ImmuneToPoison
    (0x843714, 8),  # Organic
    (0x84371C, 11),  # Bunkerable
    (0x843728, 19),  # ConsideredAircraft
    (0x84373C, 23),  # ImmuneToPsionicWeapons
    (0x843754, 17),  # ImmuneToPsionics
    (0x843768, 13),  # Parasiteable
    (0x843778, 9),  # Warpable
    (0x843784, 19),  # DefaultToGuardArea
    (0x843798, 13),  # MissileSpawn
    (0x8437A8, 16),  # SpawnReloadRate
    (0x8437B8, 13),  # SpawnsNumber
    (0x8437C8, 15),  # SpawnRegenRate
    (0x8437D8, 8),  # Spawned
    (0x8437E0, 20),  # OpenTransportWeapon
    (0x8437F4, 16),  # SlaveReloadRate
    (0x843804, 13),  # SlavesNumber
    (0x843814, 15),  # SlaveRegenRate
    (0x843830, 7),  # Slaved
    (0x843838, 13),  # BalloonHover
    (0x843848, 11),  # Underwater
    (0x843854, 18),  # ImmuneToRadiation
    (0x843868, 19),  # OmniCrushResistant
    (0x84387C, 12),  # OmniCrusher
    (0x843888, 13),  # HunterSeeker
    (0x843898, 12),  # TargetLaser
    (0x8438A4, 11),  # StupidHunt
    (0x8438B0, 28),  # AllowedToStartInMultiplayer
    (0x8438CC, 14),  # ImmuneToVeins
    (0x8438DC, 10),  # ToProtect
    (0x8438E8, 12),  # Disableable
    (0x8438F4, 14),  # UndeployDelay
    (0x843904, 11),  # DeployTime
    (0x843910, 10),  # FireAngle
    (0x84391C, 11),  # NoAutoFire
    (0x843928, 12),  # SelfHealing
    (0x843934, 13),  # RadarVisible
    (0x843944, 10),  # Invisible
    (0x843950, 11),  # Repairable
    (0x843980, 19),  # AIBasePlanningSide
    (0x843994, 6),  # Owner
    (0x84399C, 12),  # ThreatPosed
    (0x8439A8, 7),  # Points
    (0x8439B0, 18),  # PreventAttackMove
    (0x8439C4, 11),  # CloseRange
    (0x8439D0, 10),  # Unnatural
    (0x8439DC, 8),  # Natural
    (0x8439E4, 6),  # Pushy
    (0x8439EC, 12),  # SprayAttack
    (0x8439F8, 16),  # BerserkFriendly
    (0x843A08, 29),  # ReadinessReductionMultiplier
    (0x843A28, 23),  # DamageReducesReadiness
    (0x843A40, 16),  # ReloadIncrement
    (0x843A50, 12),  # EmptyReload
    (0x843A5C, 7),  # Reload
    (0x843A64, 16),  # DistributedFire
    (0x843A74, 16),  # OpportunityFire
    (0x843A84, 11),  # MobileFire
    (0x843A90, 13),  # DeployToLand
    (0x843AA0, 11),  # DeployFire
    (0x843AAC, 17),  # DeployFireWeapon
    (0x843AC0, 19),  # RadialFireSegments
    (0x843AD4, 14),  # AirRangeBonus
    (0x843AF8, 15),  # UnloadingClass
    (0x843B08, 8),  # Soylent
    (0x843B10, 27),  # EliteAirstrikeRechargeTime
    (0x843B2C, 22),  # AirstrikeRechargeTime
    (0x843B44, 23),  # EliteAirstrikeTeamType
    (0x843B5C, 18),  # AirstrikeTeamType
    (0x843B94, 16),  # ForbiddenHouses
    (0x843BA4, 13),  # SecretHouses
    (0x843BB4, 15),  # RequiredHouses
    (0x843BC4, 25),  # RequiresStolenAlliedTech
    (0x843BE0, 25),  # RequiresStolenSovietTech
    (0x843BFC, 24),  # RequiresStolenThirdTech
    (0x843C14, 24),  # CanRecalcApproachTarget
    (0x843C2C, 18),  # CanApproachTarget
    (0x843C40, 13),  # CanRetaliate
    (0x843C50, 17),  # CanPassiveAquire
    (0x843C64, 18),  # DisguiseWhenStill
    (0x843C78, 15),  # DetectDisguise
    (0x843CA4, 20),  # ResourceDestination
    (0x843CB8, 17),  # ResourceGatherer
    (0x843CCC, 11),  # OpenTopped
    (0x843CD8, 10),  # Drainable
    (0x843CE4, 12),  # RevealToAll
    (0x843CF0, 20),  # BuildTimeMultiplier
    (0x843D04, 22),  # MindControlRingOffset
    (0x843D1C, 17),  # LeadershipRating
    (0x843D30, 10),  # BombSight
    (0x843D3C, 20),  # DetectDisguiseRange
    (0x843D50, 13),  # SensorsSight
    (0x843D60, 20),  # RejoinTeamIfLimboed
    (0x843D74, 18),  # ReselectIfLimboed
    (0x843D88, 6),  # Sight
    (0x843D90, 21),  # PrerequisiteOverride
    (0x843DA8, 13),  # Prerequisite
    (0x843DB8, 8),  # PipWrap
    (0x843DC0, 27),  # PixelSelectionBracketDelta
    (0x843DDC, 24),  # LeptonMindControlOffset
    (0x843DF4, 15),  # PipsDrawForAll
    (0x843E04, 9),  # PipScale
    (0x843E10, 13),  # EliteStage%d
    (0x843E20, 8),  # Stage%d
    (0x843E28, 9),  # RateDown
    (0x843E34, 7),  # RateUp
    (0x843E3C, 13),  # WeaponStages
    (0x843E4C, 11),  # IsGattling
    (0x843E58, 8),  # Sensors
    (0x843E60, 11),  # Teleporter
    (0x843E6C, 22),  # SuperGapRadiusInCells
    (0x843E84, 17),  # GapRadiusInCells
    (0x843E98, 13),  # GapGenerator
    (0x843EB4, 11),  # DamageSelf
    (0x843EC0, 10),  # DontScore
    (0x843ECC, 8),  # Nominal
    (0x843ED4, 24),  # RefinerySmokeOffsetFour
    (0x843EEC, 25),  # RefinerySmokeOffsetThree
    (0x843F08, 23),  # RefinerySmokeOffsetTwo
    (0x843F20, 23),  # RefinerySmokeOffsetOne
    (0x843F38, 19),  # DestroySmokeOffset
    (0x843F4C, 17),  # DamSmkOffScrnRel
    (0x843F60, 18),  # DamageSmokeOffset
    (0x843F74, 23),  # DestroyParticleSystems
    (0x843F8C, 22),  # DamageParticleSystems
    (0x843FA4, 24),  # NaturalParticleLocation
    (0x843FBC, 28),  # RefinerySmokeParticleSystem
    (0x843FD8, 22),  # NaturalParticleSystem
    (0x843FF0, 12),  # DestroyAnim
    (0x843FFC, 14),  # VoiceUndeploy
    (0x84400C, 12),  # VoiceDeploy
    (0x844018, 32),  # VoiceSecondaryEliteWeaponAttack
    (0x844038, 27),  # VoiceSecondaryWeaponAttack
    (0x844054, 30),  # VoicePrimaryEliteWeaponAttack
    (0x844074, 25),  # VoicePrimaryWeaponAttack
    (0x844090, 13),  # VoiceHarvest
    (0x8440A0, 14),  # UndeploySound
    (0x8440B0, 12),  # DeploySound
    (0x8440BC, 9),  # DieSound
    (0x8440C8, 10),  # MoveSound
    (0x8440D4, 20),  # LeaveTransportSound
    (0x8440E8, 20),  # EnterTransportSound
    (0x8440FC, 18),  # TurretRotateSound
    (0x844110, 7),  # Turret
    (0x844118, 17),  # TiltCrashJumpjet
    (0x84412C, 12),  # TurretSpins
    (0x844138, 13),  # ManualReload
    (0x844148, 13),  # LightningRod
    (0x844158, 12),  # PoweredUnit
    (0x844164, 11),  # PowersUnit
    (0x844170, 14),  # UndeploysInto
    (0x844180, 12),  # DeploysInto
    (0x84418C, 5),  # Dock
    (0x844194, 9),  # Category
    (0x8441A0, 11),  # BuildLimit
    (0x8441AC, 8),  # Storage
    (0x8441B4, 10),  # CloakStop
    (0x8441C0, 13),  # VoiceCapture
    (0x8441D0, 11),  # VoiceEnter
    (0x8441DC, 13),  # VoiceSinking
    (0x8441EC, 14),  # VoiceCrashing
    (0x8441FC, 13),  # VoiceFalling
    (0x84420C, 14),  # CrashingSound
    (0x84421C, 12),  # DamageSound
    (0x844228, 12),  # CreateSound
    (0x844234, 10),  # AuxSound2
    (0x844240, 10),  # AuxSound1
    (0x84424C, 14),  # VoiceFeedback
    (0x84425C, 9),  # VoiceDie
    (0x844268, 19),  # VoiceSpecialAttack
    (0x84427C, 12),  # VoiceAttack
    (0x844288, 23),  # VoiceSelectDeactivated
    (0x8442A0, 20),  # VoiceSelectEnslaved
    (0x8442B4, 12),  # VoiceSelect
    (0x8442C0, 10),  # VoiceMove
    (0x8442CC, 15),  # EliteSecondary
    (0x8442DC, 13),  # ElitePrimary
    (0x8442EC, 10),  # Secondary
    (0x8442F8, 8),  # Primary
    (0x844354, 18),  # HasTurretTooltips
    (0x844368, 12),  # DebrisAnims
    (0x844374, 15),  # DebrisMaximums
    (0x844384, 12),  # DebrisTypes
    (0x844390, 10),  # MinDebris
    (0x84439C, 10),  # MaxDebris
    (0x8443A8, 8),  # VHPScan
    (0x8443B0, 12),  # HoverAttack
    (0x8443BC, 10),  # SizeLimit
    (0x8443C8, 13),  # PhysicalSize
    (0x8443D8, 7),  # Weight
    (0x844420, 27),  # ThreatAvoidanceCoefficient
    (0x84443C, 14),  # CloakingSpeed
    (0x844458, 11),  # PitchSpeed
    (0x844464, 10),  # RollAngle
    (0x844470, 11),  # PitchAngle
    (0x84447C, 11),  # IsDropship
    (0x844488, 26),  # DeathWeaponDamageModifier
    (0x8444A4, 11),  # GuardRange
    (0x8444B0, 12),  # DoubleOwned
    (0x8444BC, 8),  # IsTrain
    (0x8444C4, 13),  # MoveToShroud
    (0x8444D4, 9),  # IdleRate
    (0x8444E0, 9),  # WalkRate
    (0x8444EC, 11),  # TypeImmune
    (0x8444F8, 12),  # CanBeHidden
    (0x844510, 15),  # NavalTargeting
    (0x844520, 14),  # LandTargeting
    (0x844608, 19),  # SnowOccupationBits
    (0x84461C, 24),  # TemperateOccupationBits
    (0x844634, 21),  # AnimationProbability
    (0x84464C, 14),  # AnimationRate
    (0x84465C, 11),  # IsAnimated
    (0x844668, 12),  # IsFlammable
    (0x844674, 15),  # SpawnsTiberium
    (0x844684, 11),  # IsVeinhole
    (0x845C94, 9),  # AltImage
    (0x845CA0, 13),  # BurstDelay%d
    (0x845CB0, 18),  # FiringSyncFrame%d
    (0x845CC4, 16),  # MaxDeathCounter
    (0x845CD4, 16),  # StartDeathFrame
    (0x845CE4, 17),  # StartFiringFrame
    (0x845CF8, 15),  # StartWalkFrame
    (0x845D08, 16),  # StartStandFrame
    (0x845D18, 8),  # Facings
    (0x845D20, 15),  # DeathFrameRate
    (0x845D30, 12),  # DeathFrames
    (0x845D3C, 15),  # StandingFrames
    (0x845D4C, 11),  # NonVehicle
    (0x845D58, 9),  # CanBeach
    (0x845D64, 21),  # MovementRestrictedTo
    (0x845D7C, 8),  # Passive
    (0x845D84, 13),  # FiringFrames
    (0x845D94, 11),  # WalkFrames
    (0x845DA0, 16),  # UseTurretShadow
    (0x845DB0, 24),  # HalfDamageSmokeLocation
    (0x845DC8, 23),  # TooBigToFitUnderBridge
    (0x845DE0, 13),  # CarriesCrate
    (0x845DF0, 9),  # IsTilter
    (0x845DFC, 17),  # IsSimpleDeployer
    (0x845E10, 13),  # DeployToFire
    (0x845E20, 12),  # CrateGoodie
    (0x845E94, 12),  # ShareSource
    (0x845EA0, 15),  # AttachedSystem
    (0x845EB0, 11),  # VoxelIndex
    (0x845EBC, 16),  # ShareBarrelData
    (0x845ECC, 16),  # ShareTurretData
    (0x845EDC, 14),  # ShareBodyData
    (0x845EEC, 8),  # MaxZVel
    (0x845EF4, 9),  # Duration
    (0x845F00, 19),  # MaxAngularVelocity
    (0x845F14, 19),  # MinAngularVelocity
    (0x8463B8, 72),  # Warhead affect-type18 names
    (0x846400, 8),  # CRUSHER
    (0x846408, 11),  # GUARD_AREA
    (0x846414, 14),  # TIBERIUM_HEAL
    (0x846424, 9),  # FEARLESS
    (0x846430, 8),  # SENSORS
    (0x846438, 16),  # RADAR_INVISIBLE
    (0x846448, 9),  # EXPLODES
    (0x846454, 10),  # SELF_HEAL
    (0x846460, 11),  # VEIN_PROOF
    (0x84646C, 15),  # TIBERIUM_PROOF
    (0x84647C, 6),  # CLOAK
    (0x846484, 6),  # SIGHT
    (0x84648C, 10),  # FIREPOWER
    (0x846498, 9),  # STRONGER
    (0x8464A4, 7),  # FASTER
    (0x847C38, 7),  # Verses
    (0x847C40, 66),  # 100%%,100%%,100%%,100%%,100%%,100%%,100%%,100%%,100%%,100%%,100%%
    (0x847C84, 9),  # ShakeYhi
    (0x847C90, 9),  # ShakeYlo
    (0x847C9C, 9),  # ShakeXhi
    (0x847CA8, 9),  # ShakeXlo
    (0x847CB4, 9),  # Veinhole
    (0x847CC0, 8),  # Bullets
    (0x847CC8, 14),  # AffectsAllies
    (0x847CD8, 14),  # PsychicDamage
    (0x847CE8, 12),  # ProneDamage
    (0x847CF4, 10),  # NukeMaker
    (0x847D00, 14),  # MakesDisguise
    (0x847D10, 8),  # Culling
    (0x847D18, 10),  # Paralyzes
    (0x847D24, 11),  # BombDisarm
    (0x847D30, 12),  # Psychedelic
    (0x847D3C, 12),  # IsLocomotor
    (0x847D48, 16),  # ElectricAssault
    (0x847D58, 7),  # Poison
    (0x847D60, 9),  # EMEffect
    (0x847D6C, 17),  # DeformThreshhold
    (0x847D80, 7),  # Deform
    (0x847D88, 9),  # InfDeath
    (0x847D94, 9),  # AnimList
    (0x847DA0, 14),  # CLDisableBlue
    (0x847DB0, 15),  # CLDisableGreen
    (0x847DC0, 13),  # CLDisableRed
    (0x847DD0, 7),  # Bright
    (0x847DD8, 13),  # DirectRocker
    (0x847DE8, 7),  # Rocker
    (0x847DF0, 6),  # Sonic
    (0x847DF8, 7),  # Sparky
    (0x847E00, 5),  # Wood
    (0x847E08, 17),  # PenetratesBunker
    (0x847E1C, 22),  # WallAbsoluteDestroyer
    (0x847E34, 13),  # Conventional
    (0x847E44, 16),  # CombatLightSize
    (0x847E54, 15),  # DelayKillAtMax
    (0x847E64, 16),  # DelayKillFrames
    (0x847E74, 16),  # CausesDelayKill
    (0x847E84, 13),  # PercentAtMax
    (0x847E94, 10),  # CellInset
    (0x847EA0, 11),  # CellSpread
    (0x849268, 11),  # Projectile
    (0x849274, 23),  # AttachedParticleSystem
    (0x84928C, 10),  # IsMagBeam
    (0x849298, 9),  # RadLevel
    (0x8492A4, 14),  # IsRadEruption
    (0x8492B4, 10),  # IsRadBeam
    (0x8492C0, 17),  # IsAlternateColor
    (0x8492D4, 16),  # DrawBoltAsLaser
    (0x8492E4, 15),  # IsElectricBolt
    (0x8492F4, 9),  # AreaFire
    (0x849300, 13),  # IonSensitive
    (0x849310, 11),  # IsBigLaser
    (0x84931C, 14),  # LaserDuration
    (0x84932C, 17),  # LaserOuterSpread
    (0x849340, 16),  # LaserOuterColor
    (0x849350, 16),  # LaserInnerColor
    (0x849360, 7),  # Lobber
    (0x849368, 10),  # IsRailgun
    (0x849374, 22),  # DistributedWeaponFire
    (0x84938C, 9),  # OmniFire
    (0x849398, 18),  # UseSparkParticles
    (0x8493AC, 17),  # UseFireParticles
    (0x8493C0, 8),  # Charges
    (0x8493C8, 13),  # IsHouseColor
    (0x8493D8, 7),  # IsLine
    (0x8493E0, 8),  # IsLaser
    (0x8493E8, 7),  # Camera
    (0x8493F0, 15),  # OpenToppedAnim
    (0x849400, 13),  # OccupantAnim
    (0x849410, 12),  # AssaultAnim
    (0x84941C, 11),  # DownReport
    (0x849428, 13),  # MinimumRange
    (0x849438, 6),  # Burst
    (0x849440, 8),  # Supress
    (0x849448, 22),  # DisguiseFakeBlinkTime
    (0x849460, 16),  # FireInTransport
    (0x849470, 12),  # DrainWeapon
    (0x84947C, 16),  # FireWhileMoving
    (0x84948C, 20),  # InfiniteMindControl
    (0x8494A0, 17),  # DisguiseFireOnly
    (0x8494B4, 16),  # MigAttackCursor
    (0x8494C4, 15),  # SabotageCursor
    (0x8494D4, 12),  # TerrainFire
    (0x8494E0, 13),  # RevealOnFire
    (0x8494F0, 9),  # NeverUse
    (0x8494FC, 9),  # FireOnce
    (0x849508, 17),  # CellRangefinding
    (0x84951C, 14),  # DecloakToFire
    (0x84952C, 12),  # LimboLaunch
    (0x849538, 8),  # Spawner
    (0x849540, 8),  # IsSonic
    (0x849548, 14),  # AmbientDamage
)

# Original Bullet callback4E75E0 owns this24-byte header before Scenario.
# Guest writes only; there are no newly authorized fixture writes.
LIVE_NATIVE_DATA = ((0xA83C80, 24),)

LIVE_READERS = (
    dict(family='Country', entry=0x511850, caller=0x679A30, callsite=0x679A2D, vtable=0x7EAB58, vtable_slot=0x7EABBC, memberbytes=0x1B0, registry=0xA83C98, ctor=0x5113F0),
    dict(family='SuperWeapon', entry=0x6CEA20, caller=0x679A53, callsite=0x679A50, vtable=0x7F4090, vtable_slot=0x7F40F4, memberbytes=0x100, registry=0xA8E330, ctor=0x6CE5B0),
    dict(family='Anim', entry=0x427D00, caller=0x679A7A, callsite=0x679A77, vtable=0x7E3608, vtable_slot=0x7E366C, memberbytes=0x378, registry=0x8B4150, ctor=0x427530),
    dict(family='Building', entry=0x45FE50, caller=0x679A9D, callsite=0x679A9A, vtable=0x7E4570, vtable_slot=0x7E45D4, memberbytes=0x1798, registry=0xA83C68, ctor=0x45DD90),
    dict(family='Aircraft', entry=0x41CC20, caller=0x679AC0, callsite=0x679ABD, vtable=0x7E2868, vtable_slot=0x7E28CC, memberbytes=0xE10, registry=0xA8B218, ctor=0x41C8B0),
    dict(family='Unit', entry=0x747620, caller=0x679AE3, callsite=0x679AE0, vtable=0x7F6218, vtable_slot=0x7F627C, memberbytes=0xE78, registry=0xA83CE0, ctor=0x7470D0),
    dict(family='Infantry', entry=0x5240A0, caller=0x679B06, callsite=0x679B03, vtable=0x7EB610, vtable_slot=0x7EB674, memberbytes=0xED0, registry=0xA8E348, ctor=0x5236A0),
    dict(family='Weapon', entry=0x772080, caller=0x679B29, callsite=0x679B26, vtable=0x7F73B8, vtable_slot=0x7F741C, memberbytes=0x160, registry=0x887568, ctor=0x771C70),
    dict(family='Bullet', entry=0x46BEE0, caller=0x679B4C, callsite=0x679B49, vtable=0x7E4948, vtable_slot=0x7E49AC, memberbytes=0x2F8, registry=0xA83C80, ctor=0x46BBC0),
    dict(family='Warhead', entry=0x75D3A0, caller=0x679B6F, callsite=0x679B6C, vtable=0x7F6B30, vtable_slot=0x7F6B94, memberbytes=0x1D0, registry=0x8874C0, ctor=0x75CEC0),
    dict(family='Terrain', entry=0x71DEA0, caller=0x679BD8, callsite=0x679BD5, vtable=0x7F5458, vtable_slot=0x7F54BC, memberbytes=0x2BC, registry=0xA8E318, ctor=0x71DA80),
    dict(family='Smudge', entry=0x6B56D0, caller=0x679BFC, callsite=0x679BF9, vtable=0x7F3528, vtable_slot=0x7F358C, memberbytes=0x2A4, registry=0xA8EC18, ctor=0x6B5260),
    dict(family='Overlay', entry=0x5FE770, caller=0x679C1F, callsite=0x679C1C, vtable=0x7EF600, vtable_slot=0x7EF664, memberbytes=0x2BC, registry=0xA83D80, ctor=0x5FE250),
    dict(family='Particle', entry=0x644F50, caller=0x679C42, callsite=0x679C3F, vtable=0x7F0188, vtable_slot=0x7F01EC, memberbytes=0x318, registry=0xA83D98, ctor=0x644BE0),
    dict(family='ParticleSystem', entry=0x6442D0, caller=0x679C65, callsite=0x679C62, vtable=0x7F00A8, vtable_slot=0x7F010C, memberbytes=0x310, registry=0xA83D68, ctor=0x6440A0),
    dict(family='VoxelAnim', entry=0x74B050, caller=0x679C88, callsite=0x679C85, vtable=0x7F6548, vtable_slot=0x7F65AC, memberbytes=0x308, registry=0xA8EB28, ctor=0x74AD80),
)

LIVE_POSTPASSES = (("Weapon", 0x7729F0, 0x679B91), ("Building", 0x465CB0, 0x679BB4))
LIVE_MISSION = dict(entry=0x5B3760, caller=0x679CA3, callsite=0x679C9E, first=0xA8E3A8, stride=32, count=32)
