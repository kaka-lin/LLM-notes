# OpenClaw 內建工具整理與查詢方式

_更新時間：2026-03-27_

OpenClaw 提供了多種內建工具，特別是 `sessions_*` 系列的協調工具。這些工具在官方文件中被歸類為「核心工具」(Built-in Tools)，本指南詳細整理了其分類與查詢方式。

## 1. 工具、Skill 與 Plugin 的差異

OpenClaw 官方將能力分為三層架構：

- **Tool**：真正執行動作的能力。模型可以直接呼叫的具名函式 (Typed Function)。
- **Skill**：教導模型如何使用工具。透過 `SKILL.md` 操作說明，引導 Agent 在正確時機調用工具。
- **Plugin**：外部擴充能力。用於註冊額外的 Tool、Skill、模型提供者或通訊管道。

## 2. 核心功能包含哪些？

根據官方文件，內建工具大致分為以下類別：

### 2.1 執行環境與 Shell (Runtime)

- `exec`：執行 Shell 指令。
- `process`：管理背景程序。
- （`bash` 常作為 `exec` 的別名使用）。

### 2.2 網頁與瀏覽器 (Web / Browser)

- `browser`：控制 Chromium 瀏覽器（換頁、點擊、截圖）。
- `web_search`：執行網頁搜尋。
- `web_fetch`：抓取網頁原始內容。

### 2.3 檔案系統 (Filesystem)

- `read` / `write`：檔案讀寫。
- `edit`：編輯檔案內容。
- `apply_patch`：套用程式碼補丁。

### 2.4 通訊與訊息 (Messaging)

- `message`：跨平台與跨頻道傳送訊息。

### 2.5 裝置與自動化 (Automation)

- `canvas`：與繪圖節點互動。
- `nodes`：探索與配對網路中的對等節點。
- `cron`：執行排程任務。
- `gateway`：管理閘道層的高權限操作。

> [!IMPORTANT]
> 官方安全指南提醒，`gateway` 與 `cron` 屬於高風險工具。在處理不可信輸入時，建議預設禁止 (Deny) `sessions_spawn` 與 `sessions_send` 等高功能權限。

### 2.6 多媒體能力 (Media)

- `image`：圖片內容分析。
- `image_generate`：生成或編輯圖片。

### 2.7 代理人協調 (Session / Agent Coordination)

- `sessions_list`：列出所有活動中的對話。
- `sessions_history`：讀取特定對話的歷史紀錄。
- `sessions_send`：傳送跨 Agent 訊息。
- `sessions_spawn`：生成子代理人 (Sub-agent)。
- `session_status`：檢查目前工作狀態。

## 3. `sessions_list` 工具詳解

`sessions_list` 是目前最常用的管理工具之一，它將 Agent 對話資訊以陣列形式回傳。

- **支援參數**：可透過 `kinds`、`limit`、`activeMinutes` 等篩選器優化結果。
- **回傳內容**：包含 `sessionId`、`model`、`updatedAt`、`totalTokens` 以及對話脈絡資訊。

## 4. 如何查詢可用工具？

查詢工具時須區分「目錄」與「實際權限」：

### 4.1 核心目錄 (Catalog)

最直接的方式是查閱官方文件或呼叫 `tools.catalog` API，了解 OpenClaw 程式碼庫中理論上支援哪些工具。

### 4.2 運行時權限 (Runtime Policy)

工具是否可用受到 **Policy Chain** 的嚴格控管。

- **過濾層級**：包含 `tools.profile` 設定項、`tools.allow` / `tools.deny` 名單，以及個別 Agent 的覆寫設定。
- **原則**：內建並不代表一定能用， Agent 只能看見被明確授權的工具。

## 5. 實務查閱技巧

### 方法 A：使用 Control UI (推薦)

在管理介面中，可查看 **Available Right Now** 視圖。這是透過 `tools.effective()` 計算後的最終清單，即為 Agent 當下真正能用的工具。

### 方法 B：查閱設定檔

檢查 `~/.openclaw/openclaw.json` 中的 `tools.profile` 與 `group:*` 設定，以此推斷被分配的工具群組。

### 方法 C：直接驗證

嘗試使用 `/tools/invoke` 呼叫特定工具。若回傳 **404**，通常代表該工具被 Policy 封鎖或不存在。

## 6. 工具群組 (Tool Groups) 參考

大多數情況下，我們會透過群組 (Group) 來批次設定權限：

- **`group:runtime`**：含 `exec`, `process`。
- **`group:fs`**：含 `read`, `write`, `edit`, `apply_patch`。
- **`group:sessions`**：含 `sessions_*` 等 Agent 協調工具。
- **`group:web`**：含 `web_search`, `web_fetch`。
- **`group:ui`**：含 `browser`, `canvas`。

## 7. 結論與測試心得

1. **功能完整性**：透過 API 測試證明 `sessions_list` 是內建且可直接調用的。
2. **查詢路徑**：目前系統標配並無通用的 `tools.list` 查詢指令，應以 Control UI 視圖為準。
3. **安全考量**：所有工具的使用都具備追蹤與權限隔離，確保多代理環境的穩定性。

---

### 主要參考來源

- [Tools and Plugins](https://docs.openclaw.ai/tools)
- [Tools Invoke API](https://docs.openclaw.ai/gateway/tools-invoke-http-api)
- [Session Tools](https://docs.openclaw.ai/concepts/session-tool)
- [Configuration Reference](https://docs.openclaw.ai/gateway/configuration-reference)
- [OpenClaw GitHub Repository](https://github.com/openclaw/openclaw)

