"""雨天備案 Skill：先看天氣，若下雨則改推室內景點與室內活動建議。"""

from __future__ import annotations

from typing import Any, Dict, List

from tools import advice_tool, search_tool, weather_tool


def _safe_call(func, *args, **kwargs) -> Dict[str, Any]:
    try:
        return {"ok": True, "data": func(*args, **kwargs)}
    except Exception as exc:
        return {"ok": False, "error": str(exc)}


def _is_rainy(weather_desc: str) -> bool:
    text = (weather_desc or "").strip().lower()
    rainy_tokens = ["rain", "shower", "drizzle", "thunder", "storm", "雨"]
    return any(token in text for token in rainy_tokens)


def _pick_top_titles(search_result: Dict[str, Any], limit: int = 3) -> List[str]:
    results = search_result.get("results", [])
    if not isinstance(results, list):
        return []

    picked: List[str] = []
    for item in results:
        if not isinstance(item, dict):
            continue
        title = str(item.get("title", "")).strip()
        if title:
            picked.append(title)
        if len(picked) >= limit:
            break
    return picked


def build_rainy_day_backup(city: str) -> Dict[str, Any]:
    city = (city or "").strip()
    if not city:
        raise ValueError("city 不能為空")

    weather = _safe_call(weather_tool.run, {"city": city})

    weather_desc = ""
    if weather.get("ok"):
        weather_desc = str(weather.get("data", {}).get("weatherDesc", ""))
    is_rainy = _is_rainy(weather_desc)

    if is_rainy:
        spots = _safe_call(
            search_tool.run,
            {"city": f"{city} 雨天 室內景點"},
        )
        indoor_activity = _safe_call(
            search_tool.run,
            {"city": f"{city} 雨天 室內活動 建議"},
        )
    else:
        spots = _safe_call(
            search_tool.run,
            {"city": city},
        )
        indoor_activity = _safe_call(advice_tool.run, {"kind": "activity"})

    return {
        "city": city,
        "weather": weather,
        "is_rainy": is_rainy,
        "spots": spots,
        "indoor_activity": indoor_activity,
    }


def format_rainy_day_backup(briefing: Dict[str, Any]) -> str:
    city = str(briefing.get("city", "目的地"))
    lines: List[str] = [f"=== {city} 雨天備案簡報 ===", ""]

    weather = briefing.get("weather", {})
    if weather.get("ok"):
        data = weather.get("data", {})
        temp = data.get("temp_C", "?")
        desc = data.get("weatherDesc", "未知")
        lines.append(f"[天氣]  {temp}°C，{desc}")
    else:
        lines.append(f"[天氣]  取得失敗：{weather.get('error', '未知錯誤')}")
    lines.append("")

    is_rainy = bool(briefing.get("is_rainy", False))
    if is_rainy:
        lines.append("[判斷]  偵測到下雨，已切換為室內備案")
    else:
        lines.append("[判斷]  未偵測到下雨，提供一般備案")
    lines.append("")

    spots = briefing.get("spots", {})
    if spots.get("ok"):
        top_titles = _pick_top_titles(spots.get("data", {}), limit=3)
        if top_titles:
            if is_rainy:
                lines.append("[室內景點]  " + "、".join(top_titles))
            else:
                lines.append("[景點]  " + "、".join(top_titles))
        else:
            lines.append("[景點]  暫時找不到可用結果")
    else:
        lines.append(f"[景點]  取得失敗：{spots.get('error', '未知錯誤')}")
    lines.append("")

    indoor_activity = briefing.get("indoor_activity", {})
    if is_rainy:
        if indoor_activity.get("ok"):
            top_titles = _pick_top_titles(indoor_activity.get("data", {}), limit=3)
            if top_titles:
                lines.append("[室內活動建議]  " + "、".join(top_titles))
            else:
                lines.append("[室內活動建議]  可安排博物館、美術館、室內商場行程")
        else:
            lines.append(
                "[室內活動建議]  可安排博物館、美術館、室內商場行程"
            )
    else:
        if indoor_activity.get("ok"):
            data = indoor_activity.get("data", {})
            lines.append(
                f"[今日活動]  {data.get('activity', '無')}（類型：{data.get('type', '未知')}）"
            )
        else:
            lines.append(f"[今日活動]  取得失敗：{indoor_activity.get('error', '未知錯誤')}")

    return "\n".join(lines)
