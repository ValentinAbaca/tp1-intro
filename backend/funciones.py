from models import db, Personajes, Ataques, PersonajesAtaques
import os

def crear_diccionario_personaje(personaje : Personajes) -> dict:
    '''Recibe un objeto de la clase Personajes, obtenido de la base de datos y retorna un diccionario con los datos del personaje. El campo ataques del personaje \
        es una lista vacia para agregar los ataques posteriormente'''
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

def crear_diccionario_ataque(ataque : Ataques) -> dict:
    '''Recibe un objeto de la clase Ataques, obtenido de la base de datos y retorna un diccionario con los datos del ataque.'''
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

def obtener_ataques_personaje(id_personaje : int) -> list[PersonajesAtaques]:
    '''Recibe el ID de un personaje y retorna una lista con los ataques que tiene asignados obtenidos de la tabla de relaciones personajes_ataques.'''
    try:
        return PersonajesAtaques.query.filter_by(id_personaje=id_personaje).all()
    except Exception as error:
        return f"Error al obtener ataques del personaje: {str(error)}"

def agregar_data_ataques_personaje(diccionario_personaje : dict, relaciones_ataques : list):
    '''Recibe un diccionario de personaje y una lista de relaciones de personaje-ataque, y agrega los datos de los ataques al diccionario del personaje.'''
    try:
        for relacion_ataque in relaciones_ataques:
            ataque = relacion_ataque.ataque
            ataque_data = crear_diccionario_ataque(ataque)
            diccionario_personaje['ataques'].append(ataque_data)
    except Exception as error:
        return f"Error al agregar datos de ataques al personaje: {str(error)}"

def obtener_personajes() -> list[Personajes]:
    '''Retorna una lista con todos los personajes de la tabla personajes de la base de datos.'''
    try:
        return Personajes.query.all()
    except Exception as error:
        return f"Error al obtener personajes: {str(error)}"

def obtener_data_personajes() -> list[dict] | None:
    '''Retorna una lista de diccionarios de todos los personajes y sus ataques, en caso de no encontrar los personajes retorna None'''
    try:
        personajes = obtener_personajes()

        if not personajes:
            return None

        personajes_data = []
        for personaje in personajes:
            personaje_data = crear_diccionario_personaje(personaje)
            relaciones_ataques = obtener_ataques_personaje(personaje.id)
            agregar_data_ataques_personaje(personaje_data, relaciones_ataques)
            personajes_data.append(personaje_data)
        return personajes_data
    except Exception as error:
        return f"Error al obtener datos de personajes: {str(error)}"

def obtener_personaje_por_id(id_personaje : int) -> Personajes:
    '''Recibe el ID de un personaje y retorna un objeto de la clase Personajes, obtenido de la tabla personajes.'''
    try:
        return Personajes.query.filter_by(id=id_personaje).first()
    except Exception as error:
        return f"Error al obtener personaje por ID: {str(error)}"

def obtener_data_personaje_id(id_personaje : int) -> dict | None:
    '''Recibe el ID de un personaje y retorna un diccionario con los datos del personaje y sus ataques, en caso de no encontrar el personaje retorna None.'''
    try:
        personaje = obtener_personaje_por_id(id_personaje)

        if not personaje:
            return None

        personaje_data = crear_diccionario_personaje(personaje)
        relaciones_ataques = obtener_ataques_personaje(id_personaje)
        agregar_data_ataques_personaje(personaje_data, relaciones_ataques)
        return personaje_data
    except Exception as error:
        return f"Error al obtener datos del personaje por ID: {str(error)}"

def obtener_ataques() -> list[Ataques]:
    '''Retorna una lista con todos los ataques de la tabla ataques de la base de datos.'''
    try:
        return Ataques.query.all()
    except Exception as error:
        return f"Error al obtener ataques: {str(error)}"

def obtener_data_ataques() -> list | None:
    '''Retorna una lista con diccionarios de todos los ataques, en caso de no encontrar los ataques retorna None.'''
    try:
        ataques = obtener_ataques()
        if not ataques:
            return None
        ataques_data = []
        for ataque in ataques:
            ataque_data = crear_diccionario_ataque(ataque)
            ataques_data.append(ataque_data)
        return ataques_data
    except Exception as error:
        return f"Error al obtener datos de ataques: {str(error)}"

