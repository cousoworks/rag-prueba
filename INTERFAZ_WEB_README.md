# 🏛️ Consultor Legal IA - Interfaz Web

## Descripción

Una interfaz web moderna para tu chatbot RAG que responde preguntas sobre el Estatuto de los Trabajadores español. Funciona como un chat estilo ChatGPT.

## Características

✅ Interfaz moderna y responsiva estilo ChatGPT  
✅ Búsqueda de contexto en documentos legales usando embeddings (RAG)  
✅ Respuestas generadas con IA (Groq LLM)  
✅ Historial de conversaciones  
✅ Modo oscuro/claro automático  
✅ Ejemplos predefinidos  

## Instalación y Ejecución

### 1. Asegúrate de que tienes todas las dependencias instaladas:

```bash
pip install django langchain-huggingface langchain-groq pgvector dj-database-url python-dotenv
```

### 2. Ejecuta el servidor Django:

```bash
python manage.py runserver
```

O simplemente:

```bash
python run.py
```

### 3. Abre tu navegador en:

```
http://localhost:8000
```

## Estructura de Archivos

```
proyecto_rag/
├── static/
│   ├── index.html           # Página HTML (obsoleta, ver templates/)
│   ├── styles.css           # Estilos CSS
│   └── script.js            # JavaScript del cliente
├── chatbot/
│   ├── templates/chatbot/
│   │   └── index.html       # Plantilla Django (LA QUE SE UTILIZA)
│   ├── views.py             # API endpoint y vistas
│   ├── models.py            # Modelos de BD
│   └── ...
├── core/
│   ├── settings.py          # Configuración Django
│   ├── urls.py              # Rutas
│   └── ...
└── manage.py
```

## API Endpoints

### 1. Página Principal

- **GET** `/` → Carga la interfaz del chat

### 2. API de Consultas

- **POST** `/api/consultar/`

**Request:**
```json
{
    "pregunta": "¿Qué dice el Artículo 82?",
    "conversacion": []
}
```

**Response:**
```json
{
    "respuesta": "El artículo 82 se refiere a...",
    "error": null
}
```

## Cómo Funciona

1. El usuario escribe una pregunta en la web
2. JavaScript envía la pregunta a `/api/consultar/`
3. Django:
   - Genera un embedding de la pregunta con HuggingFace
   - Busca los 20 chunks más similares en la BD (usando pgvector)
   - Construye un prompt con el contexto
   - Envía el prompt a Groq LLM
4. La respuesta se muestra en el chat

## Requisitos

- Python 3.8+
- Django 6.0+
- Supabase con pgvector configurado
- API key de Groq en `.env`
- Las tablas de base de datos ya deben estar pobladas con DocumentoChunk

## Solución de Problemas

### Error: "No se encontraron referencias en los documentos"

- Asegúrate de que la tabla `DocumentoChunk` está poblada
- Verifica que los embeddings se almacenaron correctamente

### Error: "API key de Groq no encontrada"

- Comprueba que tienes `GROQ_API_KEY` en tu archivo `.env`

### CSS no carga

- Verifica que está en `static/styles.css`
- En caso contrario, ejecuta: `python manage.py collectstatic`

## Desarrollo

Para agregar más características o modificar estilos:

- **CSS**: Edita `static/styles.css`
- **HTML**: Edita `chatbot/templates/chatbot/index.html`
- **JavaScript**: Edita `static/script.js`
- **Backend**: Edita `chatbot/views.py`

## Licencia

Este proyecto utiliza modelos de IA mediante APIs de terceros.
