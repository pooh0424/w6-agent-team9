"""隨機建議與冷知識 Tool。

APIs:
- https://bored-api.appbrewery.com/random
- https://uselessfacts.jsph.pl/api/v2/facts/random
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
import json


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


@dataclass
class ActivityAdvice:
    kind: str
    activity: str
    type: str

    def to_dict(self) -> Dict[str, str]:
        return {
            "kind": self.kind,
            "activity": self.activity,
            "type": self.type,
        }


@dataclass
class RandomFact:
    kind: str
    fact: str

    def to_dict(self) -> Dict[str, str]:
        return {
            "kind": self.kind,
            "fact": self.fact,
        }


def _fetch_json(url: str) -> Dict[str, Any]:
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
        raise RuntimeError(f"API 請求失敗: {exc}") from exc
    except json.JSONDecodeError as exc:
        raise RuntimeError("API 回傳格式錯誤（非 JSON）") from exc

    if not isinstance(payload, dict):
        raise RuntimeError("API 回傳資料格式不正確")

    return payload


def get_random_activity_advice() -> Dict[str, str]:
    """取得一則今日活動建議。"""
    payload = _fetch_json("https://bored-api.appbrewery.com/random")

    activity = str(payload.get("activity", "")).strip()
    activity_type = str(payload.get("type", "")).strip()

    if not activity or not activity_type:
        raise RuntimeError("活動建議 API 回傳缺少 activity 或 type")

    return ActivityAdvice(
        kind="activity",
        activity=activity,
        type=activity_type,
    ).to_dict()


def get_random_fact() -> Dict[str, str]:
    """取得一則隨機冷知識。"""
    payload = _fetch_json("https://uselessfacts.jsph.pl/api/v2/facts/random")

    fact = str(payload.get("text", "")).strip()
    if not fact:
        raise RuntimeError("冷知識 API 回傳缺少 text")

    return RandomFact(kind="fact", fact=fact).to_dict()


def get_random_advice(kind: str) -> Dict[str, str]:
    """根據 kind 取得活動建議或冷知識。"""
    normalized_kind = (kind or "").strip().lower()
    if not normalized_kind:
        raise ValueError("kind 不能為空")
    if normalized_kind == "activity":
        return get_random_activity_advice()
    if normalized_kind == "fact":
        return get_random_fact()

    raise ValueError("kind 只能是 activity 或 fact")


def run(params: Dict[str, Any]) -> Dict[str, str]:
    """給 Agent 呼叫的統一入口。"""
    return get_random_advice(kind=str(params.get("kind", "")))


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="取得今日活動建議或隨機冷知識")
    parser.add_argument(
        "kind",
        choices=["activity", "fact"],
        help="activity 為今日活動建議，fact 為隨機冷知識",
    )
    args = parser.parse_args()

    result = get_random_advice(args.kind)
    print(json.dumps(result, ensure_ascii=False, indent=2))
