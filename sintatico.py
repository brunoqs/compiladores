#!/usr/bin/env python3

from lexico import *

# herda a classe AnalisadorLexico
class AnalisadorSintatico(AnalisadorLexico):
	def __init__(self):
		super().__init__()
		self.i = 0
		self.linha = 0
		self.coluna = 0

	def prox_token(self):
		self.i += 1
		self.linha = self.tokens[self.i][ self.tokens[self.i].find("´")+1:self.tokens[self.i].find("|") ]
		self.coluna = self.tokens[self.i][ self.tokens[self.i].find("|")+1: ]

	def conteudo_token(self):
		return self.tokens[self.i][ self.tokens[self.i].find("_")+1:self.tokens[self.i].find("´") ]

	def add_tab_simbs(self, tipo, campo):
		for x in self.tab_simbs:
			if campo == x[1] and x[2] == "tipo":
				x[2] = tipo

	'''compilationUnit ::= [package qualifiedIdentifier ;]
					{import qualifiedIdentifier ;}
					{typeDeclaration} EOF '''
	def compilation_unit(self):
		# [package qualifiedIdentifier ;]
		if "package" in self.tokens[self.i]:
			self.prox_token()
			if "id" in self.tokens[self.i]:
				self.qualified_identifier("package")
				if ";" in self.tokens[self.i]:
					self.prox_token()
				else:
					sys.stderr.write("Erro sintatico: faltando ;, linha:%s col:%s\n" % (str(self.linha), str(self.coluna)))

			else:
				sys.stderr.write("Erro sintatico: declare um package, linha:%s col:%s\n" % (str(self.linha), str(self.coluna)))

		# {import qualifiedIdentifier ;}
		while True:
			if "import" in self.tokens[self.i]:
				self.prox_token()
				if "id" in self.tokens[self.i]:
					self.qualified_identifier("import")
					if ";" in self.tokens[self.i]:
						self.prox_token()
					else:
						sys.stderr.write("Erro sintatico: faltando ;, linha:%s col:%s\n" % (str(self.linha), str(self.coluna)))
						break
				else:
					sys.stderr.write("Erro sintatico: import invalido, linha:%s col:%s\n" % (str(self.linha), str(self.coluna)))
					break
			else:
				break
				
		# {typeDeclaration}
		self.type_declaration()

	# qualifiedIdentifier ::= <identifier> {. <identifier>}
	def qualified_identifier(self, tipo):
		campo = self.conteudo_token()
		self.add_tab_simbs(tipo, campo)
		self.prox_token()
		while True:
			if "." in self.tokens[self.i]:
				self.prox_token()
				campo = self.conteudo_token()
				self.add_tab_simbs(tipo, campo)
				if "id" in self.tokens[self.i]:
					self.prox_token()
				else:
					sys.stderr.write("Erro sintatico: package invalido, linha:%s col:%s\n" % (str(self.linha), str(self.coluna)))
					break
			else:
				break

	# typeDeclaration ::= modifiers classDeclaration
	def type_declaration(self):
		self.modifiers()
		self.class_declaration()

	# modifiers ::= {public | protected | private | static | abstract}
	def modifiers(self):
		if ("public" or "protected" or "private" or "static" or "abstract") not in self.tokens[self.i]:
			sys.stderr.write("Erro sintatico: tipo invalido, linha:%s col:%s\n" % (str(self.linha), str(self.coluna)))
		else:
			while True:
				if "public" in self.tokens[self.i]:
					self.prox_token()
				elif "protected" in self.tokens[self.i]:
					self.prox_token()
				elif "private" in self.tokens[self.i]:
					self.prox_token()
				elif "abstract" in self.tokens[self.i]:
					self.prox_token()
				else:
					break

	# classDeclaration ::= class <identifier> [extends qualifiedIdentifier] classBody
	def class_declaration(self):
		if "class" in self.tokens[self.i]:
			self.prox_token()
			if "id" in self.tokens[self.i]:
				campo = self.conteudo_token()
				self.add_tab_simbs("class", campo)
				self.prox_token()
				if "extends" in self.tokens[self.i]:
					self.prox_token()
					if "id" in self.tokens[self.i]:
						self.qualified_identifier("extends")
					else:
						sys.stderr.write("Erro sintatico: extends invalido, linha:%s col:%s\n" % (str(self.linha), str(self.coluna))) 	
				self.class_body()
			else:
				sys.stderr.write("Erro sintatico: class invalida, linha:%s col:%s\n" % (str(self.linha), str(self.coluna))) 
		else:
			sys.stderr.write("Erro sintatico: class invalida, linha:%s col:%s\n" % (str(self.linha), str(self.coluna))) 

	def class_body(self):
		pass

''' TODO: Guardar linha e coluna nos tokens do analisador lexico
		
'''		