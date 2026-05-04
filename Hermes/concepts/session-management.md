# Session 管理

Hermes 的 session 設計選擇了 **SQLite + FTS5** 而非 vector DB，且加入了 **lineage tracking** 來處理 context window 不夠時的 compression。本文件解析這些選擇背後的取捨，以及 `/new`、`/reset` 等使用者指令的實際行為。

## 1. Session 是什麼

每段「連續對話」是一個 session。包含：

- 系統 prompt（含 personality、frozen MEMORY/USER）
- 所有輪訊息（user + assistant + tool calls）
- 中介資料（建立時間、平台、使用者、parent session id）

儲存位置：`~/.hermes/sessions/sessions.db`（SQLite）。

## 2. 平台隔離（Per-Platform Isolation）

同一個使用者在不同平台是**不同的 session**：

```text
user_id=12345 + platform=telegram + chat=DM   → session_A
user_id=12345 + platform=telegram + chat=群組X  → session_B
user_id=12345 + platform=discord + channel=#dev → session_C
```

設計理由：

- 平台對話風格不同（Telegram DM 是私密 1:1、Discord 頻道是團隊公共）
- 群組訊息與 DM 不該混雜（不然 agent 在群組發言會帶進私密 context）
- 使用者期待「每個平台是獨立 bot 對話」

`MEMORY.md` / `USER.md` 是**共用**的（同一個人不會因為換平台就變了一個人），但對話歷史隔離。

## 3. Lineage Tracking（壓縮樹）

當 session 對話過長、context window 滿了，**Reasoning Layer 會觸發 compression**：

```text
session_001 (parent)
  ↓ 滿了 → summarize 出摘要
session_002 (child, content="<舊對話摘要>" + 接續新對話)
  ↓ 又滿了
session_003 (grandchild, content="<更短的摘要>" + ...)
```

- 每個 child session 有 `parent_session_id`
- 舊 session **不會刪**，仍可被 search / browse
- Agent 預設只看 current session；要查更早的歷史得用 session search

### 為什麼不直接 truncate？

- **資訊保留**：truncate 會丟掉早期重要決策；summarize 至少保留 gist
- **cache 友善**：truncate 後 prefix 變了，prefix cache 失效；新 session 起頭的 system prompt 反而能 cache hit
- **可追溯**：parent chain 保留下來，使用者要查歷史可順著 lineage 走

## 4. SQLite + FTS5 選擇理由

對比常見選項：

| 方案 | 優點 | 缺點 |
| --- | --- | --- |
| **JSON files** | 簡單 | 慢、不能搜尋、寫入並發風險 |
| **SQLite + FTS5** | 全文索引、ACID、零維護 | 不支援語意搜尋 |
| **Vector DB（chroma 等）** | 語意搜尋強 | 需要 embedding model、磁碟用量大、依賴重 |

Hermes 選 SQLite + FTS5：

- **零依賴**：不需要 embedding API 也能上線
- **典型查詢就是關鍵字**：「上次我們討論 docker dns 的內容」
- **Plugin 化**：要 vector search 可寫 memory provider plugin（連 mem0）

## 5. 原子寫入與並發

每輪對話寫入透過 SQLite transaction，確保：

- 寫到一半斷電不會留 partial record
- Gateway 與 CLI 同時操作不會 corrupt（SQLite WAL mode）

但**仍不能跨容器並發**：兩個 gateway 同時開同一個 db，SQLite 雖然有 lock，但 long-held write lock 會造成嚴重 stall。所以官方明令：

> Never run two Hermes gateway containers against the same data directory simultaneously.

要多 instance → 多資料夾（每個 gateway 容器掛獨立的 `~/.hermes/` volume）。

## 6. 使用者指令行為

### `/new`（與 `/reset` 同義）

依官方文件，`/reset` 是 `/new` 的 **alias**，兩者行為完全一致：

- 建立新的 session（fresh session ID + history）
- 重新讀取 `MEMORY.md` / `USER.md`
- **不影響舊 session**：先前的對話保留在 SQLite 中，仍可 `hermes sessions browse` 或 `list` 查回

適用場景：要切換話題、不想被前面 context 干擾、或當前對話方向偏了想換一個起點。

> 📝 `/new` 不會「刪除」舊 session，只是切走、不再使用。若真的要刪掉，需明確呼叫 `hermes sessions delete <id>`。

### `/clear`

清空 CLI 顯示，但**保留當前 session**。常被誤認為跟 `/new` 一樣，實際上 `/clear` 只動畫面、不換 session。

### `/help` / `/skills` / `/cron` 等

這些是 gateway 層攔截的 slash command，**不會送進 agent loop**，所以不會消耗 LLM token。完整列表見官方 [Slash Commands Reference](https://hermes-agent.nousresearch.com/docs/reference/slash-commands)。

## 7. CLI Session 操作

```bash
# 列出近期 session
hermes sessions list

# 互動瀏覽（瀏覽訊息、跳到 parent）
hermes sessions browse

# 匯出某個 session
hermes sessions export ./out.json --session-id <id>

# 搜尋
hermes sessions list --search "docker dns"

# 刪除（包含 lineage 中的 children）
hermes sessions delete <id>

# 清理過期
hermes sessions prune --older-than 30d

# 統計
hermes sessions stats
```

## 8. Session search 在 agent 內怎麼用

Agent 在對話中可呼叫 `session_search` tool 查過往：

```python
session_search(query="docker dns vpn", limit=5)
# 回傳前 5 個相關 session 的摘要 + 該段對話 quote
```

這比直接 truncate 給 agent 高效：

- 只在需要時才 query（節省 token）
- FTS5 排名 by relevance，不是 by 時間
- 回傳是「片段」不是整 session

實務上 agent 看到「上次討論」、「前面提到」這類關鍵字會自動觸發。

## 9. Lineage 範例

假設你跟 bot 連續聊了一週：

```text
session_a (Mon)
  └─ session_b (Wed, parent=a, 因 token 滿觸發 compression)
       └─ session_c (Fri, parent=b)
            └─ session_d (Sun, parent=c, 你正在這裡)
```

當前對話 = session_d。要查週一講過什麼：

```bash
hermes sessions browse --session-id session_a
```

或在對話中問 agent：「上週一我們討論的 X 是什麼？」agent 會用 session_search 找。

## 10. 實務建議

### 10.1 不要怕 /new

很多人捨不得開新 session，怕「失去 context」。實際上：

- Memory 還在
- Session search 還能查回去
- Token 變便宜（短 prefix）

每天工作開始建議 `/new` 一下，以週為單位 prune 舊 session。

### 10.2 `/reset` 與 `/new` 是同一件事

舊版印象中「`/reset` 會真刪」並不正確 —— `/reset` 只是 `/new` 的 alias，兩者都是「換新 session」而非「清除歷史」。要刪除舊對話請用 `hermes sessions delete <id>` 或 `hermes sessions prune`。

### 10.3 Session 命名

可手動命名 session 方便日後檢索：

```bash
hermes sessions rename <id> "docker-deployment-debugging"
```

## 11. 相關文件

- [Gateway 與 Agent Loop](gateway-and-agent-loop.md)
- [Memory 系統](memory-system.md)
- 官方參考：[Slash Commands](https://hermes-agent.nousresearch.com/docs/reference/slash-commands) ／ [CLI Commands](https://hermes-agent.nousresearch.com/docs/reference/cli-commands)
