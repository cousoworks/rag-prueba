import os
import django
from dotenv import load_dotenv

# 1. Configurar Django y variables de entorno
load_dotenv()
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

# Importaciones necesarias
from chatbot.models import DocumentoChunk # noqa: E402
from pgvector.django import CosineDistance # <--- CAMBIO: Usamos CosineDistance
from langchain_huggingface import HuggingFaceEmbeddings # noqa: E402
from langchain_groq import ChatGroq # noqa: E402
from langchain_core.messages import SystemMessage, HumanMessage # noqa: E402

def realizar_consulta(pregunta):
    print(f"\n🤔 Pregunta: {pregunta}")
    
    # 2. Generar embedding de la pregunta
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vector_pregunta = embeddings.embed_query(pregunta)

    # 3. Buscar en Supabase (RAG)
    print("📖 Buscando contexto legal en Supabase...")
    
    # Cambiamos L2Distance por CosineDistance y subimos a 20 trozos
    chunks = DocumentoChunk.objects.annotate(
        distancia=CosineDistance('embedding', vector_pregunta)
    ).order_by('distancia')[:20] 

    if not chunks:
        print("⚠️ No se encontraron trozos de texto en la base de datos.")
        return

    # --- AUDITORÍA ---
    contexto = ""
    print("\n--- 🔍 TEXTO RECUPERADO (Top 20) ---")
    for i, c in enumerate(chunks, 1):
        resumen = c.contenido.replace('\n', ' ')[:100]
        print(f"[{i}] {resumen}...")
        contexto += c.contenido + "\n\n"
    print("-----------------------------------------------\n")

    # 4. Generar respuesta con Groq
    api_key_str = os.getenv("GROQ_API_KEY") or ""
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        api_key=api_key_str,  # type: ignore
        temperature=0
    )

    mensajes = [
        SystemMessage(content="""Eres un abogado experto español. Analiza los fragmentos del Estatuto de los Trabajadores que te proporciono.
        IMPORTANTE: Si la respuesta no está en el texto, di que no lo encuentras en estos fragmentos específicos, pero no inventes artículos si no aparecen.
        Si encuentras el artículo (ej. Art. 59 o Art. 38), cítalo textualmente."""),
        HumanMessage(content=f"Contexto: {contexto}\n\nPregunta: {pregunta}")
    ]

    respuesta = llm.invoke(mensajes)
    print("\n⚖️ RESPUESTA DEL ABOGADO IA:")
    print(respuesta.content)

if __name__ == "__main__":
    # Vamos a probar con el Artículo 82 que sabemos que "asomó" antes
    # O si prefieres, vuelve a poner la de las vacaciones
    pregunta_prueba = "¿Qué dice el Artículo 82?"
    realizar_consulta(pregunta_prueba)