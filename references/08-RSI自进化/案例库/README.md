# 案例库索引

> 分类：RSI自进化 | 主题：案例登记、规则版本与全局配置 | 整理日期：2026-11-10 | 适用：每次参考视频评估与自进化任务的归档入口

> ⚠️ 本文为创作流程参考，**不构成法律意见**；涉及授权与合规的决策请查阅 05-版权法规卷并由法务复核。

---

## 目录约定

```
案例库/
├── README.md              ← 本文件（索引，只追加）
├── _config.yaml           全局开关与版本指针（kill switch 在此）
├── _rules/                规则库版本 rules-vN.yaml + CHANGELOG.md
├── _frozen/               冻结回归集 / 隐藏集 / BASELINE.md（引擎只读或不可见）
├── _audit/                只追加审计日志 audit-YYYY.md
├── _counterexamples/      被驳回候选与失败案例（永久保留）
└── CASE-YYYYMMDD-NNN/     单案例：评估表 + 指纹 + 探测日志 + 方案 + 审查表 + 自进化记录
```

详见 `../06-案例库与版本治理.md`。

---

## 案例索引表（新增案例时追加一行，不删除）

| 案例 ID | 日期 | 参考视频 / 类型 | 指纹 ID | 规则版本 | 完成阶段 | 真实反馈 | 自进化结论 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| _（暂无案例）_ | | | | | | | |

「完成阶段」填：`S2 探测 / S5 评估 / S6 已确认 / S7 已交付 / S8 已回收反馈`。

---

## 规则版本表

| 版本 | 日期 | 状态 | 来源候选 | 闸门结果 | 签字 |
| --- | --- | --- | --- | --- | --- |
| `rules-v1` | 2026-11-10 | `last-known-good`（初始基线） | — | 初始 | — |

状态取值：`candidate` / `active` / `last-known-good` / `retired`。

---

## `_config.yaml` 初始内容

```yaml
evolution_enabled: true
active_rules_version: rules-v1
last_known_good: rules-v1
learning_rate_eta: 0.05
max_drift_delta: 0.1
min_support_n: 5
cooldown_days: 7
frozen_set_write_allowed: false
```

**kill switch**：把 `evolution_enabled` 改为 `false` 并把 `active_rules_version` 指回 `last_known_good`，即全局停用自进化。此操作不需要重新计算或重新训练，详见 `../05-反馈回流与自进化算法.md` §六。

---

## 新增案例步骤

1. 建目录 `CASE-YYYYMMDD-NNN/`。
2. 跑 `scripts/reference_probe.sh <参考视频> <本案例目录>`，产出 `probe.log` / `probe.json` / `metrics.csv` / `cuts.txt` / `shot_lengths.txt` / `loudness.txt` / `silence.txt` / `yavg.txt` / `satavg.txt` / `sheet_*.png`。
3. 复制 `../模板/参考视频评估表.md` 与 `../模板/风格指纹模板.yaml` 到本目录并填写。
4. 完成 S6 用户确认后，产出 `剪辑方案.md`（格式见 `../04` §五）。
5. 交付后填 `成片审查表.md`（用 `../../06-成片审查/03-审查表模板.md`）。
6. 回收真实反馈后填 `../模板/自进化记录模板.md` → `自进化记录.md`。
7. 在本文件索引表追加一行；如有批准的规则变更，同步 `_rules/`、`CHANGELOG.md`、`_audit/`。

---

## 冻结集与基线

| 集合 | 目标规模 | 当前 | 权限 |
| --- | --- | --- | --- |
| `_frozen/regression/` | ≥10 案例 | 0 | 引擎只读，人工维护 |
| `_frozen/hidden/` | 3 案例 | 0 | 引擎不可见、不可写 |
| `_counterexamples/` | 全部驳回候选 | 0 | 只追加 |

`_frozen/BASELINE.md` 记录四组元指标基线（评估质量 / 预测能力 / 结果质量 / 系统健康）。**在冻结集建立之前，不得批准任何规则变更**——没有回归基线就没有闸门。

---

## 参考来源

- `../06-案例库与版本治理.md`（目录、命名、版本、审计、回滚）
- `../05-反馈回流与自进化算法.md`（闸门与 kill switch）
- `scripts/reference_probe.sh`（探测产物清单）

检索日期：2026-11-10。
