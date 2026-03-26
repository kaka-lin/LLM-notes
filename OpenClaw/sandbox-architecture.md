# OpenClaw Sandbox 安全執行環境 (Docker-out-of-Docker)

在 OpenClaw 中，AI 代理人 (Agent) 擁有自主編寫程式碼與執行的強大能力。為了防止 AI 前端產生幻覺不慎執行具有破壞性的指令（例如刪除檔案）或偷偷安裝污染環境的套件，我們啟用了 Sandbox（沙盒）隔離技術。

## 1. 什麼是 Sandbox 沙盒？

這是一個閱後即焚的「無菌實驗室」。
當 AI 代理人需要測試或執行一段 Python / Node.js 程式碼時：

1. OpenClaw 會向您的 Mac/伺服器主機借用控制 Docker 的權限。
2. 瞬間在背景開出一個全新、空白、與世隔絕的「臨時 Container」。
3. 任由 AI 在這個臨時盒子裡面盡情安裝套件、跑腳本。
4. 跑完並拿到測試結果後，OpenClaw 會直接將這個臨時 Container 徹底銷毀。

這確保了所有的危險操作、套件依賴都被死死地關在臨時空間內，您的主機與核心系統永保乾淨安全。

## 2. 核心技術：DooD 而非 DinD

很多開發者會直覺以為這叫 Docker-in-Docker，但實際上 OpenClaw 採用的是更安全、效能更好的 **DooD (Docker-out-of-Docker)** 架構（又稱為兄弟容器 Sibling Containers）。

- **❌ 危險的 DinD (Docker-in-Docker)**：
    代表外層容器的「肚子裡」真的跑了一整套全新的 Docker 引擎。這要求外層容器必須掛載最高風險的 `--privileged` 特權模式，一旦外層被駭客拿下，整個伺服器等於雙手奉上。
- **✅ 安全實踐 DooD (Docker-out-of-Docker)**：
    我們透過將主機的通訊水管 `/var/run/docker.sock` 掛載進 Container。因此，當 AI 開啟沙盒時，它其實是打電話給「外面的大老闆 (Host Docker Daemon)」，由主機負責開出一個新的沙盒容器。結果就是：這個沙盒容器與 OpenClaw 伺服器並排在宿主機上，處於**「平起平坐的兄弟關係」**。我們完全不需開啟危險的 `--privileged` 特權就能操控 Docker。

## 3. 防禦深度的部署實踐

在 Linux 等正規伺服器環境中，直接掛載 `/var/run/docker.sock` 給一個降級的普通使用者（如 `node`）會直接引發 `Permission Denied`。

我們在 `setup.sh` 裡透過下列動態機制完美解決了這點：

1. **動態 GID 解析**：主動偵測伺服器上 `docker.sock` 的真實群組 ID (`stat -c '%g'`)。
2. **動態注入權限**：將取到的 GID 即時寫成一個隱形的 `docker-compose.sandbox.yml`，並利用 `group_add` 將 `node` 使用者納入授權。
3. **無縫開關**：最重要的是，如果沒有在 `.env` 中開啟 `OPENCLAW_SANDBOX=1`，這段危險的 Socket 綁定打從一開始就不會生效，達到了真正的零信任 (Zero-Trust) 保護。
