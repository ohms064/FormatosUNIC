import tkinter as tk
from tkinter import messagebox as mb
import os
import subprocess 

def Update():
	pull = subprocess.Popen('git pull', stdout=subprocess.PIPE,)
	stdout_value = pull.communicate()[0]
	print ('\tstdout:' + repr(stdout_value))

	if "Already up-to-date." in str(stdout_value):
		return

	log = subprocess.Popen("git log -1 --pretty=%B", stdout=subprocess.PIPE,)
	stdout_value = log.communicate()[0]

	mb.showinfo("Actualización", str(stdout_value))
	
	try:
		with open("Config/general.conf", "r") as archConf:
			self.general = json.load(archConf)
			self.general["fecha"] = self.dia	

	except (FileNotFoundError, ValueError) as err:
		with open("Config/general.conf", "w") as archConf:
			self.general = {"fecha" : self.dia, "firstRun": True}
			json.dump(self.general, archConf, indent=3)
	except:
		with open("Errors/" + self.dia, "a") as archError:
			archError.write("Log: " + fecha)
			archError.write(sys.exc_info()[0])
			archError.write("-------------------------------")

def CreateDirs():
	os.makedirs("Config", exist_ok=True)
	os.makedirs("Errors", exist_ok=True)