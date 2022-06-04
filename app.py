from flask import Flask
from flask import render_template
from flask import url_for
from flask import request
from flask import session
from flask import redirect
from flask import flash
from flaskext.mysql import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)
mysql = MySQL()

app.config['SECRET_KEY'] = "myScretKeyTulipanSpaAndresSilva"
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'tulipanspa'

mysql.init_app(app)

@app.route("/")
@app.route("/inicio")
def inicio():
    titulo = "Tulipan Spa"
    return render_template("inicio.html", title=titulo)

@app.route("/servicios")
def servicios():
    titulo = "Servicios"
    return render_template("servicios.html", title=titulo)

@app.route("/promociones", methods=["GET","POST"])
def promociones():
    titulo = "Promociones"
    return render_template("promociones.html", title=titulo)

@app.route("/agregar-imagen", methods=["GET","POST"])
def agregar_img():
    titulo = "Agregar Imagen"
    
    if request.method == "POST":
        _imagen =request.files["img-servi"]
        now = datetime.now()
        tiempo = now.strftime("%Y%H%M%S")
        
        if _imagen.filename != "":
            nuevoNombreFoto = tiempo+_imagen.filename
            _imagen.save("static/img/"+nuevoNombreFoto)
            
        sql = "INSERT INTO `galeria` (`id`, `imagen`) VALUES (NULL, %s);"
        datos = (_imagen)
        conection = mysql.connect()
        cursor = conection.cursor()
        cursor.execute(sql,datos)
        conection.commit()    
        
    return render_template("agregarImagen.html", title=titulo)

@app.route("/agregar-noticia", methods=["GET","POST"])
def agregar_noticia():
    titulo = "Agregar Noticia"
    
    if request.method == "POST":
        _imagen = request.files["img-noti"]
        now = datetime.now()
        tiempo = now.strftime("%Y%H%M%S")
        
        if _imagen.filename != "":
            nuevoNombreFoto = tiempo+_imagen.filename
            _imagen.save("static/img/"+nuevoNombreFoto)
            
            sql = "INSERT INTO `noticias` (`id`, `imagen`) VALUES (NULL, %s);"
            datos = (_imagen)
            conection = mysql.connect()
            cursor = conection.cursor()
            cursor.execute(sql,datos)
            conection.commit()
            
    return render_template("agregarNoticia.html", title=titulo)

@app.route("/agregar-Promocion", methods=["GET","POST"])
def agregar_promocion():
    titulo = "Agregar Promocion"
    
    if request.method == "POST":
        _imagen = request.files["img-prom"]
        now = datetime.now()
        tiempo = now.strftime("%Y%H%M%S")
        
        if _imagen.filename != "":
            nuevoNombreFoto = tiempo+_imagen.filename
            _imagen.save("static/img/"+nuevoNombreFoto)
            
            sql = "INSERT INTO `promociones` (`id`, `imagen`) VALUES (NULL, %s);"
            datos = (_imagen)
            conection = mysql.connect()
            cursor = conection.cursor()
            cursor.execute(sql,datos)
            conection.commit()
    
    return render_template("agregarPromocion.html", title=titulo)

@app.route("/agregar-servicio", methods=["GET","POST"])
def agregar_servicio():
    titulo = "Agregar Servicio"
    
    if request.method == "POST":
        _titulo = request.form["title-servi"]
        _precio = request.form["sale-servi"]
        _imagen = request.files["img-servi"]
        now = datetime.now()
        tiempo = now.strftime("%Y%H%M%S")
        
        if _imagen.filename != "":
            nuevoNombreFoto = tiempo+_imagen.filename
            _imagen.save("static/img/"+nuevoNombreFoto)
            
            sql = "INSERT INTO `servicios` (`id`, `titulo`, `precio`, `imagen`) VALUES (NULL, %s, %s, %s);"
            datos = (_titulo,_precio,_imagen)
            conection = mysql.connect()
            cursor = conection.cursor()
            cursor.execute(sql,datos)
            conection.commit()
    
    return render_template("agregarServicio.html", title=titulo)

@app.route("/agendar-cita")
def agendar_cita():
    titulo = "Agendar Cita"
    return render_template("agendarCita.html", title=titulo)

@app.route("/iniciar-sesion", methods=["GET","POST"])
def inicio_sesion():
    titulo = "Iniciar Sesion"
    if request.method == "POST":
        _usuario = request.form["usuario"]
        _contrasegna = request.form["contraseña"]
        
        conection = mysql.connect()
        cursor = conection.cursor()
        sql = "SELEC * FROM `usuario` WHERE usuario = {0} AND contraseña = {1};".format(_usuario,
                                                        check_password_hash(user["contraseña"], _contrasegna))
        cursor.execute(sql)
        user = cursor.fetchone()
        conction.commit()
        session["usuario"] = user["usuario"]
    return render_template("iniciarSesion.html", title=titulo)

@app.route("/salir")
def salir():
    session.clear()
    return redirect(url_for("inicio"))

if __name__ == "__main__":
    app.run(debug=True,port=5500)