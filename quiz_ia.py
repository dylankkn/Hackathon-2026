from openai import OpenAI
from dotenv import load_dotenv
import os
from config import Modelos

load_dotenv()
api_key = os.environ.get("API_KEY")
client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=api_key,
)

def gerarResposta(historico : list, prompt, modelo : Modelos = Modelos.Nemotron_3_Super):

    historico.insert(0, {
        "role": "system", 
        "content": prompt
    })

    completion = client.chat.completions.create(
        model = modelo.value,
        messages = historico,
        stream=False
    )

    message = completion.choices[0].message

    resposta = {
        "role": "assistant",
        "content": message.content or "",
        "reasoning": getattr(message, 'reasoning', "") or ""
    }

    return resposta["content"]

def iniciar_quiz():
    print("\n" + "—"*40)
    
    try:
        # 1. IA escolhe um tema (Nova sintaxe: models.generate_content)
        tema_res = gerarResposta(
            historico=[], 
            prompt="Sugira um tema curto para um quiz de 5 perguntas. Responda apenas o nome do tema."
        )
        tema = tema_res.strip()
        print(f"🤖 IA (v2.0): O tema de hoje é: {tema}!")
        acertos = 0
        numero_de_perguntas = 2
        historico = []
        # 2. Gera 5 perguntas uma por uma
        for i in range(0, numero_de_perguntas):
            print(f"\n--- Pergunta {i+1} de {numero_de_perguntas} ---")
            
            prompt = (
                f"Sobre o tema '{tema}', gere a pergunta {i+1} de {numero_de_perguntas}. "
                "Use 3 alternativas (A, B, C) e indique a correta no fim. "
                "O formato da sua resposta deve ser: PERGUNTA ; ALT_A ; ALT_B ; ALT_C ; LETRA_CORRETA"
            )

            response = gerarResposta(historico, prompt=prompt)
            
            partes = response.strip().split(";")

            if len(partes) >= 5:
                print(f"❓ {partes[0].strip()}")
                print(f"A) {partes[1].strip()}\nB) {partes[2].strip()}\nC) {partes[3].strip()}")
                
                resp = input("Sua resposta (A/B/C): ").strip().upper()
                correta = partes[4].strip().upper()

                if resp == correta:
                    print("⭐ ACERTOU!")
                    acertos += 1
                else:
                    print(f"❌ ERROU! A correta era {correta}")
            else:
                print("⚠️ Erro de resposta da IA. Continuando...")

        print(f"\n📊 FINAL: Você acertou {acertos}/{numero_de_perguntas} no tema {tema}.")
        print("Aguardando novo sinal do Arduino...")

    except Exception as e:
        print(f"Erro durante o quiz: {e}")
