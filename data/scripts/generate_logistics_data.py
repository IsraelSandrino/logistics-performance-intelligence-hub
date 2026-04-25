import csv
import random
from datetime import datetime, timedelta
from pathlib import Path


cities = ["Guarapuava", "Curitiba", "Cascavel", "Londrina", "Maringa", "Ponta Grossa"]
status = ["DELIVERED"] * 70 + ["IN_TRANSIT"] * 15 + ["DELAYED"] * 10 + ["CANCELLED"] * 5
payments = ["CREDIT_CARD", "PIX", "BOLETO"]


def build_rows(total_rows: int = 1000) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []

    for i in range(1, total_rows + 1):
        order_date = datetime.today() - timedelta(days=random.randint(0, 90))
        promised_date = order_date + timedelta(days=random.randint(2, 7))

        rows.append(
            {
                "order_id": f"ORD{i:04}",
                "customer_id": f"CUST{random.randint(1, 300):03}",
                "order_date": order_date.date().isoformat(),
                "promised_date": promised_date.date().isoformat(),
                "order_status": random.choice(status),
                "payment_type": random.choice(payments),
                "order_value": round(random.uniform(50, 1500), 2),
                "origin_city": random.choice(cities),
                "destination_city": random.choice(cities),
            }
        )

    return rows


def write_csv(rows: list[dict[str, object]]) -> Path:
    output_path = Path(__file__).resolve().parents[1] / "raw" / "dim_orders.csv"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    return output_path


if __name__ == "__main__":
    generated_rows = build_rows()
    file_path = write_csv(generated_rows)
    print(f"Arquivo gerado com sucesso em: {file_path}")
