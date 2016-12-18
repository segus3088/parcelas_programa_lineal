
from pulp import *
import math

class SolverParcelas(object):
	
	numero_meses = 0
	temperatura = {}
	precipitacion = {}
	demanda_minima = {}
	demanda_maxima = {}
	produccion = 0
	valor_x_bulto = 0

	def inicializarValores(self):
		self.numero_meses = 0
		self.temperatura = {}
		self.precipitacion = {}
		self.demanda_minima = {}
		self.demanda_maxima = {}
		self.produccion = 0
		self.valor_x_bulto = 0

	def setNumeroMeses(self, n):
		self.numero_meses = n

	def getNumeroMeses(self):
		return self.numero_meses

	def setTemperatura(self, t):
		self.temperatura = t

	def getTemperatura(self):
		return self.temperatura

	def setPrecipitacion(self, p):
		self.precipitacion = p

	def getPrecipitacion(self):
		return self.precipitacion

	def setDemandaMinima(self, d_min):
		self.demanda_minima = d_min

	def getDemandaMinima(self):
		return self.demanda_minima

	def setDemandaMaxima(self, d_max):
		self.demanda_maxima = d_max

	def getDemandaMaxima(self):
		return self.demanda_maxima

	def setProduccion(self, p):
		self.produccion = p

	def getProduccion(self):
		return self.produccion

	def setValorBulto(self, v):
		self.valor_x_bulto = v

	def getValorBulto(self):
		return self.valor_x_bulto

	def construirVariables(self):
		self.meses = list( range(1, (self.numero_meses+1)) )
		self.cosecha_vars = LpVariable.dicts("cosecha", self.meses, 0, 1, LpInteger)
		self.siembra_vars = LpVariable.dicts("siembra", self.meses, 0, 1, LpInteger)
		self.temperatura_vars = LpVariable.dicts("temperatura", self.meses, 0, 1, LpInteger)
		self.precipitacion_vars = LpVariable.dicts("precipitacion", self.meses, 0, 1, LpInteger)
		# print(self.cosecha_vars)

		self.ingresos = {}
		self.meses_no_temperatura = []
		self.meses_no_precipitacion = []
		for i in self.meses:
			# Calculo de los ingresos
			if self.produccion < self.demanda_minima[i]:
				self.ingresos[i] = (self.produccion*self.valor_x_bulto)/2
			elif self.demanda_minima[i] <= self.produccion and self.produccion <= self.demanda_maxima[i]:
				self.ingresos[i] = self.produccion*self.valor_x_bulto
			else:
				self.ingresos[i] = (self.demanda_maxima[i]*self.valor_x_bulto) + ((self.produccion-self.demanda_maxima[i])*(self.valor_x_bulto/2))

			# Determina temperatura de siembra
			if 18>self.temperatura[i] or self.temperatura[i]>20:
				self.meses_no_temperatura.append(i)

			if self.precipitacion[i]<63 :
				self.meses_no_precipitacion.append(i)

	def solucionar(self):
		self.construirVariables()
		problema = LpProblem("Cultivo de papa", LpMaximize)
		# problema = LpProblem("Cultivo de papa", LpMinimize)

		# FUNCION OBJETIVO
		problema += lpSum([self.ingresos[i]*self.cosecha_vars[i] for i in self.meses])

		# RESTRICCIONES
		# Sumatoria de cosechas es <= N/4
		problema += lpSum([self.cosecha_vars[i] for i in self.meses]) <= math.floor(self.numero_meses/4)

		# Cumplir el ciclo: X(i) + X(i+1) + X(i+2) + X(i+3) <= 1
		problema += self.cosecha_vars[1]+self.cosecha_vars[2]+self.cosecha_vars[3] == 0
		for i in range(1, self.numero_meses-2):
			problema += self.cosecha_vars[i]+self.cosecha_vars[i+1]+self.cosecha_vars[i+2]+self.cosecha_vars[i+3] <= 1

		# No cumple las condiciones de temperatura
		problema += lpSum([self.temperatura_vars[i] for i in self.meses_no_temperatura]) == 0.0
		
		# No cumple las condiciones de precipitacion
		problema += lpSum([self.precipitacion_vars[i] for i in self.meses_no_precipitacion]) == 0.0

		# CONDICIONES CLIMATICAS
		M = 100
		for i in self.meses:
			problema += self.siembra_vars[i] <= 0+M*self.temperatura_vars[i]
			problema += self.siembra_vars[i] <= 0+M*self.precipitacion_vars[i]
			# Cosecho en 3 meses
			if i<=(self.numero_meses-3):
				problema += self.siembra_vars[i] == self.cosecha_vars[i+3]


		# problema.writeLP('problema.txt')

		# print("##### PROBLEMA #####")
		# print(problema)

		# print("##### SOLUCION #####")
		status = problema.solve()
		# status = problema.solve(GLPK())
		# LpStatus[status]
		# print("status:", LpStatus[status])
		# print("objective:", value(problema.objective) )

		# print("--- VALORES ---")
		solucion = [ value(problema.objective) ]
		meses_cosecha = []
		for x in self.meses:
			# print(self.cosecha_vars[x], ":", value( self.cosecha_vars[x]) )
			if value( self.cosecha_vars[x])>0:
				meses_cosecha.append(x)
		solucion.append(meses_cosecha)
		return solucion
