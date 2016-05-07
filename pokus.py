#!/usr/bin/python3
#import time		# time.sleep(5.5)
import http.client
import time

logCtrlFile = '/tmp/kotelctl.log'

class connectionError(RuntimeError):
	def __init__(self, arg):
		self.args = arg
class sensorError(RuntimeError):
	def __init__(self, arg):
		self.args = arg

def logCtrl(str):
	file = open(logCtrlFile,'a')
	file.write(str)
	
def kotelOn():
	conn = http.client.HTTPConnection('192.168.11.99')	# nastavim spojeni na maleho kotelnika
	conn.request('GET','/on')				# necham kotel zapnout
	logCtrl(time.strftime('%d.%m.%Y %H:%M')+' ON')

def kotelOff():
	conn = http.client.HTTPConnection('192.168.11.99')	# nastavim spojeni na maleho kotelnika
	conn.request('GET','/off')				# necham kotel vypnout
	logCtrl(time.strftime('%d.%m.%Y %H:%M')+' ON')

def readSens(loc=0):
	if loc:
		data1 = b'<html><head><title>Kotelnik Senzory</title></head><body><h2>Senzory</h2><pre>\n609\n665\n674\n653\n697\n666\n174\n747\n</pre><hr></body></html>'
	else:
		conn = http.client.HTTPConnection('192.168.11.99')	# nastavim spojeni na maleho kotelnika
		conn.request('GET','/sens')				# pozadem o GET /sens
		r1 = conn.getresponse()					# ziskam vysledek
		if r1.status != 200:					# skontroluji status vysledku
			raise connectionError('/sens is not 200 OK')
		data1 = r1.read()					# vezmu si data
	sens_str = data1.decode('utf8')				# preveduje na string
	sens = sens_str.split('\n')				# rozdelim je podle odradkovani
	if len(sens) < 10: 					# mam-li mene radku, asi se zrovna Atmel resetuj
		raise sensorError('Dostal jsem malo dat.',sens)
	del(sens[-1])						# odstranim HTML paticku
	del(sens[0])						# odstranim HTML hlavicku
	return [int(s) for s in sens]

if __name__ == '__main__':
	print('Pokus: uvidime, co zmuzeme s kotelnikem.')
