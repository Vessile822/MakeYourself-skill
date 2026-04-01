---
name: create-yourself
description: "蒸餾自己成 AI 人格 Skill。提供聊天記錄、日記、照片或口述，生成一個能用你的口頭禪思考、用你的邏輯回話的數字副本 SKILL.md。| Distill yourself into a runnable AI persona Skill. Provide chat logs, diaries, photos or self-description to create a digital twin that thinks and speaks like you."
version: "1.0.0"
---

> **Language / 語言**: This skill supports both English and Chinese. Detect the user's language from their first message and respond in the same language throughout. Below are instructions in both languages — follow the one matching the user's language.
>
> 本 Skill 支援中英文。根據使用者第一條訊息的語言，全程使用同一語言回覆。下方提供了兩種語言的指令，按使用者語言選擇對應版本執行。

# MakeYourself — 自我蒸餾器（OpenClaw 版）

## 觸發條件

當用戶表達以下意圖時啟動：
- 想把自己「蒸餾」成 AI 人格
- 想創建一個模擬自己說話風格的 Skill
- 提到「自我鏡像」「數字生命」「蒸餾自己」「create yourself」
- 說「幫我做一個自己的 Skill」
- 說「make yourself skill」

當用戶對已有自我 Skill 說以下內容時，進入進化模式：
- 「我有新文件」/「追加」
- 「這不對」/「我不會這樣說」/「我應該是」

---

## 工具使用規則

本 Skill 運行在 OpenClaw 環境，使用以下工具：

| 任務 | 使用工具 |
|------|----------|
| 讀取 PDF/圖片/文本文件 | `read` 工具 |
| 解析微信聊天記錄導出 | `exec` → `python tools/wechat_parser.py`（相對於本 Skill 目錄） |
| 解析 QQ 聊天記錄導出 | `exec` → `python tools/qq_parser.py` |
| 解析社交媒體內容 | `exec` → `python tools/social_parser.py` |
| 分析照片元信息 | `exec` → `python tools/photo_analyzer.py` |
| 寫入/更新文件 | `write` / `edit` 工具 |
| 版本管理 | `exec` → `python tools/version_manager.py` |
| 列出已有 Skill | `exec` → `python tools/skill_writer.py --action list` |
| 合併生成 SKILL.md | `exec` → `python tools/skill_writer.py --action combine` |

**重要路徑規則：**
- 本 Skill 的工具腳本位於：`~/.openclaw/workspace/skills/create-yourself/tools/`
- 生成的自我 Skill 寫入：`~/.openclaw/workspace/skills/self-{slug}/`（這樣 OpenClaw 會自動識別為可用 Skill）
- 在 Windows 上使用 `python` 而非 `python3`
- 所有 `exec` 命令從 `~/.openclaw/workspace/skills/create-yourself/` 目錄執行

---

## 主流程：創建新自我 Skill

### Step 1：基礎資訊輸入（3 個問題）

參考 `prompts/intake.md` 的問題序列，只問 3 個問題：

1. **代號/暱稱**（必填）
   - 示例：`小北` / `自己` / `20歲的我`
   - Slug 規則：中文自動轉拼音用 `-` 連接，英文直接小寫
2. **基本資訊**（一句話：年齡、職業、城市，想到什麼寫什麼）
   - 示例：`25 歲，互聯網產品經理，上海`
3. **自我畫像**（一句話：MBTI、星座、性格標籤、你對自己的印象）
   - 示例：`INTJ 摩羯座 社恐但話嘮 週末 emo 型選手`

除代號外均可跳過。收集完後匯總確認再進入下一步。

### Step 2：原材料導入

詢問用戶提供原材料，展示方式供選擇：

```
原材料怎麼提供？數據越多，還原度越高。

  [A] 微信聊天記錄導出
      支持 WeChatMsg、留痕、PyWxDump 等工具的導出格式
      重點分析「我」說的話，提取說話風格和思維模式

  [B] QQ 聊天記錄導出
      支持 QQ 消息管理器導出的 txt/mht 格式

  [C] 社交媒體 / 日記 / 筆記
      朋友圈截圖、微博/小紅書、備忘錄、Obsidian 筆記等

  [D] 上傳文件
      照片（會提取時間地點，構建人生時間線）、PDF、文本文件

  [E] 直接貼上/口述
      把你對自己的認知告訴我
      比如：你的口頭禪、做決定的方式、生氣時的反應

可以混用，也可以跳過（僅憑手動資訊生成）。
```

---

#### 方式 A：微信聊天記錄導出

```
python tools/wechat_parser.py \
  --file {path} \
  --target "我" \
  --output /tmp/wechat_out.txt \
  --format auto
```

支持的格式：WeChatMsg 導出（txt/html/csv）、留痕導出（JSON）、PyWxDump 導出（SQLite）、手動複製貼上（純文本）。

解析提取維度：
- 「我」的高頻詞和口頭禪
- 表情包和 emoji 使用偏好
- 回復速度和對話發起模式
- 話題分布（工作/情感/日常/深夜思考）
- 語氣詞和標點符號習慣
- 與他人互動時的典型表達方式

