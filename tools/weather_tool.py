"""即時天氣查詢 Tool。

API: https://wttr.in/{city}?format=j1
需求：解析 temp_C 與 weatherDesc。
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen
import json


TOOL: Dict[str, Any] = {
    "name": "get_realtime_weather",
    "description": "查詢目的地即時天氣，回傳溫度(temp_C)與天氣描述(weatherDesc)",
    "parameters": {
        "type": "object",
        "properties": {
            "city": {
                "type": "string",
                "description": "城市名稱，例如 Tokyo、Taipei",
            }
        },
        "required": ["city"],
    },
}


@dataclass
class WeatherResult:
    city: str
    temp_C: str
    weatherDesc: str

    def to_dict(self) -> Dict[str, str]:
        return {
            "city": self.city,
            "temp_C": self.temp_C,
            "weatherDesc": self.weatherDesc,
        }


def _build_url(city: str) -> str:
    return f"https://wttr.in/{quote(city)}?format=j1"


def get_realtime_weather(city: str) -> Dict[str, str]:
    """查詢即時天氣並解析 temp_C、weatherDesc。"""
    city = (city or "").strip()
    if not city:
        raise ValueError("city 不能為空")

    url = _build_url(city)
    req = Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0",
            "Accept": "application/json",
        },
    )

    try:
        with urlopen(req, timeout=12) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except (HTTPError, URLError, TimeoutError) as exc:
        raise RuntimeError(f"天氣 API 請求失敗: {exc}") from exc
    except json.JSONDecodeError as exc:
        raise RuntimeError("天氣 API 回傳格式錯誤（非 JSON）") from exc

    current = payload.get("current_condition")
    if not isinstance(current, list) or not current:
        raise RuntimeError("天氣 API 回傳缺少 current_condition")

    first = current[0]
    if not isinstance(first, dict):
        raise RuntimeError("天氣 API 回傳資料格式不正確")

    temp_c = str(first.get("temp_C", "")).strip()
    weather_desc_list = first.get("weatherDesc")

    weather_desc = ""
    if isinstance(weather_desc_list, list) and weather_desc_list:
        first_desc = weather_desc_list[0]
        if isinstance(first_desc, dict):
            weather_desc = str(first_desc.get("value", "")).strip()

    if not temp_c or not weather_desc:
        raise RuntimeError("天氣 API 回傳缺少 temp_C 或 weatherDesc")

    return WeatherResult(city=city, temp_C=temp_c, weatherDesc=weather_desc).to_dict()


def run(params: Dict[str, Any]) -> Dict[str, str]:
    """給 Agent 呼叫的統一入口。"""
    return get_realtime_weather(city=str(params.get("city", "")))


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="查詢目的地即時天氣")
    parser.add_argument("city", help="城市名稱，例如 Tokyo")
    args = parser.parse_args()

    result = get_realtime_weather(args.city)
    print(json.dumps(result, ensure_ascii=False, indent=2))
