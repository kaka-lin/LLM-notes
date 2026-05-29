# Spec-Driven Development (SDD)

規格驅動開發學習筆記.

## 1. 核心概念

**規格 (specification) 是事實的唯一來源 (single source of truth), 程式碼是規格的衍生物.**

傳統開發是「想到什麼寫什麼, 文件事後補」; SDD 反過來 — 先把要做什麼、邊界在哪、怎麼驗收, 全部寫成可引用的規格, 然後才寫程式碼.

一句話總結:

> 先把要做什麼想清楚, 寫成可引用的規格; 程式碼只是規格的一種表達形式.

## 2. 跟其他方法的對比

| 方法 | 主導者 | 核心產物 | 程式碼地位 |
| --- | --- | --- | --- |
| Code-first | 工程師憑經驗 | 程式碼 | 事實來源 |
| Test-Driven (TDD) | 測試 | 測試案例 | 通過測試的最小實作 |
| Behavior-Driven (BDD) | Given/When/Then 場景 | 情境描述 | 對應情境的實作 |
| **Spec-Driven (SDD)** | **規格文件** | **編號化的需求/契約/驗收** | **規格的具體實作** |
| Doc-driven | 文件 | 使用說明 | 配合文件的實作 |

SDD 跟 BDD / TDD 不衝突 — 規格通常會「往下」展開成測試案例 (AC → test).

## 3. 一份好的 spec 由哪些部分組成

典型結構:

1. **目的與範圍** — 這份規格管什麼、不管什麼.
2. **名詞定義** — 統一術語, 避免 user / player / member 混用.
3. **功能需求 (REQ-xxx)** — 系統應該做什麼, 一條一個編號.
4. **限制 (CON-xxx)** — timeout、rate limit、payload 上限這類運行邊界.
5. **指引 (GUD-xxx)** — 不是硬性需求但建議的做法.
6. **資料契約 (DAT-xxx)** — DB schema、API payload 形狀.
7. **介面契約** — HTTP endpoints、event payload、provider interface.
8. **驗收條件 (AC-xxx)** — 怎麼算「做完」.
9. **測試策略** — 用什麼方式驗證.
10. **相依性、外部整合、合規**.

## 4. 三個關鍵設計

### 4.1 編號化 (Identifier-based traceability)

每條需求都有 `REQ-001`, `DAT-005`, `AC-012` 這種唯一 ID. 這個 ID 會出現在:

- 程式碼註解 / 模組說明
- Commit message / PR description
- 測試函式名 (例如 `test_req_019_intimacy_exp_clamping`)
- TODO / deferred list
- Code review 討論

結果是: **任何一行程式碼都可以反查到它存在的理由**, 任何一條規格都可以正向追到它的實作與測試.

常見的前綴慣例:

| 前綴 | 全稱 | 範圍 |
| --- | --- | --- |
| REQ | Requirement | 功能需求 |
| CON | Constraint | 運行限制 |
| GUD | Guideline | 指引與模式 |
| DAT | Data / Contract | 資料與契約 |
| AC | Acceptance Criteria | 驗收條件 |
| COM | Compliance | 合規相依 |
| DEP | Dependency | 相依性 |
| EXT | External | 外部系統 |

### 4.2 Deferred scope 顯式化

SDD 區分「規格存在」與「已實作」. 沒做的部分要明確寫進 `TODO.md` 或在規格條目中標 deferred, 例如:

> Phase 1 已實作獨立 endpoint 與獨立 provider; 每日 5 次免費額度、超出後計費、每日 00:00:01 重置仍為 **deferred scope**.

這樣團隊 (與 AI) 都知道**邊界在哪**, 不會偷偷把延後的做掉, 也不會以為某功能存在.

### 4.3 規格是 source of truth

改規格 → 改程式碼 → 改測試, 順序不可以倒過來. 程式碼跟規格不一致時, 永遠是程式碼錯, 不是規格錯.

任何 feature 變更必須先做 **spec impact check**: 是否影響 API 契約、SSE / event 序列、persistence model、provider 行為、安全策略. 影響到就先更新 spec.

## 5. 工作流程

```text
1. 提需求
   ↓
2. 寫 / 更新 spec (REQ-xxx, DAT-xxx, AC-xxx)
   ↓
3. spec impact check (是否影響契約 / schema / provider...)
   ↓
4. 不能立即做的 → 放 TODO.md (標 deferred)
   ↓
5. 實作 — 程式碼註解引用 REQ-ID
   ↓
6. 寫測試對應 AC-xxx
   ↓
7. Code review 用 spec 當對照表
   ↓
8. 合併, spec 與程式碼同步更新
```

