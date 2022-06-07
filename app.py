from flask import Flask
from flask import render_template
from flask import url_for
from flask import request
from flask import session
from flask import redirect
from flask import flash
from flask import send_from_directory
from flaskext.mysql import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import webbrowser as web
import os

app = Flask(__name__)
mysql = MySQL()

app.config['SECRET_KEY'] = "myScretKeyTulipanSpaAndresSilva"
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'tulipanspa'

mysql.init_app(app)

CARPETA = os.path.join('website-TulipanSpa/static/galeria')
app.config['CARPETA'] = CARPETA

@app.route("/website-TulipanSpa/static/galeria/<nombreFoto>")
def galeria(nombreFoto):
    return send_from_directory(app.config['CARPETA'],nombreFoto)

@app.route("/")
@app.route("/inicio")
def inicio():
    titulo = "Tulipan Spa"
    
    sql = "SELECT * FROM galeria"
    conection = mysql.connect()
    cursor = conection.cursor()
    cursor.execute(sql)
    imagenes = cursor.fetchall()
    
    sql = "SELECT * FROM noticias"
    conection = mysql.connect()
    cursor = conection.cursor()
    cursor.execute(sql)
    noticias = cursor.fetchall()
    
    return render_template("inicio.html", title=titulo, imagenes=imagenes, noticias=noticias)

@app.route("/servicios")
def servicios():
    titulo = "Servicios"
    
    sql = "SELECT * FROM servicios"
    conection = mysql.connect()
    cursor = conection.cursor()
    cursor.execute(sql)
    servicios = cursor.fetchall()
    
    return render_template("servicios.html", title=titulo, servicios=servicios)

@app.route("/promociones", methods=["GET","POST"])
def promociones():
    titulo = "Promociones"
    
    sql = "SELECT * FROM promociones"
    conection = mysql.connect()
    cursor = conection.cursor()
    cursor.execute(sql)
    promociones = cursor.fetchall()
    
    return render_template("promociones.html", title=titulo, promociones=promociones)

@app.route("/agregar-imagen", methods=["GET","POST"])
def agregar_img():
    titulo = "Agregar Imagen"
    
    if request.method == "POST":
        _imagen = request.files["img-galery"]
        now = datetime.now()
        tiempo = now.strftime("%Y%H%M%S")
        
        if _imagen.filename != '':
            nuevoNombreFoto = tiempo+_imagen.filename
            _imagen.save("static/galeria/"+nuevoNombreFoto)
            
        sql = "INSERT INTO `galeria` (`id`, `foto`) VALUES (NULL, %s);"
        datos = (nuevoNombreFoto)
        conection = mysql.connect()
        cursor = conection.cursor()
        cursor.execute(sql,datos)
        conection.commit()
        
        return redirect(url_for("inicio")) 
        
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
            _imagen.save("static/noticias/"+nuevoNombreFoto)
            
            sql = "INSERT INTO `noticias` (`id`, `imagen`) VALUES (NULL, %s);"
            datos = (nuevoNombreFoto)
            conection = mysql.connect()
            cursor = conection.cursor()
            cursor.execute(sql,datos)
            conection.commit()
            
            return redirect(url_for("inicio")) 
            
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
            _imagen.save("static/promociones/"+nuevoNombreFoto)
            
            sql = "INSERT INTO `promociones` (`id`, `imagen`) VALUES (NULL, %s);"
            datos = (nuevoNombreFoto)
            conection = mysql.connect()
            cursor = conection.cursor()
            cursor.execute(sql,datos)
            conection.commit()
            
            return redirect(url_for("promociones")) 
    
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
            _imagen.save("static/servicios/"+nuevoNombreFoto)
            
            sql = "INSERT INTO `servicios` (`id`, `titulo`, `precio`, `imagen`) VALUES (NULL, %s, %s, %s);"
            datos = (_titulo,_precio,nuevoNombreFoto)
            conection = mysql.connect()
            cursor = conection.cursor()
            cursor.execute(sql,datos)
            conection.commit()
            
            return redirect(url_for("servicios")) 
    
    return render_template("agregarServicio.html", title=titulo)

@app.route("/agendar-cita", methods=["GET","POST"])
def agendar_cita():
    titulo = "Agendar Cita"
    
    if request.method == "POST":
        _nombre = request.form["nombre"]
        _apellido = request.form["apellido"]
        _telefono = request.form["numeroTel"]
        _servicio = request.form["servicio"]
        _colaboradora = request.form["colaboradora"]
        
        if _nombre != "" and _apellido != "" and _telefono != "" and _servicio and _colaboradora != "":
            _mensaje = _nombre+" "+_apellido+"\n"+_telefono+"\n"+_servicio+"\n"+_colaboradora
            url = "https://api.whatsapp.com/send?phone=573016570792&text="+_mensaje
            web.open_new(url)
        
    return render_template("agendarCita.html", title=titulo)

@app.route("/iniciar-sesion", methods=["GET","POST"])
def inicio_sesion():
    titulo = "Iniciar Sesion"
    
    if request.method == "POST":
        _usuario = request.form["usuario"]
        _contrasegna = request.form["contraseña"]
        
        sql = "SELECT * FROM usuarios WHERE usuario = %s;"
        datos = (_usuario)
        conection = mysql.connect()
        cursor = conection.cursor()
        cursor.execute(sql,datos)
        user = cursor.fetchone()
        
        if user:
            if _usuario == user[1] and check_password_hash(user[2], _contrasegna):
                session["usuario"] = user[1]
                return redirect(url_for("inicio"))
               
        conection.commit()
        
    return render_template("iniciarSesion.html", title=titulo)

@app.route("/cambiar-contraseña", methods=["GET","POST"])
def cambio_contraseña():
    titulo = "Cambiar Contraseña"
    
    if request.method == "POST":
        _usuario = request.form["usuario"]
        _newPassword = request.form["contraseña-new"]
        _newPasswordEncriptada = generate_password_hash(_newPassword)
        
        sql = "UPDATE usuarios SET contraseña = %s WHERE usuario = %s"
        datos = (_newPasswordEncriptada,_usuario)
        conection = mysql.connect()
        cursor = conection.cursor()
        cursor.execute(sql,datos)
        conection.commit()
        
        #return redirect(url_for("inicio_sesion"))
        
    return render_template("cambiarContraseña.html", title=titulo)

@app.route("/salir")
def salir():
    session.clear()
    return redirect(url_for("inicio"))

if __name__ == "__main__":
    app.run(debug=True,port=5500)