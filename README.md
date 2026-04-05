（請記得將該檔名改命名為 `README.md`）

# AI agent 開發分組實作

> 課程：AI agent 開發 — Tool 與 Skill
> 主題： 旅遊前哨站 /  偵探事務所 /  生活顧問

---

## Agent 功能總覽

> 說明這個 Agent 能做什麼，使用者可以輸入哪些指令

| 使用者輸入   | Agent 行為                             | 負責組員 |
| ------------ | -------------------------------------- | -------- |
| 天氣         | 呼叫 weather_tool，查詢即時天氣        | 呂紹銘 |
| 景點         | 呼叫 search_tool，搜尋熱門景點         | 曹世杰 |
| 建議         | 呼叫 advice_tool，取得隨機建議         | （待填） |
| 出發         | 執行 trip_briefing Skill，產出行前簡報 | （待填） |

---

## 組員與分工

| 姓名 | 負責功能     | 檔案        | 使用的 API |
| ---- | ------------ | ----------- | ---------- |
| 呂紹銘 | 即時天氣查詢（temp_C、weatherDesc） | `tools/weather_tool.py`  | https://wttr.in/{city}?format=j1 |
| 曹世杰 | 熱門景點搜尋 | `tools/search_tool.py`  | DDGS |
| （待填） | 隨機建議/冷知識 | `tools/`  | （待填） |
| （待填） | Skill 整合   | `skills/` | —         |
| （待填） | Agent 主程式 | `main.py` | —         |

---

## 專案架構

範例：

```
├── tools/
│   ├── weather_tool.py
│   ├── search_tool.py   
│   └── xxx_tool.py  
├── skills/
│   └── xxx_skill.py  
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

### [功能名稱]（負責：待填）

- **Tool 名稱**：
- **使用 API**：
- **輸入**：
- **輸出範例**：

### Skill：[Skill 名稱]（負責：待填）

- **組合了哪些 Tool**：
- **執行順序**：

```
Step 1: 呼叫 ___ → 取得 ___
Step 2: 呼叫 ___ → 取得 ___
Step 3: 組合輸出 → 產生 ___
```

---

## 心得

### 遇到最難的問題

> 寫下這次實作遇到最困難的事，以及怎麼解決的

### Tool 和 Skill 的差別

> 用自己的話說說，做完後你怎麼理解兩者的不同

### 如果再加一個功能

> 如果可以多加一個 Tool，你會加什麼？為什麼？
