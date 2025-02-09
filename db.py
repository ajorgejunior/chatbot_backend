import psycopg2
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

DB_URL = os.getenv("SUPABASE_DB_URL")

def conectar_db():
    """Estabelece conexão com o banco de dados do Supabase."""
    return psycopg2.connect(DB_URL, sslmode="require")
