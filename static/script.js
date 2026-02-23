// Estado de la conversación
let conversacion = [];
let conversacionHistorial = [];

// Elemento del DOM
const inputPregunta = document.getElementById('pregunta');
const mensajesDiv = document.getElementById('mensajes');
const spinner = document.getElementById('loadingSpinner');

// Enviar pregunta con Enter
function manejarEnter(event) {
    if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        enviarPregunta();
    }
}

// Enviar pregunta
async function enviarPregunta() {
    const pregunta = inputPregunta.value.trim();
    
    if (!pregunta) return;

    // Agregar mensaje del usuario
    agregarMensaje(pregunta, 'user');
    inputPregunta.value = '';
    
    // Mostrar spinner
    spinner.classList.remove('hidden');

    try {
        // Hacer la solicitud al backend
        const response = await fetch('/api/consultar/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': obtenerCSRFToken(),
            },
            body: JSON.stringify({
                pregunta: pregunta,
                conversacion: conversacion
            })
        });

        if (!response.ok) {
            throw new Error(`Error en la solicitud: ${response.statusText}`);
        }

        const data = await response.json();

        // Agregar respuesta del bot
        if (data.respuesta) {
            agregarMensaje(data.respuesta, 'bot');
            
            // Agregar a historial de conversación
            conversacion.push({
                pregunta: pregunta,
                respuesta: data.respuesta
            });

            // Agregar al historial de conversaciones si es primera pregunta
            if (conversacion.length === 1) {
                const titulo = pregunta.substring(0, 30) + (pregunta.length > 30 ? '...' : '');
                conversacionHistorial.push({
                    id: Date.now(),
                    titulo: titulo,
                    conversacion: [...conversacion]
                });
                actualizarHistorial();
            }
        } else if (data.error) {
            agregarMensaje(`Error: ${data.error}`, 'bot');
        }
    } catch (error) {
        console.error('Error:', error);
        agregarMensaje(`Error al procesar la pregunta: ${error.message}`, 'bot');
    } finally {
        // Ocultar spinner
        spinner.classList.add('hidden');
    }
}

// Agregar mensaje al chat
function agregarMensaje(contenido, tipo) {
    const mensaje = document.createElement('div');
    mensaje.className = `message ${tipo}-message`;
    
    const contenedor = document.createElement('div');
    contenedor.className = 'message-content';
    contenedor.innerHTML = contenido;
    
    mensaje.appendChild(contenedor);
    mensajesDiv.appendChild(mensaje);
    
    // Scroll al final
    mensajesDiv.scrollTop = mensajesDiv.scrollHeight;
}

// Obtener token CSRF
function obtenerCSRFToken() {
    const cookieValue = document.cookie
        .split('; ')
        .find(row => row.startsWith('csrftoken='))
        ?.split('=')[1];
    return cookieValue || '';
}

// Nueva conversación
function nuevaConversacion() {
    conversacion = [];
    mensajesDiv.innerHTML = `
        <div class="message bot-message welcome-message">
            <div class="message-content">
                <h2>Bienvenido al Consultor Legal IA</h2>
                <p>Hola, soy tu asesor legal basado en IA. Puedo ayudarte con preguntas sobre el <strong>Estatuto de los Trabajadores</strong> español.</p>
                <p>Algunos ejemplos de preguntas que puedo responder:</p>
                <ul class="suggestions">
                    <li>¿Qué dice el Artículo 82?</li>
                    <li>¿Cuáles son mis derechos como trabajador?</li>
                    <li>¿Qué regulan los artículos sobre vacaciones?</li>
                    <li>¿Cuáles son las causas de extinción del contrato?</li>
                </ul>
            </div>
        </div>
    `;
    inputPregunta.focus();
}

// Actualizar historial de conversaciones
function actualizarHistorial() {
    const historialDiv = document.getElementById('historialConversaciones');
    historialDiv.innerHTML = '';
    
    conversacionHistorial.forEach(conv => {
        const item = document.createElement('div');
        item.className = 'history-item';
        item.textContent = conv.titulo;
        item.onclick = () => cargarConversacion(conv);
        historialDiv.appendChild(item);
    });
}

// Cargar conversación anterior
function cargarConversacion(conv) {
    conversacion = conv.conversacion;
    mensajesDiv.innerHTML = '';
    
    conversacion.forEach(msg => {
        agregarMensaje(msg.pregunta, 'user');
        agregarMensaje(msg.respuesta, 'bot');
    });
    
    inputPregunta.focus();
}

// Hacer que los ejemplos sean clickeables
document.addEventListener('DOMContentLoaded', function() {
    document.addEventListener('click', function(e) {
        if (e.target.matches('.suggestions li')) {
            inputPregunta.value = e.target.textContent;
            inputPregunta.focus();
        }
    });
});
