from flask import Flask, request, jsonify
from models import db, Personajes, Ataques, PersonajesAtaques
import os

user = "valentin" #Cambiar el usuario de la base de datos
password = "valentin" #Cambiar la contraseña de la base de datos
database = "prueba" #Cambiar el nombre de la base de datos

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql+psycopg2://{user}:{password}@localhost:5432/{database}" # Conexión a la base de datos
port = 5000

@app.route('/')
def main_route():
    return 'Backend del proyecto!'

@app.route('/personajes', methods=['GET'])
def obtener_personajes():
    try:
        personajes = Personajes.query.all()
        personajes_data = []
        for personaje in personajes:
            personaje_data = {
                'id': personaje.id,
                'nombre': personaje.nombre,
                'vida': personaje.vida,
                'ki': personaje.ki,
                'descripcion': personaje.descripcion,
                'ataques': []
            }

            ataques = PersonajesAtaques.query.filter_by(id_personaje=personaje.id).all()
            
            for ataque in ataques:
                ataque_data = {
                    'id': ataque.ataque.id,
                    'nombre': ataque.ataque.nombre,
                    'costo_ki': ataque.ataque.costo_ki,
                    'dano_max': ataque.ataque.dano_max,
                    'dano_min': ataque.ataque.dano_min
                }
                
                personaje_data['ataques'].append(ataque_data)
            personajes_data.append(personaje_data)
        return jsonify(personajes_data)
    except Exception as error:
        print(f"Error al obtener personajes: {str(error)}")
        return jsonify({'message': 'Personajes no encontrados'}), 500
    

@app.route('/personajes/<id>', methods=['GET'])
def obtener_personaje_id(id):
    try:
        personaje = Personajes.query.get(id)
        personaje_data = {
            'id': personaje.id,
            'nombre': personaje.nombre,
            'vida': personaje.vida,
            'ki': personaje.ki,
            'descripcion': personaje.descripcion,
            'ataques': []
        }
        ataques = PersonajesAtaques.query.filter_by(id_personaje=personaje.id).all()
        for ataque in ataques:
            ataque_data = {
                'id': ataque.ataque.id,
                'nombre': ataque.ataque.nombre,
                'costo_ki': ataque.ataque.costo_ki,
                'dano_max': ataque.ataque.dano_max,
                'dano_min': ataque.ataque.dano_min
            }
            personaje_data['ataques'].append(ataque_data)
        return jsonify(personaje_data)
    except Exception as error:
        print(f"Error al obtener personaje: {str(error)}")
        return jsonify({'message': 'Personaje no encontrado'}), 500

@app.route('/ataques')
def obtener_ataques():
    try:
        ataques = Ataques.query.all()
        ataques_data = []
        for ataque in ataques:
            ataque_data = {
                'id': ataque.id,
                'nombre': ataque.nombre,
                'costo_ki': ataque.costo_ki,
                'dano_max': ataque.dano_max,
                'dano_min': ataque.dano_min
            }
            ataques_data.append(ataque_data)
        return jsonify(ataques_data)
    except Exception as error:
        print(f"Error al obtener ataques: {str(error)}")
        return jsonify({'message': 'Ataques no encontrados'}), 500

