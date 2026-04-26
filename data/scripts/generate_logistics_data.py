import csv
import random
from datetime import date, timedelta
from pathlib import Path


random.seed(42)

BASE_DIR = Path(__file__).resolve().parents[1]
RAW_DIR = BASE_DIR / "data" / "raw"
OUTPUT_PATH = RAW_DIR / "dim_orders.csv"


CUSTOMER_PREFIX = "CUS"

ORDER_STATUSES = [
    "Created",
    "Paid",
    "Shipped",
    "Delivered",
    "Canceled",
]

PAYMENT_TYPES = [
    "Credit Card",
    "Debit Card",
    "Pix",
    "Bank Slip",
]

PRODUCT_CATEGORIES = [
    "Eletrônicos",
    "Moda",
    "Casa",
    "Beleza",
    "Esporte",
    "Mercado",
]

MARKETPLACE_CHANNELS = [
    "App",
    "Website",
    "Marketplace",
]

CITIES = [
    "São Paulo",
    "Rio de Janeiro",
    "Curitiba",
    "Porto Alegre",
    "Campinas",
    "Belo Horizonte",
    "Goiânia",
    "Recife",
    "Salvador",
    "Manaus",
]


def generate_rows(total_rows: int = 1000) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    start_date = date(2026, 1, 1)

    for i in range(1, total_rows + 1):
        order_date = start_date + timedelta(days=random.randint(0, 89))
        promised_delivery_date = order_date + timedelta(days=random.randint(2, 8))

        origin_city = random.choice(CITIES)
        destination_city = random.choice([city for city in CITIES if city != origin_city])

        rows.append(
            {
                "order_id": f"O{i:04d}",
                "customer_id": f"{CUSTOMER_PREFIX}{random.randint(1, 350):04d}",
                "order_date": order_date.isoformat(),
                "promised_delivery_date": promised_delivery_date.isoformat(),
                "order_status": random.choice(ORDER_STATUSES),
                "payment_type": random.choice(PAYMENT_TYPES),
                "order_value": round(random.uniform(49.90, 2500.00), 2),
                "origin_city": origin_city,
                "destination_city": destination_city,
                "product_category": random.choice(PRODUCT_CATEGORIES),
                "marketplace_channel": random.choice(MARKETPLACE_CHANNELS),
            }
        )

    return rows


def write_csv(rows: list[dict[str, object]]) -> Path:
    OUTPUT_PATH = Path(__file__).resolve().parents[1] / "raw" / "dim_orders.csv"
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    with OUTPUT_PATH.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    return OUTPUT_PATH


if __name__ == "__main__":
    generated_rows = generate_rows()
    output_path = write_csv(generated_rows)
    print(f"Arquivo gerado com sucesso em: {output_path}")