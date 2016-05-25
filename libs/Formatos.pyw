
from pylatex import Document, Section, Subsection, Subsubsection, Command, Package, Tabular, MultiRow
from pylatex.utils import italic, NoEscape, bold
from pylatex.base_classes import CommandBase
from collections import defaultdict, OrderedDict
import json
import datetime
import os

class Manager():
	def __init__(self):
		self.today = datetime.date.today()
		self.formatos = Formatos()
		self.InitConfFiles()


	def InitConfFiles(self):
		try:
			with open("Config/general.conf", "r") as archConf:
				self.general = json.load(archConf)

		except (FileNotFoundError, ValueError) as err:
			with open("Config/general.conf", "w") as archConf:
				self.general = {"Licenciatura": ["Educación","Comercio Internacional", "Contador Público", "Ingeneiría Industrial", "Ciencias de la Comunicación", "Derecho", "Mercadotecnia y Publicidad", "Recursos Humanos"] }
				json.dump(self.general, archConf, indent=3)
		except:
			with open("Errors/" + self.today, "a") as archError:
				archError.write("Log: " + fecha)
				archError.write(sys.exc_info()[0])
				archError.write("-------------------------------")

		try:
			with open("Config/inscripcion.conf", "r") as archConf:
				self.inscripcion = json.load(archConf)

		except (FileNotFoundError, ValueError) as err:
			with open("Config/inscripcion.conf", "w") as archConf:
				self.inscripcion = {"Output" : "../Outputs", "Inscritos" : 0, "PDF Name": ["Matrícula", "Apellido Paterno", "Apellido Materno", "Nombre"], "Choices": {"Tipo de Sangre":["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]}}
				json.dump(self.inscripcion, archConf, indent=3)
		except:
			with open("Errors/error" + self.today, "a") as archError:
				archError.write("Log: " + fecha)
				archError.write(sys.exc_info()[0])
				archError.write("-------------------------------")

	def InscripcionLabels(self):
		return ["Matrícula", "Licenciatura", "Semestre", "Generación" , "Foto", "", "Apellido Paterno", "Apellido Materno", "Nombre", "Lugar de Nacimiento", "Fecha de Nacimiento", "Nacionalidad", "", "Calle",\
			"Número", "Colonia", "Población", "Municipio", "Estado", "C.P.", "Teléfono Particular", "Teléfono Celular", "Correo", "", "Empresa", "Teléfono Empresa", "Calle Empresa", "Número Empresa",\
			"Colonia Empresa", "Polación Empresa", "", "Nombre del Padre", "Telefóno Particular Padre", "Dirección Padre", "Negocio Padre", "Celular Padre", "Correo Padre", "Nombre de la Madre",\
			"Teléfono Madre", "Dirección Madre", "Negocio Madre", "Celular Madre", "Correo Madre", "", "¿Enfermedad?", "Enfermedad", "Tipo de Sangre", "Nombre Contacto", "Parentesco", "Teléfono Contacto",\
			"Celular Contacto", "Correo Contacto", "Dirección Contacto", "Negocio Contacto", "Fecha"]

	def InscripcionValues(self):
		return ["ID", "Career", "Semester", "Generation" , "Photo", "", "Paternal", "Maternal", "Name", "Birthplace", "Birthday", "Nationality", "", "Street", \
			"Number" , "Colony", "Town" , "Township" , "State", "C.P." , "Phone" , "Cellphone", "Email", "", "Business", "Business' Phone", "Business' Street", "Business' Number", \
			"Business' Colony", "Business' Town", "", "Father", "Father's Phone","Father's Adress", "Father's Business", "Father's Cellphone", "Father's Email", "Mother", \
			"Mother's Phone", "Mother's Adress", "Mother's Business", "Mother's Cellphone", "Mother's Email", "", "IllnessY/N", "Illness", "Bloodtype", "Contact", "Contact Relationship","Contact's Phone", \
			"Contact's Cellphone", "Contact's Email","Contact's Adress", "Contact's Business", "Date"]

	def InscripcionDropList(self):
		return ("Licenciatura", "Tipo de Sangre")

	def InscripcionFiles(self):
		return ("Foto")

	def InscripcionCheck(self):
		return ("¿Enfermedad?")

	def InscripcionDate(self):
		return ("Fecha de Nacimiento")

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

	def FormatoInscripcion(self, enrollDict):
		
		def InsDatosEscolares(inscripcion, enrollDict):

			with inscripcion.create(Tabular(NoEscape("m{0.7in}m{0.6in}m{0.9in}m{1.5in}m{2.3in}"))) as table:
				table.add_row(("","","","",MultiRow(3, data=Command("includegraphics", NoEscape(enrollDict["Photo"][enrollDict["Photo"].rfind("/") + 1:][:enrollDict["Photo"].rfind(".")]),["width=1.5in", "height=1in"]))))
				table.add_row(("","","","",""))
				table.add_row((bold("Matrícula: "), enrollDict["ID"], bold("Licenciatura: "), enrollDict["Career"], ""))
				table.add_row((bold("Semestre: "),enrollDict["Semester"], bold("Generación: "), enrollDict["Generation"], ""))

		def InsDatosPersonales(inscripcion, enrollDict):
			with inscripcion.create(SectionUnnumbered("Datos Personales")):
				with inscripcion.create(Tabular(NoEscape("m{2in}m{2in}m{2in}"))) as table:
					table.add_row((enrollDict["Paternal"], enrollDict["Maternal"], enrollDict["Name"]))
					table.add_hline()
					table.add_row((bold("Apellido Paterno"), bold("Apellido Materno"), bold("Nombre")))

				with inscripcion.create(Tabular(NoEscape("m{2in}m{2in}m{2in}"))) as table:
					table.add_row((enrollDict["Birthplace"], enrollDict["Birthday"], enrollDict["Nationality"]))
					table.add_hline()
					table.add_row((bold("Lugar de Nacimiento"), bold("Fecha de Nacimiento"), bold("Nacionalidad")))
			
		def InsDatosDomicilio(inscripcion, enrollDict):
			with inscripcion.create(SectionUnnumbered("Domicilio Particular")):
				with inscripcion.create(Tabular(NoEscape("m{1.33in}m{0.5in}m{2in}m{2in}"))) as table:
					table.add_row((enrollDict["Street"], enrollDict["Number"], enrollDict["Colony"], enrollDict["Town"]))
					table.add_hline()
					table.add_row((bold("Calle"), bold("Número"), bold("Colonia"), bold("Poblacion")))

				with inscripcion.create(Tabular(NoEscape("m{2in}m{2in}m{2in}"))) as table:
					table.add_row((enrollDict["Township"], enrollDict["State"], enrollDict["C.P."]))
					table.add_hline()
					table.add_row((bold("Municipio"), bold("Estado"), bold("C.P.")))

				with inscripcion.create(Tabular(NoEscape("m{2in}m{2in}m{2in}"))) as table:
					table.add_row((enrollDict["Phone"], enrollDict["Cellphone"], enrollDict["Email"]))
					table.add_hline()
					table.add_row((bold("Teléfono Particular"), bold("Teléfono Celular"), bold("Correo Electrónico")))

		def InsDatosTrabajo(inscripcion, enrollDict):
			with inscripcion.create(SectionUnnumbered("Datos del Trabajo")):
				inscripcion.append(NoEscape(\
					r"{}: {} {}: {}\\"\
					.format(bold("Empresa o Institución"), makeUnderline(enrollDict["Business"], 2.5),bold("Teléfono"), makeUnderline(enrollDict["Business' Phone"], 1.65))
					))

				with inscripcion.create(Tabular(NoEscape("m{1.3in}m{0.5in}m{2in}m{2in}"))) as table:
					table.add_row((enrollDict["Business' Street"], enrollDict["Business' Number"], enrollDict["Business' Colony"], personal["Business' Township"]))
					table.add_hline()
					table.add_row((bold("Calle"), bold("Número"), bold("Colonia"), bold("Municipio")))

		def InsDatosFamiliares(inscripcion, enrollDict):
			with inscripcion.create(SectionUnnumbered("Datos Familiares")):
				inscripcion.append(NoEscape(\
					r"{}: {} {}: {}\\{}: {} {}: {}\\"\
					.format(bold("Nombre del Padre"), makeUnderline(enrollDict["Father"], 2.75),bold("Teléfono"), makeUnderline(enrollDict["Father's Phone"], 1.65),\
						bold("Domicilio"), makeUnderline(enrollDict["Father's Adress"], 3.35),bold("Empresa"), makeUnderline(enrollDict["Father's Business"], 1.63))
					))
			
				with inscripcion.create(Tabular(NoEscape("m{2in}m{2in}m{2in}"))) as table:
					table.add_row((enrollDict["Father's Phone"], enrollDict["Father's Cellphone"], enrollDict["Father's Email"]))
					table.add_hline()
					table.add_row((bold("Teléfono Particular"), bold("Teléfono Celular"), bold("Correo Electrónico")))

				inscripcion.append(NoEscape(\
					r"{}: {} {}: {}\\{}: {} {}: {}\\"\
					.format(bold("Nombre de la Madre"), makeUnderline(enrollDict["Mother"], 2.75),bold("Teléfono"), makeUnderline(enrollDict["Mother's Phone"], 1.55),\
						bold("Domicilio"), makeUnderline(enrollDict["Mother's Adress"], 3.35),bold("Empresa"), makeUnderline(enrollDict["Mother's Business"], 1.63))
					))

				with inscripcion.create(Tabular(NoEscape("m{2in}m{2in}m{2in}"))) as table:
					table.add_row((enrollDict["Mother's Phone"], enrollDict["Mother's Cellphone"], enrollDict["Mother's Email"]))
					table.add_hline()
					table.add_row((bold("Teléfono Particular"), bold("Teléfono Celular"), bold("Correo Electrónico")))
		
		def InsDatosEmergencia(inscripcion, enrollDict):
			with inscripcion.create(SectionUnnumbered("En caso de emergencia")):
				inscripcion.append(NoEscape(\
					r"{}{} {}: {} \\{}: {}\\"\
					.format(bold("¿Padece alguna enfermedad?"), makeUnderline(enrollDict["IllnessY/N"], 0.2),bold("Especifique"), makeUnderline(enrollDict["Illness"], 3.4), bold("Tipo de Sangre"), makeUnderline(enrollDict["Bloodtype"], .5))
					))

				inscripcion.append(NoEscape(\
					r"{}:\\{}: {} {}: {}\\ "\
					.format(bold("Contactar a"), bold("Nombre"), makeUnderline(enrollDict["Contact"], 3.52),bold("Parentesco"), makeUnderline(enrollDict["Contact Relationship"], 1.5))
					))

				with inscripcion.create(Tabular(NoEscape("m{2in}m{2in}m{2in}"))) as table:
					table.add_row((enrollDict["Contact's Phone"], enrollDict["Contact's Cellphone"], enrollDict["Contact's Email"]))
					table.add_hline()
					table.add_row((bold("Teléfono Particular"), bold("Teléfono Celular"), bold("Correo Electrónico")))

				inscripcion.append(NoEscape(\
					r"{}: {} {}: {}\\"\
					.format(bold("Domicilio"), makeUnderline(enrollDict["Contact's Adress"], 3.35),bold("Empresa"), makeUnderline(enrollDict["Contact's Business"], 1.63))
					))

		self.inscripcion = Document()
		
		self.inscripcion.packages.append(Package("geometry", options=["a4paper"]))
		self.inscripcion.packages.append(Package("array"))
		self.inscripcion.packages.append(Package("fullpage"))
		self.inscripcion.packages.append(Package("graphicx"))

		#self.inscripcion.preamble.append(Command("addtolength", arguments=Command("voffset"), extra_arguments=NoEscape("0.5in")))
		self.inscripcion.preamble.append(Command("title", bold(NoEscape(r"Solicidutd de Inscripción"))))
		self.inscripcion.preamble.append(Command('date', NoEscape(r"\vspace{-12ex}")))
		self.inscripcion.preamble.append(Command("pagenumbering", "gobble"))
		self.inscripcion.preamble.append(Command("graphicspath", NoEscape("{}".format("{" + enrollDict["Photo"][:enrollDict["Photo"].rfind("/")] +"/}"))))
		
		self.inscripcion.append(NoEscape(r'\maketitle'))

		self.inscripcion.append(NoEscape(r"\noindent"))
		InsDatosEscolares(self.inscripcion, enrollDict)
		InsDatosPersonales(self.inscripcion, enrollDict)
		InsDatosDomicilio(self.inscripcion, enrollDict)
		InsDatosTrabajo(self.inscripcion, enrollDict)
		InsDatosFamiliares(self.inscripcion, enrollDict)
		InsDatosEmergencia(self.inscripcion, enrollDict)

		self.inscripcion.append(NoEscape("{} {}: {}".format(Command("hfill").dumps(), bold("Fecha"), Command("today").dumps())))
		
	def FormatoPAE(self, paeDict):
		pass


if __name__ == "__main__":
	f = Formatos()
	personal = defaultdict(str)

	personal["ID"] = "308633184"
	personal["Career"] = "Computer Engineering"
	personal["Semester"] = "2016-2"
	personal["Generation"] = "2011-1"
	personal["Photo"] = "../Imagenes/omar2.jpg"

	personal["Paternal"] = "Rodríguez"
	personal["Maternal"] = "Pérez"
	personal["Name"] = "Omar"
	personal["Birthplace"] = "Cuernavaca"
	personal["Birthday"] = "22/02/1992"
	personal["Nationality"] = "Mexicana"

	personal["Street"] = "Av. Universidad"
	personal["Number"] = "2014"
	personal["Colony"] = "Romero de Terreros"
	personal["Town"] = "Coyoacán"
	personal["Township"] = "Coyoacán"
	personal["State"] = "Ciudad de México"
	personal["C.P."] = 56520
	personal["Phone"] = 56592180
	personal["Cellphone"] = 7771481259
	personal["Email"] = "otokonoko064@gmail.com"

	personal["Business"] = "Quetzal Studio"
	personal["Business' Phone"] = "56592180"
	personal["Business' Street"] = "Benito Juarez"
	personal["Business' Number"] = 2
	personal["Buseness' Colony"] = "Copilco"
	personal["Business' Town"] = "Coyoacán"

	personal["Father"] = "Alfonso Rodríguez Nájera"
	personal["Father's Phone"] = ""
	personal["Father's Adress"] = "Not an earthly one at least"
	personal["Father's Business"] = ""
	personal["Father's Cellphone"] = ""
	personal["Father's Email"] = ""
	personal["Mother"] = "Diana Pérez Brito"
	personal["Mother's Phone"] = "3189538"
	personal["Mother's Adress"] = "Av. Los Cizos #2 Acapatzingo"
	personal["Mother's Business"] = "Universidad Cuauhnáhuac"
	personal["Mother's Cellphone"] = 777507402
	personal["Mother's Email"] = "dpbrito@hotmail.com"

	personal["IllnessY/N"] = "Si"
	personal["Illness"] = "Poca visión en el ojo derecho"
	personal["Bloodtype"] = "O+"
	personal["Contact"] = "Diana Pérez Brito"
	personal["Contact Relationship"] = "Mamá"
	personal["Contact's Phone"] = 3189538
	personal["Contact's Cellphone"] = 7772507402
	personal["Contact's Email"] = "dpbrito@hotmail.com"
	personal["Contact's Adress"] = "Av. Los Cizos #2 Acapatzingo"
	personal["Contact's Business"] = "UNIC"


	f.FormatoInscripcion(personal)

	f.inscripcion.generate_tex("../Outputs/outputIns")