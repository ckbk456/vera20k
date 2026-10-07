"""Reviewed original Steam Rules.Process tail declarations.

Only literal native code and immutable data are enrolled. Difficulty66D270
is inherited from STEAM_HOUSE_RULES_PROFILE, and Tiberium has its existing
physical navigation owner. No runtime discovery, loading, callbacks, fixture
writes, service results or sinks are provided here. See steam_rules_tail_scope.md.
Native SHA256: 3e81a61775d2745d1dabe397325ef663cd994ffc194da4e998e3bf5d2d308600.
"""

from tools.native_oracle import RET_MAGIC

TAIL_REGIONS = (
    # Original retained Rules.Process tail; RET4 at668FA2.
    (0x668EF5, 0x668FA5, "5537f8b52388cfc6568129a91e3c628ca98fc7d3fd96f94910cefdea0f73ba6b"),
    # CrateRules original complete reader.
    (0x66B900, 0x66BBA2, "7f8280472e9c77d4d0777490e06d5f08100ee52dc6db75ce30ce8deb5aec7e02"),
    # CombatDamage original complete reader.
    (0x66BBB0, 0x66CF65, "e043a6fe358bf7496b0cdc8ca7d03b4d1c0307c5bec682948d8ed63c062fbf9d"),
    # Radiation original complete reader.
    (0x66CF70, 0x66D147, "50827b481df96f23b59a86a1ba7b0d221ecfbaf4f3110da9da5247314e49ad88"),
    # ElevationModel original complete reader.
    (0x66D150, 0x66D1EA, "ee5383629c836be724aa369e4206721077139d2105aa4a71e58bb2bb784b67c4"),
    # WallModel original complete reader.
    (0x66D1F0, 0x66D263, "b86b02b17d336dfa154512ae6a5d039f965c14831da5685112826abe518914a2"),
    # AudioVisual original complete reader.
    (0x6691E0, 0x66B900, "9f36f6157d6d14e61d6d6344ff1f4d134dc6b90c3b534f8d82c25b4849aa72fe"),
    # SpecialWeapons original complete reader and Warhead reread loop.
    (0x668FB0, 0x6691D1, "c52ba9ecce95045f441e039f332b38564015ee01fc98ee46cd172412364393eb"),
    # Original command-bar selector and section-existence gate only.
    (0x674650, 0x674688, "20068a8ecd2c6299ff185eefe5bfb9b7444d674d59f7fe332c914a9158242baa"),
    # Original command-bar absent-section RET8; present body excluded.
    (0x67471E, 0x67472B, "30688665e4f4c3ba5ebad8f227872d9db2a176335f524699486598a5b288e0bf"),
    # Crate Powerups-name ReadString wrapper; no host enum.
    (0x4759F0, 0x475A3D, "769d71a3fb5ecdbc5b4e82e670e86cf11eb2efb00b24860b7a04c81928637989"),
    # Powerups nineteen-name parser, fixed end7E5288.
    (0x48DE70, 0x48DEA8, "02d27b9e604e8d33176af9d760fa81ce947531758a0194d1bf23b14872c60e6a"),
    # Combat native pointer-vector assignment; actual receiver VT7F0D1C.
    (0x67AE00, 0x67AE6C, "cd7ceb24a2c0bbf4cfeb250e9035240fd5adb00f56d49bbeb7828fbbabe97c0f"),
    # Combat base vector clear, also exact7F0D88 target.
    (0x67AF60, 0x67AF87, "0a25537b191f668ebd2a94b65a8e6231e4464dac62639799bbbd88eb6f363c40"),
    # Combat temporary native pointer-vector constructor.
    (0x67AFF0, 0x67B04D, "7c21dedb3999566416e48c1299b136f8f60335725c6a435e94c43ff8c870413e"),
    # Combat native pointer append; caller resets VT7F0D1C.
    (0x67B100, 0x67B150, "30af68b9c6a673326067624c6aebf06e6d7145fa754b7738b9265393be87482f"),
    # Actual active VT7F0D1C+8 target read by67B128; original resize RET8.
    (0x67B050, 0x67B100, "aca2300d3257664e92d2cf71e9219966458738f4513ffce495f8c29b9f7d1fa4"),
    # Actual active VT7F0D1C+C target read by67AE0E / zero-size resize.
    (0x67A680, 0x67A6AA, "bb9c92b529fbb405ec08deb96075c355d330e4a4a20493e5a1376122739ff3b7"),
    # Combat native vector copy constructor; returns VT7F0D1C.
    (0x67C280, 0x67C308, "7c52f942f75155a90b932d8b7fb032e95ee4341d6c2971c1a5f8433f66cf2ff8"),
)

