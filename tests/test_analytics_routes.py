def test_health_check(client):
    response = client.get('/api/v1/health')
    assert response.status_code == 200
    assert response.get_json()['status'] == "healthy"
    assert response.get_json()['service'] == "telemetry-analytics"

def test_nominal_telemetry(client):
    data = {
        "astronautId": "ASTRO-01",
        "timestamp": "2026-11-14T15:30:00Z",
        "heartRate": 60,
        "spo2": 96,
        "radiationDoseMsv": 0.4,
        "sleepHours": 7.0
        }
    response = client.post('/api/v1/analyze', json=data)
    assert response.status_code == 200
    assert response.get_json()['riskLevel'] == "NOMINAL"
    assert response.get_json()['recommendedAction'] == "Manter cronograma nominal da missão e monitoramento telemétrico padrão."

def test_warning_telemetry(client):
    data = {
        "astronautId": "ASTRO-01",
        "timestamp": "2026-11-14T15:30:00Z",
        "heartRate": 105,
        "spo2": 96,
        "radiationDoseMsv": 0.4,
        "sleepHours": 7.0
        }
    response = client.post('/api/v1/analyze', json=data)
    assert response.status_code == 200
    assert response.get_json()['riskLevel'] == "WARNING"
    assert response.get_json()['recommendedAction'] == "Reduzir carga física, reforçar hidratação e reavaliar sinais vitais em 15 minutos."

def test_cross_rule_cardiorespiratory_critical(client):
    data = {
        "astronautId": "ASTRO-01",
        "timestamp": "2026-11-14T15:30:00Z",
        "heartRate": 115,
        "spo2": 92,
        "radiationDoseMsv": 0.4,
        "sleepHours": 7.0
        }
    response = client.post('/api/v1/analyze', json=data)
    assert response.status_code == 200
    assert response.get_json()['riskLevel'] == "CRITICAL"
    assert "Abortar atividade extraveicular (EVA)" in response.get_json()['recommendedAction']

def test_invalid_telemetry_returns_422(client):
    data = {
        "astronautId": "ASTRO-01",
        "timestamp": "2026-11-14T15:30:00Z",
        "heartRate": 118,
        "spo2": 150,
        "radiationDoseMsv": 0.4,
        "sleepHours": 7.0
        }
    response = client.post('/api/v1/analyze', json=data)
    assert response.status_code == 422

def test_empty_payload_returns_400(client):
    response = client.post('/api/v1/analyze')
    assert response.status_code == 400

def test_unknown_fields_are_excluded(client):
    data = {
        "astronautId": "ASTRO-01",
        "timestamp": "2026-11-14T15:30:00Z",
        "heartRate": 118,
        "spo2": 96,
        "radiationDoseMsv": 0.4,
        "sleepHours": 7.0,
        "temperature": 31
        }
    response = client.post('/api/v1/analyze', json=data)
    assert response.status_code == 200
    assert "temperature" not in response.get_json()