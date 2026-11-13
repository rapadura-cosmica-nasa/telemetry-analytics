<a id="top"></a>
<div align="center">

# 🛰️ Telemetry Analytics (`telemetry-analytics`)

**Clinical Risk Assessment & Aerospace Biometrics Microservice — Team Rapadura Cósmica**

[![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-Application_Factory-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Marshmallow](https://img.shields.io/badge/Marshmallow-Validation-2E8B57?style=for-the-badge&logo=python&logoColor=white)](https://marshmallow.readthedocs.io/)
[![Pytest](https://img.shields.io/badge/Pytest-Tested-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white)](https://docs.pytest.org/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)

[🇺🇸 English](#english-docs) • [🇧🇷 Português](#portugues-docs)

</div>

---

<a id="english-docs"></a>
## 🇺🇸 English

### Overview

This microservice is the **Clinical Intelligence & Risk Analysis Engine** (`telemetry-analytics`) developed by **Team Rapadura Cósmica** for the NASA Space Apps Challenge.

Operating as a stateless inference service within a decoupled microservice architecture, it receives raw astronaut biometric and environmental telemetry from the **Core API (Java / Spring Boot)**, validates payload integrity, evaluates individual and cross-biomarker clinical rules, and returns a classified risk assessment for persistence and real-time mission dashboard visualization.

### System Flow

```text
[Simulator / Hardware] ──(POST /api/telemetry)──► [Core API: Spring Boot] ──► [H2 Database]
                                                         │          │
                               (GET /api/telemetry/latest)          └──(POST /api/v1/analyze)──► [Flask Analytics Engine]
                                         ▼                                                               │
                                [Mission Dashboard] ◄───────────────(200 OK: Classified JSON)───────────┘
```

### Project Architecture

Built following the **Flask Application Factory** pattern to ensure strict separation between HTTP transport, schema validation, and aerospace medical logic:

```text
telemetry-edge-engine/
├── app/
│   ├── __init__.py                 # create_app() - Application Factory
│   ├── core/
│   │   ├── config.py               # Environment settings
│   │   └── error_handlers.py       # Standardized HTTP JSON error handlers (400, 422, 500)
│   ├── schemas/
│   │   └── telemetry_schema.py     # Marshmallow contract validation & camelCase mapping
│   ├── routes/
│   │   └── analytics_routes.py     # Blueprint: POST /api/v1/analyze & GET /health
│   └── services/
│       └── biometrics_analyzer.py  # Clinical rule engine (thresholds + cross-correlation)
├── tests/
│   ├── test_biometrics_analyzer.py # Unit tests for clinical triage rules
│   └── test_analytics_routes.py    # Integration tests for API endpoints
├── Dockerfile
├── requirements.txt
└── run.py
```

### API Contract

#### Healthcheck
* **Endpoint:** `GET /health`
* **Response (`200 OK`):**
```json
{
  "status": "UP",
  "service": "telemetry-analytics"
}
```

#### Clinical Risk Analysis
* **Endpoint:** `POST /api/v1/analyze`
* **Request Payload (from Core API):**
```json
{
  "astronautId": "ASTRO-01",
  "timestamp": "2026-11-14T15:30:00Z",
  "heartRate": 118,
  "spo2": 96,
  "radiationDoseMsv": 1.4,
  "sleepHours": 5.2
}
```
* **Response Payload (`200 OK` — Enriched Telemetry):**
```json
{
  "astronautId": "ASTRO-01",
  "timestamp": "2026-11-14T15:30:00Z",
  "heartRate": 118,
  "spo2": 96,
  "radiationDoseMsv": 1.4,
  "sleepHours": 5.2,
  "riskLevel": "CRITICAL",
  "alertMessage": "Frequência cardíaca elevada detectada. Recomenda-se hidratação e repouso. | Atividade solar elevada (0.5 - 2.0 mSv). Monitorar exposição. | Fadiga moderada por sono insuficiente (< 7h). | Alerta cruzado: Exaustão física e cognitiva crítica."
}
```

### Clinical Triage Matrix

| Biomarker | `NOMINAL` | `WARNING` | `CRITICAL` |
| :--- | :--- | :--- | :--- |
| **`heartRate` (bpm)** | `60 – 100` | `50 – 59` or `101 – 120` | `< 50` or `> 120` |
| **`spo2` (%)** | `95 – 100` | `90 – 94` | `< 90` |
| **`radiationDoseMsv` (mSv)** | `< 0.5` | `0.5 – 2.0` | `> 2.0` |
| **`sleepHours` (hours)** | `7.0 – 9.0` | `5.0 – 6.9` | `< 5.0` |

#### Cross-Biomarker Rules (Escalation to `CRITICAL`)
1. **Cardiorespiratory Stress:** `heartRate > 110` **AND** `spo2 < 93` (compensatory tachycardia during oxygen drop).
2. **Acute Operational Exhaustion:** `sleepHours < 5.5` **AND** `heartRate > 115` (high risk of syncope or cognitive error during EVA/operations).

### Getting Started

```bash
# 1. Clone the repository
git clone https://github.com/MuriloDev07/telemetry-analytics.git
cd telemetry-analytics

# 2. Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the development server
python run.py

# 5. Run unit and integration tests
pytest
```

---

<a id="portugues-docs"></a>
## 🇧🇷 Português

[⬆️ Back to top / Voltar ao topo](#top)

### Visão Geral

Este microsserviço é o **Motor de Inteligência Clínica e Análise de Riscos** (`telemetry-analytics`) desenvolvido pela equipe **Rapadura Cósmica** para o NASA Space Apps Challenge.

Operando como um serviço de inferência *stateless* dentro de uma arquitetura de microsserviços desacoplados, ele recebe os dados biométricos e ambientais brutos da **Core API (Java / Spring Boot)**, valida a integridade do contrato JSON, avalia regras clínicas individuais e cruzadas e devolve a classificação de risco para persistência e exibição no painel da missão.

### Fluxo no Sistema

```text
[Simulador / Hardware] ──(POST /api/telemetry)──► [Core API: Spring Boot] ──► [Banco H2]
                                                         │          │
                               (GET /api/telemetry/latest)          └──(POST /api/v1/analyze)──► [Motor Flask Analytics]
                                         ▼                                                               │
                                [Painel da Missão] ◄───────────────(200 OK: JSON Classificado)───────────┘
```

### Arquitetura do Projeto

Estruturado sob o padrão **Flask Application Factory** para garantir separação clara entre transporte HTTP, validação de schema e regras médicas aeroespaciais:

```text
telemetry-edge-engine/
├── app/
│   ├── __init__.py                 # create_app() - Application Factory
│   ├── core/
│   │   ├── config.py               # Configurações de ambiente
│   │   └── error_handlers.py       # Tratamento padronizado de erros HTTP JSON (400, 422, 500)
│   ├── schemas/
│   │   └── telemetry_schema.py     # Validação Marshmallow e mapeamento camelCase
│   ├── routes/
│   │   └── analytics_routes.py     # Blueprint: POST /api/v1/analyze e GET /health
│   └── services/
│       └── biometrics_analyzer.py  # Motor clínico (limiares individuais + regras cruzadas)
├── tests/
│   ├── test_biometrics_analyzer.py # Testes unitários das regras de triagem clínica
│   └── test_analytics_routes.py    # Testes de integração dos endpoints da API
├── Dockerfile
├── requirements.txt
└── run.py
```

### Contrato da API

#### Healthcheck
* **Endpoint:** `GET /health`
* **Resposta (`200 OK`):**
```json
{
  "status": "UP",
  "service": "telemetry-analytics"
}
```

#### Análise de Risco Clínico
* **Endpoint:** `POST /api/v1/analyze`
* **Payload de Entrada (enviado pela Core API):**
```json
{
  "astronautId": "ASTRO-01",
  "timestamp": "2026-11-14T15:30:00Z",
  "heartRate": 118,
  "spo2": 96,
  "radiationDoseMsv": 1.4,
  "sleepHours": 5.2
}
```
* **Payload de Saída (`200 OK` — Telemetria Enriquecida):**
```json
{
  "astronautId": "ASTRO-01",
  "timestamp": "2026-11-14T15:30:00Z",
  "heartRate": 118,
  "spo2": 96,
  "radiationDoseMsv": 1.4,
  "sleepHours": 5.2,
  "riskLevel": "CRITICAL",
  "alertMessage": "Frequência cardíaca elevada detectada. Recomenda-se hidratação e repouso. | Atividade solar elevada (0.5 - 2.0 mSv). Monitorar exposição. | Fadiga moderada por sono insuficiente (< 7h). | Alerta cruzado: Exaustão física e cognitiva crítica."
}
```

### Matriz de Triagem Clínica

| Biomarcador | `NOMINAL` | `WARNING` | `CRITICAL` |
| :--- | :--- | :--- | :--- |
| **`heartRate` (bpm)** | `60 – 100` | `50 – 59` ou `101 – 120` | `< 50` ou `> 120` |
| **`spo2` (%)** | `95 – 100` | `90 – 94` | `< 90` |
| **`radiationDoseMsv` (mSv)** | `< 0.5` | `0.5 – 2.0` | `> 2.0` |
| **`sleepHours` (horas)** | `7.0 – 9.0` | `5.0 – 6.9` | `< 5.0` |

#### Regras Cruzadas (Escalonamento para `CRITICAL`)
1. **Estresse Cardiorrespiratório:** `heartRate > 110` **E** `spo2 < 93` (taquicardia compensatória associada à queda de oxigenação).
2. **Exaustão Operacional Aguda:** `sleepHours < 5.5` **E** `heartRate > 115` (alto risco de síncope ou erro cognitivo em atividade operacional).

### Como Executar Localmente

```bash
# 1. Clone o repositório
git clone https://github.com/MuriloDev07/telemetry-analytics.git
cd telemetry-analytics

# 2. Crie e ative o ambiente virtual
python3 -m venv venv
source venv/bin/activate

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Inicie o servidor de desenvolvimento
python run.py

# 5. Execute os testes automatizados
pytest
```
