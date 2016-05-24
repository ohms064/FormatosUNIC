if __name__ == "__main__":
	from Formatos import Manager
else:
	from libs.Formatos import Manager
import tkinter as tk
from collections import defaultdict
from tkinter import messagebox as mb

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
		self.CreateWidgets()

	def CreateWidgets(self):
		tk.Button(self.master, text="Inscripción", command=self.AbrirInscripcion).place(x=50,y=20)
		tk.Button(self.master, text="PAE1", command=self.AbrirInscripcion).place(x=65,y=60)
		#tk.Button(self.master, text="", command=self.datosCierre).place(x=45,y=110)
		#tk.Button(self.master, text="", command=self.estadoActual).place(x=45, y=150)
		#tk.Button(self.master, text="", command=self.abrirClientesGUI).place(x=55, y=190)	

	def AbrirInscripcion(self):
		FormatoInscripcionGUI(self._manager, tk.Toplevel(self), self)

	def Withdraw(self):
		self.master.withdraw()

	def AbrirVentana(self):
		self.master.update()
		self.master.deiconify()

	def OnCloseWindow(self):
		del self._manager
		self.master.destroy()

class FormatoInscripcionGUI(tk.Frame):
	def __init__(self, _manager, master=None, padre=None):
		tk.Frame.__init__(self, master)		
		self.padre = padre
		self._manager = _manager
		self.master.wm_title("Cierre")
		self.master.geometry("1500x250")
		#self.pack()
		self.master.protocol("WM_DELETE_WINDOW", self.ShowMain)
		self.CreateWidgets()

	def CreateWidgets(self):
		keys = self._manager.InscripciónLabels()
		values = self._manager.InscripcionValues()
		form = dict((k, v) for k,v in zip(keys, values))
		formValues = dict()
		r = 0
		c = 0
		for label in keys:
			print("r: {} c: {}, Label: {}".format(r,c, label))
			formValues[form[label]] = tk.StringVar()
			tk.Label(self.master, text="{}:".format(label)).grid(row=r, column=c, sticky=tk.SE)
			tk.Entry(self.master, textvariable=formValues[form[label]]).grid(row=r, column=c + 1)
			r += 1
			if r > 10:
				r = 0
				c += 5


	def ShowMain(self):
		"""
		Se retorna a la ventana padre.
		"""
		self.master.destroy()
		
def BeginLoop():
	root = tk.Tk()
	app = FormatosGUI(master=root)
	app.mainloop()

if __name__ == '__main__':
	BeginLoop()

"""
from Tkinter import *

class ListBoxChoice(object):
    def __init__(self, master=None, title=None, message=None, list=[]):
        self.master = master
        self.value = None
        self.list = list[:]
        
        self.modalPane = Toplevel(self.master)

        self.modalPane.transient(self.master)
        self.modalPane.grab_set()

        self.modalPane.bind("<Return>", self._choose)
        self.modalPane.bind("<Escape>", self._cancel)

        if title:
            self.modalPane.title(title)

        if message:
            Label(self.modalPane, text=message).pack(padx=5, pady=5)

        listFrame = Frame(self.modalPane)
        listFrame.pack(side=TOP, padx=5, pady=5)
        
        scrollBar = Scrollbar(listFrame)
        scrollBar.pack(side=RIGHT, fill=Y)
        self.listBox = Listbox(listFrame, selectmode=SINGLE)
        self.listBox.pack(side=LEFT, fill=Y)
        scrollBar.config(command=self.listBox.yview)
        self.listBox.config(yscrollcommand=scrollBar.set)
        self.list.sort()
        for item in self.list:
            self.listBox.insert(END, item)

        buttonFrame = Frame(self.modalPane)
        buttonFrame.pack(side=BOTTOM)

        chooseButton = Button(buttonFrame, text="Choose", command=self._choose)
        chooseButton.pack()

        cancelButton = Button(buttonFrame, text="Cancel", command=self._cancel)
        cancelButton.pack(side=RIGHT)

    def _choose(self, event=None):
        try:
            firstIndex = self.listBox.curselection()[0]
            self.value = self.list[int(firstIndex)]
        except IndexError:
            self.value = None
        self.modalPane.destroy()

    def _cancel(self, event=None):
        self.modalPane.destroy()
        
    def returnValue(self):
        self.master.wait_window(self.modalPane)
        return self.value

if __name__ == '__main__':
    import random
    root = Tk()
    
    returnValue = True
    list = [random.randint(1,100) for x in range(50)]
    while returnValue:
        returnValue = ListBoxChoice(root, "Number Picking", "Pick one of these crazy random numbers", list).returnValue()
        print returnValue
"""