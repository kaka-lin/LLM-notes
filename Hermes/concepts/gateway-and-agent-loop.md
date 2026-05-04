# Gateway 與 Agent Loop

Hermes 的核心是兩段分離但緊密協作的設計：**Gateway** 負責訊息平台 IO，**Agent Loop** 負責推理與工具執行。理解這個分割，才能弄懂為什麼某些設定（allowlist、平台 mention 規則）放在 gateway 層，而另一些（personality、memory、skills）屬於 agent loop。

## 1. 系統訊息流

一則來自使用者的訊息會經過：

```text
[Telegram / Discord / Slack 等]
        │
        ▼
┌──────────────────────────┐
│       Gateway 層         │
│  • 平台 adapter (polling │
│    / socket / webhook)   │
│  • Session 路由          │
│  • 授權檢查 (allowlist /  │
│    pairing)              │
│  • Slash command dispatch│
│  • Hook (on-message 等)  │
└──────────┬───────────────┘
           │ 訊息已通過授權
           ▼
┌──────────────────────────┐
│      Agent Loop 層       │
│  • Provider 選擇         │
│  • Prompt 組裝（含       │
│    personality + MEMORY  │
│    + skills + context）  │
│  • 工具執行 / retry      │
│  • 結果寫入 session DB   │
└──────────┬───────────────┘
           │ 回覆訊息
           ▼
┌──────────────────────────┐
│       Gateway 層         │
│  • 透過原 adapter 回覆   │
│  • 處理 voice / file 轉換│
└──────────────────────────┘
```

## 2. Gateway 層職責

Gateway 是 long-running 服務（`gateway run`），負責所有與**訊息平台外部世界**互動的事情：

- **多平台 adapter（官方目前列出 18 個訊息平台）**：每個平台有獨立的連線方式（Telegram polling、Slack socket、Discord WebSocket、WhatsApp Web、Signal 等），涵蓋 Telegram / Discord / Slack / WhatsApp / Signal / Matrix / Mattermost / Email / SMS / DingTalk / Feishu / WeCom / Weixin / BlueBubbles (iMessage) / QQ / Yuanbao / Home Assistant 等。
- **Session 路由**：根據平台 + 使用者 + 頻道組合決定要使用哪個 session（同一個 user 在不同頻道是不同 session）。
- **授權檢查**：依序檢查 per-platform allow-all、pairing list、per-platform allowlist、global allowlist、global allow-all、否則拒絕。
- **Slash command dispatch**：`/new`、`/reset`、`/help` 等指令在 gateway 攔截處理，不會送進 agent loop。
- **Hook 觸發**：`on-message`、`on-error` 等事件在 gateway 觸發。

> ⚠️ Gateway 是**有狀態**的（持有 polling connection、socket connection），不可隨意重啟。
>
> 但 CLI 工具（`hermes pairing approve`、`hermes sessions list`）是另一條入口，與 gateway 同步存取 `~/.hermes/`，互不影響。

## 3. Agent Loop 層職責

Agent Loop 是 **synchronous、platform-agnostic** 的核心，被多種前端共用：

- CLI（`hermes chat`）
- Gateway（每則訊息進來呼叫一次）
- ACP（Agent Communication Protocol）
- Batch processing
- API server（OpenAI 相容介面）

Agent Loop 內部負責：

- **Provider 選擇**：根據 routing rule 把請求送到 Anthropic / OpenAI / OpenRouter / 本地 LLM。
- **Prompt 組裝**：personality + `MEMORY.md` + `USER.md` + 已啟用的 skills + context files。
- **工具執行**：豐富的內建 tool registry，依官方分類涵蓋 8 大主軸（Web / Terminal & Files / Browser / Media / Agent orchestration / Memory & recall / Automation & delivery / Integrations），常用 toolsets 包括 `web`、`search`、`terminal`、`file`、`browser`、`vision`、`memory`、`session_search`、`cronjob`、`messaging`、`skills`、`delegation`、`code_execution` 等，並可動態載入 MCP toolsets。
- **Retries / 錯誤處理**：API 限流、timeout、token 過長時的 compression。
- **Session 寫入**：每輪對話原子寫入 SQLite。

## 4. 為什麼這樣分？

### 4.1 多前端共用核心

如果 agent loop 跟 gateway 綁死，要支援 CLI / batch / API server 就得各自實作一份。分離後 agent loop 只關注「給定一段對話與 context，產生下一輪回應」，前端負責 IO 細節。

### 4.2 Gateway 重啟不影響 session

Gateway 重啟只是重連訊息平台；session、memory、cron 都存 `~/.hermes/`，重啟後立即 resume。

### 4.3 多平台統一行為

Telegram / Discord / Slack 對同一個 agent loop 而言只是不同的「使用者來源」。同一個 user 跨平台仍是不同 session（per-platform isolation），但他們共用同一個 agent personality / memory / skills。

## 5. 設計取捨：為何 Gateway 有自己的 hooks

Gateway 在某些事件上有「always-registered hooks」：

- `on-startup`：啟動時跑（如同步 bundled skills）
- `on-message-received`：每次收到訊息（在送進 agent 前）
- `on-message-sent`：成功回覆後

這些是 gateway 層的事件，**早於 agent loop**。例：你可以在 `on-message-received` 過濾掉特定關鍵字訊息（即使 agent loop 在跑也不要進去）。

Plugin 開發者可以額外註冊 hooks 在這些 lifecycle point 上。

## 6. 一個訊息的完整生命週期（範例）

使用者在 Telegram 對 bot 發 `summarize https://example.com`：

```text
1. Telegram → polling getUpdates → gateway 拿到 update
2. gateway adapter 轉成統一 message 格式
3. on-message-received hook 觸發（可被攔截）
4. 授權檢查：使用者在 TELEGRAM_ALLOWED_USERS → 通過
5. Slash command 檢查：不是 /xxx → 不攔截
6. Session 路由：找到（或建立）對應 session
7. 訊息傳入 agent loop
   ├─ 載入 personality
   ├─ 注入 frozen MEMORY.md / USER.md
   ├─ 啟用 skills（網頁摘要相關）
   ├─ 組 prompt → 送 Anthropic API
   ├─ LLM 決定使用 web.fetch tool
   ├─ 執行 tool → 拿到網頁內容
   ├─ 二輪 LLM → 產生摘要
   └─ 結果寫入 session DB
8. agent loop 回傳文字到 gateway
9. on-message-sent hook 觸發
10. gateway 透過 telegram adapter 把回覆發出去
```

整個流程的耗時主要在 step 7（LLM 推理 + tool 執行），其他都是毫秒級。

## 7. 實務影響

### 7.1 改 allowlist 不需要等 agent

Allowlist 在 gateway 層檢查，重啟 gateway 即可生效，與 agent loop 無關。

### 7.2 改 personality / skills 不需要重連平台

這些屬於 agent loop。理論上可 hot reload 而不重連 telegram polling，但實務上 `docker compose restart hermes` 一次重啟比較簡單可靠。

### 7.3 切換 LLM provider 不影響訊息平台

Provider 是 agent loop 內部設定。你切到別的 LLM 提供者，使用者完全無感，bot 還是同一個 bot。

## 8. 相關文件

- [Memory 系統](memory-system.md)
- [Session 管理](session-management.md)
- 官方參考：[Hermes Architecture](https://hermes-agent.nousresearch.com/docs/developer-guide/architecture) ／ [CLI Commands](https://hermes-agent.nousresearch.com/docs/reference/cli-commands)
