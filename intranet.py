import urllib2
import json
import requests
from flask import jsonify
import transmissionrpc

def main():
	monitoreo = urllib2.urlopen("http://0.0.0.0:5001/who")
	monitoreo = json.loads(monitoreo.read())
	who = monitoreo['users']
	monitoreo = urllib2.urlopen("http://0.0.0.0:5001/os")
	os = monitoreo.read()
	os = json.loads(os)
	kernel = os['kernel']
	kernelversion = os['kernel_version']
	operatingsystem = os['operating_system']
	monitoreo = urllib2.urlopen("http://0.0.0.0:5001/cpu/us")
	monitoreo = json.loads(monitoreo.read())
	cpu = monitoreo['cpu us']
	monitoreo = urllib2.urlopen("http://0.0.0.0:5001/mem/swpd")
	monitoreo = json.loads(monitoreo.read())
	swap = monitoreo['mem swpd']
	monitoreo = urllib2.urlopen("http://0.0.0.0:5001/mem/free")
	monitoreo = json.loads(monitoreo.read())
	free = monitoreo['mem free']
	message = {}
	message['who'] = who.replace('\n','')
	message['kernel'] = kernel.replace('\n','')
	message['kernel_version'] = kernelversion.replace('\n','')
	message['operating_system'] = operatingsystem.replace('\n','')
	message['free'] = free.replace('\n','')
	message['swap'] = swap.replace('\n','')
	message['cpu'] = cpu.replace('\n','')
	message = json.dumps(message)
	solicitud = requests.post("http://proyectoredes2.herokuapp.com/Monitoreo", message)
	print(solicitud.status_code, solicitud.reason)
	tconn = transmissionrpc.Client('localhost', port=9091, user='transmission', password='transmission')
	tconn.get_torrents()
	descargas = urllib2.urlopen("http://proyectoredes2.herokuapp.com/Descarga")
	descargas = json.loads(descargas.read())
	for i in range(len(descargas)):
		tconn.add_torrent(descargas['enlace'+str(i)])
	for torrent in tconn.get_torrents() :
		nombre = torrent.name
		nombre = nombre.replace('+',' ')
		porcentaje = str(torrent.metadataPercentComplete)
		message = {}
		message['nombre'] = nombre
		message['porcentaje'] = porcentaje
		message = json.dumps(message)
		solicitud = requests.post("http://proyectoredes2.herokuapp.com/EstadoDescarga", message)
		print(solicitud.status_code, solicitud.reason)


if __name__=='__main__':
	main()
