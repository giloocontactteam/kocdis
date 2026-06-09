# Giloo AI 發行助手

> 讓一人行銷團隊用 AI 高效發行全球獨立電影。

## 快速開始

### Claude Code 用戶

直接講你要做什麼就好：「上架新片《片名》」「剪片」「找觀眾」「翻譯字幕」「投廣告」「看成效」

Claude Code 會自己讀 `CLAUDE.md` 和 `.skills/distribution-agent/SKILL.md`，不用你手動指定。

### Claude Cowork 用戶

1. 在 Cowork 裡選這個資料夾
2. 把 `cowork-instructions.md` 的內容貼到 Folder Instructions
3. 開始做事：「請讀 distribution-sop.md，然後幫我上架新片《片名》」

---

## 兩條軌道

這個 repo 有兩條獨立的工作軌道，不要混在一起想：

### 軌道 A：發行 Pipeline（per-film，6 階段）

每部片走一遍，有狀態，追蹤在 `current-status.md`。

| 階段 | 資料夾         | 做什麼                                    |
| ---- | -------------- | ----------------------------------------- |
| 1    | `01-onboard/`  | 影片進場：填 metadata、抓主題、定目標市場 |
| 2    | `02-clips/`    | Clip Factory：幫每個平台寫短影片 brief    |
| 3    | `03-audience/` | Audience Mapping：找 micro-tribes         |
| 4    | `04-localize/` | 在地化：翻字幕 + 文化適配                 |
| 5    | `05-launch/`   | Campaign Launch：寫投放企劃 + Ad-Ops      |
| 6    | `06-measure/`  | 成效追蹤：看數字 + 記學到什麼             |

每個資料夾裡有 `_template/README.md`，新片從 template 開始。

### 軌道 B：日常 ops（routine，跟特定影片無關）

Amy 角色每天/每週重複的動作，**不會**反映在 `current-status.md`。

| 資料夾                            | 做什麼                      | 何時用            |
| --------------------------------- | --------------------------- | ----------------- |
| `team-ops/support-inbox-triage/`  | 客服信箱不漏信              | 每天早上          |
| `team-ops/director-outreach/`     | 影展找導演 → 開發信 → 追蹤  | 開新一輪 outreach |
| `team-ops/creator-signup-mockup/` | Creator 自助註冊提案 mockup | 一次性            |

詳見 `team-ops/README.md`。

---

## 重要文件

| 文件                     | 幹嘛用的                      | 誰讀          |
| ------------------------ | ----------------------------- | ------------- |
| `CLAUDE.md`              | Claude Code 的專案指令        | Claude Code   |
| `cowork-instructions.md` | Cowork 的 folder instructions | Claude Cowork |
| `distribution-sop.md`    | 品質標準 + 完整工作流程       | 兩邊都讀      |
| `giloo-voice.md`         | 品牌聲音規範                  | 兩邊都讀      |
| `about-giloo.md`         | Giloo 背景 + 團隊限制         | 兩邊都讀      |
| `current-status.md`      | Pipeline 進度追蹤             | 兩邊都讀      |
| `prompt-library/`        | 可複用的 prompt 模板          | 兩邊都用      |

---

## 新增影片

1. 把 `01-onboard/_template/README.md` 複製到 `01-onboard/[film-slug]/README.md`
2. 填入影片資訊
3. 依序推進 02 → 06 各階段
4. 每次 session 結束記得更新 `current-status.md`
