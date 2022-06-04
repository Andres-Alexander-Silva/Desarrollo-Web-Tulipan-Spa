from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __table_args__ = {'schema':'tulipanspa'}
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(40), unique=True, nullable=False)
    contraseña = db.Column(db.String(300), nullable=False)
    
    def __init__(self, usuario, contraseña):
        self.usuario = usuario
        self.contraseña = contraseña

class Service(db.Model):
    __table_args__ = {'schema':'tulipanspa'}
    __tablename__ = "service"
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(150), nullable=False)
    precio = db.Column(db.String(50), nullable=False)
    
    def __init__(self, titulo, precio):
        self.titulo = titulo
        self.precio = precio

class Promociones(db.Model):
    __table_args__ = {'schema':'tulipanspa'}
    __tablename__ = "promociones"
    id = db.Column(db.Integer, primary_key=True)
    imagen = db.Column(db.LargeBinary)
    
    def __init__(self, imagen):
        self.imagen = imagen 