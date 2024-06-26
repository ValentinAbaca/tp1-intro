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
        raise error

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
        raise error

def obtener_ataques_personaje(id_personaje : int) -> list[PersonajesAtaques]:
    '''Recibe el ID de un personaje y retorna una lista con los ataques que tiene asignados obtenidos de la tabla de relaciones personajes_ataques.'''
    try:
        return PersonajesAtaques.query.filter_by(id_personaje=id_personaje).all()
    except Exception as error:
        raise error

def agregar_data_ataques_personaje(diccionario_personaje : dict, relaciones_ataques : list):
    '''Recibe un diccionario de personaje y una lista de relaciones de personaje-ataque, y agrega los datos de los ataques al diccionario del personaje.'''
    try:
        for relacion_ataque in relaciones_ataques:
            ataque = relacion_ataque.ataque
            ataque_data = crear_diccionario_ataque(ataque)
            diccionario_personaje['ataques'].append(ataque_data)
    except Exception as error:
        raise error

def obtener_personajes() -> list[Personajes]:
    '''Retorna una lista con todos los personajes de la tabla personajes de la base de datos.'''
    try:
        return Personajes.query.all()
    except Exception as error:
        raise error

def obtener_data_personajes() -> dict:
    '''Retorna un diccionario con el campo success y el campo personajes que contiene una lista de diccionarios de todos los personajes y sus ataques'''
    try:
        personajes = obtener_personajes()

        if not personajes:
            return {'success' : True, 'personajes' : []}

        personajes_data = []
        for personaje in personajes:
            personaje_data = crear_diccionario_personaje(personaje)
            relaciones_ataques = obtener_ataques_personaje(personaje.id)
            agregar_data_ataques_personaje(personaje_data, relaciones_ataques)
            personajes_data.append(personaje_data)
        return {'success' : True, 'personajes' : personajes_data}
    except Exception as error:
        return {'success' : False, 'error' : "ERROR:"+str(error)}

def obtener_personaje_por_id(id_personaje : int) -> Personajes:
    '''Recibe el ID de un personaje y retorna un objeto de la clase Personajes, obtenido de la tabla personajes.'''
    try:
        return Personajes.query.filter_by(id=id_personaje).first()
    except Exception as error:
        raise error

def obtener_data_personaje_id(id_personaje : int) -> dict:
    '''Recibe el ID de un personaje y retorna un diccionario con los datos del personaje y sus ataques'''
    try:
        personaje = obtener_personaje_por_id(id_personaje)

        if not personaje:
            return {'success' : False, 'error' : 'ERROR: No se encontro el personaje'}

        personaje_data = crear_diccionario_personaje(personaje)
        relaciones_ataques = obtener_ataques_personaje(id_personaje)
        agregar_data_ataques_personaje(personaje_data, relaciones_ataques)
        return {'success' : True, 'personaje' : personaje_data}
    except Exception as error:
        return {'success' : False, 'error' : "ERROR:" + str(error)}

def obtener_ataques() -> list[Ataques]:
    '''Retorna una lista con todos los ataques de la tabla ataques de la base de datos.'''
    try:
        return Ataques.query.all()
    except Exception as error:
        raise error

def obtener_data_ataques() -> dict:
    '''Retorna un diccionario con el campo success y el campo ataques que contiene una lista de diccionarios de todos los ataques.'''
    try:
        ataques = obtener_ataques()
        if not ataques:
            return {'success' : True, 'ataques' : []}
        ataques_data = []
        for ataque in ataques:
            ataque_data = crear_diccionario_ataque(ataque)
            ataques_data.append(ataque_data)
        return {'success' : True, 'ataques' : ataques_data}
    except Exception as error:
        return {'success' : False, 'error' : "ERROR:"+str(error)}

def obtener_ataque_id(id_ataque : int) -> Ataques:
    '''Recibe el ID de un ataque y retorna un objeto de la clase Ataques, obtenido de la tabla ataques.'''
    try:
        return Ataques.query.filter_by(id=id_ataque).first()
    except Exception as error:
        raise error

def obtener_data_ataque_id(id_ataque : int) -> dict:
    '''Recibe el ID de un ataque y retorna un diccionario con los datos del ataque'''
    try:
        ataque = obtener_ataque_id(id_ataque)
        if not ataque:
            return {'success' : False, 'error' : 'ERROR: No se encontro el ataque'}
        ataque_data = crear_diccionario_ataque(ataque)
        return {'success' : True, 'ataque' : ataque_data}
    except Exception as error:
        return {'success' : False, 'error' : "ERROR:" + str(error)}

