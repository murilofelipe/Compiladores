tabelaDeSimbolos = []

class symbolTabel:

	identifier = ''
	category = ""
	level = 0
	variantInfo = []

	def _init_(self,id,cat,lvl,varInfo):
		self.identifier = id
		self.category = cat
		self.lvl = lvl
		self.variantInfo = varInfo

if _name_ == '_main_':
	x = symbolTabel('x',"category",0,[1,2])
	tabelaDeSimbolos.append(x)
	y = symbolTabel('y',"category",0,[1,2,3])
	tabelaDeSimbolos.append(y)