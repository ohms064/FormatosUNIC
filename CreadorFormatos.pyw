from libs.Templates.InscripcionTemplate import Inscripcion
from libs.Templates.PAETemplate import PAE
import tkinter as tk
from tkinter import messagebox as mb
from libs.CustomTK import UserForm
from tkinter import messagebox as mb
from tkinter import filedialog as fd
from collections import defaultdict
import os
import subprocess 
import json
import datetime


def Update():
	pull = subprocess.Popen('git pull', stdout=subprocess.PIPE,)
	stdout_value = pull.communicate()[0]
	print ('\tstdout:' + repr(stdout_value))

	if "Already up-to-date." in str(stdout_value):
		return

	log = subprocess.Popen("git log -1 --pretty=%B", stdout=subprocess.PIPE,)
	stdout_value = log.communicate()[0]

	mb.showinfo("Actualización", str(stdout_value))


class FormatosGUI(tk.Frame):
	"""
		Ventana principal donde se sacaran nuevas comandas y se hará el cierre de caja
	"""
	def __init__(self, master=None):
		tk.Frame.__init__(self, master)
		self.master.title("Formatos UNIC")
		self.master.geometry("300x25")
		#self.pack()
		master.protocol("WM_DELETE_WINDOW", self.OnCloseWindow)
		self._manager = Manager()
		self.done = tk.BooleanVar()
		self.done.set(False)
		self.CreateMenu()
		self.CreateWidgets()

	def CreateWidgets(self):
		self.frame = tk.Frame(self.master)
		self.frame.grid(row=0, column=0)

	def CreateMenu(self):
		self.menubar = tk.Menu(self.master)

		self.fileMenu = tk.Menu(self.menubar, tearoff=0)
		self.fileMenu.add_command(label="Salir", command=self.OnCloseWindow)

		self.formatosMenu = tk.Menu(self.menubar, tearoff=0)
		self.formatosMenu.add_command(label="Inscripción", command=self.AbrirInscripcion)
		self.formatosMenu.add_command(label="PAE", command=self.AbrirPAE)

		self.configMenu = tk.Menu(self.menubar, tearoff=0)
		self.configMenu.add_command(label="Folder Inscripción", command=self.CambiarDestino(self.master, self._manager.inscripcionJSON, title="Inscripción"))
		self.configMenu.add_command(label="Folder PAE", command=self.CambiarDestino(self.master, self._manager.paeJSON, title="PAE"))
		self.configMenu.add_separator()
		self.configMenu.add_command(label="Excel Inscripción", command=self.CambiarDestino(self.master, self._manager.inscripcionJSON, csv=True, title="Inscripcion"))
		self.configMenu.add_command(label="Excel PAE", command=self.CambiarDestino(self.master, self._manager.paeJSON, csv=True, title="PAE"))

		self.menubar.add_cascade(label="Archivo", menu=self.fileMenu)
		self.menubar.add_cascade(label="Formatos", menu=self.formatosMenu)
		self.menubar.add_cascade(label="Configuración", menu=self.configMenu)
		
		self.master.config(menu=self.menubar)

	def CambiarDestino(self, master, configFile, csv=False, title="Escoge un archivo"):
		def File():
			dirname = fd.askdirectory(parent=master, mustexist=True, title=title)
			if dirname != "":
				configFile["Output"] = dirname

		def CSV():
			dirname = fd.askdirectory(parent=master, mustexist=True, title=title)
			if dirname != "":
				dirname += "/{}".format(configFile["CSV"][configFile["CSV"].rfind("/") + 1:] )
				configFile["CSV"] = dirname

		if csv:
			return CSV
		return File

	def AbrirInscripcion(self):
		self.frame.destroy()
		self.CreateWidgets()
		keys = self._manager.inscripcionJSON["Labels"]
		dateKeys = self._manager.inscripcionJSON["Date"]
		fileKeys = self._manager.inscripcionJSON["Files"]
		choicesDict = self._manager.generalJSON["Choices"]
		choicesDict.update(self._manager.inscripcionJSON["Choices"])
		defaultDict = {"Semestre": self._manager.generalJSON["Semestre"]}
		UserForm(self.frame, self.done, rows=13, col_size=5, \
			keyLabels=keys, dateBox=dateKeys, fileBox=fileKeys, \
			choices=choicesDict, defaultValues=defaultDict, formValues=self._manager.inscripcion.data)
		self.frame.grid(row=0, column=0)
		self.master.geometry("1700x375")
		self.master.wait_variable(self.done)
		self.done.set(False)
		self.CrearFormatoInscripcion()

	def AbrirPAE(self):
		self.frame.destroy()
		self.CreateWidgets()
		keys = self._manager.paeJSON["Labels"]
		dateKeys = self._manager.paeJSON["Date"]
		fileKeys = self._manager.paeJSON["Files"]
		choicesDict = self._manager.paeJSON["Choices"]
		choicesDict.update(self._manager.generalJSON["Choices"])
		defaultDict = {"Semestre": self._manager.generalJSON["Semestre"]}
		UserForm(self.frame, self.done, rows=6, col_size=5, \
			keyLabels=keys, dateBox=dateKeys, fileBox=fileKeys, \
			choices=choicesDict, defaultValues=defaultDict, formValues=self._manager.pae.data)
		self.frame.grid(row=0, column=0)
		self.master.geometry("600x225")
		self.master.wait_variable(self.done)
		self.done.set(False)
		self.CrearFormatoPAE()

	def CrearFormatoInscripcion(self):
		self._manager.CreateInscripcion()
		self.AbrirInscripcion()

	def CrearFormatoPAE(self):
		self._manager.CreatePAE()
		self.AbrirPAE()

	def OnCloseWindow(self):
		del self._manager
		self.master.destroy()
		self.master.quit()

