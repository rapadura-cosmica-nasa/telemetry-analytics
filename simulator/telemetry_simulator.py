from datetime import datetime, timezone
import os
import random
import time
import requests

API_URL = os.getenv("API_URL","http://localhost:8080/api/telemetry")


def gerar_dados_astronauta(modo: str = "aleatorio") -> dict:
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    if modo == "nominal":
        heart_rate = random.randint(65, 88)
        spo2 = random.randint(96, 99)
        radiation = round(random.uniform(0.1, 0.35), 2)
        sleep_hours = round(random.uniform(7.2, 8.5), 1)
    elif modo == "critico":
        # Simula estresse cardiorrespiratório agudo
        heart_rate = random.randint(114, 128)
        spo2 = random.randint(88, 92)
        radiation = round(random.uniform(1.8, 2.4), 2)
        sleep_hours = round(random.uniform(4.2, 5.2), 1)
    else:
        heart_rate = random.randint(55, 130)
        spo2 = random.randint(86, 100)
        radiation = round(random.uniform(0.2, 2.3), 2)
        sleep_hours = round(random.uniform(4.5, 9.0), 1)

    return {
        "astronautId": "ASTRO-01",
        "timestamp": timestamp,
        "heartRate": heart_rate,
        "spo2": spo2,
        "radiationDoseMsv": radiation,
        "sleepHours": sleep_hours,
    }


def iniciar_simulacao():
    print("=== SIMULADOR DE TELEMETRIA ESPACIAL (RAPADURA CÓSMICA) ===")
    print("Escolha o cenário de simulação:")
    print("  [1] Missão Nominal (Sinais estáveis)")
    print("  [2] Alerta Crítico (Estresse cardiorrespiratório / Radiação)")
    print("  [3] Aleatório (Variação contínua)")

    opcao = input("Opção (padrão 3): ").strip()
    modos = {"1": "nominal", "2": "critico", "3": "aleatorio"}
    modo_selecionado = modos.get(opcao, "aleatorio")

    print(f"\nIniciando transmissão em modo [{modo_selecionado.upper()}] para: {API_URL}")
    print("Pressione Ctrl+C para encerrar.\n")

    try:
        while True:
            payload = gerar_dados_astronauta(modo=modo_selecionado)
            print(f"[{payload['timestamp']}] Enviando: HR={payload['heartRate']} bpm | SpO2={payload['spo2']}% | Rad={payload['radiationDoseMsv']} mSv | Sono={payload['sleepHours']}h")

            try:
                resposta = requests.post(API_URL, json=payload, timeout=2)
                if resposta.ok:
                    dados_retorno = resposta.json() if resposta.content else {}
                    risco = dados_retorno.get("riskLevel", "PROCESSADO")
                    print(f"  -> OK ({resposta.status_code}) | Classificação: {risco}\n")
                else:
                    print(f"  -> Rejeitado pela API ({resposta.status_code}): {resposta.text}\n")
            except requests.exceptions.ConnectionError:
                print("  -> [Aviso] API Java offline em localhost:8080. Tentando novamente em 3s...\n")
            except requests.exceptions.RequestException as err:
                print(f"  -> [Erro de Rede] {err}\n")

            time.sleep(3)

    except KeyboardInterrupt:
        print("\nSimulação encerrada com segurança pelo operador.")


if __name__ == "__main__":
    iniciar_simulacao()