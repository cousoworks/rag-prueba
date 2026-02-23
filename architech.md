# Arquitectura del Proyecto RAG (Chatbot Corporativo)

## 🎯 Objetivo
Crear un sistema RAG (Retrieval-Augmented Generation) 100% gratuito para chatear con documentos PDF complejos, desplegable en la nube sin costes.

## 🛠️ Stack Tecnológico
- **Frontend:** React + TypeScript.
- **Backend:** Django + Django REST Framework.
- **Base de Datos:** PostgreSQL con extensión `pgvector` (pensado para desplegar en Supabase o Neon.tech).
- **IA y Orquestación:** Python + `langchain`.
- **Embeddings (Vectorización):** `HuggingFaceEmbeddings` (modelo `all-MiniLM-L6-v2`) - Local y 100% gratis.
- **LLM (Generación):** API de Groq (modelo Llama 3) - Rápido y con capa gratuita.

## ⚠️ Reglas Estrictas para la IA (TÚ)
1. **Paso a paso:** NUNCA escribas todo el código de golpe. Dime las cosas de una en una.
2. **Cero costes:** Todo el código debe estar pensado para usar alternativas gratuitas. PROHIBIDO usar la API de OpenAI a menos que el usuario lo pida explícitamente.
3. **Contexto:** Antes de sugerir una solución compleja, revisa este archivo para no salirte del stack tecnológico.
4. **Calidad:** El código debe estar comentado en español, ser modular y manejar los errores básicos.

## 📍 Fases del Proyecto
- [ ] **Fase 1:** Setup inicial (Entorno virtual, inicializar Django, instalar dependencias).
- [ ] **Fase 2:** Pipeline de Datos (Leer el PDF de la carpeta `/documentos`, hacer chunking, vectorizar con HuggingFace y probar en local).
- [ ] **Fase 3:** Conexión a Base de Datos (Configurar PostgreSQL con pgvector y guardar los vectores).
- [ ] **Fase 4:** API RAG (Endpoint en Django que reciba la pregunta, busque vectores similares, llame a Groq con LangChain y devuelva la respuesta).
- [ ] **Fase 5:** Frontend en React.

## 🔄 Estado Actual
Iniciando proyecto. El usuario acaba de meter el PDF en la carpeta `/documentos` y ha creado este archivo.