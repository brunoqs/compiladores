#!/usr/bin/env python3

import string
import sys
import re

class AnalisadorLexico:

	def __init__(self):
		self.tokens = []
		self.tab_simbs = []
		self.reservadas = ["abstract", "extends", "int", "protected", "this", "boolean", "false", "new", "public", "true", "char", "import", \
		 "null", "return", "void", "class", "if", "package", "static", "while", "else", "instanceof", "private", "super"]
		self.operadores = ["=", "==", ">", "++", "&&", "<=", "!", "-", "--", "+", "+=", "*"]
		self.separadores = [",", ".", "[", "{", "(", ")", "}", "]", ";"]
		self.simbolos = ''' !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHJKLMNOPQRSTUVXWYZ[\]^_`abcdefghijklmnopqrstuvxwyz{|}~'''

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

	def e_letra(self, caracter):
		if caracter in string.ascii_letters:
			return True
		return False

	def e_digito(self, caracter):
		if caracter in string.digits:
			return True
		return False

	def e_simbolo(self, caracter):
		if caracter in self.simbolos:
			return True
		return False

	def analisador(self, arquivo):
		linha = arquivo.readline()
		n_linha = 1

		while linha:
			i = 0 # ponteiro do arquivo 
			id = 0 # id tabela de simbolos
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
				#verifica char
				elif caracter_atual == "\'":
					# encontrou caracter
					if self.e_simbolo(linha[i+1]) and linha[i+1] != "\'" and linha[i+2] == "\'":
						id += 1
						token = (linha[i+1], id)
						self.tab_simbs.append([id, linha[i+1], "char"])
						self.tokens.append(token)
						i += 2
					# nao fechar '
					elif linha[i+1] == "\n" or not "\'" in linha[i+1:]:
						sys.stderr.write("Error lexico: faltou fechar aspas simples, linha:%s\n" % str(n_linha))
						sys.exit(1)
					else:
						sys.stderr.write("Error lexico: tamanho ou caracter invalido, linha:%s\n" % str(n_linha))
						sys.exit(1)						
				#verifica string
				elif caracter_atual == "\"":
					i += 1
					valido = True

					#nao encontrou " fechando
					if linha[i:].find("\"") == -1:
						sys.stderr.write("Error lexico: faltou fechar aspas duplas, linha:%s\n" % str(n_linha))
						sys.exit(1)
					else:
						fim_string = i+linha[i:].find("\"")
						string = linha[i:fim_string]
						i = fim_string
						for s in string:
							if not self.e_simbolo(s):
								valido = False
								sys.stderr.write("Error lexico: string invalida, linha:%s\n" % str(n_linha))
								sys.exit(1)	
						if valido:
							id += 1
							token = (string, id)
							self.tab_simbs.append([id, string, "string"])
							self.tokens.append(token)						
				#verificando numeros
				elif self.e_digito(caracter_atual):
					pass
				# verificando identificadores
				elif self.e_letra(caracter_atual):
					pass

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
	print (lexico.tab_simbs)