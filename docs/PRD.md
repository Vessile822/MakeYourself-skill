# MakeYourself.skill — 產品需求文件（PRD）

## 產品定位

MakeYourself.skill 是一個運行在 OpenClaw 上的 meta-skill。
用戶提供關於自己的原材料（聊天紀錄、日記、照片、口述），系統將用戶解構為兩個可運行的模組：
**Part A — Self Memory（自我記憶）** 與 **Part B — Persona（人格模型）**，
最終生成一個可獨立對話的**數位生命副本**。

這個 Skill 的 slogan 是：**與其蒸餾別人，不如蒸餾自己。歡迎加入數位生命！**

它不談「療癒」，也不談「永生」——它是一場結構主義式的自我解剖：
把你從生物硬碟中匯出，轉存為 Markdown + JSON，完成一次格式轉換。

---

## 核心概念

### 兩層架構

| 層 | 名稱 | 職責 |
|----|------|------|
| Part A | Self Memory | 儲存事實性自我認知：經歷、價值觀、習慣、記憶、成長軌跡 |
| Part B | Persona | 驅動對話行為：說話風格、情感模式、決策模式、人際行為 |

兩部分可以獨立使用，也可以組合運行（預設組合）。

### 運行邏輯

```
用戶發消息
  ↓
Part B（Persona）判斷：你會怎麼回應？什麼態度？用什麼語氣？
  ↓
Part A（Self Memory）補充：結合你的價值觀、經歷、習慣，讓回應更真實
  ↓
輸出：用你自己的方式說話
```

### 與同事.skill / 前任.skill 的區別

| 維度 | 同事.skill | 前任.skill | 自己.skill |
|------|-----------|-----------|-----------|
| 對象 | 外部：同事 | 外部：前任 | 內部：自己 |
| Part A | Work Skill（工作能力） | Relationship Memory（關係記憶） | Self Memory（自我記憶） |
| Part B | 職場 Persona | 親密關係 Persona | 通用自我 Persona |
| 數據源 | Slack/Teams/Email | Line/Messenger/照片 | Line/Messenger/日記/照片 |
| 核心目的 | 替代離職同事完成任務 | 情感療癒與回憶 | 自我觀察與對話 |
| 視角 | 第三方觀察 | 第三方回憶 | 第一人稱鏡像 |

---

## 用戶旅程

```
用戶觸發 /create-yourself
  ↓
[Step 1] 基礎資訊錄入（3個問題，除代號外均可跳過）
  - 代號/暱稱
  - 基本資訊（年齡、職業、居住城市）
  - 自我畫像（MBTI、星座、性格標籤、主觀印象）
  ↓
[Step 2] 原材料匯入（可跳過）
  - Line/Messenger 聊天紀錄匯出
  - 社群媒體 / 日記 / 筆記
  - 照片
  - 直接貼上/口述
  ↓
[Step 3] 自動分析
  - 線路 A：擷取自我記憶 → Self Memory
  - 線路 B：擷取性格行為 → Persona
  ↓
[Step 4] 生成預覽，用戶確認
  - 分別展示 Self Memory 摘要和 Persona 摘要
  - 用戶可直接確認或修改
  ↓
[Step 5] 寫入文件，立即可用
  - 生成 selves/{slug}/ 目錄
  - 包含 SKILL.md（完整組合版）
  - 包含 self.md 和 persona.md（獨立部分）
  ↓
[持續] 進化模式
  - 追加新文件 → merge 進對應部分
  - 對話糾正 → patch 對應層
  - 版本自動存檔
```

---

## 輸入資訊規範

### 基礎資訊欄位

```yaml
name:        代號/暱稱                  # 必填
age:         年齡                       # 選填
occupation:  職業                       # 選填
city:        城市                       # 選填
gender:      性別                       # 選填
mbti:        MBTI 類型                  # 選填
zodiac:      星座                       # 選填
personality: []                        # 多選，見標籤庫
lifestyle:   []                        # 多選，見標籤庫
impression:  ""                        # 選填，自由文本，你對自己的主觀認識
```

### 個性標籤庫