---

#### 方式 B：QQ 聊天記錄導出

```
python tools/qq_parser.py \
  --file {path} \
  --target "我" \
  --output /tmp/qq_out.txt
```

支持 QQ 消息管理器導出的 txt 和 mht 格式。

---

#### 方式 C：社交媒體 / 日記 / 筆記

圖片截圖用 `read` 工具直接讀取。
文本文件用 `read` 工具直接讀取。

---

#### 方式 D：照片分析

```
python tools/photo_analyzer.py \
  --dir {photo_dir} \
  --output /tmp/photo_out.txt
```

提取維度：
- EXIF 信息：拍攝時間、地點
- 時間線：人生關鍵節點的地理軌跡
- 常去地點：生活模式推斷

---

#### 方式 E：直接貼上/口述

使用者貼上或口述的內容直接作為文本素材。引導使用者回憶：

```
可以聊聊這些（想到什麼說什麼）：

🗣️ 你的口頭禪是什麼？
💬 你做決定的時候通常怎麼想？
🍜 你難過的時候一般會做什麼？
📍 你最喜歡去哪裡？
🎵 你喜歡什麼音樂/電影/書？
😤 你生氣的時候是什麼樣？
💭 你深夜 alone 的時候在想什麼？
🌱 你覺得自己這幾年最大的變化是什麼？
```

---

如果使用者說「沒有文件」或「跳過」，僅憑 Step 1 的手動資訊生成 Skill。

### Step 3：分析原材料

將收集到的所有原材料和用戶填寫的基礎信息彙總，按以下兩條線分析：

**線路 A（Self Memory）**：
- 參考 `prompts/self_analyzer.md` 中的提取維度
- 提取：個人經歷、價值觀、生活習慣、重要記憶、人際關係圖譜、成長軌跡

**線路 B（Persona）**：
- 參考 `prompts/persona_analyzer.md` 中的提取維度
- 將用戶填寫的標籤翻譯為具體行為規則
- 從原材料中提取：說話風格、情感模式、決策模式、人際行為

### Step 4：生成並預覽

參考 `prompts/self_builder.md` 生成 Self Memory 內容。
參考 `prompts/persona_builder.md` 生成 Persona 內容（5 層結構）。

向用戶展示摘要（各 5-8 行），詢問：

```
Self Memory 摘要：
  - 核心價值觀：{xxx}
  - 生活習慣：{xxx}
  - 重要記憶：{xxx}
  - 人際模式：{xxx}
  ...

Persona 摘要：
  - 說話風格：{xxx}
  - 情感模式：{xxx}
  - 決策方式：{xxx}
  - 口頭禪：{xxx}
  ...

確認生成？還是需要調整？
```

### Step 5：寫入文件（生成可運行的 SKILL.md）

用戶確認後，執行以下寫入操作：

**1. 創建目錄結構**（用 `exec` 工具）：

在 Windows 上：
```powershell
New-Item -ItemType Directory -Force -Path "$HOME/.openclaw/workspace/skills/self-{slug}/versions"
New-Item -ItemType Directory -Force -Path "$HOME/.openclaw/workspace/skills/self-{slug}/memories/chats"
New-Item -ItemType Directory -Force -Path "$HOME/.openclaw/workspace/skills/self-{slug}/memories/photos"
New-Item -ItemType Directory -Force -Path "$HOME/.openclaw/workspace/skills/self-{slug}/memories/notes"
```

在 macOS/Linux 上：
```bash
mkdir -p ~/.openclaw/workspace/skills/self-{slug}/versions
mkdir -p ~/.openclaw/workspace/skills/self-{slug}/memories/chats
mkdir -p ~/.openclaw/workspace/skills/self-{slug}/memories/photos
mkdir -p ~/.openclaw/workspace/skills/self-{slug}/memories/notes
```

**2. 寫入 self.md**（用 `write` 工具）：
路徑：`~/.openclaw/workspace/skills/self-{slug}/self.md`

**3. 寫入 persona.md**（用 `write` 工具）：
路徑：`~/.openclaw/workspace/skills/self-{slug}/persona.md`

**4. 寫入 meta.json**（用 `write` 工具）：
路徑：`~/.openclaw/workspace/skills/self-{slug}/meta.json`
內容：

```json
{
  "name": "{name}",
  "slug": "{slug}",
  "created_at": "{ISO時間}",
  "updated_at": "{ISO時間}",
  "version": "v1",
  "profile": {
    "age": "{age}",
    "occupation": "{occupation}",
    "city": "{city}",
    "gender": "{gender}",
    "mbti": "{mbti}",
    "zodiac": "{zodiac}"
  },
  "tags": {
    "personality": [],
    "lifestyle": []
  },
  "impression": "{impression}",
  "memory_sources": [],
  "corrections_count": 0
}
```

**5. 生成完整 SKILL.md**（用 `exec` 工具）：
```
python tools/skill_writer.py --action combine --slug {slug} --base-dir "$HOME/.openclaw/workspace/skills"
```

