import fitz
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
import os

embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
db = FAISS.from_texts([], embedding_model)

def extrair_texto_pdf(pdf_path):
    """Extrai texto de um PDF usando PyMuPDF."""
    texto = ""
    doc = fitz.open(pdf_path)
    for pagina in doc:
        texto += pagina.get_text("text") + "\n"
    return texto

def processar_pdfs():
    """Lê PDFs do diretório e adiciona ao banco vetorial."""
    documentos = []
    for arquivo in os.listdir("documentos_pdfs"):
        if arquivo.endswith(".pdf"):
            caminho = os.path.join("documentos_pdfs", arquivo)
            texto = extrair_texto_pdf(caminho)
            documentos.append(texto)
    db.add_texts(documentos)

def buscar_resposta_rag(pergunta):
    """Busca informações nos documentos antes de responder."""
    resultados = db.similarity_search(pergunta, k=3)
    contexto = "\n".join([r.page_content for r in resultados])
    return contexto
