# AI Coding Skills

收集為 AI coding agent 加上「框架」與「紀律」的開源 skill / workflow 套件，比較它們的切入角度與適用情境。

## 為什麼需要這類工具

讓 AI 自由生成程式碼會有兩個典型痛點：

- **AI slop**：拼湊式垃圾程式碼，看起來能跑但結構腐爛、缺乏一致性。
- **Context Rot**（脈絡腐化）：對話一長，AI 就忘記前面定下的設定、慣例、邊界。

這類工具的共同目標是：**強制 AI 按某種紀律工作**，而不是讓它「自由發揮」。但每個專案的切入角度不同 — 有的提供「角色觀點」，有的強制「開發流程」，有的乾脆把整套方法論做成 skill。

## 目前收錄

| 專案 | 切入角度 | 筆記 |
| --- | --- | --- |
| gstack | 提供「決策與角色觀點」（讓 AI 變成有指導意見的虛擬團隊） | [gstack/](./gstack/) |
| superpowers | 提供「嚴格的開發流程紀律」（強制 AI 走 TDD、原子任務） | [superpowers/](./superpowers/) |

## 相關主題

- [SDD](../SDD/) — Spec-Driven Development。同樣是「給 AI 紀律」的精神，但層次不同：SDD 是**方法論**（怎麼寫規格、怎麼編號、怎麼追溯），不依賴特定工具；這個目錄收的是**具體 skill 套件**。兩者可以互相搭配，例如用 SDD 寫好 spec、再用 superpowers 的 TDD 流程實作。

## 想找實際可用的 skill？

這個目錄是**研究筆記** — 整理各家 skill 套件的設計理念與差異，方便比較取捨。

如果想找實際可裝、可直接給 agent 用的 artifact，請看 [`agent-library/`](https://github.com/kaka-lin/agent-library)：

- [`skills/`](https://github.com/kaka-lin/agent-library/tree/main/skills/) — 例如 `systematic-debugging`, `office-hours`, `git-commit-helper`, `analyzing-fastapi-projects`
- [`workflows/`](https://github.com/kaka-lin/agent-library/tree/main/workflows/) — 多步驟 SOP 流程
- [`rules/`](https://github.com/kaka-lin/agent-library/tree/main/rules/) — 編碼風格與全域規則

## 參考

- [Agent Skills 開放規範](https://agentskills.io/)
- [Agent Skills Marketplace](https://skillsmp.com/)
- [Claude Marketplaces](https://claudemarketplaces.com/)
