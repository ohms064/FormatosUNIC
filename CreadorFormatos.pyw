from libs.Templates.InscripcionTemplate import Inscripcion
import tkinter as tk
from tkinter import messagebox as mb
from libs.CustomTK import UserForm
from tkinter import messagebox as mb
from tkinter import filedialog as fd
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
		self.formatosMenu.add_command(label="PAE")
		self.formatosMenu.add_command(label="PAE2")
		self.menubar.add_cascade(label="Archivo", menu=self.fileMenu)
		self.menubar.add_cascade(label="Formatos", menu=self.formatosMenu)
		self.master.config(menu=self.menubar)

	def AbrirInscripcion(self):
		keys = self._manager.InscripcionLabels()
		listKeys = self._manager.InscripcionDropList()
		dateKeys = self._manager.InscripcionDate()
		fileKeys = self._manager.InscripcionFiles()
		choicesDict = self._manager.generalJSON
		choicesDict.update(self._manager.inscripcionJSON["Choices"])
		defaultDict = {"Semestre": "{}-1".format(self._manager.today.year) if int(self._manager.today.month) > 6 else "{}-2".format(self._manager.today.year - 1)}
		UserForm(self.frame, self.done, rows=13, col_size=5, \
			keyLabels=keys, listBox=listKeys, dateBox=dateKeys, fileBox=fileKeys, \
			choices=choicesDict, defaultValues=defaultDict, formValues=self._manager.inscripcion.data)
		self.frame.grid(row=0, column=0)
		self.master.geometry("1700x375")
		self.master.wait_variable(self.done)
		self.done.set(False)
		self.CrearFormatoInscripcion()

	def CrearFormatoInscripcion(self):
		self._manager.CreateFormatoInscripcion(self._manager.inscripcion.data)
		self.frame.destroy()
		self.CreateWidgets()
		self.AbrirInscripcion()
		self.master.geometry("300x25")

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
		self.InitConfFiles()


	def InitConfFiles(self):
		try:
			with open("Config/general.conf", "r", encoding='utf8') as archConf:
				self.generalJSON = json.load(archConf)

		except (FileNotFoundError, ValueError) as err:
			with open("Config/general.conf", "w") as archConf:
				self.generalJSON = {"Licenciatura": ["Educación","Comercio Internacional", "Contador Público", "Ingeneiría Industrial", "Ciencias de la Comunicación", "Derecho", "Mercadotecnia y Publicidad", "Recursos Humanos"] }
				json.dump(self.generalJSON, archConf, indent=3, ensure_ascii=False)

		try:
			with open("Config/doc.conf", "r", encoding='utf8') as archConf:
				self.inscripcionJSON = json.load(archConf)
		except (FileNotFoundError, ValueError) as err:
			with open("Config/doc.conf", "w") as archConf:
				self.inscripcionJSON = {"Output" : "H:/Documentos/Trabajo/UNIC/Outputs", "Inscritos" : 0, \
				"PDF Name": ["Matrícula", "Apellido Paterno", "Apellido Materno", "Nombre"], \
				"Choices": {"Tipo de Sangre":["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]},\
				"CSV": "H:/Documentos/Trabajo/UNIC/Outputs/Inscritos.csv"\
				}
				json.dump(self.inscripcionJSON, archConf, indent=3, ensure_ascii=False)

	def InscripcionLabels(self):
		return ["Matrícula", "Licenciatura", "Semestre", "Generación" , "Foto", "", "Apellido Paterno", "Apellido Materno", "Nombre", "Lugar de Nacimiento", "Fecha de Nacimiento", "Nacionalidad", "", "Calle",\
			"Número", "Colonia", "Población", "Municipio", "Estado", "C.P.", "Teléfono Particular", "Teléfono Celular", "Correo", "", "Empresa", "Teléfono Empresa", "Calle Empresa", "Número Empresa",\
			"Colonia Empresa", "Municipio Empresa", "", "Nombre del Padre", "Teléfono Padre", "Dirección Padre", "Negocio Padre", "Teléfono Negocio Padre", "Celular Padre", "Correo Padre", "Nombre de la Madre",\
			"Teléfono Madre", "Dirección Madre", "Negocio Madre", "Teléfono Negocio Madre" ,"Celular Madre", "Correo Madre", "", "¿Enfermedad?", "Enfermedad", "Tipo de Sangre", "Nombre Contacto", "Parentesco", "Teléfono Contacto",\
			"Celular Contacto", "Correo Contacto", "Dirección Contacto", "Negocio Contacto", "Fecha"]

	def InscripcionDropList(self):
		return ("Licenciatura", "Tipo de Sangre")

	def InscripcionFiles(self):
		return ("Foto")

	def InscripcionCheck(self):
		return ("¿Enfermedad?")

	def InscripcionDate(self):
		return ("Fecha de Nacimiento")

	def CreateFormatoInscripcion(self, inscripcionDict):
		self.inscripcion.CreateDoc(inscripcionDict, self.inscripcionJSON["PDF Name"], self.inscripcionJSON["Output"])

CreateDirs()
Update()
BeginLoop()