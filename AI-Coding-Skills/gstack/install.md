# gstack 安裝指南

直接照官方 README 跑指令很容易卡住，因為 gstack 的「安裝」其實同時做兩件事，而且依「agent / 單人 vs 團隊」分成 5 種變化。先看完前半段心智模型再去對指令，會省很多時間。

## 1. 先理解兩個核心觀念

### 1.1 一次安裝 = 兩件事

gstack 本質上就是一堆 **skill 檔案**（`/office-hours`、`/qa` 那些 slash command）。所以「安裝」同時包含：

1. **把 skill 檔案放到對的目錄**（讓你的 AI agent 找得到）
2. **改你的 config 檔**（`CLAUDE.md` 或 `AGENTS.md`，告訴 AI「哦對了你身上多了這些技能、規矩是這樣這樣」）

所以**單純 `git clone` 不算安裝完**。這就是為什麼官方建議「貼 prompt 給 Claude Code」—— 讓 AI 一口氣把兩件事都做完。

### 1.2 路徑常識

| 場景 | clone 到哪 |
| --- | --- |
| Claude Code / OpenClaw（透過 Claude Code） | `~/.claude/skills/gstack` |
| 其他 host（Codex / Cursor / …） | `~/gstack`（然後 setup 會把 skill 散到該 host 的目錄） |

別搞混，否則 setup 找不到東西。

## 2. 5 種安裝方式對應誰

| # | 名稱 | 給誰用 | 是替代還是疊加？ |
| --- | --- | --- | --- |
| 1 | Step 1 個人安裝 | Claude Code 用戶 | 基礎 |
| 2 | Step 2 團隊模式 | Claude Code + 共用 repo | 疊在 Step 1 之上 |
| 3 | OpenClaw 主流程 | OpenClaw 用戶（要全部 23 個 skill） | 底下還是要做 Step 1 那段 clone+setup |
| 4 | OpenClaw ClawHub 原生 skill | OpenClaw 用戶（只要輕量 4 個） | 可獨立、也可跟 3 並存 |
| 5 | 其他 agent（`--host`） | 用 Codex / Cursor / 等等 | 取代 Step 1 |

## 3. 決策樹

```
你主要用什麼 agent？
│
├── Claude Code
│   ├── 自己一個人      ─→ §4.2 Step 1
│   └── 跟隊友共用 repo ─→ §4.2 Step 1 + §4.3 Step 2
│
├── OpenClaw
│   ├── 要全部 23 個 skill ─→ §4.4（底下還是裝 Claude Code）
│   └── 只要輕量 4 個      ─→ §4.5（也可以跟 §4.4 並存）
│
└── 其他（Cursor / Codex / …）─→ §4.6
```

## 4. 詳細指令

### 4.1 系統需求

- **Claude Code**（或對應 host）
- **Git**
- **Bun v1.0+**（gstack 內部腳本用 Bun 跑，不是 Node）
- **Node.js**（只有 Windows 需要）

沒裝 Bun 的話：

```bash
# macOS / Linux
curl -fsSL https://bun.sh/install | bash
# 或
brew install bun

# Windows（PowerShell）
powershell -c "irm bun.sh/install.ps1 | iex"
```

### 4.2 Step 1：Claude Code 個人安裝

**不要**自己貼 shell 指令到 terminal。打開 Claude Code，把整段下面這個 prompt 貼進去：

> Install gstack: run `git clone --single-branch --depth 1 https://github.com/garrytan/gstack.git ~/.claude/skills/gstack && cd ~/.claude/skills/gstack && ./setup` then add a "gstack" section to CLAUDE.md that says to use the /browse skill from gstack for all web browsing, never use mcp__claude-in-chrome__\* tools, and lists the available skills: /office-hours, /plan-ceo-review, /plan-eng-review, /plan-design-review, /design-consultation, /design-shotgun, /design-html, /review, /ship, /land-and-deploy, /canary, /benchmark, /browse, /connect-chrome, /qa, /qa-only, /design-review, /setup-browser-cookies, /setup-deploy, /setup-gbrain, /retro, /investigate, /document-release, /document-generate, /codex, /cso, /autoplan, /plan-devex-review, /devex-review, /careful, /freeze, /guard, /unfreeze, /gstack-upgrade, /learn. Then ask the user if they also want to add gstack to the current project so teammates get it.

Claude Code 會：

1. clone repo 到 `~/.claude/skills/gstack`
2. 跑 `./setup`
3. 在你的 **全域 `CLAUDE.md`** 寫入 gstack 區塊（列出 skill、規定 `/browse` 走 gstack、禁用 `mcp__claude-in-chrome__*`）
4. 問你要不要把這份設定也加進當前 repo

### 4.3 Step 2：團隊模式（Claude Code + 共用 repo）

做完 Step 1 之後，在你的 repo 根目錄跑：

```bash
(cd ~/.claude/skills/gstack && ./setup --team) \
    && ~/.claude/skills/gstack/bin/gstack-team-init required \
    && git add .claude/ CLAUDE.md \
    && git commit -m "require gstack for AI-assisted work"
```

- repo 內**不會 vendor gstack 檔案**，只塞一個 pointer
- 每位隊友開 Claude Code session 時自動 update check（限流 1 次 / 小時，斷網安全、完全靜默）
- `required` 強制隊友啟用；想只是建議就改 `optional`

### 4.4 OpenClaw 主流程（透過 Claude Code session）

