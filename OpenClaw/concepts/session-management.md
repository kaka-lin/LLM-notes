# 會話隔離與重置機制 (Session Management)

本篇整理了 OpenClaw 的 Session 管理、重置指令、記憶系統，以及各平台下如何正確操作。

> **官方文件**：<https://docs.openclaw.ai/concepts/session>

## 1. 核心觀念：Session Key

所有對話上下文都綁定在一把獨一無二的 **Session Key** 上。系統根據來源動態產生：

| 來源 | Session Key 格式 | 隔離方式 |
| :--- | :--- | :--- |
| WebUI | `agent:<agentId>:web:<randomId>` | 每次 `/new` 產生新 ID |
| Discord 頻道 / Thread | `agent:<agentId>:discord:channel:<channelId>` | 每個 頻道 / Thread 獨立 |
| Telegram / Discord DM | 依 `session.dmScope` 設定而定 | 預設共用 DM session；多使用者建議設 `per-channel-peer` |
| Cron Job | 依 `--session` / `sessionTarget` 而定 | `isolated` 會使用 dedicated `cron:<jobId>`；也可跑在 `main`、`current` 或 `session:<id>` |
| Webhook | 每個 hook 獨立 | 自動隔離 |

相同 Session Key = 同一次對話（有上下文連貫性）。不同 Key = 徹底隔離。

## 2. Session 生命週期

Session 會在以下情況自動或手動結束：

| 觸發條件 | 說明 |
| :--- | :--- |
| **每日自動重置** | 預設每天凌晨 4:00（本地時間）自動清空 |
| **閒置重置** | 超過設定的閒置時間後自動清空 |
| **手動重置** | 使用者發送 `/new` 或 `/reset` |
| **Compaction** | Context 超過限制時自動壓縮（不清空，但會摘要化） |

Session 資料儲存在：`~/.openclaw/agents/<agentId>/sessions/`

## 3. 重置指令

### 3.1 `/new` — 開新 Session（最常用）

在任何平台的聊天框直接輸入 `/new`。

| 平台 | 效果 |
| :--- | :--- |
| **WebUI** | 產生全新 Session ID（URL 變成 `/#/chat/<new_id>`），舊對話保留在側邊欄 |
| **Discord / Telegram DM** | 清空目前 DM scope 對應 session 的對話歷史，重新載入 bootstrap 檔案 |
| **Discord 頻道** | 清空該頻道的 session |

**可選參數：**

- `/new <model>` — 開新 session 同時切換模型
- `/new --clear-memory` — 開新 session 同時清除 workspace memory

> **DM 的體驗差異**：畫面上舊訊息還在（手機/Discord 不會自動清除聊天記錄），但該 DM session 的 agent 上下文已經重置。若多個人會私訊同一個 agent，務必設定 `session.dmScope: "per-channel-peer"` 避免共用上下文。

### 3.2 `/reset` — 更徹底的重置

與 `/new` 類似但更徹底。屬於 hooks 系統會監聽的 lifecycle event，可觸發自訂的 hook 腳本（如自動儲存 session 記憶）。

### 3.3 `/stop` — 中止當前執行

停止 agent 當前正在執行的任務，但不清空 session。

### 3.4 CLI 層級的重置

```bash
# 重置設定（不影響 session）
openclaw reset --scope config

# 重置設定 + 憑證 + session
openclaw reset --scope config+creds+sessions

# 完全重置
openclaw reset --scope full

# 預覽不執行
openclaw reset --dry-run
```

> 建議先跑 `openclaw backup create` 再做 CLI reset。

## 4. 各平台最佳實踐

### 4.1 Discord：開新 Thread（推薦）

在 Discord 中，**最優雅的做法是直接開新 Thread**，而不是打 `/new`。新 Thread 有全新的 Channel ID，OpenClaw 自動分配新 Session Key。

好處：

