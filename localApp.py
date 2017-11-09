import os
from urllib import parse
import psycopg2
from flask import Flask
from flask import request
from flask import render_template
from flask import jsonify
import json
app = Flask(__name__)


conn = psycopg2.connect(
    database='d6p3s2drb04bi5',
    user='ymelghrwalpley',
    password='f1b24c02a5a1b528688ea519c410fb35a7e616003d2949f5a1a66542bb37762e',
    host='ec2-107-22-211-182.compute-1.amazonaws.com',
    port='5432'
)

@app.route('/')
def homepage():
    resultado = "<h3>Por favor ingrese a uno de los siguientes enlaces </h3>"
    resultado += "<p><a href=EstadoDescarga>proyectoredes2.herokuapp.com/EstadoDescarga</a></p>"
    resultado += "<p><a href=Monitoreo>proyectoredes2.herokuapp.com/Monitoreo</a></p>"
    resultado += "<p><a href=AgregarDescarga>proyectoredes2.herokuapp.com/AgregarDescarga</a></p>"
    return resultado;

@app.route('/AgregarDescarga', methods=['GET','POST'])
def agregarDescarga():
    resultado = "<h1>200 ok</h1>"
    if request.method == 'POST':
    	enlace = request.form['enlace']
    	cursor = conn.cursor()
    	cursor.execute("SELECT * FROM descarga WHERE enlace = %s", [enlace]);
    	if cursor.rowcount < 1:
    		cursor.execute("INSERT INTO descarga (enlace) VALUES (%s)", [enlace])
    		conn.commit()
    		if cursor.rowcount < 1:
    			resultado += "<h1>Error 404</h1><p>Error, no se pudo completar la transacción</p>"
    		else:
    			resultado += "<p>Transacción completada</p>"
    	else:
    		resultado += "<h1>Error 404</h1><p>Error, no se pudo completar la transacción</p>"
    	return resultado
    else:
    	return render_template('agregar.html')

@app.route('/<string:recurso>', methods=['GET'])
def mostrar(recurso):
    resultado = "<h1>Datos Obtenidos</h1>"
    cursor = conn.cursor()
    if recurso == "EstadoDescarga":
    	data = 'estadodescarga'
    elif recurso == "Monitoreo":
    	data = 'monitoreo'
    elif recurso == "Descarga":
    	data = 'descarga'
    	cursor.execute("SELECT * FROM " + data)
    	result = cursor.fetchall()
    	resultado = {}
    	i = 0
    	for r in result:
    		resultado['enlace'+ str(i)] = r[0]
    		i+=1
    		cursor.execute("DELETE FROM descarga WHERE enlace=%s", [r[0]])
    		conn.commit()
    	resultado = json.dumps(resultado)
    	return resultado
    else:
        return "<h1>Error 404</h1>"

    cursor.execute("SELECT * FROM " + data)
    result = cursor.fetchall()
    for r in result:
    	resultado += "<p>" + str(r) + "</p>"

    return resultado;

@app.route('/<string:recurso>', methods=['POST'])
def actualizar(recurso):
    resultado = "<h1>200 Ok</h1>"
    cursor = conn.cursor()
    archivo = request.data
    archivo = archivo.decode("utf-8","strict")
    archivo = json.loads(archivo)
    if recurso == "EstadoDescarga":
    	nombre = archivo['nombre']
    	porcentaje = archivo['porcentaje']
    	cursor.execute("SELECT * FROM estadodescarga")
    	if cursor.rowcount < 1:
    		cursor.execute("INSERT INTO estadodescarga (nombre, porcentaje) VALUES (%s, %s)", (nombre, porcentaje));
    		conn.commit()
    	else:
    		cursor.execute("UPDATE estadodescarga SET porcentaje=%s WHERE nombre=%s", [porcentaje,nombre])
    		conn.commit()
    elif recurso == "Monitoreo":
    	kernel = archivo['kernel']
    	cpu = archivo['cpu']
    	swap = archivo['swap']
    	kernelversion = archivo['kernel_version']
    	free = archivo['free']
    	operatingsystem = archivo['operating_system']
    	who = archivo['who']
    	cursor.execute("SELECT * FROM monitoreo")
    	if cursor.rowcount < 1:
    		cursor.execute("INSERT INTO monitoreo (who, kernel, cpu, swap, kernelversion, free, operatingsystem) VALUES (%s, %s, %s, %s, %s, %s, %s)",  [who, kernel, cpu, swap, kernelversion, free, operatingsystem]);
    		conn.commit()
    	else:
    		cursor.execute("UPDATE monitoreo SET kernel=%s, cpu=%s, swap=%s, kernelversion=%s, free=%s, operatingsystem=%s WHERE who=%s", [kernel, cpu, swap, kernelversion, free, operatingsystem, who]) 
    		conn.commit()
    else:
    	resultado = "<h1>Error 404</h1>"

    return resultado;


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)

