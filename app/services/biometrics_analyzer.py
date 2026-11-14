SEVERITY_WEIGHTS = {
    "NOMINAL": 0,
    "WARNING": 1,
    "CRITICAL": 2,
}

DEFAULT_NOMINAL_ACTION = "Manter cronograma nominal da missão e monitoramento telemétrico padrão."
DEFAULT_WARNING_ACTION = "Reduzir carga física, reforçar hidratação e reavaliar sinais vitais em 15 minutos."

INDIVIDUAL_RULES = [
    # --- CRITICAL ---
    {
        "biomarker": "heartRate",
        "severity": "CRITICAL",
        "condition": lambda d: d["heartRate"] < 50 or d["heartRate"] > 120,
        "message": "Frequência cardíaca crítica detectada (< 50 ou > 120 bpm).",
        "action": "Manter repouso absoluto e iniciar eletrocardiograma contínuo para telemetria médica.",
    },
    {
        "biomarker": "spo2",
        "severity": "CRITICAL",
        "condition": lambda d: d["spo2"] < 90,
        "message": "Hipóxia crítica detectada (SpO2 < 90%).",
        "action": "Verificar vedação do traje/cabine e administrar oxigênio suplementar a 100%.",
    },
    {
        "biomarker": "radiationDoseMsv",
        "severity": "CRITICAL",
        "condition": lambda d: d["radiationDoseMsv"] > 2.0,
        "message": "Exposição crítica à radiação (> 2.0 mSv).",
        "action": "Recolher tripulante ao módulo blindado contra radiação solar e monitorar dosimetria.",
    },
    {
        "biomarker": "sleepHours",
        "severity": "CRITICAL",
        "condition": lambda d: d["sleepHours"] < 5.0,
        "message": "Privação severa de sono (< 5.0h).",
        "action": "Realocar turnos da tripulação para garantir ciclo mínimo de recuperação de 8 horas.",
    },
    # --- WARNING ---
    {
        "biomarker": "heartRate",
        "severity": "WARNING",
        "condition": lambda d: (50 <= d["heartRate"] <= 59) or (101 <= d["heartRate"] <= 120),
        "message": "Frequência cardíaca elevada/baixa detectada.",
        "action": DEFAULT_WARNING_ACTION,
    },
    {
        "biomarker": "spo2",
        "severity": "WARNING",
        "condition": lambda d: 90 <= d["spo2"] <= 94,
        "message": "Saturação de oxigênio em alerta (90% - 94%). Monitorar respiração.",
        "action": DEFAULT_WARNING_ACTION,
    },
    {
        "biomarker": "radiationDoseMsv",
        "severity": "WARNING",
        "condition": lambda d: 0.5 <= d["radiationDoseMsv"] <= 2.0,
        "message": "Atividade solar elevada (0.5 - 2.0 mSv).",
        "action": DEFAULT_WARNING_ACTION,
    },
    {
        "biomarker": "sleepHours",
        "severity": "WARNING",
        "condition": lambda d: 5.0 <= d["sleepHours"] <= 6.9,
        "message": "Fadiga moderada por baixa duração de sono (5.0h - 6.9h).",
        "action": DEFAULT_WARNING_ACTION,
    },
]

CROSS_RULES = [
    {
        "severity": "CRITICAL",
        "condition": lambda d: d["heartRate"] > 110 and d["spo2"] < 93,
        "message": "Alerta cruzado: Estresse cardiorrespiratório agudo (taquicardia com queda de oxigenação).",
        "action": "Abortar atividade extraveicular (EVA), iniciar oxigenoterapia suplementar imediata e acionar médico de voo.",
    },
    {
        "severity": "CRITICAL",
        "condition": lambda d: d["sleepHours"] < 5.5 and d["heartRate"] > 115,
        "message": "Alerta cruzado: Exaustão física e cognitiva crítica.",
        "action": "Suspender tarefas críticas de operação e instituir protocolo imediato de repouso assistido.",
    },
]

def analyze_telemetry(data:dict) -> dict:
    result = data.copy()
    max_severity = "NOMINAL"
    alerts = []
    evaluated_biomarkers = set()
    primary_action = DEFAULT_NOMINAL_ACTION
    action_priority = 0

    for rule in INDIVIDUAL_RULES:
        biomarker = rule['biomarker']
        if biomarker not in evaluated_biomarkers:
            if rule['condition'](result):
                evaluated_biomarkers.add(biomarker)
                alerts.append(rule['message'])
                sev = rule['severity']

                if SEVERITY_WEIGHTS[sev] > SEVERITY_WEIGHTS[max_severity]:
                    max_severity = sev

                priority = 2 if sev == "CRITICAL" else 1
                if priority > action_priority:
                    action_priority = priority
                    primary_action = rule['action']

    for rule in CROSS_RULES:
        if rule['condition'](result):
            alerts.append(rule['message'])
            sev = rule['severity']

            if SEVERITY_WEIGHTS[sev] > SEVERITY_WEIGHTS[max_severity]:
                max_severity = sev

            if 3 > action_priority:
                action_priority = 3
                primary_action = rule['action']


    result['riskLevel'] = max_severity
    result['alertMessage'] = " | ".join(alerts) if alerts else "Todos os parâmetros biométricos dentro da faixa nominal."
    result['recommendedAction'] = primary_action

    return result