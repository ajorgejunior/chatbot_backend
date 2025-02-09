import openai
import os

# Obtém a chave da API do OpenAI do ambiente
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def perguntar_chatgpt(pergunta, contexto=""):
    """Faz uma requisição para a API do ChatGPT (OpenAI) usando GPT-3.5 Turbo e retorna a resposta."""
    
    try:
        client = openai.OpenAI(api_key=OPENAI_API_KEY)

        resposta = client.chat.completions.create(
            model="gpt-3.5-turbo",  # 🔥 Mudamos para GPT-3.5 Turbo
            messages=[
                {"role": "system", "content": "Você é um assistente para um professor universitário."},
                {"role": "user", "content": f"Pergunta: {pergunta}\nContexto: {contexto}"}
            ],
            max_tokens=500,
            temperature=0.7
        )

        # Verifica se há resposta
        if not resposta.choices:
            return "Erro: A API do ChatGPT não retornou uma resposta válida."

        return resposta.choices[0].message.content

    except Exception as e:
        return f"Erro ao acessar a API do ChatGPT: {e}"


