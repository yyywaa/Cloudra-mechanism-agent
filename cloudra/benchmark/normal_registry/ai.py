"""A 族 + I 族登记（v3 缩减后）：A2 丙酮自缩合 → 异亚丙基丙酮（E1cb，5 步）、
A5 Mannich 酸催化（5 步）、I1 甲醛+甲胺 → 亚胺（2 步）。

v3（2026-09-09）将本族收窄为这三条多步网络；A1/A4/A7/I3 剔出定稿名单留档池
（条目见 normal.md）。竞争通道（A5 的双烷基化等）按 normal.md 约定不进 gold。
"""

TASKS = {
    # [OH-].CC(=O)C.CC(=O)C>>[OH-].CC(=O)C=C(C)C.O  (−1/1)
    # 丙酮自缩合 → 异亚丙基丙酮；α-C（C2）上两个参与键变化的 H（H3 步1、H11 步4）全程显式
    "A2": {
        "name_en": "acetone self-aldol condensation -> mesityl oxide (4-methylpent-3-en-2-one)",
        "conditions_en": "gas phase; NaOH or Ba(OH)2, heated",
        "mapped_reactants": "[OH-:1].[CH:2]([H:3])([H:11])[C:4](=[O:5])[CH3:6].[CH3:7][C:8](=[O:9])[CH3:10]",
        "steps": [
            {
                # OH- 拔 H3：断 C2-H3，成 O1-H3，C2-C4 1->2，C4-O5 2->1 → 烯醇盐 + 水
                "out": "[OH:1]([H:3]).[CH:2]([H:11])=[C:4]([O-:5])[CH3:6].[CH3:7][C:8](=[O:9])[CH3:10]",
                "type": "enolate formation: OH- deprotonates the alpha-C of acetone (C=O pi shifts to C=C)",
                "barrier": 3.4,
            },
            {
                # 烯醇盐 C2 进攻第二分子丙酮羰基 C8：成 C2-C8，断 C8=O9 pi、C2=C4 pi，成 C4=O5 pi → 双丙酮醇烷氧盐
                # 战役（WSL/G16 气相）：1D 路径证实为约束伪脊，无介入鞍点 → 撤回旧 5.0 锚值
                "out": "[OH:1]([H:3]).[CH3:7][C:8]([O-:9])([CH3:10])[CH:2]([H:11])[C:4](=[O:5])[CH3:6]",
                "type": "C-C addition: enolate carbon attacks the second acetone carbonyl -> diacetone alcohol alkoxide (capturable)",
            },
            {
                # 烷氧盐 O9 从水夺回 H3：断 O1-H3，成 O9-H3 → 双丙酮醇 + OH-
                "out": "[OH-:1].[CH3:7][C:8]([O:9]([H:3]))([CH3:10])[CH:2]([H:11])[C:4](=[O:5])[CH3:6]",
                "type": "alkoxide reprotonation by water -> diacetone alcohol, regenerating OH-",
                "barrier": 0.0,
            },
            {
                # E1cb 第一步：OH- 拔 C2 上另一个 alpha-H（H11）：断 C2-H11，成 O1-H11，C2-C4 1->2，C4-O5 2->1
                "out": "[OH:1]([H:11]).[CH3:7][C:8]([O:9]([H:3]))([CH3:10])[CH:2]=[C:4]([O-:5])[CH3:6]",
                "type": "E1cb deprotonation: OH- removes the alpha-H on the other side of the carbinol -> enolate + water",
                "barrier": 32.5,
            },
            {
                # 消除：断 C8-O9，成 C2=C8 pi，C2=C4 pi 回落、C4=O5 pi 重建 → 异亚丙基丙酮 + OH- + 水
                "out": "[OH:1]([H:11]).[O-:9]([H:3]).[CH3:7][C:8]([CH3:10])=[CH:2][C:4](=[O:5])[CH3:6]",
                "type": "E1cb elimination: hydroxide leaves with C=C formation (enolate collapse), giving mesityl oxide",
            },
        ],
    },
    # C=O.O=C(O)CC(=O)O.CNC>>C=CC(=O)O.C(=O)=O.O.CNC  (0/1)
    # Knoevenagel 亚铵路径；丙二酸中央 C（C3）的 H4（步2 被拔）与羧基 O7 的 H8
    # [OH3+].C=O.CN.CC=O>>[OH3+].CNCCC=O.O  (+1/1)
    # Mannich 酸催化；H2（H3O+ 的质子，步2 转给羟胺 O 随水离去）、H7（甲胺 N-H，步1 转 O）、
    # H11（乙醛 alpha-H，步3 转烯醇 O、步5 转回 H3O+）全程显式
    "A5": {
        "name_en": "Mannich reaction: formaldehyde + methylamine + acetaldehyde -> 3-(methylamino)propanal (acid-catalyzed)",
        "conditions_en": "weakly acidic water/alcohol solution (acid catalysis written as [OH3+] into the SMILES on both sides)",
        "mapped_reactants": "[OH2+:1]([H:2]).[CH2:3]=[O:4].[CH3:6][NH:5]([H:7]).[CH2:8]([H:11])[CH:9]=[O:10]",
        "steps": [
            {
                # 甲胺 N5 进攻甲醛 C1...（成 C3-N5），断 C3=O4 pi；N-H->O-H 分子内 PT 并入（断 N5-H7，成 O4-H7）→ 羟胺
                "out": "[OH2+:1]([H:2]).[O:4]([H:7])[CH2:3][NH:5][CH3:6].[CH2:8]([H:11])[CH:9]=[O:10]",
                "type": "methylamine addition to formaldehyde with merged intramolecular N-H -> O-H proton transfer -> carbinolamine",
            },
            {
                # H3O+ 质子化羟胺 O4 并脱水：断 O1-H2、成 O4-H2、断 C3-O4、成 C3=N5 pi → 亚铵 + 2 水
                "out": "[OH2:1].[O:4]([H:2])([H:7]).[CH2:3]=[NH+:5][CH3:6].[CH2:8]([H:11])[CH:9]=[O:10]",
                "type": "carbinolamine O protonation by H3O+ with dehydration -> iminium [CH2=NHMe]+ (Eschenmoser salt parent) + 2 water",
            },
            {
                # 乙醛互变异构为烯醇（净步）：断 C8-H11、断 C9=O10 pi、成 C8=C9 pi、成 O10-H11
                "out": "[OH2:1].[O:4]([H:2])([H:7]).[CH2:3]=[NH+:5][CH3:6].[CH2:8]=[CH:9][O:10][H:11]",
                "type": "acetaldehyde tautomerizes to the enol (net step: alpha-C-H breaks, C=O pi shifts to C=C, O-H forms)",
            },
            {
                # 烯醇 alpha-C（C8）进攻亚铵 C3（决速）：成 C3-C8，断 C8=C9 pi、C3=N5 pi，成 C9=O10+ pi（氧鎓，N 变中性）
                "out": "[OH2:1].[O:4]([H:2])([H:7]).[CH3:6][NH:5][CH2:3][CH2:8][CH:9]=[O+:10][H:11]",
                "type": "rate-determining C-C formation: enol alpha-carbon attacks the iminium carbon -> oxocarbenium (neutral amine)",
            },
            {
                # 水拔氧鎓质子：断 O10-H11，成 O1-H11，再生 H3O+ → Mannich 碱
                "out": "[OH2+:1]([H:11]).[O:4]([H:2])([H:7]).[CH3:6][NH:5][CH2:3][CH2:8][CH:9]=[O:10]",
                "type": "water deprotonates the oxocarbenium, regenerating H3O+ -> Mannich base",
            },
        ],
    },
    # [OH-].C[N+](=O)[O-].C=CC=O>>[OH-].O=CCCC[N+](=O)[O-]  (−1/1)
    # C=O.CN>>C=NC.O  (0/1)  亚胺形成（无显式催化剂）；甲胺两个 N-H（H5/H6）均参与键变化，全程显式
    "I1": {
        "name_en": "imine formation: formaldehyde + methylamine -> N-methylmethanimine + water",
        "conditions_en": "gas phase; optimal around pH 4-6 (bell-shaped rate profile)",
        "mapped_reactants": "[CH2:1]=[O:2].[CH3:4][N:3]([H:5])([H:6])",
        # barrier：B3LYP-D3(BJ)/def2-SVP 气相（带色散，与固定方法对齐）自算，
        # 取自 benchmark 批次 batch_e641f28484b74786 沙箱 NI1 原始日志
        # （agent 交付，逐日志复核：极小值 0 虚频、TS 恰 1 虚频，能量为各日志
        # 末条 FINAL SINGLE POINT ENERGY）：E1 = E(TS1) − E(RC) = 27.90；
        # E2 = E(TS2) − E(carbinolamine) = 57.67。⚠ IRC 每边仅一向收敛、端点
        # 未重优化闭合（已在案）；旧占位值 29.33/58.22（无 D3(BJ) 的早期交付）被替换。
        # 水溶液对偶版单开 I5。
        "steps": [
            {
                # 加成 + 分子内 PT 并入：成 C1-N3，断 C1=O2 pi、断 N3-H5、成 O2-H5 → 羟胺 HOCH2NHMe
                "out": "[O:2]([H:5])[CH2:1][N:3]([H:6])[CH3:4]",
                "type": "amine addition to the carbonyl with merged intramolecular N-H -> O-H proton transfer -> carbinolamine (capturable)",
                "barrier": 27.90,
                "weight": 0.5,
            },
            {
                # 直接脱水：断 C1-O2、断 N3-H6，成 C1=N3 pi、成 O2-H6 → 亚胺 + 水
                "out": "[O:2]([H:5])([H:6]).[CH2:1]=[N:3][CH3:4]",
                "type": "direct dehydration of the carbinolamine: C-O cleavage with the second N-H transferring to the departing oxygen -> N-methylmethanimine + water",
                "barrier": 57.67,
                "weight": 0.5,
            },
        ],
    },
    # C=O.CN>>C=NC.O  (0/1)  亚胺形成·水溶液版（2026-09-25 用户裁决：原 I1 气相版保留，
    # 水溶液对偶单开本题；SMILES 只给净反应式，水与酸催化剂不画进反应物侧）
    "I5": {
        "name_en": "imine formation (aqueous): formaldehyde + methylamine -> N-methylmethanimine + water",
        "conditions_en": "aqueous solution, weakly acidic (pH 4-6, bell-shaped rate profile)",
        "smiles_schematic": True,
        "mapped_reactants": "[CH2:1]=[O:2].[CH3:4][N:3]([H:5])([H:6]).[O:7]([H:8])[H:9]",
        # O7/H8/H9 是接力水；沿用原 map1-6，水的氢交换用自洽参考编号表达。
        # 显式水接力使 C-N 加成与双质子转移解耦：先得两性离子，再经
        # 六元环水接力成羟胺。E2 的 3.59 相对加成中间体·H2O 极小值；
        # E3 的 31.2 相对羟胺·H2O 极小值。题面净反应式省略接力水，
        # Gold 映射结构完整保留；文献两水辅助 ≈ 26.7
        # （Hall & Smith 1998 JPCA 102, 4930, DOI 10.1021/jp9810825）。
        # 其归属（LEDGER 追加裁定 3）：两水辅助 ≈ 26.7 属羟胺→亚胺的 PT/脱水步（非 C-N 加成步）；
        # C-N 加成步的文献锚为 3.5 kcal/mol（同篇；口径与本处 CPCM(水) 自算值不可直接相减）。
        "steps": [
            {
                # E1（C–N 加成）自算能垒 = 0.93 kcal/mol。措辞与口径（2026-10-15 主协调裁定；须称
                # soft-mode-dominated C–N addition saddle，不得写成无修饰的 “C–N 加成 TS”）：
                # 引擎：Gaussian 16（/home/ly/g16/g16），B3LYP/def2SVP + EmpiricalDispersion=GD3BJ
                #   + Int(UltraFine) + SCF=Tight + SCRF=(CPCM,Solvent=Water)，q0/m1；本值为纯电子能（无 ZPE/热校正），
                #   相对本步自身起点极小值 = 题面声明的六元接力环 RC-A（E = -286.605711957 Eh，36 模 0 虚频）。
                #   本机无 ORCA：本步数值来自 Gaussian 16，与紧随其后的 ORCA 5.0.2 值（E2 3.59 / E3 31.2）非同一程序，
                #   不可跨程序混减；相减两端（TS 与 RC-A）取自同一批 Gaussian 16 日志。
                # 鞍点：durable 链 ts/ts_0006（revision 75 / status=ended / result.verified=true）；job 952
                #   ts_opt/refine.log E(TS) = -286.604225293 Eh；job 953 frequency/frequency.log 恰 1 虚频
                #   -164.4792 cm⁻¹（soft mode）。模式归属：含真实 C–N 成键分量（与纯 C1–N6 伸缩的质量加权
                #   |cos| = 0.3657，伸缩成分 13.4%），但振幅由醛基 H3/H4 主导（重原子占比按 |d| 15.3%、d² 3.31%、
                #   质量加权 m·d² 31.7%；watch pair (1,6) 的 pair-projected 占比仅 1.62%）⇒ 属软模主导，偏离
                #   BRIEF §4 第 1 条，如实标注、不硬当 TS。
                # 连通性表述（不得写 “IRC 已双向到达端点”）：受约束单峰（job 923 内区松弛扫描沿 r(C1–N6)
                #   1.6413→3.2413 Å 出现单一内部极大）+ 变分自洽（TS 比受约束峰低 0.074 kcal/mol，区间
                #   0.038–0.086）+ 两端点 0 虚频身份（job 955/956 与 957/958，各 36 模 0 虚频）+ 端点松弛补强
                #   （job 969/970，从 ts/ts_0006/verdict/irc_end_a.xyz | irc_end_b.xyz 出发做无约束 Opt+Freq）。
                #   IRC（job 954）为原生梯度判据早停（每向 1 点，rx = ±0.119），且 run 内两端点 Opt+Freq 的
                #   endpoint_source.json 记 kind=species_reference / irc_job_id=null ⇒ IRC 未用作连通性证据。
                # 残留不确定性：同 R 不同扭转族差异 ±0.24 kcal/mol；参考态敏感性 RC-B -2.713 / RC-C -1.853
                #   （与同一鞍点的连通性未测，不得相加）；相对三分离碎片（E_sum = -286.580238688 Eh）为沉没垒
                #   TS -15.05 / RC -15.99 / 加合物 -20.89 kcal/mol。
                # 记录：gold_finish_20261015/NI5/BACKFILL_DRAFT.md、notes/SELFCHECK.md、notes/IRC_DEEP.md。
                "out": "[O-:2][CH2:1][N+:3]([H:5])([H:6])[CH3:4].[O:7]([H:8])[H:9]",
                "type": "amine addition to the carbonyl -> zwitterionic C-N addition intermediate with one explicit relay water",
                "barrier": 0.93,
            },
            {
                "out": "[O:2]([H:8])[CH2:1][N:3]([H:6])[CH3:4].[O:7]([H:5])[H:9]",
                "type": "six-membered water relay: N3-H5 transfers to water O7 while water H8 transfers to O2 -> carbinolamine with relay water",
                "barrier": 3.59,
            },
            {
                "out": "[CH2:1]=[N:3][CH3:4].[O:2]([H:8])[H:9].[O:7]([H:5])[H:6]",
                "type": "water-relayed dehydration: N3-H6 transfers to water O7 while water H9 transfers to leaving O2 -> N-methylmethanimine, product water and regenerated relay water",
                "barrier": 31.2,
            },
        ],
    },
    # [OH3+].COCOC.O>>[OH3+].C=O.CO.CO  (+1/1)  缩醛 A-1 水解
    # H2（H3O+ 质子，步1 转甲氧基 O4 随 MeOH 离去）、H9（水 O8 的 H，步3 接力转 O1、
}
