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
		self.master.geometry("170x220")
		self.pack()
		master.protocol("WM_DELETE_WINDOW", self.OnCloseWindow)
		self._manager = Manager()
		self.CreateMenu()
		self.CreateWidgets()

	def CreateWidgets(self):
		tk.Button(self.master, text="Inscripción", command=self.AbrirInscripcion).place(x=50,y=20)
		tk.Button(self.master, text="PAE1", command=self.AbrirInscripcion).place(x=65,y=60)
		#tk.Button(self.master, text="", command=self.datosCierre).place(x=45,y=110)
		#tk.Button(self.master, text="", command=self.estadoActual).place(x=45, y=150)
		#tk.Button(self.master, text="", command=self.abrirClientesGUI).place(x=55, y=190)	

	def CreateMenu(self):
		pass

	def AbrirInscripcion(self):
		keys = self._manager.InscripcionLabels()
		values = self._manager.InscripcionValues()
		listKeys = self._manager.InscripcionDropList()
		dateKeys = self._manager.InscripcionDate()
		fileKeys = self._manager.InscripcionFiles()
		choicesDict = self._manager.general
		choicesDict.update(self._manager.inscripcion["Choices"])
		defaultDict = {"Semestre": "{}-1".format(self._manager.today.year) if int(self._manager.today.month) > 6 else "{}-2".format(self._manager.today.year - 1)}
		UserForm(tk.Toplevel(self), title="Inscripción", size="1700x350", rows=11, col_size=5, \
			keyLabels=keys, variables=values, listBox=listKeys, dateBox=dateKeys, fileBox=fileKeys, \
			choices=choicesDict, defaultValues=defaultDict)
		
	def Withdraw(self):
		self.master.withdraw()

	def AbrirVentana(self):
		self.master.update()
		self.master.deiconify()

	def OnCloseWindow(self):
		del self._manager
		self.master.destroy()

def BeginLoop():
	root = tk.Tk()
	app = FormatosGUI(master=root)
	app.mainloop()

if __name__ == '__main__':
	BeginLoop()