def obtener_ataque_id(id_ataque : int) -> Ataques:
    '''Recibe el ID de un ataque y retorna un objeto de la clase Ataques, obtenido de la tabla ataques.'''
    try:
        return Ataques.query.filter_by(id=id_ataque).first()
    except Exception as error:
        return f"Error al obtener ataque por ID: {str(error)}"

def obtener_data_ataque_id(id_ataque : int) -> dict | None:
    '''Recibe el ID de un ataque y retorna un diccionario con los datos del ataque, en caso de no encontrar el ataque retorna None.'''
    try:
        ataque = obtener_ataque_id(id_ataque)
        if not ataque:
            return None
        ataque_data = crear_diccionario_ataque(ataque)
        return ataque_data
    except Exception as error:
        return f"Error al obtener datos del ataque por ID: {str(error)}"

def obtener_id_max(tabla) -> int:
    '''Recibe una tabla de la base de datos y retorna el ID máximo de la tabla, en caso de no encontrar un ID retorna None.'''
    try:
        id_max = tabla.query.order_by(tabla.id.desc()).first()
        if id_max:
            return id_max.id
        return None
    except Exception as error:
        return f"Error al obtener el ID máximo: {str(error)}"

def generar_id_nuevo(tabla) -> int:
    '''Genera un nuevo ID para una tabla de la base de datos, en caso de no encontrar un ID previo en esa tabla retorna 1.'''
    try:
        id_max = obtener_id_max(tabla)
        if id_max:
            return id_max + 1
        return 1
    except Exception as error:
        return f"Error al generar un nuevo ID: {str(error)}"

def verificar_existencia_por_nombre(tabla, nombre : str) -> bool:
    '''Recibe una tabla de la base de datos y un nombre, verifica si existe un registro con ese nombre en la tabla y retorna True o False.'''
    try:
        if tabla.query.filter_by(nombre=nombre).first():
            return True
        return False
    except Exception as error:
        return f"Error al verificar la existencia por nombre de la tabla {tabla}: {str(error)}"


def crear_nuevo_personaje(data) -> dict | None:
    '''Recibe un json con los datos de un personaje, \
    crea un nuevo personaje en la base de datos y retorna un diccionario con los datos del personaje, \
    en caso de ya existir el personaje retorna None.'''
    try:
        if verificar_existencia_por_nombre(Personajes , data['nombre']):
            return None

        id = generar_id_nuevo(Personajes)
        personaje = Personajes(id=id, nombre=data['nombre'], vida=data['vida'], ki=data['ki'], descripcion=data['descripcion'], raza=data['raza'], imagen=data['imagen'])
        db.session.add(personaje)

        ataques = data['ataques'].split(',')
        for ataque in ataques:
            agregar_relacion_personaje_ataque(id, ataque)

        db.session.commit()
        return obtener_data_personaje_id(id)
    except Exception as error:
        return f"Error al crear un nuevo personaje: {str(error)}"

def crear_nuevo_ataque(data : dict) -> dict | None:
    '''Recibe un diccionario con los datos de un ataque y crea un nuevo ataque en la base de datos, \
        retorna un diccionario con los datos del ataque y en caso de existir el ataque retorna None'''
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


def borrar_ataques_personaje(id_personaje : int):
    '''Recibe el ID de un personaje y borra todas las relaciones de personaje-ataque que tenga asignadas.'''
    personaje_ataques = obtener_ataques_personaje(id_personaje)
    for personaje_ataque in personaje_ataques:
        db.session.delete(personaje_ataque)
        db.session.commit()
    
def borrar_personaje(id_personaje: int) -> bool | None:
    '''Recibe el ID de un personaje y lo borra de la base de datos, retorna True si se borra correctamente y None si no se encuentra el personaje.'''
    try:
        personaje = obtener_personaje_por_id(id_personaje)

        if not personaje:
            return None

    
        borrar_ataques_personaje(id_personaje)
        db.session.delete(personaje)
        db.session.commit()
        return True
    except Exception as error:
        return f"Error al borrar un personaje: {str(error)}"
    
def borrar_ataque(id_ataque : int) -> bool | None:
    '''Recibe el ID de un ataque y lo borra de la base de datos, retorna True si se borra correctamente y None si no se encuentra el ataque.'''
    try:
        ataque = obtener_ataque_id(id_ataque)
        if not ataque:
            return None
        db.session.delete(ataque)
        db.session.commit()
        return True
    except Exception as error:
        return f"Error al borrar un ataque: {str(error)}"


