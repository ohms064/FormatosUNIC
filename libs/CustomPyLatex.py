from pylatex import Section, Subsection, Subsubsection
from pylatex.utils import NoEscape
from pylatex.base_classes import CommandBase
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