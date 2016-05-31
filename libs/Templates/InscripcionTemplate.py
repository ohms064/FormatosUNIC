from pylatex import Command, Package, Tabular, MultiRow
from pylatex.utils import NoEscape, bold
import os
from libs.CustomPyLatex import *
from libs.Templates.BaseTemplate import Formato


class Inscripcion(Formato):

	def CreateDoc(self, outputNameRef=[""], outputDir=""):
		
		def InsDatosEscolares(hasImage):

			with self.doc.create(Tabular(NoEscape("m{0.8in}m{0.6in}m{0.9in}m{1.5in}m{2.3in}"))) as table:
				if hasImage:
					image = MultiRow(3, data=Command("includegraphics", NoEscape(self.data["Foto"][self.data["Foto"].rfind("/") + 1:][:self.data["Foto"].rfind(".")]),["width=1.5in", "height=1in"]))					
				else:
					image = ""
				table.add_row(("","","","",""))
				table.add_row(("","","","", image))
				table.add_row((bold("Matrícula: "), self.data["Matrícula"], bold("Licenciatura: "), self.data["Licenciatura"], ""))
				table.add_row((bold("Semestre: "),self.data["Semestre"], bold("Generación: "), self.data["Generación"], ""))

		def InsDatosPersonales():
			with self.doc.create(SectionUnnumbered("Datos Personales")):
				with self.doc.create(Tabular(NoEscape("m{2in}m{2in}m{2in}"))) as table:
					table.add_row((self.data["Apellido Paterno"], self.data["Apellido Materno"], self.data["Nombre"]))
					table.add_hline()
					table.add_row((bold("Apellido Paterno"), bold("Apellido Materno"), bold("Nombre")))

				with self.doc.create(Tabular(NoEscape("m{2in}m{2in}m{2in}"))) as table:
					table.add_row((self.data["Lugar de Nacimiento"], self.data["Fecha de Nacimiento"], self.data["Nacionalidad"]))
					table.add_hline()
					table.add_row((bold("Lugar de Nacimiento"), bold("Fecha de Nacimiento"), bold("Nacionalidad")))
			
		def InsDatosDomicilio():
			with self.doc.create(SectionUnnumbered("Domicilio Particular")):
				Command("vspace", NoEscape("-1ex"))
				with self.doc.create(Tabular(NoEscape("m{1.33in}m{0.6in}m{2in}m{1.9in}"))) as table:
					table.add_row((self.data["Calle"], self.data["Número"], self.data["Colonia"], self.data["Población"]))
					table.add_hline()
					table.add_row((bold("Calle"), bold("Número"), bold("Colonia"), bold("Poblacion")))

				with self.doc.create(Tabular(NoEscape("m{2in}m{2in}m{2in}"))) as table:
					table.add_row((self.data["Municipio"], self.data["Estado"], self.data["C.P."]))
					table.add_hline()
					table.add_row((bold("Municipio"), bold("Estado"), bold("C.P.")))

				with self.doc.create(Tabular(NoEscape("m{2in}m{2in}m{2in}"))) as table:
					table.add_row((self.data["Teléfono Particular"], self.data["Teléfono Celular"], self.data["Correo"]))
					table.add_hline()
					table.add_row((bold("Teléfono Particular"), bold("Teléfono Celular"), bold("Correo Electrónico")))

		def InsDatosTrabajo():
			with self.doc.create(SectionUnnumbered("Datos del Trabajo")):
				Command("vspace", NoEscape("-1ex"))
				self.doc.append(NoEscape(\
					r"{}: {} {}: {}\\"\
					.format(bold("Empresa o Institución"), makeUnderline(self.data["Empresa"], 2.5),bold("Teléfono"), makeUnderline(self.data["Teléfono Empresa"], 1.65))
					))

				with self.doc.create(Tabular(NoEscape("m{1.3in}m{0.6in}m{2in}m{1.9in}"))) as table:
					table.add_row((self.data["Calle Empresa"], self.data["Número Empresa"], self.data["Colonia Empresa"], self.data["Municipio Empresa"]))
					table.add_hline()
					table.add_row((bold("Calle"), bold("Número"), bold("Colonia"), bold("Municipio")))

		def InsDatosFamiliares():
			with self.doc.create(SectionUnnumbered("Datos Familiares")):
				Command("vspace", NoEscape("-1ex"))
				self.doc.append(NoEscape(\
					r"{}: {} {}: {}\\{}: {} {}: {}\\"\
					.format(bold("Nombre del Padre"), makeUnderline(self.data["Nombre del Padre"], 2.75),bold("Teléfono"), makeUnderline(self.data["Teléfono Padre"], 1.65),\
						bold("Domicilio"), makeUnderline(self.data["Dirección Padre"], 3.35),bold("Empresa"), makeUnderline(self.data["Negocio Padre"], 1.63))
					))
			
				with self.doc.create(Tabular(NoEscape("m{2in}m{2in}m{2in}"))) as table:
					table.add_row((self.data["Teléfono Padre"], self.data["Celular Padre"], self.data["Correo Padre"]))
					table.add_hline()
					table.add_row((bold("Teléfono Particular"), bold("Teléfono Celular"), bold("Correo Electrónico")))

				self.doc.append(NoEscape(\
					r"{}: {} {}: {}\\{}: {} {}: {}\\"\
					.format(bold("Nombre de la Madre"), makeUnderline(self.data["Nombre de la Madre"], 2.75),bold("Teléfono"), makeUnderline(self.data["Teléfono Madre"], 1.55),\
						bold("Domicilio"), makeUnderline(self.data["Dirección Madre"], 3.35),bold("Empresa"), makeUnderline(self.data["Negocio Madre"], 1.63))
					))

				with self.doc.create(Tabular(NoEscape("m{2in}m{2in}m{2in}"))) as table:
					table.add_row((self.data["Teléfono Madre"], self.data["Celular Madre"], self.data["Correo Madre"]))
					table.add_hline()
					table.add_row((bold("Teléfono Particular"), bold("Teléfono Celular"), bold("Correo Electrónico")))
		
		def InsDatosEmergencia():
			with self.doc.create(SectionUnnumbered("En caso de emergencia")):
				Command("vspace", NoEscape("-1ex"))
				self.doc.append(NoEscape(\
					r"{}{} {}: {} \\{}: {}\\"\
					.format(bold("¿Padece alguna enfermedad?"), makeUnderline(self.data["¿Enfermedad?"], 0.2),bold("Especifique"), makeUnderline(self.data["Enfermedad"], 3.4), bold("Tipo de Sangre"), makeUnderline(self.data["Tipo de Sangre"], .5))
					))

				self.doc.append(NoEscape(\
					r"{}:\\{}: {} {}: {}\\ "\
					.format(bold("Contactar a"), bold("Nombre"), makeUnderline(self.data["Nombre Contacto"], 3.52),bold("Parentesco"), makeUnderline(self.data["Parentesco"], 1.5))
					))

				with self.doc.create(Tabular(NoEscape("m{2in}m{2in}m{2in}"))) as table:
					table.add_row((self.data["Teléfono Contacto"], self.data["Celular Contacto"], self.data["Correo Contacto"]))
					table.add_hline()
					table.add_row((bold("Teléfono Particular"), bold("Teléfono Celular"), bold("Correo Electrónico")))

				self.doc.append(NoEscape(\
					r"{}: {} {}: {}\\"\
					.format(bold("Domicilio"), makeUnderline(self.data["Dirección Contacto"], 3.35),bold("Empresa"), makeUnderline(self.data["Negocio Contacto"], 1.63))
					))

		if outputDir is "":
			outputDir = os.sys.path[0]
		#self.doc = Document()

		hasImage = self.data["Foto"] != ""
		
		self.doc.packages.append(Package("geometry", options=["a4paper"]))
		self.doc.packages.append(Package("array"))
		self.doc.packages.append(Package("fullpage"))

		self.doc.preamble.append(Command("title", bold(NoEscape(r"Solicitud de Inscripción"))))
		self.doc.preamble.append(Command('date', Command("vspace", NoEscape("-15ex"))))
		self.doc.preamble.append(Command("pagenumbering", "gobble"))
		self.doc.preamble.append(Command("hfuzz=2cm"))
		if hasImage:
			self.doc.packages.append(Package("graphicx"))
			self.doc.preamble.append(Command("graphicspath", NoEscape("{}".format("{" + self.data["Foto"][:self.data["Foto"].rfind("/")] +"/}"))))
		
		self.doc.append(NoEscape(r'\maketitle'))

		self.doc.append(NoEscape(r"\noindent"))
		InsDatosEscolares(hasImage)
		InsDatosPersonales()
		InsDatosDomicilio()
		InsDatosTrabajo()
		InsDatosFamiliares()
		InsDatosEmergencia()

		self.doc.append(NoEscape("{} {}: {}".format(Command("hfill").dumps(), bold("Fecha"), self.data["Fecha"])))

		outputName = "Inscripción_" + str("{}_" * len(outputNameRef)).format(*[self.data[x] for x in outputNameRef])[:-1]
		outputName = outputName.replace(" ", "_")

		self.doc.generate_tex("{}/{}".format("Outputs", outputName))
		os.system("{} {}/{}.tex -output-directory={}".format("pdflatex", "Outputs", outputName, outputDir))
		os.startfile("{}/{}.pdf".format(outputDir, outputName))
		os.remove("{}/{}.AUX".format(outputDir, outputName))
		os.remove("{}/{}.log".format(outputDir, outputName))

