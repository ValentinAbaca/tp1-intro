// import { personajes } from "./personajes.js";
import {
  dibujar_grilla_personajes,
  switch_botones,
  obtener_id_personaje,
  actualizar_contendor_personaje,
  setear_query_strings,
  actualizar_texto,
  fetch_personajes,
} from "./funciones.js";

const personajes = await fetch_personajes();

// Referencias HTML
const contenedor_personaje_1 = document.querySelector(".personajes__1");
const contenedor_personaje_2 = document.querySelector(".personajes__2");
const boton_confirmar_pj1 = document.querySelector("#confirmar_personaje_1");
const boton_confirmar_pj2 = document.querySelector("#confirmar_personaje_2");
const boton_iniciar = document.querySelector("#iniciar_juego");
const texto_status = document.querySelector(".personajes__text");

// Variables de estado
let id_personaje_1, id_personaje_2, id_personaje_elegido;

// Inicializar html
actualizar_contendor_personaje(contenedor_personaje_1, personajes[0]);
actualizar_contendor_personaje(contenedor_personaje_2, personajes[1]);
dibujar_grilla_personajes(personajes);
const contenedores_personajes = document.querySelectorAll(
  ".grillaPersonajes__thumbnail--img"
);

// Asignar eventos
for (const contenedor of contenedores_personajes) {
  contenedor.addEventListener(
    "click",
    (event) => (id_personaje_elegido = obtener_id_personaje(event))
  );
}

boton_confirmar_pj1.addEventListener("click", () => {
  id_personaje_1 = id_personaje_elegido;
  id_personaje_elegido = null;
  switch_botones(
    id_personaje_1,
    id_personaje_2,
    boton_confirmar_pj1,
    boton_confirmar_pj2,
    boton_iniciar
  );
  if (id_personaje_1) {
    const personaje = personajes.filter((pj) => pj.id === id_personaje_1)[0];
    actualizar_contendor_personaje(contenedor_personaje_1, personaje);
    actualizar_texto(texto_status, "Jugador 2, escoja su personaje");
  }
});
boton_confirmar_pj2.addEventListener("click", () => {
  id_personaje_2 = id_personaje_elegido;
  id_personaje_elegido = null;
  switch_botones(
    id_personaje_1,
    id_personaje_2,
    boton_confirmar_pj1,
    boton_confirmar_pj2,
    boton_iniciar
  );
  if (id_personaje_1 && id_personaje_2) {
    const personaje = personajes.filter((pj) => pj.id === id_personaje_2)[0];
    actualizar_contendor_personaje(contenedor_personaje_2, personaje);
    actualizar_texto(texto_status, "Personajes Listos. ¡A pelear!");
    setear_query_strings(
      boton_iniciar,
      "./juego.html",
      id_personaje_1,
      id_personaje_2
    );
  }
});
