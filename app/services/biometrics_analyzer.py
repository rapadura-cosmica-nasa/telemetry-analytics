SEVERITY_WEIGHTS = {
    "NOMINAL": 0,
    "WARNING": 1,
    "CRITICAL": 2,
}

WEIGHT_TO_SEVERITY = {
    0: "NOMINAL",
    1: "WARNING",
    2: "CRITICAL",
}

INDIVIDUAL_RULES = [
    ("heartRate", lambda v: v < 50 or v > 120, "CRITICAL", "Frequência cardíaca crítica detectada (< 50 ou > 120 bpm)."),
    ("heartRate", lambda v: (50 <= v <= 59) or (101 <= v <= 120), "WARNING", "Frequência cardíaca elevada/baixa detectada. Recomenda-se hidratação e repouso."),
    ("spo2", lambda v: v < 90, "CRITICAL", "Hipóxia crítica detectada (SpO2 < 90%). Acionar suporte de oxigênio."),
    ("spo2", lambda v: 90 <= v <= 94, "WARNING", "Saturação de oxigênio em alerta (90% - 94%). Monitorar respiração."),
    ("radiationDoseMsv", lambda v: v > 2.0, "CRITICAL", "Exposição crítica à radiação (> 2.0 mSv). Recolher imediatamente para módulo blindado."),
    ("radiationDoseMsv", lambda v: 0.5 <= v <= 2.0, "WARNING", "Atividade solar elevada (0.5 - 2.0 mSv). Monitorar exposição."),
    ("sleepHours", lambda v: v < 5.0, "CRITICAL", "Privação severa de sono (< 5.0h). Risco crítico de falha operacional."),
    ("sleepHours", lambda v: 5.0 <= v <= 6.9, "WARNING", "Fadiga moderada por sono insuficiente (< 7.0h)."),
]

CROSS_RULES = [
    (
        lambda d: d["heartRate"] > 110 and d["spo2"] < 93,
        "CRITICAL",
        "Alerta cruzado: Estresse cardiorrespiratório agudo (taquicardia com queda de oxigenação)."
    ),
    (
        lambda d: d["sleepHours"] < 5.5 and d["heartRate"] > 115,
        "CRITICAL",
        "Alerta cruzado: Exaustão física e cognitiva crítica."
    ),
]

def analyze_telemetry(data:dict) -> dict:
    max_weight = 0
    alerts = []
    evaluated_biomarkers = set()

    for biomarker, condition, severity, message in INDIVIDUAL_RULES:
        if biomarker not in evaluated_biomarkers:
            if condition(data[biomarker]):
                max_weight = max(max_weight, SEVERITY_WEIGHTS[severity])
                alerts.append(message)
                evaluated_biomarkers.add(biomarker)

    for condition, severity, message in CROSS_RULES:
        if condition(data):
            max_weight = max(max_weight, SEVERITY_WEIGHTS[severity])
            alerts.append(message)

    risk_level = WEIGHT_TO_SEVERITY[max_weight]
    if alerts:
        alert_message = " | ".join(alerts)
    else:
        alert_message = "Todos os parâmetros biométricos dentro da normalidade."

    result = data.copy()
    result['riskLevel'] = risk_level
    result['alertMessage'] = alert_message
    return result