# Memory 系統

Hermes 的 memory 設計刻意「兩層分離」：**短期** session 上下文由 Reasoning Layer 處理，**長期**個人化記憶則由兩份固定大小的 Markdown 檔案承載。理解這個設計，才知道為什麼 memory 有「字元上限」、為什麼修改 memory 不會即時影響當前對話。

## 1. 兩個核心檔案

`~/.hermes/memories/` 下有兩份檔案：

### 1.1 `MEMORY.md` — Agent 的個人筆記

- **大小限制**：2,200 字元
- **內容類型**：環境細節、專案慣例、工具偏好、過去的 workaround、完成過的任務
- **由誰維護**：agent 自己（透過 `memory` tool 增刪改）
- **範例**：

    ```markdown
    - User runs Mac M2 with Docker Desktop
    - Project root: ~/Projects/kaka/hermes-server
    - Use `docker compose restart hermes` after .env changes
    - User prefers zh-TW for explanations, but code in English
    ```

### 1.2 `USER.md` — 使用者 Profile

- **大小限制**：1,375 字元
- **內容類型**：個人偏好、時區、技術背景、溝通風格
- **由誰維護**：agent + 使用者明確指示
- **範例**：

    ```markdown
    - Name: Kaka
    - Timezone: Asia/Taipei
    - Preferred tone: concise, direct, technical
    - Skill level: senior engineer (Python, Docker, ML systems)
    - Avoid: long explanations, repeated apologies
    ```

## 2. 為什麼是「Frozen Snapshot」

每個 session 開始時，這兩個檔案會被讀取並**直接拼進 system prompt**。在該 session 結束前，**檔案內容的後續修改不會影響當前對話**。

設計動機：

- **保留 prefix cache**：LLM provider（Anthropic、OpenAI）對相同 prefix 提供 cache hit 折扣。如果 memory 在對話中變動，每輪都得重新付出 prompt token。
- **避免認知不一致**：agent 在同一 session 中認知的「自己記得什麼」要穩定，否則對話邏輯混亂。
- **批次寫入優化**：agent 在 session 中可能多次更新 memory，但實際 disk write 都是即時的；只是「下次 session」才反映在 prompt 上。

## 3. Memory Tool 介面

Agent 透過 `memory` tool 操作這兩個檔案，**沒有 read 動作**（因為內容已在 system prompt 中）。三個 action：

- **add**：新增條目
- **replace**：以 substring matching 改寫既有條目
- **remove**：刪除條目

```python
# agent 內部呼叫示意
memory(action="add", target="MEMORY.md", content="- User uses zsh, not bash")
memory(action="replace", target="MEMORY.md",
       old="prefers terse comments", new="prefers no comments unless WHY non-obvious")
memory(action="remove", target="USER.md", content="- Old preference about X")
```

## 4. Session vs 持久 Memory

Hermes 區分三種「記憶」資源：

| 名稱 | 儲存 | 存活範圍 | 注入 prompt 時機 |
| --- | --- | --- | --- |
| **MEMORY.md / USER.md** | Markdown 檔案 | 永久（直到使用者刪） | 每 session 開始 |
| **Session 對話歷史** | SQLite (`sessions.db`) | 該 session 內 | 該 session 內每輪 |
| **Session search** | SQLite + FTS5 索引 | 永久 | 不自動注入；agent 主動 query |

Session search 讓 agent 在需要時用全文搜尋查過往對話（例如「上次我問你 X 是怎麼設的」），不會因為對話過長而把全部歷史都塞進 context。

## 5. 什麼時候適合放進 MEMORY.md

寫入 memory 的判斷：

- ✅ **環境事實**：「user 的 docker-compose 在 ~/Projects/X」、「VPN 開著時用 cloudflare DNS」。
- ✅ **使用者偏好**：「希望解釋用 zh-TW、code 用英文」、「不要一直道歉」。
- ✅ **專案上下文**：當前正在做 X 專案，要點是 Y、Z。
- ❌ **臨時對話狀態**：「剛才提到的那個 bug」—— 屬於 session 自然會記得。
- ❌ **可以重新查到的程式碼結構**：grep 一下就有，不必占 memory 額度。

## 6. 與 OpenClaw 的差異

OpenClaw 也有類似機制（MEMORY.md、Daily Notes、Dreaming），對比：

| 特性 | OpenClaw | Hermes |
| --- | --- | --- |
| 個人記憶檔 | `MEMORY.md` | `MEMORY.md` + `USER.md` |
| 字元上限 | 軟性（提示注意） | 硬性（2,200 / 1,375） |
| Daily Notes | ✅ 每日自動產生 | ❌ 內建沒有 |
| Dreaming（離線整理） | ✅ | ❌ |
| Session search | 有（vector） | 有（FTS5 全文） |
| 外部 memory provider | 部分支援 | 原生 plugin（honcho、mem0） |

Hermes 強調「精簡、可預期」，OpenClaw 強調「全自動、富表達」。實務上可依需求選擇。

## 7. Pluggable Memory Provider

`hermes memory setup` 可接外部 memory provider，官方目前內建 8 個 plugin：

- **Honcho**：開源、本地優先、結構化
- **OpenViking**：開源、輕量
- **Mem0**：雲端服務、向量化記憶
- **Hindsight**：知識圖譜風格
- **Holographic**：壓縮式長期記憶
- **RetainDB**：可查詢記憶 DB
- **ByteRover**：向量 + 結構混合
- **Supermemory**：雲端跨來源記憶
- **自製 plugin**：`~/.hermes/plugins/memory/<name>/`，實作 `MemoryProvider` ABC

> ⚠️ 任一時間只能啟用**一個**外部 provider，內建 `MEMORY.md` / `USER.md` 仍持續運作。

CLI 操作：

```bash
hermes memory setup     # 互動式選擇與設定 provider
hermes memory status    # 顯示目前啟用的 provider
hermes memory off       # 關閉外部 provider（保留內建 memory）
```

> ⚠️ 切到外部 provider 後，`MEMORY.md` / `USER.md` 不會自動同步。要先匯出 / 重新填寫。

## 8. ContextEngine：壓縮與壓力閾值

當對話超出 context window 時，**ContextEngine** 介入做 compression。

- 預設實作：lossy summarization（把舊對話摘要成短文字）
- 可寫 plugin 取代：`~/.hermes/plugins/context_engines/<name>/`
- 觸發條件：剩餘 token 預算低於閾值時

Compression 後會建立**新 session（child）**，舊 session 標記為 parent，形成 lineage tree。詳見 [Session 管理](session-management.md)。

## 9. 實務建議

1. **不要用 memory 存程式碼結構**：那是 grep 的事，不是 memory 的事。
2. **明確指示比隱性學習可靠**：直接跟 agent 說「請記住我用 zsh」比期待它 inferring 來得確定。
3. **定期 review memory**：每隔一陣子 `cat ~/.hermes/memories/MEMORY.md`，把過時內容刪掉。
4. **多 profile 分隔工作 / 個人 memory**：透過不同 `~/.hermes/` 目錄（或 docker volume）拆分 profile。

## 10. 相關文件

- [Gateway 與 Agent Loop](gateway-and-agent-loop.md)
- [Session 管理](session-management.md)
- 官方參考：[Memory Feature](https://hermes-agent.nousresearch.com/docs/user-guide/features/memory) ／ [CLI Commands](https://hermes-agent.nousresearch.com/docs/reference/cli-commands)
