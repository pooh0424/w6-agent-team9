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
| 景點         | 呼叫 search_tool，搜尋熱門景點         | （待填） |
| 建議         | 呼叫 advice_tool，取得隨機建議         | （待填） |
| 出發         | 執行 trip_briefing Skill，產出行前簡報 | （待填） |

---

## 組員與分工

| 姓名 | 負責功能     | 檔案        | 使用的 API |
| ---- | ------------ | ----------- | ---------- |
| 呂紹銘 | 即時天氣查詢（temp_C、weatherDesc） | `tools/weather_tool.py`  | https://wttr.in/{city}?format=j1 |
| （待填） | 熱門景點搜尋 | `tools/`  | （待填） |
| （待填） | 隨機建議/冷知識 | `tools/`  | （待填） |
| （待填） | Skill 整合   | `skills/` | —         |
| （待填） | Agent 主程式 | `main.py` | —         |

---

## 專案架構

範例：

```
├── tools/
│   ├── weather_tool.py
│   ├── xxx_tool.py   
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

### [功能名稱]（負責：待填）

- **Tool 名稱**：
- **使用 API**：
- **輸入**：
- **輸出範例**：

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
