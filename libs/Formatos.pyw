
from pylatex import Document, Section, Subsection, Subsubsection, Command, Package, Tabular, MultiRow
from pylatex.utils import italic, NoEscape, bold
from pylatex.base_classes import CommandBase
from collections import defaultdict, OrderedDict
import json
import datetime
import os
import csv

class Manager():
	def __init__(self):
		self.today = datetime.date.today()
		self.formatos = Formatos()
		self.inscripcionDict = dict()
		self.InitConfFiles()


	def InitConfFiles(self):
		try:
			with open("libs/Config/general.conf", "r", encoding='utf8') as archConf:
				self.general = json.load(archConf)

		except (FileNotFoundError, ValueError) as err:
			with open("libs/Config/general.conf", "w") as archConf:
				self.general = {"Licenciatura": ["Educación","Comercio Internacional", "Contador Público", "Ingeneiría Industrial", "Ciencias de la Comunicación", "Derecho", "Mercadotecnia y Publicidad", "Recursos Humanos"] }
				json.dump(self.general, archConf, indent=3, ensure_ascii=False)

		try:
			with open("libs/Config/inscripcion.conf", "r", encoding='utf8') as archConf:
				self.inscripcion = json.load(archConf)
		except (FileNotFoundError, ValueError) as err:
			with open("libs/Config/inscripcion.conf", "w") as archConf:
				self.inscripcion = {"Output" : "H:/Documentos/Trabajo/UNIC/Outputs", "Inscritos" : 0, \
				"PDF Name": ["Matrícula", "Apellido Paterno", "Apellido Materno", "Nombre"], \
				"Choices": {"Tipo de Sangre":["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]},\
				}
				json.dump(self.inscripcion, archConf, indent=3, ensure_ascii=False)

	def InscripcionLabels(self):
		return ["Matrícula", "Licenciatura", "Semestre", "Generación" , "Foto", "", "Apellido Paterno", "Apellido Materno", "Nombre", "Lugar de Nacimiento", "Fecha de Nacimiento", "Nacionalidad", "", "Calle",\
			"Número", "Colonia", "Población", "Municipio", "Estado", "C.P.", "Teléfono Particular", "Teléfono Celular", "Correo", "", "Empresa", "Teléfono Empresa", "Calle Empresa", "Número Empresa",\
			"Colonia Empresa", "Municipio Empresa", "", "Nombre del Padre", "Teléfono Padre", "Dirección Padre", "Negocio Padre", "Celular Padre", "Correo Padre", "Nombre de la Madre",\
			"Teléfono Madre", "Dirección Madre", "Negocio Madre", "Celular Madre", "Correo Madre", "", "¿Enfermedad?", "Enfermedad", "Tipo de Sangre", "Nombre Contacto", "Parentesco", "Teléfono Contacto",\
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
		self.formatos.FormatoInscripcion(inscripcionDict, self.inscripcion["PDF Name"], self.inscripcion["Output"])

class newline(CommandBase):
	_latex_name = "newline"

class SectionUnnumbered(Section):
	_latex_name = "section*"

class SubsectionUnnumbered(Subsection):
	_latex_name = "subsection*"

class SubsubsectionUnnumbered(Subsubsection):
	_latex_name = "subsubsection*"

class makebox(CommandBase):
	_latex_name = "makebox"

class underline(CommandBase):
	_latex_name = "underline"

def makeUnderline(cadena, size):
	return underline(NoEscape(makebox(cadena, options="{}in".format(size)).dumps())).dumps()

class Formatos():

	def FormatoInscripcion(self, enrollDict, outputNameRef=[""], outputDir=""):
		
		def InsDatosEscolares(inscripcion, enrollDict, hasImage):

			with inscripcion.create(Tabular(NoEscape("m{0.8in}m{0.6in}m{0.9in}m{1.5in}m{2.3in}"))) as table:
				if hasImage:
					image = MultiRow(3, data=Command("includegraphics", NoEscape(enrollDict["Foto"][enrollDict["Foto"].rfind("/") + 1:][:enrollDict["Foto"].rfind(".")]),["width=1.5in", "height=1in"]))					
				else:
					image = ""
				table.add_row(("","","","", image))
				table.add_row(("","","","",""))
				table.add_row((bold("Matrícula: "), enrollDict["Matrícula"], bold("Licenciatura: "), enrollDict["Licenciatura"], ""))
				table.add_row((bold("Semestre: "),enrollDict["Semestre"], bold("Generación: "), enrollDict["Generación"], ""))

		def InsDatosPersonales(inscripcion, enrollDict):
			with inscripcion.create(SectionUnnumbered("Datos Personales")):
				with inscripcion.create(Tabular(NoEscape("m{2in}m{2in}m{2in}"))) as table:
					table.add_row((enrollDict["Apellido Paterno"], enrollDict["Apellido Materno"], enrollDict["Nombre"]))
					table.add_hline()
					table.add_row((bold("Apellido Paterno"), bold("Apellido Materno"), bold("Nombre")))

				with inscripcion.create(Tabular(NoEscape("m{2in}m{2in}m{2in}"))) as table:
					table.add_row((enrollDict["Lugar de Nacimiento"], enrollDict["Fecha de Nacimiento"], enrollDict["Nacionalidad"]))
					table.add_hline()
					table.add_row((bold("Lugar de Nacimiento"), bold("Fecha de Nacimiento"), bold("Nacionalidad")))
			
		def InsDatosDomicilio(inscripcion, enrollDict):
			with inscripcion.create(SectionUnnumbered("Domicilio Particular")):
				with inscripcion.create(Tabular(NoEscape("m{1.33in}m{0.6in}m{2in}m{1.9in}"))) as table:
					table.add_row((enrollDict["Calle"], enrollDict["Número"], enrollDict["Colonia"], enrollDict["Población"]))
					table.add_hline()
					table.add_row((bold("Calle"), bold("Número"), bold("Colonia"), bold("Poblacion")))

				with inscripcion.create(Tabular(NoEscape("m{2in}m{2in}m{2in}"))) as table:
					table.add_row((enrollDict["Municipio"], enrollDict["Estado"], enrollDict["C.P."]))
					table.add_hline()
					table.add_row((bold("Municipio"), bold("Estado"), bold("C.P.")))

				with inscripcion.create(Tabular(NoEscape("m{2in}m{2in}m{2in}"))) as table:
					table.add_row((enrollDict["Teléfono Particular"], enrollDict["Teléfono Celular"], enrollDict["Correo"]))
					table.add_hline()
					table.add_row((bold("Teléfono Particular"), bold("Teléfono Celular"), bold("Correo Electrónico")))

		def InsDatosTrabajo(inscripcion, enrollDict):
			with inscripcion.create(SectionUnnumbered("Datos del Trabajo")):
				inscripcion.append(NoEscape(\
					r"{}: {} {}: {}\\"\
					.format(bold("Empresa o Institución"), makeUnderline(enrollDict["Empresa"], 2.5),bold("Teléfono"), makeUnderline(enrollDict["Teléfono Empresa"], 1.65))
					))

				with inscripcion.create(Tabular(NoEscape("m{1.3in}m{0.6in}m{2in}m{1.9in}"))) as table:
					table.add_row((enrollDict["Calle Empresa"], enrollDict["Número Empresa"], enrollDict["Colonia Empresa"], enrollDict["Municipio Empresa"]))
					table.add_hline()
					table.add_row((bold("Calle"), bold("Número"), bold("Colonia"), bold("Municipio")))

		def InsDatosFamiliares(inscripcion, enrollDict):
			with inscripcion.create(SectionUnnumbered("Datos Familiares")):
				inscripcion.append(NoEscape(\
					r"{}: {} {}: {}\\{}: {} {}: {}\\"\
					.format(bold("Nombre del Padre"), makeUnderline(enrollDict["Nombre del Padre"], 2.75),bold("Teléfono"), makeUnderline(enrollDict["Teléfono Padre"], 1.65),\
						bold("Domicilio"), makeUnderline(enrollDict["Dirección Padre"], 3.35),bold("Empresa"), makeUnderline(enrollDict["Negocio Padre"], 1.63))
					))
			
				with inscripcion.create(Tabular(NoEscape("m{2in}m{2in}m{2in}"))) as table:
					table.add_row((enrollDict["Teléfono Padre"], enrollDict["Celular Padre"], enrollDict["Correo Padre"]))
					table.add_hline()
					table.add_row((bold("Teléfono Particular"), bold("Teléfono Celular"), bold("Correo Electrónico")))

				inscripcion.append(NoEscape(\
					r"{}: {} {}: {}\\{}: {} {}: {}\\"\
					.format(bold("Nombre de la Madre"), makeUnderline(enrollDict["Nombre de la Madre"], 2.75),bold("Teléfono"), makeUnderline(enrollDict["Teléfono Madre"], 1.55),\
						bold("Domicilio"), makeUnderline(enrollDict["Dirección Madre"], 3.35),bold("Empresa"), makeUnderline(enrollDict["Negocio Madre"], 1.63))
					))

				with inscripcion.create(Tabular(NoEscape("m{2in}m{2in}m{2in}"))) as table:
					table.add_row((enrollDict["Teléfono Madre"], enrollDict["Celular Madre"], enrollDict["Correo Madre"]))
					table.add_hline()
					table.add_row((bold("Teléfono Particular"), bold("Teléfono Celular"), bold("Correo Electrónico")))
		
		def InsDatosEmergencia(inscripcion, enrollDict):
			with inscripcion.create(SectionUnnumbered("En caso de emergencia")):
				inscripcion.append(NoEscape(\
					r"{}{} {}: {} \\{}: {}\\"\
					.format(bold("¿Padece alguna enfermedad?"), makeUnderline(enrollDict["¿Enfermedad?"], 0.2),bold("Especifique"), makeUnderline(enrollDict["Enfermedad"], 3.4), bold("Tipo de Sangre"), makeUnderline(enrollDict["Tipo de Sangre"], .5))
					))

				inscripcion.append(NoEscape(\
					r"{}:\\{}: {} {}: {}\\ "\
					.format(bold("Contactar a"), bold("Nombre"), makeUnderline(enrollDict["Nombre Contacto"], 3.52),bold("Parentesco"), makeUnderline(enrollDict["Parentesco"], 1.5))
					))

				with inscripcion.create(Tabular(NoEscape("m{2in}m{2in}m{2in}"))) as table:
					table.add_row((enrollDict["Teléfono Contacto"], enrollDict["Celular Contacto"], enrollDict["Correo Contacto"]))
					table.add_hline()
					table.add_row((bold("Teléfono Particular"), bold("Teléfono Celular"), bold("Correo Electrónico")))

				inscripcion.append(NoEscape(\
					r"{}: {} {}: {}\\"\
					.format(bold("Domicilio"), makeUnderline(enrollDict["Dirección Contacto"], 3.35),bold("Empresa"), makeUnderline(enrollDict["Negocio Contacto"], 1.63))
					))

		if outputDir is "":
			outputDir = os.sys.path[0]
		self.inscripcion = Document()

		hasImage = enrollDict["Foto"] != ""
		
		self.inscripcion.packages.append(Package("geometry", options=["a4paper"]))
		self.inscripcion.packages.append(Package("array"))
		self.inscripcion.packages.append(Package("fullpage"))

		self.inscripcion.preamble.append(Command("title", bold(NoEscape(r"Solicidutd de Inscripción"))))
		self.inscripcion.preamble.append(Command('date', NoEscape(r"\vspace{-12ex}")))
		self.inscripcion.preamble.append(Command("pagenumbering", "gobble"))
		self.inscripcion.preamble.append(Command("hfuzz=2cm"))
		if hasImage:
			self.inscripcion.packages.append(Package("graphicx"))
			self.inscripcion.preamble.append(Command("graphicspath", NoEscape("{}".format("{" + enrollDict["Foto"][:enrollDict["Foto"].rfind("/")] +"/}"))))
		
		self.inscripcion.append(NoEscape(r'\maketitle'))

		self.inscripcion.append(NoEscape(r"\noindent"))
		InsDatosEscolares(self.inscripcion, enrollDict, hasImage)
		InsDatosPersonales(self.inscripcion, enrollDict)
		InsDatosDomicilio(self.inscripcion, enrollDict)
		InsDatosTrabajo(self.inscripcion, enrollDict)
		InsDatosFamiliares(self.inscripcion, enrollDict)
		InsDatosEmergencia(self.inscripcion, enrollDict)

		self.inscripcion.append(NoEscape("{} {}: {}".format(Command("hfill").dumps(), bold("Fecha"), enrollDict["Fecha"])))

		outputName = str("{}_" * len(outputNameRef)).format(*[enrollDict[x] for x in outputNameRef])[:-1]

		self.inscripcion.generate_tex("{}/{}".format("Outputs", outputName))
		os.system("{} {}/{}.tex -output-directory={}".format("pdflatex", "Outputs", outputName, outputDir))
		os.startfile("{}/{}.pdf".format(outputDir, outputName))

	def FormatoPAE(self, paeDict):
		pass

class CSVLink:
	pass