@app.route('/nuevo_personaje', methods=['POST'])
def crear_personaje():
    try:
        id_max = Personajes.query.order_by(Personajes.id.desc()).first()
        id = id_max.id + 1

        data = request.form
        nuevo_nombre = data['nombre']

        verificar_personaje = Personajes.query.filter_by(nombre=nuevo_nombre).first()
        if verificar_personaje:
            return jsonify({'message': 'El personaje ya existe'}), 400

        nueva_vida = data['vida']
        nuevo_ki = data['ki']
        nueva_descripcion = data['descripcion']
        nueva_raza = data['raza']
        
        nueva_imagen = request.files['imagen']
        nueva_imagen.save(f"static/img/{nueva_imagen.filename}")
        print(f"Imagen guardada en: static/img/{nueva_imagen.filename}")
        path = f"http://localhost:5000/static/img/{nueva_imagen.filename}"

        personaje = Personajes(id=id, nombre=nuevo_nombre, vida=nueva_vida, ki=nuevo_ki, descripcion=nueva_descripcion, raza=nueva_raza, imagen=path)
        db.session.add(personaje)
        db.session.commit()

        ataques = data['ataques'].split(',')
        for ataque in ataques:
            ataque_id = int(ataque)
            max_id_relacion = PersonajesAtaques.query.order_by(PersonajesAtaques.id.desc()).first()
            id_relacion = max_id_relacion.id + 1
            personaje_ataque = PersonajesAtaques(id=id_relacion, id_personaje=id, id_ataque=ataque_id)
            db.session.add(personaje_ataque)
            db.session.commit()

        nuevos_ataques = []
        for ataque in ataques:
            ataque_id = int(ataque)
            ataque = Ataques.query.get(ataque_id)
            ataque_data = {
                'id': ataque.id,
                'nombre': ataque.nombre,
                'costo_ki': ataque.costo_ki,
                'dano_max': ataque.dano_max,
                'dano_min': ataque.dano_min
            }
            nuevos_ataques.append(ataque_data)

        return jsonify({"personaje" : {"id" : personaje.id, 
                                        "nombre" : personaje.nombre, 
                                        "vida" : personaje.vida, 
                                        "ki" : personaje.ki, 
                                        "descripcion" : personaje.descripcion,
                                        "raza" : personaje.raza, 
                                        "imagen" : personaje.imagen,
                                        "ataques" : nuevos_ataques
                                        }}), 201
    except Exception as error:
        print(f"Error al crear personaje: {str(error)}")
        return jsonify({'message': 'Error al crear personaje'}), 500

@app.route('/nuevo_ataque', methods=['POST'])
def crear_ataque():
    try:
        id_max = Ataques.query.order_by(Ataques.id.desc()).first()
        id = id_max.id + 1

        data = request.form
        nuevo_nombre = data['nombre']
        
        verificar_ataque = Ataques.query.filter_by(nombre=nuevo_nombre).first()
        if verificar_ataque:
            return jsonify({'message': 'El ataque ya existe'}), 400

        nuevo_costo_ki = data['costo_ki']
        nuevo_dano_max = data['dano_max']
        nuevo_dano_min = data['dano_min']

        ataque = Ataques(id=id, nombre=nuevo_nombre, costo_ki=nuevo_costo_ki, dano_max=nuevo_dano_max, dano_min=nuevo_dano_min)
        db.session.add(ataque)
        db.session.commit()

        return jsonify({"ataque" : {"id" : ataque.id, 
                                    "nombre" : ataque.nombre, 
                                    "costo_ki" : ataque.costo_ki, 
                                    "dano_max" : ataque.dano_max, 
                                    "dano_min" : ataque.dano_min
                                    }}), 201
    except Exception as error:
        print(f"Error al crear ataque: {str(error)}")
        return jsonify({'message': 'Error al crear ataque'}), 500

@app.route('/borrar_personaje/<id>', methods=['DELETE'])
def borrar_personaje(id):
    try:
        personaje_ataques = PersonajesAtaques.query.filter_by(id_personaje=id).all()
        for personaje_ataque in personaje_ataques:
            db.session.delete(personaje_ataque)
            db.session.commit()
        
        personaje = Personajes.query.get(id)

        img_path = personaje.imagen.split('/')[-1]
        os.remove(f"static/img/{img_path}")

        db.session.delete(personaje)
        db.session.commit()
        return jsonify({'message': f'Personaje id: {id} borrado correctamente'}), 200

    except Exception as error:
        print(f"Error al borrar personaje: {str(error)}")
        return jsonify({'message': f'Error al borrar personaje {id}'}), 400
    
@app.route('/borrar_ataque/<id>', methods=['DELETE'])
def borrar_ataque(id):
    try:
        ataques_personajes = PersonajesAtaques.query.filter_by(id_ataque=id).all()
        for ataque_personaje in ataques_personajes:
            db.session.delete(ataque_personaje)
            db.session.commit()
        
        ataque = Ataques.query.get(id)
        db.session.delete(ataque)
        db.session.commit()
        return jsonify({'message': f'Ataque id: {id} borrado correctamente'}), 200

    except Exception as error:
        print(f"Error al borrar ataque: {str(error)}")
        return jsonify({'message': f'Error al borrar ataque {id}'}), 500

if __name__ == '__main__':
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', debug=True, port=port)