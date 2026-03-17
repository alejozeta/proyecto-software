# Predictiva — Plataforma Predictiva de Producción de Hidrocarburos

## Descripción

Predictiva es una plataforma para pronosticar la producción futura de hidrocarburos. Permite a equipos de planificación e ingeniería de reservorios consultar pronósticos por pozo, simular escenarios what-if y consumir resultados vía API REST.

El sistema busca reducir la incertidumbre en la planificación operativa y presupuestaria, reemplazando planillas dispersas y modelos manuales por una plataforma integrada con trazabilidad completa.

## Estado Actual

**Fase 1 — Demo del Servicio** (en desarrollo, entrega: 2026-04-28)

Entregables de esta fase:
- Pipeline CI/CD automatizado (GitHub Actions)
- Contenerización completa (Docker + Docker Compose)
- Mock de API REST con endpoints funcionales y datos estáticos
- Documentación OpenAPI/Swagger accesible en línea
- Dashboard de monitoreo (Prometheus + Grafana)

## Arquitectura

```
┌─────────────────────────────────┐
│     Capa API / UI (FastAPI)     │  ← Fase 1: mock de endpoints
└────────────────┬────────────────┘
                 │
┌────────────────▼────────────────┐
│   Módulo de Machine Learning    │  ← Fase 3: modelos predictivos
└────────────────┬────────────────┘
                 │
┌────────────────▼────────────────┐
│        Módulo de Datos          │  ← Fase 2: ingesta y almacenamiento
└─────────────────────────────────┘

══════════════════════════════════
  Data Platform (Gobernanza + Orquestación)   ← capa horizontal
══════════════════════════════════
```

Cada fase agrega una capa sin reestructurar las existentes. Ver [ADR-001](docs/adr/ADR-001-tech-stack-and-architecture.md) para la justificación completa.

## Stack Tecnológico

| Tecnología | Uso |
|---|---|
| Python 3.12 + FastAPI | API REST con documentación OpenAPI automática |
| Docker + Docker Compose | Contenerización de todos los servicios |
| GitHub Container Registry (ghcr.io) | Registro privado de imágenes Docker |
| GitHub Actions | Pipeline de CI/CD |
| Prometheus | Recolección de métricas |
| Grafana | Dashboards de monitoreo |
| pytest + httpx | Testing |
| Railway / Render | Despliegue en la nube |

## Prerrequisitos

- [Docker](https://docs.docker.com/get-docker/) (v20.10+)
- [Docker Compose](https://docs.docker.com/compose/install/) (v2+)
- Git

## Ejecución Local

### 1. Clonar el repositorio

```bash
git clone https://github.com/alejozeta/proyecto-software.git
cd proyecto-software
```

### 2. Levantar todos los servicios

```bash
docker compose up --build
```

### 3. Acceder a los servicios

| Servicio | URL | Credenciales |
|---|---|---|
| API (FastAPI) | http://localhost:8000 | — |
| Swagger / OpenAPI Docs | http://localhost:8000/docs | — |
| Prometheus | http://localhost:9090 | — |
| Grafana | http://localhost:3000 | usuario: `admin`, contraseña: `admin` |

### 4. Detener los servicios

```bash
docker compose down
```

## Uso de la API

### Autenticación

Todos los endpoints requieren el header `X-API-Key` con el valor `abcdef12345`. Sin este header o con un valor incorrecto, la API retorna HTTP 403.

### Endpoints

#### GET /api/v1/wells — Listar pozos activos

```bash
curl -H "X-API-Key: abcdef12345" \
  "http://localhost:8000/api/v1/wells?date_query=2023-10-01"
```

Respuesta:
```json
[
  { "id_well": "POZO-001" },
  { "id_well": "POZO-002" }
]
```

#### GET /api/v1/forecast — Obtener pronóstico por pozo

```bash
curl -H "X-API-Key: abcdef12345" \
  "http://localhost:8000/api/v1/forecast?id_well=POZO-001&date_start=2023-10-01&date_end=2023-10-05"
```

Respuesta:
```json
{
  "id_well": "POZO-001",
  "data": [
    { "date": "2023-10-01", "prod": 150.5 },
    { "date": "2023-10-02", "prod": 148.2 }
  ]
}
```

#### Ejemplo sin API Key (error 403)

```bash
curl "http://localhost:8000/api/v1/wells?date_query=2023-10-01"
```

Respuesta: HTTP 403 Forbidden.

## Ejecución de Tests

```bash
# Con Docker
docker compose run --rm api pytest

# Sin Docker (requiere Python 3.12 y dependencias instaladas)
pip install -r requirements.txt
pytest
```

## Estructura del Repositorio

```
proyecto-software/
├── app/                          # Código de la aplicación FastAPI
│   ├── __init__.py
│   └── main.py                   # Punto de entrada de la aplicación
├── tests/                        # Tests (pytest)
├── docs/
│   ├── adr/                      # Architecture Decision Records
│   └── specs/                    # PRD y especificaciones técnicas por fase
├── monitoring/
│   ├── prometheus/               # Configuración de Prometheus
│   └── grafana/provisioning/     # Datasources y dashboards de Grafana
├── .github/workflows/            # Pipelines de GitHub Actions
├── Dockerfile                    # Imagen Docker de la API
├── docker-compose.yml            # Orquestación de todos los servicios
├── requirements.txt              # Dependencias de Python
├── CLAUDE.md                     # Contexto del proyecto para Claude Code
└── README.md                     # Este archivo
```

## Architecture Decision Records (ADRs)

Las decisiones de diseño y arquitectura se documentan como ADRs en [`docs/adr/`](docs/adr/).

| ADR | Título | Estado |
|---|---|---|
| [ADR-001](docs/adr/ADR-001-tech-stack-and-architecture.md) | Stack tecnológico y arquitectura | Aceptado |

## Equipo

| Nombre | Rol |
|---|---|
| *Timoteo Menceyra* | *Owner* |
| *Felipe Viaggio* | *Owner* |
| *Alejo Zimmermann* | *Owner* |

## Historial de Entregas

| Fase | Fecha | URL Desplegada | Commit |
|---|---|---|---|
| Fase 1 | 2026-04-28 | *Pendiente* | *Pendiente* |
| Fase 2 | 2026-06-09 | *Pendiente* | *Pendiente* |
| Fase 3 | 2026-06-30 | *Pendiente* | *Pendiente* |