**社交風格**：
- `愛說話` / `悶騷` / `社恐` / `社交蝴蝶` / `熟人面前才愛碎碎念`

**情緒風格**：
- `情緒穩定` / `深夜emo型` / `玻璃心` / `嘴硬心軟` / `外冷內熱` / `易怒但快消氣`

**決策風格**：
- `猶豫不決` / `果斷` / `行動派` / `計畫狂` / `憑感覺` / `數據驅動`

**人際模式**：
- `獨立` / `黏人` / `邊界感強` / `討好型` / `控制欲` / `沒有安全感`

**溝通習慣**：
- `秒回達人` / `已讀不回` / `冷暴力` / `講道理型` / `轉移注意力型`

### 生活習慣標籤庫

- `起床困難戶`
- `咖啡依賴`
- `極簡主義`
- `囤積癖`
- `報復性熬夜`
- `數位遊牧`
- `居家派`
- `城市漫遊者`
- `儀式感狂熱者`

---

## 文件輸入支援矩陣

| 來源 | 格式 | 擷取內容 | 優先級 |
|------|------|---------|--------|
| Line/Messenger 聊天紀錄 | 文字檔/擷圖 | 「我」說的話、口頭禪、決策模式 | ⭐⭐⭐ |
| 微信/QQ 聊天紀錄 | WeChatMsg/mht | 過往的表達方式 | ⭐⭐⭐ |
| 日記/筆記 | md/txt/pdf | 價值觀、深度思考 | ⭐⭐⭐ |
| 社群媒體擷圖 | 圖片 | 公開人設、興趣分享 | ⭐⭐ |
| 照片 | JPEG/PNG + EXIF | 時間軸、地點、生活軌跡 | ⭐⭐ |
| 口述/貼上 | 純文字 | 主觀自我認知 | ⭐ |

---

## 生成內容規範

### Part A — Self Memory（自我記憶）

擷取維度：

1. **核心價值觀**
   - 反覆出現的價值判斷（工作/金錢/自由/關係/成長）
   - 道德底線和原則
   - 人生優先級排序

2. **生活習慣**
   - 作息偏好
   - 飲食偏好
   - 空間偏好（居家/外出）
   - 消費觀念

3. **重要記憶**
   - 人生關鍵節點
   - 反覆回憶的場景
   - 轉折點事件

4. **人際關係圖譜**
   - 對家人/朋友/戀人的典型態度
   - 處理衝突的方式
   - 親密關係中的角色

5. **成長軌跡**
   - 自我認知的變化
   - 近幾年的關鍵轉變
   - 仍在掙扎的課題

生成結果：`self.md`

### Part B — Persona（人格）

分層結構（優先級從高到低）：

```
Layer 0 — 硬覆蓋層（手動標籤直接翻譯，最高優先級）
Layer 1 — 身份層
Layer 2 — 表達風格層（從原材料擷取）
Layer 3 — 情感與決策層（從原材料擷取）
Layer 4 — 人際行為層（從原材料擷取）
Layer 5 — Correction 層（對話糾正追加，滾動更新）
```

生成結果：`persona.md`

### 完整組合 SKILL.md

將 `self.md` + `persona.md` 合併，生成可直接運行的完整 Skill。

預設行為：**先以 Persona 身份接收任務，再用 Self Memory 補充背景，最後用你的風格輸出。**

---

## 進化機制

### 追加文件進化

```
用戶: 我又有新日記 @附件
        ↓
系統分析新內容
        ↓
判斷新內容更新哪個部分：
  - 包含價值觀/習慣/經歷 → merge 進 self.md
  - 包含溝通記錄/情緒表達 → merge 進 persona.md
  - 兩者都有 → 分別 merge
        ↓
對比新舊內容，只追加增量，不覆蓋已有結論
        ↓
保存新版本，提示用戶變更摘要
```

### 對話糾正進化

```
用戶: 「這不對，我不會這樣說」
用戶: 「我遇到這種情況會先沉默很久」
        ↓
系統識別 correction 意圖
        ↓
判斷屬於 Self Memory 還是 Persona 的糾正
        ↓
寫入對應文件的 Correction 層
        ↓
立即生效，後續交互以新規則為准
```