# All literal widths include NUL. Keys/section names are native byte-scanned
# sources; every157 direct ReadString default is inherited empty889F64.
# New fixed dispatch words follow the original active receiver and callsites.
TAIL_READ_ONLY = (
    (0x7F0C78, 4),  # SpecialWeapons section pointer
    (0x7F0C7C, 4),  # AudioVisual section pointer
    (0x7F0C80, 4),  # CrateRules section pointer
    (0x7F0C84, 4),  # CombatDamage section pointer
    (0x7F0C88, 4),  # Radiation section pointer
    (0x7F0C8C, 4),  # ElevationModel section pointer
    (0x7F0C90, 4),  # WallModel section pointer
    (0x7F0CE8, 4),  # AdvancedCommandBar section pointer
    (0x7F0CEC, 4),  # MultiplayerAdvancedCommandBar section pointer
    (0x7F0D24, 4),  # Actual VT7F0D1C+8 target67B050; call67B128
    (0x7F0D28, 4),  # Actual VT7F0D1C+C target67A680; call67AE0E/67B0DE
    (0x7F0D88, 4),  # Original base vector+C dispatch to67AF60; call67C2A2
    (0x839D1C, 30),  # MultiplayerAdvancedCommandBar section
    (0x839D3C, 19),  # AdvancedCommandBar section
    (0x839E64, 10),  # WallModel section
    (0x839E70, 15),  # ElevationModel section
    (0x839E8C, 13),  # CombatDamage section
    (0x839E9C, 11),  # CrateRules section
    (0x839EA8, 12),  # AudioVisual section
    (0x839EB4, 15),  # SpecialWeapons section
    (0x83A0DC, 18),  # EMPulseProjectile; 66916F
    (0x83A0F0, 15),  # EMPulseWarhead; 669130
    (0x83A100, 23),  # MutateExplosionWarhead; 6690F2
    (0x83A118, 14),  # MutateWarhead; 6690B3
    (0x83A128, 9),  # NukeDown; 669074
    (0x83A134, 15),  # NukeProjectile; 669036
    (0x83A144, 12),  # NukeWarhead; 668FF7
    (0x83A150, 20),  # FallBackCoefficient; 66B8D5
    (0x83A164, 25),  # DirectRockingCoefficient; 66B8AB
    (0x83A180, 17),  # ForceShieldColor; 66B884
    (0x83A194, 13),  # BerserkColor; 66B864
    (0x83A1A4, 17),  # IronCurtainColor; 66B844
    (0x83A1B8, 17),  # LaserTargetColor; 66B825
    (0x83A1CC, 17),  # OreTwinkleChance; 66B805
    (0x83A1E0, 15),  # MagnaBeamColor; 66B7DE
    (0x83A1F0, 16),  # ChronoBeamColor; 66B7B4
    (0x83A200, 23),  # LineTrailColorOverride; 66B789
    (0x83A218, 16),  # LocalRadarColor; 66B75B
    (0x83A228, 19),  # ExtraAircraftLight; 66B730
    (0x83A23C, 19),  # ExtraInfantryLight; 66B6E7
    (0x83A250, 15),  # ExtraUnitLight; 66B69E
    (0x83A260, 13),  # TimerWarning; 66B660
    (0x83A270, 11),  # SpeakDelay; 66B639
    (0x83A27C, 18),  # AmbientChangeStep; 66B612
    (0x83A290, 18),  # AmbientChangeRate; 66B5EB
    (0x83A2A4, 15),  # IceCrackSounds; 66B577
    (0x83A2B4, 21),  # IceSolidifyFrameTime; 66B543
    (0x83A2CC, 14),  # IceGrowthRate; 66B523
    (0x83A2DC, 15),  # VeinGrowthRate; 66B4FD
    (0x83A2EC, 8),  # FogRate; 66B4D7
    (0x83A2F4, 11),  # ShroudRate; 66B4B1
    (0x83A300, 12),  # SavourDelay; 66B48B
    (0x83A30C, 15),  # NamedCivilians; 66B465
    (0x83A31C, 10),  # MovieTime; 66B446
    (0x83A328, 13),  # MessageDelay; 66B41F
    (0x83A338, 20),  # IdleActionFrequency; 66B3F8
    (0x83A34C, 8),  # Gravity; 66B3D1
    (0x83A354, 12),  # EnemyHealth; 66B3B1
    (0x83A360, 15),  # DropZoneRadius; 66B391
    (0x83A370, 16),  # ConditionYellow; 66B372
    (0x83A380, 13),  # ConditionRed; 66B34B
    (0x83A390, 11),  # AllyReveal; 66B310
    (0x83A39C, 10),  # LargeFire; 66B2DF
    (0x83A3A8, 10),  # SmallFire; 66B2A0
    (0x83A3B4, 16),  # EliteFlashTimer; 66B273
    (0x83A3C4, 7),  # OnFire; 66B0F9
    (0x83A3CC, 9),  # TreeFire; 66AFC8
    (0x83A3D8, 22),  # ShellButtonSlideSound; 66AF8D
    (0x83A3F0, 16),  # LightningSounds; 66AEF7
    (0x83A400, 11),  # StormSound; 66AEBA
    (0x83A40C, 13),  # ScatterSound; 66AE78
    (0x83A41C, 11),  # GuardSound; 66AE37
    (0x83A428, 13),  # BuildingDrop; 66ADB3
    (0x83A438, 12),  # GenericBeep; 66AD72
    (0x83A444, 13),  # GenericClick; 66AD30
    (0x83A454, 11),  # ChuteSound; 66ACEE
    (0x83A460, 20),  # BuildingDamageSound; 66ACAD
    (0x83A474, 9),  # TeslaZap; 66AC6B
    (0x83A480, 12),  # TeslaCharge; 66AC29
    (0x83A48C, 11),  # ScoldSound; 66ABE8
    (0x83A498, 9),  # MovieOff; 66ABA6
    (0x83A4A4, 8),  # MovieOn; 66AB64
    (0x83A4AC, 9),  # RadarOff; 66AB23
    (0x83A4B8, 8),  # RadarOn; 66AAE1
    (0x83A4C0, 13),  # BuildingSlam; 66AA9F
    (0x83A4D0, 17),  # BuildingDieSound; 66AA5E
    (0x83A4E4, 12),  # CreditTicks; 66A9C8
    (0x83A4F0, 13),  # PlayerJoined; 66A949
    (0x83A500, 11),  # PlayerLeft; 66A908
    (0x83A50C, 12),  # GameForming; 66A8C6
    (0x83A518, 15),  # OptionsChanged; 66A884
    (0x83A528, 12),  # SystemError; 66A843
    (0x83A534, 17),  # MessageCharTyped; 66A801
    (0x83A548, 16),  # IncomingMessage; 66A7BF
    (0x83A558, 11),  # GameClosed; 66A77E
    (0x83A564, 10),  # SellSound; 66A73C
    (0x83A570, 11),  # CloakSound; 66A6FA
    (0x83A57C, 12),  # ShakeScreen; 66A6CD
    (0x83A588, 17),  # ScrollMultiplier; 66A6AD
    (0x83A59C, 11),  # ShroudGrow; 66A686
    (0x83A5A8, 9),  # GateDown; 66A652
    (0x83A5B4, 7),  # GateUp; 66A611
    (0x83A5BC, 16),  # AtmosphereEntry; 66A5D2
    (0x83A5CC, 4),  # Dig; 66A593
    (0x83A5D0, 24),  # SpySatDeactivationSound; 66A552
    (0x83A5E8, 22),  # SpySatActivationSound; 66A510
    (0x83A600, 25),  # PsychicSensorDetectSound; 66A4CE
    (0x83A61C, 18),  # IFVTransformSound; 66A48D
    (0x83A630, 20),  # CreateAircraftSound; 66A44B
    (0x83A644, 20),  # CreateInfantrySound; 66A409
    (0x83A658, 21),  # SpyPlaneCameraFrames; 66A39A
    (0x83A670, 18),  # DiskLaserChargeUp; 66A366
    (0x83A684, 25),  # LetsDoTheTimeWarpInAgain; 66A325
    (0x83A6A0, 26),  # LetsDoTheTimeWarpOutAgain; 66A2E3
    (0x83A6BC, 15),  # SpyPlaneCamera; 66A2A1
    (0x83A758, 21),  # AirstrikeAttackVoice; 66A094
    (0x83A770, 20),  # AirstrikeAbortSound; 66A052
    (0x83A784, 29),  # MasterMindOverloadDeathSound; 66A011
    (0x83A7A4, 27),  # PsychicRevealActivateSound; 669FCF
    (0x83A7C0, 28),  # GeneticMutatorActivateSound; 669F8D
    (0x83A7DC, 30),  # PsychicDominatorActivateSound; 669F4C
    (0x83A7FC, 18),  # RepairBridgeSound; 669F0A
    (0x83A810, 21),  # BunkerWallsDownSound; 669EC8
    (0x83A828, 19),  # BunkerWallsUpSound; 669E87
    (0x83A83C, 24),  # SlaveMinerUndeploySound; 669E45
    (0x83A854, 22),  # SlaveMinerDeploySound; 669E03
    (0x83A86C, 16),  # SlavesFreeSound; 669DC2
    (0x83A87C, 15),  # VoiceIFVRepair; 669D80
    (0x83A88C, 18),  # UpgradeEliteSound; 669D3E
    (0x83A8A0, 20),  # UpgradeVeteranSound; 669CFD
    (0x83A8B4, 21),  # BaseUnderAttackSound; 669CBB
    (0x83A8CC, 22),  # BuildingRepairedSound; 669C79
    (0x83A8E4, 23),  # BuildingAbandonedSound; 669C38
    (0x83A8FC, 24),  # BuildingGarrisonedSound; 669BF6
    (0x83A914, 17),  # PlaceBeaconSound; 669BB4
    (0x83A928, 17),  # ExecutePlanSound; 669B73
    (0x83A93C, 28),  # AddPlanningModeCommandSound; 669B31
    (0x83A958, 21),  # YuriMindControlSound; 669AEF
    (0x83A970, 16),  # BombAttachSound; 669AAE
    (0x83A980, 17),  # BombTickingSound; 669A6C
    (0x83A9E8, 18),  # CratePromoteSound; 6698E2
    (0x83A9FC, 15),  # CrateUnitSound; 6698A0
    (0x83AA0C, 16),  # CrateSpeedSound; 66985F
    (0x83AA1C, 17),  # CrateArmourSound; 66981D
    (0x83AA30, 15),  # CrateFireSound; 6697DB
    (0x83AA40, 17),  # CrateRevealSound; 66979A
    (0x83AA54, 16),  # CrateMoneySound; 669758
    (0x83AA64, 21),  # EndPlanningModeSound; 669716
    (0x83AA7C, 23),  # StartPlanningModeSound; 6696D5
    (0x83AA94, 19),  # DefaultChronoSound; 669693
    (0x83AAA8, 11),  # CheerSound; 669651
    (0x83AAB4, 15),  # ScoreAnimSound; 669610
    (0x83AAC4, 17),  # GUICheckboxSound; 6695CE
    (0x83AAD8, 19),  # GUIComboCloseSound; 66958C
    (0x83AAEC, 18),  # GUIComboOpenSound; 66954B
    (0x83AB00, 15),  # GUIMoveInSound; 669509
    (0x83AB10, 16),  # GUIMoveOutSound; 6694C7
    (0x83AB20, 14),  # GUICloseSound; 669486
    (0x83AB30, 13),  # GUIOpenSound; 669444
    (0x83AB40, 12),  # GUITabSound; 669402
    (0x83AB4C, 14),  # GUIBuildSound; 6693C1
    (0x83AB5C, 19),  # GUIMainButtonSound; 66937F
    (0x83AB70, 9),  # DigSound; 66933D
    (0x83AB7C, 11),  # VeinAttack; 6692FF
    (0x83AB88, 23),  # WaypointAnimationSpeed; 6692D4
    (0x83ABA0, 12),  # DropPodPuff; 6692A9
    (0x83ABAC, 10),  # DeployDir; 66927F
    (0x83ABB8, 8),  # PoseDir; 669262
    (0x83ABC0, 22),  # DetailBufferZoneWidth; 669248
    (0x83ABD8, 24),  # DetailMinFrameRateMovie; 66922F
    (0x83ABF0, 25),  # DetailMinFrameRateNormal; 669216
    (0x83AC0C, 11),  # WaterCrate; 66BB74
    (0x83AC18, 10),  # WoodCrate; 66BB54
    (0x83AC24, 12),  # SilverCrate; 66BB35
    (0x83AC30, 15),  # SoloCrateMoney; 66BB15
    (0x83AC40, 14),  # UnitCrateType; 66BAE4
    (0x83AC50, 11),  # CrateRegen; 66BAB7
    (0x83AC5C, 12),  # CrateRadius; 66BA90
    (0x83AC68, 13),  # CrateMaximum; 66BA70
    (0x83AC78, 13),  # CrateMinimum; 66BA50
    (0x83AC88, 15),  # HealCrateSound; 66BA1D
    (0x83AC98, 14),  # WaterCrateImg; 66B9DE
    (0x83ACA8, 9),  # CrateImg; 66B99F
    (0x83ACB4, 13),  # WoodCrateImg; 66B961
    (0x83ACC4, 8),  # FreeMCV; 66B936
    (0x83ACCC, 15),  # CollapseChance; 66CF3C
    (0x83ACDC, 9),  # Incoming; 66CF1C
    (0x83ACE8, 14),  # TreeTargeting; 66CEFC
    (0x83ACF8, 14),  # PlayerScatter; 66CEDD
    (0x83AD08, 17),  # PlayerReturnFire; 66CEBD
    (0x83AD1C, 16),  # PlayerAutoCrush; 66CE9D
    (0x83AD2C, 18),  # TiberiumExplosive; 66CE7E
    (0x83AD40, 10),  # MinDamage; 66CE5E
    (0x83AD4C, 10),  # MaxDamage; 66CE3E
    (0x83AD58, 14),  # HomingScatter; 66CE1F
    (0x83AD68, 12),  # FireSupress; 66CDFF
    (0x83AD74, 10),  # ExpSpread; 66CDDF
    (0x83AD80, 6),  # Crush; 66CDBB
    (0x83AD88, 8),  # C4Delay; 66CD9A
    (0x83AD90, 15),  # BridgeStrength; 66CD73
    (0x83ADA0, 17),  # BallisticScatter; 66CD53
    (0x83ADB4, 11),  # AtomDamage; 66CD35
    (0x83ADCC, 15),  # BerzerkAllowed; 66CCF0
    (0x83ADDC, 28),  # DefaultRepairParticleSystem; 66CCC2
    (0x83ADF8, 26),  # DefaultTestParticleSystem; 66CC83
    (0x83AE14, 24),  # DefaultFireStreamSystem; 66CC45
    (0x83AE2C, 25),  # DefaultDebrisSmokeSystem; 66CC06
    (0x83AE48, 27),  # DefaultSmallRedSmokeSystem; 66CBC7
    (0x83AE64, 27),  # DefaultLargeRedSmokeSystem; 66CB89
    (0x83AE80, 19),  # DefaultSparkSystem; 66CB4A
    (0x83AE94, 28),  # DefaultSmallGreySmokeSystem; 66CB0B
    (0x83AEB0, 28),  # DefaultLargeGreySmokeSystem; 66CACD
    (0x83AECC, 17),  # IonCannonWarhead; 66CA8E
    (0x83AEE0, 29),  # PermaControlledAnimationType; 66CA4F
    (0x83AF00, 24),  # ControlledAnimationType; 66CA11
    (0x83AF18, 22),  # CurrentStrengthDamage; 66C9E3
    (0x83AF30, 24),  # FallingDamageMultiplier; 66C9C5
    (0x83AF48, 17),  # DrainMoneyAmount; 66C99F
    (0x83AF5C, 21),  # DrainMoneyFrameDelay; 66C97F
    (0x83AF74, 19),  # DrainAnimationType; 66C94F
    (0x83AF88, 28),  # MindControlAttackLineFrames; 66C921
    (0x83AFA4, 15),  # OverloadFrames; 66C8B3
    (0x83AFB4, 15),  # OverloadDamage; 66C839
    (0x83AFC4, 14),  # OverloadCount; 66C7C0
    (0x83AFD4, 23),  # OpenToppedWarpDistance; 66C794
    (0x83AFEC, 21),  # OpenToppedRangeBonus; 66C774
    (0x83B004, 27),  # OpenToppedDamageMultiplier; 66C756
    (0x83B020, 23),  # BunkerWeaponRangeBonus; 66C730
    (0x83B038, 20),  # BunkerROFMultiplier; 66C712
    (0x83B04C, 23),  # BunkerDamageMultiplier; 66C6EC
    (0x83B064, 18),  # OccupyWeaponRange; 66C6C7
    (0x83B078, 20),  # OccupyROFMultiplier; 66C6A9
    (0x83B08C, 23),  # OccupyDamageMultiplier; 66C682
    (0x83B0A4, 20),  # PsychicRevealRadius; 66C65D
    (0x83B0B8, 20),  # IronCurtainDuration; 66C63E
    (0x83B0CC, 20),  # IvanIconFlickerRate; 66C61E
    (0x83B0E0, 13),  # CHRONOSK.SHP; 66C5FB
    (0x83B0F0, 13),  # BOMBCURS.SHP; 66C5E9
    (0x83B100, 15),  # IvanTimedDelay; 66C5DA
    (0x83B110, 11),  # IvanDamage; 66C5BB
    (0x83B128, 21),  # CanDetonateDeathBomb; 66C55C
    (0x83B140, 20),  # CanDetonateTimeBomb; 66C53D
    (0x83B154, 12),  # IvanWarhead; 66C50C
    (0x83B160, 18),  # CMislEliteWarhead; 66C4CD
    (0x83B174, 13),  # CMislWarhead; 66C497
    (0x83B184, 18),  # DMislEliteWarhead; 66C458
    (0x83B198, 15),  # V3EliteWarhead; 66C419
    (0x83B1A8, 13),  # DMislWarhead; 66C3DB
    (0x83B1B8, 10),  # V3Warhead; 66C39C
    (0x83B1C4, 13),  # CrushWarhead; 66C35D
    (0x83B1D4, 10),  # C4Warhead; 66C31F
    (0x83B1E0, 13),  # FlameDamage2; 66C2E0
    (0x83B1F0, 12),  # FlameDamage; 66C2A1
    (0x83B1FC, 11),  # SplashList; 66C199
    (0x83B208, 10),  # Scorches4; 66C096
    (0x83B214, 10),  # Scorches3; 66BF93
    (0x83B220, 10),  # Scorches2; 66BE91
    (0x83B22C, 10),  # Scorches1; 66BD8E
    (0x83B238, 9),  # Scorches; 66BC8B
    (0x83B244, 17),  # TiberiumStrength; 66BC64
    (0x83B258, 24),  # TiberiumExplosionDamage; 66BC44
    (0x83B270, 20),  # RailgunDamageRadius; 66BC24
    (0x83B284, 16),  # IonCannonDamage; 66BC05
    (0x83B294, 16),  # AmmoCrateDamage; 66BBE8
    (0x83B2A4, 15),  # RadSiteWarhead; 66D0F6
    (0x83B2B4, 9),  # RadColor; 66D0BD
    (0x83B2C0, 14),  # RadTintFactor; 66D09D
    (0x83B2D0, 15),  # RadLightFactor; 66D076
    (0x83B2E0, 15),  # RadLevelFactor; 66D04F
    (0x83B2F0, 14),  # RadLightDelay; 66D028
    (0x83B300, 14),  # RadLevelDelay; 66D008
    (0x83B310, 12),  # RadLevelMax; 66CFE8
    (0x83B31C, 20),  # RadApplicationDelay; 66CFC9
    (0x83B330, 20),  # RadDurationMultiple; 66CFA9
    (0x83B344, 18),  # ElevationBonusCap; 66D1C9
    (0x83B358, 24),  # ElevationIncrementBonus; 66D1A2
    (0x83B370, 19),  # ElevationIncrement; 66D17B
    (0x83B384, 24),  # WallPenetratorThreshold; 66D242
    (0x83B39C, 23),  # AlliedWallTransparency; 66D21B
)

