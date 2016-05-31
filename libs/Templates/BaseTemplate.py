from pylatex import Document
from collections import defaultdict
class Formato():
	def __init__(self):
		self.doc = Document()
		self.data = defaultdict(str)

	def CreateDoc(self, dataDict, outputNameRef=[""], outputDir=""):
		pass

	def Flush(self):
		self.__init__()