def obtener_id_max(tabla) -> int:
    '''Recibe una tabla de la base de datos y retorna el ID máximo de la tabla, en caso de no encontrar un ID retorna None.'''
    try:
        id_max = tabla.query.order_by(tabla.id.desc()).first()
        if id_max:
            return id_max.id
        return None
    except Exception as error:
        raise error

def generar_id_nuevo(tabla) -> int:
    '''Genera un nuevo ID para una tabla de la base de datos, en caso de no encontrar un ID previo en esa tabla retorna 1.'''
    try:
        id_max = obtener_id_max(tabla)
        if id_max:
            return id_max + 1
        return 1
    except Exception as error:
        raise error

def verificar_existencia_por_nombre(tabla, nombre : str) -> bool:
    '''Recibe una tabla de la base de datos y un nombre, verifica si existe un registro con ese nombre en la tabla y retorna True o False.'''
    try:
        if tabla.query.filter_by(nombre=nombre).first():
            return True
        return False
    except Exception as error:
        raise error


def crear_nuevo_personaje(data) -> dict | None:
    '''Recibe un json con los datos de un personaje, \
    crea un nuevo personaje en la base de datos y retorna un diccionario con los datos del personaje, \
    en caso de ya existir el personaje retorna None.'''
    try:
        if verificar_existencia_por_nombre(Personajes , data['nombre']):
            return {'success' : False, 'error' : 'ERROR: El personaje ya existe'}

        id = generar_id_nuevo(Personajes)
        personaje = Personajes(id=id, nombre=data['nombre'], vida=data['vida'], ki=data['ki'], descripcion=data['descripcion'], raza=data['raza'], imagen=data['imagen'])
        db.session.add(personaje)

        ataques = data['ataques']
        if len(ataques) == 0:
            return {'success' : False, 'error' : 'No se puede dejar un personaje sin ataques'}
        for ataque in ataques:
            agregar_relacion_personaje_ataque(id, ataque)

        db.session.commit()
        return {'success' : True, 'personaje' : obtener_data_personaje_id(id)['personaje']}
    except Exception as error:
        return {'success' : False, 'error' : "ERROR: " + str(error)}

def crear_nuevo_ataque(data : dict) -> dict:
    '''Recibe un diccionario con los datos de un ataque y crea un nuevo ataque en la base de datos, \
        retorna un diccionario con los datos del ataque.'''
    try:
        if verificar_existencia_por_nombre(Ataques , data['nombre']):
            return {'success' : False, 'error' : 'ERROR: El ataque ya existe'}
        
        id = generar_id_nuevo(Ataques)
        ataque = Ataques(id=id, nombre=data['nombre'], costo_ki=data['costo_ki'], dano_max=data['dano_max'], dano_min=data['dano_min'])
        db.session.add(ataque)
        db.session.commit()
        return {'success' : True, 'ataque' : obtener_data_ataque_id(id)['ataque']}
    except Exception as error:
        return {'success' : False, 'error' : "ERROR: " + str(error)}


def borrar_ataques_personaje(id_personaje : int):
    '''Recibe el ID de un personaje y borra todas las relaciones de personaje-ataque que tenga asignadas.'''
    try:
        personaje_ataques = obtener_ataques_personaje(id_personaje)
        for personaje_ataque in personaje_ataques:
            db.session.delete(personaje_ataque)
        db.session.commit()
    except Exception as error:
        raise error

def borrar_personajes_ataque(id_ataque : int):
    '''Recibe el ID de un ataque y borra todas las relaciones de personaje-ataque que tenga asignadas.'''
    try:
        personajes_ataque = PersonajesAtaques.query.filter_by(id_ataque=id_ataque).all()
        for personaje_ataque in personajes_ataque:
            id_personaje = personaje_ataque.id_personaje
            if PersonajesAtaques.query.filter_by(id_personaje=id_personaje).count() == 1:
                raise Exception(f"No se puede borrar el ataque porque es el único ataque de un personaje")
            else:
                db.session.delete(personaje_ataque)
        db.session.commit()
    except Exception as error:
        raise error

def borrar_personaje(id_personaje: int) -> dict:
    '''Recibe el ID de un personaje y lo borra de la base de datos, retorna un diccionario con el campo success y un mensaje de error en caso de no poder borrarlo'''
    try:
        personaje = obtener_personaje_por_id(id_personaje)

        if not personaje:
            return {'success' : False, 'error' : 'ERROR: No se encontro el personaje'}
    
        borrar_ataques_personaje(id_personaje)
        db.session.delete(personaje)
        db.session.commit()
        return {'success' : True, 'message' : 'Personaje borrado correctamente'}
    except Exception as error:
        return {'success' : False, 'error' : str(error)}
    