def BeginLoop():
	root = tk.Tk()
	app = FormatosGUI(master=root)
	app.mainloop()

def CreateDirs():
	os.makedirs("Config", exist_ok=True)
	#os.makedirs("libs/Errors", exist_ok=True)
	os.makedirs("Outputs", exist_ok=True)
	os.makedirs("Imagenes", exist_ok=True)

class Manager():
	def __init__(self):
		self.today = datetime.date.today()
		self.inscripcion = Inscripcion()
		self.pae = PAE()
		self.InitConfFiles()
		csvLabels = self.inscripcionJSON["Labels"].copy()
		csvLabels.remove("Foto")
		self.inscripcionCSV = CSVTable(self.inscripcionJSON["CSV"], csvLabels)
		csvLabels = self.paeJSON["Labels"].copy()
		csvLabels.remove("Foto")
		self.paeCSV = CSVTable(self.paeJSON["CSV"], csvLabels)
		del csvLabels

	def InitConfFiles(self):
		try:
			with open("Config/general.conf", "r", encoding='utf8') as archConf:
				self.generalJSON = json.load(archConf)
				self.generalJSON["Semestre"] = "{}-1".format(self.today.year) if int(self.today.month) > 6 else "{}-2".format(self.today.year - 1)

		except (FileNotFoundError, ValueError) as err:
			with open("Config/general.conf", "w", encoding='utf8') as archConf:
				self.generalJSON = {"Choices" : {"Licenciatura": ["Educación","Comercio Internacional", "Contador Público", "Ingeneiría Industrial", "Ciencias de la Comunicación", "Derecho", "Mercadotecnia y Publicidad", "Recursos Humanos"] }}
				self.generalJSON["Semestre"] = "{}-1".format(self.today.year) if int(self.today.month) > 6 else "{}-2".format(self.today.year - 1)
				json.dump(self.generalJSON, archConf, indent=3, ensure_ascii=False)

		try:
			with open("Config/inscripcion.conf", "r", encoding='utf8') as archConf:
				self.inscripcionJSON = json.load(archConf)
		except (FileNotFoundError, ValueError) as err:
			with open("Config/inscripcion.conf", "w", encoding='utf8') as archConf:
				self.inscripcionJSON = {"Output" : "H:/Documentos/Trabajo/UNIC/Outputs", "Inscritos" : 0, \
				"PDF Name": ["Matrícula", "Apellido Paterno", "Apellido Materno", "Nombre"], \
				"Choices": {"Tipo de Sangre":["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"], "¿Enfermedad?": ["Sí","No"]},\
				"CSV": "H:/Documentos/Trabajo/UNIC/Outputs/Inscritos.csv",\
				"Labels": ["Matrícula", "Licenciatura", "Semestre", "Generación" , "Foto", "", "Apellido Paterno", "Apellido Materno", "Nombre", "Lugar de Nacimiento", "Fecha de Nacimiento", "Nacionalidad", "", "Calle",\
					"Número", "Colonia", "Población", "Municipio", "Estado", "C.P.", "Teléfono Particular", "Teléfono Celular", "Correo", "", "Empresa", "Teléfono Empresa", "Calle Empresa", "Número Empresa",\
					"Colonia Empresa", "Municipio Empresa", "", "Nombre del Padre", "Teléfono Padre", "Dirección Padre", "Negocio Padre", "Teléfono Negocio Padre", "Celular Padre", "Correo Padre", "Nombre de la Madre",\
					"Teléfono Madre", "Dirección Madre", "Negocio Madre", "Teléfono Negocio Madre" ,"Celular Madre", "Correo Madre", "", "¿Enfermedad?", "Enfermedad", "Tipo de Sangre", "Nombre Contacto", "Parentesco", "Teléfono Contacto",\
					"Celular Contacto", "Correo Contacto", "Dirección Contacto", "Negocio Contacto", "Fecha"],\
				"Drop List": ["Licenciatura", "Tipo de Sangre"],\
				"Files" : ["Foto"],\
				"Date" : ["Fecha de Nacimiento", "Fecha"],\
				}
				json.dump(self.inscripcionJSON, archConf, indent=3, ensure_ascii=False)

		try:
			with open("Config/pae.conf", "r", encoding='utf8') as archConf:
				self.paeJSON = json.load(archConf)
		except (FileNotFoundError, ValueError) as err:
			with open("Config/pae.conf", "w", encoding='utf8') as archConf:
				self.paeJSON = {"Output" : "H:/Documentos/Trabajo/UNIC/Outputs", "Inscritos" : 0, \
				"PDF Name": ["Matrícula", "Nombre"], \
				"Choices": {"Turno":["Vespertino", "Matutino", "Sabatino"], \
				"Porcentaje" :[ "30", "40", "50", "55"],\
				"Promedio Mínimo":["8.0", "8.5", "9.0", "9.5"],\
				"Asistencia Mínima": ["80"]},\
				"CSV": "H:/Documentos/Trabajo/UNIC/Outputs/PAE.csv",\
				"Labels": ["Foto", "Porcentaje", "Nombre", "Matrícula", "Licenciatura", \
					"Turno", "Semestre", "Generación", "Primer Ciclo Escolar",  "Promedio Mínimo", "Asistencia Mínima", "Fecha"],\
				"Files" : ["Foto"],\
				"Date" : ["Fecha"],\
				}
				json.dump(self.paeJSON, archConf, indent=3, ensure_ascii=False)

	def CreateInscripcion(self):
		self.inscripcion.CreateDoc(self.inscripcionJSON["PDF Name"], self.inscripcionJSON["Output"])
		self.inscripcionCSV.WriteRow(self.inscripcion.data.copy())
		self.inscripcion.Flush()

	def CreatePAE(self):
		self.pae.CreateDoc(self.paeJSON["PDF Name"], self.paeJSON["Output"])
		self.paeCSV.WriteRow(self.pae.data.copy())
		self.pae.Flush()

	def __del__(self):
		with open("Config/inscripcion.conf", "w", encoding='utf8') as archConf:
			json.dump(self.inscripcionJSON, archConf, indent=3, ensure_ascii=False)

		with open("Config/general.conf", "w", encoding='utf8') as archConf:
			json.dump(self.generalJSON, archConf, indent=3, ensure_ascii=False)

		with open("Config/pae.conf", "w", encoding='utf8') as archConf:
			json.dump(self.paeJSON, archConf, indent=3, ensure_ascii=False)

class CSVTable:
	def __init__(self, filename, columnsName):
		self.filename = filename
		self.rowLenght = len(columnsName)
		try:
			with open(self.filename, "r", encoding='utf8') as csvFile:
				self.columnsOrder = csvFile.readline().split(",")
				if csvFile.tell() == 0:
					print("Pasó! " + str(csvFile.tell()))
					raise EmptyFileError
				self.columnsOrder.remove("\n")

		except (FileNotFoundError, EmptyFileError):
			print("mirad")
			with open(self.filename, "w", encoding='utf8') as csvFile:
				csvFile.write(str("{}," * self.rowLenght).format(*columnsName) + "\n")
				self.columnsOrder = columnsName

	def WriteRow(self, dictRow):
		row = str("{}," * self.rowLenght).format(*[dictRow[data] for data in self.columnsOrder])
		with open(self.filename, "a", encoding='utf8') as csvFile:
			csvFile.write("{}\n".format(row))

	def __iter__(self):
		with open(filename, "r", encoding='utf8') as csvFile:
			for line in csvFile:
				yield line

class EmptyFileError(Exception):
	pass


if __name__ == "__main__":
	CreateDirs()
	Update()
	BeginLoop()