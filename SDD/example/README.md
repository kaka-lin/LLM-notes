# SDD Example — URL Shortener

最小可跑的 SDD 範例. 三層構成一個閉環:

- [spec/url_shortener.md](spec/url_shortener.md): 規格 (REQ / CON / DAT / AC 編號化).
- [app/main.py](app/main.py): 實作, 每段邏輯註解對應到 spec 編號.
- [tests/test_main.py](tests/test_main.py): 測試, 每個 test 對應一條 AC.

## 目錄結構

```text
example/
├── README.md
├── pyproject.toml
├── app/                # 實作
│   ├── __init__.py
│   └── main.py
├── tests/              # pytest 測試
│   └── test_main.py
├── spec/               # 規格 (single source of truth)
│   └── url_shortener.md
└── data/               # runtime artifact (gitignore 候選)
    └── shortener.db
```

`spec/` / `app/` / `tests/` / `data/` 四層分離的用意:

- **`spec/`**: 規格層, 屬於版本控管的事實來源.
- **`app/`**: 實作層, import 路徑為 `app.main:app`.
- **`tests/`**: pytest 預設搜尋的測試目錄, 與實作分離方便獨立打包.
- **`data/`**: runtime 產物 (DB 檔、暫存), 不影響規格或實作邏輯.

## 安裝

使用 [uv](https://docs.astral.sh/uv/) 管理環境與相依套件. 本資料夾已附 [pyproject.toml](pyproject.toml), 直接同步即可:

```bash
uv sync
```

## 跑起來

```bash
uv run uvicorn app.main:app --reload --port 8080
```

呼叫範例:

```bash
curl -X POST http://localhost:8080/shorten \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}'

# 回傳 {"short_code": "xxxxxx"}, 然後用該 code 重導:
curl -I http://localhost:8080/<short_code>
```

啟動後會自動在 [data/](data/) 建立 `shortener.db`.

## 跑測試

```bash
uv run pytest -v
```

## 怎麼看出 SDD 的對應

任選一條 REQ / CON / AC, 在三層 grep:

```bash
grep -rn "REQ-003" spec/ app/ tests/
grep -rn "AC-001"  spec/ app/ tests/
grep -rn "CON-001" spec/ app/ tests/
```

每條都應該至少能在 spec / 實作 / 測試三邊各 grep 到一次.
這就是 SDD 的可追溯性 (traceability) — 任一處都能對齊其他兩處.
