# 缓存库 · 目录与数据约定

> 分类：素材记忆 | 主题：缓存目录结构、索引与记账字段、只追加与隐私约定 | 整理日期：2026-11-10 | 适用：首次运行 `material_cache.py` 前；排查命中异常或审计复用历史时

> ⚠️ 本卷为工程流程参考，**不构成法律意见**；缓存可能含人脸、地点与授权信息，须按 `../../05-版权法规/04` 与内部数据政策管理。

---

## 目录结构

本目录只存**描述与索引**，不存原视频本体。首次运行 `register` / `use` 时工具自动创建下表文件。

```
09-素材记忆/缓存库/
├── README.md                 ← 本文件
├── _config.json              ← 全局开关（kill switch 等）
├── index.csv                 ← 素材主索引，一素材一行
├── usage.csv                 ← 每次 lookup / use 的流水（token 记账）
├── audit.log                 ← 只追加审计日志
├── cards/
│   ├── <MID>.yaml            ← 权威描述卡（mdc-v1）
│   └── <MID>.v<N>.yaml       ← 纠错后的历史版本（保留，不覆盖当前卡）
├── themes/
│   └── <MID>.csv             ← 该素材被哪些主题采用（L2 适配层）
└── thumbnails/               ← 可选抽帧拼图（含人脸/车牌时按敏感素材管理）
```

---

## 字段定义

### `index.csv`

| 列 | 说明 |
| --- | --- |
| `mid` | `MID-<sha256 前 12 位>`，主键 |
| `quick_sha` / `full_sha` | 采样哈希 / 全量哈希（`--full` 时填写） |
| `hash_mode` | `sampled` / `full`；决定 `verify` 的严格度 |
| `size_bytes` / `duration_s` | 参与身份判定与 token 估算 |
| `card` | `cards/<MID>.yaml` 相对路径 |
| `card_version` | 从 1 起，纠错递增 |
| `status` | `active / superseded / blocked / unverified` |
| `rights_status` | `cleared / pending / restricted / blocked / unknown` |
| `aliases` | 分号分隔的文件名/代号，**仅检索用** |
| `source_path` | 登记时的绝对路径；`lookup` 用它识别「同路径但字节已变」的 `STALE` 状态 |
| `created` / `updated` | ISO 日期 |

### `usage.csv`

| 列 | 说明 |
| --- | --- |
| `ts` | ISO 8601 本地时间 |
| `event` | `MISS / HIT / HIT_BLOCKED / STALE / UNVERIFIED / USE / VERIFY / BLOCK` |
| `mid` / `theme` | 素材 ID / 主题 ID（无主题填 `-`） |
| `hash_mode` / `duration_s` | 用于估算 |
| `est_tokens` | `ceil(duration_s × rate)`，`rate` 默认 100 tok/s |
| `actual_tokens` | 实测 `usage_metadata` 值；未填留空 |
| `model` | 模型名与版本（仅 MISS 时填） |
| `note` | 说明，如「直接读卡;未请求模型」 |

### `themes/<MID>.csv`

`ts, theme_id, theme_title, clip_ranges, narrative_role, rights_scope_check, note, outcome`
——字段含义见 `../模板/主题适配记录模板.md`。以 `(theme_id, clip_ranges)` 去重，重复 `use` 只更新时间。

### `_config.json`

```json
{
  "cache_enabled": true,
  "default_token_rate": 100,
  "high_res_token_rate": 300,
  "default_hash_mode": "sampled",
  "require_full_hash_for_delivery": true,
  "block_unknown_rights": true
}
```

`cache_enabled: false` 是 kill switch：`lookup` 恒返回 `MISS`，用于排查缓存投毒或描述污染；**不会删除任何数据**。`default_token_rate` 与 `high_res_token_rate` 是估算口径，不同厂商不同，改前回查官方文档。

---

## 治理约定

