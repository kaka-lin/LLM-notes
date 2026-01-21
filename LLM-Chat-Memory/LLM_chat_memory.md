# LLM Chat Memory 兩種常見方式整理

本文件整理兩種常見的「LLM 對話記憶（chat memory）」作法：

1. **外部 Chat Memory（獨立儲存）**：把對話狀態存到外部 storage，再在每次請求時取回。
2. **Prompt Templating + Conditional Context Injection（條件式注入）**：像 PR-Agent 目前的做法，把「對話/回饋」從 PR thread 抓出來，透過 Jinja2 template `{% if question_str %}` 把它插入 prompt。

> 名詞對齊：
>
> - **Prompt templating**：用模板語法（例如 Jinja2）把變數渲染成最終 prompt
> - **Context injection**：把外部資訊（對話、規則、diff）注入到 prompt
> - **(Windowed) conversational memory**：只保留最近 N 則對話的「視窗型記憶」

---

## 選擇建議

- 你要的是 **最低部署成本、最少依賴、可審計、多人共享上下文**： 優先用 **條件式 prompt 注入**（尤其像 PR / issue thread 這種本來就有 comment timeline 的場景。
- 你要的是 **跨請求長期記憶、跨 thread/session 的偏好、超長對話的檢索/摘要、私有記憶不想寫在公開 thread**： 考慮 **外部 chat memory**（DB/redis/vector store）。
- 很多成熟系統會走 **Hybrid**：外部 memory（摘要/檢索） + 最後仍然注入 prompt（讓模型當次看得到）。

---

## 方式 1: 外部 Chat Memory

### 外部記憶的核心概念

把對話歷史（messages）、摘要（summary）、偏好（preferences）、工具呼叫結果等，存到外部儲存（DB/Redis/向量庫）。
每次 LLM 呼叫時，依照 **session id / user id / thread id** 取回相關記憶，再組成 prompt 或做 RAG 檢索。

### 常見實作形態

- **Raw transcript store**：直接存完整 messages（user/assistant）。
- **Summary store**：對很久的歷史做摘要，減少 token。
- **Vector memory / RAG**：把歷史 or 重點 chunk 做 embedding，按 query 相似度取回。
- **Structured memory**：把「決策/限制/偏好」抽成結構化欄位（JSON），例如：語言偏好、輸出格式、禁止事項。

### 解決的痛點

- **長期/跨回合**：模型本身無記憶，外部 store 可以跨請求保存。
- **超長對話 token 不夠**：用摘要 or 檢索只取 relevant parts。
- **跨 thread / 跨任務共享偏好**：例如同一個 user 的風格偏好、公司規範。
- **不想把記憶暴露在公開介面**：可以私有保存（前提是你自己負責權限與合規）。

### 優點

- **可真正做到長期記憶**。
- **可做精準檢索**（RAG），減少 token 浪費。
- **可跨多種 UI / 通道** 共用記憶。
- **更容易做結構化規則**：把約束變成欄位，而不是混在文字裡。

### 缺點 / 成本

- **部署複雜度高**：需要 DB/Redis/vector store、schema、migrations、監控。
- **權限/隔離難題**：多租戶、不同 repo/project 的資料隔離、誰可以讀寫。
- **資料治理**：retention、刪除、PII/敏感資訊處理、備份與加密。
- **除錯成本**：模型行為不符合預期時，要追「取回了哪些記憶、為什麼」。

### 適合情境

- 產品型聊天助理。
- 多渠道（Web/Slack/API）共享同一個 session。
- 對話可能很長，需要摘要/檢索。
- 有明確的資料合規/權限模型與基礎設施支援。

## 方式 2: Conditional Prompt Templating (條件式提示詞模板化)

> 以下用 [PR Agent](https://github.com/qodo-ai/pr-agent/tree/main) 解說。

### Prompt Templating 的核心概念

把「記憶」視為 **prompt 的一部分**：

1. 從某個可取得的外部來源抓上下文（例如 PR comments、issue comments、單次 UI session）
2. 轉成一段可讀文字（chat window / bullet points）
3. 在 prompt template 裡用條件式 block 注入：

```jinja2
{%- if answer_str %}
User input context:
-----
{{ answer_str }}
-----
{%- endif %}
```

> [!IMPORTANT]
> 「在使用模板化時，需注意對 User Input (answer_str) 進行基本的過濾或格式化，防止潛在的提示詞注入攻擊。」

### 解決的痛點

- **模型無狀態**：每次請求都把必要上下文塞進 prompt，讓它「看起來有記憶」。
- **低成本/低依賴**：不用 DB、不用 vector store。
- **多人共享上下文**（在 Git PR thread）：所有人看到的 comment timeline 就是共同的上下文來源。

### 優點

- **部署最簡單**：幾乎不用額外 infra。
- **可審計/可回溯**：記憶本身存在原本就會保存的地方（例如 PR comments）。
- **權限天然一致**：能看到 PR comments 的人才能看到上下文（交給 Git provider 控管）。
- **行為可預期**：prompt 裡放了什麼，一眼可查。

### 缺點 / 限制

- **受 token 限制**：上下文太長很容易爆炸。**開發者通常需在 Jinja2 模板中實作 `last_n_messages` 邏輯，手動控制 Context Window 的長度。**
- **檢索不精準**：通常是「最近 N 則」而非「與當次問題最相關」。
- **資訊可能太 noisy**：thread 太雜會污染 prompt（需要格式化、摘要或過濾）。
- **私有性較差**：如果你把 sensitive context 寫在公共 thread，它就公開了（除非該平台本來就私有）。


### 適合情境

- PR review / code suggestion 這種「thread 有天然 timeline」的產品。
- 你只需要短期記憶（最近幾輪討論），不需要跨 PR 長期偏好。
- 你要快速落地、低維運。

---

## 對照表

| 面向 | 外部 Chat Memory | 條件式提示詞模板化 |
| --- | --- | --- |
| 技術本質 | **狀態化存儲 (Stateful)** | **無狀態傳遞 (Stateless / Templated)** |
| 記憶範圍 | 可長期、跨 session | 通常僅限於當前對話視窗 (Windowed) |
| Token 成本 | 透過 RAG/摘要精確控制，成本相對穩定 | 隨對話增長線性上升，直至達到模型上限 |
| 部署複雜度 | 高（需額外維護數據庫與檢索邏輯） | 極低（僅需處理字串與模板渲染） |
| 可審計性 | 需透過 Log 系統追蹤檢索紀錄 | 極高（Prompt 本身即是完整的執行脈絡） |
| 權限/隔離 | 需自行實作多租戶與資料權限控管 | 常直接繼承平台權限 (如 Git provider/Slack) |
| 典型場景 | 客服機器人、個人化 AI 助理 | **PR 審閱工具、單次工作流自動化、腳本** |

---

## Hybrid

很多系統會把兩者結合：

1. **先把長對話做摘要或向量檢索**：取回「與當次任務最相關」的幾段。
2. **再把取回結果注入 prompt**：模型當次真的看得到，才能影響輸出。

Hybrid 通常能同時解決：

- token 爆炸（摘要/檢索）
- 規則/決策延續
- 多來源上下文（PR thread + 外部偏好）
