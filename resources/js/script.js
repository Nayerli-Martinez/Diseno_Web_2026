// PRODUCTOS

const form = document.getElementById("formProductos");
const lista = document.getElementById("listaProductos");
const mensaje = document.getElementById("mensaje");
const total = document.getElementById("total");

const nombreInput = document.getElementById("nombre");
const descripcionInput = document.getElementById("descripcion");
const categoriaInput = document.getElementById("categoria");

const errorNombre = document.getElementById("errorNombre");
const errorDescripcion = document.getElementById("errorDescripcion");
const errorCategoria = document.getElementById("errorCategoria");

let contador = 0;

// VALIDAR NOMBRE
function validarNombre() {
    const valor = nombreInput.value.trim();

    if (valor === "") {
        errorNombre.textContent = "El nombre es obligatorio.";
        nombreInput.classList.add("is-invalid");
        nombreInput.classList.remove("is-valid");
        return false;
    }

    if (valor.length < 3) {
        errorNombre.textContent = "Mínimo 3 caracteres.";
        nombreInput.classList.add("is-invalid");
        nombreInput.classList.remove("is-valid");
        return false;
    }

    errorNombre.textContent = "";
    nombreInput.classList.remove("is-invalid");
    nombreInput.classList.add("is-valid");
    return true;
}

// VALIDAR DESCRIPCIÓN
function validarDescripcion() {
    const valor = descripcionInput.value.trim();

    if (valor === "") {
        errorDescripcion.textContent = "La descripción es obligatoria.";
        descripcionInput.classList.add("is-invalid");
        descripcionInput.classList.remove("is-valid");
        return false;
    }

    if (valor.length < 10) {
        errorDescripcion.textContent =
            "Debe contener al menos 10 caracteres.";
        descripcionInput.classList.add("is-invalid");
        descripcionInput.classList.remove("is-valid");
        return false;
    }

    errorDescripcion.textContent = "";
    descripcionInput.classList.remove("is-invalid");
    descripcionInput.classList.add("is-valid");
    return true;
}

// VALIDAR CATEGORÍA
function validarCategoria() {

    if (categoriaInput.value === "") {
        errorCategoria.textContent = "Seleccione una categoría.";
        categoriaInput.classList.add("is-invalid");
        categoriaInput.classList.remove("is-valid");
        return false;
    }

    errorCategoria.textContent = "";
    categoriaInput.classList.remove("is-invalid");
    categoriaInput.classList.add("is-valid");
    return true;
}

// EVENTOS EN TIEMPO REAL
nombreInput.addEventListener("input", validarNombre);
nombreInput.addEventListener("blur", validarNombre);

descripcionInput.addEventListener("input", validarDescripcion);
descripcionInput.addEventListener("blur", validarDescripcion);

categoriaInput.addEventListener("change", validarCategoria);
categoriaInput.addEventListener("blur", validarCategoria);

// ENVÍO DEL FORMULARIO
form.addEventListener("submit", function (e) {

    e.preventDefault();

    const nombreValido = validarNombre();
    const descripcionValida = validarDescripcion();
    const categoriaValida = validarCategoria();

    if (!nombreValido || !descripcionValida || !categoriaValida) {

        mensaje.innerHTML =
            '<div class="alert alert-danger">Corrija los campos del formulario.</div>';

        return;
    }

    const nombre = nombreInput.value.trim();
    const descripcion = descripcionInput.value.trim();
    const categoria = categoriaInput.value;

    mensaje.innerHTML =
        '<div class="alert alert-success">Producto agregado correctamente.</div>';

    const li = document.createElement("li");

    li.className =
        "list-group-item d-flex justify-content-between align-items-center";

    li.innerHTML = `
        <div>
            <strong>${nombre}</strong> - ${descripcion}
            <span class="badge bg-info">${categoria}</span>
        </div>
        <button class="btn btn-danger btn-sm eliminar">
            Eliminar
        </button>
    `;

    lista.appendChild(li);

    contador++;
    total.textContent = contador;

    form.reset();

    nombreInput.classList.remove("is-valid");
    descripcionInput.classList.remove("is-valid");
    categoriaInput.classList.remove("is-valid");

    li.querySelector(".eliminar").addEventListener("click", function () {

        lista.removeChild(li);

        contador--;
        total.textContent = contador;
    });
});
// CONTACTO

