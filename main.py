"""旅遊前哨站 Agent 主程式。"""

from __future__ import annotations

import argparse

from skills.rainy_day_backup_skill import build_rainy_day_backup, format_rainy_day_backup
from skills.trip_briefing_skill import build_trip_briefing, format_trip_briefing


def run(city: str, mode: str = "trip") -> str:
    normalized_mode = (mode or "trip").strip().lower()
    if normalized_mode == "rainy":
        briefing = build_rainy_day_backup(city)
        return format_rainy_day_backup(briefing)

    briefing = build_trip_briefing(city)
    return format_trip_briefing(briefing)


def main() -> None:
    parser = argparse.ArgumentParser(description="旅遊前哨站：輸入城市，輸出行前簡報")
    parser.add_argument("city", nargs="?", help="城市名稱，例如 Tokyo、Taipei")
    parser.add_argument(
        "--mode",
        choices=["trip", "rainy"],
        default="trip",
        help="輸出模式：trip 為一般行前簡報，rainy 為雨天備案簡報",
    )
    args = parser.parse_args()

    city = args.city
    if not city:
        city = input("請輸入想去的城市：").strip()

    if not city:
        raise SystemExit("城市名稱不能為空")

    output = run(city, mode=args.mode)
    print(output)


if __name__ == "__main__":
    main()