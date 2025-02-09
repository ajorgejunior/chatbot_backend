import openai
import os

# 🔑 Pegue sua chave da OpenAI e adicione como variável de ambiente
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def perguntar_chatgpt(pergunta, contexto=""):
    """Faz uma requisição ao GPT-3.5 Turbo da OpenAI."""
    
    try:
        resposta = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Você é um assistente que responde com base em documentos fornecidos."},
                {"role": "user", "content": f"Contexto: {contexto}\nPergunta: {pergunta}"}
            ],
            max_tokens=500,
            temperature=0.7
        )

        return resposta["choices"][0]["message"]["content"].strip()

    except Exception as e:
        return f"Erro ao acessar OpenAI: {str(e)}"
