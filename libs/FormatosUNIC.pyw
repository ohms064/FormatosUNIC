if __name__ == "__main__":
	from Formatos import Manager
	from CustomTK import *
else:
	from libs.Formatos import Manager
	from libs.CustomTK import *
import tkinter as tk
from tkinter import messagebox as mb
from tkinter import filedialog as fd

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
		choicesDict = self._manager.general
		choicesDict.update(self._manager.inscripcion["Choices"])
		defaultDict = {"Semestre": "{}-1".format(self._manager.today.year) if int(self._manager.today.month) > 6 else "{}-2".format(self._manager.today.year - 1)}
		UserForm(self.frame, self.done, rows=11, col_size=5, \
			keyLabels=keys, listBox=listKeys, dateBox=dateKeys, fileBox=fileKeys, \
			choices=choicesDict, defaultValues=defaultDict, formValues=self._manager.inscripcionDict)
		self.frame.grid(row=0, column=0)
		self.master.geometry("1700x350")
		self.master.wait_variable(self.done)
		self.done.set(False)
		self.CrearFormatoInscripcion()

	def CrearFormatoInscripcion(self):
		self._manager.CreateFormatoInscripcion(self._manager.inscripcionDict)
		self.frame.destroy()
		self.CreateWidgets()
		self.AbrirInscripcion()
		self.master.geometry("300x25")

	def OnCloseWindow(self):
		del self._manager
		self.master.destroy()

def BeginLoop():
	root = tk.Tk()
	app = FormatosGUI(master=root)
	app.mainloop()