- 舊對話完整保留在原 Thread
- 新對話完全乾淨
- 等同 WebUI「開新 tab + 舊 tab 存檔」的體驗

### 4.2 Telegram DM

只能用 `/new`，因為 Telegram DM 沒有 Thread 機制。舊訊息視覺上還在畫面，但 agent 已重置。

### 4.3 WebUI

直接點 `/new` 或側邊欄的「新對話」按鈕。

## 5. 記憶系統 (Memory)

Session 重置只清除**對話歷史**，不影響持久記憶。OpenClaw 的記憶是純 Markdown 檔案：

| 檔案 | 用途 | 載入時機 |
| :--- | :--- | :--- |
| `MEMORY.md` | 長期記憶（持久事實、偏好） | 每次 session 開始 |
| `memory/YYYY-MM-DD.md` | 每日筆記（短期 context） | 今天和昨天的自動載入 |
| `DREAMS.md` | 記憶整合日誌（optional） | 背景 dreaming 產出 |

### 5.1 記憶工具

Agent 可以使用兩個工具存取記憶：

- **`memory_search`** — 語意搜尋（向量 + 關鍵字混合）
- **`memory_get`** — 直接讀取特定檔案或行範圍

### 5.2 清除記憶

| 操作 | 方法 |
| :--- | :--- |
| 清除對話歷史（保留記憶） | `/new` |
| 清除對話歷史 + 記憶 | `/new --clear-memory` |
| 修復記憶索引 | `openclaw memory status --fix` |
| 手動清除長期記憶 | 直接編輯或刪除 workspace 內的 `MEMORY.md` |
| 手動清除每日筆記 | 刪除 `memory/` 目錄下的 `.md` 檔案 |

### 5.3 Active Memory（選用外掛）

啟用後，agent 會在回覆前**主動搜尋**記憶，自動注入相關 context：

```json5
{
  "plugins": {
    "entries": {
      "active-memory": {
        "enabled": true,
        "config": {
          "agents": ["main"],
          "queryMode": "recent",
          "promptStyle": "balanced"
        }
      }
    }
  }
}
```

聊天中控制：`/active-memory on|off|status`

### 5.4 Dreaming（背景記憶整合，選用）

自動在背景執行記憶整合，經過三個階段：

1. **Light** — 暫存短期素材
2. **REM** — 反思並提煉主題
3. **Deep** — 將合格的事實升級到 `MEMORY.md`

所有階段的產出都寫入 `DREAMS.md`，只有 Deep 階段會修改 `MEMORY.md`。

## 6. Session 維護

### 6.1 自動維護設定

```json5
{
  "session": {
    "maintenance": {
      "mode": "enforce",     // "enforce" 自動清理，"warn" 只警告
      "pruneAfter": "30d",   // 超過 30 天的 session 自動清除
      "maxEntries": 500,     // 最多保留 500 個 session
      "rotateBytes": "10mb"  // 單一 transcript 超過 10MB 自動輪轉
    }
  }
}
```

### 6.2 手動清理

```bash
# 預覽清理結果（不執行）
openclaw sessions cleanup --dry-run

# 執行清理
openclaw sessions cleanup --enforce

# 修復遺失的 transcript 檔案
openclaw sessions cleanup --fix-missing

# 列出所有 session
openclaw sessions --all-agents
```

## 7. 常見情境速查

| 我想要... | 做法 |
| :--- | :--- |
| Agent 忘掉剛才的對話 | `/new` |
| Agent 忘掉所有記憶 | `/new --clear-memory` + 手動刪 `MEMORY.md` |
| 換一個模型重新聊 | `/new claude-opus-4-6` |
| Heartbeat 讀到舊指令 | `/new` 重置 session + 確認 `HEARTBEAT.md` 已更新 |
| 清理磁碟空間 | `openclaw sessions cleanup --enforce` |
| 查看 session 狀態 | `/status` 或 `openclaw sessions --json` |
