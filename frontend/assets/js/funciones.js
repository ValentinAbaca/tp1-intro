/**
 * Renderiza una grilla de personajes en la página web basada en los datos de personajes proporcionados.
 *
 * @param {Array} personajes - Un array de objetos de personajes que contienen imagen, nombre e id.
 * @return {void} Esta función no devuelve un valor.
 */
export const dibujar_grilla_personajes = (personajes) => {
  const contenedor = document.querySelector(".grillaPersonajes");
  let esqueleto_contenedor = "";
  for (const personaje of personajes) {
    esqueleto_contenedor += `
           <div class="grillaPersonajes__thumbnail">
            <img
              src="${personaje.imagen}"
              alt="${personaje.nombre}"
              data-id="${personaje.id}"
              class="grillaPersonajes__thumbnail--img"
            />
          </div>
          `;
  }
  contenedor.innerHTML = esqueleto_contenedor;
};

/**
 * Asigna el valor de el atributo 'data-id' del target el evento al parámetro 'id' .
 *
 * @param {Event} event - El objeto event.
 * @param {number} id - El ID a asignarle a el atributo 'data-id'.
 * @return {void} La función no devuelve ningun valor.
 */
export const obtener_id_personaje = (event) => {
  return parseInt(event.target.getAttribute("data-id"));
};

/**
 * Una función que cambia los estados de los botones basados en los IDs proporcionados.
 *
 * @param {any} id_1 - El primer ID.
 * @param {any} id_2 - El segundo ID.
 * @param {HTMLElement} boton_1 - El primer elemento de botón.
 * @param {HTMLElement} boton_2 - El segundo elemento de botón.
 * @param {HTMLElement} boton_iniciar - El elemento de botón de inicio.
 * @return {void} Esta función no devuelve ningún valor.
 */
export const switch_botones = (id_1, id_2, boton_1, boton_2, boton_iniciar) => {
  if (id_1 && !id_2) {
    boton_1.disabled = true;
    boton_2.disabled = false;
  } else if (id_1 && id_2) {
    boton_2.disabled = true;
    boton_iniciar.disabled = false;
  }
};

/**
 * Actualiza el contenedor con los datos del personaje proporcionados.
 *
 * @param {HTMLElement} contenedor - El elemento contenedor que se actualizará.
 * @param {Object} datos_personaje - Los datos del personaje a mostrar.
 * @return {void} Esta función no devuelve un valor.
 */
export const actualizar_contendor_personaje = (contenedor, datos_personaje) => {
  const name = contenedor.querySelector(".personajes__nombre");
  const imagen = contenedor.querySelector(".personajes__img");
  imagen.src = datos_personaje.imagen;
  imagen.alt = datos_personaje.nombre;
  name.innerText = datos_personaje.nombre;
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
export const setear_query_strings = (
  boton,
  route,
  id_personaje_1,
  id_personaje_2
) => {
  const url = `${route}?personaje_1=${id_personaje_1}&personaje_2=${id_personaje_2}`;
  boton.href = url;
};

export const actualizar_texto = (contenedor, texto) => {
  contenedor.innerText = texto;
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
