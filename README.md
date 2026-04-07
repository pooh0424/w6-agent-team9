# AI agent 開發分組實作

> 課程：AI agent 開發 — Tool 與 Skill
> 主題： 旅遊前哨站 /  偵探事務所 /  生活顧問

---

## Agent 功能總覽

> 說明這個 Agent 能做什麼，使用者可以輸入哪些指令

| 使用者輸入   | Agent 行為                             | 負責組員 |
| ------------ | -------------------------------------- |------|
| 天氣         | 呼叫 weather_tool，查詢即時天氣        | 呂紹銘  |
| 景點         | 呼叫 search_tool，搜尋熱門景點         | 曹世杰  |
| 建議         | 呼叫 advice_tool，取得隨機建議         | 林楷祐  |
| 出發（城市） | 執行 trip_briefing Skill，產出行前簡報 | 呂紹銘 |
| 雨天備案（城市） | 執行 rainy_day_backup Skill，雨天時改推室內景點與室內活動 | 呂紹銘 |

---

## 組員與分工

| 姓名   | 負責功能     | 檔案                      | 使用的 API                                                                                               |
|------| ------------ |-------------------------|-------------------------------------------------------------------------------------------------------|
| 呂紹銘  | 即時天氣查詢（temp_C、weatherDesc） | `tools/weather_tool.py` | https://wttr.in/{city}?format=j1                                                                      |
| 曹世杰  | 熱門景點搜尋 | `tools/search_tool.py`  | DDGS                                                                                                  |
| 林楷祐  | 隨機建議/冷知識 | `tools/advice_tool.py`  | 隨機活動建議 https://bored-api.appbrewery.com/random 隨機冷知識 https://uselessfacts.jsph.pl/api/v2/facts/random |
| 呂紹銘 | Skill 整合（行前簡報） | `skills/trip_briefing_skill.py` | 整合 weather/search/advice 三個 Tool                                                                  |
| 呂紹銘 | Skill 整合（雨天備案） | `skills/rainy_day_backup_skill.py` | 先查天氣，若下雨則切換室內景點與室內活動建議                                                          |
| 呂紹銘 | Agent 主程式 | `main.py`               | 透過 CLI 輸入城市並輸出行前簡報                                                                        |

---

## 專案架構

範例：

```
├── tools/
│   ├── weather_tool.py
│   ├── search_tool.py   
│   └── advice_tool.py  
├── skills/
│   └── trip_briefing_skill.py  
│   └── rainy_day_backup_skill.py
├── main.py        
├── requirements.txt
└── README.md
```

---

## 使用方式

範例：

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python tools/weather_tool.py Tokyo
python tools/search_tool.py Tokyo
python tools/advice_tool.py activity
python tools/advice_tool.py fact
python main.py Tokyo
python main.py Tokyo --mode rainy
```

---

## 執行結果

> 貼上程式執行的實際範例輸出

```
PS C:\Users\USER\Desktop\code\w6-agent-team9> .venv\Scripts\python.exe tools/weather_tool.py Tokyo
{
    "city": "Tokyo",
    "temp_C": "18",
    "weatherDesc": "Partly cloudy"
}
```

```
PS C:\Users\USER\Desktop\code\w6-agent-team9> .venv\Scripts\python.exe tools/search_tool.py Tokyo
{
    "query": "Tokyo 熱門景點推薦",
    "results": [
        {
            "title": "【2026東京景點攻略】50個東京自由行市區景點與郊區玩法一次看! - Mimi韓の旅遊指南",
            "url": "https://mimigo.tw/tokyo-trips/",
            "snippet": "東京 (Tokyo) 是台灣人最愛的日本旅遊城市，有豐富的景點等著大家。在這篇「東京景點攻略」除了彙整東京景點地圖收錄超過50個東京熱門旅遊景點，再特別精選不可錯過的30個東京好玩景點＋10個東京郊區景點。"
        },
        {
            "title": "【2026東京景點】TOP50東京必去/新景點推薦,東京自由行一日遊必讀!",
            "url": "https://gowithmarkhazyl.com/must-visit-places-in-tokyo/",
            "snippet": "東京車站一番街 共有四個區塊分別是「TokyoGift Palette」、「東京拉麵街」、「東京零食天堂」、「東京Character Street」..."
        }
    ]
}
```

```
linkaiyu@linkaiyoudeMacBook-Pro-3 w6-agent-team9 % python3 tools/advice_tool.py activity

{
  "kind": "activity",
  "activity": "Volunteer at your local food bank",
  "type": "charity"
}
```

```
linkaiyu@linkaiyoudeMacBook-Pro-3 w6-agent-team9 % python3 tools/advice_tool.py fact

{
"kind": "fact",
"fact": "The first McDonald's restaurant in Canada was in Richmond, British Columbia."
}
```

```
PS C:\Users\USER\Desktop\code\w6-agent-team9> .venv\Scripts\python.exe main.py Tokyo
=== Tokyo 行前簡報 ===

[天氣]  18°C，Partly cloudy