def borrar_ataque(id_ataque : int) -> bool | None:
    '''Recibe el ID de un ataque y lo borra de la base de datos, retorna True si se borra correctamente y None si no se encuentra el ataque.'''
    try:
        ataque = obtener_ataque_id(id_ataque)
        if not ataque:
            return {'success' : False, 'error' : 'ERROR: No se encontro el ataque'}
        
        borrar_personajes_ataque(id_ataque)
        db.session.delete(ataque)
        db.session.commit()
        return {'success' : True, 'message' : 'Ataque borrado correctamente'}
    except Exception as error:
        return {'success' : False, 'error' : str(error)}


def agregar_relacion_personaje_ataque(id_personaje : int, id_ataque: int):
    '''Recibe un ID de personaje y un ID de ataque, agrega una nueva relación de personaje-ataque en la base de datos.'''
    try:
        ataque = obtener_ataque_id(id_ataque)
        if not ataque:
            raise Exception(f"El ataque id {id_ataque} que intentas agregar no existe.")
        id = generar_id_nuevo(PersonajesAtaques)
        personaje_ataque = PersonajesAtaques(id= id, id_personaje=id_personaje, id_ataque=id_ataque)
        db.session.add(personaje_ataque)
    except Exception as error:
        raise error

def obtener_relacion(id_personaje: int, id_ataque: int) -> PersonajesAtaques:
    '''Recibe un ID de personaje y un ID de ataque, retorna un objeto de la clase PersonajesAtaques, obtenido de la tabla personajes_ataques de la base de datos.'''
    try:
        return PersonajesAtaques.query.filter_by(id_ataque=id_ataque, id_personaje=id_personaje).first()
    except Exception as error:
        raise error


def borrar_relacion_personaje_ataque(id_personaje : int, id_ataque : int):
    '''Recibe un ID de personaje y un ID de ataque, borra una relación de personaje-ataque de la base de datos.'''
    try:
        relacion = obtener_relacion(id_personaje, id_ataque)
        db.session.delete(relacion)
    except Exception as error:
        raise error

def obtener_ids_ataques_personaje(id_personaje: int) -> list[int]:
    '''Recibe el ID de un personaje y retorna una lista con los IDs de los ataques que tiene asignados.'''
    try:
        ataques = obtener_ataques_personaje(id_personaje)
        ids_ataques = []
        for ataque in ataques:
            ids_ataques.append(ataque.id_ataque)
        return ids_ataques
    except Exception as error:
        raise error
    
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
        db.session.commit()
    except Exception as error:
        raise error

def modificar_personaje(id : int, data : dict) -> dict:
    '''Recibe un ID de personaje y un diccionario con los datos del personaje, \
    modifica los datos del personaje y sus relaciones de personaje-ataque y retorna un diccionario con dos campos, success y la data del personaje modificado.
    En caso de no encontrar el personaje retorna un diccionario con el campo success en False y un mensaje de error.'''
    try:
        personaje = obtener_personaje_por_id(id)

        if not personaje:
            return {'success' : False, 'error' : 'No se encontro el personaje'}

        ataques = data['ataques']
        if len(ataques) == 0:
            return {'success' : False, 'error' : 'No se puede dejar un personaje sin ataques'}
        modificar_relaciones(id, ataques)

        personaje.nombre = data['nombre']
        personaje.vida = data['vida']
        personaje.ki = data['ki']
        personaje.descripcion = data['descripcion']
        personaje.raza = data['raza']
        personaje.imagen = data['imagen']

        db.session.commit()

        return {'success' : True, 'personaje' : obtener_data_personaje_id(id)['personaje']}
    
    except Exception as error:
        print("entro aca")
        return {'success' : False, 'error' : str(error)}
    

def modificar_ataque(id : int, data : dict) -> dict:
    '''Recibe un ID de ataque y un diccionario con los datos del ataque, modifica los datos del ataque y retorna un diccionario con el campo success y otro campo \
    con los datos del ataque modificado, en caso de no encontrar el ataque retorna success en False y un mensaje de error.'''
    try:
        ataque = obtener_ataque_id(id)
        if not ataque:
            return {'success' : False, 'error' : 'No se encontro el ataque'}
        ataque.nombre = data['nombre']
        ataque.costo_ki = data['costo_ki']
        ataque.dano_max = data['dano_max']
        ataque.dano_min = data['dano_min']
        db.session.commit()
        return {'success' : True, 'ataque' : obtener_data_ataque_id(id)['ataque']}
    except Exception as error:
        return {'success' : False, 'error' : str(error)} 
