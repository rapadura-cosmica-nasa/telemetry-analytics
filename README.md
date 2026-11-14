<a id="top"></a>
<div align="center">

# 🛰️ Telemetry Analytics (`telemetry-analytics`)

**Clinical Risk Assessment, Operational Protocol & Aerospace Biometrics Microservice — Team Rapadura Cósmica**

[![Python](https://img.shields.io/badge/Python-3.12+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-Application_Factory-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Marshmallow](https://img.shields.io/badge/Marshmallow-Validation-2E8B57?style=for-the-badge&logo=python&logoColor=white)](https://marshmallow.readthedocs.io/)
[![Pytest](https://img.shields.io/badge/Pytest-Tested-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white)](https://docs.pytest.org/)

[🇺🇸 English](#english-docs) • [🇧🇷 Português](#portugues-docs)

</div>

---

<a id="english-docs"></a>
## 🇺🇸 English

### Overview

This microservice is the **Clinical Intelligence, Risk Analysis & Operational Protocol Engine** (`telemetry-analytics`) developed by **Team Rapadura Cósmica** for the NASA Space Apps Challenge.

Operating as a stateless inference service within a decoupled microservice architecture, it receives raw astronaut biometric and environmental telemetry from the **Core API (Java / Spring Boot)**, validates payload integrity, evaluates individual and cross-biomarker clinical rules, and returns a classified risk assessment along with prioritized operational action directives (`recommendedAction`) for persistence and real-time mission dashboard visualization.

### System Flow

```text
[Telemetry Simulator] ──(POST /api/telemetry)──► [Core API: Spring Boot] ──► [H2 Database]
                                                        │          │
                              (GET /api/telemetry/latest)          └──(POST /api/v1/analyze)──► [Flask Analytics Engine]
                                        ▼                                                               │
                               [Mission Dashboard] ◄───────────────(200 OK: Enriched JSON)────────────┘
```

### Project Architecture

Built following the **Flask Application Factory** pattern to ensure strict separation between HTTP transport, schema validation, aerospace medical logic, and synthetic telemetry simulation:

```text
telemetry-analytics/
├── app/
│   ├── __init__.py                 # create_app() - Application Factory & global error handlers
│   ├── core/                       # Core settings & application utilities
│   ├── schemas/
│   │   └── telemetry_schema.py     # Marshmallow contract validation & camelCase mapping
│   ├── routes/
│   │   └── analytics_routes.py     # Blueprint: POST /api/v1/analyze & GET /api/v1/health
│   └── services/
│       └── biometrics_analyzer.py  # Clinical rule engine (thresholds, cross-rules & action protocols)
├── simulator/
│   └── telemetry_simulator.py      # Interactive spatial telemetry generator (Nominal, Critical, Random)
├── tests/
│   ├── conftest.py                 # Pytest Flask test client fixtures
│   ├── test_biometrics_analyzer.py # Parameterized unit tests for clinical rules & action priority
│   └── test_analytics_routes.py    # Integration tests for HTTP endpoints & contract validation
├── requirements.txt
└── run.py
```

### API Contract

#### Healthcheck
* **Endpoint:** `GET /api/v1/health`
* **Response (`200 OK`):**
```json
{
  "status": "healthy",
  "service": "telemetry-analytics"
}
```

#### Clinical Risk Analysis & Action Protocol
* **Endpoint:** `POST /api/v1/analyze`
* **Request Payload (from Core API):**
```json
{
  "astronautId": "ASTRO-01",
  "timestamp": "2026-11-14T15:30:00Z",
  "heartRate": 115,
  "spo2": 92,
  "radiationDoseMsv": 1.4,
  "sleepHours": 5.2
}
```
* **Response Payload (`200 OK` — Enriched Telemetry):**
```json
{
  "astronautId": "ASTRO-01",
  "timestamp": "2026-11-14T15:30:00Z",
  "heartRate": 115,
  "spo2": 92,
  "radiationDoseMsv": 1.4,
  "sleepHours": 5.2,
  "riskLevel": "CRITICAL",
  "alertMessage": "Frequência cardíaca elevada/baixa detectada. | Saturação de oxigênio em alerta (90% - 94%). Monitorar respiração. | Atividade solar elevada (0.5 - 2.0 mSv). | Fadiga moderada por baixa duração de sono (5.0h - 6.9h). | Alerta cruzado: Estresse cardiorrespiratório agudo (taquicardia com queda de oxigenação).",
  "recommendedAction": "Abortar atividade extraveicular (EVA), iniciar oxigenoterapia suplementar imediata e acionar médico de voo."
}
```

### Clinical Triage Matrix & Operational Directives

| Biomarker | `NOMINAL` | `WARNING` | `CRITICAL` | Critical Operational Directive (`recommendedAction`) |
| :--- | :--- | :--- | :--- | :--- |
| **`heartRate` (bpm)** | `60 – 100` | `50 – 59` or `101 – 120` | `< 50` or `> 120` | Absolute rest & continuous ECG medical telemetry. |
| **`spo2` (%)** | `95 – 100` | `90 – 94` | `< 90` | Verify suit/cabin seal & administer 100% supplemental oxygen. |
| **`radiationDoseMsv` (mSv)** | `< 0.5` | `0.5 – 2.0` | `> 2.0` | Relocate crew member to radiation-shielded module & monitor dosimetry. |
| **`sleepHours` (hours)** | `7.0 – 9.0` | `5.0 – 6.9` | `< 5.0` | Reallocate crew shifts to enforce an 8-hour minimum recovery cycle. |

#### Cross-Biomarker Rules (Highest Priority Escalation to `CRITICAL`)
1. **Acute Cardiorespiratory Stress:** `heartRate > 110` **AND** `spo2 < 93` $\rightarrow$ *Abort EVA, initiate immediate supplemental oxygen therapy, and notify flight surgeon.*
2. **Acute Physical & Cognitive Exhaustion:** `sleepHours < 5.5` **AND** `heartRate > 115` $\rightarrow$ *Suspend mission-critical operations and enforce immediate assisted rest protocol.*

### Telemetry Simulator & Hardware Concept

* **Synthetic Telemetry Generator (`simulator/telemetry_simulator.py`):** Interactive CLI script capable of streaming continuous JSON payloads every 3 seconds in three mission modes (`Nominal`, `Critical`, and `Random`) directly to the Core API (`http://localhost:8080/api/telemetry`).
* **Wearable Hardware Prototype (Tinkercad):** Conceptual Arduino Uno + Potentiometer prototype simulating continuous analog biometric variance serialized into JSON over UART (`9600 baud`).

### Getting Started

```bash
# 1. Clone the repository
git clone https://github.com/rapadura-cosmica-nasa/telemetry-analytics.git
cd telemetry-analytics

# 2. Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the analytics microservice (Port 5000)
python run.py

# 5. Run unit and integration test suite
pytest -v

# 6. (Optional) Start the interactive telemetry simulator
python simulator/telemetry_simulator.py
```

---

<a id="portugues-docs"></a>
## 🇧🇷 Português

[⬆️ Back to top / Voltar ao topo](#top)

### Visão Geral

Este microsserviço é o **Motor de Inteligência Clínica, Análise de Riscos e Protocolos Operacionais** (`telemetry-analytics`) desenvolvido pela equipe **Rapadura Cósmica** para o NASA Space Apps Challenge.

Operando como um serviço de inferência *stateless* dentro de uma arquitetura de microsserviços desacoplados, ele recebe os dados biométricos e ambientais brutos da **Core API (Java / Spring Boot)**, valida a integridade do contrato JSON, avalia regras clínicas individuais e cruzadas e devolve a classificação de risco acompanhada de diretrizes operacionais priorizadas (`recommendedAction`) para persistência e exibição no painel da missão.

### Fluxo no Sistema

```text
[Simulador de Telemetria] ──(POST /api/telemetry)──► [Core API: Spring Boot] ──► [Banco H2]
                                                            │          │
                                  (GET /api/telemetry/latest)          └──(POST /api/v1/analyze)──► [Motor Flask Analytics]
                                            ▼                                                               │
                                   [Painel da Missão] ◄───────────────(200 OK: JSON Enriquecido)────────────┘
```

### Arquitetura do Projeto

Estruturado sob o padrão **Flask Application Factory** para garantir separação clara entre transporte HTTP, validação de schema, regras médicas aeroespaciais e simulação de telemetria:

```text
telemetry-analytics/
├── app/
│   ├── __init__.py                 # create_app() - Application Factory e handlers globais de erro
│   ├── core/                       # Configurações e utilitários centrais
│   ├── schemas/
│   │   └── telemetry_schema.py     # Validação Marshmallow e mapeamento camelCase
│   ├── routes/
│   │   └── analytics_routes.py     # Blueprint: POST /api/v1/analyze e GET /api/v1/health
│   └── services/
│       └── biometrics_analyzer.py  # Motor clínico (limiares, regras cruzadas e protocolos de ação)
├── simulator/
│   └── telemetry_simulator.py      # Gerador interativo de telemetria espacial (Nominal, Crítico, Aleatório)
├── tests/
│   ├── conftest.py                 # Fixtures Pytest para o cliente HTTP Flask
│   ├── test_biometrics_analyzer.py # Testes unitários parametrizados das regras e prioridade de ação
│   └── test_analytics_routes.py    # Testes de integração dos endpoints e contrato JSON
├── requirements.txt
└── run.py
```

### Contrato da API

#### Healthcheck
* **Endpoint:** `GET /api/v1/health`
* **Resposta (`200 OK`):**
```json
{
  "status": "healthy",
  "service": "telemetry-analytics"
}
```

#### Análise de Risco Clínico e Protocolo de Ação
* **Endpoint:** `POST /api/v1/analyze`
* **Payload de Entrada (enviado pela Core API):**
```json
{
  "astronautId": "ASTRO-01",
  "timestamp": "2026-11-14T15:30:00Z",
  "heartRate": 115,
  "spo2": 92,
  "radiationDoseMsv": 1.4,
  "sleepHours": 5.2
}
```
* **Payload de Saída (`200 OK` — Telemetria Enriquecida):**
```json
{
  "astronautId": "ASTRO-01",
  "timestamp": "2026-11-14T15:30:00Z",
  "heartRate": 115,
  "spo2": 92,
  "radiationDoseMsv": 1.4,
  "sleepHours": 5.2,
  "riskLevel": "CRITICAL",
  "alertMessage": "Frequência cardíaca elevada/baixa detectada. | Saturação de oxigênio em alerta (90% - 94%). Monitorar respiração. | Atividade solar elevada (0.5 - 2.0 mSv). | Fadiga moderada por baixa duração de sono (5.0h - 6.9h). | Alerta cruzado: Estresse cardiorrespiratório agudo (taquicardia com queda de oxigenação).",
  "recommendedAction": "Abortar atividade extraveicular (EVA), iniciar oxigenoterapia suplementar imediata e acionar médico de voo."
}
```

### Matriz de Triagem Clínica e Diretrizes Operacionais

| Biomarcador | `NOMINAL` | `WARNING` | `CRITICAL` | Diretriz Operacional Crítica (`recommendedAction`) |
| :--- | :--- | :--- | :--- | :--- |
| **`heartRate` (bpm)** | `60 – 100` | `50 – 59` ou `101 – 120` | `< 50` ou `> 120` | Manter repouso absoluto e iniciar eletrocardiograma contínuo para telemetria médica. |
| **`spo2` (%)** | `95 – 100` | `90 – 94` | `< 90` | Verificar vedação do traje/cabine e administrar oxigênio suplementar a 100%. |
| **`radiationDoseMsv` (mSv)** | `< 0.5` | `0.5 – 2.0` | `> 2.0` | Recolher tripulante ao módulo blindado contra radiação solar e monitorar dosimetria. |
| **`sleepHours` (horas)** | `7.0 – 9.0` | `5.0 – 6.9` | `< 5.0` | Realocar turnos da tripulação para garantir ciclo mínimo de recuperação de 8 horas. |

#### Regras Cruzadas (Prioridade Máxima — Escalonamento para `CRITICAL`)
1. **Estresse Cardiorrespiratório Agudo:** `heartRate > 110` **E** `spo2 < 93` $\rightarrow$ *Abortar atividade extraveicular (EVA), iniciar oxigenoterapia suplementar imediata e acionar médico de voo.*
2. **Exaustão Física e Cognitiva Crítica:** `sleepHours < 5.5` **E** `heartRate > 115` $\rightarrow$ *Suspender tarefas críticas de operação e instituir protocolo imediato de repouso assistido.*

### Simulador de Telemetria e Conceito de Hardware

* **Gerador Sintético (`simulator/telemetry_simulator.py`):** Script CLI interativo que transmite pacotes JSON a cada 3 segundos em três cenários de missão (`Nominal`, `Crítico` e `Aleatório`) diretamente para a Core API (`http://localhost:8080/api/telemetry`).
* **Protótipo Conceitual de Hardware (Tinkercad):** Circuito conceitual com Arduino Uno + Potenciômetro simulando variação biométrica analógica contínua serializada em JSON via UART (`9600 baud`).

### Como Executar Localmente

```bash
# 1. Clone o repositório
git clone https://github.com/rapadura-cosmica-nasa/telemetry-analytics.git
cd telemetry-analytics

# 2. Crie e ative o ambiente virtual
python3 -m venv venv
source venv/bin/activate

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Inicie o microsserviço de análise (Porta 5000)
python run.py

# 5. Execute a suíte de testes unitários e de integração
pytest -v

# 6. (Opcional) Inicie o simulador interativo de telemetria
python simulator/telemetry_simulator.py
```
