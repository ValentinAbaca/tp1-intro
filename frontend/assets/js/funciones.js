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
 * @param {Event} event - The event object.
 * @param {number} id - The parameter to assign the 'data-id' value to.
 * @return {void} This function does not return a value.
 */
export const obtener_id_personaje = (event) => {
  return parseInt(event.target.getAttribute("data-id"));
};

export const switch_botones = (id_1, id_2, boton_1, boton_2, boton_iniciar) => {
  if (id_1 && !id_2) {
    boton_1.disabled = true;
    boton_2.disabled = false;
  } else if (id_1 && id_2) {
    boton_2.disabled = true;
    boton_iniciar.disabled = false;
  }
};

export const actualizar_contendor_personaje = (contenedor, datos_personaje) => {
  const name = contenedor.querySelector(".personajes__nombre");
  const imagen = contenedor.querySelector(".personajes__img");
  imagen.src = datos_personaje.imagen;
  imagen.alt = datos_personaje.nombre;
  name.innerText = datos_personaje.nombre;
};

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
