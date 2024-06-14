import {
  renderizar_personajes,
  obtener_id_personaje,
  actualizar_contenedor_personaje,
  navegar_pagina,
  actualizar_texto,
  marcar_seleccion,
  desmarcar_seleccion,
  habilitar_boton,
  deshabilitar_boton,
  fetch_personajes,
} from "./funciones.js";

const personajes = await fetch_personajes();

// Referencias HTML
const grilla_personajes = document.querySelector(".grillaPersonajes");
const contenedor_personaje_1 = document.querySelector(".personajes__1");
const contenedor_personaje_2 = document.querySelector(".personajes__2");
const boton_confirmar_jugador1 = document.querySelector(
  "#confirmar_personaje_1"
);
const boton_confirmar_jugador2 = document.querySelector(
  "#confirmar_personaje_2"
);
const boton_iniciar = document.querySelector("#iniciar_juego");
const texto_estado = document.querySelector(".personajes__text");
renderizar_personajes(grilla_personajes, personajes);
const iconos_personajes = document.querySelectorAll(
  ".grillaPersonajes__thumbnail"
);

const estado = {
  jugador1: {
    personaje: personajes[0],
    esta_eligiendo: true,
  },
  jugador2: {
    personaje: personajes[1],
    esta_eligiendo: false,
  },
  personaje_seleccionado: null,
};

const confirmar_seleccion_jugador1 = () => {
  if (!(estado.personaje_seleccionado === null)) {
    estado.jugador1.personaje = estado.personaje_seleccionado;
    estado.personaje_seleccionado = null;
  }
  desmarcar_seleccion(grilla_personajes, estado.jugador1.personaje.id);
  actualizar_contenedor_personaje(
    contenedor_personaje_1,
    estado.jugador1.personaje
  );
  actualizar_texto(texto_estado, "Jugador 2, escoja su personaje");
  habilitar_boton(boton_confirmar_jugador2);
  deshabilitar_boton(boton_confirmar_jugador1);
  estado.jugador1.esta_eligiendo = false;
  estado.jugador2.esta_eligiendo = true;
};

const confirmar_seleccion_jugador2 = () => {
  if (!(estado.personaje_seleccionado === null)) {
    estado.jugador2.personaje = estado.personaje_seleccionado;
    estado.personaje_seleccionado = null;
  }
  desmarcar_seleccion(grilla_personajes, estado.jugador2.personaje.id);
  actualizar_contenedor_personaje(
    contenedor_personaje_2,
    estado.jugador2.personaje
  );
  actualizar_texto(texto_estado, "¡Jugadores listos!, ¡Iniciar pelea!");
  deshabilitar_boton(boton_confirmar_jugador2);
  habilitar_boton(boton_iniciar);
  estado.jugador2.esta_eligiendo = false;
};

const seleccionar_personaje = (event) => {
  const icono_personaje = event.target;
  const id_personaje_elegido = obtener_id_personaje(icono_personaje);
  if (estado.personaje_seleccionado !== null) {
    desmarcar_seleccion(grilla_personajes, estado.personaje_seleccionado.id);
  }
  estado.personaje_seleccionado = personajes.filter(
    (personaje) => personaje.id === id_personaje_elegido
  )[0];
  marcar_seleccion(grilla_personajes, id_personaje_elegido);
  if (estado.jugador1.esta_eligiendo) {
    actualizar_contenedor_personaje(
      contenedor_personaje_1,
      estado.personaje_seleccionado
    );
  } else {
    actualizar_contenedor_personaje(
      contenedor_personaje_2,
      estado.personaje_seleccionado
    );
  }
};

const iniciar_juego = () => {
  navegar_pagina(
    "/pages/juego",
    estado.jugador1.personaje.id,
    estado.jugador2.personaje.id
  );
};

// Inicializar html
actualizar_contenedor_personaje(
  contenedor_personaje_1,
  estado.jugador1.personaje
);
actualizar_contenedor_personaje(
  contenedor_personaje_2,
  estado.jugador2.personaje
);

// Asignar eventos
for (const icono_personaje of iconos_personajes) {
  icono_personaje.addEventListener("click", seleccionar_personaje);
}

boton_confirmar_jugador1.addEventListener(
  "click",
  confirmar_seleccion_jugador1
);

boton_confirmar_jugador2.addEventListener(
  "click",
  confirmar_seleccion_jugador2
);

boton_iniciar.addEventListener("click", iniciar_juego);