# Retained Rules allocation, mode, registries, vectors and heap mutations
# remain under their existing owners; this tail adds no mutable global scope.
TAIL_NATIVE_DATA = ()

# Runtime selects each difficulty row by its actual original return caller.
TAIL_READERS = (
    dict(name='Easy', entry=0x66D270, physicalsection='Easy', caller=0x668F07),
    dict(name='Normal', entry=0x66D270, physicalsection='Normal', caller=0x668F19),
    dict(name='Difficult', entry=0x66D270, physicalsection='Difficult', caller=0x668F2B),
    dict(name='CrateRules', entry=0x66B900, physicalsection='CrateRules', caller=0x668F33),
    dict(name='CombatDamage', entry=0x66BBB0, physicalsection='CombatDamage', caller=0x668F3B),
    dict(name='Radiation', entry=0x66CF70, physicalsection='Radiation', caller=0x668F43),
    dict(name='ElevationModel', entry=0x66D150, physicalsection='ElevationModel', caller=0x668F4B),
    dict(name='WallModel', entry=0x66D1F0, physicalsection='WallModel', caller=0x668F53),
    dict(name='AudioVisual', entry=0x6691E0, physicalsection='AudioVisual', caller=0x668F5B),
    dict(name='SpecialWeapons', entry=0x668FB0, physicalsection='SpecialWeapons', caller=0x668F63),
    # Caller metadata only; original code/entry belongs to the physical owner.
    dict(name='Tiberiums', entry=0x721D10, physicalsection='Tiberiums', caller=0x668F6A),
    dict(name='AdvancedCommandBar', entry=0x674650, physicalsection='AdvancedCommandBar', caller=0x668F9B),
)

