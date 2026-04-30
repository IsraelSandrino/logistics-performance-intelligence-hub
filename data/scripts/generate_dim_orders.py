import csv
import random
from datetime import date, timedelta
from pathlib import Path

random.seed(42)

# Configuração de caminhos
BASE_DIR = Path(__file__).resolve().parents[1]
RAW_DIR = BASE_DIR / "raw"
OUTPUT_PATH = RAW_DIR / "dim_orders.csv"

# Constantes para geração de dados
CUSTOMER_PREFIX = "CUS"
PAYMENT_TYPES = ["Credit Card", "Debit Card", "Pix", "Bank Slip"]
MARKETPLACE_CHANNELS = ["App", "Website", "Marketplace"]

# Categorias com faixas de peso (em kg) para maior realismo nos custos de frete
PRODUCT_CATEGORIES = {
    "Eletrônicos": (0.5, 5.0),
    "Moda": (0.2, 1.5),
    "Casa": (2.0, 30.0),
    "Beleza": (0.1, 1.0),
    "Esporte": (0.5, 10.0),
    "Mercado": (1.0, 15.0),
}

def read_csv_rows(file_name: str) -> list[dict[str, str]]:
    file_path = RAW_DIR / file_name
    if not file_path.exists():
        return []
    with file_path.open("r", newline="", encoding="utf-8") as csv_file:
        return list(csv.DictReader(csv_file))

def generate_rows(total_rows: int = 1000) -> list[dict[str, object]]:
    # Lê as rotas para obter as cidades e suas coordenadas
    routes = read_csv_rows("dim_routes.csv")
    
    if not routes:
        print("Aviso: dim_routes não encontrada. Coordenadas serão simuladas.")
        destinations_map = {
            "São Paulo": {"state": "SP", "lat": -23.5505, "long": -46.6333},
            "Rio de Janeiro": {"state": "RJ", "lat": -22.9068, "long": -43.1729}
        }
    else:
        # Cria um mapeamento: Cidade -> {estado, latitude, longitude}
        # Isso evita fazer buscas repetitivas dentro do loop
        destinations_map = {}
        for r in routes:
            city = r["destination_city"]
            if city not in destinations_map:
                destinations_map[city] = {
                    "state": r["destination_state"],
                    "lat": r["latitude_destino"],
                    "long": r["longitude_destino"]
                }

    available_cities = list(destinations_map.keys())
    rows: list[dict[str, object]] = []
    start_date = date(2026, 1, 1)

    for i in range(1, total_rows + 1):
        category = random.choice(list(PRODUCT_CATEGORIES.keys()))
        weight_range = PRODUCT_CATEGORIES[category]
        
        order_date = start_date + timedelta(days=random.randint(0, 89))
        promised_days = random.randint(4, 12)
        promised_delivery_date = order_date + timedelta(days=promised_days)

        # Seleciona uma cidade e recupera seus dados geográficos do mapa
        dest_city = random.choice(available_cities)
        geo_info = destinations_map[dest_city]

        rows.append(
            {
                "order_id": f"O{i:04d}",
                "customer_id": f"{CUSTOMER_PREFIX}{random.randint(1, 350):04d}",
                "order_date": order_date.isoformat(),
                "promised_delivery_date": promised_delivery_date.isoformat(),
                "payment_type": random.choice(PAYMENT_TYPES),
                "order_value": round(random.uniform(49.90, 2500.00), 2),
                "product_category": category,
                "product_weight_kg": round(random.uniform(*weight_range), 2),
                "destination_city": dest_city,
                "destination_state": geo_info["state"],
                "latitude_destino": geo_info["lat"],
                "longitude_destino": geo_info["long"],
                "marketplace_channel": random.choice(MARKETPLACE_CHANNELS),
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
    try:
        generated_rows = generate_rows(1000)
        output_path = write_csv(generated_rows)
        print(f"Sucesso! dim_orders.csv gerado com coordenadas em: {output_path}")
        print(f"Exemplo de linha: {generated_rows[0]}")
    except Exception as e:
        print(f"Erro ao gerar o arquivo: {e}")