## 6. 推薦的目錄結構

實務上把規格放在獨立目錄, 跟程式碼、runtime 產物分開. 一個常見佈局:

```text
my-service/
├── AGENTS.md           # 給 AI agent 的工作規則, 引用 spec/ 為事實來源
├── TODO.md             # 顯式列出 deferred 需求
├── pyproject.toml
├── app/                # 實作 — import 路徑 app.main:app
│   ├── __init__.py
│   ├── main.py
│   ├── models.py
│   └── services/
├── tests/              # pytest 測試 — test 名引用 AC / REQ ID
│   ├── conftest.py
│   └── test_*.py
├── spec/               # 規格 — single source of truth
│   └── SERVICE_NAME_SPEC.md
└── data/               # runtime artifact (SQLite, fixtures, dumps)
```

要點:

- **`spec/` 與實作分離**: 規格是契約, 不該跟實作檔混在同一層, 避免 review 時被淹沒.
- **`app/` 與 `tests/` 平行**: 對齊 pytest 與 Python packaging 慣例; `tests/` 可獨立打包或排除.
- **`data/` 與 spec 分離**: runtime 產物 (DB 檔、暫存) 不影響規格邏輯, 通常 gitignore.
- **`AGENTS.md` 在 root**: AI agent 第一個讀的入口, 內含 spec 路徑、commit gate、deferred 政策.

## 7. 簡單範例

以一個 **URL Shortener API** 示範完整對應關係. 完整檔案在 [example/](example/), 採用上述目錄佈局.

### 7.1 規格片段 (spec/url_shortener.md)

```markdown
## 需求

- REQ-001: 系統應接受 HTTP POST `/shorten` 請求, body 為 `{"url": <string>}`, 回傳 `{"short_code": <string>}`.
- REQ-002: `short_code` 長度應為 6 個字元, 由 a-z, A-Z, 0-9 組成.
- REQ-003: 重複呼叫同一個 URL 應回傳相同 `short_code` (冪等性).
- REQ-004: 系統應接受 HTTP GET `/{short_code}`, 若存在則 302 重導向至原始 URL, 否則回傳 404.

## 限制

- CON-001: URL 長度上限為 2048 字元, 超過回傳 400.
- CON-002: 無效 URL 格式 (缺少 scheme / host) 回傳 400.

## 資料契約

- DAT-001: 短網址對應儲存於 SQLite, schema 為 `mappings(short_code TEXT PRIMARY KEY, original_url TEXT NOT NULL UNIQUE, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)`.

## 驗收條件

- AC-001: POST `/shorten` 同一個 URL 兩次, 兩次回傳的 short_code 必須相等.
- AC-002: GET `/{不存在的 code}` 回傳 status 404.
- AC-003: POST `/shorten` 帶 2049 字元的 URL 回傳 status 400.

## Deferred

- 自訂短網址 (custom alias) → TODO
- 過期時間 (TTL) → TODO
- 點擊計數 → TODO
```

### 7.2 實作片段 (app/main.py)

```python
# REQ-001, REQ-002, REQ-003 — POST /shorten
@app.post("/shorten")
def shorten(req: ShortenRequest) -> ShortenResponse:
    # CON-001
    if len(req.url) > 2048:
        raise HTTPException(400, "URL too long")
    # CON-002
    if not is_valid_url(req.url):
        raise HTTPException(400, "Invalid URL")

    # REQ-003 冪等性: 先查現有對應
    existing = store.get_by_url(req.url)
    if existing:
        return ShortenResponse(short_code=existing)

    code = generate_code()  # REQ-002
    store.insert(code, req.url)  # DAT-001
    return ShortenResponse(short_code=code)
```

### 7.3 測試片段 (tests/test_main.py)

```python
def test_ac_001_same_url_returns_same_code(client):
    """AC-001: POST /shorten 同一個 URL 兩次, short_code 必須相等."""
    r1 = client.post("/shorten", json={"url": "https://example.com"})
    r2 = client.post("/shorten", json={"url": "https://example.com"})
    assert r1.json()["short_code"] == r2.json()["short_code"]


def test_ac_002_missing_code_returns_404(client):
    """AC-002: GET 不存在的 code 回傳 404."""
    r = client.get("/abc999")
    assert r.status_code == 404


def test_ac_003_url_too_long_returns_400(client):
    """AC-003: 2049 字元 URL 回傳 400."""
    long_url = "https://example.com/" + "x" * 2030
    r = client.post("/shorten", json={"url": long_url})
    assert r.status_code == 400
```

### 7.4 看出來的好處