def agregar_relacion_personaje_ataque(id_personaje : int, id_ataque: int):
    '''Recibe un ID de personaje y un ID de ataque, agrega una nueva relación de personaje-ataque en la base de datos.'''
    try:
        id = generar_id_nuevo(PersonajesAtaques)
        personaje_ataque = PersonajesAtaques(id= id, id_personaje=id_personaje, id_ataque=id_ataque)
        db.session.add(personaje_ataque)
        db.session.commit()
    except Exception as error:
        return f"Error al agregar una relación de personaje y ataque: {str(error)}"

def obtener_relacion(id_personaje: int, id_ataque: int) -> PersonajesAtaques:
    '''Recibe un ID de personaje y un ID de ataque, retorna un objeto de la clase PersonajesAtaques, obtenido de la tabla personajes_ataques de la base de datos.'''
    try:
        return PersonajesAtaques.query.filter_by(id_ataque=id_ataque, id_personaje=id_personaje).first()
    except Exception as error:
        return f"Error al obtener una relación de personaje y ataque: {str(error)}"


def borrar_relacion_personaje_ataque(id_personaje : int, id_ataque : int):
    '''Recibe un ID de personaje y un ID de ataque, borra una relación de personaje-ataque de la base de datos.'''
    try:
        relacion = obtener_relacion(id_personaje, id_ataque)
        db.session.delete(relacion)
        db.session.commit()
    except Exception as error:
        return f"Error al borrar una relación de personaje y ataque: {str(error)}"

def obtener_ids_ataques_personaje(id_personaje: int) -> list[int]:
    '''Recibe el ID de un personaje y retorna una lista con los IDs de los ataques que tiene asignados.'''
    try:
        ataques = obtener_ataques_personaje(id_personaje)
        ids_ataques = []
        for ataque in ataques:
            ids_ataques.append(ataque.id_ataque)
        return ids_ataques
    except Exception as error:
        return f"Error al obtener los IDs de los ataques del personaje: {str(error)}"
    
def modificar_relaciones(id_personaje : int, lista_ids_nuevos_ataques : list[int]):
    '''Recibe el ID de un personaje y una lista con los IDs de los nuevos ataques, \
    compara los IDs de los ataques viejos con los nuevos y agrega o borra las relaciones de personaje-ataque necesarias.'''
    try:
        ids__viejos_ataques = obtener_ids_ataques_personaje(id_personaje)
        for id_ataque in ids__viejos_ataques: # Si esta en los viejos pero no en los nuevos hay que borrarlo
            if id_ataque not in lista_ids_nuevos_ataques:
                borrar_relacion_personaje_ataque(id_personaje, id_ataque)
        for id_ataque in lista_ids_nuevos_ataques: # Si esta en los nuevos pero no en los viejos hay que agregarlo
            if id_ataque not in ids__viejos_ataques:
                agregar_relacion_personaje_ataque(id_personaje, id_ataque)
    except Exception as error:
        return f"Error al modificar las relaciones de personaje y ataque: {str(error)}"

def modificar_personaje(id : int, data : dict) -> dict | None:
    '''Recibe un ID de personaje y un diccionario con los datos del personaje, \
    modifica los datos del personaje y sus relaciones de personaje-ataque y retorna un diccionario con los datos del personaje modificado, \
    en caso de no encontrar el personaje retorna None.'''
    try:
        personaje = obtener_personaje_por_id(id)

        if not personaje:
            return None

        personaje.nombre = data['nombre']
        personaje.vida = data['vida']
        personaje.ki = data['ki']
        personaje.descripcion = data['descripcion']
        personaje.raza = data['raza']
        personaje.imagen = data['imagen']
        db.session.commit()

        ataques = data.get('ataques')
        
        modificar_relaciones(id, ataques)

        return obtener_data_personaje_id(id)
    
    except Exception as error:
        return f"Error al modificar un personaje: {str(error)}"
    

def modificar_ataque(id : int, data : dict) -> dict | None:
    '''Recibe un ID de ataque y un diccionario con los datos del ataque, modifica los datos del ataque y retorna un diccionario con los datos del ataque modificado, \
    en caso de no encontrar el ataque retorna None.'''
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