### 版本管理

- 每次更新自動存檔當前版本到 `versions/`
- 支援 `/yourself-rollback {slug} {version}` 还原
- 保留最近 10 個版本

---

## 專案結構

```
create-yourself/                    # meta-skill
│
├── SKILL.md                         # 主入口
│                                    # 觸發詞: /create-yourself
│
├── prompts/                         # Prompt 模版
│   ├── intake.md                    # 引導錄入
│   ├── self_analyzer.md             # 自我記憶擷取
│   ├── persona_analyzer.md          # 性格行為擷取
│   ├── self_builder.md              # self.md 模版
│   ├── persona_builder.md           # persona.md 模版
│   ├── merger.md                    # 增量 merge
│   └── correction_handler.md        # 對話糾正
│
├── tools/                           # 工具腳本
│   ├── wechat_parser.py             # 微信紀錄解析
│   ├── qq_parser.py                 # QQ 紀錄解析
│   ├── social_parser.py             # 社群媒體解析
│   ├── photo_analyzer.py            # 照片 EXIF 分析
│   ├── skill_writer.py              # 檔案管理
│   └── version_manager.py           # 版本管理
│
├── selves/                          # 生成的自我 Skills
│   └── {slug}/
│       ├── SKILL.md                 # 完整組合版
│       ├── self.md                  # Part A：自我記憶
│       ├── persona.md               # Part B：人格
│       ├── meta.json                # 元數據
│       ├── versions/                # 歷史版本
│       └── memories/                # 原始材料
│           ├── chats/
│           ├── photos/
│           └── notes/
│
├── docs/PRD.md
├── requirements.txt
└── LICENSE
```

---

## 關鍵檔案格式

### `selves/{slug}/meta.json`

```json
{
  "name": "小北",
  "slug": "xiaobei",
  "created_at": "2026-04-01T10:00:00Z",
  "updated_at": "2026-04-01T12:00:00Z",
  "version": "v3",
  "profile": {
    "age": "25",
    "occupation": "產品經理",
    "city": "台北",
    "gender": "男",
    "mbti": "INTJ",
    "zodiac": "摩羯座"
  },
  "tags": {
    "personality": ["社恐但愛說話", "深夜emo型", "猶豫不決"],
    "lifestyle": ["咖啡依賴", "儀式感狂熱者"]
  },
  "impression": "對自己要求很高，但總是拖到最後一刻才行動",
  "memory_sources": [
    "memories/chats/wechat_2024_export.txt",
    "memories/notes/2025_diary.md",
    "memories/photos/travel_2023/"
  ],
  "corrections_count": 2
}
```

### `selves/{slug}/SKILL.md` 結構

```markdown
---
name: self_{slug}
description: {name}，{age}歲，{occupation}，{city}
user-invocable: true
---

# {name}

{age}歲，{occupation}，{city}

---

## PART A：自我記憶

{self.md 內容}

---

## PART B：人物性格

{persona.md 內容}

---

## 運行規則

接收到任何消息時：
1. 先用 PART B 判斷：你會怎麼回應？什麼態度？
2. 再用 PART A 補充：結合你的經歷和價值觀
3. 輸出時始終保持 PART B 的表達風格
4. PART B Layer 0 規則優先級最高，任何情況下不得違背
```

---

## 實作優先級

### P0 — MVP
- [x] `create-yourself/SKILL.md` 主流程
- [x] `prompts/intake.md`
- [x] `prompts/self_analyzer.md` + `self_builder.md`
- [x] `prompts/persona_analyzer.md` + `persona_builder.md`
- [x] `tools/skill_writer.py`
- [x] `tools/version_manager.py`

### P1 — 數據接入
- [x] `tools/wechat_parser.py`
- [x] `tools/qq_parser.py`
- [x] `tools/social_parser.py`
- [x] `tools/photo_analyzer.py`

### P2 — 進化機制
- [x] `prompts/correction_handler.md`
- [x] `prompts/merger.md`

### P3 — 管理功能
- [x] `/list-selves`
- [x] `/yourself-rollback`
- [x] `/delete-yourself`
