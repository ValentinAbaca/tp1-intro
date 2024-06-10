from flask import Flask, request, jsonify
from models import db, Personajes, Ataques, PersonajesAtaques

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

if __name__ == '__main__':
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', debug=True, port=port)