OpenClaw 透過 ACP 生 Claude Code session 來做事，所以**底下還是要先讓 Claude Code 裝好 gstack**。打開 OpenClaw agent，貼這段：

> Install gstack: run `git clone --single-branch --depth 1 https://github.com/garrytan/gstack.git ~/.claude/skills/gstack && cd ~/.claude/skills/gstack && ./setup` to install gstack for Claude Code. Then add a "Coding Tasks" section to AGENTS.md that says: when spawning Claude Code sessions for coding work, tell the session to use gstack skills. Include these examples — security audit: "Load gstack. Run /cso", code review: "Load gstack. Run /review", QA test a URL: "Load gstack. Run /qa https://...", build a feature end-to-end: "Load gstack. Run /autoplan, implement the plan, then run /ship", plan before building: "Load gstack. Run /office-hours then /autoplan. Save the plan, don't implement."

差別在配置檔是 `AGENTS.md`（OpenClaw 看的），不是 `CLAUDE.md`。設定完之後對 OpenClaw 講自然語言就會自動派工：

| 你說 | 結果 |
| --- | --- |
| 「Fix the typo in README」 | 純 Claude Code session，不載 gstack |
| 「Run a security audit on this repo」 | Spawn Claude Code，跑 `/cso` |
| 「Build me a notifications feature」 | Spawn Claude Code，`/autoplan` → 實作 → `/ship` |
| 「Help me plan the v2 API redesign」 | Spawn Claude Code，`/office-hours` → `/autoplan`，存 plan 不實作 |

進階派工 / `gstack-lite`、`gstack-full` prompt template 看 [`docs/OPENCLAW.md`](https://github.com/garrytan/gstack/blob/main/docs/OPENCLAW.md)。

### 4.5 OpenClaw ClawHub 原生 skill（不必開 Claude Code）

```bash
clawhub install gstack-openclaw-office-hours \
    gstack-openclaw-ceo-review \
    gstack-openclaw-investigate \
    gstack-openclaw-retro
```

這 4 個是對話式 skill，OpenClaw 直接在聊天裡跑，**不用 spawn Claude Code session**：

- `gstack-openclaw-office-hours`：6 個強制提問做產品 reframe
- `gstack-openclaw-ceo-review`：4 種 scope 模式做策略挑戰
- `gstack-openclaw-investigate`：根因調試方法論
- `gstack-openclaw-retro`：週度工程回顧

跟 §4.4 是兩條獨立的路，可以**同時並存** —— 輕量任務用 ClawHub 4 個、重任務 spawn Claude Code 跑剩下 19 個。

### 4.6 其他 AI agent（Codex / Cursor / OpenCode / …）

clone 到 **`~/gstack`**（注意路徑不一樣）：

```bash
git clone --single-branch --depth 1 \
    https://github.com/garrytan/gstack.git ~/gstack
cd ~/gstack && ./setup
```

`setup` 會自動偵測你裝了哪些 agent；要強制指定就加 `--host <name>`：

| Agent | Flag | 安裝路徑 |
| --- | --- | --- |
| OpenAI Codex CLI | `--host codex` | `~/.codex/skills/gstack-*/` |
| OpenCode | `--host opencode` | `~/.config/opencode/skills/gstack-*/` |
| Cursor | `--host cursor` | `~/.cursor/skills/gstack-*/` |
| Factory Droid | `--host factory` | `~/.factory/skills/gstack-*/` |
| Slate | `--host slate` | `~/.slate/skills/gstack-*/` |
| Kiro | `--host kiro` | `~/.kiro/skills/gstack-*/` |
| Hermes | `--host hermes` | `~/.hermes/skills/gstack-*/` |
| GBrain（mod） | `--host gbrain` | `~/.gbrain/skills/gstack-*/` |

其他 flag：

- `--no-prefix`：用短指令（`/qa`）
- `--prefix`：用命名空間版（`/gstack-qa`），避免跟其他 skill 撞名

想加新 host 改一個 TypeScript config 就好，零程式變動 —— 見 [`docs/ADDING_A_HOST.md`](https://github.com/garrytan/gstack/blob/main/docs/ADDING_A_HOST.md)。

> ⚠️ 跟 Claude Code 那條路徑不同：這邊**沒有官方 prompt 自動改 config**，每個 agent 規矩不同，你要自己負責讓 agent 認得這些 skill。

## 5. 解除安裝

```bash
~/.claude/skills/gstack/bin/gstack-uninstall [--keep-state] [--force]
```

repo 已被刪掉的情況，手動清這幾個位置：

- `~/.claude/skills/gstack*`
- `~/.gstack`
- 各 host 目錄下的 `gstack*`（例：`~/.codex/skills/gstack*`、`~/.cursor/skills/gstack*` 等）

## 6. 平台需求補充

- **macOS / Linux**：完整 symlink，`git pull` 即更新
- **Windows 11**：需要 Git Bash 或 WSL；Bun 之外**必須**裝 Node.js；symlink 改成檔案複製，每次 `git pull` 後要再跑一次 `./setup`

## 7. 延伸閱讀

- 官方 install 段：<https://github.com/garrytan/gstack#install--30-seconds>
- OpenClaw 進階派工：[`docs/OPENCLAW.md`](https://github.com/garrytan/gstack/blob/main/docs/OPENCLAW.md)
- 新增 host 支援：[`docs/ADDING_A_HOST.md`](https://github.com/garrytan/gstack/blob/main/docs/ADDING_A_HOST.md)
- Bun：<https://bun.sh/>
