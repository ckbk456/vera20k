"""Reviewed Steam Rules prerequisites for retained Process668EC5..668EED.

Original Steam gamemd SHA2563e81a61775d2745d1dabe397325ef663cd994ffc194da4e998e3bf5d2d308600.
Static evidence: rules-prereaders-20261006/prereaders-enrollment.static.json
and its rooted caller/helper packets under .local/fv-movement-validation.
These are declarations, not a profile, runtime discovery or execution receipt.
General66D530 has its separate closure; Land674000 is already inherited.

Rules665650 initializes the retained Building vectors with7ED90C and the
Int vector at+9A8 with7E4DD8. Their resize/clear slots select50EA90/50E4A0
and477E10/477840. Temporary7EAA08 clear selects50EA00;7E4DB8 clear selects
477D20. Existing allocator7C8E17/delete7C8B3D sinks remain the only services.
Generic base resize50E950/477C70 and non-C-locale branches are not enrolled.

Powerups arrays preserve file-backed defaults at81DA8C/81DAD8. Initial
zeroes at89EC28/89ECC0 belong to the existing supplied fresh-loader BSS
boundary; this module establishes no original CRT initialization proof.
Native data grants below do not authorize fixture writes or retained resets.
"""

# Full rooted reader ranges include their absent-section return tails.
PREREADER_REGIONS = (
    (0x668EC5, 0x668EED, '26e0a80ecc4ecaa3384fadaba3fc9b0bb4a1b723006e309457b1d583f16453b1'),
    (0x672AE0, 0x673E77, '76cf0af130a1306793f627a51b1a7423da434ea398f2ffd6761bb822611fcb73'),
    (0x673E80, 0x673FF6, '16afa900a9dee497ea4acbe79891e32bc6bac87d6f32a5d3a535bd6f260b2439'),
    (0x674240, 0x6743CD, 'a05e260b1f18fb090c4e672d14c1cc5fa6e15fa57eff4908c6d2f4be9788d362'),
    # AI vector copies, temporary construction, assignment and append.
    (0x4779E0, 0x477A68, 'b4705fb74e72e29307de9c7a9277c0f0e948fdf8f3ce0be40c37c9939fc5efa5'),
    (0x50EA00, 0x50EA27, '702da33d4a119766cd5059aba9f71eca2739b14fcf93b004f646f2dcd44b2859'),
    (0x50EA90, 0x50EB40, '6cf3f6190bc51eec098b419eb9681e0576bb6b8e00dd151b175b1dec0c143ca8'),
    (0x5AC400, 0x5AC422, '62f1947b049e2edb1620406cbe216fe3dd3246befdc32c72592439500fff75ff'),
    (0x5AC430, 0x5AC4B4, '08e01f650f356ff67d04da4b07f2f8eb860cf5cd916bf752ceb9b75ea7766f81'),
    (0x5AC900, 0x5AC95D, '53ae27c97123fff04565d07131d79ceab0591d01d6394e4fedab5593d9649e3c'),
    (0x5AD660, 0x5AD6E8, '16e41d31bfb6f4308b5b109ce6a1cb3d7d995e35cc4ecae64214621e6b56c129'),
    (0x5AD7D0, 0x5AD820, '30af68b9c6a673326067624c6aebf06e6d7145fa754b7738b9265393be87482f'),
    (0x67A110, 0x67A189, '470772c1582f6d2c88b361d806493c4e990890c69ef4a489952ff20707c08a6c'),
    (0x67A570, 0x67A5F4, 'bb37cdd0ac17454f6f162984d97530130cd25550093097047888c776ba948d19'),
    (0x67B180, 0x67B1EC, 'a724265d92da31900a4102f89f80fbd90722bd006bf924f2a8d50777d431c64c'),
    (0x67B550, 0x67B720, '209e6d92d27aa41e31e9be67a216ab7bdd7e2ef3bf5801bb266f243db675c4f5'),
    # Powerups Anim ordinal and atof wrapper; scanner/conversion inherited.
    (0x422B20, 0x422B73, '708d3598a73761ab224b0d3dcecd71aac7301fbccf117116b6ace517f6503183'),
    (0x7C9D66, 0x7C9DBD, '13f40bbbedea64cf4a8e42dd7105b9f2dcf54065bc7e84f63f4b89248afd2219'),
    (0x7D151E, 0x7D159D, '56594af045de4c48f74574d4e7ea6de0b40e1e81bf33b2eb1b280eaa7d2ed63f'),
)

