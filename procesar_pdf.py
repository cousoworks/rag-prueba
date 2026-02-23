import os
import django

# 1. Configurar el entorno de Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from chatbot.models import DocumentoChunk # noqa: E402
from langchain_community.document_loaders import PyPDFLoader # noqa: E402
from langchain_text_splitters import RecursiveCharacterTextSplitter # noqa: E402 
from langchain_huggingface import HuggingFaceEmbeddings # noqa: E402

print("🚀 Iniciando el proceso de carga OPTIMIZADA en Supabase...")

# 2. Cargamos el PDF
loader = PyPDFLoader("documentos/estatuto.pdf")
documents = loader.load()

# OPTIMIZACIÓN: Saltamos las primeras páginas si son solo índices (ej. las primeras 10)
# Si sabes que el texto real empieza en la pág 15, podrías filtrar:
# documents = [doc for doc in documents if doc.metadata["page"] > 15]

# Partimos el texto con trozos más grandes
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1500,         # Trozos más grandes para dar contexto
    chunk_overlap=300,       # Solapamiento para no perder el hilo
    separators=["\n\n", "\n", ". ", " ", ""] # Prioridad de corte natural
)
chunks = text_splitter.split_documents(documents)

# 3. Inicializamos el modelo de embeddings
print("📥 Cargando modelo de IA en memoria...")
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# 4. Guardamos en la BD
total = len(chunks)
print(f"📦 Total de trozos optimizados a subir: {total}")

for idx, chunk in enumerate(chunks, start=1):
    # Generamos el vector
    vector = embeddings.embed_query(chunk.page_content)

    # Guardamos (ahora cada trozo es más rico en información)
    DocumentoChunk.objects.create(
        nombre_archivo="estatuto.pdf",
        contenido=chunk.page_content,
        embedding=vector
    )

    if idx % 50 == 0 or idx == total:
        print(f"✅ Procesados {idx}/{total} chunks...")

print("\n🎉 ¡LISTO! Base de datos actualizada con contenido de alta calidad.")