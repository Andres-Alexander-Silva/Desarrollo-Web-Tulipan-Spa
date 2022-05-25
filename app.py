from flask import Flask
from flask import render_template
from flask import url_for
from config import DevelopmentConfig

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)

@app.route("/")
@app.route("/inicio")
def inicio():
    titulo = "Tulipan Spa"
    return render_template("inicio.html", title=titulo)

@app.route("/acerca-de")
def acerca_de():
    titulo = "Acerca de"
    return render_template("acercaDe.html", title=titulo)

@app.route("/servicios")
def servicios():
    titulo = "Servicios"
    return render_template("servicios.html", title=titulo)

@app.route("/promociones")
def promociones():
    titulo = "Promociones"
    return render_template("promociones.html", title=titulo)

@app.route("/agregar-imagen", methods=["GET","POST"])
def agregar_img():
    titulo = "Agregar Imagen"
    return render_template("agregarImagen.html", title=titulo)

@app.route("/agregar-noticia", methods=["GET","POST"])
def agregar_noticia():
    titulo = "Agregar Noticia"
    return render_template("agregarNoticia.html", title=titulo)

@app.route("/agregar-Promocion", methods=["GET","POST"])
def agregar_promocion():
    titulo = "Agregar Promocion"
    return render_template("agregarPromocion.html", title=titulo)

@app.route("/agregar-servicio", methods=["GET","POST"])
def agregar_servicio():
    titulo = "Agregar Servicio"
    return render_template("agregarServicio.html", title=titulo)

@app.route("/agendar-cita")
def agendar_cita():
    titulo = "Agendar Cita"
    return render_template("agendarCita.html", title=titulo)

@app.route("/iniciar-sesion", methods=["GET","POST"])
def inicio_sesion():
    titulo = "Iniciar Sesion"
    return render_template("iniciarSesion.html", title=titulo)

if __name__ == "__main__":
    app.run(port=5500)