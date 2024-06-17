from flask import Flask, request, jsonify
from flask_cors import CORS
from models import db
from dotenv import load_dotenv
import os

from funciones import obtener_data_personajes, obtener_data_personaje_id, obtener_data_ataques, obtener_data_ataque_id, \
    crear_nuevo_personaje, crear_nuevo_ataque, borrar_personaje, borrar_ataque, modificar_personaje, modificar_ataque

load_dotenv() #Carga variables de ambiente del archivo .env
DATABASE_USER = os.getenv("DATABASE_USER")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
DATABASE_NAME = os.getenv("DATABASE_NAME")

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql+psycopg2://{DATABASE_USER}:{DATABASE_PASSWORD}@localhost:5432/{DATABASE_NAME}" # Conexión a la base de datos
port = 5000

@app.route('/')
def main_route():
    return 'Backend del proyecto!'

@app.route('/personajes', methods=['GET'])
def obtener_personajes():
    personajes_data = obtener_data_personajes()

    if not personajes_data:
        return jsonify({'Error': 'Personajes no encontrados'}), 404

    return jsonify(personajes_data)

@app.route('/personajes/<id>', methods=['GET'])
def obtener_personaje_id(id):
    personaje_data = obtener_data_personaje_id(id)
    if not personaje_data:
        return jsonify({'Error': 'Personaje no encontrado'}), 404
    return jsonify(personaje_data)

@app.route('/ataques', methods=['GET'])
def obtener_ataques():
    ataques_data = obtener_data_ataques()
    if not ataques_data:
        return jsonify({'Error': 'Ataques no encontrados'}), 404
    return jsonify(ataques_data)

@app.route('/ataques/<id>', methods=['GET'])
def obtener_ataque_id(id):
    ataque_data = obtener_data_ataque_id(id)
    if not ataque_data:
        return jsonify({'Error': 'Ataque no encontrado'}), 404
    return jsonify(ataque_data)

@app.route('/nuevo_personaje', methods=['POST'])
def crear_personaje():
    data = request.json
    personaje = crear_nuevo_personaje(data)
    if personaje == None:
        return jsonify({'message': 'El personaje ya existe'}), 400
    return jsonify({'succes' : True, 'personaje' : personaje}), 201

@app.route('/nuevo_ataque', methods=['POST'])
def crear_ataque():
    data = request.json
    ataque = crear_nuevo_ataque(data)
    if not ataque:
        return jsonify({'message': 'El ataque ya existe'}), 400
    return jsonify({'succes' : True, 'Ataque': ataque}), 201

@app.route('/borrar_personaje/<id>', methods=['DELETE'])
def borrar_personaje_por_id(id):
    borrar = borrar_personaje(id)
    if not borrar:
        return jsonify({'message': 'Personaje no encontrado'}), 404
    return jsonify({'message': f'Personaje id: {id} borrado correctamente'}), 200

@app.route('/borrar_ataque/<id>', methods=['DELETE'])
def borrar_ataque_por_id(id):
    borrar = borrar_ataque(id)
    if not borrar:
        return jsonify({'message': 'Ataque no encontrado'}), 404
    return jsonify({'message': f'Ataque id: {id} borrado correctamente'}), 200

@app.route('/modificar_ataque/<id>', methods=['PUT'])
def modificar_ataque_por_id(id):
    data = request.json
    ataque = modificar_ataque(id, data)
    if not ataque:
        return jsonify({'message': 'Ataque no encontrado'}), 404
    return jsonify({"Ataque" : ataque, "success" : True}), 200

@app.route('/modificar_personaje/<id>', methods=['PUT'])
def modificar_personaje_por_id(id):
    data = request.json
    personaje = modificar_personaje(id, data)
    if not personaje:
        return jsonify({'message': 'Personaje no encontrado'}), 404
    return jsonify({"personaje" : personaje, "success" : True}), 200

if __name__ == '__main__':
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', debug=True, port=port)