- 拿到任何一段程式碼, 都能反查到對應的 REQ / CON / DAT.
- 拿到 spec 任何一條, 都能 grep 出實作與測試位置.
- 新人 (或 AI agent) 接手只要讀 spec 就能知道「應該做什麼、什麼不該做、哪些是延後」.
- Code review 不再依賴口頭傳統知識, spec 條目就是 review checklist.

## 8. SDD 在 AI 時代的復興

「規格驅動」這個概念其實一直存在, 在「契約即產品」或合規敏感領域早就是標配:

| 領域 | 形式 | 已存在多久 |
| --- | --- | --- |
| 航太 / 醫療 / 金融 | 形式化規格、需求追溯矩陣 | 數十年 |
| API / SDK | OpenAPI、Protobuf、GraphQL schema | 10+ 年 |
| Web 標準 | W3C / IETF RFC | 30+ 年 |
| 區塊鏈 | EIP、BIP | 10+ 年 |
| 大型企業內部 | RFC / Design Doc 文化 (Google、Amazon) | 20+ 年 |

最近 (2024~2026) 明顯回溫的推手是 AI coding agent:

- **GitHub Spec Kit** — GitHub 官方推的 spec-driven workflow toolkit.
- **Amazon Kiro** — AWS 推的 IDE, 主打 spec-driven AI development.
- **AGENTS.md 約定** — OpenAI Codex / Cursor / Claude Code 對「給 AI 看的規則檔」形成共識.
- **Anthropic / OpenAI 官方 best practice** — 都強調給 agent 明確的 spec 與護欄.
- **"Vibe coding" 的反作用力** — AI 隨手生成程式碼很快, 但維護災難浮現後, 社群開始補規格層.

### 為什麼 AI 把 SDD 推回主流

不是 SDD 變好, 是沒有 SDD 的代價在 AI 時代被放大:

- **AI 寫得太快** — 一天生 5000 行, 沒規格就沒人知道哪些該保留.
- **AI 沒有長期記憶** — 每次 session 都要重新理解專案, 規格是唯一可靠的對齊基準.
- **AI 容易過度發揮** — 沒護欄就會偷加功能、偷改契約.
- **多 agent 協作** — agent A 和 agent B 必須對著同一份 spec 工作, 不然會打架.
- **Code review 變瓶頸** — AI 產出量大, 人類審查跟不上, 需要 spec 當對照表加速.

SDD 從「奢侈品」變成「AI 協作的基礎建設」.

## 9. 何時用、何時不用

適合 SDD:

- 長期維護的系統 (後端服務、平台、SDK)
- 多人協作 / 大量 AI 協作
- API 或契約本身就是產品
- 合規敏感 (金融、醫療、隱私)

不適合 SDD:

- 新創早期 / MVP — 還在找 PMF, 規格寫完就過時.
- 個人專案 / 探索性研究 — 殺雞用牛刀.
- 前端 UI / 設計密集 — 設計稿和原型本身就是規格.
- 腳本 / 一次性工具 — 純浪費時間.

業界更常見的是**混合策略**:

- 核心契約 (API、persistence、安全) 用 SDD.
- 內部實作細節用 code-first + 良好命名 + 測試.
- UI / 互動用設計稿 + Storybook 驅動.

判斷標準: **這個程式碼要活幾年, 會有多少人 (含 AI) 接手?** 答案越大, SDD 投資回報越高.

## 10. 工具與生態

- **GitHub Spec Kit** — Spec-driven 工作流範本.
- **Amazon Kiro** — Spec-first AI IDE.
- **AGENTS.md** — AI agent 工作規則檔的社群約定 (見本專案 [LLM-notes/AGENTS.md](../AGENTS.md) 範例).
- **OpenAPI / AsyncAPI / Protobuf** — API / event 層級的形式化契約.
- **JSON Schema / Pydantic** — runtime 驗證, 把契約映射到程式碼.
- **ADR (Architecture Decision Record)** — 設計決策的長期紀錄, 跟 spec 互補.
- **Linear / Notion** — 需求編號可以直接掛 ticket ID.

## 11. 延伸閱讀

- GitHub Spec Kit: <https://github.com/github/spec-kit>
- Amazon Kiro: <https://kiro.dev>
- AGENTS.md 約定討論: <https://agents.md>
- Google 的 Design Doc 文化 (How Google Tests Software, ch. 設計文件部分)

## 相關主題

- [AI-Coding-Skills](../AI-Coding-Skills/) — 為 AI agent 加上紀律的開源 skill / workflow 套件研究 (gstack, superpowers 等). SDD 是方法論層次, 這些是具體可裝的工具; 兩者可搭配 — 例如用 SDD 寫好 spec, 再用 superpowers 的 TDD 流程實作.
