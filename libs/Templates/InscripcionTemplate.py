from pylatex import Command, Package, Tabular, MultiRow
from pylatex.utils import NoEscape, bold
import os
from libs.CustomPyLatex import *
from libs.Templates.BaseTemplate import Formato


class Inscripcion(Formato):

	def CreateDoc(self, enrollDict, outputNameRef=[""], outputDir=""):
		
		def InsDatosEscolares(enrollDict, hasImage):

			with self.doc.create(Tabular(NoEscape("m{0.8in}m{0.6in}m{0.9in}m{1.5in}m{2.3in}"))) as table:
				if hasImage:
					image = MultiRow(3, data=Command("includegraphics", NoEscape(enrollDict["Foto"][enrollDict["Foto"].rfind("/") + 1:][:enrollDict["Foto"].rfind(".")]),["width=1.5in", "height=1in"]))					
				else:
					image = ""
				table.add_row(("","","","",""))
				table.add_row(("","","","", image))
				table.add_row((bold("Matrícula: "), enrollDict["Matrícula"], bold("Licenciatura: "), enrollDict["Licenciatura"], ""))
				table.add_row((bold("Semestre: "),enrollDict["Semestre"], bold("Generación: "), enrollDict["Generación"], ""))

		def InsDatosPersonales(enrollDict):
			with self.doc.create(SectionUnnumbered("Datos Personales")):
				with self.doc.create(Tabular(NoEscape("m{2in}m{2in}m{2in}"))) as table:
					table.add_row((enrollDict["Apellido Paterno"], enrollDict["Apellido Materno"], enrollDict["Nombre"]))
					table.add_hline()
					table.add_row((bold("Apellido Paterno"), bold("Apellido Materno"), bold("Nombre")))

				with self.doc.create(Tabular(NoEscape("m{2in}m{2in}m{2in}"))) as table:
					table.add_row((enrollDict["Lugar de Nacimiento"], enrollDict["Fecha de Nacimiento"], enrollDict["Nacionalidad"]))
					table.add_hline()
					table.add_row((bold("Lugar de Nacimiento"), bold("Fecha de Nacimiento"), bold("Nacionalidad")))
			
		def InsDatosDomicilio(enrollDict):
			with self.doc.create(SectionUnnumbered("Domicilio Particular")):
				Command("vspace", NoEscape("-1ex"))
				with self.doc.create(Tabular(NoEscape("m{1.33in}m{0.6in}m{2in}m{1.9in}"))) as table:
					table.add_row((enrollDict["Calle"], enrollDict["Número"], enrollDict["Colonia"], enrollDict["Población"]))
					table.add_hline()
					table.add_row((bold("Calle"), bold("Número"), bold("Colonia"), bold("Poblacion")))

				with self.doc.create(Tabular(NoEscape("m{2in}m{2in}m{2in}"))) as table:
					table.add_row((enrollDict["Municipio"], enrollDict["Estado"], enrollDict["C.P."]))
					table.add_hline()
					table.add_row((bold("Municipio"), bold("Estado"), bold("C.P.")))

				with self.doc.create(Tabular(NoEscape("m{2in}m{2in}m{2in}"))) as table:
					table.add_row((enrollDict["Teléfono Particular"], enrollDict["Teléfono Celular"], enrollDict["Correo"]))
					table.add_hline()
					table.add_row((bold("Teléfono Particular"), bold("Teléfono Celular"), bold("Correo Electrónico")))

		def InsDatosTrabajo(enrollDict):
			with self.doc.create(SectionUnnumbered("Datos del Trabajo")):
				Command("vspace", NoEscape("-1ex"))
				self.doc.append(NoEscape(\
					r"{}: {} {}: {}\\"\
					.format(bold("Empresa o Institución"), makeUnderline(enrollDict["Empresa"], 2.5),bold("Teléfono"), makeUnderline(enrollDict["Teléfono Empresa"], 1.65))
					))

				with self.doc.create(Tabular(NoEscape("m{1.3in}m{0.6in}m{2in}m{1.9in}"))) as table:
					table.add_row((enrollDict["Calle Empresa"], enrollDict["Número Empresa"], enrollDict["Colonia Empresa"], enrollDict["Municipio Empresa"]))
					table.add_hline()
					table.add_row((bold("Calle"), bold("Número"), bold("Colonia"), bold("Municipio")))

		def InsDatosFamiliares(enrollDict):
			with self.doc.create(SectionUnnumbered("Datos Familiares")):
				Command("vspace", NoEscape("-1ex"))
				self.doc.append(NoEscape(\
					r"{}: {} {}: {}\\{}: {} {}: {}\\"\
					.format(bold("Nombre del Padre"), makeUnderline(enrollDict["Nombre del Padre"], 2.75),bold("Teléfono"), makeUnderline(enrollDict["Teléfono Padre"], 1.65),\
						bold("Domicilio"), makeUnderline(enrollDict["Dirección Padre"], 3.35),bold("Empresa"), makeUnderline(enrollDict["Negocio Padre"], 1.63))
					))
			
				with self.doc.create(Tabular(NoEscape("m{2in}m{2in}m{2in}"))) as table:
					table.add_row((enrollDict["Teléfono Padre"], enrollDict["Celular Padre"], enrollDict["Correo Padre"]))
					table.add_hline()
					table.add_row((bold("Teléfono Particular"), bold("Teléfono Celular"), bold("Correo Electrónico")))

				self.doc.append(NoEscape(\
					r"{}: {} {}: {}\\{}: {} {}: {}\\"\
					.format(bold("Nombre de la Madre"), makeUnderline(enrollDict["Nombre de la Madre"], 2.75),bold("Teléfono"), makeUnderline(enrollDict["Teléfono Madre"], 1.55),\
						bold("Domicilio"), makeUnderline(enrollDict["Dirección Madre"], 3.35),bold("Empresa"), makeUnderline(enrollDict["Negocio Madre"], 1.63))
					))

				with self.doc.create(Tabular(NoEscape("m{2in}m{2in}m{2in}"))) as table:
					table.add_row((enrollDict["Teléfono Madre"], enrollDict["Celular Madre"], enrollDict["Correo Madre"]))
					table.add_hline()
					table.add_row((bold("Teléfono Particular"), bold("Teléfono Celular"), bold("Correo Electrónico")))
		
		def InsDatosEmergencia(enrollDict):
			with self.doc.create(SectionUnnumbered("En caso de emergencia")):
				Command("vspace", NoEscape("-1ex"))
				self.doc.append(NoEscape(\
					r"{}{} {}: {} \\{}: {}\\"\
					.format(bold("¿Padece alguna enfermedad?"), makeUnderline(enrollDict["¿Enfermedad?"], 0.2),bold("Especifique"), makeUnderline(enrollDict["Enfermedad"], 3.4), bold("Tipo de Sangre"), makeUnderline(enrollDict["Tipo de Sangre"], .5))
					))

				self.doc.append(NoEscape(\
					r"{}:\\{}: {} {}: {}\\ "\
					.format(bold("Contactar a"), bold("Nombre"), makeUnderline(enrollDict["Nombre Contacto"], 3.52),bold("Parentesco"), makeUnderline(enrollDict["Parentesco"], 1.5))
					))

				with self.doc.create(Tabular(NoEscape("m{2in}m{2in}m{2in}"))) as table:
					table.add_row((enrollDict["Teléfono Contacto"], enrollDict["Celular Contacto"], enrollDict["Correo Contacto"]))
					table.add_hline()
					table.add_row((bold("Teléfono Particular"), bold("Teléfono Celular"), bold("Correo Electrónico")))

				self.doc.append(NoEscape(\
					r"{}: {} {}: {}\\"\
					.format(bold("Domicilio"), makeUnderline(enrollDict["Dirección Contacto"], 3.35),bold("Empresa"), makeUnderline(enrollDict["Negocio Contacto"], 1.63))
					))

		if outputDir is "":
			outputDir = os.sys.path[0]
		#self.doc = Document()

		hasImage = enrollDict["Foto"] != ""
		
		self.doc.packages.append(Package("geometry", options=["a4paper"]))
		self.doc.packages.append(Package("array"))
		self.doc.packages.append(Package("fullpage"))

		self.doc.preamble.append(Command("title", bold(NoEscape(r"Solicitud de Inscripción"))))
		self.doc.preamble.append(Command('date', Command("vspace", NoEscape("-15ex"))))
		self.doc.preamble.append(Command("pagenumbering", "gobble"))
		self.doc.preamble.append(Command("hfuzz=2cm"))
		if hasImage:
			self.doc.packages.append(Package("graphicx"))
			self.doc.preamble.append(Command("graphicspath", NoEscape("{}".format("{" + enrollDict["Foto"][:enrollDict["Foto"].rfind("/")] +"/}"))))
		
		self.doc.append(NoEscape(r'\maketitle'))

		self.doc.append(NoEscape(r"\noindent"))
		InsDatosEscolares(enrollDict, hasImage)
		InsDatosPersonales(enrollDict)
		InsDatosDomicilio(enrollDict)
		InsDatosTrabajo(enrollDict)
		InsDatosFamiliares(enrollDict)
		InsDatosEmergencia(enrollDict)

		self.doc.append(NoEscape("{} {}: {}".format(Command("hfill").dumps(), bold("Fecha"), enrollDict["Fecha"])))

		outputName = str("{}_" * len(outputNameRef)).format(*[enrollDict[x] for x in outputNameRef])[:-1]

		self.doc.generate_tex("{}/{}".format("Outputs", outputName))
		os.system("{} {}/{}.tex -output-directory={}".format("pdflatex", "Outputs", outputName, outputDir))
		os.startfile("{}/{}.pdf".format(outputDir, outputName))
		os.remove("{}/{}.AUX".format(outputDir, outputName))
		os.remove("{}/{}.log".format(outputDir, outputName))

	def FormatoPAE(self, paeDict):
		pass