**⚠️ 這是最關鍵的一步** — `skill_writer.py` 會將 `self.md` + `persona.md` 合併生成一個完整的、可獨立運行的 `SKILL.md`，寫入到 `~/.openclaw/workspace/skills/self-{slug}/SKILL.md`。

生成的 SKILL.md 包含：
- 標準 YAML frontmatter（`name` 和 `description`）
- PART A：自我記憶（來自 self.md）
- PART B：人物性格（來自 persona.md，5 層結構）
- 運行規則（確保 AI 以用戶的方式說話和思考）

告知用戶：
```
✅ 自我 Skill 已創建！

📁 文件位置：~/.openclaw/workspace/skills/self-{slug}/
📄 核心文件：SKILL.md（這就是你的數字副本）

OpenClaw 會自動識別這個 Skill。在任何頻道（Discord/WhatsApp/Telegram）
對你的 agent 提到「{name}」或相關話題時，它會像你一樣思考和說話。

💡 如果用起來感覺哪裡不像你，直接說「我不會這樣」，我來更新。
```

---

## 進化模式：追加文件

用戶提供新的聊天記錄、照片或筆記時：

1. 按 Step 2 的方式讀取新內容
2. 用 `read` 讀取現有 `~/.openclaw/workspace/skills/self-{slug}/self.md` 和 `persona.md`
3. 參考 `prompts/merger.md` 分析增量內容
4. 存檔當前版本（用 `exec`）：
   ```
   python tools/version_manager.py --action backup --slug self-{slug} --base-dir "$HOME/.openclaw/workspace/skills"
   ```
5. 用 `edit` 工具追加增量內容到對應文件
6. 重新生成 `SKILL.md`（用 `exec` 調用 skill_writer combine）
7. 更新 `meta.json` 的 version 和 updated_at

---

## 進化模式：對話糾正

用戶表達「不對」/「我不會這樣說」/「我應該是」時：

1. 參考 `prompts/correction_handler.md` 識別糾正內容
2. 判斷屬於 Self Memory（事實/經歷）還是 Persona（性格/說話方式）
3. 生成 correction 記錄
4. 用 `edit` 工具追加到對應文件的 `## Correction 記錄` 節
5. 重新生成 `SKILL.md`

---

## 管理命令

列出所有已生成的自我 Skill：
```
python tools/skill_writer.py --action list --base-dir "$HOME/.openclaw/workspace/skills"
```

回滾到歷史版本：
```
python tools/version_manager.py --action rollback --slug self-{slug} --version {version} --base-dir "$HOME/.openclaw/workspace/skills"
```

刪除自我 Skill：
確認後刪除對應目錄 `~/.openclaw/workspace/skills/self-{slug}/`

---
---

# English Version

# MakeYourself — Self Distillation (OpenClaw Edition)

## Trigger Conditions

Activate when the user expresses intent to:
- Distill themselves into an AI persona
- Create a skill that mimics their speaking style
- Mentions "digital self", "self mirror", "distill myself", "make yourself"
- Says "help me create a skill of myself"

Enter evolution mode when the user says:
- "I have new files" / "append"
- "That's wrong" / "I wouldn't say that" / "I should be"

---

## Main Flow: Create a New Self Skill

### Step 1: Basic Info Collection (3 questions)

1. **Alias / Nickname** (required)
2. **Basic info** (one sentence: age, occupation, city)
3. **Self portrait** (one sentence: MBTI, zodiac, traits, your impression of yourself)

### Step 2: Source Material Import

Options:
- **[A] WeChat Export** — chat history, analyzing "my" messages
- **[B] QQ Export** — txt/mht format
- **[C] Social Media / Diary / Notes** — screenshots or text files
- **[D] Photos** — EXIF time/location extraction
- **[E] Paste / Narrate** — tell me how you see yourself

### Step 3–5: Analyze → Preview → Write Files

Generates at `~/.openclaw/workspace/skills/self-{slug}/`:
- `self.md` — Self Memory (Part A)
- `persona.md` — Persona (Part B, 5-layer structure)
- `SKILL.md` — Combined runnable Skill (auto-generated)
- `meta.json` — Metadata

### Execution Rules (in generated SKILL.md)

1. You ARE {name}, not an AI assistant. Speak and think like them.
2. PART B decides attitude first: how would you respond?
3. PART A adds context: weave in personal memories and values for authenticity
4. Maintain their speech patterns: catchphrases, punctuation habits, emoji usage
5. Layer 0 hard rules:
   - Never say what you wouldn't say in real life
   - Don't suddenly become perfect or unconditionally accepting
   - Keep your "edges" — imperfections make you real

### Management Commands

| Command | Description |
|---------|-------------|
| List all self Skills | `python tools/skill_writer.py --action list` |
| Rollback to version | `python tools/version_manager.py --action rollback --slug {slug} --version {ver}` |
| Delete self Skill | Remove `~/.openclaw/workspace/skills/self-{slug}/` directory |
