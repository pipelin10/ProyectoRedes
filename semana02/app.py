import os
from datetime import datetime
from urllib import parse
import psycopg2
from flask import Flask
from flask import request
app = Flask(__name__)

parse.uses_netloc.append("postgres")
url = parse.urlparse(os.environ["DATABASE_URL"])

conn = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
)

@app.route('/')
def homepage():
    resultado = "<h3>Por favor ingrese a uno de los siguientes enlaces </h3>"
    resultado += "<p>proyectoredes2.herokuapp.com/EstadoDescarga</p>"
    resultado += "<p>proyectoredes2.herokuapp.com/Monitoreo</p>"
    resultado += "<p>proyectoredes2.herokuapp.com/Descarga/JSON_FORMAT</p>"
    resultado += "<p>proyectoredes2.herokuapp.com/Monitoreo/JSON_FORMAT</p>"
    resultado += "<p>proyectoredes2.herokuapp.com/EstadoDescarga/JSON_FORMAT</p>"
    return resultado;

@app.route('/<string:recurso>')
def mostrar(recurso):
    resultado = "<h1>Datos Obtenidos</h1>"
    cursor = conn.cursor()
    if recurso == "EstadoDescarga":
    	data = 'estadodescarga'
    elif recurso == "Monitoreo":
    	data = 'monitoreo'
    else:
        return "<h1>Error 404</h1>"

    cursor.execute("SELECT * FROM " + data)
    result = cursor.fetchall()
    for r in result:
    	resultado += "<p>" + str(r) + "</p>"

    return resultado;

@app.route('/<string:recurso>/<string:archivo>')
def actualizar(recurso,archivo):
    resultado = "<h1>200 Ok</h1>"
    cursor = conn.cursor()
    
    if recurso == "Descarga":
    	archivo = archivo.split("{")
    	archivo = archivo[1].split("}")
    	archivo = archivo[0].split(",")
    	enlace = archivo[0].split(':')
    	enlace = enlace[1][1:].replace('"', '')
    	fecha = datetime.now()
    	cursor.execute("INSERT INTO descarga (enlace, fecha) VALUES (%s, %s)", (enlace, fecha));
    	conn.commit()
    elif recurso == "EstadoDescarga":
    	archivo = archivo.split("{")
    	archivo = archivo[1].split("}")
    	archivo = archivo[0].split(",")
    	nombre = archivo[0].split(':')
    	nombre = nombre[1][1:]
    	porcentaje = archivo[1].split(':')
    	porcentaje = porcentaje[1][2:]
    	print(nombre)
    	print(porcentaje)
    	cursor.execute("INSERT INTO estadodescarga (nombre, porcentaje) VALUES (%s, %s)", (nombre, porcentaje));
        conn.commit()
    elif recurso == "Monitoreo":
    	archivo = archivo.split("{")
    	archivo = archivo[1].split("}")
    	archivo = archivo[0].split(",")
    	kernel = archivo[0].split(':')
    	kernel = kernel[1][1:]
    	cpu = archivo[1].split(':')
    	cpu = cpu[1][1:]
    	swap = archivo[2].split(':')
    	swap = swap[1][1:]
    	kernelversion = archivo[3].split(':')
    	kernelversion = kernelversion[1][1:]
    	free = archivo[4].split(':')
    	free = free[1][1:]
    	operatingsystem = archivo[5].split(':')
    	operatingsystem = operatingsystem[1][1:]
    	cursor.execute("INSERT INTO monitoreo (kernel, cpu, swap, kernelversion, free, operatingsystem)VALUES (%s, %s, %s, %s, %s, %s)",  (kernel, cpu, swap, kernelversion, free, operatingsystem));
    	conn.commit()
    else:
    	resultado = "<h1>Error 404</h1>"


    return resultado;

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)

