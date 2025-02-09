import requests
import os

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

def perguntar_deepseek(pergunta, contexto=""):
    """Faz uma requisição para a API do DeepSeek e retorna a resposta."""
    url = "https://api.deepseek.com/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "Você é um assistente para um professor universitário."},
            {"role": "user", "content": f"Pergunta: {pergunta}\nContexto: {contexto}"}
        ],
        "max_tokens": 500,
        "temperature": 0.7
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response_data = response.json()

        # 🔥 Adiciona logs para debug
        print("🔵 Resposta da API do DeepSeek:", response_data)

        # Verifica se a resposta contém 'choices'
        if "choices" not in response_data or not response_data["choices"]:
            return f"Erro: Resposta inesperada da API do DeepSeek: {response_data}"

        return response_data["choices"][0]["message"]["content"]

    except requests.exceptions.RequestException as e:
        return f"Erro ao acessar a API do DeepSeek: {e}"
