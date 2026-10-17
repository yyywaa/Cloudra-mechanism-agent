# NY3 prep 证据溯源（写于 ts_prepare 首次声明前）

日期：2026-10-15 ｜ 包：NY3（as_bf15af420101498f）
工作根：/home/ly/Cloudra-mechanism-agent

## 本文件存在的理由
ts_prepare 的 provided guess 要求 evidence_refs 指向**真实存在的 artifact 文件**（纯文本会被拒）。
本文件即 RC 起点、E1 四元环 TS 初猜的构造链与 sha256 记录。

## 文件（gold_finish_20261015/NY3/prep/）
| 文件 | sha256 | 原子数 | 说明 |
|---|---|---|---|
| rc.xyz | c2e0db4302f9f3c15bd3c28b904a28d3a41a0284a5736c1f807d1b7fd10cf8e3 | 11 | Na⁺ 桥联 O1/O5、O1 对准 C4 的离子-偶极复合物 |
| rc.mol | 11060cbba1f27c339034dc01e0a0cc66f8f677d5206f9b29dd5ee1bc15c6d090 | 11 | 由 format_converter 从 rc.xyz 生成（无键表） |
| i1.xyz | d1b3b5a35548d4c1dd9c02de631ee84894ac2628b884046c28d6d7080354cea3 | 11 | 四面体烷氧盐（E1 产物 = E2 起点） |
| i1.mol | c4165dfc33a88e26990c32b4c3911259ffc1b092b67aeeb1d595bea33feea184 | 11 | builder 原生 MOL（含 bond block + M CHG） |
| ts_e1_guess.xyz | 7115db0d0cb184317a0de03eb1847a0658d043f8e0e2adc6904fafd2a4f0a25d | 11 | E1 四元环（Na–O1···C4–O5）TS 初猜 |
| p.xyz / p.mol | 64b5ac9b... / 165702ab... | 11 | 产物（甲酸根 + 甲醇 + Na⁺） |

## 原子序（1-based，含显式 H）与关键距离（由 prep 道给出，PREP.md 会更完整）
- rc.xyz：1 Na | 2 O1 | 3 H6 | 4 C2 | 5 O3 | 6 C4 | 7 O5 | 8-10 H(C2) | 11 H(C4)
  Na–O1 2.276 / Na–O5 2.274 / O1···C4 2.792 / O1–H6 0.982 / C4=O5 1.228 Å
- i1.xyz：1 Na | 2 C2 | 3 O3 | 4 C4 | 5 O1 | 6 O5(烷氧) | 7-9 H(C2) | 10 H(C4) | 11 H6
  Na–O5 2.166 / Na–O1 2.531 / C4–O1 1.407 / C4–O5 1.309 / C4–O3 1.425 Å
- ts_e1_guess.xyz：原子序同 rc.xyz；C4–O1 2.192 / Na–O1 2.279 / Na–O5 2.252 Å

## 构造链（可审计）
build/g_RC_w283/guided_assembly/assembly/complex_candidate_000.xyz（builder 原生产物）
 → internal_coordinates transform 5 步刚性旋转（不改拓扑、不加约束力）→ rc.xyz。
build/g_TS1_w21/closest_attempt.xyz（FF 受约束组装，O1 最近到 C4 2.54 Å）
 → 5 步刚性旋转 → ts_e1_guess.xyz。

## 边界
本包未提交任何 QM 作业于此阶段；以上均为 RDKit/MMFF 组装与刚性几何变换产物。身份核验以 builder MOL 的 bond block 为准（internal_coordinates 的 RDKit 键感知在含 Na⁺ 复合物上会失败，见 PREP.md）。
