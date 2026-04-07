"""行前簡報 Skill：整合多個 Tool 輸出旅遊前哨站簡報。"""

from __future__ import annotations

from typing import Any, Dict, List

from tools import advice_tool, search_tool, weather_tool


def _safe_call(func, *args, **kwargs) -> Dict[str, Any]:
    """包裝工具呼叫，避免單一 API 失敗中斷整份簡報。"""
    try:
        return {"ok": True, "data": func(*args, **kwargs)}
    except Exception as exc:
        return {"ok": False, "error": str(exc)}


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


def build_trip_briefing(city: str) -> Dict[str, Any]:
    """整合 4 項功能：天氣、景點、活動建議、冷知識。"""
    city = (city or "").strip()
    if not city:
        raise ValueError("city 不能為空")

    # 一律透過各 Tool 的 run(params) 入口呼叫，確保使用既有工具介面。
    weather = _safe_call(weather_tool.run, {"city": city})
    spots = _safe_call(search_tool.run, {"city": city})
    activity = _safe_call(advice_tool.run, {"kind": "activity"})
    fact = _safe_call(advice_tool.run, {"kind": "fact"})

    return {
        "city": city,
        "weather": weather,
        "spots": spots,
        "activity": activity,
        "fact": fact,
    }


def format_trip_briefing(briefing: Dict[str, Any]) -> str:
    """將整合資料格式化為可讀的行前簡報文字。"""
    city = str(briefing.get("city", "目的地"))
    lines: List[str] = [f"=== {city} 行前簡報 ===", ""]

    weather = briefing.get("weather", {})
    if weather.get("ok"):
        data = weather.get("data", {})
        temp = data.get("temp_C", "?")
        desc = data.get("weatherDesc", "未知")
        lines.append(f"[天氣]  {temp}°C，{desc}")
    else:
        lines.append(f"[天氣]  取得失敗：{weather.get('error', '未知錯誤')}")
    lines.append("")

    spots = briefing.get("spots", {})
    if spots.get("ok"):
        top_titles = _pick_top_titles(spots.get("data", {}), limit=3)
        if top_titles:
            lines.append("[景點]  " + "、".join(top_titles))
        else:
            lines.append("[景點]  暫時找不到可用結果")
    else:
        lines.append(f"[景點]  取得失敗：{spots.get('error', '未知錯誤')}")
    lines.append("")

    activity = briefing.get("activity", {})
    if activity.get("ok"):
        data = activity.get("data", {})
        lines.append(
            f"[今日活動]  {data.get('activity', '無')}（類型：{data.get('type', '未知')}）"
        )
    else:
        lines.append(f"[今日活動]  取得失敗：{activity.get('error', '未知錯誤')}")
    lines.append("")

    fact = briefing.get("fact", {})
    if fact.get("ok"):
        lines.append(f"[冷知識]  {fact.get('data', {}).get('fact', '無')}")
    else:
        lines.append(f"[冷知識]  取得失敗：{fact.get('error', '未知錯誤')}")

    return "\n".join(lines)