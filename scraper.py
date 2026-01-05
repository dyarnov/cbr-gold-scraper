import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json
import os

URL = "https://www.cbr.ru/hd_base/metall/metall_base_new/"
OUTPUT_DIR = "data"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "gold.json")


def fetch_gold_prices():
    response = requests.get(URL, timeout=30)
    response.encoding = "utf-8"
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    table = soup.find("table")
    if not table:
        raise RuntimeError("Таблица с данными не найдена")

    records = []

    for row in table.find_all("tr")[1:]:
        cols = row.find_all("td")
        if len(cols) < 2:
            continue

        # дата
        date_str = cols[0].get_text(strip=True)
        date = datetime.strptime(date_str, "%d.%m.%Y").date()

        # золото (руб./грамм)
        gold_str = (
            cols[1]
            .get_text(strip=True)
            .replace(" ", "")
            .replace(",", ".")
        )

        try:
            gold_price = float(gold_str)
        except ValueError:
            continue

        records.append({
            "date": date.isoformat(),
            "gold": gold_price
        })

    return records


def save_to_json(records):
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # если файл существует — читаем и объединяем
    if os.path.exists(OUTPUT_FILE):
        with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
            old_records = json.load(f)
    else:
        old_records = []

    # объединение без дублей по дате
    merged = {r["date"]: r for r in old_records}
    for r in records:
        merged[r["date"]] = r

    result = list(sorted(merged.values(), key=lambda x: x["date"]))

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"Данные сохранены: {OUTPUT_FILE}")


def main():
    records = fetch_gold_prices()
    if not records:
        print("Данные не получены")
        return

    save_to_json(records)


if __name__ == "__main__":
    main()
