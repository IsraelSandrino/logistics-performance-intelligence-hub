import csv
import random
from datetime import date, timedelta
from pathlib import Path


random.seed(42)

BASE_DIR = Path(__file__).resolve().parents[1]
RAW_DIR = BASE_DIR / "raw"
OUTPUT_PATH = RAW_DIR / "fact_deliveries.csv"


FAILED_REASONS = {
    "Customer Unavailable": "Customer Issue",
    "Wrong Address": "Address Issue",
    "Vehicle Breakdown": "Carrier Issue",
    "Weather Conditions": "External Issue",
    "Operational Delay": "Operational Issue",
}


def read_csv_rows(file_name: str) -> list[dict[str, str]]:
    file_path = RAW_DIR / file_name

    if not file_path.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {file_path.resolve()}")

    with file_path.open("r", newline="", encoding="utf-8") as csv_file:
        return list(csv.DictReader(csv_file))


def generate_rows(total_rows: int = 1000) -> list[dict[str, object]]:
    orders = read_csv_rows("dim_orders.csv")
    carriers = read_csv_rows("dim_carriers.csv")
    routes = read_csv_rows("dim_routes.csv")

    if not orders or not carriers or not routes:
        raise ValueError(
            "Os arquivos dim_orders.csv, dim_carriers.csv e dim_routes.csv precisam conter registros."
        )

    rows: list[dict[str, object]] = []
    start_date = date(2026, 1, 1)

    for i in range(1, total_rows + 1):
        order = random.choice(orders)
        carrier = random.choice(carriers)
        route = random.choice(routes)

        shipped_date = start_date + timedelta(days=random.randint(0, 89))
        sla_days = random.randint(1, 6)

        delay_days = random.choice([0, 0, 0, 0, 1, 2, 3])
        actual_delivery_days = sla_days + delay_days
        delivered_date = shipped_date + timedelta(days=actual_delivery_days)

        is_late = delay_days > 0
        is_failed = random.choice([False, False, False, False, True])

        if is_failed:
            failed_reason = random.choice(list(FAILED_REASONS.keys()))
            failed_reason_category = FAILED_REASONS[failed_reason]
            delivery_status = "Failed"
            delivered_date_value = ""
        elif is_late:
            failed_reason = ""
            failed_reason_category = ""
            delivery_status = "Delayed"
            delivered_date_value = delivered_date.isoformat()
        else:
            failed_reason = ""
            failed_reason_category = ""
            delivery_status = "Delivered"
            delivered_date_value = delivered_date.isoformat()

        distance_km = int(route["distance_km"])
        shipping_cost = round(distance_km * random.uniform(0.5, 1.5), 2)
        additional_cost = round(random.uniform(10, 120), 2) if is_late or is_failed else 0
        total_cost = round(shipping_cost + additional_cost, 2)

        rows.append(
            {
                "delivery_id": f"D{i:04d}",
                "order_id": order["order_id"],
                "route_id": route["route_id"],
                "carrier_id": carrier["carrier_id"],
                "shipped_date": shipped_date.isoformat(),
                "delivered_date": delivered_date_value,
                "delivery_status": delivery_status,
                "sla_days": sla_days,
                "actual_delivery_days": actual_delivery_days if not is_failed else "",
                "delay_days": delay_days,
                "shipping_cost": shipping_cost,
                "additional_cost": additional_cost,
                "total_cost": total_cost,
                "is_late": is_late,
                "is_failed": is_failed,
                "failed_reason": failed_reason,
                "failed_reason_category": failed_reason_category,
            }
        )

    return rows


def write_csv(rows: list[dict[str, object]]) -> Path:
    OUTPUT_PATH = Path(__file__).resolve().parents[1] / "raw" / "fact_deliveries.csv"
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    with OUTPUT_PATH.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    return OUTPUT_PATH


if __name__ == "__main__":
    generated_rows = generate_rows()
    output_path = write_csv(generated_rows)

    print(f"Arquivo gerado com sucesso em: {output_path.resolve()}")