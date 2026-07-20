
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

const spinner = document.getElementById("spinner");

let productos = [];


// ===============================
// MOSTRAR PRODUCTOS EN CARDS
// ===============================

function mostrarProductos() {

    lista.innerHTML = "";


    if(productos.length === 0){

        lista.innerHTML = `

        <div class="col-12">

            <div class="alert alert-warning text-center">

                No existen productos registrados.

            </div>

        </div>

        `;

        total.textContent = 0;

        return;

    }



    productos.forEach((producto,index)=>{


        lista.innerHTML += `


        <div class="col-md-4">


            <div class="card shadow h-100">


                <div class="card-body">


                    <h5 class="card-title text-success">

                        ${producto.nombre}

                    </h5>



                    <p class="card-text">

                        ${producto.descripcion}

                    </p>



                    <span class="badge bg-info">

                        ${producto.categoria}

                    </span>



                    <div class="mt-3">


                        <button 
                        class="btn btn-danger btn-sm"
                        onclick="eliminarProducto(${index})">


                            Eliminar


                        </button>


                    </div>



                </div>


            </div>


        </div>


        `;


    });


    total.textContent = productos.length;

}



// ===============================
// ELIMINAR PRODUCTO
// ===============================


function eliminarProducto(index){


    productos.splice(index,1);


    mostrarProductos();


    mensaje.innerHTML = `

    <div class="alert alert-danger">

        Producto eliminado.

    </div>

    `;


}


// VALIDAR NOMBRE


function validarNombre(){


    const valor = nombreInput.value.trim();



    if(valor === ""){


        errorNombre.textContent =
        "El nombre es obligatorio.";


        nombreInput.classList.add("is-invalid");


        return false;

    }



    if(valor.length < 3){


        errorNombre.textContent =
        "Mínimo 3 caracteres.";


        nombreInput.classList.add("is-invalid");


        return false;

    }



    errorNombre.textContent="";


    nombreInput.classList.remove("is-invalid");

    nombreInput.classList.add("is-valid");



    return true;


}

// VALIDAR DESCRIPCIÓN


function validarDescripcion(){


    const valor = descripcionInput.value.trim();



    if(valor===""){


        errorDescripcion.textContent =
        "La descripción es obligatoria.";


        descripcionInput.classList.add("is-invalid");


        return false;

    }



    if(valor.length < 10){


        errorDescripcion.textContent =
        "Debe contener al menos 10 caracteres.";


        descripcionInput.classList.add("is-invalid");


        return false;


    }

    errorDescripcion.textContent="";


    descripcionInput.classList.remove("is-invalid");


    descripcionInput.classList.add("is-valid");



    return true;


}

// VALIDAR CATEGORÍA

function validarCategoria(){


    if(categoriaInput.value===""){


        errorCategoria.textContent =
        "Seleccione una categoría.";


        categoriaInput.classList.add("is-invalid");


        return false;

    }



    errorCategoria.textContent="";


    categoriaInput.classList.remove("is-invalid");


    categoriaInput.classList.add("is-valid");


    return true;


}




// EVENTOS

nombreInput.addEventListener("input",validarNombre);

nombreInput.addEventListener("blur",validarNombre);


descripcionInput.addEventListener("input",validarDescripcion);

descripcionInput.addEventListener("blur",validarDescripcion);


categoriaInput.addEventListener("change",validarCategoria);

categoriaInput.addEventListener("blur",validarCategoria);




// GUARDAR PRODUCTO


form.addEventListener("submit",(e)=>{


    e.preventDefault();



    const nombreValido = validarNombre();

    const descripcionValida = validarDescripcion();

    const categoriaValida = validarCategoria();



    if(!nombreValido || !descripcionValida || !categoriaValida){


        mensaje.innerHTML = `

        <div class="alert alert-danger">

        Corrija los campos del formulario.

        </div>

        `;


        return;


    }




    spinner.classList.remove("d-none");



    setTimeout(()=>{



        spinner.classList.add("d-none");



        productos.push({


            nombre:nombreInput.value,

            descripcion:descripcionInput.value,

            categoria:categoriaInput.value


        });



        mostrarProductos();




        mensaje.innerHTML = `


        <div class="alert alert-success alert-dismissible fade show">


        Producto agregado correctamente.


        <button class="btn-close"
        data-bs-dismiss="alert"></button>


        </div>


        `;




        const modal = new bootstrap.Modal(
            document.getElementById("modalProducto")
        );


        modal.show();




        form.reset();



    },1000);



});




mostrarProductos();
// ===============================
// CONTACTO
// ===============================


const formContacto = document.getElementById("formContacto");

const listaContactos = document.getElementById("listaContactos");

const mensajeContactoValidacion =
document.getElementById("mensajeContactoValidacion");

const totalContactos =
document.getElementById("totalContactos");



const nombreContacto =
document.getElementById("nombreContacto");


const correoContacto =
document.getElementById("correoContacto");


