import pytest
from app.services.biometrics_analyzer import analyze_telemetry

@pytest.mark.parametrize(
    "biomarker, value, expected_risk, expected_substring",
    [
        ("radiationDoseMsv", 2.5, "CRITICAL", "Exposição crítica à radiação"),
        ("radiationDoseMsv", 1.2, "WARNING", "Atividade solar elevada"),
        ("sleepHours", 4.0, "CRITICAL", "Privação severa de sono"),
        ("sleepHours", 6.0, "WARNING", "Fadiga moderada"),
        ("spo2", 88, "CRITICAL", "Hipóxia crítica"),
        ("heartRate", 45, "CRITICAL", "Frequência cardíaca crítica"),
    ],
)
def test_individual_biomarker_thresholds(biomarker, value, expected_risk, expected_substring):
    base_payload = {
        "astronautId": "ASTRO-01",
        "timestamp": "2026-11-14T15:30:00Z",
        "heartRate": 75,
        "spo2": 98,
        "radiationDoseMsv": 0.2,
        "sleepHours": 8.0,
    }
    base_payload[biomarker] = value

    result = analyze_telemetry(base_payload)

    assert result['riskLevel'] == expected_risk
    assert expected_substring in result['alertMessage']

def test_critical_rule_prevents_duplicate_warning_for_same_biomarker():
    payload = {
        "astronautId": "ASTRO-01",
        "timestamp": "2026-11-14T15:30",
        "heartRate": 130,
        "spo2": 98,
        "radiationDoseMsv": 0.2,
        "sleepHours": 8.0,
    }

    result = analyze_telemetry(payload)

    assert result['riskLevel'] == "CRITICAL"
    assert "Frequência cardíaca crítica detectada" in result["alertMessage"]
    assert "Frequência cardíaca elevada/baixa detectada" not in result["alertMessage"]

def test_cross_rule_exhaustion_critical():
    payload = {
        "astronautId": "ASTRO-01",
        "timestamp": "2026-11-14T15:30:00Z",
        "heartRate": 118,
        "spo2": 98,
        "radiationDoseMsv": 0.2,
        "sleepHours": 5.0,
    }

    result = analyze_telemetry(payload)

    assert result["riskLevel"] == "CRITICAL"
    assert "Exaustão física e cognitiva crítica" in result["alertMessage"]

def test_input_payload_is_not_mutated():
    original_payload = {
        "astronautId": "ASTRO-01",
        "timestamp": "2026-11-14T15:30:00Z",
        "heartRate": 75,
        "spo2": 98,
        "radiationDoseMsv": 0.2,
        "sleepHours": 8.0,
    }

    result = analyze_telemetry(original_payload)

    assert "riskLevel" not in original_payload
    assert "riskLevel" in result