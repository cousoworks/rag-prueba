import json
import os
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.staticfiles.views import serve
from django.conf import settings

from chatbot.models import DocumentoChunk
from pgvector.django import CosineDistance
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage


def index(request):
    """Servir la página principal de chat"""
    return render(request, 'chatbot/index.html')


@require_http_methods(["GET"])
def static_files(request, path):
    """Servir archivos estáticos"""
    return serve(request, path, document_root=os.path.join(settings.BASE_DIR, 'static'))


@csrf_exempt
@require_http_methods(["POST"])
def consultar_api(request):
    """
    API endpoint para procesar preguntas sobre los estatutos
    
    Espera:
    {
        "pregunta": "¿Qué dice el Artículo 82?",
        "conversacion": []
    }
    
    Retorna:
    {
        "respuesta": "El artículo 82...",
        "error": null
    }
    """
    try:
        # Parsear JSON
        data = json.loads(request.body)
        pregunta = data.get('pregunta', '').strip()
        
        if not pregunta:
            return JsonResponse({
                'respuesta': None,
                'error': 'Por favor, escribe una pregunta.'
            }, status=400)
        
        # Realizar la consulta
        respuesta = realizar_consulta(pregunta)
        
        return JsonResponse({
            'respuesta': respuesta,
            'error': None
        })
    
    except json.JSONDecodeError:
        return JsonResponse({
            'respuesta': None,
            'error': 'Error al procesar la solicitud.'
        }, status=400)
    except Exception as e:
        print(f"Error en la consulta: {str(e)}")
        return JsonResponse({
            'respuesta': None,
            'error': f'Error al procesar tu pregunta: {str(e)}'
        }, status=500)


def realizar_consulta(pregunta):
    """
    Realiza una consulta al sistema RAG utilizando embeddings y Groq
    
    Args:
        pregunta (str): Pregunta del usuario
        
    Returns:
        str: Respuesta del LLM
    """
    # 1. Generar embedding de la pregunta
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vector_pregunta = embeddings.embed_query(pregunta)

    # 2. Buscar en la base de datos (RAG)
    chunks = DocumentoChunk.objects.annotate(
        distancia=CosineDistance('embedding', vector_pregunta)
    ).order_by('distancia')[:20]

    if not chunks:
        return "No se encontraron referencias en los documentos disponibles. Por favor, intenta con otra pregunta."

    # 3. Construir contexto
    contexto = ""
    for chunk in chunks:
        contexto += chunk.contenido + "\n\n"

    # 4. Generar respuesta con Groq
    api_key_str = os.getenv("GROQ_API_KEY") or ""
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        api_key=api_key_str,
        temperature=0
    )

    mensajes = [
        SystemMessage(content="""Eres un abogado experto español. Analiza los fragmentos del Estatuto de los Trabajadores que te proporciono.
        IMPORTANTE: Si la respuesta no está en el texto, di que no lo encuentras en estos fragmentos específicos, pero no inventes artículos si no aparecen.
        Si encuentras el artículo (ej. Art. 59 o Art. 38), cítalo textualmente.
        Responde de manera clara y concisa."""),
        HumanMessage(content=f"Contexto: {contexto}\n\nPregunta: {pregunta}")
    ]

    respuesta = llm.invoke(mensajes)
    return respuesta.content
