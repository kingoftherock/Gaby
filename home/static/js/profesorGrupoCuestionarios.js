
function cambiar_preguntas(){
	contenido = document.getElementById("Preguntas_aplicar");
	boton = document.getElementById("cambiar_preguntas");
	numero = document.getElementById("numero_Preguntas").value;
    numero2 = document.getElementById("preguntas_input");
    contenido.innerHTML =
        "<input type='text' id='input_cambiar' name='input_cambio_preguntas' value='"+numero+"'>"+
        "<input type='submit' value='Listo' id='cambiar_algo'>";
    forma = document.getElementById("primero_form");
    forma.style.display = "inline";
    forma.style.width = "400px";
    forma.style.marginLeft = "95px";
    preguntas = document.getElementById("Preguntas");
    preguntas.style.width = "400px";
    contenido.style.display = "inline";
    contenido.style.width = "400px";
    numero2.style.width = "400px";
    boton.style.display = "none";
    }