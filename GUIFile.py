
from tkinter import *
import tkinter.filedialog as tkf
from time import time
import random
import copy

from SolverParcelas import SolverParcelas

class GUIFile(Frame):
	
	def __init__(self, parent):
		Frame.__init__(self, parent)
		self.parent = parent
		self.initUI()

	def initUI(self):
		self.solverParcelas = SolverParcelas()
		self.parent.title("CULTIVO DE PARCELAS")
		Button(self.parent, text="Cargar Archivo", command=self.abrirArchivo).grid(row=0, column=0)
		
		Label(self.parent, text="Archivo:").grid(row=0, column=1)
		self.vsRutaArchivo = StringVar()
		Label(self.parent, textvariable=self.vsRutaArchivo).grid(row=0, column=2, columnspan=50)

		for fila in range(7):
			fila += 1
			if fila == 1:
				Label(self.parent, text="Número de parcelas:").grid(row=fila, column=0, sticky=W)
				self.vsNumeroMeses = StringVar()
				Label(self.parent, textvariable=self.vsNumeroMeses).grid(row=fila, column=2, columnspan=50, sticky=W)
			elif fila == 2:
				Label(self.parent, text="Tiempos cultipo por parcela:").grid(row=fila, column=0, sticky=W)
				self.vsTemperatura = StringVar()
				Label(self.parent, textvariable=self.vsTemperatura).grid(row=fila, column=2, columnspan=50, sticky=W)
			elif fila == 3:
				Label(self.parent, text="Tiempo Total:").grid(row=fila, column=0, sticky=W)
				self.vsPrecipitacion = StringVar()
				Label(self.parent, textvariable=self.vsPrecipitacion).grid(row=fila, column=2, columnspan=50, sticky=W)
			elif fila == 4:
				Label(self.parent, text="Beneficios parcela #:").grid(row=fila, column=0, sticky=W)
				self.vsDemandaMinima = StringVar()
				Label(self.parent, textvariable=self.vsDemandaMinima).grid(row=fila, column=2, columnspan=50, sticky=W)
			elif fila == 5:
				Label(self.parent, text="Beneficios parcela #").grid(row=fila, column=0, sticky=W)
				self.vsDemandaMaxima = StringVar()
				Label(self.parent, textvariable=self.vsDemandaMaxima).grid(row=fila, column=2, columnspan=50, sticky=W)
			elif fila == 6:
				Label(self.parent, text="Beneficios parcela #:").grid(row=fila, column=0, sticky=W)
				self.vsProduccion = StringVar()
				Label(self.parent, textvariable=self.vsProduccion).grid(row=fila, column=2, columnspan=50, sticky=W)
			elif fila == 7:
				Label(self.parent, text="Beneficios parcela #:").grid(row=fila, column=0, sticky=W)
				self.vsValorPorBulto = StringVar()
				Label(self.parent, textvariable=self.vsValorPorBulto).grid(row=fila, column=2, columnspan=50, sticky=W)

		Button(self.parent, text="Solucionar", command=self.solucionarProblema).grid(row=8, column=0)
		Button(self.parent, text="Solucionar y escribir", command=self.solucionarProblemaEscribir).grid(row=8, column=1)

		Label(self.parent, text="Tiempo de solucion (seg.):").grid(row=9, column=0, sticky=W)
		self.vsTiempoSolucion = StringVar()
		Label(self.parent, textvariable=self.vsTiempoSolucion).grid(row=9, column=2, columnspan=50, sticky=W)

		Label(self.parent, text="Ingresos totales recibidos:").grid(row=10, column=0, sticky=W)
		self.vsIngresos = StringVar()
		Label(self.parent, textvariable=self.vsIngresos).grid(row=10, column=2, columnspan=50, sticky=W)

		Label(self.parent, text="Número de meses de cosecha:").grid(row=11, column=0, sticky=W)
		self.vsNumeroMesesCosecha = StringVar()
		Label(self.parent, textvariable=self.vsNumeroMesesCosecha).grid(row=11, column=2, columnspan=50, sticky=W)

		Label(self.parent, text="Meses de cosecha:").grid(row=12, column=0, sticky=W)
		self.vsMesesCosecha = StringVar()
		Label(self.parent, textvariable=self.vsMesesCosecha).grid(row=12, column=2, columnspan=50, sticky=W)

	def leerArchivo(self, ruta):
		if ruta != '':
			fila = 1
			archivo = open(ruta, "r")
			for linea in archivo.readlines():
				linea = linea.replace("\n", "")
				
				if fila == 1:
					self.vsNumeroMeses.set(linea)
					self.num_meses = int(linea)
				elif fila == 2:
					self.vsTemperatura.set(linea)
					temperatura_entrada = linea.split(" ")
					self.temperatura = {}
					for index in range( len(temperatura_entrada) ):
						self.temperatura[(index+1)] = int(temperatura_entrada[index])
				elif fila == 3:
					self.vsPrecipitacion.set(linea)
					precipitacion_entrada = linea.split(" ")
					self.precipitacion = {}
					for index in range( len(precipitacion_entrada) ):
						self.precipitacion[(index+1)] = int(precipitacion_entrada[index])
				elif fila == 4:
					self.vsDemandaMinima.set(linea)
					demanda_min_entrada = linea.split(" ")
					self.demanda_min = {}
					for index in range( len(demanda_min_entrada) ):
						self.demanda_min[(index+1)] = int(demanda_min_entrada[index])
				elif fila == 5:
					self.vsDemandaMaxima.set(linea)
					demanda_max_entrada = linea.split(" ")
					self.demanda_max = {}
					for index in range( len(demanda_max_entrada) ):
						self.demanda_max[(index+1)] = int(demanda_max_entrada[index])
				elif fila == 6:
					self.vsProduccion.set(linea)
					self.produccion = int(linea)
				elif fila == 7:
					self.vsValorPorBulto.set(linea)
					self.valor_x_bulto = int(linea)

				fila += 1

			self.solverParcelas.setNumeroMeses(self.num_meses)
			self.solverParcelas.setTemperatura(self.temperatura)
			self.solverParcelas.setPrecipitacion(self.precipitacion)
			self.solverParcelas.setDemandaMinima(self.demanda_min)
			self.solverParcelas.setDemandaMaxima(self.demanda_max)
			self.solverParcelas.setProduccion(self.produccion)
			self.solverParcelas.setValorBulto(self.valor_x_bulto)
				

	def abrirArchivo(self):
		file_types = [('Archivos TXT', '*.txt')]
		ventana_dialogo = tkf.Open(self, filetypes = file_types)
		ruta_archivo = ventana_dialogo.show()
		self.vsRutaArchivo.set(ruta_archivo)
		self.solverParcelas.inicializarValores()

		self.vsTiempoSolucion.set("")
		self.vsIngresos.set("")
		self.vsNumeroMesesCosecha.set("")
		self.vsMesesCosecha.set("")

		self.leerArchivo(ruta_archivo)

	def solucionarProblema(self):
		solucion = None
		tiempo_inicio = time()
		solucion = self.solverParcelas.solucionar()
		tiempo_total = time() - tiempo_inicio
		self.vsTiempoSolucion.set(tiempo_total)
		self.mostrarSolucion(solucion)
	
	def solucionarProblemaEscribir(self):
		solucion = None
		tiempo_inicio = time()
		solucion = self.solverParcelas.solucionar()
		tiempo_total = time() - tiempo_inicio
		self.vsTiempoSolucion.set(tiempo_total)
		self.mostrarSolucion(solucion)
		self.escribirSolucion(solucion)

	def mostrarSolucion(self, solucion):
		if solucion != None:
			self.vsIngresos.set( str(solucion[0]) )
			self.vsNumeroMesesCosecha.set( str(len(solucion[1])) )
			meses_cosecha = []
			for un_mes in solucion[1]:
				meses_cosecha.append( str(un_mes) )
			self.vsMesesCosecha.set( " - ".join(meses_cosecha) )

	def escribirSolucion(self, solucion):
		if solucion != None:
			ruta = self.vsRutaArchivo.get()
			ruta_solucion = ruta.replace(".txt", "_sol.txt")
			archivo = open(ruta_solucion, "w")
			archivo.write( str(solucion[0])+"\n" )
			archivo.write( str(len(solucion[1]))+"\n" )
			for i in solucion[1]:
				archivo.write( str(i)+"\n" )