const formContacto = document.getElementById("formContacto");
const listaContactos = document.getElementById("listaContactos");
const mensajeContactoValidacion = document.getElementById("mensajeContactoValidacion");
const totalContactos = document.getElementById("totalContactos");

const nombreContacto = document.getElementById("nombreContacto");
const correoContacto = document.getElementById("correoContacto");
const mensajeContacto = document.getElementById("mensajeContacto");

const errorNombreContacto = document.getElementById("errorNombreContacto");
const errorCorreoContacto = document.getElementById("errorCorreoContacto");
const errorMensajeContacto = document.getElementById("errorMensajeContacto");

let contadorContactos = 0;

// VALIDAR NOMBRE
function validarNombreContacto() {

    if (nombreContacto.value.trim() === "") {
        errorNombreContacto.textContent = "El nombre es obligatorio.";
        nombreContacto.classList.add("is-invalid");
        nombreContacto.classList.remove("is-valid");
        return false;
    }

    errorNombreContacto.textContent = "";
    nombreContacto.classList.remove("is-invalid");
    nombreContacto.classList.add("is-valid");
    return true;
}

// VALIDAR CORREO
// VALIDAR CORREO
function validarCorreoContacto() {

    const correo = correoContacto.value.trim();

    if (correo === "") {
        errorCorreoContacto.textContent = "El correo es obligatorio.";
        correoContacto.classList.add("is-invalid");
        correoContacto.classList.remove("is-valid");
        return false;
    }

    const formatoCorreo = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    if (!formatoCorreo.test(correo)) {
        errorCorreoContacto.textContent =
            "Ingrese un correo válido. Ejemplo: usuario@gmail.com";
        correoContacto.classList.add("is-invalid");
        correoContacto.classList.remove("is-valid");
        return false;
    }

    errorCorreoContacto.textContent = "";
    correoContacto.classList.remove("is-invalid");
    correoContacto.classList.add("is-valid");
    return true;
}

// VALIDAR MENSAJE
function validarMensajeContacto() {

    if (mensajeContacto.value.trim() === "") {
        errorMensajeContacto.textContent = "El mensaje es obligatorio.";
        mensajeContacto.classList.add("is-invalid");
        mensajeContacto.classList.remove("is-valid");
        return false;
    }

    errorMensajeContacto.textContent = "";
    mensajeContacto.classList.remove("is-invalid");
    mensajeContacto.classList.add("is-valid");
    return true;
}

// EVENTOS
nombreContacto.addEventListener("input", validarNombreContacto);
nombreContacto.addEventListener("blur", validarNombreContacto);

correoContacto.addEventListener("input", validarCorreoContacto);
correoContacto.addEventListener("blur", validarCorreoContacto);

mensajeContacto.addEventListener("input", validarMensajeContacto);
mensajeContacto.addEventListener("blur", validarMensajeContacto);

// ENVÍO DEL FORMULARIO
formContacto.addEventListener("submit", function (e) {

    e.preventDefault();

    const nombreValido = validarNombreContacto();
    const correoValido = validarCorreoContacto();
    const mensajeValido = validarMensajeContacto();

    if (!nombreValido || !correoValido || !mensajeValido) {

        mensajeContactoValidacion.innerHTML =
            '<div class="alert alert-danger">Todos los campos son obligatorios.</div>';

        return;
    }

    mensajeContactoValidacion.innerHTML =
        '<div class="alert alert-success">Contacto registrado correctamente.</div>';

    const li = document.createElement("li");

    li.className =
        "list-group-item d-flex justify-content-between align-items-center";

    li.innerHTML = `
        <div>
            <strong>${nombreContacto.value}</strong> - ${correoContacto.value}
            <p>${mensajeContacto.value}</p>
        </div>
        <button class="btn btn-danger btn-sm eliminar">
            Eliminar
        </button>
    `;

    listaContactos.appendChild(li);

    contadorContactos++;
    totalContactos.textContent = contadorContactos;

    formContacto.reset();

    nombreContacto.classList.remove("is-valid");
    correoContacto.classList.remove("is-valid");
    mensajeContacto.classList.remove("is-valid");

    li.querySelector(".eliminar").addEventListener("click", function () {

        listaContactos.removeChild(li);

        contadorContactos--;
        totalContactos.textContent = contadorContactos;
    });

    
    
});