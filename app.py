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
from decouple import config
import webbrowser as web
import os

app = Flask(__name__)
mysql = MySQL()

app.config['SECRET_KEY'] = config('SECRET_KEY')
app.config['MYSQL_DATABASE_HOST'] = config('MYSQL_DATABASE_HOST')
app.config['MYSQL_DATABASE_USER'] = config('MYSQL_DATABASE_USER')
app.config['MYSQL_DATABASE_PASSWORD'] = config('MYSQL_DATABASE_PASSWORD')
app.config['MYSQL_DATABASE_DB'] = config('MYSQL_DATABASE_DB')

mysql.init_app(app)

GALERIA = os.path.join('static/galeria')
NOTICIA = os.path.join('static/noticias')
PROMOCION = os.path.join('static/promociones')
SERVICIO = os.path.join('static/servicios')

app.config['GALERIA'] = GALERIA
app.config['NOTICIA'] = NOTICIA
app.config['PROMOCION'] = PROMOCION
app.config['SERVICIO'] = SERVICIO

@app.route("/static/galeria/<nombreFoto>")
def galeria(nombreFoto):
    return send_from_directory(app.config['GALERIA'],nombreFoto)

@app.route('/static/noticias/<nombreFoto>')
def noticia(nombreFoto):
    return send_from_directory(app.config['NOTICIA'],nombreFoto)

@app.route('/static/promociones/<nombreFoto>')
def promocion(nombreFoto):
    return send_from_directory(app.config['PROMOCION'],nombreFoto)

@app.route('/static/servicios/<nombreFoto>')
def servicio(nombreFoto):
    return send_from_directory(app.config['SERVICIO'],nombreFoto)

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

@app.route('/lista-agendados')
def lista_agendados():
    titulo = "Listado de Agendados"
    
    sql = "SELECT * FROM citas"
    conection = mysql.connect()
    cursor = conection.cursor()
    cursor.execute(sql)
    citas = cursor.fetchall()
    
    return render_template("listarCitas.html",title=titulo, citas=citas)

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

@app.route('/editar/<int:id>', methods=['GET','POST'])
def editar(id):
    titulo = "Editar Citas"
    
    conection = mysql.connect()
    cursor = conection.cursor()
    sql = "SELECT * FROM citas WHERE id=%s"
    datos = (id)
    cursor.execute(sql,id)
    citas = cursor.fetchall()
    conection.commit()
    
    return render_template("editarCitas.html", title=titulo, citas=citas)

@app.route('/actualizar', methods=['GET','POST'])
def actualizar():
    if request.method == "POST":
        _nombre = request.form['nombre']
        _numCell = request.form['numCell']
        _servicio = request.form['servicio']
        _colaborado = request.form['colaboradora']
        _fecha = request.form['fecha']
        _id = request.form['id']
        
        sql = "UPDATE citas SET nombre=%s, telefono=%s, servicio=%s, colaboradora=%s, fecha=%s WHERE id=%s"
        datos = (_nombre, _numCell, _servicio, _colaborado, _fecha, _id)
        
        conection = mysql.connect()
        cursor = conection.cursor()
        cursor.execute(sql,datos)
        conection.commit()
        
        return redirect(url_for("lista_agendados"))

@app.route('/elimiar/<int:id>')
def eliminar(id):
    conection = mysql.connect()
    cursor = conection.cursor()
    cursor.execute("DELETE FROM citas WHERE id=%s",(id))
    conection.commit()
    return redirect(url_for("lista_agendados"))

@app.route('/borrar-img-galeria/<int:id>')
def borrar_img_galeria(id):
    conection = mysql.connect()
    cursor = conection.cursor()
    
    cursor.execute("SELECT foto FROM galeria WHERE id=%s",(id))
    fila = cursor.fetchall()
    os.remove(os.path.join(app.config['GALERIA'],fila[0][0]))
              
    cursor.execute("DELETE FROM galeria WHERE id=%s",(id))
    conection.commit()
    
    return redirect(url_for("inicio"))          

@app.route('/borrar-img-noticia/<int:id>')
def borrar_img_noticia(id):
    conection = mysql.connect()
    cursor = conection.cursor()
    
    cursor.execute("SELECT imagen FROM noticiaS WHERE id=%s",(id))
    fila = cursor.fetchall()
    os.remove(os.path.join(app.config['NOTICIA'],fila[0][0]))
              
    cursor.execute("DELETE FROM noticias WHERE id=%s",(id))
    conection.commit()
    
    return redirect(url_for("inicio"))

@app.route('/borrar-img-promocion/<int:id>')
def borrar_img_promocion(id):
    conection = mysql.connect()
    cursor = conection.cursor()
    
    cursor.execute("SELECT imagen FROM promociones WHERE id=%s",(id))
    fila = cursor.fetchall()
    os.remove(os.path.join(app.config['PROMOCION'],fila[0][0]))
              
    cursor.execute("DELETE FROM promociones WHERE id=%s",(id))
    conection.commit()
    
    return redirect(url_for("promociones"))

@app.route('/borrar-servicio/<int:id>')
def borrar_servicio(id):
    conection = mysql.connect()
    cursor = conection.cursor()
    
    cursor.execute("SELECT imagen FROM servicios WHERE id=%s",(id))
    fila = cursor.fetchall()
    os.remove(os.path.join(app.config['SERVICIO'],fila[0][0]))
              
    cursor.execute("DELETE FROM servicios WHERE id=%s",(id))
    conection.commit()
    
    return redirect(url_for("servicios")) 

@app.route('/agendar', methods=['GET','POST'])
def agendar():
    titulo = "Agendar"
    return render_template("agendar.html",title=titulo)   

@app.route('/cita', methods=['GET', 'POST'])
def cita():
    if request.method == "POST":
        _nombre = request.form['nombre']
        _numCell = request.form['num-cell']
        _servicio = request.form['servicio']
        _colaborado = request.form['colaboradora']
        _fecha = request.form['fecha']
        
        sql = """INSERT INTO citas (`id`, `nombre`, `telefono`, `servicio`, `colaboradora`, `fecha`) 
        VALUES (NULL, %s, %s, %s, %s, %s)"""
        datos = (_nombre, _numCell, _servicio, _colaborado, _fecha)
        conection = mysql.connect()
        cursor = conection.cursor()
        cursor.execute(sql,datos)
        conection.commit()
        
        return redirect(url_for("lista_agendados"))

@app.route("/agendar-cita", methods=["GET","POST"])
def agendar_cita():
    titulo = "Agendar Cita"
    
    if request.method == "POST":
        _nombre = request.form["nombre"]
        _apellido = request.form["apellido"]
        _telefono = request.form["numeroTel"]
        _servicio = request.form["servicio"]
        _colaboradora = request.form["colaboradora"]
        _fecha = request.form["fecha"]
        
        if _nombre != "" and _apellido != "" and _telefono != "" and _servicio and _colaboradora != "":
            _mensaje = _nombre+" "+_apellido+" "+_telefono+" "+_servicio+" "+_colaboradora+" "+_fecha
            url = "https://api.whatsapp.com/send?phone=573203410602&text="+_mensaje
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
        
    return render_template("cambiarContraseña.html", title=titulo)

@app.route("/salir")
def salir():
    session.clear()
    return redirect(url_for("inicio"))

if __name__ == "__main__":
    app.run(debug=True,port=config('PORT'))