| 约定 | 内容 |
| --- | --- |
| **只追加** | `usage.csv`、`audit.log`、历史卡版本只追加；不删行、不覆盖已签字记录 |
| **纠错不覆盖** | 原卡复制为 `<MID>.v<N>.yaml` 后写新卡，`corrections` 记字段/旧值/新值/依据/签字 |
| **授权到期** | `status: blocked` + 审计日志，**不删卡**；所有引用它的适配记录保留但标记失效 |
| **并发** | 工具用独占锁 + 原子写（临时文件 `os.replace`）；失败不留半张卡 |
| **损坏降级** | 卡片或索引解析失败按 `MISS` 处理并写日志，不中断剪辑流程 |
| **隐私** | 不缓存原视频；`subjects` 不写真名/身份；`geo_hint` 不存精确 GPS；含人脸/车牌的缩略图按敏感素材管理 |
| **备份** | `usage.csv`、`index.csv`、`cards/` 纳入 3-2-1 备份（口径见 `../../01-剪辑技巧/03`）；描述重建成本高于存储成本 |
| **易变信息** | token 速率、模型版本、厂商缓存 TTL 属易变信息，引用前回查官方最新文档 |

---

## 首次使用

```bash
PY="scripts/material_cache.py"

# 1. 查缓存（HIT 就直接读 cards/<MID>.yaml，别再请求模型）
python "$PY" lookup "D:/素材/example.mp4"

# 2. 未命中：本地探测 → 一次全量模型请求 → 填 ../模板/素材描述卡模板.yaml
python "$PY" validate /tmp/MID-xxxxxxxxxxxx.yaml
python "$PY" register "D:/素材/example.mp4" --card /tmp/MID-xxxxxxxxxxxx.yaml --tokens 18000

# 3. 之后每个主题只记一条
python "$PY" use "D:/素材/example.mp4" --theme "T-2026-示例主题" --clip "00:00:03-00:00:08" --note "开场空镜"

# 4. 体检与统计
python "$PY" verify "D:/素材/example.mp4"
python "$PY" stats
```

工具零第三方依赖（仅 Python 标准库），可直接在本机运行；`fingerprint` 会调用本机 `ffprobe`（8.1.2 已实测）读取规格，调用失败时降级为「仅哈希 + 文件大小」并在日志标注。

---

## 排查速查

| 现象 | 先查 |
| --- | --- |
| 明明分析过却 `MISS` | 文件字节是否变了（重导出/转码）；`_config.json` 的 `cache_enabled`；缓存目录是否被移动 |
| `HIT` 但描述对不上 | `verify` 重算哈希；若 `hash_mode: sampled`，改用 `--full` 复核（未采样区改动可能漏检） |
| `HIT_BLOCKED` | `rights_status` 或 `rights_expiry`；补授权凭证后人工改卡并留 `corrections` |
| 命中率异常高 | 可能把不同素材误判为同一哈希，或为刷指标强行命中；抽查 3 张卡的原片 |
| `stats` 数字与账单差很多 | 估算只算视频输入 token；用实测 `usage_metadata` 填 `actual_tokens` |
| 卡片字段缺项 | `python "$PY" validate <卡片>`，按 V1–V8 提示补齐 |

---

## 参考来源

- 本卷 `../01-素材描述卡规范.md`（V1–V8）、`../02-缓存复用协议与Token节省.md`（状态机、记账、并发、隐私）、`../03-多主题适配与引用治理.md`
- Content-Hash File Cache Pattern（内容哈希、路径无关、损坏按未命中降级）：https://lobehub.com/ru/skills/sehoon787-my-claude-content-hash-cache-pattern
- Google《Video understanding》与《Context caching》（token 速率与缓存口径）：https://ai.google.dev/gemini-api/docs/video-understanding 、 https://ai.google.dev/gemini-api/docs/caching
- `../../01-剪辑技巧/03-剪辑工作流与工程规范.md`（3-2-1 备份）、`../../08-RSI自进化/06-案例库与版本治理.md`（只追加与回滚）

检索日期：2026-11-10。目录结构、CSV 字段与 `_config.json` 开关均为本知识库自定义约定，非行业标准。
