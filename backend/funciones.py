from models import db, Personajes, Ataques, PersonajesAtaques
import os

def crear_diccionario_personaje(personaje):
    try:
        personaje_data = {
            'id': personaje.id,
            'nombre': personaje.nombre,
            'vida': personaje.vida,
            'ki': personaje.ki,
            'descripcion': personaje.descripcion,
            'raza': personaje.raza,
            'imagen': personaje.imagen,
            'ataques': []
        }
        return personaje_data
    except Exception as error:
        return f"Error al crear diccionario de personaje: {str(error)}"

def crear_diccionario_ataque(ataque):
    try:
        ataque_data = {
            'id': ataque.id,
            'nombre': ataque.nombre,
            'costo_ki': ataque.costo_ki,
            'dano_max': ataque.dano_max,
            'dano_min': ataque.dano_min
        }
        return ataque_data
    except Exception as error:
        return f"Error al crear diccionario de ataque: {str(error)}"

def obtener_ataques_personaje(id_personaje):
    try:
        return PersonajesAtaques.query.filter_by(id_personaje=id_personaje).all()
    except Exception as error:
        return f"Error al obtener ataques del personaje: {str(error)}"

def agregar_data_ataques_personaje(diccionario_personaje, relaciones_ataques):
    try:
        for relacion_ataque in relaciones_ataques:
            ataque = relacion_ataque.ataque
            ataque_data = crear_diccionario_ataque(ataque)
            diccionario_personaje['ataques'].append(ataque_data)
    except Exception as error:
        return f"Error al agregar datos de ataques al personaje: {str(error)}"

def obtener_personajes():
    try:
        return Personajes.query.all()
    except Exception as error:
        return f"Error al obtener personajes: {str(error)}"

def obtener_data_personajes():
    try:
        personajes = obtener_personajes()

        if not personajes:
            return False

        personajes_data = []
        for personaje in personajes:
            personaje_data = crear_diccionario_personaje(personaje)
            relaciones_ataques = obtener_ataques_personaje(personaje.id)
            agregar_data_ataques_personaje(personaje_data, relaciones_ataques)
            personajes_data.append(personaje_data)
        return personajes_data
    except Exception as error:
        return f"Error al obtener datos de personajes: {str(error)}"

def obtener_personaje_por_id(id_personaje):
    try:
        return Personajes.query.filter_by(id=id_personaje).first()
    except Exception as error:
        return f"Error al obtener personaje por ID: {str(error)}"

def obtener_data_personaje_id(id_personaje):
    try:
        personaje = obtener_personaje_por_id(id_personaje)

        if not personaje:
            return False

        personaje_data = crear_diccionario_personaje(personaje)
        relaciones_ataques = obtener_ataques_personaje(id_personaje)
        agregar_data_ataques_personaje(personaje_data, relaciones_ataques)
        return personaje_data
    except Exception as error:
        return f"Error al obtener datos del personaje por ID: {str(error)}"

def obtener_ataques():
    try:
        return Ataques.query.all()
    except Exception as error:
        return f"Error al obtener ataques: {str(error)}"

def obtener_data_ataques():
    try:
        ataques = obtener_ataques()
        if not ataques:
            return False
        ataques_data = []
        for ataque in ataques:
            ataque_data = crear_diccionario_ataque(ataque)
            ataques_data.append(ataque_data)
        return ataques_data
    except Exception as error:
        return f"Error al obtener datos de ataques: {str(error)}"

def obtener_ataque_id(id_ataque):
    try:
        return Ataques.query.filter_by(id=id_ataque).first()
    except Exception as error:
        return f"Error al obtener ataque por ID: {str(error)}"

def obtener_data_ataque_id(id_ataque : int) -> dict:
    try:
        ataque = obtener_ataque_id(id_ataque)
        if not ataque:
            return False
        ataque_data = crear_diccionario_ataque(ataque)
        return ataque_data
    except Exception as error:
        return f"Error al obtener datos del ataque por ID: {str(error)}"

def obtener_id_max(tabla):
    try:
        id_max = tabla.query.order_by(tabla.id.desc()).first()
        if id_max:
            return id_max.id
        return None
    except Exception as error:
        return f"Error al obtener el ID máximo: {str(error)}"

def generar_id_nuevo(tabla):
    try:
        id_max = obtener_id_max(tabla)
        if id_max:
            return id_max + 1
        return 1
    except Exception as error:
        return f"Error al generar un nuevo ID: {str(error)}"

def verificar_existencia_por_nombre(tabla, nombre):
    try:
        if tabla.query.filter_by(nombre=nombre).first():
            return True
        return False
    except Exception as error:
        return f"Error al verificar la existencia por nombre de la tabla {tabla}: {str(error)}"

def guardar_imagen(imagen):
    try:
        imagen.save(f'static/img/{imagen.filename}')
        return f'static/img/{imagen.filename}'
    except Exception as error:
        return f"Error al guardar la imagen: {str(error)}"

def crear_nuevo_personaje(data, imagen):
    try:
        if verificar_existencia_por_nombre(Personajes , data['nombre']):
            return None
        
        path_imagen = f"http://localhost:5000/{guardar_imagen(imagen)}"

        id = generar_id_nuevo(Personajes)
        personaje = Personajes(id=id, nombre=data['nombre'], vida=data['vida'], ki=data['ki'], descripcion=data['descripcion'], raza=data['raza'], imagen=path_imagen)
        db.session.add(personaje)

        ataques = data['ataques'].split(',')
        for ataque in ataques:
            agregar_relacion_personaje_ataque(id, ataque)

        db.session.commit()
        return obtener_data_personaje_id(id)
    except Exception as error:
        return f"Error al crear un nuevo personaje: {str(error)}"

