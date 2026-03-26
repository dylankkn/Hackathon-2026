from openai import OpenAI
from dotenv import load_dotenv
import os
from config import Modelos
import serial

load_dotenv()
api_key = os.environ.get("API_KEY")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

def gerarResposta(historico: list, prompt, modelo: Modelos = Modelos.StepFun_35_FLASH):
    historico.insert(0, {
        "role": "system",
        "content": prompt
    })
    completion = client.chat.completions.create(
        model=modelo.value,
        messages=historico,
        stream=False
    )
    message = completion.choices[0].message
    resposta = {
        "role": "assistant",
        "content": message.content or "",
        "reasoning": getattr(message, 'reasoning', "") or ""
    }
    return resposta["content"]

def iniciar_quiz(arduino):
    print("\n" + "="*40)
    historico = []

    # Solicita tema do quiz
    prompt = "Sugira um tema curto para um quiz. Apenas o nome."
    tema = gerarResposta(historico, prompt=prompt)
    print(f"🎯 Tema: {tema}")

    acertos = 0
    total = 1  # Número de perguntas

    for i in range(total):
        print(f"\nPergunta {i+1}")
        prompt = (
            f"Sobre o tema '{tema}', gere a pergunta {i+1} de {total}. "
            "Use 3 alternativas (A, B, C) e indique a correta no fim. "
            "O formato da sua resposta deve ser: PERGUNTA ; ALT_A ; ALT_B ; ALT_C ; LETRA_CORRETA"
        )
        pergunta = gerarResposta(historico, prompt=prompt)
        partes = pergunta.split(";")

        if len(partes) < 5:
            print("⚠️ Erro IA: resposta inválida")
            continue

        # Exibe a pergunta e alternativas
        print(partes[0])
        print("A)", partes[1])
        print("B)", partes[2])
        print("C)", partes[3])
        print("Aguardando resposta do Arduino...")

        resposta = None

        # Espera resposta do Arduino
        while True:
            if arduino.in_waiting:
                msg = arduino.readline().decode().strip()

                if msg == "RESPOSTA_A":
                    resposta = "A"
                    # Envia comando para resetar LEDs de resposta
                    arduino.write(b'RESET_QUIZ\n')
                    break
                elif msg == "RESPOSTA_B":
                    resposta = "B"
                    arduino.write(b'RESET_QUIZ\n')
                    break
                elif msg == "RESPOSTA_C":
                    resposta = "C"
                    arduino.write(b'RESET_QUIZ\n')
                    break

        correta = partes[4].strip().upper()
        print("Resposta:", resposta)

        if resposta == correta:
            print("✅ Acertou!")
            acertos += 1
        else:
            print("❌ Errou! Correta:", correta)

    print(f"\n📊 Resultado final: {acertos}/{total}")