# MakeYourself Skill （OpenClaw 版）

> 與其蒸餾別人，不如蒸餾自己。歡迎加入數字生命！

提供你的聊天記錄、日記、照片，加上你對自己的描述，我們將你解構為一套可運行的結構：
- **Part A — Self Memory（自我記憶）**
- **Part B — Persona（人格模型）**

生成一個能用你口頭禪思考、用你邏輯回話的數字副本 `SKILL.md`。

Inspired by [colleague-skill](https://github.com/notdog1998/colleague-skill) and [yourself-skill](https://github.com/notdog1998/yourself-skill).

## 安裝

### OpenClaw

```bash
# 方式一：直接 clone 到 workspace skills 目錄
git clone https://github.com/Vessile822/MakeYourself-skill.git ~/.openclaw/workspace/skills/create-yourself

# 方式二：clone 到 managed skills 目錄（所有 agent 共享）
git clone https://github.com/Vessile822/MakeYourself-skill.git ~/.openclaw/skills/create-yourself
```

### 依賴（可選）

聊天記錄解析功能需要 Python 依賴：

```bash
# Windows
cd ~/.openclaw/workspace/skills/create-yourself
setup.bat

# macOS / Linux
pip install -r requirements.txt
```

## 使用

在 OpenClaw 的任何頻道（Discord / WhatsApp / Telegram / Slack 等）對你的 agent 說：

- 「幫我蒸餾自己」
- 「我想創建一個自己的 Skill」
- "Help me create a skill of myself"
- "I want to distill myself into a skill"

按提示輸入你的代號、基本信息、自我畫像，然後選擇資料來源。所有欄位均可跳過，僅憑描述也能生成。

完成後，agent 會在 `~/.openclaw/workspace/skills/self-{slug}/` 生成一個獨立的 `SKILL.md`。OpenClaw 會自動讀取這個新 Skill，你的數字副本就上線了。

## 管理命令

| 功能 | 說明 |
|------|------|
| 追加記憶 | 找到更多聊天記錄/日記/照片，對 agent 說「我有新文件」 |
| 對話糾正 | 覺得回答不像你？說「我不會這樣說」，立即修正 |
| 版本回滾 | 每次更新自動存檔，支持回滾到歷史版本 |

## 效果示例

輸入：25 歲產品經理，INTJ，摩羯座，社恐但話嘮，深夜emo型選手

**場景一：日常聊天**
```
用戶 ❯ 最近好累
自己.skill ❯ 正常，你每次都是快撐不住了才說累
               先睡吧，別熬夜了，雖然你估計也聽不進去
```

**場景二：幫你分析自己**
```
用戶 ❯ 我為什麼總是拖延
自己.skill ❯ 因為你只會在 deadline 前感受到真實的恐懼。
               其他時候的焦慮都是表演式的，騙自己「我在焦慮所以我在努力」。
               真想改的話，先把任務拆到能騙過大腦的程度。
```

## 項目結構

```
create-yourself/
├── SKILL.md                 # Skill 入口（OpenClaw 格式）
├── prompts/                 # Prompt 模板
│   ├── intake.md            # 對話式信息錄入
│   ├── self_analyzer.md     # 自我記憶/認知提取
│   ├── persona_analyzer.md  # 性格行為提取（含標籤翻譯表）
│   ├── self_builder.md      # self.md 生成模板
│   ├── persona_builder.md   # persona.md 五層結構模板
│   ├── merger.md            # 增量 merge 邏輯
│   └── correction_handler.md # 對話糾正處理
├── tools/                   # Python 工具
│   ├── wechat_parser.py     # 微信聊天記錄解析
│   ├── qq_parser.py         # QQ 聊天記錄解析
│   ├── social_parser.py     # 社交媒體內容解析
│   ├── photo_analyzer.py    # 照片元信息分析
│   ├── skill_writer.py      # Skill 文件管理
│   └── version_manager.py   # 版本存檔與回滾
├── selves/                  # 生成的自我 Skill 範例
│   └── example_me/          # 範例：小北
├── setup.bat                # Windows 一鍵安裝
├── requirements.txt         # Python 依賴
└── LICENSE                  # MIT License
```

## 注意事項

- 原材料質量決定還原度：聊天記錄 + 日記/筆記 > 僅口述
- 建議優先提供：
  1. 深夜對話/獨白 — 最能暴露真實性格
  2. 情緒波動的記錄 — 生氣、難過、興奮時的表達
  3. 做決定的聊天記錄 — 暴露決策模式
  4. 日常閒扯 — 提煉口頭禪和語氣詞
- 這是一個幫助你觀察自己的工具，不是逃避現實的出口
- 你一直在變化，這個 Skill 只代表你被蒸餾時的那個自己

## 致敬 & 引用

- [yourself-skill](https://github.com/notdog1998/yourself-skill) — 原始 Claude Code 版本
- [colleague-skill](https://github.com/notdog1998/colleague-skill) — 靈感來源
- [AgentSkills](https://agentskills.io) — 開放標準

## License

MIT
