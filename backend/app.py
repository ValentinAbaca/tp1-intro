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

if __name__ == '__main__':
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', debug=True, port=port)