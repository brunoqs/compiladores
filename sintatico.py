#!/usr/bin/env python3

from lexico import *
import pdb

'''TODO: Verificar questao da comparacao com id com o token 

'''

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

	def ant_token(self):
		self.i -= 1
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
			if "id" in self.tokens[self.i] and "_" in self.tokens[self.i]:
				self.qualified_identifier("package")
				if ";" in self.tokens[self.i]:
					self.prox_token()
				else:
					self.ant_token()
					sys.stderr.write("Erro sintatico: faltando ;, linha:%s col:%s\n" % (str(self.linha), str(self.coluna)))
					self.prox_token()
			else:
				sys.stderr.write("Erro sintatico: package invalido, linha:%s col:%s\n" % (str(self.linha), str(self.coluna)))
				while "import" not in self.tokens[self.i]:
					self.prox_token()

		# {import qualifiedIdentifier ;}
		while True:
			if "import" in self.tokens[self.i]:
				self.prox_token()
				if "id" in self.tokens[self.i] and "_" in self.tokens[self.i]:
					self.qualified_identifier("import")
					if ";" in self.tokens[self.i]:
						self.prox_token()
					else:
						self.ant_token()
						sys.stderr.write("Erro sintatico: faltando ;, linha:%s col:%s\n" % (str(self.linha), str(self.coluna)))
						self.prox_token()
				else:
					sys.stderr.write("Erro sintatico: import invalido, linha:%s col:%s\n" % (str(self.linha), str(self.coluna)))
					#while ("public" not in self.tokens[self.i]) or ("protected" not in self.tokens[self.i]) or ("private" not in self.tokens[self.i]):
					#	self.prox_token()
			else:
				break
				
		# {typeDeclaration} obs: falta loop
		self.type_declaration()

	# qualifiedIdentifier ::= <identifier> {. <identifier>}
	def qualified_identifier(self, tipo=""):
		id = self.conteudo_id()
		self.add_tab_simbs(id, tipo)
		self.prox_token()
		while True:
			if "." in self.tokens[self.i]:
				self.prox_token()
				id = self.conteudo_id()
				self.add_tab_simbs(id, tipo)
				if "id" in self.tokens[self.i] and "_" in self.tokens[self.i]:
					self.prox_token()
				else:
					sys.stderr.write("Erro sintatico: " +tipo+ " invalido, linha:%s col:%s\n" % (str(self.linha), str(self.coluna)))

			else:
				break

	# typeDeclaration ::= modifiers classDeclaration
	def type_declaration(self):
		mods = self.modifiers()
		self.class_declaration(mods)

	# modifiers ::= {public | protected | private | static | abstract} obs:falta verificar o if elif
	def modifiers(self):
		mods = ""
		if "public" in self.tokens[self.i] or "protected" in self.tokens[self.i] or "private" in self.tokens[self.i] or "static" in self.tokens[self.i] or "abstract" in self.tokens[self.i]:
			while True:
				if "public" in self.tokens[self.i]:
					mods += "public "
					self.prox_token()
				elif "protected" in self.tokens[self.i]:
					mods += "protected "
					self.prox_token()
				elif "private" in self.tokens[self.i]:
					mods += "private "
					self.prox_token()
				elif "abstract" in self.tokens[self.i]:
					mods += "abstract "
					self.prox_token()
				elif "static" in self.tokens[self.i]:
					mods += "static "
					self.prox_token()
				else:
					break
		else:
			sys.stderr.write("Erro sintatico: modificador invalido, linha:%s col:%s\n" % (str(self.linha), str(self.coluna)))
			self.prox_token()
		return mods

	# classDeclaration ::= class <identifier> [extends qualifiedIdentifier] classBody
	def class_declaration(self, mods):
		if "class" in self.tokens[self.i]:
			self.prox_token()
			if "id" in self.tokens[self.i] and "_" in self.tokens[self.i]:
				id = self.conteudo_id()
				self.add_tab_simbs(id, mods+"class")
				self.prox_token()
				if "extends" in self.tokens[self.i]:
					self.prox_token()
					if "id" in self.tokens[self.i] and "_" in self.tokens[self.i]:
						self.qualified_identifier("extends")
					else:
						sys.stderr.write("Erro sintatico: extends invalido, linha:%s col:%s\n" % (str(self.linha), str(self.coluna))) 	
				self.class_body()
			else:
				sys.stderr.write("Erro sintatico: class invalida, linha:%s col:%s\n" % (str(self.linha), str(self.coluna))) 
		else:
			sys.stderr.write("Erro sintatico: class invalida, linha:%s col:%s\n" % (str(self.linha), str(self.coluna)))
			while "{" not in self.tokens[self.i]:
				self.prox_token()
			self.class_body()

	# classBody ::= { {modifiers memberDecl} } 
	def class_body(self):
		if "{" in self.tokens[self.i]:
			self.prox_token()
			while "}" not in self.tokens[self.i]:
				mods = self.modifiers()
				self.member_decl(mods)
			if "}" in self.tokens[self.i]:
				if self.i < len(self.tokens)-1:
					self.prox_token()
			else:
				sys.stderr.write("Erro sintatico: faltou }, linha:%s col:%s\n" % (str(self.linha), str(self.coluna)))			
		else:
			sys.stderr.write("Erro sintatico: faltou {, linha:%s col:%s\n" % (str(self.linha), str(self.coluna))) 
	

	''' memberDecl ::= <identifier> // constructor
				formalParameters block
				| (void | type) <identifier> // method
				formalParameters (block | ;)
				| type variableDeclarators ; // field '''
	def member_decl(self, mods):
		if "id" in self.tokens[self.i] and "_" in self.tokens[self.i]:
			id = self.conteudo_id()
			self.add_tab_simbs(id, mods)
			self.prox_token()
			self.formal_parameters()
			self.block()
		elif (("int" in self.tokens[self.i]) or ("void" in self.tokens[self.i]) or ("char" in self.tokens[self.i]) or ("boolean" in self.tokens[self.i])) and ("(" in self.tokens[self.i+2]):
			tipo = ""
			if "void" == self.conteudo_token():
				self.prox_token()
				tipo = "void"
			else:
				tipo = self.type()
			if "id" in self.tokens[self.i] and "_" in self.tokens[self.i]:
				id = self.conteudo_id()
				self.add_tab_simbs(id, mods+tipo)
				self.prox_token()
				self.formal_parameters()
				if ";" in self.tokens[self.i]:
					self.prox_token()
				else:
					self.block()
		# verificar se e ambiguidade
		elif "int" in self.tokens[self.i] or "char" in self.tokens[self.i] or "boolean" in self.tokens[self.i]:
			tipo = self.type()
			self.variable_declarators(mods+tipo)
			if ";" in self.tokens[self.i]:
				self.prox_token()
			else:
				self.ant_token()
				sys.stderr.write("Erro sintatico: faltou ;, linha:%s col:%s\n" % (str(self.linha), str(self.coluna))) 	
				self.prox_token()
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
					if ")" in self.tokens[self.i]:
						self.prox_token()
		else:
			sys.stderr.write("Erro sintatico: faltou ( ou ), linha:%s col:%s\n" % (str(self.linha), str(self.coluna)))
			while "{" not in self.tokens[self.i]:
				self.prox_token()  

	# formalParameter ::= type <identifier>
	def formal_parameter(self):
		tipo = self.type()
		if "id" in self.tokens[self.i] and "_" in self.tokens[self.i]:
			id = self.conteudo_id()
			self.add_tab_simbs(id, tipo)
			self.prox_token()
		else:
			sys.stderr.write("Erro sintatico: identificador invalido, linha:%s col:%s\n" % (str(self.linha), str(self.coluna))) 

	# type ::= referenceType | basicType obs:falta implementaçao
	def type(self):
		# verifica 1 token a frente se tem []
		if "[" in self.tokens[self.i+1]:
			tipo = self.reference_type()
		else:
			tipo = self.basic_type()
		return tipo

	''' referenceType ::= basicType [ ] {[ ]}
				| qualifiedIdentifier {[ ]} obs:falta analisar qualified_identifier e loop''' 
	def reference_type(self):
		if self.tokens[self.i+1] == ".":
			self.qualified_identifier()
		else:
			tipo = self.basic_type()
			if "[" in self.tokens[self.i]:
				self.prox_token()
				if "]" in self.tokens[self.i]:
					self.prox_token()
				else:
					sys.stderr.write("Erro sintatico: faltou ] , linha:%s col:%s\n" % (str(self.linha), str(self.coluna))) 
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


	# block ::= { {blockStatement} } obs: falta fazer o loop
	def block(self):
		if "{" in self.tokens[self.i]:
			self.prox_token()
			while "}" not in self.tokens[self.i]:
				self.block_statement()
			if "}" in self.tokens[self.i]:
				if self.i < len(self.tokens)-1:
					self.prox_token()
			else:
				sys.stderr.write("Erro sintatico: faltou }, linha:%s col:%s\n" % (str(self.linha), str(self.coluna)))	
		else:
			sys.stderr.write("Erro sintatico: faltou {, linha:%s col:%s\n" % (str(self.linha), str(self.coluna))) 


	# blockStatement ::= localVariableDeclarationStatement | statement
	def block_statement(self):
		if ("int" in self.tokens[self.i]) or ("char" in self.tokens[self.i]) or ("boolean" in self.tokens[self.i]):
			self.local_variable_declatarion_statement()
		else:
			self.statement()

	# localVariableDeclarationStatement ::= type variableDeclarators ;
	def local_variable_declatarion_statement(self):
		tipo = self.type()
		self.variable_declarators(tipo)
		if ";" in self.tokens[self.i]:
			self.prox_token()
		else:
			sys.stderr.write("Erro sintatico: faltando ;, linha:%s col:%s\n" % (str(self.linha), str(self.coluna)))

	# variableDeclarators ::= variableDeclarator {, variableDeclarator} obs: falta errors
	def variable_declarators(self, tipo):
		self.variable_declarator(tipo)
		if "," in self.tokens[self.i]:
			while True:
				if "," in self.tokens[self.i]:
					self.prox_token()
					self.variable_declarator(tipo)
				else:
					break

	# variableDeclarator ::= <identifier> [= variableInitializer] obs: falta errors
	def variable_declarator(self, tipo):
		if "id" in self.tokens[self.i] and "_" in self.tokens[self.i]:
			id = self.conteudo_id()
			self.add_tab_simbs(id, tipo)
			self.prox_token()
			if "=" in self.tokens[self.i]:
				self.prox_token()
				inicial = self.variable_initializer(tipo)
				id = self.conteudo_id()
				self.add_tab_simbs(id, inicial)

	# variableInitializer ::= arrayInitializer | expression
	def variable_initializer(self, tipo):
		if "{" in self.tokens[self.i]:
			self.prox_token()
			self.array_initializer(tipo)
		else:
			return self.expression()

	# arrayInitializer ::= { [variableInitializer {, variableInitializer}] } obs: falta errors
	def array_initializer(self, tipo):
		 if "}" in self.tokens[self.i]:
		 	self.prox_token()
		 else:
		 	while True:
		 		if ("num" or "id") and "_" in self.tokens[self.i]:
		 			id = self.conteudo_id()
		 			self.add_tab_simbs(id, tipo)
		 			self.prox_token()
		 		elif "," in self.tokens[self.i]:
		 			self.prox_token()
		 		elif "}" in self.tokens[self.i]:
		 			self.prox_token()
		 			break

	# expression ::= assignmentExpression
	def expression(self):
		return self.assignment_expression()

	'''assignmentExpression ::= conditionalAndExpression // must be a valid lhs
						[(= | +=) assignmentExpression] '''
	def assignment_expression(self):
		lhs = self.conditional_and_expression()
		flag = True
		while flag:
			if "=" in self.tokens[self.i]:
				self.prox_token()
				self.assignment_expression()
			elif "+=" in self.tokens[self.i]:
				self.prox_token()
				self.assignment_expression()
			else:
				flag = False
		return lhs

	'''conditionalAndExpression ::= equalityExpression // level 10
							{&& equalityExpression} '''
	def conditional_and_expression(self):
		lhs = self.equality_expression()
		flag = True
		while flag:
			if "&&" in self.tokens[self.i]:
				self.prox_token()
				self.equality_expression()
			else:
				flag = False
		return lhs

	'''equalityExpression ::= relationalExpression // level 6
						{== relationalExpression} '''
	def equality_expression(self):
		lhs = self.relational_expression()
		flag = True
		while flag:
			if "==" in self.tokens[self.i]:
				self.prox_token()
				self.relational_expression()
			else:
				flag = False
		return lhs

	'''relationalExpression ::= additiveExpression // level 5
						[(> | <=) additiveExpression | instanceof referenceType] obs:falta instanceof'''
	def relational_expression(self):
		lhs = self.additive_expression()
		flag = True
		while flag:
			if ">" in self.tokens[self.i]:
				self.prox_token()
				self.additive_expression()
			elif "<=" in self.tokens[self.i]:
				self.prox_token()
				self.additive_expression()
			else:
				flag = False
		return lhs

	'''additiveExpression ::= multiplicativeExpression // level 3
						{(+ | -) multiplicativeExpression} '''
	def additive_expression(self):
		lhs = self.multiplicative_expression()
		flag = True
		while flag:
			if "+" in self.tokens[self.i]:
				self.prox_token()
				self.unary_expression()
			elif "-" in self.tokens[self.i]:
				self.prox_token()
				self.unary_expression()
			else:
				flag = False
		return lhs

	''' multiplicativeExpression ::= unaryExpression // level 2
							{* unaryExpression}''' 
	def multiplicative_expression(self):
		lhs = self.unary_expression()
		flag = True
		while flag:
			if "*" in self.tokens[self.i]:
				self.prox_token()
				self.unary_expression()
			else:
				flag = False
		return lhs 

	''' unaryExpression ::= ++ unaryExpression // level 1
					| - unaryExpression
					| simpleUnaryExpression ''' 
	def unary_expression(self):
		if "++" in self.tokens[self.i]:
			self.prox_token()
			self.unary_expression()
		elif "-" in self.tokens[self.i]:
			self.prox_token()
			self.unary_expression()
		else:
			return self.simple_unary_expression()

	''' simpleUnaryExpression ::= ! unaryExpression
						| ( basicType ) unaryExpression //cast
						| ( referenceType ) simpleUnaryExpression // cast
						| postfixExpression obs:falta implementacao'''
	def simple_unary_expression(self):
		if "!" in self.tokens[self.i]:
			self.prox_token()
			self.unary_expression()
		else:
			return self.postfix_expression()

	# postfixExpression ::= primary {selector} {--} obs:falta implementacao
	def postfix_expression(self):
		primary = self.primary()
		if "." in self.tokens[self.i]:
			self.selector()
		return primary


	''' primary ::= parExpression
			| this [arguments]
			| super (arguments | . <identifier> [arguments])
			| literal
			| new creator
			| qualifiedIdentifier [arguments] obs:falta implementacao''' 
	def primary(self):
		if "(" in self.tokens[self.i]:
			self.par_expression()
		elif "this" in self.tokens[self.i]:
			self.prox_token()
			if "(" in self.tokens[self.i]:
				self.arguments()
		elif "super" in self.tokens[self.i]:
			pass
		elif "new" in self.tokens[self.i]:
			self.creator()
		elif "id" in self.tokens[self.i] and "_" in self.tokens[self.i]:
			self.qualified_identifier()
		else:
			return self.literal()

	# parExpression ::= ( expression )
	def par_expression(self):
		if "(" in self.tokens[self.i]:
			self.prox_token()
			inicial = self.expression()
			id = self.conteudo_id()
			self.add_tab_simbs(id, inicial)
			if ")" in self.tokens[self.i]:
				self.prox_token()
			else:
				sys.stderr.write("Erro sintatico: faltando ), linha:%s col:%s\n" % (str(self.linha), str(self.coluna)))


	# arguments ::= ( [expression {, expression}] )
	def arguments(self):
		if "(" in self.tokens[self.i] and ")" in self.tokens[self.i+1]:
			self.prox_token()
			self.prox_token()
			return 
		else: # implementar
			self.prox_token()
			exp = self.expression()
			id = self.conteudo_id()
			self.add_tab_simbs(id, exp)
			if "," in self.tokens[self.i]:
				while True:
					if "," in self.tokens[self.i]:
						self.prox_token()



	# literal ::= <int_literal> | <char_literal> | <string_literal> | true | false | null
	def literal(self):
		if "num" in self.tokens[self.i] and "_" in self.tokens[self.i]:
			self.prox_token()
			return "int"
		elif "ch" in self.tokens[self.i] and "_" in self.tokens[self.i]:
			self.prox_token()
			return "char"
		elif "str" in self.tokens[self.i] and "_" in self.tokens[self.i]:
			self.prox_token()
			return "String"
		elif "true" in self.tokens[self.i]:
			self.prox_token()
			return "true"
		elif "false" in self.tokens[self.i]:
			self.prox_token()
			return "false"
		elif "null" in self.tokens[self.i]:
			self.prox_token()
			return "null"

	''' creator ::= (basicType | qualifiedIdentifier)
			( arguments
			| [ ] {[ ]} [arrayInitializer]
			| newArrayDeclarator '''
	def creator(self):
		pass

	# newArrayDeclarator ::= [ expression ] {[ expression ]} {[ ]}
	def new_array_declarator(self):
		pass

	# selector ::= . qualifiedIdentifier [arguments] | [ expression ]
	def selector(self):
		if "." in self.tokens[self.i]:
			self.prox_token()
			self.qualified_identifier()

	''' statement ::= block
			| <identifier> : statement
			| if parExpression statement [else statement]
			| while parExpression statement
			| return [expression] ;
			| ;
			| statementExpression ; '''
	def statement(self):
		if "{" in self.tokens[self.i]:
			self.block()
		elif "if" in self.tokens[self.i]:
			self.prox_token()
			self.par_expression()
			self.statement()
			if "else" in self.tokens[self.i]:
				self.prox_token()
				self.statement()
		elif "while" in self.tokens[self.i]:
			self.prox_token()
			self.par_expression()
			self.statement()
		elif "return" in self.tokens[self.i]:
			self.prox_token()
			if ";" in self.tokens[self.i]:
				self.prox_token()
			else:
				self.expression()
		elif ";" in self.tokens[self.i]:
			self.prox_token()
		else:
			self.statement_expression()

	# statementExpression ::= expression // but must have side-e↵ect, eg i++
	def statement_expression(self):
		self.expression()
