# Proyecto RAG (Chatbot corporativo)

Este repositorio contiene un backend Django orientado a crear un sistema **Retrieval-Augmented Generation** (RAG) que permite chatear con el contenido de documentos PDF.

---

## 📁 Estructura básica

- `core/` – Configuración del proyecto Django (settings, urls, wsgi, asgi).
- `chatbot/` – Aplicación principal con el modelo `DocumentoChunk` que almacena los fragmentos vectorizados.
- `procesar_pdf.py` – Script independiente para convertir un PDF de `documentos/` en ``chunks`` y guardar sus embeddings en la base de datos.
- `test_chat.py` – Script de prueba que toma una pregunta, busca los trozos más similares en la BD y usa el LLM de Groq para generar una respuesta.
- `documentos/` – Carpeta donde se coloca el PDF a procesar (ej. `estatuto.pdf`).
- `manage.py` – Utilidad de Django para comandos habituales.
- `architech.md` – Documento con la visión y reglas de arquitectura del proyecto.

---

## ⚙️ Tecnología y dependencias

- **Backend**: Django 6 + Django REST Framework (aún no usado).
- **Base de datos**: PostgreSQL con `pgvector` para almacenar embeddings vectoriales.
- **Embeddings**: HuggingFace `all-MiniLM-L6-v2` (modelo local y gratuito).
- **LLM**: API de *Groq* (`llama-3.3-70b-versatile`) para generación de texto.
- **Carga de PDF**: `langchain-community` y `langchain_text_splitters`.

> El stack está pensado para ser gratuito y desplegable en plataformas como Supabase o Neon.tech.

---

## 🚀 Flujo de trabajo principal

1. **Configurar el entorno**: crear un virtualenv, instalar dependencias y apuntar `DATABASE_URL` y `GROQ_API_KEY` en un `.env`.
2. **Inicializar Django**: ejecutar `python manage.py migrate` para preparar la tabla `DocumentoChunk`.
3. **Procesar un PDF**:
   ```bash
   python procesar_pdf.py
   ```
   El script lee `documentos/estatuto.pdf`, lo fragmenta en trozos grandes, genera embeddings y los guarda en la BD.
4. **Probar la consulta**:
   ```bash
   python test_chat.py
   ```
   Hace una consulta de ejemplo (`¿Qué dice el Artículo 82?`), recupera los 20 chunks más cercanos y pregunta al modelo de Groq.

Los scripts pueden adaptarse para integrarlos en views o endpoints REST más adelante.

---

## 📌 Detalles clave

- `DocumentoChunk` almacena el nombre del archivo, el texto y un vector de dimensión 384.
- `test_chat.py` usa `pgvector` con `CosineDistance` para ordenar los fragmentos.
- Los prompts del LLM especifican que actúe como un abogado español y que cite literalmente si encuentra artículos legales.

---

## 📝 Próximos pasos sugeridos

1. **Añadir endpoints** en Django para subir PDFs y consultar mediante la API.
2. **Frontend React/TS** que permita al usuario chatear con los documentos.
3. **Persistir vectores en la base de datos** y opcionalmente usar Supabase.
4. **Control de errores y validaciones** en los scripts.

---

Este README es un resumen para entender rápidamente qué hace el proyecto y cómo empezar a usarlo. Para más detalles técnicos, revisa `architech.md`.
# rag-prueba
