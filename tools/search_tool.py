"""搜尋當地熱門景點或注意事項 Tool。

使用 DuckDuckGo Search API 搜尋旅遊相關資訊。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List
import json

from ddgs import DDGS


TOOL: Dict[str, Any] = {
    "name": "get_site_search",
    "description": "查詢目的地相關之景點資訊",
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
class SearchResult:
    title: str
    url: str
    snippet: str

    def to_dict(self) -> Dict[str, str]:
        return {
            "title": self.title,
            "url": self.url,
            "snippet": self.snippet,
        }


@dataclass
class SearchResults:
    query: str
    results: List[SearchResult] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "query": self.query,
            "results": [r.to_dict() for r in self.results],
        }


def get_site_search(city: str, max_results: int = 5) -> Dict[str, Any]:
    """根據城市名稱，使用 DuckDuckGo 搜尋當地熱門景點。"""
    city = (city or "").strip()
    if not city:
        raise ValueError("city 不能為空")

    query = f"{city} 熱門景點推薦"
    max_results = max(1, min(max_results, 10))

    try:
        with DDGS() as ddgs:
            raw_results = list(ddgs.text(
                query,
                region="tw-tzh",
                max_results=max_results,
            ))
    except Exception as exc:
        raise RuntimeError(f"DuckDuckGo 搜尋失敗: {exc}") from exc

    results = [
        SearchResult(
            title=item.get("title", ""),
            url=item.get("href", ""),
            snippet=item.get("body", ""),
        )
        for item in raw_results
    ]

    return SearchResults(query=query, results=results).to_dict()


def run(params: Dict[str, Any]) -> Dict[str, Any]:
    """給 Agent 呼叫的統一入口。"""
    return get_site_search(city=str(params.get("city", "")))


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="搜尋當地熱門景點或注意事項")
    parser.add_argument("city", help="城市名稱，例如 Tokyo")
    args = parser.parse_args()

    result = get_site_search(args.city)
    print(json.dumps(result, ensure_ascii=False, indent=2))
