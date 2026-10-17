# NY3 prep 道 · 状态与交接（写于 2026-10-15 18:4x，平台 API 重启窗口前）

道：small_mol / prep（只做非 QM 准备 + 只读取证）｜包 Coordinator：as_7479852819ea48c0｜工作根：/home/ly/Cloudra-mechanism-agent
边界（用户给定，未越界）：**本道不提交任何 QM 作业**（Gaussian/ORCA/xTB/CREST 均未调用）；只在 gold_finish_20261015/NY3/ 内写文件；未写 ts/ 目录、未改平台文件/DB/进程、未 git。

## 1 已完成（全部落盘，可被继承人直接接手）
| 文件 | sha256 | 说明 |
|---|---|---|
| prep/rc.xyz | c2e0db4302f9f3c15bd3c28b904a28d3a41a0284a5736c1f807d1b7fd10cf8e3 | RC：Na⁺ 桥联 O1/O5 且 O1 对准 C4（O1···C4 2.792） |
| prep/i1.xyz | d1b3b5a35548d4c1dd9c02de631ee84894ac2628b884046c28d6d7080354cea3 | I1 四面体烷氧盐（Na–O5 2.166） |
| prep/i2.xyz | 579e33e5ca1404a844e49f9d3c3385ec1b801ec19ee09ee732066c7860b4f665 | I2：Na⁺ 桥联甲酸 O1(2.524)/甲醇盐 O3(2.427) |
| prep/p.xyz | 64b5ac9b3fb41718ff88ec882c1e88974b14186828c394f8ac7bd8ec5f78e796 | P：甲酸根 + 甲醇 + Na⁺（Na–O1 2.433） |
| prep/ts_e1_guess.xyz | 7115db0d0cb184317a0de03eb1847a0658d043f8e0e2adc6904fafd2a4f0a25d | E1 四元环 TS 初猜（C4–O1 2.192） |
| prep/ts_e23_guess.xyz | 8c651f44ae7a7f5bc4b187109c1b4bfaf2f48c86a1899c7154fdedce6ae30399 | E2+E3 六元环 TS 初猜（C4–O3 2.011；O3···H6 1.372 / H6–O1 1.380） |
| prep/i1.mol, prep/p.mol | c4165dfc… / 165702ab… | builder 原生 MOL（含 bond block + M CHG），身份核验用 |
| prep/rc.mol, prep/i2.mol, ts_*.mol | 11060cbb… / 69684485… / 47ddf41e… / 1b7ffab7… | format_converter 产物：**bond 数 0、无 M CHG**（见 PREP_TOOL_REPRO.md P4） |
| prep/PREP.md | c9f0f844714cfd45fe22febc46839968ccbf1a265f13e7f4c697e1979a8be0f8 | 主交付：原子序表/距离表/身份核验/构造链/偏差/申请的计算/上轮核对 |
| prep/TS_DECL_TEMPLATE.md | 05d3a67d24f5fc4ae0cdfaed824ac54697cafd1bd87bb0a011a2c2eb8ea247b2 | explorer 的 A 帖 + B 帖逐字拼接（代落盘） |
| NY3/PREP_TOOL_REPRO.md | 7a7178f8489730bd1a2fcdded06cbbf01e265fd00c2cad4f5052420258d40da3 | P1–P6 工具面最小复现清单（147 行 / 18811 B，**已冻结**，issue #179 comment 用） |
另有 6 个 .zmat（rc/i1/i2/p/ts_e1_guess/ts_e23_guess）+ prep/build/ 下全部源产物与中间几何（guided assembly、轨迹、变换中间帧）。

## 2 关键几何（一眼可用，全部来自真实文件测量）
- rc.xyz：Na–O1 2.276 / Na–O5 2.274 / O1···C4 2.792 / O1–H6 0.982；O1–C4···O5 104.6°（Bürgi–Dunitz 方向）
- ts_e1_guess.xyz：Na–O1 2.279 / Na–O5 2.252 / C4–O1 2.192 / O1–H6 0.982
- i1.xyz：Na–O5(烷氧) 2.166 / C4–O1 1.407 / C4–O5 1.309 / C4–O3 1.425（C4 四面体）
- i2.xyz：Na–O1 2.524 / Na–O3 2.427 / Na–O5 3.463 / Na···H6 2.106 / O1···O3 2.671
- p.xyz：Na–O1 2.433 / Na–O5 2.091 / O1···H6 1.614（甲酸根–甲醇氢键）
- ts_e23_guess.xyz 六元环：Na–O5 2.166 / O5–C4 1.309 / C4–O3 2.011 / O3···H6 1.372 / H6–O1 1.380 / O1···Na 2.531（O1···H6···O3 179.6°）

## 3 文件序（1-based）速查 —— ts_prepare 的 reaction_center/ring_order/scans/freeze 用**文件下标**，不是 map 号
- rc.xyz / ts_e1_guess.xyz：1 Na | 2 O1 | 3 H6 | 4 C2 | 5 O3 | 6 C4 | 7 O5 | 8,9,10 H(C2) | 11 H(C4) → E1 reaction_center [2,6,7]；scan d(O1-C4)=[2,6]
- i1.xyz / ts_e23_guess.xyz：1 Na | 2 C2 | 3 O3 | 4 C4 | 5 O1 | 6 O5 | 7,8,9 H | 10 H(C4) | 11 H6 → E2 断[4,3]/成[4,6]；E3 质子[5,11]、O3···H6[3,11]；provided 六元环 ring_order [1,6,4,3,11,5]
- i2.xyz：1 Na | 2 C2 | 3 O3 | 4,5,6 H | 7 C4 | 8 O5 | 9 O1 | 10 H(C4) | 11 H6

## 4 待他人决策/已知偏差（本道不擅自处理）
1) 原子数是 **11**（NaC2H5O3，3N-6=27），题面写 12 与 registry 不符。
2) I2 的 Na 位置：声明要桥联 O1/O3（已按此交付），MMFF 偏好双齿 O3/O5（2.11/2.27）；强行桥联使 Na···H6 2.106 Å → 建议 I2 起点 Opt 自决。
3) ts_e23_guess 的 C4–O5 1.309 继承 I1 的 MMFF 值（未收紧）。
4) E2/E3 是否真耦合（六元环）只能由 TS/IRC 判定；本道只给几何。
5) 工具面 6 条（P1–P6）见 PREP_TOOL_REPRO.md；其中 P4（xyz→mol 丢键表）已被证实是 ts_prepare build 卡住的成因，规避路径：reactant/product 用 builder 原生 MOL。

## 5 本道在等什么 / 下一步
- **不等待**任何本道作业（0 个 QM 作业），无在飞 job_id。
- 下一步（若被指示）：只读复核 —— log_parser（Normal termination、虚频个数与模式成分、watch-pair 占比）、internal_coordinates（IRC 两端身份/ring 一致性）、format_converter（导帧）。需要绝对路径的原生 .log。
- 本道不会改动已冻结的 PREP_TOOL_REPRO.md；如需更正先报 Coordinator，按「同一轮更正」处理。
