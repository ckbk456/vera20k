"""Reviewed original General66D530 declarations for the retained W02 VM.

Native image SHA256: 3e81a61775d2745d1dabe397325ef663cd994ffc194da4e998e3bf5d2d308600.
Only immutable original code/data extents are declared here. The existing
startup owner supplies the initialized Rules/type/INI objects and selects
the new profile before creating its VM; this module performs no loading,
discovery, emulation, fixture writes, service substitution or JSON enrollment.

Original callers/receivers and retail General were reviewed on 2026-10-06.
Static receipts: .local/fv-movement-validation/rules-general-20261006/.
Current ownership and reproducible review: steam_rules_general_scope.md.
"""

# Original668EE8 calls66D530 after AI/Powerups/Land/IQ; full return671E99.
# An absent General section returnsAL0; present keys retain original defaults,
# conversions, native type factories and vector mutations. No scalar is supplied.
GENERAL_REGIONS = (
    (0x66D530, 0x671E99, "7562c49086fd7bb2c5e56fcf39b9db6f4727658a85ad8201e2af016aebd91374"),
    # Original caller 47738F.
    (0x45E7B0, 0x45E7F1, "8d26f89e9fefe83df1ca3478d1716e5d2440bab98c8333eb29971affda404fde"),
    # Original callers 66F2E3, 6702A1, 6702C0, 6702E0 (other callers share this body).
    (0x474620, 0x47465A, "b4a6382be418657abc846fb597353ae9fe5b29da0bd3404b89781baf405952fd"),
    # Original callers 66E78C, 66E820, 66E8B3, 66E947 (other callers share this body).
    (0x4770E0, 0x47743B, "e1180128a0124e228f4a81758ac49003ee07de763364f3784854c2f6d8a47b46"),
    # Original caller 4773CB.
    (0x4779E0, 0x477A68, "b4705fb74e72e29307de9c7a9277c0f0e948fdf8f3ce0be40c37c9939fc5efa5"),
    # Original caller 4773A6.
    (0x477EC0, 0x477F10, "30af68b9c6a673326067624c6aebf06e6d7145fa754b7738b9265393be87482f"),
    # Original callers 66F3F1, 66F62D.
    (0x50EA00, 0x50EA27, "702da33d4a119766cd5059aba9f71eca2739b14fcf93b004f646f2dcd44b2859"),
    # Cold/temporary derived vector resize: VT7ED90C+08 (cold66621E/list67B5AC).
    (0x50EA90, 0x50EB40, "6cf3f6190bc51eec098b419eb9681e0576bb6b8e00dd151b175b1dec0c143ca8"),
    # Infantry derived clear: VT7EAC08+0C, cold66666F/list67BB6C.
    (0x5128A0, 0x5128CA, "cd4dddf4709131ca36ea81a5a55c884f4e0d5238d7388dbce1daa13fbfa22fa6"),
    # Unit derived clear: VT7EABE8+0C, cold666535/list67B77C.
    (0x512900, 0x51292A, "9d9f8fd59ba8f8f341d795509d5398517b71f3faa054f91c68ba72cd08b51605"),
    # Aircraft derived clear: VT7EABC8+0C, cold66657B/list67B94C.
    (0x512990, 0x5129BA, "28ea1f51e86327ed6ea01b34c46b295a85886774659a22a028642df2f05e3a22"),
    # Original caller 67BC00.
    (0x512BD0, 0x512C3C, "0f99ecf93607dd0c361952d87bb89e3d3f305e06ae3005f33651e720337ad663"),
    # Original fixed clear slot 7EAC34.
    (0x512D30, 0x512D57, "8144405b3ee35c3048e8973f87627e9037afe4d61b030456dd8d94d4e428f4df"),
    # Cold/temporary derived vector resize: VT7EAC08+08.
    (0x512E70, 0x512F20, "1e4e0502e210dd01a607d66d46911357cad25122f36bdd72b5ce24a78889cf3e"),
    # Original callers 66F88D, 66F990, 67B810.
    (0x512FA0, 0x51300C, "38e7f3b70c8686d71f22c15e1bcdce02beb260ddb85fbf042ba3367ef7cd19db"),
    # Original callers 66F869, 66F96C.
    (0x513100, 0x513127, "6bca347936a10378e773e830cb4966c9b79d794cacd5b89fa4d613939d365258"),
    # Original callers 66F7F7, 66F8FA.
    (0x513190, 0x5131ED, "ce81c825f813ba0d5eda1a628bdf2f2a5d5041873f89b4c9fd90df09a7920a21"),
    # Cold/temporary derived vector resize: VT7EABE8+08 (cold666535/list67B77C).
    (0x513240, 0x5132F0, "822e8ca4d2a8ea6a789edda41cb31c87a1da3236c11006ec320bf8a09c64586d"),
    # Original callers 66F837, 66F93A.
    (0x5132F0, 0x513340, "30af68b9c6a673326067624c6aebf06e6d7145fa754b7738b9265393be87482f"),
    # Original caller 67B9E0.
    (0x513370, 0x5133DC, "1a673dbce7933fcd249dceaa9b2e93847aa25902f9e233220123f41b13991b14"),
    # Original fixed clear slot 7EAC74.
    (0x5134D0, 0x5134F7, "e4f2cfa5f9c5040bdd14727787180179bf67a08929a2407af2ede75a62609142"),
    # Cold/temporary derived vector resize: VT7EABC8+08.
    (0x513610, 0x5136C0, "2b2296a3d599f480e5cbb21b0f0a8685fa678295a9b9a10a6e759962e511fdfa"),
    # Original callers 66F858, 66F87B, 66F95B, 66F97E.
    (0x513740, 0x5137C8, "4e613a9546b9ee8a7bd77916c0d3b6c6ce29151b992133369bc95def9a326294"),
    # Original callers 66D626, 66D953, 66DA55, 66DB58 (other callers share this body).
    (0x525060, 0x5250CC, "80641b4354868afcd348b5fc2b9ea73bd9cade3ccfc2d3e971dfff2022ade738"),
    # Original callers 66D602, 66D92F, 66DA31, 66DB34 (other callers share this body).
    (0x5251C0, 0x5251E7, "230c853acc6c31ce623cc8138217a64fcdc3c4c49c314f7f29a676433422f927"),
    # Original callers 66D590, 66D8BD, 66D9BF, 66DAC2 (other callers share this body).
    (0x525250, 0x5252AD, "6548d59399795e3351f1d69c797e2a46a9339fc9b55d856f7b4220f3a5f21d8b"),
    # Cold/temporary derived vector resize: VT7EB6D4+08 (cold665A43/General66D59F).
    (0x525300, 0x5253B0, "ad0a7f9cd6d3a3e4e716d4e33a983a5dcfe443e47a263af62e0d9464828f9222"),
    # Original callers 66D5D0, 66D8FD, 66D9FF, 66DB02 (other callers share this body).
    (0x5253B0, 0x525400, "30af68b9c6a673326067624c6aebf06e6d7145fa754b7738b9265393be87482f"),
    # Original callers 66D5F1, 66D614, 66D91E, 66D941 (other callers share this body).
    (0x5255F0, 0x525678, "cde0c491b949ba4a856abb6d2e9f499015f59f8479009db258ba396fa97d0f21"),
    # Original callers 66F37F, 66F5BB.
    (0x5AC900, 0x5AC95D, "53ae27c97123fff04565d07131d79ceab0591d01d6394e4fedab5593d9649e3c"),
    # Original callers 66F3E0, 66F403, 66F61C, 66F63F.
    (0x5AD660, 0x5AD6E8, "16e41d31bfb6f4308b5b109ce6a1cb3d7d995e35cc4ecae64214621e6b56c129"),
    # Original callers 66F3BF, 66F5FB.
    (0x5AD7D0, 0x5AD820, "30af68b9c6a673326067624c6aebf06e6d7145fa754b7738b9265393be87482f"),
    # Original caller 66FAA8.
    (0x679FA0, 0x679FCD, "7dc704609638ae3a52e8ff38076eac9ba5495f50b7d57a58dd8f609b0e1e3754"),
    # Original caller 66FA75.
    (0x679FD0, 0x679FFD, "c1ffb9d5637a44e8b5736bc72e05e7c2c3eb5b674f716900ca01ec43a0e9c6b6"),
    # Original caller 66F9F5.
    (0x67A000, 0x67A02D, "1fb56809ce22c7a663095d82db024ba15e83c37d835b48d1766224a1ff406c8a"),
    # Original callers 66FA42, 670659, 6706C1, 670729 (other callers share this body).
    (0x67A030, 0x67A05D, "7114efacd7b2e407401e248bf8999d5c0b7992a2deab1b628df24420adc5a442"),
    # Original caller 671D6E.
    (0x67A060, 0x67A08D, "1534f5724f24dcb7dd3a504d23680f4417f643fa87c368c427028f9a22e4d8c3"),
    # Original caller 66FA9F.
    (0x67A110, 0x67A189, "470772c1582f6d2c88b361d806493c4e990890c69ef4a489952ff20707c08a6c"),
    # Original caller 66FA6C.
    (0x67A190, 0x67A209, "404774232ec0a1425fcbacde49c7e5a379c6400224a7441dbbe371a1f36e5db9"),
    # Original caller 66F9EC.
    (0x67A210, 0x67A289, "6f333840df79d18e102162c1eac264ebf55d73867be6e1d8c06abeff6f1f4097"),
    # Original callers 66FA39, 670650, 6706B8, 670720 (other callers share this body).
    (0x67A290, 0x67A309, "ca3d4b597161a3d5200547d8269b88807a0f6781dac53beb674010a6c517765a"),
    # Original caller 671D65.
    (0x67A310, 0x67A389, "44907b99f2e10d30914a8b0fc42a9bb628afc855f89af7e54873c72045fcd566"),
    # Original caller 66FAC9.
    (0x67A730, 0x67A734, "74032ad0e931f3c4730df99da43479f9f5315cc898c7c8614278631cb2c16a62"),
    # Original caller 66FABC.
    (0x67A7C0, 0x67A7C4, "74032ad0e931f3c4730df99da43479f9f5315cc898c7c8614278631cb2c16a62"),
    # Original caller 66FAAF.
    (0x67A8A0, 0x67A8A4, "74032ad0e931f3c4730df99da43479f9f5315cc898c7c8614278631cb2c16a62"),
    # Terrain derived clear: VT7F0CFC+0C, cold666BF9/list67BE2C.
    (0x67A930, 0x67A95A, "9f6dceaef7815c8f5fdc486d6f62c20dec3bea792adf4a7bb13251311e5c82ab"),
    # Original callers 66D79A, 66F062.
    (0x67AA80, 0x67AAEC, "26f4055623f049c6819c32abfdad8446970b0d8fff050521733d823e2f8b6d41"),
    # Original callers 66D77C, 66F03E.
    (0x67ABE0, 0x67AC07, "ffc0cfe377a6834af37a1a0beebb6eab6cd81eaad241311d0ac0e2ccb0555ce1"),
    # Original callers 66D70A, 66EFCC.
    (0x67AC70, 0x67ACCD, "6c3398c7b2fa42e4f71d0776ffc25f9a549cceee6e4074dd929c27150a0b8497"),
    # Cold/temporary derived vector resize: VT7F0D3C+08 (cold6656E4/General66D719).
    (0x67ACD0, 0x67AD80, "e8694abf1d73a4fed2327e064844c43cdb7c2e092a831e9ae91a4ae27abc7055"),
    # Original callers 66D74A, 66F00C.
    (0x67AD80, 0x67ADD0, "30af68b9c6a673326067624c6aebf06e6d7145fa754b7738b9265393be87482f"),
    # Original callers 66F415, 66F651, 67B640.
    (0x67B180, 0x67B1EC, "a724265d92da31900a4102f89f80fbd90722bd006bf924f2a8d50777d431c64c"),
    # Original fixed clear slot 7F0DA8.
    (0x67B2E0, 0x67B307, "07f477204ef4a5b5e262e8e8e4d1e6edc0427f8410547704944e70204b14b0b4"),
    # Cold/temporary derived vector resize: VT7F0CFC+08.
    (0x67B3D0, 0x67B480, "79e9173b8a1bee1bc962877be7daf2ab16bb100051712d461156108d9012c46a"),
    # Original caller 671067.
    (0x67B500, 0x67B549, "e6ffac388c65f6c6705606dd22147f570bb41d2f6ca049f3b9f3800908dea6e8"),
    # Original caller 66FA93.
    (0x67B550, 0x67B720, "209e6d92d27aa41e31e9be67a216ab7bdd7e2ef3bf5801bb266f243db675c4f5"),
    # Original caller 66FA60.
    (0x67B720, 0x67B8F0, "33737a34d788fe9839bd07df72c0f8f66e3813883347c576164eae6bfde0e851"),
    # Original caller 66F9E4.
    (0x67B8F0, 0x67BAC0, "3af3e1da38afe9693df963449beaf9a91b6cde844ba2326517435e3ad492b08d"),
    # Original callers 66FA31, 670648, 6706B0, 670718 (other callers share this body).
    (0x67BB10, 0x67BCE0, "aec3cf7c76f9b2664a26b42b77bd01de3bef56943406529fcd3468b9c9228b67"),
    # Original caller 671144.
    (0x67BCE0, 0x67BD29, "c09d72f827e43850f146ac2432ae63aec99524a1c412088a44a4339bb087e936"),
    # Original caller 671D39.
    (0x67BD80, 0x67BDC9, "294e94265a0dd36b882f0c3ec539c2dbe3a2221819406f662ac24fd846a5ab14"),
    # Original caller 671D5D.
    (0x67BDD0, 0x67BFA0, "0445c7f10a7c27d4d724c8e8cd8613e1c36d1bfe46297b27e2bee86d0849cd74"),
    # Original caller 67BEC0.
    (0x67BFA0, 0x67C00C, "67717883b161a52f82ab08e5291e782cf9d14f17a349d84a5682543f4abb6259"),
    # Original callers 66D76B, 66D78B, 66F02D, 66F050.
    (0x67C1F0, 0x67C278, "c6d0b52006250da9299dfe4ca532c0d2fa3a9a16bb8c06504ff34f77bb9b579b"),
)