# Replace the historical668EF5 ->668F2B entry in the NEW profile only.
TAIL_ENTRIES = (
    (0x668EF5, (RET_MAGIC,)),
    (0x66D270, (RET_MAGIC,)),
    (0x66B900, (RET_MAGIC,)),
    (0x66BBB0, (RET_MAGIC,)),
    (0x66CF70, (RET_MAGIC,)),
    (0x66D150, (RET_MAGIC,)),
    (0x66D1F0, (RET_MAGIC,)),
    (0x6691E0, (RET_MAGIC,)),
    (0x668FB0, (RET_MAGIC,)),
    (0x674650, (RET_MAGIC,)),
)

# Exact immutable spans pinned independently of the executable identity.
TAIL_DATA_SHA256 = {
    (0x7F0C78, 4): "3f461661868d584073dbdf16ed9f7ecb57e5705411c5a41c82cbf3cee31e9c20",
    (0x7F0C7C, 4): "f63abbb87b839f31dd76a8b176243e49a9ba65d21a5f1e043a0d8ef908802de5",
    (0x7F0C80, 4): "7ca38fec1517818e24f0192e0f2c190ec46b1fa2a2463c1f23def5c3a3a93351",
    (0x7F0C84, 4): "2c1ba53da03e500cb68f96d0ef4761bfb16915dfb60d5fc15ce2b5dde18f759d",
    (0x7F0C88, 4): "b96d08dc8411a49e42c6ae88b56076ad0c03bef06bbf4f37236a37ff481a5709",
    (0x7F0C8C, 4): "64e945e3dd037490b9cb088d387958c810b37c67f91c3b3c2264492e70fae58c",
    (0x7F0C90, 4): "9962d97272287f2e5af7258b2af5bd7e09bfd7e1042cd422263e268c98f582c1",
    (0x7F0CE8, 4): "9e688b6a19584b231a281ad62adaaf71c9b46286d53e5acd12dc33b1aeabcb3c",
    (0x7F0CEC, 4): "6eca001200031730bc2fd4114f4b0ec44501edf45ab492c891eb1081e7e93153",
    (0x7F0D24, 4): "425462475cd660269dc9ef933e9cbfb7316a1fd60fcac26274b57c00f0d4067f",
    (0x7F0D28, 4): "4e255a67590c9d37e66375c7ef427324e6d2d7bd5876c3b39972b5ca8faf90b3",
    (0x7F0D88, 4): "61cd7996a3d08beb4f7bdff967e2d4d646999536ff0e1569c796a726b33da62a",
    (0x839D1C, 30): "0b716912ece41523a84d7df50bb1637a7dbed20992bf5f5e728de8638988d070",
    (0x839D3C, 19): "40141bbbdd777708dd402a55cb44cade630f719ee57f9ef80347ca5956c9920c",
    (0x839E64, 10): "23eb71d511c188b1788617e25a85e0cb2aa2cb167dfa1803fdc8514b43b6db62",
    (0x839E70, 15): "148b069152e1138a7525b891faa94128e950649c81d6648ee0077fe7627daff7",
    (0x839E8C, 13): "c2a8bfd788194e175c15fe7af33726f476ef9c5c6d44fc62fa211302aff7cb61",
    (0x839E9C, 11): "0c27d4d2704d1698f547e89e4f27b861550869144d486a77a41313e0d0024b99",
    (0x839EA8, 12): "6353afe22eeb66a945409d38edebdcfcc21f3c24449fcbcbc54e83c4e1656c57",
    (0x839EB4, 15): "218b7fef6e6eac108bd09e49dd9d214ea0d47b34f847602d4f81370922a068fa",
    (0x83A0DC, 18): "ad48880b849a301b32b4edb7b1c8cf6bd153f6df1d4edee9e693f2f7526c1cde",
    (0x83A0F0, 15): "d106a915c67f99f175dc3bc9cbdbc3cd8883286a00c0ab60421cc225187015c6",
    (0x83A100, 23): "942d7c2ee4fd6e59bca64fc38e56c35732a8f61b39852ad4da13fd0f49307a3f",
    (0x83A118, 14): "dd26334f8c07cb1bbbfc574925f0f1e921f2dc2bef8aaa7ffeba409af58a0b9c",
    (0x83A128, 9): "e87935487caf5b934a67b261526c7d0e3dd3fcf8eaf038e8b1403f5100def654",
    (0x83A134, 15): "ed6528477243b87d8f4612967d3280546386c69cf19dde2d6935a680bea60a13",
    (0x83A144, 12): "f9ba96bb709c4ac3b99bed754e690d547c748c9fb581d013ef81ec173fb5e9f0",
    (0x83A150, 20): "4a466a67364cf6f6eb5a8230e5eaa1bf9ccb7780a4eecd75469e408f97fc3c64",
    (0x83A164, 25): "fe62d29a4fc39d9c7a2bcc1a1bf17310a94e3ab5363f71b9c174831717969fd0",
    (0x83A180, 17): "1bab89735101fab349820e034297016087f4a6eb2c0640d470b1d794fc9161ec",
    (0x83A194, 13): "67f94c9bff1934f72065ba41c05948e7f216a7c7cd702720721cf0d0d5af43fa",
    (0x83A1A4, 17): "bb0f48d0ee403527f3755707735b6f3fa2749fcb26b34070bc4dad1a75674440",
    (0x83A1B8, 17): "b146e9c318bc5dcf873c618e922ec9d0627bc883ac6deb5fbdab32a63e1c90c1",
    (0x83A1CC, 17): "9a31f05086a04b2175798850873fe82552216d6dd9a5ccd07116951daa2f21d1",
    (0x83A1E0, 15): "4b090afdd85a1442a2e1fd07efcd8459fc264ba675442e2bcb234cd499e90e92",
    (0x83A1F0, 16): "d03c37cd9b2d14f4ef00d05f89c3557f9328f00f6d5d90870b49cadcc9920807",
    (0x83A200, 23): "1dfccc11c83539501c6de2813ef86adffa2916abce74ff9814d74fb8f1211d3f",
    (0x83A218, 16): "1e68eef985a6a956ba42f58a5076b0aa150a1b1bc764b15d611c224c8b309590",
    (0x83A228, 19): "98baab64ada3db914ec5283ecad94a2ba5cfa89005c9700440cf93b97ccc70eb",
    (0x83A23C, 19): "e02866310faefd0a0bc587dab347f2b913eafe1f4e9104e2073e7f8ed8f7c6c3",
    (0x83A250, 15): "99e8b23c966eb4ea67d22e67abcdf769e4c2121d2c8370a31a6376a0afd83efd",
    (0x83A260, 13): "f4775cddb52e9c8cc2aa97a7a84a5c9496bedc1ef9d76702c795424b3a5b81eb",
    (0x83A270, 11): "33e620147aafdf42790c20c75a8b5ae468b3759e7866b57effceedd746cae4e7",
    (0x83A27C, 18): "2b30ab67e95880fad1c81ae33c633e89224276a021ac2e985a0b27177f6dee5e",
    (0x83A290, 18): "e0a8963d1e0113f9516cdb30389034c85d85b14311642669d8a6c81357deb2d8",
    (0x83A2A4, 15): "972caf86e5dd52a415c227ba789c469ce7d605610e6ea99ed15172fff1429304",
    (0x83A2B4, 21): "f82071a6ab604a8cff8900fdbaf77f52dad69e94a235661fb2a93a7ce8e18213",
    (0x83A2CC, 14): "2212cd569d16a497298de83f3bde52d8a5f7cc6c558027bdba88205e7ef8a53a",
    (0x83A2DC, 15): "235f97db1243b7d1c67ee13897c5b6ee1d0788c28ba8849c5fabc0bafcd2f53c",
    (0x83A2EC, 8): "a77f69c1b34713e9984361195524fe6c83079022fab3ff0d648794ddae7ba7cf",
    (0x83A2F4, 11): "697e45af67982abffdf35b83273e2ac0c46e0f7473f5b53d2efdede518641829",
    (0x83A300, 12): "c4ec8583a52204bd7d99f280d774ded35bcb11b5313c05ac0da3bad83c4cef5f",
    (0x83A30C, 15): "3883e8f688593bb7158eef45f5e2f8c46461c2a137598ab0374b3c0212ff03c2",
    (0x83A31C, 10): "9de3361195ae4bc98cb05d5bd260487d2b3f78ed9f85c242e51c079388a61a2d",
    (0x83A328, 13): "0cd7cb4d4cced09cdc82b63171c0c81d2fdf3046b2856baaed380602a58a8e48",
    (0x83A338, 20): "672f33c639b21259f51f4aecd62d12ff9fe2215765d10fe931120e4fdc43e806",
    (0x83A34C, 8): "63c417843b34c2932db449af6269a2f289a5960f79e472fdc49f3b88e8e0e4f3",
    (0x83A354, 12): "dd4a66982d95f6d09ce72e9b3497c16a51dc044966406c621fecf2ed741f1d07",
    (0x83A360, 15): "125a27b6a1ee01a0c480d84cb89b8cd2210467550cfe35f728cdbb90cef03949",
    (0x83A370, 16): "7efc200b9812f321d69a1fa5e0ad0cb8cc6d6f1707f2ca04ac27aded3bf0ba01",
    (0x83A380, 13): "5812107a249c76ad4d99cdacf27b0131d2ed283c4955b3cabda33ee1736df4a5",
    (0x83A390, 11): "654a71744776dbe8d6d70c33ad4fee45fbd10ef43917add8dfc2af63b3f324df",
    (0x83A39C, 10): "0b5d81f8d3db41bcae59f3cc07163cdf99eed6ee3549d2da90549c207f7d64d6",
    (0x83A3A8, 10): "65fd467711bb01dd834dc3fbddc79bb259cf2c2847ddd02ff12fb213e635c7e9",
    (0x83A3B4, 16): "6ea6d206d1faf736a42e5cb50f0c56ca1a77731e52f567ae157d3a8ea66f9268",
    (0x83A3C4, 7): "6885bc2dbbeedaef566ea93bcaf928c75c5d2868181a89a60567d6c80bf8627e",
    (0x83A3CC, 9): "d1d7d404c412c307e227ef149b9dcad2edfca75389336d03db54205e55542bc5",
    (0x83A3D8, 22): "2b2785ddb6ba5d58ec72671cb0c6fd0e7323ac46eaaa63e81f61acc8583d2a18",
    (0x83A3F0, 16): "5ef9cedb7fe84973c9756f0b5ae7525c49ba37ce5b66b25bcd5e338de0b3a600",
    (0x83A400, 11): "279238dc252a114b52f2327b9942f4ba74713549ca0e320fcdd57130adca6678",
    (0x83A40C, 13): "f65c5ccf8dfe0b4882c7f6fad409c7d757f19b703b2dc196842d0541cf89e3c7",
    (0x83A41C, 11): "f737531a80c565dd8fcc8e97cd5f6287369c3acab02286e0a598bca8f03819ed",
    (0x83A428, 13): "c7ffb0af4b938b6e1c3e7fc11f202d58ff48107aa99b29ad12a5bf24aea43301",
    (0x83A438, 12): "23c002b3809284088ece763e07f71e0e9f7581563f59c36342311706d6b5c452",
    (0x83A444, 13): "547a95a7b99e70313b1e144e6512ddbd732710a17a970f658a59ad380cf00479",
    (0x83A454, 11): "9adfcd4d3aa00af5eadfd7261f60ad496e3642c5b9ad4ba077f23967b67b9f66",
    (0x83A460, 20): "9a01e560420238fbd3da728885442b5ba9b73c1af99a33591fa9241d5c5f981f",
    (0x83A474, 9): "b0dcfdf5633285c4a9b723d56ce4d85eef95441f5954306a43b925ea04779fb1",
    (0x83A480, 12): "7940b83e186cafc8c082f733a423caecdf0e8467f2c009207eff0e478014474d",
    (0x83A48C, 11): "1011e296b854a76cb4c7d2640e387de9f4c6c8d61e31a9edd6512a193cdeb151",
    (0x83A498, 9): "8b6e23e6e4204a0e833f724791c31de6128d610e1bebd55a18304bcf0550301a",
    (0x83A4A4, 8): "4ea904909963a17995664ef4ec00d05d239ae19db2de1ae7c5b98353dc7a0b29",
    (0x83A4AC, 9): "39878b1626e0525471cd7f399340310a8ab6afc9e60ee413444da583345d6609",
    (0x83A4B8, 8): "e9bcbcb16ef93e0104f0f45d7fc28b2d2ee3d57ace3e3239f6f8f21634182e03",
    (0x83A4C0, 13): "c71ff5e781f60f12646d6f63b2dece5c924ca3db05bab56962e74598c08fff2c",
    (0x83A4D0, 17): "91cf375ad024226d6168fc69317fd2800e577aefa5774e2f777225f97e2a10df",
    (0x83A4E4, 12): "c38b8c3d0b99a7edc480d3bf6238dbc755234c26a0880ea9ef9b5df7011dfe36",
    (0x83A4F0, 13): "d19b4fac61817ecff0945d004541bb32022652014307e5eaf1069fc586cdb94f",
    (0x83A500, 11): "937ea59724d903e2493b1d8a665b2a24876e01d0d8097acfb8bde1ec77c00e0e",
    (0x83A50C, 12): "17c48fb71933c4127d045ea3f8e654d02451df603f3cb31ff770bc9196d8300f",
    (0x83A518, 15): "be835280a614bc0ab5d6cb090e6fd7f406aa84fed431b737fec4f3d024653b43",
    (0x83A528, 12): "afc559eab78a056f5e8ef5459d5a6c210005d145fbbb3872e9cac94dbe636cdf",
    (0x83A534, 17): "be121cea81278d15de23d1b94549e0993508e4a8ee0c9e3bf4b452614c72d860",
    (0x83A548, 16): "177167457728f54dfccee2621897fe41b9c8b56a494a9c0502db68b142e9a581",
    (0x83A558, 11): "c6f0f976d9906ad5f988f06823b212181f965bfefc22a76baac8c12158c2d724",
    (0x83A564, 10): "af5b9ac74e98849efffb74078894491dce7bc5161d069dc6acb9820efa93371f",
    (0x83A570, 11): "d49cc59b6b592650fbc569797e331f85547ed7a89c37cacdd76f937a45034f1c",
    (0x83A57C, 12): "9f61d4e89c78a80d133a2b8e54bd25c82b5cb78f34c75acefa1287a57c05d463",
    (0x83A588, 17): "cdbbe5a2be596fe77b5251d6c708674df6e05f277275d7a896a65e0fd6fda74f",
    (0x83A59C, 11): "4f511e909ed27e682474ecefc44aed4884dd2e9c03855fa511acd4bf848362b1",
    (0x83A5A8, 9): "65baf6b47a2fd23912098d07166edbb42b55e36d493568d3f87ae4f55390cc0f",
    (0x83A5B4, 7): "2b2ac374e99a75ed5b5f0ce2c5ffc5987cef563ffd1d1559f66f60659e7af1b3",
    (0x83A5BC, 16): "ccd4ebea395a9b1dd2bc49a1adb9be434bac4b9da44a2bdf04231e82091b8622",
    (0x83A5CC, 4): "4c72acadc58be3941e4f3322d188088d23542ecde7624f7a8735a608e18fb6cf",
    (0x83A5D0, 24): "238c2d77b87dc870784ef6672beb33e0b253ff7fefccc38966118e49143b49a9",
    (0x83A5E8, 22): "a6c3f492c9283cae883648d48c8feed62459686fc2ad8bc1e21912a52f900d86",
    (0x83A600, 25): "95ae91bf4b071408a68cb217b9f63010d824090ffc830c56caba2b20c80d0f6c",
    (0x83A61C, 18): "adee313ffd53af89a5321588eabbdabc9362d47723cdc689f8119b7b52a1227e",
    (0x83A630, 20): "3259a23f356b3161b3dccea98fae1c011c5d5098c9db75cab34981dd1a312aac",
    (0x83A644, 20): "cd1bb8fed62c2a83c9d5c4416c887a9443ed6c4c50ae1cbd9b0704aa99f701e7",
    (0x83A658, 21): "5975be5406c436393c2c04da18ab3e812b5aaedc3270b5f77dc305847c008200",
    (0x83A670, 18): "b4f94c1c379109fa682f7d8b032347b84150e292d34acd29167524e076caf1da",
    (0x83A684, 25): "e0488b9dc7802824ebbd2a4c9161ab0964ffebb4801e870f162f44e756d19171",
    (0x83A6A0, 26): "a63ad001b52124259cccc34c0697411d3c40b4c5c274045c351cfeef5084b24e",
    (0x83A6BC, 15): "1729c7d1ea24228dc332b996f7be3dd38e9b99eb062fc0e46e207954936bc462",
    (0x83A758, 21): "0d4cdf6732fdbaefb526734ee71561dde2550a2dc0728bc78357cc64fb5140ef",
    (0x83A770, 20): "c64411b473ee4427e32d77acd5bb9dc79346b3d2d315f1aabf6b8599e8b03f44",
    (0x83A784, 29): "dbebc2b0e3de8b26962ba8e0f99851ecd0ebc027aa270de5e4bed9c0d7c4a609",
    (0x83A7A4, 27): "60b7a125530ad395f3054d17e20bb4e6b73693242c1ce5f9ce5b3938e56407b2",
    (0x83A7C0, 28): "e6d153e128c2aa5145c855540018f5a23b655089f6bd5bb2a6983b4ec7b8cee1",
    (0x83A7DC, 30): "faef546b19aec0c0a4a2b103dff923ef8ab91e25e411b3b388874f39d5a6290f",
    (0x83A7FC, 18): "f55b1aa1fb5649fea1a125302783ecced18e61caa5aed71358bbca52f9811ab2",
    (0x83A810, 21): "d249db867316f7051c361c68562f8032649cfe0bd8b4183c64d9868d722674d0",
    (0x83A828, 19): "528e4df8da24abed535179f4bc7078414f4e414d44504ae962c350a5ccf0e1a7",
    (0x83A83C, 24): "7648ce4ff989f190726b9d082945997745199620baf8e344c40b8bbe256a510a",
    (0x83A854, 22): "03499e3521ce29085e2fb4a88f5f47e380db0d0751adbe0b182c081ae3b79e31",
    (0x83A86C, 16): "c671ff206329d59c178e490b63b3c9667a03d66e8ededc4b3e4b085a2cbe2757",
    (0x83A87C, 15): "f487114fe8fefb40022cec1bc8e9fcef5b27049e7c0178a899dadadc7ce90ce4",
    (0x83A88C, 18): "0b3f19d856e83246f924dfb9832f94f485d22ed1275691356536e5d431ad3cd4",
    (0x83A8A0, 20): "da371155fbd5f779988df73853082699f2acbdb9e9b2f13ac05a2b5d30c63329",
    (0x83A8B4, 21): "6cf21cc2b707ed550ec4bd6b5ce31bd0f0efa814a85a8500ee4468af6aac1f61",
    (0x83A8CC, 22): "d78b875339cfe09f1148eeb2b47bb0a75ec93b7b9bf21460be0a68c0ade06650",
    (0x83A8E4, 23): "779822e91aabdba96376cdaf0bea4570cb40b258fbccbbc2c3bac3a50433884b",
    (0x83A8FC, 24): "373ba1ed863fe0b7c463ac2fb3c4b7283ea1fac69a356a2cc38101ffa978973b",
    (0x83A914, 17): "57d9ab02480cdd88354e6993c6059db77badcccb909f2249a1f4fec6fcf0268a",
    (0x83A928, 17): "af998aed00ad0a28681c4168c786c4b7bc92466efe439733dcd216d498d927cd",
    (0x83A93C, 28): "54105b188c6697a7be1ddc54d1a5728fc58893bca25de599d9f7cacde6357e9d",
    (0x83A958, 21): "60fc60da02c4eff06b061be0e7250a13bd79eb37fe84601e3212e4c27ba3057c",
    (0x83A970, 16): "88cfc3f7a5348dc54b5bcce20c735fa3683207fb6dfdb66e469500bb10ff37d7",
    (0x83A980, 17): "4f63aa05456f0c6759ed88206d3e633dba1de2f34dd183833974738d3a7efe5b",
    (0x83A9E8, 18): "95606fc65131c1b14670b3a1858c9fedfa2a5016382d82c642e61fa594cf04ac",
    (0x83A9FC, 15): "9e3d844d6ff5b70ed2d7bd83d7ace62d7bac1d79f2ac3e65d7972b36191d462f",
    (0x83AA0C, 16): "d4f5a6f91a46dc2be65eb1125112a44b252e6ce7493fc1287ac9c6bafca5557c",
    (0x83AA1C, 17): "288bc3633d2cecc1fef4c9e25e45cc78d6a0f216b8330db010289518833d008c",
    (0x83AA30, 15): "7c4a5e82972208dd3534e008d585fb9b8bce9ee2dcc23ade41c8621f4a084995",
    (0x83AA40, 17): "bbb760eeaf421a328337a7bd88291031e9af26aa8fe67ddb35ae1c0ea40ffaaa",
    (0x83AA54, 16): "dfe73b8d1758f5ed1e3fb236ddf561f8a08e691e626a04bb358f0d5200c8ca51",
    (0x83AA64, 21): "7ada3c3a98f00cf27b2148030d5abe6eb41dc8d2c165f0dfed310d447b6dba4a",
    (0x83AA7C, 23): "1ecaa3848792fa2bb7a2f2cba7f685478392a0842629164dbde453b96ed24228",
    (0x83AA94, 19): "47da4af45986eb4080fbbdfd73936e5705a5e2b0bf329309cc1e4af14c66ef3f",
    (0x83AAA8, 11): "f87435a6a316e6b4fc0bc00263749a37f9b64f350d7c42d86e749cec50741c89",
    (0x83AAB4, 15): "8d7435295f0dca2337fcfc9c23f6f3e91805a32618e61161fe1c0bb96188d469",
    (0x83AAC4, 17): "8b05f7a47cae3a23b22c7100b800695ef3861f53c2408fd265b15d255c903e90",
    (0x83AAD8, 19): "9c28d9a57acba560cc0ee808252d0b181660d7a0da585dec44f67b56e5e091f8",
    (0x83AAEC, 18): "961b07e7debaf7b771fe97e6ce64fd46af760d8cf75a02cdda6531c9ba5b948a",
    (0x83AB00, 15): "9c302d7bb8289a2475433c3452d7fd2bf6a30fb486b566a955d49396d65b7cd1",
    (0x83AB10, 16): "ac111001f56dc526f1f8b775409121ef224b7d712f97f09e6ea02148e3e54825",
    (0x83AB20, 14): "56bcd2ba883d0954b8d5b173beed0788b1758d43ffcef8535971b87d7cf46239",
    (0x83AB30, 13): "da0c3bc6438247a40d1084c3a10a69c8f357ed153b4e7b656997aa30b2e47989",
    (0x83AB40, 12): "4042205df0531c360a078be343447b600505c96c7cff5ba5c0bbcaf692cc7c70",
    (0x83AB4C, 14): "74f58cdd72b7865fc8793772daa9ffe925e63caa33ea672c0b4b458a02d6f3f8",
    (0x83AB5C, 19): "ba919ec87cd20be10697818037235835c1676846da8453a63aed258bcc22b844",
    (0x83AB70, 9): "cdfa5f1af2ddcc0d491ab76135490a04a88dadf15f31bf9c5d0513773eb9aabf",
    (0x83AB7C, 11): "b82d9bcab5adf381c3db849222d845e1e2d9740fabde05486ba80fe622366288",
    (0x83AB88, 23): "e850bce25e403f70822594f02a75566cdbb1ac211a329a5b7f3686206bbcfdeb",
    (0x83ABA0, 12): "0f3a0d266924c6cbb7726ff9ef0a7d0024180062ea22a9fc16d133a60e6bbf10",
    (0x83ABAC, 10): "0f6fc27f2a9edcd74c3b64e91b820623d989191d085352746f96e7d51ce13dec",
    (0x83ABB8, 8): "f1daf24247f84900a94cf5650fdf4ec530ef34223485d060f63d510f127dc070",
    (0x83ABC0, 22): "9f07be576f6960fe4cd7d8734347c127a8269df695b7f0b95e50316820ad0ec6",
    (0x83ABD8, 24): "4bcd36c3eaffaa4a2a0f6d3cedcd513171a7242a36c865b48d87fcf96a826a24",
    (0x83ABF0, 25): "d07291088d30e696b4db715cf2ab69dcca43a1e564846924b09fb64d2ebadc1c",
    (0x83AC0C, 11): "ae345293592a858be619ed895b3fd70011ad2ecf87b680a0856409a9fb0920e0",
    (0x83AC18, 10): "21e0058842310a921b0297ce52c6dce07873b96fb5c9e7a411cc00d793a316cd",
    (0x83AC24, 12): "ffc06d05544e84c9c7f25290d9033e92c6437ed584a116ef73d5489fd07a8885",
    (0x83AC30, 15): "eb24fa3a11506ff3d5f10d3b4e0f3fadbc39f8886cf141b3166e6e0a0f971766",
    (0x83AC40, 14): "f159bd2abd296e9ff188240d11af2e700f322e896bc1fcb25c73d70e92d5d28c",
    (0x83AC50, 11): "75f9331e435c8e75bcb10a90c7d14e2cdee5ad3b562f6a947180685f4abb0591",
    (0x83AC5C, 12): "295ac9f00cf68505bd198e2b12678c931bcd18e5c4bec0d7d2bd568dd19a77df",
    (0x83AC68, 13): "f6a950a6828326bd54690a7fdacdd2c643fab3522885667d1c3aa5f2d62141d9",
    (0x83AC78, 13): "94aed9df4f26f485b9ea4be309df1e007e23a6b0d035d2d0e4684bcf201a12f6",
    (0x83AC88, 15): "1bb2edfda5f77d3d157099087bdc16ed5a50634e3c02d81fa0a6a5a08c8fd88f",
    (0x83AC98, 14): "112fe2292703500669709108a80211a24ddaf17013c2ea6e992b6c3ef8307359",
    (0x83ACA8, 9): "66d9b5fd34f3ec42b07669582706a46c19bc6e3225288859ebc0c0fa6485dc88",
    (0x83ACB4, 13): "0cfc78150b145cd0e843d05a5493d7106c2216064e30302241ade84b79c4bc67",
    (0x83ACC4, 8): "404429818635dfb113ef9c83d0d90b85c374322b1052fe71fd65f7a4584b1ba4",
    (0x83ACCC, 15): "5f893a48879b9cee33426262cbe93742ec7f88a2c5ca83c45155085ce2181e45",
    (0x83ACDC, 9): "ae986bf983683ef3618d22c2fb499860ef5fc7de03ba61841e3598a7aa7c6d9f",
    (0x83ACE8, 14): "e78c881b7f45a1cdec194a3fb88e439fa1155642142349693a895b2d98f5fde1",
    (0x83ACF8, 14): "4630ddd12f94e79fda01e49d9408772c40b0ef70e6f169731716cb01d8b99f4b",
    (0x83AD08, 17): "9992b02d1f541b056b6e6116226481070eccc4ed128e2226a94093fa9569ca71",
    (0x83AD1C, 16): "99d6fe6adeddd8a6d2b945a652694d3afa4c946e8d71e0c23216e76ea44b15c4",
    (0x83AD2C, 18): "47a0e26e48df7961c92e23901498e4d3323864be567e0afb3d87e3f85b1fcdf5",
    (0x83AD40, 10): "5208449d0761a97b8b1b55ec483c913fd6e5dabedb180ff44a5594166ca9c673",
    (0x83AD4C, 10): "edef38ab5bd8db6cd6526ba03faccf741510b6167895a663d44765451c71d103",
    (0x83AD58, 14): "bd7d062640e345f44e2c3fda572e630300af7b4f18984a053222b1cecd704eb0",
    (0x83AD68, 12): "18365135c5ad6434150171931a61a93767bda2cfdcfcbb9c91c222f57d57017d",
    (0x83AD74, 10): "7085558f71fcf0c074f154e653b755559a0526d3ab91d37c0f766524557f98d1",
    (0x83AD80, 6): "5a856f97691019139ec5ed2dde0318d183033b791a619a3deb7dcb8121379a44",
    (0x83AD88, 8): "68c2f21b204940f8ea467672dae3666019432b16d95514d88bc606038c94de2f",
    (0x83AD90, 15): "958995f19915ae61b3c8eef137bc1dd7894eaee3fc7042253296d7818ec99df6",
    (0x83ADA0, 17): "0abd3eac135bb7a21ca62adf5002b5809ec1035a948cc1b410963a836633d4c8",
    (0x83ADB4, 11): "31b739330d88dbb4bb0caaf8cbe0b54b565c2cd98ee0267ca87f843d8ded25e7",
    (0x83ADCC, 15): "f00882f6d69361e836bd93a42b74461d77e993485a65c8b3dcec716843d3cb3e",
    (0x83ADDC, 28): "03e9b311734a8a354893887d9a3f3e46f3352c9d083ec28c20dfebcb158b1893",
    (0x83ADF8, 26): "67c8bbb9a6d7a08d5b8307ad1a76778a216353412a207830c04bd81892101603",
    (0x83AE14, 24): "170a27b41b03942e41cd3e2d1856d9af2065532f2d92e1835368c04046d82f52",
    (0x83AE2C, 25): "b2e66bf8151f2ae47d8492680c530a72628899fe56824e489d6313b079b81834",
    (0x83AE48, 27): "e508ea435dc2234ebd420a4719e6d6e013b55ad2928b29396cc2481227b7a4f9",
    (0x83AE64, 27): "f8f71931036b1d8d3498bb2661be85b39d27c5c96ff7b756e45801b5aa3d9a00",
    (0x83AE80, 19): "aa734bb81008cec90a99ba28ea32b1695a5ef8dafdf65c9ffea97f9350e5529c",
    (0x83AE94, 28): "4d9d45534e74dcc09b57d2f53a091a83030e16b1e37314f1885f79f4c334db82",
    (0x83AEB0, 28): "84127a9f0c649bfe55bc13d555636a7ac223450f6a1ad319766f594965840ed1",
    (0x83AECC, 17): "5699f850258c235a461040189d53d375c87904bb6dcc04503ee4052fbbc0b1f2",
    (0x83AEE0, 29): "2eba618aa416a9c3ceeae8a223fa02821e3f6a30682c3a52eed05e1bfb791a24",
    (0x83AF00, 24): "640961a5dfb241fec129c7da509485eef0371a121521318ed75a64e2ae1201d0",
    (0x83AF18, 22): "6bd1743de97627e5e2509a660ee7d1c8cc846b9771e450da8f819323cac0318b",
    (0x83AF30, 24): "cda6af0d182a0035ad6276eaa870f098d626e62b8825cfaa4f71c9a4318e8542",
    (0x83AF48, 17): "8dc535d5a6cabb388b84e3f750411b76cdc04b28d9ae05d4598e79f002a852cd",
    (0x83AF5C, 21): "140070cc24bf6d02e22b81f56623adfe37065f18dddcaa37c27521fa3eafd8d5",
    (0x83AF74, 19): "e6d1ab83a7385b4032e78d175a3ea36250af0aa232afa48a036e3d2d8799870e",
    (0x83AF88, 28): "932c16a32d84d839ce97aba80e06cead0c4cfd2312447d1aa359a0f047f2c9ce",
    (0x83AFA4, 15): "bfce1163c92bf03f55ab530d1d9092daa3545073fa011ca713504db25f29b839",
    (0x83AFB4, 15): "5dec635634b745f7b572e2eab36134be0d720a316bb1cb31015a97ac040d82a2",
    (0x83AFC4, 14): "6a0d41d4555caa6fba0d5deb49a1247f486b16d9e5e262db49fea3a3fdbb89a2",
    (0x83AFD4, 23): "5d37fc181115c3789fc19477afb1567c8cb30082b56813f2f39e71e9b2df7ce2",
    (0x83AFEC, 21): "07b0d703a9bb53451e88053d09bf0728055983672b2b28ab1b577b5bbb2ae25a",
    (0x83B004, 27): "bdf7235678a4399359cda2a3c8330a8451cb945dcf263e3e3648452a8529d8cc",
    (0x83B020, 23): "5447ac3c4f7eb93ceab11bc0cfe0c591a63ef117dee2b4e7127fa8b4cba08e9b",
    (0x83B038, 20): "95f1fcfe1dee4a00bb189ebdf7add0c193efedd8cad67acf501e934a8b7e3035",
    (0x83B04C, 23): "9edd7fe8efc6093fb6ba7cafc22142d585018db255097dc4e375826e2074d2ff",
    (0x83B064, 18): "4c6a58fd4c9f647ad6c8dfbbfb68741fe5710d89b8cff0654367e5599d40aeea",
    (0x83B078, 20): "0ea073fc877826424fc9a5e74e66cebe033f281a5324be309baa789ea5ede38b",
    (0x83B08C, 23): "ec1238d07a64b1a87988f7a59811e720a83bb88e3f9d8d48d65dd787febb744a",
    (0x83B0A4, 20): "2a1334250d39916680639b78064074e46a857bd97024d0230c10bce40d7fc26b",
    (0x83B0B8, 20): "64e67ca49e652475ec5f0815f060f950513f0ff649b977975ec1a4bef2e65d7b",
    (0x83B0CC, 20): "6b1520a6143bf564ec81c030bc55389ac817417aa369a04c5cf6e38d5e675fd0",
    (0x83B0E0, 13): "f05761eb0c8083b1d48f02ad74f401988ac14221fa550f57860ceb8c239a732c",
    (0x83B0F0, 13): "53f582032a4d6523869a95fe769650497ffb56d3d5a927e123406f54c0c8d00d",
    (0x83B100, 15): "44dee8b55bd43549425727528b6bf845ba22d588f370464a27ee6022bc07f9df",
    (0x83B110, 11): "c06ad53cfa4c3d1b87c10806b64925f43174b8e88616102c55a63eaeff96ae8f",
    (0x83B128, 21): "7e5b304547b3711fffe223f46ad1bc3602ec91b45deaebfc11653ccc292a6c1b",
    (0x83B140, 20): "86d2222bafe1b6e54eaaef5092b009034a038565eb294a5f4295ec7afd8b6071",
    (0x83B154, 12): "a346437047e18f8fd091823d8334875fc7d45349cc5db2a7733a1dee4ef62508",
    (0x83B160, 18): "63fc9dab7c91d172ffa367802ba1e8c6ee0937f2473c7f28de5e9773026b3de4",
    (0x83B174, 13): "1e61259c86b183e80820115363efb5940e3b773f8b116c46da6d1c84a3498ae5",
    (0x83B184, 18): "cd85f2ac22492061573c8ceba78fab51855761f7e07080f4d5546acd3be28df0",
    (0x83B198, 15): "c33853d26593f43d1e7cfed567620cb5a78b4c4939cd54451f9a84c93fd05fdf",
    (0x83B1A8, 13): "b8895bd93d415654f89cbb9604b45cbf1b8ee894ec59270015e28747c0cc6c26",
    (0x83B1B8, 10): "20a5c955c0bf4149874031f4249c092bd8528ac05e230a0701203cd735ecaeb3",
    (0x83B1C4, 13): "8ccf3c86cd6cb3f26b421ac15264307e56b41f2174a2727f05f45b87f7481ec5",
    (0x83B1D4, 10): "2c0ce919352c2f04777437e1a0c7a16395ec1bc42dc65688309eb5886e4cffb0",
    (0x83B1E0, 13): "f95bf3c3c577207733bdca8940596d9853f7650053f0d7013efaccc48c0ecfcc",
    (0x83B1F0, 12): "fa1542becb2b7c9c4fba7912aead38950927baf46adf898cd235e7b1a7ee4182",
    (0x83B1FC, 11): "04fc7ddfed878afe319a83e5dc8b4fa7ea8f7c2cc2337d219186a5add8c8197d",
    (0x83B208, 10): "8f61bdd4cce1494cf0452395a2bcb9fd93edf2cecb587cee60851b378d3873af",
    (0x83B214, 10): "af3a40fce2ac86b1efca2edebe253e0c2abf270c153aa9e5db705f33e5aa044a",
    (0x83B220, 10): "fb5155ef4c9ae0b2d130de17a43e5df0f7cc900eb6c1b18b9b4f8431504ea8e5",
    (0x83B22C, 10): "839b0cfef125d6f405708be117d42d608e302404c3a86fe48396a1a1af2c82e4",
    (0x83B238, 9): "23a1ddb6e36a783db4230a933e3c937d2428178d557a0efba816a687ae16bf70",
    (0x83B244, 17): "92d23d5421a62bad78ee12506a6ce304ecc2cfa94f5ebd1aea269ca57dd53de5",
    (0x83B258, 24): "1b10574e2a7ebcec805ea96c00116945167efab96282d0f4b87452feeadb39a7",
    (0x83B270, 20): "3befaab705f3eb5712ad21b84a2313b0f701f96fe09e7716af50cd960775bec5",
    (0x83B284, 16): "811a18012547ebb9588ee157c7784335e8db7ba79c5b7ff4bf5cbd76ab78dd43",
    (0x83B294, 16): "7c9f5c253795964090d124d9a9488b4d891b1905f2076c8ae9dfdae7285330f6",
    (0x83B2A4, 15): "2e35ed658d42c0ec310bba24ae599e7e885536bb6f26be7fe9bb7d7fa533c3df",
    (0x83B2B4, 9): "5b656a1a4bfd11cbb4480d6e9643a4a2703a9c083b9d433f2328bdbfbaed04fe",
    (0x83B2C0, 14): "23e070d4bff8787529badbe7b0d7e360df6e19c7f068ebadae108de884b99a13",
    (0x83B2D0, 15): "c8a440e05d106c21be08b02c877e25b15a58b0bef2e8fa51c259b684a184fc46",
    (0x83B2E0, 15): "b3af48b2e592c6bfbc67fd6ba5060873e8067dba1867405b11c695c43f627ef7",
    (0x83B2F0, 14): "e757afe2ea7a92cff19af1fb2c3d8f9cd15de55eb652d5b08ee779e376d5e2cc",
    (0x83B300, 14): "d4d1c2df4e2a2ecfe130da003a35db0ec5c704de29546c490d2d9568e2e47462",
    (0x83B310, 12): "33b57ea72b815e27f11728c62844b584d7d1afb3958dfd75df64d55c03cd65e1",
    (0x83B31C, 20): "70aa3e3a7e9d6663a1200f982ee60ab46981a2a5384804a51c34d7861e115d4f",
    (0x83B330, 20): "8ca8be9e0919070402144c8cf4435c859fe5f871376091a880a6232eb522a3d4",
    (0x83B344, 18): "791170e17381ec3f2f0931095dbebbf28a16a46b4638143eefd6fad2be0f9afc",
    (0x83B358, 24): "d94a4c9500f8844136b7bf634ebc903fa35e8e3e21f05f55023b4c6f95d3f5dc",
    (0x83B370, 19): "66e04bd43099ab49575a9b7034ca8798eeecb7e392553a8a0e4cccfe836f2102",
    (0x83B384, 24): "89e23c42816a466722355c30e8efe231e77da04d742f7eac588018c0c40a10b5",
    (0x83B39C, 23): "4fc204f5b378e0b55bdf30d8ae84ce1b5fee22ef79b67999ac871a3b3cd80fd4",
}
