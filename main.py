#!/usr/bin/env python3

import string
import sys
import re

class AnalisadorLexico:

	def __init__(self):
		self.tokens = []
		self.reservadas = ["abstract", "extends", "int", "protected", "this", "boolean", "false", "new", "public", "true", "char", "import", \
		 "null", "return", "void", "class", "if", "package", "static", "while", "else", "instanceof", "private", "super"]
		self.operadores = ["=", "==", ">", "++", "&&", "<=", "!", "-", "--", "+", "+=", "*"]
		self.operadores_s = "=>+&<!-*"
		self.separadores = ",.[{()}];"

	# verifica se uma palavra do codigo fonte e uma palavra reservada
	def e_reservada(self, palavra):
		for reservada in self.reservadas:
			if reservada == palavra:
				token = ("reservada")
				self.tokens.append(token)
			#elif reservada in palavra:
				#pos = palavra.find(reservada)
				#if palavra[pos] 
				# todo with re

	def e_operador(self, palavra, id):
		for operador in self.operadores:
			if operador == palavra: # se o operador esta sozinho
				token = (operador)
				self.tokens.append(token)
			elif operador in palavra: # se o operador esta no meio da palavra
				pos = palavra.find(operador)
				if palavra[pos+1] in self.operadores_s: # pega mais um operador se tiver
					token = (operador+palavra[pos+1])
				if palavra[:pos] not in self.separadores and palavra[:pos] not in self.reservadas: # pega um identificador
					token = ("identificador", id)
				if palavra[pos:] not in self.separadores and palavra[:pos] not in self.reservadas: # pega um identificador
					token = ("identificador", id)

	def e_indentificador(self, palavra, id):
		if palavra in string.ascii_letters or palavra in string.digits:
			token = ("identificador", id)

	def e_separador(self, palavra):
		pass

if __name__ == '__main__':
	nome_arquivo = sys.argv[1]
	arquivo = open(nome_arquivo, "r")
	arquivo = arquivo.readlines()
	lexico = AnalisadorLexico()
	id = 0
	for linha in arquivo:
		linha = linha.split()
		print (linha)
		lexico.e_reservada(linha)
		print (lexico.tokens)