const mensajeContacto =
document.getElementById("mensajeContacto");



const errorNombreContacto =
document.getElementById("errorNombreContacto");


const errorCorreoContacto =
document.getElementById("errorCorreoContacto");


const errorMensajeContacto =
document.getElementById("errorMensajeContacto");



let contactos = [];



// ===============================
// MOSTRAR CONTACTOS EN CARDS
// ===============================


function mostrarContactos(){


    listaContactos.innerHTML = "";



    if(contactos.length === 0){


        listaContactos.innerHTML = `

        <div class="col-12">

            <div class="alert alert-info text-center">

                No existen contactos registrados.

            </div>

        </div>

        `;


        totalContactos.textContent = 0;


        return;


    }




    contactos.forEach((contacto,index)=>{



        listaContactos.innerHTML += `


        <div class="col-md-4">


            <div class="card shadow h-100">


                <div class="card-body">


                    <h5 class="card-title text-primary">

                        ${contacto.nombre}

                    </h5>



                    <p class="card-text">

                        <strong>Correo:</strong>

                        ${contacto.correo}

                    </p>



                    <p class="card-text">

                        ${contacto.mensaje}

                    </p>



                    <button

                    class="btn btn-danger btn-sm"

                    onclick="eliminarContacto(${index})">


                        Eliminar


                    </button>



                </div>


            </div>


        </div>


        `;



    });



    totalContactos.textContent = contactos.length;


}

// VALIDAR NOMBRE CONTACTO

function validarNombreContacto(){


    const valor =
    nombreContacto.value.trim();



    if(valor===""){


        errorNombreContacto.textContent =
        "El nombre es obligatorio.";


        nombreContacto.classList.add("is-invalid");


        return false;


    }



    errorNombreContacto.textContent="";


    nombreContacto.classList.remove("is-invalid");

    nombreContacto.classList.add("is-valid");



    return true;


}

// VALIDAR CORREO

function validarCorreoContacto(){


    const correo =
    correoContacto.value.trim();



    const formato =
    /^[^\s@]+@[^\s@]+\.[^\s@]+$/;



    if(correo===""){


        errorCorreoContacto.textContent =
        "El correo es obligatorio.";


        correoContacto.classList.add("is-invalid");


        return false;


    }

    if(!formato.test(correo)){


        errorCorreoContacto.textContent =
        "Ingrese un correo válido.";


        correoContacto.classList.add("is-invalid");


        return false;


    }

    errorCorreoContacto.textContent="";


    correoContacto.classList.remove("is-invalid");


    correoContacto.classList.add("is-valid");



    return true;


}


// VALIDAR MENSAJE

function validarMensajeContacto(){


    const valor =
    mensajeContacto.value.trim();



    if(valor===""){


        errorMensajeContacto.textContent =
        "El mensaje es obligatorio.";


        mensajeContacto.classList.add("is-invalid");


        return false;


    }



    errorMensajeContacto.textContent="";


    mensajeContacto.classList.remove("is-invalid");


    mensajeContacto.classList.add("is-valid");



    return true;


}

// EVENTOS DE VALIDACIÓN

nombreContacto.addEventListener(
"input",
validarNombreContacto
);


nombreContacto.addEventListener(
"blur",
validarNombreContacto
);



correoContacto.addEventListener(
"input",
validarCorreoContacto
);


correoContacto.addEventListener(
"blur",
validarCorreoContacto
);



mensajeContacto.addEventListener(
"input",
validarMensajeContacto
);


mensajeContacto.addEventListener(
"blur",
validarMensajeContacto
);


// ENVIAR CONTACTO

formContacto.addEventListener("submit",(e)=>{


    e.preventDefault();



    const nombreValido =
    validarNombreContacto();


    const correoValido =
    validarCorreoContacto();


    const mensajeValido =
    validarMensajeContacto();




    if(!nombreValido ||
       !correoValido ||
       !mensajeValido){



        mensajeContactoValidacion.innerHTML = `


        <div class="alert alert-danger">


            Complete correctamente todos los campos.


        </div>


        `;


        return;


    }


    contactos.push({


        nombre:
        nombreContacto.value,


        correo:
        correoContacto.value,


        mensaje:
        mensajeContacto.value



    });



    mostrarContactos();




    mensajeContactoValidacion.innerHTML = `


    <div class="alert alert-success alert-dismissible fade show">


        Contacto registrado correctamente.


        <button class="btn-close"
        data-bs-dismiss="alert"></button>


    </div>


    `;


    formContacto.reset();



    nombreContacto.classList.remove("is-valid");

    correoContacto.classList.remove("is-valid");

    mensajeContacto.classList.remove("is-valid");



});


// ELIMINAR CONTACTO


function eliminarContacto(index){


    contactos.splice(index,1);


    mostrarContactos();



    mensajeContactoValidacion.innerHTML = `


    <div class="alert alert-warning">


        Contacto eliminado.


    </div>


    `;


}

mostrarContactos();