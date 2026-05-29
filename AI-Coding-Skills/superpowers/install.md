# superpowers 安裝指南

superpowers 沒有單一 installer，而是把安裝這件事完全外包給各 agent 的 plugin 系統 —— 結果就是「8 個 agent 8 種安裝方式」。直接照官方 README 對指令很容易混淆，先看完前半段心智模型再去對指令，會省很多時間。

## 1. 先理解兩個核心觀念

### 1.1 沒有單一 installer

superpowers 本質上是一包符合 [Agent Skills 規範](https://agentskills.io/) 的 skill 檔案，**沒有自己的 installer / setup 腳本**。安裝這件事完全由各 agent 自己的 plugin / extension 系統負責：

- Claude Code、Copilot CLI、Factory Droid → **plugin marketplace**
- Codex CLI / App → **內建 plugin 搜尋**
- Cursor → **內建 plugin 系統**
- Gemini CLI → **`gemini extensions` 命令**
- OpenCode → **完全沒有 plugin 系統，要叫 OpenCode 自己照 `INSTALL.md` 跑**

### 1.2 多 agent 要分別安裝

superpowers **沒有跨 host 部署的腳本**，也沒有「一次裝完全部 agent」的選項。如果你 Claude Code、Cursor、Codex 都用，就要在三邊各裝一次。貢獻指南明確要求 skill 更新「必須在所有支援的 agent 間運作」，但**這條規矩是給開發者用的，不是給使用者用的**。

## 2. 8 種安裝方式對應誰

| # | Agent | 安裝管道 | 一行摘要 |
| --- | --- | --- | --- |
| 1 | Claude Code | Plugin marketplace（官方 / Superpowers） | 主力平台，兩個來源擇一 |
| 2 | Cursor | 內建 plugin | 一行指令 |
| 3 | Codex CLI | `/plugins` 搜尋 | 互動式安裝 |
| 4 | Codex App | 側邊欄 Plugins | GUI 點擊 |
| 5 | Google Gemini CLI | `gemini extensions install` | 直接吃 GitHub URL |
| 6 | OpenCode | 對話式（丟連結） | 沒 plugin 系統，要叫 OpenCode 跑指令 |
| 7 | Factory Droid | `droid plugin install` | 兩段：marketplace + plugin |
| 8 | GitHub Copilot CLI | `copilot plugin install` | 兩段：marketplace + plugin |

## 3. 詳細指令

### 3.1 Claude Code

兩個來源擇一即可：

**官方 plugin marketplace：**

```text
/plugin install superpowers@claude-plugins-official
```

**Superpowers marketplace（作者自家的，通常更新較快）：**

```text
/plugin marketplace add obra/superpowers-marketplace
/plugin install superpowers@superpowers-marketplace
```

兩者都會把 skill 註冊到 Claude Code session 內，重啟後 `/test-driven-development`、`/systematic-debugging` 等指令就能用。

### 3.2 Cursor

在 Cursor 聊天框打：

```text
/add-plugin superpowers
```

或在 Cursor 的 plugin marketplace UI 搜尋「superpowers」手動加。

### 3.3 Codex CLI

進入 Codex CLI 後：

```text
/plugins
```

在 plugin 搜尋介面打「Superpowers」，選 **Install Plugin**。

### 3.4 Codex App

GUI 路徑：

1. 打開 Codex App
2. 側邊欄找 **Plugins**
3. 在 **Coding** 區段找到 **Superpowers**
4. 點 `+` 並照提示完成

### 3.5 Google Gemini CLI

直接吃 GitHub URL：

```bash
gemini extensions install https://github.com/obra/superpowers
```

更新：

```bash
gemini extensions update superpowers
```

### 3.6 OpenCode

OpenCode 沒有正規 plugin 系統，作者用一招繞過：**把官方 INSTALL.md 的 URL 丟給 OpenCode，叫它自己照做**。打開 OpenCode 並貼：

> Fetch and follow instructions from <https://raw.githubusercontent.com/obra/superpowers/refs/heads/main/.opencode/INSTALL.md>

OpenCode 會 fetch 那份指示並照做（複製 skill 檔案、改 config）。詳細運作細節見 [`docs/README.opencode.md`](https://github.com/obra/superpowers/blob/main/docs/README.opencode.md)。

> ⚠️ 這條路徑等於把「裝什麼、改什麼」的決策權交給 AI，跟其他平台的 plugin marketplace 信任模型不同。對 prompt injection 敏感的人請先讀過那份 `INSTALL.md` 再貼。

### 3.7 Factory Droid

兩段式：先註冊 marketplace，再裝 plugin。

```bash
droid plugin marketplace add https://github.com/obra/superpowers
droid plugin install superpowers@superpowers
```

### 3.8 GitHub Copilot CLI

跟 Factory Droid 同樣結構：

```bash
copilot plugin marketplace add obra/superpowers-marketplace
copilot plugin install superpowers@superpowers-marketplace
```

## 4. 多 agent 並用

superpowers **沒有跨 host / 一次部署到多 agent 的機制**。所以多 agent 並用就是**每個都跑一次對應的安裝指令**。

實務建議：

- **主力 agent**（最常用的那個）先裝、跑一輪確認 skill 觸發機制
- **副力 agent** 後裝，並注意：同一個 skill 名在不同 agent 上**觸發語法可能不同**（slash command prefix、namespacing 規則各異）
- 跟其他 skill 套件並裝時，注意 slash command 是否撞名 —— superpowers 的指令前綴是 `test-driven-development`、`systematic-debugging` 這類，跟多數套件不會衝突

## 5. 解除安裝

各 agent 自己的 plugin 移除指令，沒有統一介面：

| Agent | 移除方式 |
| --- | --- |
| Claude Code | `/plugin remove superpowers` |
| Cursor | plugin marketplace UI 移除 |
| Codex CLI | `/plugins` → 找到 Superpowers → uninstall |
| Codex App | 側邊欄 Plugins → 移除 |
| Gemini CLI | `gemini extensions uninstall superpowers` |
| OpenCode | 手動清理（OpenCode 安裝時放的 skill 檔案） |
| Factory Droid | `droid plugin uninstall superpowers` |
| Copilot CLI | `copilot plugin uninstall superpowers` |

OpenCode 因為是對話式安裝，最乾淨的辦法是**叫 OpenCode 自己反向操作**：把 INSTALL.md URL 丟給它並要求「undo what that file says to do」。

## 6. 延伸閱讀

- 官方 README：<https://github.com/obra/superpowers>
- Marketplace：<https://claudemarketplaces.com/skills/obra/superpowers>
- OpenCode 安裝指示原文：<https://raw.githubusercontent.com/obra/superpowers/refs/heads/main/.opencode/INSTALL.md>
- Agent Skills 開放規範：<https://agentskills.io/>