[景點]  東京景點必遊、必打卡懶人包｜東京景點Top10熱門景點推薦、東京自由行：完整 行程、季節、景點、交通 - 神燈假期、【2026東京景點推薦】22個超好玩東京必去景點！ 來東京自由行這樣玩 ...

[今日活動]  Meditate for five minutes（類型：relaxation）

[冷知識]  Shakespeare invented the word `assassination` and `bump`.
```

```
PS C:\Users\USER\Desktop\code\w6-agent-team9> .venv\Scripts\python.exe main.py Tokyo --mode rainy
=== Tokyo 雨天備案簡報 ===

[天氣]  18°C，Partly cloudy

[判斷]  未偵測到下雨，提供一般備案

[景點]  【2026東京景點攻略】50個東京自由行市區景點與郊區玩法一次看! - Mimi韓の旅遊指南、【2026東京景點】TOP50東京必去/新景點推薦,東京自由行一日遊必讀!、東京必去景點｜Trip.com 東京

[今日活動]  Organize your dresser（類型：busywork）
```

---

## 各功能說明

### 即時天氣查詢（負責：呂紹銘）

- **Tool 名稱**：`get_realtime_weather`
- **使用 API**：`https://wttr.in/{city}?format=j1`
- **輸入**：城市名稱（例如：`Tokyo`、`Taipei`）
- **輸出範例**：

```json
{
  "city": "Tokyo",
  "temp_C": "18",
  "weatherDesc": "Partly cloudy"
}
```

```python
TOOL = {
    "name": "get_realtime_weather",
    "description": "查詢目的地即時天氣，回傳溫度(temp_C)與天氣描述(weatherDesc)",
    "parameters": {
        "type": "object",
        "properties": {
            "city": {
                "type": "string",
                "description": "城市名稱，例如 Tokyo、Taipei"
            }
        },
        "required": ["city"]
    }
}
```

### 景點推薦（負責：曹世杰）

- **Tool 名稱**：`get_site_search`
- **使用 API**：`DDGS`
- **輸入**：`Tokyo 熱門景點推薦`
- **輸出範例**：

```json
{
    "query": "Tokyo 熱門景點推薦",
    "results": [
        {
        "title":
    "【2026東京景點攻略】50個東京自由行市區景點與郊區玩法一次看! -
    Mimi韓の旅遊指南",
        "url": "https://mimigo.tw/tokyo-trips/",
        "snippet": "東京 (Tokyo)
    是台灣人最愛的日本旅遊城市，有豐富的景點等著大家。
    在這篇「東京景點攻略」除了彙整東京景點地圖收錄超過50個東京熱門旅遊景點
    ，再特別精選不可錯過的30個東京好玩景點＋10個東京郊區景點。"
        },
        {
        "title":
    "【2026東京景點】TOP50東京必去/新景點推薦,東京自由行一日遊必讀!",
        "url":
    "https://gowithmarkhazyl.com/must-visit-places-in-tokyo/",
        "snippet": "東京車站一番街 共有四個區塊分別是「TokyoGift
    Palette」、「東京拉麵街」、「東京零食天堂」、「東京Character
    Street」，零食天堂可以買到日本三大品牌固力果、超人氣薯條三兄弟Calbee、
    森永旗下的各種零食，甚至Calbee還有東京車站限定的現炸的薯條、薯塊。"
        },
        {
        "title": "【2026東京旅遊完全攻略】最新名勝‧人氣景點‧排隊美食‧購
    物名產‧交通規劃‧行程安排｜Lazy Japan 懶遊日本",
        "url": "https://lazyjapan.com/regions/tokyo/spots/main/",
        "snippet": "究竟東京人氣最高的五大景點有哪些呢？
    懶懶哥將在下方一一介紹。 NO.1 東京晴空塔（TokyoSkytree） 高達 634
    公尺的新東京鐵塔──東京晴空塔（TokyoSkytree）2012
    年完工啟用後，不但成為世界第一高塔，也躍升為東京最熱門的觀光景點。"
        },
        {
        "title": "【2026
    東京景點推薦】精選35個東京必去景點地圖、熱門好玩的東京觀光景點 |
    BringYou",
        "url": "https://www.bring-you.info/zh-tw/tokyo-attractions",
        "snippet": "【2026
    東京景點推薦】精選35個東京必去景點地圖、熱門好玩的東京觀光景點
    淺草雷門、東京迪士尼樂園、東京鐵塔、晴空塔、台場、豐洲市場、銀座、明治
    神宮、新宿、阿美橫町、上野恩賜公園，都是來東京必去的景點!
    飄兒就在這裡精選必去東京好玩景點。"
        },
        {
        "title": "【2026東京景點地圖】Top20必去景點攻略：地鐵沿線分區標
    記，新手自由行必看 |
    小布少爺旅遊誌｜看地圖玩日本：獨家景點地圖與深度自由行攻略",
        "url": "https://boo2k.com/tokyo/",
        "snippet": "東京景點推薦看這篇!小布整理東京自由行必去景點TOP30，
    包含淺草寺、東京晴空塔、SHIBUYA SKY、銀座、新宿、台場與東京迪士尼，搭
    配東京景點地圖、順路玩法與五天行程，新手也能輕鬆規劃。"
        }
    ]
}
```

