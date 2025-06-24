// Incluye js-sha256 (https://cdnjs.cloudflare.com/ajax/libs/js-sha256/0.9.0/sha256.min.js)
// Puedes descargar el archivo y ponerlo en static/sha256.min.js, o usar CDN en index.html

// Pipeline JS simplificado: XOR global + salt + hash SHA256 (sin PNG ni fragmentación)

// Polyfill sha256 usando js-sha256
function sha256(text) {
    return sha256_lib(text); // sha256_lib es la función importada de js-sha256
}

function generarSalt(longitud = 8) {
    const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    let salt = '';
    for (let i = 0; i < longitud; i++) {
        salt += chars.charAt(Math.floor(Math.random() * chars.length));
    }
    return salt;
}

function xorConClave(texto, clave) {
    let res = '';
    for (let i = 0; i < texto.length; i++) {
        res += String.fromCharCode(texto.charCodeAt(i) ^ clave.charCodeAt(i % clave.length));
    }
    return res;
}

function base64encode(str) {
    return btoa(unescape(encodeURIComponent(str)));
}
function base64decode(str) {
    return decodeURIComponent(escape(atob(str)));
}

// Cifrado pipeline
async function cifrar_pipeline_js(mensaje, clave, usuario) {
    const salt = generarSalt(8);
    const limpio_con_salt = salt + mensaje;
    const xor = xorConClave(limpio_con_salt, clave);
    const cifrado = base64encode(xor);
    const hash = sha256(mensaje);
    const metadatos = { salt, hash };
    return { cifrado, metadatos };
}

// Descifrado pipeline
async function descifrar_pipeline_js(cifrado, clave, usuario, metadatos) {
    const xor = base64decode(cifrado);
    const limpio_con_salt = xorConClave(xor, clave);
    const salt = metadatos.salt;
    if (!limpio_con_salt.startsWith(salt)) throw new Error('Salt incorrecto o clave incorrecta');
    const limpio = limpio_con_salt.slice(salt.length);
    const hash = sha256(limpio);
    if (hash !== metadatos.hash) throw new Error('Hash de verificación no coincide');
    return limpio;
} 