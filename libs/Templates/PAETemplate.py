from pylatex import Command, Package, Tabular, MultiRow, Enumerate
from pylatex.utils import NoEscape, bold
import os
from libs.CustomPyLatex import *
from libs.Templates.BaseTemplate import Formato

class PAE(Formato):
	def CreateDoc(self, outputNameRef=[""], outputDir=""):

		if outputDir is "":
			outputDir = os.sys.path[0]

		hasImage = self.data["Foto"] != ""
		self.doc.packages.append(Package("geometry", options=["a4paper"]))
		self.doc.packages.append(Package("array"))
		self.doc.packages.append(Package("fullpage"))
		self.doc.packages.append(Package("enumitem"))

		self.doc.preamble.append(Command("title", bold(NoEscape(r"Programa de Ayuda Económica\\PAE"))))
		self.doc.preamble.append(Command('date', Command("vspace", NoEscape("-10ex"))))
		self.doc.preamble.append(Command("pagenumbering", "gobble"))
		self.doc.preamble.append(Command("hfuzz=2cm"))
		self.doc.preamble.append(Command(command="newcolumntype", arguments="P", options="1", extra_arguments=NoEscape(r">{\centering\arraybackslash}p{#1}")))
		if hasImage:
			self.doc.packages.append(Package("graphicx"))
			self.doc.preamble.append(Command("graphicspath", NoEscape("{}".format("{" + self.data["Foto"][:self.data["Foto"].rfind("/")] +"/}"))))
		
		self.doc.append(NoEscape(r'\maketitle'))

		self.doc.append(NoEscape(r"\noindent"))

		if hasImage:
			image = NoEscape(r"{}{}\\".format(Command("hfill").dumps(), Command("includegraphics", NoEscape(self.data["Foto"][self.data["Foto"].rfind("/") + 1:][:self.data["Foto"].rfind(".")]),["width=1.5in", "height=1in"]).dumps()	))
			self.doc.append(image)
		else:
			self.doc.append(NoEscape(r" \\\\\\\\\\"))

		intro = NoEscape(r"La {} otorga al presente {} consistente en un financiamiento de: {}\% en las cuotas de inscripción y colecgiaturas mensuales a:\\"\
			.format(bold("Universidad Cuauhnáhuac"), bold("Ayuda Económica"), self.data["Porcentaje"]))

		self.doc.append(intro)

		self.doc.append(NoEscape(\
					r"{}: {} {}: {} \\"\
					.format( bold("Nombre"), makeUnderline(self.data["Nombre"], 2.5), bold("Matrícula No"), makeUnderline(self.data["Matrícula"], 1.5) )
					))
		
		self.doc.append(NoEscape(\
					r"{}: {} {}: {}\\"\
					.format( bold("Licenciatura"), makeUnderline(self.data["Licenciatura"], 2.0), bold("Turno"), makeUnderline(self.data["Turno"],1.0))
					))

		self.doc.append(NoEscape(\
					r"{}: {} {}: {}\\"\
					.format(bold("Semestre"), makeUnderline(self.data["Semestre"], 3.35),bold("Generación"), makeUnderline(self.data["Generación"], 1.63))
					))

		self.doc.append(NoEscape(\
					r"{}: {} \\"\
					.format(bold("Primer ciclo escolar"), makeUnderline(self.data["Primer Ciclo Escolar"], 3))
					))

		self.doc.append("Comprometiéndose a cumplir lo siguiente")

		with self.doc.create(Enumerate(options=[NoEscape(r"label=\Alph*)")])) as enum:
			enum.add_item(NoEscape("Obtener un promedio mínimo general al término de cada semestre de: " + self.data["Promedio Mínimo"]))
			enum.add_item(NoEscape(r"Tener como mínimo " + self.data["Asistencia Mínima"] + "\% de asistencia a clases."))
			enum.add_item(NoEscape("Cumplir con las disposiciones del reglamento de los alumnos."))
			enum.add_item(NoEscape("Concluir sus estudios universitarios en UNIC."))
			enum.add_item(NoEscape(r"En caso de que al término de cada semestre no cumpla con el promedio al cual se comprometió el punto “A” se reducirá en un 10\% la ayuda del presente apoyo a la cuota vigente."))
			enum.add_item(NoEscape("En caso de que el alumno solicita su baja definitiva deberá cubrir el importe total financiado, del tiempo que cursó sus estudios en la Universidad Cuauhnáhuac."))
			enum.add_item(NoEscape("Al concluir el alumno con sus estudios universitarios se cancelará automáticamente el importe total de la parte financiada."))

		with self.doc.create(CustomTabular(NoEscape("|P{1.8in}|P{1.8in}|P{1.8in}|"))) as table:
			table.add_hline()
			table.add_row((NoEscape(bold("Alumno")), NoEscape(bold("Padre o Tutor")), NoEscape(bold("Autorización"))))
			table.add_row(("","",""))
			table.add_row(("","",""))
			table.add_row(("","",""))
			table.add_row(("Nombre y Firma", "Nombre y Firma", "Diana Pérez Brito"))
			table.add_hline()

		self.doc.append(NoEscape(Command("centering").dumps()))
		self.doc.append(NoEscape(bold(NoEscape(r"\\Este documento no será válido si presenta tachaduras o enmendaduras\\"))))

		self.doc.append(NoEscape("{} {}: {}".format(Command("hfill").dumps(), bold("Fecha"), self.data["Fecha"])))

		outputName = "PAE_" + str("{}_" * len(outputNameRef)).format(*[self.data[x] for x in outputNameRef])[:-1]

		outputName = outputName.replace(" ", "_")
		self.doc.generate_tex("{}/{}".format("Outputs", outputName))

		os.system("{} {}/{}.tex -output-directory={} -quiet".format("pdflatex", "Outputs", outputName, outputDir))
		os.startfile("{}/{}.pdf".format(outputDir, outputName))
		os.remove("{}/{}.AUX".format(outputDir, outputName))
		os.remove("{}/{}.log".format(outputDir, outputName))