```python
TOOL = {
    "name": "get_site_search",
    "description": "查詢目的地相關之景點資訊",
    "parameters": {
        "type": "object",
        "properties": {
            "city": {
                "type": "string",
                "description": "城市名稱，例如 Tokyo、Taipei"
            }
        },
        "required": ["city"]
    }
}
```

### 隨機建議/冷知識（負責：林楷祐）

- **Tool 名稱**：get_random_activity_advice
- **使用 API**：https://bored-api.appbrewery.com/random
- **輸入**：無
- **輸出範例**：
```json
{
  "kind": "activity",
  "activity": "Clean out your garage",
  "type": "busywork"
}
```

```python
TOOL: Dict[str, Any] = {
    "name": "get_random_advice",
    "description": "取得一則今日活動建議或隨機冷知識",
    "parameters": {
        "type": "object",
        "properties": {
            "kind": {
                "type": "string",
                "enum": ["activity", "fact"],
                "description": "advice 類型：activity 為今日活動建議，fact 為隨機冷知識",
            }
        },
        "required": ["kind"],
    },
}
```

### 隨機冷知識（負責：林楷祐）

- **Tool 名稱**：get_random_fact
- **使用 API**：https://uselessfacts.jsph.pl/api/v2/facts/random
- **輸入**：無
- **輸出範例**：
```json
{
  "kind": "fact",
  "fact": "The longest one-syllable word in the English language is \"screeched.\""
}
```

```python
TOOL: Dict[str, Any] = {
    "name": "get_random_advice",
    "description": "取得一則今日活動建議或隨機冷知識",
    "parameters": {
        "type": "object",
        "properties": {
            "kind": {
                "type": "string",
                "enum": ["activity", "fact"],
                "description": "advice 類型：activity 為今日活動建議，fact 為隨機冷知識",
            }
        },
        "required": ["kind"],
    },
}
```

### Skill：`trip_briefing_skill`（負責：呂紹銘）

- **組合了哪些 Tool**：
    - `tools/weather_tool.py`（`run({"city": city})`）
    - `tools/search_tool.py`（`run({"city": city})`）
    - `tools/advice_tool.py`（`run({"kind": "activity"})`）
    - `tools/advice_tool.py`（`run({"kind": "fact"})`）
- **執行順序**：

```
Step 1: 呼叫 weather_tool.run → 取得即時天氣（temp_C、weatherDesc）
Step 2: 呼叫 search_tool.run → 取得當地熱門景點搜尋結果
Step 3: 呼叫 advice_tool.run(kind=activity) → 取得今日活動建議
Step 4: 呼叫 advice_tool.run(kind=fact) → 取得旅遊冷知識
Step 5: 組合輸出 → 產生「=== 城市 行前簡報 ===」
```

### Skill：`rainy_day_backup_skill`（負責：呂紹銘）

- **功能目標**：先看天氣，如果下雨就自動改推薦室內景點與室內活動建議。
- **組合了哪些 Tool**：
    - `tools/weather_tool.py`（`run({"city": city})`）
    - `tools/search_tool.py`（`run({"city": city + " 雨天 室內景點"})`）
    - `tools/search_tool.py`（`run({"city": city + " 雨天 室內活動 建議"})`）
    - `tools/advice_tool.py`（天氣非雨天時，`run({"kind": "activity"})`）
- **執行順序**：

```
Step 1: 呼叫 weather_tool.run → 取得即時天氣
Step 2: 判斷 weatherDesc 是否包含 rain/shower/drizzle/storm/雨
Step 3: 若下雨，呼叫 search_tool.run(室內景點 + 室內活動關鍵字)
Step 4: 若未下雨，維持一般景點與今日活動建議
Step 5: 組合輸出 → 產生「=== 城市 雨天備案簡報 ===」
```

- **使用範例**：

```bash
python main.py Tokyo --mode rainy
```

---

## 心得

### 遇到最難的問題

這次最難的地方是「多個 Tool 串接後的穩定性」。
例如景點搜尋在部分環境會遇到套件相依問題，若沒有處理好，整份行前簡報就會中斷。
我們的做法是在 Skill 層加上安全呼叫與錯誤訊息回傳：即使某一個 Tool 失敗，其他區塊（天氣、活動、冷知識）仍可正常輸出，讓使用者至少拿到可用的行前資訊。

### Tool 和 Skill 的差別

Tool 是「單一能力」，例如查天氣、找景點、拿建議；
Skill 是「流程編排」，會依照任務目標決定呼叫哪些 Tool、呼叫順序與最後輸出格式。
這次的 `trip_briefing_skill` 就是把多個 Tool 的結果整合成一份完整「行前簡報」，這也是 Agent 真正提供價值的地方。

### 如果再加一個功能

我們會想加「旅遊預算估算 Tool」。
使用者輸入旅遊天數與城市後，回傳住宿、交通、餐食的區間估算，並搭配目前簡報的天氣與活動建議，做成更完整的出發前決策資訊。
