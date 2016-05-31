from pylatex import Section, Subsection, Subsubsection, Tabular, Package
from pylatex.base_classes import Environment
from pylatex.utils import NoEscape
from pylatex.base_classes import CommandBase
from collections import Counter
import re

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

class CustomTabular(Tabular, Environment):
	_latex_name = "tabular"
	def __init__(self, table_spec, data=None, pos=None, **kwargs):
		self.width = _get_table_width(table_spec)
		Environment.__init__(self, data=data, options=pos, arguments=table_spec, **kwargs)

def _get_table_width(table_spec):

	column_letters = ['l', 'c', 'r', 'p', 'm', 'b', 'P']

	# Remove things like {\bfseries}
	cleaner_spec = re.sub(r'{[^}]*}', '', table_spec)
	spec_counter = Counter(cleaner_spec)

	return sum(spec_counter[l] for l in column_letters)