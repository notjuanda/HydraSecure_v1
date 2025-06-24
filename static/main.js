let ws = null;
let nombre = '';
let clave = '';

function scrollChat() {
    const mensajes = document.getElementById('mensajes');
    mensajes.scrollTop = mensajes.scrollHeight;
}

function addBurbuja(text, tipo) {
    const div = document.createElement('div');
    div.className = 'burbuja ' + tipo;
    div.textContent = text;
    document.getElementById('mensajes').appendChild(div);
    scrollChat();
}

// Deshabilita input y botón al inicio
window.onload = function() {
    document.getElementById('msg').disabled = true;
    document.querySelector('#form-msg button').disabled = true;
};

document.getElementById('entrar').onclick = function() {
    nombre = document.getElementById('nombre').value.trim();
    clave = document.getElementById('clave').value;
    if (!nombre || !clave) {
        alert('Ingresa tu nombre y clave secreta.');
        return;
    }
    document.getElementById('login').style.display = 'none';
    document.getElementById('chat').style.display = '';
    document.getElementById('user-label').textContent = nombre;
    conectarWS();
};

document.getElementById('salir').onclick = function() {
    if (ws) ws.close();
    document.getElementById('chat').style.display = 'none';
    document.getElementById('login').style.display = '';
    document.getElementById('mensajes').innerHTML = '';
    document.getElementById('nombre').value = '';
    document.getElementById('clave').value = '';
    document.getElementById('msg').disabled = true;
    document.querySelector('#form-msg button').disabled = true;
};

function conectarWS() {
    ws = new WebSocket(`ws://${window.location.host}/ws`);
    ws.onopen = () => {
        addBurbuja('Conectado al chat.', 'sistema');
        document.getElementById('msg').disabled = false;
        document.querySelector('#form-msg button').disabled = false;
    };
    ws.onmessage = async (event) => {
        try {
            const data = JSON.parse(event.data);
            // Solo intentamos descifrar si tenemos la clave
            if (data.cifrado && data.nombre && data.metadatos) {
                let texto = '';
                try {
                    texto = await descifrar_pipeline_js(data.cifrado, clave, data.nombre, data.metadatos);
                } catch (e) {
                    texto = '[Mensaje cifrado: clave incorrecta]';
                }
                addBurbuja(`${data.nombre}: ${texto}`, data.nombre === nombre ? 'emisor' : 'receptor');
            }
        } catch (e) {
            // Mensaje de sistema o error
        }
    };
    ws.onclose = () => {
        addBurbuja('Desconectado.', 'sistema');
        document.getElementById('msg').disabled = true;
        document.querySelector('#form-msg button').disabled = true;
    };
}

document.getElementById('form-msg').onsubmit = async function(e) {
    e.preventDefault();
    const msg = document.getElementById('msg').value.trim();
    if (!msg) return;
    if (!ws || ws.readyState !== 1) {
        addBurbuja('No conectado. Espera a que el chat esté listo.', 'sistema');
        return;
    }
    // Cifra el mensaje antes de enviarlo
    const { cifrado, metadatos } = await cifrar_pipeline_js(msg, clave, nombre);
    ws.send(JSON.stringify({ nombre, cifrado, metadatos }));
    document.getElementById('msg').value = '';
}; 