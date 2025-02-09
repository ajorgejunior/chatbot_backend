import fitz
import os
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings


# Inicializa o modelo de embeddings
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
db = None  # O banco vetorial será criado apenas se houver textos extraídos

def extrair_texto_pdf(pdf_path):
    """Extrai texto de um PDF usando PyMuPDF."""
    texto = ""
    try:
        doc = fitz.open(pdf_path)
        for pagina in doc:
            texto += pagina.get_text("text") + "\n"
    except Exception as e:
        print(f"Erro ao processar o PDF {pdf_path}: {e}")
    return texto

def processar_pdfs():
    """Lê PDFs do diretório e retorna os textos extraídos."""
    documentos = []
    diretorio = "documentos_pdfs"

    # Criar o diretório se ele não existir
    if not os.path.exists(diretorio):
        print(f"⚠️ Diretório `{diretorio}` não encontrado! Criando...")
        os.makedirs(diretorio)
    
    arquivos_pdf = [f for f in os.listdir(diretorio) if f.endswith(".pdf")]

    if not arquivos_pdf:
        print("⚠️ Nenhum PDF encontrado no diretório `documentos_pdfs`.")
        return []  # Retorna lista vazia se não houver PDFs

    for arquivo in arquivos_pdf:
        caminho = os.path.join(diretorio, arquivo)
        texto = extrair_texto_pdf(caminho)
        if texto.strip():  # Evita adicionar arquivos vazios
            documentos.append(texto)

    return documentos

def inicializar_banco_vetorial():
    """Inicializa o banco vetorial FAISS apenas se houver textos processados."""
    global db
    textos = processar_pdfs()
    if textos:
        db = FAISS.from_texts(textos, embedding_model)
        print("✅ Banco vetorial criado com sucesso!")
    else:
        db = None
        print("⚠️ Nenhum texto carregado. O banco vetorial não foi inicializado.")

def buscar_resposta_rag(pergunta):
    """Busca informações nos documentos antes de responder."""
    if db is None:
        print("⚠️ Banco vetorial não inicializado. Retornando resposta vazia.")
        return "Nenhum documento carregado para responder à pergunta."

    resultados = db.similarity_search(pergunta, k=3)
    if not resultados:
        return "Nenhuma informação relevante encontrada nos documentos."

    contexto = "\n".join([r.page_content for r in resultados])
    return contexto

# Inicializar FAISS ao carregar o módulo
inicializar_banco_vetorial()
