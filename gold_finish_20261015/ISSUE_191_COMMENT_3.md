## 补充实测：步预算随作业/阶段不同（且与 route 的 maxcycles 无关）

同一战役、同一方法级别（B3LYP-D3(BJ)/def2SVP + ultrafine + tightSCF + CPCM）的 Gaussian 16 opt / ts_opt 作业，日志回显的步上限**互不相同**，且均为「自 Step 1 起即打印」：

| 作业 | 类型 | 日志回显的步上限 | 证据 |
|---|---|---|---|
| job 1012 | I2 极小值 opt（calcfc，route 写 maxcycles=200） | **100** | `i2_min_conv.log` L1096 |
| job 1016 | I2 极小值 opt（readfc，route 写 maxcycles=200；Link1 回显 `1/6=200`） | **100** | `i2_min_readfc.log` L735 |
| job 1018 | ts_opt（NY3_E1 第 4 版） | **45** | `ts/ts_0007/jobs/declaration_0004/ts_opt/refine.log` L21963 `Step number 45 out of a maximum of 45` |
| job 997 | ts_opt（同 run 第 2 版） | **45** | 同 run 早期日志 |
| job 999 | ts_opt（HI1_E3） | **232** | `ts/ts_0011/jobs/declaration_0004/ts_opt/refine.log` |
| job 1008 | ts_opt（HI1_E2） | **226** | `ts/ts_0009/jobs/declaration_0005/ts_opt/refine.log` |
| job 1013 | ts_opt（HI1_EM1） | **240** | `ts/ts_0012/jobs/declaration_0001/ts_opt/refine.log` |
| job 1017 | ts_opt（HI1_E1） | **246** | `ts/ts_0008/jobs/declaration_0003/ts_opt/refine.log` |

**含义**：步预算显然来自平台/生成层的某个注入值（且随作业/阶段变化），而不是 route 里写的 `maxcycles`。这使使用方无法预估「失败前会跑多少步」（本战役同时出现「45 步即 l9999」与「246 步上限」）。建议：按作业类型/阶段显式登记该值，或在输入/回显中标注真实步预算；若已有预期语义（例如随体系规模/自由度数变化），请在文档中说明。