import json
import matplotlib.pyplot as plt
from datetime import datetime

DATA_FILE = "data/gold.json"

def main():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    dates = [datetime.fromisoformat(r["date"]) for r in data]
    prices = [r["gold"] for r in data]

    plt.figure(figsize=(10, 5))
    plt.plot(dates, prices, marker="o")

    plt.title("Курс золота (ЦБ РФ), руб./грамм")
    plt.xlabel("Дата")
    plt.ylabel("Рублей за 1 грамм")
    plt.grid(True)

    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