# Keys/sections are NUL-inclusive byte scopes: REPNE SCASB528A73/52771C
# supplies the exact length to CRC4A1DE0; tokens and ASCII strcmp read bytes.
# Only default0,NONE is an actual strncpy source: aligned load7C9266 can
# read up to3 original bytes afterNUL, so its declaration alone uses len+4.
PREREADER_READ_ONLY = (
    (0x7F0CD4, 12),  # AI, Powerups, IQ section-pointer cells.
    (0x839DA4, 3),   # AI
    (0x839D98, 9),  # Powerups
    (0x824DD8, 3),   # IQ
    (0x7EAA14, 4),   # Temporary BuildingPtr vector clear50EA00.
    (0x7E523C, 76),  # Exactly19 Powerups name pointers.
    (0x7E3808, 8),   # Original percentage multiplier; inherited numeric owner.
    (0x817F70, 2),   # Comma tokenizer delimiter.
    # AI keys, in original literal-address order.
    (0x83D110, 28),  # ComputerBaseDefenseResponse
    (0x83D12C, 24),  # MaximumBaseDefenseValue
    (0x83D144, 26),  # GDIBaseDefenseCoefficient
    (0x83D160, 26),  # NodBaseDefenseCoefficient
    (0x83D17C, 26),  # GDIWallDefenseCoefficient
    (0x83D198, 15),  # GDIWallDefense
    (0x83D1A8, 14),  # AIBaseSpacing
    (0x83D1B8, 15),  # PowerEmergency
    (0x83D1C8, 9),  # Paranoid
    (0x83D1D4, 14),  # CompEasyBonus
    (0x83D1E4, 14),  # AirstripLimit
    (0x83D1F4, 14),  # AirstripRatio
    (0x83D204, 13),  # HelipadLimit
    (0x83D214, 13),  # HelipadRatio
    (0x83D224, 11),  # TeslaLimit
    (0x83D230, 11),  # TeslaRatio
    (0x83D23C, 8),  # AALimit
    (0x83D244, 8),  # AARatio
    (0x83D24C, 13),  # DefenseLimit
    (0x83D25C, 13),  # DefenseRatio
    (0x83D26C, 9),  # WarLimit
    (0x83D278, 9),  # WarRatio
    (0x83D284, 14),  # BarracksLimit
    (0x83D294, 14),  # BarracksRatio
    (0x83D2A4, 14),  # RefineryLimit
    (0x83D2B4, 14),  # RefineryRatio
    (0x83D2C4, 12),  # BaseSizeAdd
    (0x83D2D0, 13),  # PowerSurplus
    (0x83D2E0, 17),  # InfantryBaseMult
    (0x83D2F4, 16),  # InfantryReserve
    (0x83D304, 15),  # AutocreateTime
    (0x83D314, 18),  # BlockagePathDelay
    (0x83D328, 10),  # PathDelay
    (0x83D334, 14),  # CreditReserve
    (0x83D344, 11),  # PatrolScan
    (0x83D350, 12),  # AttackDelay
    (0x83D35C, 15),  # AttackInterval
    (0x83D36C, 21),  # NeutralTechBuildings
    (0x83D384, 11),  # BuildDummy
    (0x83D390, 15),  # BuildNavalYard
    (0x83D3A0, 8),  # EWGates
    (0x83D3A8, 8),  # NSGates
    (0x83D3B0, 14),  # ConcreteWalls
    (0x83D3C0, 11),  # BuildRadar
    (0x83D3CC, 13),  # BuildHelipad
    (0x83D3DC, 8),  # BuildAA
    (0x83D3E4, 14),  # BuildPDefense
    (0x83D3F4, 13),  # BuildDefense
    (0x83D404, 23),  # AIForcePredictionFudge
    (0x83D41C, 18),  # ThirdBaseDefenses
    (0x83D430, 19),  # SovietBaseDefenses
    (0x83D444, 19),  # AlliedBaseDefenses
    (0x83D458, 13),  # BuildWeapons
    (0x83D468, 10),  # BuildTech
    (0x83D474, 14),  # BuildBarracks
    (0x83D484, 14),  # BuildRefinery
    (0x83D494, 11),  # BuildPower
    (0x83D4A0, 11),  # BuildConst
    # Powerups defaults/bool literals and all19 table-selected key names.
    (0x825BF4, 3),   # no
    (0x825BF8, 4),   # yes
    (0x83D4AC, 10),  # 0,NONE; original ReadString default copied by strncpy.
    (0x81DA20, 6),   # Money
    (0x81746C, 5),   # Unit
    (0x81DA14, 9),  # HealBase
    (0x81DA0C, 6),   # Cloak
    (0x81DA00, 10),  # Explosion
    (0x81D9F8, 7),  # Napalm
    (0x81D9F0, 6),   # Squad
    (0x81D9E4, 9),  # Darkness
    (0x81D9DC, 7),  # Reveal
    (0x81D9D4, 6),   # Armor
    (0x81D9CC, 6),   # Speed
    (0x81D9C0, 10),  # Firepower
    (0x81D9B8, 5),   # ICBM
    (0x81D9A8, 16),  # Invulnerability
    (0x81D9A0, 8),  # Veteran
    (0x81D994, 9),  # IonStorm
    (0x81D990, 4),   # Gas
    (0x817278, 9),  # Tiberium
    (0x81D98C, 4),   # Pod
    # IQ keys.
    (0x817460, 9),  # Aircraft
    (0x81BEBC, 10),  # GuardArea
    (0x82C284, 8),  # Scatter
    (0x83B3B4, 12),  # ContentScan
    (0x83D4C0, 9),  # SellBack
    (0x83D4CC, 10),  # Harvester
    (0x83D4D8, 10),  # AutoCrush
    (0x83D4E4, 11),  # RepairSell
    (0x83D4F0, 11),  # Production
    (0x83D4FC, 13),  # SuperWeapons
    (0x83D50C, 12),  # MaxIQLevels
)

# Original Powerups loop673EAC..673FD7 executes19 ordinals. Preserve the
# loaded share counts and FFFFFFFF Anim ordinals; extended values/bools start
# at supplied-loader zero-BSS and are written only by original token branches.
PREREADER_NATIVE_DATA = (
    (0x81DA8C, 19 * 4),  # Shares; native store673F05.
    (0x81DAD8, 19 * 4),  # Anim ordinals; native store673F2F.
    (0x89EC28, 19 * 8),  # Extended values; native store673FCA.
    (0x89ECC0, 19),      # Three-token boolean; stores673F64/673F7F.
)

READER_ENTRIES = (
    ('AI', 0x672AE0),
    ('Powerups', 0x673E80),
    ('Land', 0x674000),
    ('IQ', 0x674240),
    ('General', 0x66D530),
)
