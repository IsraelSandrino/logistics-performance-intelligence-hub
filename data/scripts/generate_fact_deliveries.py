import csv
import random
from datetime import date, timedelta
from pathlib import Path

random.seed(42)

# Configuração de caminhos
BASE_DIR = Path(__file__).resolve().parents[1]
RAW_DIR = BASE_DIR / "raw"
OUTPUT_PATH = RAW_DIR / "fact_deliveries.csv"

# Mapeamentos de Status
ORDER_STATUS_MAP = {
    "Delivered": ["Delivered", "Paid"],
    "Delayed":   ["Shipped", "Paid"],
    "Failed":    ["Canceled", "Created"],
}

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
        raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")
    with file_path.open("r", newline="", encoding="utf-8") as csv_file:
        return list(csv.DictReader(csv_file))

def generate_rows(total_rows: int = 1000) -> list[dict[str, object]]:
    orders = read_csv_rows("dim_orders.csv")
    carriers = read_csv_rows("dim_carriers.csv")
    routes = read_csv_rows("dim_routes.csv")
    
    rows: list[dict[str, object]] = []

    # Criamos um índice de rotas por cidade de destino para acelerar a busca
    routes_by_city = {}
    for r in routes:
        city = r["destination_city"]
        if city not in routes_by_city:
            routes_by_city[city] = []
        routes_by_city[city].append(r)

    for i in range(1, total_rows + 1):
        # 1. Seleciona um pedido e sua respectiva rota baseada no destino
        order = random.choice(orders)
        dest_city = order["destination_city"]
        
        # Se houver rota para a cidade, usa ela. Se não, pega uma aleatória (fallback)
        possible_routes = routes_by_city.get(dest_city, routes)
        route = random.choice(possible_routes)
        
        # 2. Seleciona uma transportadora que cubra a região da rota
        route_region = route["region"]
        possible_carriers = [
            c for c in carriers 
            if c["coverage_region"] == "Nacional" or route_region in c["coverage_region"]
        ]
        carrier = random.choice(possible_carriers)

        # 3. Lógica de SLA e Datas
        # SLA = Dias médios da transportadora + penalidade por tipo de rota
        base_carrier_days = int(carrier["avg_delivery_days"])
        route_penalty = 2 if route["route_type"] == "Longa Distância" else (1 if route["route_type"] == "Interestadual" else 0)
        sla_days = base_carrier_days + route_penalty

        order_date = date.fromisoformat(order["order_date"])
        ship_lag = random.randint(1, 3) # Tempo de separação no HUB
        shipped_date = order_date + timedelta(days=ship_lag)
        
        # Probabilidade de atraso (maior em rotas de longa distância)
        if route["route_type"] == "Longa Distância":
            delay_days = random.choice([0, 0, 1, 2, 4, 7])
        else:
            delay_days = random.choice([0, 0, 0, 0, 1, 2])
        
        actual_delivery_days = sla_days + delay_days
        delivered_date = shipped_date + timedelta(days=actual_delivery_days)

        # 4. Status de Falha e Atraso
        is_late = delay_days > 0
        is_failed = random.random() < 0.05 # 5% de chance de falha total

        if is_failed:
            delivery_status = "Failed"
            delivered_date_val = ""
            actual_days_val = ""
            failed_reason = random.choice(list(FAILED_REASONS.keys()))
            failed_reason_category = FAILED_REASONS[failed_reason]
        else:
            delivery_status = "Delayed" if is_late else "Delivered"
            delivered_date_val = delivered_date.isoformat()
            actual_days_val = actual_delivery_days
            failed_reason = ""
            failed_reason_category = ""

        # 5. Cálculos Financeiros Reais
        dist_km = float(route["distance_km"])
        weight = float(order["product_weight_kg"])
        
        cost_km = float(carrier["cost_per_km"])
        cost_kg = float(carrier["cost_per_kg"])
        
        shipping_cost = round((dist_km * cost_km) + (weight * cost_kg), 2)
        additional_cost = round(shipping_cost * 0.2, 2) if is_late or is_failed else 0
        total_cost = round(shipping_cost + additional_cost, 2)

        rows.append({
            "delivery_id": f"D{i:04d}",
            "order_id": order["order_id"],
            "route_id": route["route_id"],
            "carrier_id": carrier["carrier_id"],
            "hub_id": route["origin_hub_id"],
            "shipped_date": shipped_date.isoformat(),
            "delivered_date": delivered_date_val,
            "delivery_status": delivery_status,
            "sla_days": sla_days,
            "actual_delivery_days": actual_days_val,
            "delay_days": delay_days,
            "shipping_cost": shipping_cost,
            "additional_cost": additional_cost,
            "total_cost": total_cost,
            "is_late": is_late,
            "is_failed": is_failed,
            "failed_reason": failed_reason,
            "failed_reason_category": failed_reason_category
        })

    return rows

def write_csv(rows: list[dict[str, object]]) -> Path:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_PATH.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    return OUTPUT_PATH

if __name__ == "__main__":
    try:
        data = generate_rows(1500) # Gerando 1500 entregas
        path = write_csv(data)
        print(f"Sucesso! fact_deliveries.csv gerado em: {path}")
    except Exception as e:
        print(f"Erro: {e}")