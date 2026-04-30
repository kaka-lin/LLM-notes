# OpenClaw Skills 與 ClawHub 架構概念

本文檔整理自 OpenClaw 官方生態系，介紹 AgentSkills 標準、`SKILL.md` 的撰寫方式，以及 ClawHub 平台的定位。

## 1. 什麼是技能 (Skills)？

OpenClaw 的技能系統是建立在 **AgentSkills** 標準之上。技能本質上是一個將「提示詞 (Prompt)」、「專屬設定」與「外部工具腳本」整合在一起的模組化資料夾。每個技能都必須包含一個主指令檔：`SKILL.md`。

## 2. SKILL.md 格式規範

`SKILL.md` 是技能的核心檔案，檔案的開頭段落（Frontmatter）必須使用 YAML 格式來定義中繼資料 (Metadata)。

### 2.1 基礎欄位

```markdown
---
name: image-lab
description: Generate or edit images via a provider-backed image workflow
---

# 你的技能指令放這裡
當使用者要求...
```

- `name`：系統識別用的唯一 ID。
- `description`：幫助 AI 模型判斷何時該觸發此技能的簡短敘述。

### 2.2 進階欄位與環境要求 (Metadata Gating)

在單行的 `metadata` 區塊中，可以設定該技能載入的前提條件（Gating）。如果滿足不了這些條件（例如系統中沒安裝該軟體），技能將不會被載入。

```markdown
---
name: image-lab
description: 使用圖片生成工作流
metadata: { "openclaw": { "requires": { "bins": ["uv"], "env": ["GEMINI_API_KEY"], "config": ["browser.enabled"] } } }
---
```

常見的限制條件包含：

- **`requires.bins`**：指定的執行檔必須在環境 PATH 中（例如：`python3`, `uv`）。
- **`requires.env`**：需要存在的環境變數（此變數通常由 `openclaw.json` 在執行期注入）。
- **`requires.config`**：需要開啟的 OpenClaw 設定值。
- **`os`**：限制作業系統（例如：`["darwin", "linux"]`）。

### 2.3 觸發行為控制

- **`user-invocable`**：預設為 `true`。是否允許使用者透過斜線指令主動觸發。
- **`disable-model-invocation`**：預設為 `false`。若設為 `true`，模型在自由對話中「不會」自動調用此技能，只能由使用者強制觸發。
- **`command-dispatch`**：若設為 `tool`，使用斜線指令觸發時，會直接把參數拋給指定底層工具，跳過模型解析。

## 3. 什麼是 ClawHub？

[ClawHub](https://clawhub.ai) 是由社群驅動的 OpenClaw 技能註冊中心與管理平台（Registry）。

### 3.1 核心功能定位

- **發現與共享**：提供基於向量語意搜尋的技能庫，讓開發者尋找實用的 `SKILL.md` 套件。
- **版本控制**：發布的技能會標記 SemVer 版本號（支援 `latest` 等 tag），並且提供改版紀錄 (Changelog)。
- **審核機制**：提供社群通報機制（Report），若技能被舉報過多次將會自動隱藏，確保安全。
- **相依性打包**：透過指令下載的套件會封裝為 zip，解開後能直接放入 `skills` 目錄無縫運行。

### 3.2 下載與發布機制

- 身為**使用者**：可以透過 OpenClaw 本身的 `openclaw skills search / install / update` 來直接瀏覽與更新網路上的技能。
- 身為**開發者**：若要將自己寫的技能發布，必須額外安裝開源的 `clawhub` CLI，透過 `clawhub login` 與 `clawhub publish` 甚至 CI/CD 來同步發布。

## 4. 架構設計：全域安裝與 Agent 權限隔離

在多 Agent 系統中，常常會遇到一個設計問題：「為什麼不把每個技能直接放進個別 Agent 專屬的 Workspace 資料夾就好，而是要統一放在全域並用設定檔去管空白名單？」

主要原因有兩個：

1. **全域外掛管理 (Global Registry)**：從 ClawHub 下載的第三方技能，通常會安裝在系統全域層級（例如 `~/.openclaw/skills`）。與其手動複製一份一模一樣的檔案到 10 個不同的 Agent 專屬資料夾中，不如在全域安裝一次，再統一透過設定檔來分配存取權。
2. **共用 Workspace 情境 (Shared Context)**：如果有多個 Agent 共用同一個專案目錄（例如：Coder Agent 負責寫扣、Reviewer Agent 負責審查程式，兩者操作同一個 Workspace），這時就無法單純用「資料夾實體位置」來隔離權限。必須依賴系統層級的技能白名單，來限制特定 Agent（如審查員）不能偷偷調用具有破壞性（寫入）的技能。
