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

	def conteudo_id(self):
		return self.tokens[self.i][ :self.tokens[self.i].find("_") ]

	def add_tab_simbs(self, id, tipo):
		for x in self.tab_simbs:
			if id == x[0]:
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
		id = self.conteudo_id()
		self.add_tab_simbs(id, tipo)
		self.prox_token()
		while True:
			if "." in self.tokens[self.i]:
				self.prox_token()
				id = self.conteudo_id()
				self.add_tab_simbs(id, tipo)
				if "id" in self.tokens[self.i]:
					self.prox_token()
				else:
					sys.stderr.write("Erro sintatico: " +tipo+ " invalido, linha:%s col:%s\n" % (str(self.linha), str(self.coluna)))
					break
			else:
				break

	# typeDeclaration ::= modifiers classDeclaration
	def type_declaration(self):
		mods = self.modifiers()
		self.class_declaration(mods)

	# modifiers ::= {public | protected | private | static | abstract} obs:falta verificar o if elif
	def modifiers(self):
		mods = ""
		if ("public" or "protected" or "private" or "static" or "abstract") not in self.tokens[self.i]:
			sys.stderr.write("Erro sintatico: tipo invalido, linha:%s col:%s\n" % (str(self.linha), str(self.coluna)))
		else:
			while True:
				if "public" in self.tokens[self.i]:
					mods += "public "
					self.prox_token()
				elif "protected" in self.tokens[self.i]:
					mods += "protected"
					self.prox_token()
				elif "private" in self.tokens[self.i]:
					mods += "private"
					self.prox_token()
				elif "abstract" in self.tokens[self.i]:
					mods += "abstract "
					self.prox_token()
				elif "static" in self.tokens[self.i]:
					mods += "static "
					self.prox_token()
				else:
					break
		return mods

	# classDeclaration ::= class <identifier> [extends qualifiedIdentifier] classBody
	def class_declaration(self, mods):
		if "class" in self.tokens[self.i]:
			self.prox_token()
			if "id" in self.tokens[self.i]:
				id = self.conteudo_id()
				self.add_tab_simbs(id, mods+"class")
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

	# classBody ::= { {modifiers memberDecl} } obs:falta fazer o loop
	def class_body(self):
		if "{" in self.tokens[self.i]:
			self.prox_token()
			mods = self.modifiers()
			self.member_decl(mods)
			'''if "}" in self.tokens[self.i]:
				self.prox_token()
			else:
				sys.stderr.write("Erro sintatico: faltou }, linha:%s col:%s\n" % (str(self.linha), str(self.coluna))) '''			
		else:
			sys.stderr.write("Erro sintatico: faltou {, linha:%s col:%s\n" % (str(self.linha), str(self.coluna))) 
	

	''' memberDecl ::= <identifier> // constructor
				formalParameters block
				| (void | type) <identifier> // method
				formalParameters (block | ;)
				| type variableDeclarators ; // field '''
	def member_decl(self, mods):
		if "id" in self.tokens[self.i]:
			id = self.conteudo_id()
			self.add_tab_simbs(id, mods)
			self.prox_token()
			self.formal_parameters()
			self.block()
		else:
			sys.stderr.write("Erro sintatico: identificador invalido, linha:%s col:%s\n" % (str(self.linha), str(self.coluna))) 
		
	# formalParameters ::= ( [formalParameter {, formalParameter}] ) obs:verificar questao do )
	def formal_parameters(self):
		if "(" in self.tokens[self.i]:
			self.prox_token()
			if ")" in self.tokens[self.i]:
				self.prox_token()
			else:
				self.formal_parameter()
				if "," in self.tokens[self.i]:
					while True:
						if "," in self.tokens[self.i]:
							self.prox_token()
							self.formal_parameter()
							if ")" in self.tokens[self.i]:
								self.prox_token()
								break
						else: # verificar necessidade
							sys.stderr.write("Erro sintatico: faltou ',' , linha:%s col:%s\n" % (str(self.linha), str(self.coluna)))
							'''while self.tokens[self.i] != ")":
								self.prox_token()'''
							break

		else:
			sys.stderr.write("Erro sintatico: faltou (, linha:%s col:%s\n" % (str(self.linha), str(self.coluna))) 

	# formalParameter ::= type <identifier>
	def formal_parameter(self):
		tipo = self.type()
		if "id" in self.tokens[self.i]:
			id = self.conteudo_id()
			self.add_tab_simbs(id, tipo)
			self.prox_token()
		else:
			sys.stderr.write("Erro sintatico: identificador invalido, linha:%s col:%s\n" % (str(self.linha), str(self.coluna))) 

	# type ::= referenceType | basicType obs:falta implementaçao
	def type(self):
		tipo = self.basic_type()
		return tipo

	''' referenceType ::= basicType [ ] {[ ]}
				| qualifiedIdentifier {[ ]} obs:falta implementaçao''' 
	def reference_type(self):
		tipo = self.basic_type()
		return tipo

	# basicType ::= boolean | char | int
	def basic_type(self):
		tipo = ""
		if "boolean" in self.tokens[self.i]:
			self.prox_token()
			tipo = "boolean"
		elif "char" in self.tokens[self.i]:
			self.prox_token()
			tipo = "char"
		elif "int" in self.tokens[self.i]:
			self.prox_token()
			tipo = "int"
		else:
			sys.stderr.write("Erro sintatico: tipo invalido, linha:%s col:%s\n" % (str(self.linha), str(self.coluna)))
			self.prox_token()
		return tipo


	# block ::= { {blockStatement} }
	def block(self):
		pass