# Cold665650 establishes the derived receivers before General:
# Anim7EB6D4(665A43 etc), Int7E4DD8(665B53 etc), Voxel7F0D3C(6656E4/665EB4),
# Building7ED90C(66621E etc), Unit7EABE8(666535/666558/6667CD),
# Aircraft7EABC8(66657B), Infantry7EAC08(66666F etc), Terrain7F0CFC(666BF9).
# General list helpers override generic constructor vtables before +8 growth:
# 67B5AC Building;67B77C Unit;67B94C Aircraft;67BB6C Infantry;67BE2C Terrain.
# Original absent-key copies invoke the fixed generic+C clear slots below.
# Generic+8 resize candidates50E950/513050/513420/512C80/67B230/67AB30/
# 525110/477C70 have no admitted receiver and are deliberately absent.
# Only +8/+C dispatch words are readable; unused vtable methods stay excluded.
GENERAL_READ_ONLY = (
    (0x7EAA14, 4),  # Building generic clear→50EA00;67B6B0/5AD682.
    (0x7EAC34, 4),  # Infantry generic clear→512D30;67BC70.
    (0x7EAC54, 4),  # Unit generic clear→513100;67B880/513762.
    (0x7EAC74, 4),  # Aircraft generic clear→5134D0;67BA50.
    (0x7EB700, 4),  # Anim generic clear→5251C0;525612.
    (0x7F0D68, 4),  # Voxel generic clear→67ABE0;67C212.
    (0x7F0DA8, 4),  # Terrain generic clear→67B2E0;67BF30.
    (0x7E4DC4, 4),  # Int generic clear→477D20;4777D2/477A02/477B82.
    (0x7EABF0, 8),  # Unit derived+8/+C→513240/512900.
    (0x7EABD0, 8),  # Aircraft derived+8/+C→513610/512990.
    (0x7EAC10, 8),  # Infantry derived+8/+C→512E70/5128A0.
    (0x7F0D04, 8),  # Terrain derived+8/+C→67B3D0/67A930.
    (0x7F0D44, 8),  # Voxel derived+8/+C→67ACD0/67A410.
    (0x7EB6DC, 8),  # Anim derived+8/+C→525300/524ED0.
    (0x7ED914, 8),  # Building derived+8/+C→50EA90/50E4A0.
    (0x7E4DE0, 8),  # Int derived+8/+C→477E10/477840.
    (0x7ED8A0, 8),  # DropPodAngle lower native double;66ED4F/66ED60.
    (0x7F0DC0, 8),  # DropPodAngle upper native double;66ED30/66ED41.
    (0x7F0DB8, 4),  # TalkBubbleTime reciprocal native float;671E60.

    # Every key below is an original pushed literal, not printable vtable data.
    # Readers526810/5276D0/5283D0/528A10/5295F0 scan key length with byte
    # SCASB and CRC4A1DE0 reads bytes; categorystricmp7C8D40/43 also reads
    # bytes in the retained C locale. These literal extents includeNUL only.
    # Native strncpy7C9266 DWORD overreads apply to cached INI value/default
    # sources owned by the existing cache, never these key/category literals.
    (0x81ABF0, 15),  # SecretInfantry;push66FA25.
    (0x81C014, 6),  # RADAR;push47726F.
    (0x81C01C, 9),  # BARRACKS;push477211.
    (0x81C028, 8),  # FACTORY;push4771B3.
    (0x81C030, 6),  # POWER;push477153.
    (0x81C1C0, 5),  # PROC;push47732B.
    (0x81C1C8, 5),  # TECH;push4772CD.
    (0x82596C, 9),  # Engineer;push66FC88.
    (0x825A20, 11),  # DeadBodies;push66D9A2.
    (0x83B404, 15),  # TalkBubbleTime;push671E69.
    (0x83B414, 21),  # EngineerCaptureLevel;push671E03, 671E2A.
    (0x83B43C, 22),  # MaxWaypointPathLength;push671DBF.
    (0x83B454, 21),  # MaximumQueuedObjects;push671D9F.
    (0x83B46C, 26),  # InfantryBlinkDisguiseTime;push671D7F.
    (0x83B488, 23),  # DefaultMirageDisguises;push671D51.
    (0x83B4A0, 18),  # VeinholeTypeClass;push671D32.
    (0x83B4B4, 11),  # VeinDamage;push671D12.
    (0x83B4C0, 19),  # VeinholeShrinkRate;push671CF2.
    (0x83B4D4, 19),  # VeinholeGrowthRate;push671CD3.
    (0x83B4E8, 18),  # MaxVeinholeGrowth;push671CB3.
    (0x83B4FC, 24),  # VeinholeMonsterStrength;push671C93.
    (0x83B514, 22),  # EnemyHouseThreatBonus;push671C74.
    (0x83B52C, 30),  # DumbTargetDistanceCoefficient;push671C4D.
    (0x83B54C, 30),  # DumbTargetStrengthCoefficient;push671C26.
    (0x83B56C, 35),  # DumbTargetSpecialThreatCoefficient;push671BFF.
    (0x83B590, 35),  # DumbTargetEffectivenessCoefficient;push671BD8.
    (0x83B5B4, 31),  # DumbMyEffectivenessCoefficient;push671BB1.
    (0x83B5D4, 33),  # TargetDistanceCoefficientDefault;push671B8A.
    (0x83B5F8, 33),  # TargetStrengthCoefficientDefault;push671B63.
    (0x83B61C, 38),  # TargetSpecialThreatCoefficientDefault;push671B3C.
    (0x83B644, 38),  # TargetEffectivenessCoefficientDefault;push671B15.
    (0x83B66C, 34),  # MyEffectivenessCoefficientDefault;push671AEE.
    (0x83B690, 21),  # RadarEventColorSpeed;push671ACA.
    (0x83B6A8, 20),  # RadarEventMinRadius;push671AAB.
    (0x83B6BC, 20),  # RadarEventDurations;push671A7F.
    (0x83B6D0, 30),  # RadarEventVisibilityDurations;push671A46.
    (0x83B6F0, 31),  # RadarEventSuppressionDistances;push671A0C.
    (0x83B710, 24),  # RadarEventRotationSpeed;push6719E2.
    (0x83B728, 16),  # RadarEventSpeed;push6719BF.
    (0x83B738, 21),  # RadarCombatFlashTime;push671999.
    (0x83B750, 15),  # FlashFrameTime;push671979.
    (0x83B760, 13),  # WeedCapacity;push67195A.
    (0x83B770, 32),  # AITriggerTrackRecordCoefficient;push67193A.
    (0x83B790, 28),  # AITriggerFailureWeightDelta;push671913.
    (0x83B7AC, 28),  # AITriggerSuccessWeightDelta;push6718EC.
    (0x83B7C8, 32),  # ConditionRedSparkingProbability;push6718C5.
    (0x83B7E8, 35),  # ConditionYellowSparkingProbability;push67189E.
    (0x83B80C, 26),  # WallBuildSpeedCoefficient;push671877.
    (0x83B828, 19),  # ChargeToDrainRatio;push671850.
    (0x83B83C, 20),  # RevealTriggerRadius;push671829.
    (0x83B850, 16),  # SpotlightRadius;push671809.
    (0x83B860, 15),  # SpotlightAngle;push6717EA.
    (0x83B870, 22),  # SpotlightAcceleration;push6717C3.
    (0x83B888, 15),  # SpotlightSpeed;push67179C.
    (0x83B898, 24),  # SpotlightLocationRadius;push671775.
    (0x83B8B0, 24),  # SpotlightMovementRadius;push671755.
    (0x83B8C8, 15),  # ParadropRadius;push671735.
    (0x83B8D8, 10),  # CMislType;push671717.
    (0x83B8E4, 15),  # CMislLazyCurve;push6716F7.
    (0x83B8F4, 16),  # CMislBodyLength;push6716D8.
    (0x83B904, 17),  # CMislEliteDamage;push6716B8.
    (0x83B918, 12),  # CMislDamage;push671698.
    (0x83B924, 14),  # CMislAltitude;push671673.
    (0x83B934, 18),  # CMislAcceleration;push67165B.
    (0x83B948, 15),  # CMislRaiseRate;push67162F.
    (0x83B958, 14),  # CMislTurnRate;push67160C.
    (0x83B968, 16),  # CMislPitchFinal;push6715E8.
    (0x83B978, 18),  # CMislPitchInitial;push6715C1.
    (0x83B98C, 16),  # CMislTiltFrames;push67159C.
    (0x83B99C, 17),  # CMislPauseFrames;push67157D.
    (0x83B9B0, 10),  # DMislType;push67155E.
    (0x83B9BC, 15),  # DMislLazyCurve;push67153E.
    (0x83B9CC, 16),  # DMislBodyLength;push67151E.
    (0x83B9DC, 17),  # DMislEliteDamage;push6714FE.
    (0x83B9F0, 12),  # DMislDamage;push6714DF.
    (0x83B9FC, 14),  # DMislAltitude;push6714BF.
    (0x83BA0C, 18),  # DMislAcceleration;push6714A1.
    (0x83BA20, 15),  # DMislRaiseRate;push671478.
    (0x83BA30, 14),  # DMislTurnRate;push671451.
    (0x83BA40, 16),  # DMislPitchFinal;push67142E.
    (0x83BA50, 18),  # DMislPitchInitial;push67140A.
    (0x83BA64, 16),  # DMislTiltFrames;push6713E3.
    (0x83BA74, 17),  # DMislPauseFrames;push6713C3.
    (0x83BA88, 13),  # V3RocketType;push6713A4.
    (0x83BA98, 18),  # V3RocketLazyCurve;push671384.
    (0x83BAAC, 19),  # V3RocketBodyLength;push671364.
    (0x83BAC0, 20),  # V3RocketEliteDamage;push671345.
    (0x83BAD4, 15),  # V3RocketDamage;push671325.
    (0x83BAE4, 17),  # V3RocketAltitude;push671305.
    (0x83BAF8, 21),  # V3RocketAcceleration;push6712E6.
    (0x83BB10, 18),  # V3RocketRaiseRate;push6712BE.
    (0x83BB24, 17),  # V3RocketTurnRate;push671298.
    (0x83BB38, 19),  # V3RocketPitchFinal;push671273.
    (0x83BB4C, 21),  # V3RocketPitchInitial;push671250.
    (0x83BB64, 19),  # V3RocketTiltFrames;push67122A.
    (0x83BB78, 20),  # V3RocketPauseFrames;push67120A.
    (0x83BB8C, 19),  # PrismSupportHeight;push6711EB.
    (0x83BBA0, 21),  # PrismSupportDuration;push6711CB.
    (0x83BBB8, 18),  # PrismSupportDelay;push6711AB.
    (0x83BBCC, 16),  # PrismSupportMax;push67118C.
    (0x83BBDC, 21),  # PrismSupportModifier;push671161.
    (0x83BBF4, 10),  # PrismType;push67113D.
    (0x83BC00, 16),  # MutateExplosion;push67111D.
    (0x83BC10, 29),  # ForceShieldPlayFadeSoundTime;push6710FE.
    (0x83BC30, 28),  # ForceShieldBlackoutDuration;push6710DE.
    (0x83BC4C, 20),  # ForceShieldDuration;push6710BE.
    (0x83BC60, 18),  # ForceShieldRadius;push67109F.
    (0x83BC74, 19),  # LightningPrintText;push67107F.
    (0x83BC88, 17),  # LightningWarhead;push671060.
    (0x83BC9C, 20),  # LightningSeparation;push671040.
    (0x83BCB0, 20),  # LightningCellSpread;push671020.
    (0x83BCC4, 22),  # LightningScatterDelay;push671001.
    (0x83BCDC, 18),  # LightningHitDelay;push670FE1.
    (0x83BCF0, 23),  # LightningStormDuration;push670FC1.
    (0x83BD08, 16),  # LightningDamage;push670FA2.
    (0x83BD18, 19),  # LightningDeferment;push670F82.
    (0x83BD2C, 21),  # TiberiumTransmogrify;push670F62.
    (0x83BD44, 24),  # LeptonsPerSightIncrease;push670F43.
    (0x83BD5C, 28),  # AttackingAircraftSightRange;push670F26.
    (0x83BD78, 11),  # BlendedFog;push670F09.
    (0x83BD84, 12),  # CloseEnough;push670EEA.
    (0x83BD90, 15),  # GuardModeStray;push670ECA.
    (0x83BDA0, 13),  # RelaxedStray;push670EAA.
    (0x83BDB0, 6),  # Stray;push670E8B.
    (0x83BDB8, 12),  # IRepairRate;push670E6B.
    (0x83BDC4, 12),  # URepairRate;push670E44.
    (0x83BDD0, 11),  # RepairRate;push670E1D.
    (0x83BDDC, 12),  # IRepairStep;push670DF6.
    (0x83BDE8, 11),  # RepairStep;push670DD6.
    (0x83BDF4, 14),  # RepairPercent;push670DB7.
    (0x83BE04, 14),  # RefundPercent;push670D90.
    (0x83BE14, 11),  # GrowthRate;push670D69.
    (0x83BE20, 12),  # DamageDelay;push670D42.
    (0x83BE2C, 11),  # BuildSpeed;push670D1B.
    (0x83BE38, 18),  # HarvesterLoadRate;push670CF4.
    (0x83BE4C, 18),  # HarvesterDumpRate;push670CD4.
    (0x83BE60, 12),  # BuildupTime;push670CAD.
    (0x83BE6C, 11),  # ReloadRate;push670C86.
    (0x83BE78, 21),  # ThirdSurvivorDivisor;push670C5F.
    (0x83BE90, 22),  # SovietSurvivorDivisor;push670C3F.
    (0x83BEA8, 22),  # AlliedSurvivorDivisor;push670C20.
    (0x83BEC0, 13),  # SurvivorRate;push670C00.
    (0x83BED0, 13),  # SuspendDelay;push670BD9.
    (0x83BEE0, 16),  # SuspendPriority;push670BB2.
    (0x83BEF0, 17),  # BaseDefenseDelay;push670B92.
    (0x83BF04, 17),  # SeparateAircraft;push670B6C.
    (0x83BF18, 9),  # BaseBias;push670B4D.
    (0x83BF24, 14),  # GameSpeedBias;push670B26.
    (0x83BF34, 11),  # CloakDelay;push670AFF.
    (0x83BF40, 23),  # AIIonCannonTempleValue;push670AC8.
    (0x83BF58, 24),  # AIIonCannonHelipadValue;push670A8F.
    (0x83BF70, 21),  # AIIonCannonPlugValue;push670A55.
    (0x83BF88, 28),  # AIIonCannonBaseDefenseValue;push670A1B.
    (0x83BFA4, 20),  # AIIonCannonAPCValue;push6709E2.
    (0x83BFB8, 20),  # AIIonCannonMCVValue;push6709A8.
    (0x83BFCC, 26),  # AIIonCannonHarvesterValue;push67096E.
    (0x83BFE8, 22),  # AIIonCannonThiefValue;push670935.
    (0x83C000, 25),  # AIIonCannonEngineerValue;push6708FB.
    (0x83C01C, 27),  # AIIonCannonTechCenterValue;push6708C1.
    (0x83C038, 22),  # AIIonCannonPowerValue;push670888.
    (0x83C050, 27),  # AIIonCannonWarFactoryValue;push67084E.
    (0x83C06C, 24),  # AIIonCannonConYardValue;push670814.
    (0x83C084, 15),  # AnimToInfantry;push6707DC.
    (0x83C094, 16),  # YuriParaDropNum;push6707AC.
    (0x83C0A4, 16),  # YuriParaDropInf;push670774.
    (0x83C0B4, 15),  # SovParaDropNum;push670744.
    (0x83C0C4, 15),  # SovParaDropInf;push67070C.
    (0x83C0D4, 16),  # AllyParaDropNum;push6706DC.
    (0x83C0E4, 16),  # AllyParaDropInf;push6706A4.
    (0x83C0F4, 16),  # AmerParaDropNum;push670674.
    (0x83C104, 16),  # AmerParaDropInf;push67063C.
    (0x83C114, 18),  # AIExtraRefineries;push67060C.
    (0x83C128, 22),  # HarvestersPerRefinery;push6705D3.
    (0x83C140, 19),  # AISlaveMinerNumber;push670599.
    (0x83C154, 19),  # AIVirtualPurifiers;push67055F.
    (0x83C168, 16),  # MultiplayerAICM;push670526.
    (0x83C178, 21),  # AICaptureWoundedMark;push6704FE.
    (0x83C190, 22),  # AICaptureLowMoneyMark;push6704D8.
    (0x83C1A8, 18),  # AICaptureLowMoney;push6704A8.
    (0x83C1BC, 18),  # AICaptureLowPower;push67046E.
    (0x83C1D0, 17),  # AICaptureWounded;push670435.
    (0x83C1E4, 16),  # AICaptureNormal;push6703FB.
    (0x83C1F4, 23),  # AISuperDefenseDistance;push6703D1.
    (0x83C20C, 21),  # AISuperDefenseFrames;push6703B1.
    (0x83C224, 26),  # AISuperDefenseProbability;push670381.
    (0x83C240, 25),  # SlaveMinerKickFrameDelay;push670357.
    (0x83C25C, 25),  # SlaveMinerScanCorrection;push670337.
    (0x83C278, 19),  # SlaveMinerLongScan;push670317.
    (0x83C28C, 20),  # SlaveMinerSlaveScan;push6702F8.
    (0x83C2A0, 20),  # SlaveMinerShortScan;push6702D8.
    (0x83C2B4, 17),  # TiberiumLongScan;push6702B8.
    (0x83C2C8, 18),  # TiberiumShortScan;push670299.
    (0x83C2DC, 33),  # MaximumBuildingPlacementFailures;push670279.
    (0x83C300, 23),  # AIAutoDeployFrameDelay;push670249.
    (0x83C318, 33),  # DisabledDisguiseDetectionPercent;push67020F.
    (0x83C33C, 21),  # AINavalYardAdjacency;push6701E6.
    (0x83C354, 21),  # NormalTargetingDelay;push6701C6.
    (0x83C36C, 24),  # GuardAreaTargetingDelay;push6701A7.
    (0x83C384, 23),  # CampaignMoneyDeltaHard;push670187.
    (0x83C39C, 23),  # CampaignMoneyDeltaEasy;push670167.
    (0x83C3B4, 30),  # ApproachTargetResetMultiplier;push670148.
    (0x83C3D4, 18),  # ThreatPerOccupant;push670128.
    (0x83C3E8, 22),  # AIRestrictReplaceTime;push670103.
    (0x83C400, 25),  # AIPickWallDefensePercent;push6700D9.
    (0x83C41C, 23),  # ThirdBaseDefenseCounts;push6700A0.
    (0x83C434, 24),  # SovietBaseDefenseCounts;push670066.
    (0x83C44C, 24),  # AlliedBaseDefenseCounts;push67002C.
    (0x83C464, 25),  # ChronoHarvTooFarDistance;push670003.
    (0x83C480, 24),  # HarvesterTooFarDistance;push66FFE3.
    (0x83C498, 25),  # AIMinorSuperReadyPercent;push66FFC4.
    (0x83C4B4, 15),  # AISafeDistance;push66FF9F.
    (0x83C4C4, 26),  # DissolveUnfilledTeamDelay;push66FF80.
    (0x83C4E0, 18),  # UseMinDefenseRule;push66FF60.
    (0x83C4F4, 15),  # TotalAITeamCap;push66FF30.
    (0x83C504, 24),  # MaximumAIDefensiveTeams;push66FEF6.
    (0x83C51C, 24),  # MinimumAIDefensiveTeams;push66FEBD.
    (0x83C534, 28),  # FillEarliestTeamProbability;push66FE83.
    (0x83C550, 14),  # AIBuildsWalls;push66FE59.
    (0x83C560, 17),  # NodAIBuildsWalls;push66FE39.
    (0x83C574, 31),  # AIUseTurbineUpgradeProbability;push66FE19.
    (0x83C594, 34),  # AIAlternateProductionCreditCutoff;push66FDF3.
    (0x83C5B8, 13),  # AIHateDelays;push66FDC4.
    (0x83C5C8, 11),  # TeamDelays;push66FD8B.
    (0x83C5D4, 16),  # FineDiffControl;push66FD61.
    (0x83C5E4, 14),  # CurleyShuffle;push66FD42.
    (0x83C5F4, 10),  # ThirdCrew;push66FD23.
    (0x83C600, 11),  # SovietCrew;push66FD04.
    (0x83C60C, 11),  # AlliedCrew;push66FCE5.
    (0x83C618, 6),  # Pilot;push66FCC6.
    (0x83C620, 11),  # Technician;push66FCA7.
    (0x83C62C, 14),  # PurifierBonus;push66FC6A.
    (0x83C63C, 23),  # AttackCursorOnDisguise;push66FC43.
    (0x83C654, 21),  # SpyMoneyStealPercent;push66FC25.
    (0x83C66C, 17),  # SpyPowerBlackout;push66FBFE.
    (0x83C680, 14),  # ThirdDisguise;push66FBDF.
    (0x83C690, 15),  # SovietDisguise;push66FBC0.
    (0x83C6A0, 15),  # AlliedDisguise;push66FBA1.
    (0x83C6B0, 19),  # ChronoRangeMinimum;push66FB81.
    (0x83C6C4, 19),  # ChronoMinimumDelay;push66FB61.
    (0x83C6D8, 14),  # ChronoTrigger;push66FB42.
    (0x83C6E8, 21),  # ChronoDistanceFactor;push66FB22.
    (0x83C700, 17),  # ChronoReinfDelay;push66FB02.
    (0x83C714, 12),  # ChronoDelay;push66FAE3.
    (0x83C720, 16),  # SecretBuildings;push66FA87.
    (0x83C730, 12),  # SecretUnits;push66FA54.
    (0x83C73C, 12),  # Paratrooper;push66FA09.
    (0x83C748, 12),  # PadAircraft;push66F9D8.
    (0x83C754, 14),  # HarvesterUnit;push66F8DD.
    (0x83C764, 9),  # BaseUnit;push66F7DA.
    (0x83C770, 26),  # PrerequisiteProcAlternate;push66F7A2.
    (0x83C78C, 16),  # ThirdPowerPlant;push66F763.
    (0x83C79C, 17),  # NodAdvancedPower;push66F724.
    (0x83C7B0, 16),  # NodRegularPower;push66F6E6.
    (0x83C7C0, 14),  # GDIPowerPlant;push66F6A7.
    (0x83C7D0, 9),  # Shipyard;push66F59E.
    (0x83C7DC, 10),  # WallTower;push66F565.
    (0x83C7E8, 11),  # NodGateTwo;push66F526.
    (0x83C7F4, 11),  # NodGateOne;push66F4E8.
    (0x83C800, 11),  # GDIGateTwo;push66F4A9.
    (0x83C80C, 11),  # GDIGateOne;push66F46A.
    (0x83C818, 10),  # RepairBay;push66F362.
    (0x83C824, 23),  # NoParachuteMaxFallRate;push66F33A.
    (0x83C83C, 21),  # ParachuteMaxFallRate;push66F31B.
    (0x83C854, 12),  # FlightLevel;push66F2FB.
    (0x83C860, 12),  # CameraRange;push66F2DB.
    (0x83C86C, 14),  # WindDirection;push66F2BC.
    (0x83C87C, 16),  # WheeledDownhill;push66F29C.
    (0x83C88C, 14),  # WheeledUphill;push66F275.
    (0x83C89C, 16),  # TrackedDownhill;push66F24E.
    (0x83C8AC, 14),  # TrackedUphill;push66F227.
    (0x83C8BC, 15),  # PlacementDelay;push66F200.
    (0x83C8CC, 23),  # CliffBackImpassability;push66F1D9.
    (0x83C8E4, 18),  # IceBreakingWeight;push66F1B8.
    (0x83C8F8, 18),  # IceCrackingWeight;push66F192.
    (0x83C90C, 18),  # ShipSinkingWeight;push66F16C.
    (0x83C920, 15),  # CloakingStages;push66F146.
    (0x83C930, 17),  # ScrapVoxelDebris;push66F116.
    (0x83C944, 16),  # TireVoxelDebris;push66F0D7.
    (0x83C954, 15),  # BridgeVoxelMax;push66F0A9.
    (0x83C964, 21),  # ExplosiveVoxelDebris;push66EFAF.
    (0x83C97C, 11),  # VeteranCap;push66EF87.
    (0x83C988, 11),  # VeteranROF;push66EF61.
    (0x83C994, 13),  # VeteranArmor;push66EF3B.
    (0x83C9A4, 13),  # VeteranSight;push66EF15.
    (0x83C9B4, 13),  # VeteranSpeed;push66EEEF.
    (0x83C9C4, 14),  # VeteranCombat;push66EEC9.
    (0x83C9D4, 13),  # VeteranRatio;push66EEA3.
    (0x83C9E4, 11),  # HoverBrake;push66EE7D.
    (0x83C9F0, 18),  # HoverAcceleration;push66EE57.
    (0x83CA04, 11),  # HoverBoost;push66EE31.
    (0x83CA10, 12),  # HoverHeight;push66EE0B.
    (0x83CA1C, 9),  # HoverBob;push66EDEC.
    (0x83CA28, 12),  # HoverDampen;push66EDC5.
    (0x83CA34, 12),  # TunnelSpeed;push66EDA1.
    (0x83CA40, 11),  # CrewEscape;push66ED80.
    (0x83CA4C, 13),  # DropPodAngle;push66ED1B.
    (0x83CA5C, 13),  # DropPodSpeed;push66ECF4.
    (0x83CA6C, 14),  # DropPodHeight;push66ECD4.
    (0x83CA7C, 14),  # DropPodWeapon;push66ECA3.
    (0x83CA8C, 16),  # MissileSpeedVar;push66EC76.
    (0x83CA9C, 22),  # MissileSafetyAltitude;push66EC4F.
    (0x83CAB4, 14),  # MissileROTVar;push66EC2F.
    (0x83CAC4, 17),  # TreeFlammability;push66EC08.
    (0x83CAD8, 17),  # MaximumCheerRate;push66EBE1.
    (0x83CAEC, 16),  # MultipleFactory;push66EBC3.
    (0x83CAFC, 24),  # LowPowerPenaltyModifier;push66EB9F.
    (0x83CB14, 27),  # MaxLowPowerProductionSpeed;push66EB78.
    (0x83CB30, 27),  # MinLowPowerProductionSpeed;push66EB55.
    (0x83CB4C, 18),  # AircraftFogReveal;push66EB2F.
    (0x83CB60, 31),  # AllowShroudedSubteranneanMoves;push66EB0F.
    (0x83CB80, 15),  # RevealByHeight;push66EAF0.
    (0x83CB90, 13),  # ZoomInFactor;push66EAD0.
    (0x83CBA0, 17),  # PrerequisiteProc;push66EA4A.
    (0x83CBB4, 17),  # PrerequisiteTech;push66E9B7.
    (0x83CBC8, 18),  # PrerequisiteRadar;push66E923.
    (0x83CBDC, 21),  # PrerequisiteBarracks;push66E890.
    (0x83CBF4, 20),  # PrerequisiteFactory;push66E7FC.
    (0x83CC08, 18),  # PrerequisitePower;push66E763.
    (0x83CC1C, 19),  # SelfHealUnitAmount;push66E738.
    (0x83CC30, 19),  # SelfHealUnitFrames;push66E71F.
    (0x83CC44, 23),  # SelfHealInfantryAmount;push66E705.
    (0x83CC5C, 23),  # SelfHealInfantryFrames;push66E6EB.
    (0x83CC74, 13),  # TiberiumHeal;push66E6D2.
    (0x83CC84, 15),  # SmallVisceroid;push66E6A3.
    (0x83CC94, 15),  # LargeVisceroid;push66E66A.
    (0x83CCA4, 16),  # EMPulseSparkles;push66E62E.
    (0x83CCB4, 13),  # DropZoneAnim;push66E5F0.
    (0x83CCC4, 14),  # BombParachute;push66E5B1.
    (0x83CCD4, 10),  # Parachute;push66E572.
    (0x83CCE0, 10),  # MoveFlash;push66E534.
    (0x83CCEC, 7),  # Behind;push66E4F5.
    (0x83CCF4, 15),  # InfantryMutate;push66E4B6.
    (0x83CD04, 14),  # InfantryBrute;push66E478.
    (0x83CD14, 14),  # InfantryVirus;push66E439.
    (0x83CD24, 14),  # InfantryNuked;push66E3FA.
    (0x83CD34, 16),  # InfantryHeadPop;push66E3BC.
    (0x83CD44, 16),  # FlamingInfantry;push66E37D.
    (0x83CD54, 16),  # InfantryExplode;push66E33E.
    (0x83CD64, 15),  # ChronoSparkle1;push66E300.
    (0x83CD74, 18),  # WeaponNullifyAnim;push66E2C1.
    (0x83CD88, 22),  # ForceShieldInvokeAnim;push66E282.
    (0x83CDA0, 22),  # IronCurtainInvokeAnim;push66E244.
    (0x83CDB8, 9),  # WarpAway;push66E205.
    (0x83CDC4, 8),  # WarpOut;push66E1C6.
    (0x83CDCC, 7),  # WarpIn;push66E188.
    (0x83CDD4, 16),  # ChronoBlastDest;push66E149.
    (0x83CDE4, 12),  # ChronoBlast;push66E10A.
    (0x83CDF0, 11),  # ChronoBeam;push66E0CC.
    (0x83CDFC, 16),  # ChronoPlacement;push66E08D.
    (0x83CE0C, 16),  # DominatorDamage;push66E05F.
    (0x83CE1C, 22),  # DominatorCaptureRange;push66E040.
    (0x83CE34, 26),  # DominatorFireAtPercentage;push66E020.
    (0x83CE50, 20),  # DominatorSecondAnim;push66DFEF.
    (0x83CE64, 19),  # DominatorFirstAnim;push66DFB1.
    (0x83CE78, 17),  # DominatorWarhead;push66DF72.
    (0x83CE8C, 24),  # WeatherConBoltExplosion;push66DF33.
    (0x83CEA4, 16),  # WeatherConBolts;push66DE2B.
    (0x83CEB4, 17),  # WeatherConClouds;push66DD28.
    (0x83CEC8, 8),  # IonBeam;push66DCEF.
    (0x83CED0, 9),  # IonBlast;push66DCB0.
    (0x83CEDC, 17),  # BridgeExplosions;push66DBA8.
    (0x83CEF0, 15),  # MetallicDebris;push66DAA5.
    (0x83CF00, 8),  # DropPod;push66D8A0.
    (0x83CF08, 5),  # Wake;push66D867.
    (0x83CF10, 12),  # NukeTakeOff;push66D829.
    (0x83CF1C, 15),  # BarrelParticle;push66D7ED.
    (0x83CF2C, 13),  # BarrelDebris;push66D6ED.
    (0x83CF3C, 14),  # BarrelExplode;push66D6B7.
    (0x83CF4C, 11),  # OreTwinkle;push66D67B.
    (0x83CF58, 16),  # DamageFireTypes;push66D573.
)
