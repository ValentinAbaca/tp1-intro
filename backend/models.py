import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Personajes(db.Model):
    __tablename__ = 'personajes'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    vida = db.Column(db.Integer, nullable=False)
    ki = db.Column(db.Integer, nullable=False)
    descripcion = db.Column(db.String(255), nullable=False)
    raza = db.Column(db.String(255), nullable=False)
    imagen = db.Column(db.String(255), nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.datetime.now)

class Ataques(db.Model):
    __tablename__ = 'ataques'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    costo_ki = db.Column(db.Integer, nullable=False)
    dano_max = db.Column(db.Integer, nullable=False)
    dano_min = db.Column(db.Integer, nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.datetime.now)

class PersonajesAtaques(db.Model):
    __tablename__ = 'personajes_ataques'
    id = db.Column(db.Integer, primary_key=True)
    id_personaje = db.Column(db.Integer, db.ForeignKey('personajes.id'), nullable=False)
    id_ataque = db.Column(db.Integer, db.ForeignKey('ataques.id'), nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.datetime.now)
    personaje = db.relationship('Personajes')
    ataque = db.relationship('Ataques')