# Dicionário de Dados — Logistics Performance Intelligence Hub

## 1. Objetivo
Documentar o modelo de dados do projeto com foco em análise logística, custos e SLA.

Modelo: **estrela**
Granularidade: **1 linha = 1 entrega**

---

## 2. Tabela fato

### fact_deliveries

| Campo | Tipo | Descrição |
|---|---|---|
| delivery_id | bigint | ID único da entrega (PK) |
| date_id | int | FK para dim_date |
| customer_id | int | FK para dim_customer |
| origin_id | int | FK para dim_origin |
| destination_id | int | FK para dim_destination |
| carrier_id | int | FK para dim_carrier |
| driver_id | int | FK para dim_driver |
| vehicle_id | int | FK para dim_vehicle |
| order_id | varchar | ID do pedido |
| delivery_status | varchar | Status da entrega |
| promised_delivery_date | date | Data prometida |
| actual_delivery_date | date | Data real |
| delivery_distance_km | numeric | Distância |
| freight_cost | numeric | Custo frete |
| fuel_cost | numeric | Custo combustível |
| maintenance_cost | numeric | Custo manutenção |
| total_delivery_cost | numeric | Custo total |
| sla_days | int | SLA em dias |
| delay_days | int | Dias de atraso |
| is_delayed | boolean | Flag atraso |

---

## 3. Dimensões

### dim_date
| Campo | Tipo |
|---|---|
| date_id (PK) | int |
| date | date |
| month | int |
| year | int |
| quarter | int |
| week_of_year | int |

---

### dim_customer
| Campo | Tipo |
|---|---|
| customer_id (PK) | int |
| customer_name | varchar |
| customer_type | varchar |
| city | varchar |
| state | varchar |
| region | varchar |

---

### dim_origin
| Campo | Tipo |
|---|---|
| origin_id (PK) | int |
| origin_name | varchar |
| city | varchar |
| state | varchar |
| region | varchar |

---

### dim_destination
| Campo | Tipo |
|---|---|
| destination_id (PK) | int |
| destination_city | varchar |
| destination_state | varchar |
| destination_region | varchar |

---

### dim_carrier
| Campo | Tipo |
|---|---|
| carrier_id (PK) | int |
| carrier_name | varchar |
| carrier_type | varchar |

---

### dim_driver
| Campo | Tipo |
|---|---|
| driver_id (PK) | int |
| driver_name | varchar |
| driver_type | varchar |

---

### dim_vehicle
| Campo | Tipo |
|---|---|
| vehicle_id (PK) | int |
| vehicle_type | varchar |
| vehicle_brand | varchar |
| vehicle_model | varchar |
| capacity_kg | numeric |

---

## 4. Relacionamentos

Todos: **1:N (dimensão → fato)**

---

## 5. KPIs suportados

- Entregas totais  
- Entregas no prazo  
- Taxa de atraso  
- Custo total logístico  
- Custo por entrega  
- Custo por km  
- Performance por transportadora  
- Performance por região  

---

## 6. Regras

- Fato = métricas  
- Dimensão = atributos  
- Filtro sempre dimensão → fato  