/**
 * Renderiza la lista de personajes dada en el elemento de contenedor especificado.
 *
 * @param {HTMLDivElement} grilla - El elemento de contenedor donde se renderizarán los personajes.
 * @param {Array<Object>} personajes - La lista de personajes a renderizar.
 * @return {void} Esta función no devuelve nada.
 */
export const renderizar_personajes = (grilla, personajes) => {
  const COLUMNAS = 5;
  const FILAS = Math.ceil(personajes.length / 5);
  let indice_personaje = 0;
  for (let i = 0; i < FILAS; i++) {
    let esqueleto_fila = "";
    const fila = document.createElement("div");
    fila.classList.add("grillaPersonajes__fila", "h-100", "w-100", "d-flex");
    let j = 0;
    while(j < COLUMNAS && indice_personaje < personajes.length) {
      const personaje = personajes[indice_personaje];
      esqueleto_fila += `
              <img
                src="${personaje.imagen}"
                alt="${personaje.nombre}"
                data-id="${personaje.id}"
                class="grillaPersonajes__thumbnail"
              />
             
            `;
      j++;
      indice_personaje++;
    }
    fila.innerHTML = esqueleto_fila;
    grilla.appendChild(fila);
  }
};

/**
 * Devuelve el ID de un personaje a partir del elemento icono_personaje dado.
 *
 * @param {HTMLImageElement} icono_personaje - El elemento icono_personaje del cual se obtendrá el ID.
 * @return {number} El ID del personaje.
 */
export const obtener_id_personaje = (icono_personaje) => {
  return parseInt(icono_personaje.getAttribute("data-id"));
};

/**
 * Actualiza el contenedor con los datos del personaje proporcionados.
 *
 * @param {HTMLDivElement} contenedor - El elemento contenedor que se actualizará.
 * @param {Object} datos_personaje - Los datos del personaje a mostrar.
 * @return {void} Esta función no devuelve un valor.
 */
export const actualizar_contenedor_personaje = (contenedor, personaje) => {
  const name = contenedor.querySelector(".personajes__nombre");
  const imagen = contenedor.querySelector(".personajes__img");
  imagen.src = personaje.imagen;
  imagen.alt = personaje.nombre;
  name.innerText = personaje.nombre;
};

/**
 * Navega a una nueva página con los parámetros de los personajes seleccionados.
 *
 * @param {string} route - La ruta base de la página a la que se quiere navegar.
 * @param {string} id_personaje_1 - El ID del primer personaje.
 * @param {string} id_personaje_2 - El ID del segundo personaje.
 */
export const navegar_pagina = (route, id_personaje_1, id_personaje_2) => {
  const url = `${route}?personaje_1=${id_personaje_1}&personaje_2=${id_personaje_2}`;
  location.assign(url);
};

/**
 * Actualiza el texto de un contenedor.
 *
 * @param {HTMLElement} contenedor - El elemento HTML cuyo texto se va a actualizar.
 * @param {string} texto - El nuevo texto a establecer en el contenedor.
 */
export const actualizar_texto = (contenedor, texto) => {
  contenedor.innerText = texto;
};

/**
 * Marca un personaje como seleccionado en una grilla de personajes.
 *
 * @param {HTMLDivElement} grilla_personajes - El contenedor de la grilla de personajes.
 * @param {string} id_personaje_elegido - El ID del personaje a marcar como seleccionado.
 */
export const marcar_seleccion = (grilla_personajes, id_personaje_elegido) => {
  const icono_personaje = grilla_personajes.querySelector(
    `[data-id="${id_personaje_elegido}"]`
  );
  icono_personaje.classList.add("grillaPersonajes__thumbnail--selected");
};

/**
 * Desmarca un personaje como seleccionado en una grilla de personajes.
 *
 * @param {HTMLDivElement} grilla_personajes - El contenedor de la grilla de personajes.
 * @param {string} id_personaje_elegido - El ID del personaje a desmarcar como seleccionado.
 */
export const desmarcar_seleccion = (
  grilla_personajes,
  id_personaje_elegido
) => {
  const icono_personaje = grilla_personajes.querySelector(
    `[data-id="${id_personaje_elegido}"]`
  );
  icono_personaje.classList.remove("grillaPersonajes__thumbnail--selected");
};

/**
 * Deshabilita un botón.
 *
 * @param {HTMLButtonElement} boton - El botón a deshabilitar.
 */
export const deshabilitar_boton = (boton) => {
  boton.disabled = true;
};

/**
 * Habilita un botón.
 *
 * @param {HTMLButtonElement} boton - El botón a habilitar.
 */
export const habilitar_boton = (boton) => {
  boton.disabled = false;
};

export const fetch_personajes = async () => {
  let personajes;
  await fetch("http://localhost:5000/personajes")
    .then((response) => {
      return response.json();
    })
    .then((response) => {
      if (response.length > 0) {
        personajes = response;
      } else {
        throw new Error(response.message);
      }
    })
    .catch((error) => {
      location.assign("/");
      alert(error);
    });
  return personajes;
};
