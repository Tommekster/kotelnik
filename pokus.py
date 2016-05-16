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

class mTime:
	def __init__(self,_h,_m):
		self.h=_h
		self.m=_m

class mDay:
	def __init__(self):
		pass

	def setStartTime(self,h,m):
		setattr(self,'start',mTime(h,m))

	def setStopTime(self,h,m):
		setattr(self,'stop',mTime(h,m))

	def setStartStop(self,h,m,hh,mm):
		setattr(self,'start',mTime(h,m))
		setattr(self,'stop',mTime(hh,mm))


class mWeek:
	def __init__(self):
		self.days=[mDay() for i in range(0,7)]
	
	#def getDay(self,index):
	#	return self.days[index]

	def isTimeForHeating():
		day = self.days[time.localtime().tm_wday]
		# if 

class Kotelnik:
	def __init__(self):
		self.out_temperature = 15.0	# je-li venku vyssi teplota, tak netopi
		self.pipes_temperature = 30.0	# je-li trubka ohrata, tak kotel topi
		self.week = mWeek()
		self.week.days[0].setStartStop(5,0,22,30)	# casy na vytapeni behem tydne
		self.week.days[1].setStartStop(5,0,22,30)
		self.week.days[2].setStartStop(5,0,22,30)
		self.week.days[3].setStartStop(5,0,22,30)
		self.week.days[4].setStartStop(5,0,23,59)
		self.week.days[5].setStartStop(8,0,23,59)
		self.week.days[6].setStartStop(8,0,23,0)
		self.timeout_interval = 3600	# kdyz bude podle trubek natopeno, jak dlouho ma kotel odpocivat
		self.filterWeight = 1/32	# parametr dolnopropustoveho filtru
		self.referenceVoltage=1.1	# referencni napeti pro mereni referencnich "5V"
		self.temperatures = [15.0 for i in range(0,6)]	# vychozi teploty, aby predesli selhani

	def refreshTemperature(self):
		try:
			sens = readSens()	# ziskam hodnoty ze senzoru
		except (sensorError,connectionError):
			return
		pom = sens[-2]		# pomer merice VCC
		vcc = sens[-1]		# hodnota na merici VCC pri VREF
		rawTemps = [s/10.24*vcc/pom*1.1-273 for s in sens[:-2]]	# prepocet hodnot senzoru do stupni Celsia
		newTemps = [self.temperatures[i] + (rawTemps[i] - self.temperatures[i])*self.filterWeight for i in range(0,6)]
		

if __name__ == '__main__':
	print('Pokus: uvidime, co zmuzeme s kotelnikem.')
