from datetime import datetime, timezone
import random
import time
import requests

url = "http://localhost:8080/api/telemetry"

print("--- SIMULADOR DE TELEMETRIA ESPACIAL (NASA SPACE APPS" \
") ---")
print("Escolha o modo de operação para a demonstração:")
print("1 - Missão Nominal (Valores seguros/estáveis)")
print("2 - Tempestade Solar / Crítico (Gera alertas para os jurados)")
print("3 - Aleatório (Comportamento padrão)")

escolha = input("Digite o número do modo desejado (padrão 3): ").strip()
if escolha not in ["1", "2", "3"]:
    escolha = "3"


def gerar_dados_astronauta(modo):
    astronautId = "ASTRO-01"
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    if modo == "1": 
        heartRate = random.randint(65, 85)
        spo2 = random.randint(97, 100)
        radiationDoseMsv = round(random.uniform(0.1, 0.4), 2)
        sleepHours = round(random.uniform(7.5, 8.5), 1)
    elif modo == "2": 
        heartRate = random.randint(125, 145)
        spo2 = random.randint(82, 89)
        radiationDoseMsv = round(random.uniform(2.1, 3.5), 2)
        sleepHours = round(random.uniform(3.0, 4.5), 1)
    else:
        heartRate = random.randint(55, 130)
        spo2 = random.randint(85, 100)
        radiationDoseMsv = round(random.uniform(0.3, 2.3), 2)
        sleepHours = round(random.uniform(4.0, 9.5), 1)

    dados = {
        "astronautId": astronautId,
        "timestamp": timestamp,
        "heartRate": heartRate,
        "spo2": spo2,
        "radiationDoseMsv": radiationDoseMsv,
        "sleepHours": sleepHours,
    }
    return dados


print(f"\nIniciando envio para: {url} (Modo selecionado: {escolha})\n")

try:
    while True:
        biometria = gerar_dados_astronauta(escolha)
        print("Dados gerados:", biometria if "biometripa" in locals() else biometria)

        try:
            resposta = requests.post(url, json=biometria, timeout=3)
            print(f" -> Enviado com sucesso! Status HTTP: {resposta.status_code}")

            if resposta.content and "application/json" in resposta.headers.get(
                "Content-Type", ""
            ):
                analise = resposta.json()
                if "riskLevel" in analise:
                    print(f" -> Nível de Risco Retornado: {analise['riskLevel']}")

            print()
        except requests.exceptions.RequestException as e:
            print(
                f" -> [Aviso] API Java offline ou instável ({e}). Tentando novamente no próximo ciclo...\n"
            )

        time.sleep(3)

except KeyboardInterrupt:
    print("\nSimulação encerrada pelo usuário.")