def crear_nuevo_ataque(data):
    try:
        if verificar_existencia_por_nombre(Ataques , data['nombre']):
            return None
        
        id = generar_id_nuevo(Ataques)
        ataque = Ataques(id=id, nombre=data['nombre'], costo_ki=data['costo_ki'], dano_max=data['dano_max'], dano_min=data['dano_min'])
        db.session.add(ataque)
        db.session.commit()
        return obtener_data_ataque_id(id)
    except Exception as error:
        return f"Error al crear un nuevo ataque: {str(error)}"

def borrar_imagen(nombre_imagen):
    try:
        os.remove(f"static/img/{nombre_imagen}")
    except Exception as error:
        return f"Error al borrar la imagen: {str(error)}"

def borrar_ataques_personaje(id_personaje):
    personaje_ataques = obtener_ataques_personaje(id_personaje)
    for personaje_ataque in personaje_ataques:
        db.session.delete(personaje_ataque)
        db.session.commit()
    
def borrar_personaje(id_personaje):
    try:
        personaje = obtener_personaje_por_id(id_personaje)

        if not personaje:
            return False

        nombre_imagen = personaje.imagen.split('/')[-1]
        borrar_ataques_personaje(id_personaje)
        db.session.delete(personaje)
        db.session.commit()
        borrar_imagen(nombre_imagen)
        return True
    except Exception as error:
        return f"Error al borrar un personaje: {str(error)}"
    
def borrar_ataque(id_ataque):
    try:
        ataque = obtener_ataque_id(id_ataque)
        if not ataque:
            return False
        db.session.delete(ataque)
        db.session.commit()
        return True
    except Exception as error:
        return f"Error al borrar un ataque: {str(error)}"

def verificar_existencia_relacion(id_personaje, id_ataque):
    try:
        return PersonajesAtaques.query.filter_by(id_personaje=id_personaje, id_ataque=id_ataque).count() > 0
    except Exception as error:
        return f"Error al verificar la existencia de la relación: {str(error)}"

def agregar_relacion_personaje_ataque(id_personaje, id_ataque):
    try:
        id = generar_id_nuevo(PersonajesAtaques)
        personaje_ataque = PersonajesAtaques(id= id, id_personaje=id_personaje, id_ataque=id_ataque)
        db.session.add(personaje_ataque)
        db.session.commit()
    except Exception as error:
        return f"Error al agregar una relación de personaje y ataque: {str(error)}"

def obtener_relacion(id_personaje, id_ataque):
    try:
        return PersonajesAtaques.query.filter_by(id_ataque=id_ataque, id_personaje=id_personaje).first()
    except Exception as error:
        return f"Error al obtener una relación de personaje y ataque: {str(error)}"


def borrar_relacion_personaje_ataque(id_personaje, id_ataque):
    try:
        relacion = obtener_relacion(id_personaje, id_ataque)
        db.session.delete(relacion)
        db.session.commit()
    except Exception as error:
        return f"Error al borrar una relación de personaje y ataque: {str(error)}"
    
def obtener_ataques_personaje(id_personaje):
    try:
        return PersonajesAtaques.query.filter_by(id_personaje=id_personaje).all()
    except Exception as error:
        return f"Error al obtener ataques del personaje: {str(error)}"

def obtener_ids_ataques_personaje(id_personaje):
    try:
        ataques = obtener_ataques_personaje(id_personaje)
        ids_ataques = []
        for ataque in ataques:
            ids_ataques.append(ataque.id_ataque)
        return ids_ataques
    except Exception as error:
        return f"Error al obtener los IDs de los ataques del personaje: {str(error)}"
    
def modificar_relaciones(id_personaje, lista_ids_nuevos_ataques):
    try:
        ids__viejos_ataques = obtener_ids_ataques_personaje(id_personaje)
        for id_ataque in ids__viejos_ataques:
            if id_ataque not in lista_ids_nuevos_ataques:
                borrar_relacion_personaje_ataque(id_personaje, id_ataque)
        for id_ataque in lista_ids_nuevos_ataques:
            if id_ataque not in ids__viejos_ataques:
                agregar_relacion_personaje_ataque(id_personaje, id_ataque)
    except Exception as error:
        return f"Error al modificar las relaciones de personaje y ataque: {str(error)}"

def modificar_personaje(id, data, imagen):
    try:
        personaje = obtener_personaje_por_id(id)

        if not personaje:
            return None

        if imagen:
            path_imagen = f"http://localhost:5000/{guardar_imagen(imagen)}"
            borrar_imagen(personaje.imagen.split('/')[-1])
            personaje.imagen = path_imagen

        personaje.nombre = data['nombre']
        personaje.vida = data['vida']
        personaje.ki = data['ki']
        personaje.descripcion = data['descripcion']
        personaje.raza = data['raza']
        db.session.commit()

        ataques = data['ataques'].split(',')
        modificar_relaciones(id, ataques)

        return obtener_data_personaje_id(id)
    
    except Exception as error:
        return f"Error al modificar un personaje: {str(error)}"
    

def modificar_ataque(id, data):
    try:
        ataque = obtener_ataque_id(id)
        if not ataque:
            return None
        ataque.nombre = data['nombre']
        ataque.costo_ki = data['costo_ki']
        ataque.dano_max = data['dano_max']
        ataque.dano_min = data['dano_min']
        db.session.commit()
        return obtener_data_ataque_id(id)
    except Exception as error:
        return f"Error al modificar un ataque: {str(error)}"

