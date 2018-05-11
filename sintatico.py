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
		self.linha = self.tokens[self.i][ self.tokens[self.i].find("´")+2:self.tokens[self.i].find("|") ]
		self.coluna = self.tokens[self.i][ self.tokens[self.i].find("|")+1: ]

	def compilation_unit(self):
		if "package" in self.tokens[self.i]:
			self.prox_token()
			if "id" in self.tokens[self.i]:
				
		else:
			sys.stderr.write("Erro sintatico: declare um package, linha:%s col:%s\n" % (str(self.linha), str(self.coluna)))

	def qualified_identifier(self):
		

''' TODO: Guardar linha e coluna nos tokens do analisador lexico
		
'''		