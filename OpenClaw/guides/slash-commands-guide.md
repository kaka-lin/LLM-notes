# 斜線指令 (Slash Commands) 指南

OpenClaw 提供了一套豐富的指令系統來控制會話、調整模型設定以及呼叫外掛工具。這套系統分為兩種層次的觸發方式：

## 1. 指令類型分析

### 1.1 純文字指令 (Text Commands)

這是最通用的觸發方式。使用者在對話框中輸入以 `/` 或 `!` 開頭的特定文字即算觸發。
只要設定 `commands.text: true`（預設），系統便會在送給模型前將這些指令攔截。

**特性：**

- **無平台限制**：即使是在 WhatsApp、Signal 或 iMessage 等「不支援原生 Bot 指令」的平台上，純文字指令依然有效。
- **內聯暗示 (Inline hints)**：如果一則訊息包含文字與指令（例如：「/fast 請幫我分析這個」），指令會當作單次的 Hint 來執行，而不會將效果永久寫入當前會話 (Session)。
- **會話持久化**：如果訊息「只有指令」（例如純粹送出 `/think high`），這個效果將會持久化保存至當前會話。

### 1.2 原生指令 (Native Commands)

指在特定通訊軟體（例如 Discord 或 Telegram）中，透過打出 `/` 後自動彈出的平台內建 UI 互動選單。

**特性：**

- 依賴 `commands.native: "auto"` 與 `commands.nativeSkills: "auto"` 來控制是否向平台註冊指令。
- 只有支援原生指令機器人的平台才有效（Discord/Telegram 全面支援，Slack 則需要手動設置）。

## 2. 核心內建指令 (Core Built-in Commands)

這是一系列直接由 Gateway 負責解析並控制運行狀態的指令。

### 2.1 會話與模型控制

- `/new [model]`：以此身分開起一個全新的空白 Session。
- `/stop`：強制中止目前正在生產回覆的模型。
- `/model`：顯示或切換當前對話使用的模型與 Provider。
- `/compact`：整理並壓縮目前過度肥大的歷史上下文。

### 2.2 推理與性能調節

- `/think <off|minimal|low|medium|high|xhigh>`：設定思考層級。
- `/reasoning <on|off|stream>`：決定是否要能看到模型的推理輸出。
- `/fast <on|off>`：切換極速模式（禁用多餘的工具流程來換取反應速度）。

### 2.3 工具與權限

- `/skill <name>`：強制觸發某一個在工作區註冊的技能。
- `/bash <command>`：執行本機端 Shell 腳本（需同時開啟高權限工具與特定設定）。
- `/exec`：管理本機執行工具（Host execution）的詢問與安全模式。

## 3. 權限認證機制 (Authorization)

斜線指令擁有改變全域與系統層級的能力，因此受限於嚴格的授權政策：

1. **唯一最高權限表**：如果設定檔設定了 `commands.allowFrom`，這將成為系統認定「誰有權限下指令」的唯一依據（會覆寫通道本身的白名單與 Group 授權）。
2. **無權限處理**：若非白名單內之用戶傳送了包含 `/think` 等文字，系統會當作「普通對話字串」傳給模型，不會觸發功能。
3. **Owner 專用指令**：如 `/config`（讀寫系統設定）或 `/plugins`（安裝外掛），擁有獨立的 `commands.ownerAllowFrom` 防火牆。
