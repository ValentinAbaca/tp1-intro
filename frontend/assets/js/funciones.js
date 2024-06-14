export const renderizar_personajes = (grilla, personajes) => {
  let esqueleto_contenedor = "";
  for (const personaje of personajes) {
    esqueleto_contenedor += `
            <img
              src="${personaje.imagen}"
              alt="${personaje.nombre}"
              data-id="${personaje.id}"
              class="grillaPersonajes__thumbnail"
            />
          `;
  }
  grilla.innerHTML = esqueleto_contenedor;
};

/**
 * Asigna el valor de el atributo 'data-id' del target el evento al parámetro 'id' .
 *
 * @param {Event} event - El objeto event.
 * @param {number} id - El ID a asignarle a el atributo 'data-id'.
 * @return {void} La función no devuelve ningun valor.
 */
export const obtener_id_personaje = (icono_personaje) => {
  return parseInt(icono_personaje.getAttribute("data-id"));
};

/**
 * Actualiza el contenedor con los datos del personaje proporcionados.
 *
 * @param {HTMLElement} contenedor - El elemento contenedor que se actualizará.
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
 * Setea los query strings para la ruta dada and con los IDs de personajes, y actualiza el href del botón.
 *
 * @param {HTMLElement} boton - El boton a actualizar.
 * @param {string} route - La ruta base para construir la URL.
 * @param {number} id_personaje_1 - El ID del primer personaje.
 * @param {number} id_personaje_2 - El ID del segundo personaje.
 * @return {void} La función no devuelve ningun valor.
 */
export const navegar_pagina = (route, id_personaje_1, id_personaje_2) => {
  const url = `${route}?personaje_1=${id_personaje_1}&personaje_2=${id_personaje_2}`;
  location.assign(url);
};

export const actualizar_texto = (contenedor, texto) => {
  contenedor.innerText = texto;
};

export const marcar_seleccion = (grilla_personajes, id_personaje_elegido) => {
  const icono_personaje = grilla_personajes.querySelector(
    `[data-id="${id_personaje_elegido}"]`
  );
  icono_personaje.classList.add("grillaPersonajes__thumbnail--selected");
};

export const desmarcar_seleccion = (
  grilla_personajes,
  id_personaje_elegido
) => {
  const icono_personaje = grilla_personajes.querySelector(
    `[data-id="${id_personaje_elegido}"]`
  );
  icono_personaje.classList.remove("grillaPersonajes__thumbnail--selected");
};

export const deshabilitar_boton = (boton) => {
  boton.disabled = true;
};
export const habilitar_boton = (boton) => {
  boton.disabled = false;
};

export const fetch_personajes = async () => {
  try {
    let data = await fetch("http://localhost:5000/personajes");
    if (data?.ok) {
      data = await data.json();
      return data;
    }
    if (data?.status === 500) {
      throw new Error(data.data.message);
    }
  } catch (error) {
    console.log(error);
  }
};
