import csv
import random
from datetime import date, timedelta
from pathlib import Path


random.seed(42)

BASE_DIR = Path(__file__).resolve().parents[1]
RAW_DIR = BASE_DIR / "raw"
OUTPUT_PATH = RAW_DIR / "fact_deliveries.csv"

region_factor = {
    "Sul": 1.0,
    "Sudeste": 0.95,
    "Nordeste": 1.25,
    "Norte": 1.4,
    "Centro-Oeste": 1.15,
}

carrier_factor = {
    "Correios PAC": 1.0,
    "Correios SEDEX": 0.9,
    "JadLog": 1.0,
    "Total Express": 0.95,
    "Loggi": 0.9,
    "Rappi Entregas": 1.1,
    "Azul Cargo": 1.15,
    "Brasspress": 1.0,
    "Sequoia LogÃ­stica": 1.05,
    "Mercado Envios": 0.95,
    "Amazon Logistics": 0.9,
    "Transportadora SulLog": 0.98,
    "Expresso Nordeste": 1.1,
    "LogÃ­stica Centro-Oeste": 1.05,
    "Flash Courier": 0.92,
}

delay_probability = {
    "Sul": 0.05,
    "Sudeste": 0.1,
    "Nordeste": 0.25,
    "Norte": 0.35,
    "Centro-Oeste": 0.18,
}

failed_reason_weights = [
    ("Cliente ausente", 0.28),
    ("Endereco incorreto", 0.18),
    ("Recusa no recebimento", 0.12),
    ("Area de risco", 0.10),
    ("Problema operacional", 0.14),
    ("Avaria no transporte", 0.08),
    ("Extravio", 0.05),
    ("Pedido cancelado", 0.05),
]


def read_csv_rows(file_name: str) -> list[dict[str, str]]:
    file_path = RAW_DIR / file_name

    with file_path.open("r", newline="", encoding="utf-8") as csv_file:
        return list(csv.DictReader(csv_file))


def generate_failure_outcome() -> tuple[str, str | None]:
    delivery_status = random.choices(["Delivered", "Failed"], weights=[0.92, 0.08], k=1)[0]

    if delivery_status == "Failed":
        reasons = [reason for reason, _ in failed_reason_weights]
        weights = [weight for _, weight in failed_reason_weights]
        failed_reason = random.choices(reasons, weights=weights, k=1)[0]
    else:
        failed_reason = None

    return delivery_status, failed_reason


def generate_delivery(route: dict[str, str], carrier: dict[str, str]) -> tuple[float, int, int, str, str, str | None]:
    distance = int(route["distance_km"])
    region = route["region"]
    carrier_name = carrier["carrier_name"]

    base_cost = distance * 0.75
    total_cost = base_cost * region_factor.get(region, 1.0) * carrier_factor.get(carrier_name, 1.0)

    sla_days = max(1, round(distance / 400))

    if random.random() < delay_probability.get(region, 0.1):
        delay_days = random.randint(1, 5)
    else:
        delay_days = 0

    delivery_status, failed_reason = generate_failure_outcome()

    if delivery_status == "Failed":
        status = "Failed"
    else:
        status = "Delayed" if delay_days > 0 else "Delivered"

    return round(total_cost, 2), sla_days, delay_days, status, delivery_status, failed_reason


def generate_rows(total_rows: int = 1000) -> list[dict[str, object]]:
    orders = read_csv_rows("dim_orders.csv")
    carriers = read_csv_rows("dim_carriers.csv")
    hubs = read_csv_rows("dim_hubs.csv")
    routes = read_csv_rows("dim_routes.csv")

    if not orders or not carriers or not hubs or not routes:
        raise ValueError("Os arquivos de dimensao precisam conter registros para gerar fact_deliveries.csv.")

    rows: list[dict[str, object]] = []
    start_date = date(2026, 1, 1)

    for i in range(1, total_rows + 1):
        order = random.choice(orders)
        carrier = random.choice(carriers)
        hub = random.choice(hubs)
        route = random.choice(routes)

        delivery_date = start_date + timedelta(days=random.randint(0, 89))
        freight_cost, sla_days, delay_days, status, delivery_status, failed_reason = generate_delivery(route, carrier)
        estimated_delivery_date = delivery_date + timedelta(days=sla_days)
        actual_delivery_date = estimated_delivery_date + timedelta(days=delay_days)

        delivery_time_hours = (actual_delivery_date - delivery_date).days * 24
        delay_hours = max(0, (actual_delivery_date - estimated_delivery_date).days * 24)
        distance_km = int(route["distance_km"])
        on_time_flag = 1 if delay_days == 0 and delivery_status == "Delivered" else 0

        rows.append(
            {
                "delivery_id": f"D{i:04d}",
                "order_id": order["order_id"],
                "carrier_id": carrier["carrier_id"],
                "route_id": route["route_id"],
                "hub_id": hub["hub_id"],
                "delivery_date": delivery_date.isoformat(),
                "estimated_delivery_date": estimated_delivery_date.isoformat(),
                "actual_delivery_date": actual_delivery_date.isoformat(),
                "status": status,
                "delivery_time_hours": round(delivery_time_hours, 2),
                "distance_km": distance_km,
                "freight_cost": freight_cost,
                "delay_hours": round(delay_hours, 2),
                "on_time_flag": on_time_flag,
                "delivery_status": delivery_status,
                "failed_reason": failed_reason,
            }
        )

    return rows


def write_csv(rows: list[dict[str, object]]) -> Path:
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
