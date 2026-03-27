# OpenClaw 內建工具整理與查詢方式

_更新時間：2026-03-27_

OpenClaw 提供了多種內建工具，特別是 `sessions_*` 系列的 session / agent 協調工具。這些工具在官方文件中被歸類為內建工具（built-in tools），並在 session tool 專頁中有詳細說明。

**主要參考來源：**

- [OpenClaw Tools](https://docs.openclaw.ai/tools)
- [Session Tools](https://docs.openclaw.ai/concepts/session-tool)
- [OpenClaw GitHub](https://github.com/openclaw/openclaw)

## 1. OpenClaw 的工具、Skill、Plugin 是什麼差別？

OpenClaw 官方把能力分成三層：

- **Tool**：真正執行動作的能力。模型可以直接呼叫的 typed function。
- **Skill**：教模型怎麼用工具。透過 `SKILL.md` 等操作說明，引導 agent 何時、如何使用工具。
- **Plugin**：額外擴充能力。可額外註冊 tool、skill、model provider 或 channel。

## 2. OpenClaw 內建工均有哪些？

根據官方 `Tools and Plugins` 文件，OpenClaw 內建工具大致分成這些：

### 2.1 Runtime / Shell

- `exec`
- `process`
- （`bash` 在設定群組中可作為 `exec` 的 alias）

用途：執行 shell 指令、管理背景程序。

### 2.2 Web / Browser

- `browser`
- `web_search`
- `web_fetch`

用途：

- `browser`：控制 Chromium 瀏覽器（開頁、點擊、截圖）
- `web_search`：搜尋網頁
- `web_fetch`：抓取網頁內容

### 2.3 檔案系統

- `read`
- `write`
- `edit`
- `apply_patch`

用途：在 workspace 內做檔案讀寫與 patch。

### 2.4 Messaging / Sending

- `message`

用途：跨 channel 傳送訊息。

### 2.5 UI / Device / Node

- `canvas`
- `nodes`

用途：

- `canvas`：與 node Canvas 互動
- `nodes`：發現與指定配對裝置/節點

### 2.6 Automation / Control Plane

- `cron`
- `gateway`

用途：

- `cron`：排程工作
- `gateway`：管理 gateway、部分控制平面操作

> 注意：官方安全文件特別提醒，`gateway` 和 `cron` 屬於高風險工具；另外也建議在不可信輸入場景下，預設 deny `sessions_spawn`、`sessions_send`。這代表它們能力很強，但也要小心授權。

### 2.7 Image / Media

- `image`
- `image_generate`

用途：

- `image`：圖片分析
- `image_generate`：圖片生成或編修

### 2.8 Session / Agent Coordination

- `sessions_list`
- `sessions_history`
- `sessions_send`
- `sessions_spawn`
- `session_status`
- （某些文件/群組條目也提到 `sessions_yield`、`subagents`、`agents_list`）

用途：

- 查目前 session
- 讀取某個 session 的歷史
- 傳訊息給另一個 session
- 生成 sub-agent / sub-session
- 查 session 狀態

## 3. `sessions_list` 是做什麼的？

官方 Session Tools 文件列出的 tool names 包含：

- `sessions_list`
- `sessions_history`
- `sessions_send`
- `sessions_spawn`

其中 `sessions_list` 用來「列出 session 作為一個 rows array」。支援的常見參數包含：

- `kinds?: string[]`
- `limit?: number`
- `activeMinutes?: number`
- `messageLimit?: number`

回傳每列通常會含有：

- `key`
- `kind`
- `channel`
- `displayName`
- `updatedAt`
- `sessionId`
- `model`
- `contextTokens`
- `totalTokens`
- `lastTo`
- `deliveryContext`
- `transcriptPath`
- 以及可選的 `messages`

這也和你目前測試程式裡用 `/tools/invoke` 呼叫 `sessions_list` 的方式一致。

## 4. 如何查「有哪些工具」？

這個問題要分成兩種：

### 4.1 查「OpenClaw 理論上有哪些內建工具」

最直接的方法：

1. 看官方文件：`Tools and Plugins`
2. 看 `tools.profile` / `tool groups` / `configuration reference`
3. 看 session tools / web tools / browser tools 等分頁

這能查到 **catalog 層級** 的工具，也就是 OpenClaw 內建支援哪些工具。

### 4.2 查「你這個 session / 這個 agent 現在實際可用哪些工具」

這才是最重要的。

官方文件明確說明：**工具是否可用，會經過 policy chain 過濾**，包含：

- `tools.profile`
- `tools.allow`
- `tools.deny`
- `tools.byProvider.*`
- per-agent 覆寫
- group / channel policy
- subagent policy

所以：

- 內建 ≠ 一定能用
- 某工具存在 ≠ 你目前這個 session 一定拿得到

## 5. 實務上怎麼查目前可用工具？

### 方法 A：Control UI 看 runtime tool list

官方 WebChat / Control UI 文件提到 `/agents` 的 Tools panel 有兩種視圖：

1. **Available Right Now**：使用 `tools.effective(sessionKey=...)`，顯示當前 session 真正可用的工具。
2. **Tool Configuration**：使用 `tools.catalog`，顯示工具目錄與設定語意。

這目前是查閱可用工具最直接的官方方法。

### 方法 B：看設定檔

查看 `~/.openclaw/openclaw.json` 裡的：

- `tools.profile`
- `tools.allow`
- `tools.deny`
- `tools.byProvider`
- `agents.list[].tools.*`

再對照官方文件中的 tool groups，例如 `group:runtime`、`group:fs` 等，可以推估 agent 最終拿到哪些工具。

### 方法 C：直接試 `/tools/invoke`

透過 Gateway API 測試：

```json
{
  "tool": "sessions_list",
  "action": "json",
  "args": {}
}
```

如果工具被 policy 擋掉，`/tools/invoke` 會回傳 **404**。這個方法適合針對特定工具進行驗證。

### 方法 D：從 Control UI 的 Agents / Tools & Plugins 頁面

透過 UI 的 tools panel 視圖可以很方便地分辨：

- 目錄（catalog）中有哪些工具
- 目前運行（runtime）真正能用哪些工具

## 6. 有沒有官方 `tools.list` 之類的 API？

以我這次查到的公開資料來看：

- 官方文件明確提到的是 `tools.effective(sessionKey=...)` 與 `tools.catalog`（出現在 Control UI / Agents tools panel 的說明裡）
- 官方對外穩定公開、你現在直接能打的是 `POST /tools/invoke`
- 我沒有找到一個在官方 API 文件裡清楚列為公開 HTTP API 的 `tools.list` endpoint

另外，GitHub issue 也出現過有人提到：

- `openclaw gateway call tools.list` 會回 `unknown method: tools.list`
- 某些 debug 命令在特定版本不存在

> **不要假設有通用公開的 `tools.list` HTTP API。**
> 查可用工具時，優先用 **Control UI 的 Available Right Now / Tool Configuration**，或直接看設定與 `/tools/invoke` 測試。

## 7. Tool Profiles 與 Tool Groups 整理

官方 configuration reference 列出的 profile：

### Profiles

- `minimal`：`session_status` only
- `coding`：`group:fs`, `group:runtime`, `group:sessions`, `group:memory`, `image`
- `messaging`：`group:messaging`, `sessions_list`, `sessions_history`, `sessions_send`, `session_status`
- `full`：不限制（等同 unset）

### Tool Groups

- `group:runtime` → `exec`, `process`
- `group:fs` → `read`, `write`, `edit`, `apply_patch`
- `group:sessions` → `sessions_list`, `sessions_history`, `sessions_send`, `sessions_spawn`, `session_status`
- `group:memory` → `memory_search`, `memory_get`
- `group:web` → `web_search`, `web_fetch`
- `group:ui` → `browser`, `canvas`
- `group:automation` → `cron`, `gateway`
- `group:messaging` → `message`
- `group:nodes` → `nodes`
- `group:openclaw` → 所有內建 OpenClaw 工具（不含 provider plugins）

這一段很重要，因為很多時候你不是一個一個 allow tool，而是直接 allow 一個 `group:*`。

## 8. 你現在這個 `sessions_list` 測試代表什麼？

你的測試腳本是：

```python
payload = {
  "tool": "sessions_list",
  "action": "json",
  "args": {}
}
```

這代表：

1. 你的 Gateway `/tools/invoke` endpoint 可達
2. bearer token 正常
3. 目前這個 session / agent policy 沒有擋掉 `sessions_list`
4. OpenClaw 端確實有註冊 `sessions_list` 這個工具

也就是說，至少在你目前這套環境裡，`sessions_list` 不只是文件上的 built-in tool，**而且是實際可調用的 tool**。

## 9. 給你的結論

### Q1. `sessions_list` 是不是 OpenClaw 內建工具？

**是。** 它屬於官方 `sessions_*` session tools 的一部分。

### Q2. OpenClaw 內建工具有哪些？

官方文件列出的 built-in tools 包含：

- `exec`, `process`
- `browser`
- `web_search`, `web_fetch`
- `read`, `write`, `edit`
- `apply_patch`
- `message`
- `canvas`
- `nodes`
- `cron`, `gateway`
- `image`, `image_generate`
- `sessions_*`, `agents_list`
- 另外在 configuration/tool groups 中也能看到：`memory_search`, `memory_get`, `session_status`

### Q3. 怎麼查有哪些工具？

這也和你目前測試程式裡用 `/tools/invoke` 呼叫 `sessions_list` 的方式一致。

## 10. 主要參考來源

- [Tools and Plugins](https://docs.openclaw.ai/tools)
- [Tools Invoke API](https://docs.openclaw.ai/gateway/tools-invoke-http-api)
- [Session Tools](https://docs.openclaw.ai/concepts/session-tool)
- [Configuration Reference](https://docs.openclaw.ai/gateway/configuration-reference)
- [WebChat / Control UI tools panel](https://docs.openclaw.ai/web/webchat)
- [OpenClaw GitHub repository](https://github.com/openclaw/openclaw)
