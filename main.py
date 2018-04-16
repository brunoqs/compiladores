#!/usr/bin/env python3

import string
import sys
import re

class AnalisadorLexico:

	def __init__(self):
		self.tokens = []
		self.tab_simb = []
		self.reservadas = ["abstract", "extends", "int", "protected", "this", "boolean", "false", "new", "public", "true", "char", "import", \
		 "null", "return", "void", "class", "if", "package", "static", "while", "else", "instanceof", "private", "super"]
		self.operadores = ["=", "==", ">", "++", "&&", "<=", "!", "-", "--", "+", "+=", "*"]
		self.separadores = [",", ".", "[", "{", "(", ")", "}", "]", ";"]

	def e_reservada(self, palavra):
		if palavra in self.reservadas:
			return True
		return False

	def e_operador(self, palavra):
		if palavra in self.operadores:
			return True
		return False

	def e_separador(self, caracter):
		if caracter in self.separadores:
			return True
		return False

	def e_indentificador(self, palavra):
		if palavra in string.ascii_letters or palavra in string.digits:
			return True
		return False

	def analisador(self, arquivo):
		linha = arquivo.readline()
		n_linha = 1

		while linha:
			i = 0
			tam_linha = len(linha)
			while i < tam_linha:
				caracter_atual = linha[i]
				caracter_seguinte = None

				# pega prox caracter se existir
				if i+1 < tam_linha:
					caracter_seguinte = linha[i+1]

				#armazena separador no token
				if self.e_separador(caracter_atual):
					self.tokens.append(caracter_atual)
				#ignora comentario
				elif caracter_atual == "/" and caracter_seguinte == "/":
					i = tam_linha
				#armazena operador de 2 simbolo no token
				elif caracter_seguinte != None and self.e_operador(caracter_atual+caracter_seguinte):
					self.tokens.append(caracter_atual+caracter_seguinte)
					i += 1 
				#armazena operador de 1 simbolo no token
				elif self.e_operador(caracter_atual):
					self.tokens.append(caracter_atual)

				# incrementa leitura de caracter
				i += 1

			linha = arquivo.readline()
			n_linha += 1

if __name__ == '__main__':
	nome_arquivo = sys.argv[1]
	arquivo = open(nome_arquivo, "r")

	lexico = AnalisadorLexico()
	lexico.analisador(arquivo)
	print (lexico.tokens)