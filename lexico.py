#!/usr/bin/env python3

#A estrutura token contem a linha e a coluna do token capturado, ex:
# apos ´ tem a linha e apos | tem a coluna
# {´5|5

#Caso o token seja um identificador, um numero, um char ou uma string será respresentado como o ex, respectivamente:
# id_nomevariavel´1|2
# num_12321´5|6
# ch_a´1|2
# str_ola´1|2

import string
import sys
import numpy as np

class AnalisadorLexico(object):

	def __init__(self):
		self.tokens = []
		self.tab_simbs = []
		self.reservadas = ["abstract", "extends", "int", "protected", "this", "boolean", "false", "new", "public", "true", "char", "import", \
		 "null", "return", "void", "class", "if", "package", "static", "while", "else", "instanceof", "private", "super"]
		self.operadores = ["=", "==", ">", "++", "&&", "<=", "!", "-", "--", "+", "+=", "*"]
		self.separadores = [",", ".", "[", "{", "(", ")", "}", "]", ";"]
		self.simbolos = ''' !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHJKLMNOPQRSTUVXWYZ[\]^_`abcdefghijklmnopqrstuvxwyz}{~'''

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
		if caracter in string.ascii_letters or caracter in "_":
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
		id = 0 # id tabela de simbolos

		while linha:
			i = 0 # ponteiro do arquivo 
			tam_linha = len(linha)
			while i < tam_linha:
				caracter_atual = linha[i]
				caracter_seguinte = None

				# pega prox caracter se existir
				if i+1 < tam_linha:
					caracter_seguinte = linha[i+1]

				#armazena separador no token
				if self.e_separador(caracter_atual):
					if caracter_atual == "." and self.e_digito(caracter_seguinte):
						sys.stderr.write("Erro lexico: float nao e permitido, linha:%s col:%s\n" % (str(n_linha), str(i)))
						while self.e_digito(caracter_seguinte):
							i += 1
							caracter_seguinte = linha[i]
							if not self.e_digito(caracter_seguinte):
								i -= 1
					else:
						self.tokens.append(caracter_atual+"´"+str(n_linha)+"|"+str(i))
				#ignora comentario
				elif caracter_atual == "/" and caracter_seguinte == "/":
					i = tam_linha
				#armazena operador de 2 simbolo no token
				elif caracter_seguinte != None and self.e_operador(caracter_atual+caracter_seguinte):
					self.tokens.append(caracter_atual+caracter_seguinte+"´"+str(n_linha)+"|"+str(i))
					i += 1 
				#armazena operador de 1 simbolo no token
				elif self.e_operador(caracter_atual):
					self.tokens.append(caracter_atual+"´"+str(n_linha)+"|"+str(i))
				#verifica char
				elif caracter_atual == "\'":
					# encontrou caracter
					if self.e_simbolo(linha[i+1]) and linha[i+1] != "\'" and linha[i+2] == "\'":
						id += 1
						self.tab_simbs.append(["ch"+str(id), linha[i+1], "char"])
						self.tokens.append("ch"+str(id)+"_"+linha[i+1]+"´"+str(n_linha)+"|"+str(i))
						i += 2
					# nao fechar '
					elif linha[i+1] == "\n" or not "\'" in linha[i+1:]:
						sys.stderr.write("Erro lexico: faltou fechar aspas simples, linha:%s col:%s\n" % (str(n_linha), str(i)))
						i = tam_linha
					else:
						sys.stderr.write("Erro lexico: tamanho ou caracter invalido, linha:%s col:%s\n" % (str(n_linha), str(i)))
						i = linha.find("\'") + linha[i+1:].find("\'")+1	
				#verifica string
				elif caracter_atual == "\"":
					i += 1

					#nao encontrou " fechando
					if linha[i:].find("\"") == -1:
						sys.stderr.write("Erro lexico: faltou fechar aspas duplas, linha:%s col:%s\n" % (str(n_linha), str(i)))
						i = tam_linha
					else:
						flag = False
						fim_string = i+linha[i:].find("\"")
						string = linha[i:fim_string]
						i = fim_string
						for s in string:
							if not self.e_simbolo(s):
								flag = True
								sys.stderr.write("Erro lexico: string invalida, linha:%s col:%s\n" % (str(n_linha), str(i)))
								break
						if not flag:
							id += 1
							self.tab_simbs.append(["str"+str(id), string, "string"])
							self.tokens.append("str"+str(id)+"_"+string+"´"+str(n_linha)+"|"+str(i))						
				#verificando numeros
				elif self.e_digito(caracter_atual):
					num = caracter_atual
					i += 1
					# percorre o caracter se for digito e se nao for final de linha
					while i < tam_linha:
						caracter_atual = linha[i]
						if self.e_digito(caracter_atual):
							num += linha[i] # agrupa os digitos
						else:
							i -= 1
							break
						i += 1

					# deteccao de float
					if linha[i] == ".": # codigo n entra aq
						sys.stderr.write("Erro lexico: float nao e permitido, linha:%s col:%s\n" % (str(n_linha), str(i)))
						sys.exit(1)	
					else:
						id += 1
						self.tab_simbs.append(["num"+str(id), num, "int"])
						self.tokens.append("num"+str(id)+"_"+num+"´"+str(n_linha)+"|"+str(i))
				# verificando identificadores e reservadas
				elif self.e_letra(caracter_atual):
					erro = False
					ident = caracter_atual
					i += 1
					while i < tam_linha:
						caracter_atual = linha[i]

						if self.e_letra(caracter_atual) or self.e_digito(caracter_atual):
							ident += caracter_atual
						elif self.e_separador(caracter_atual) or caracter_atual == " " or caracter_atual == "\t":
							i -= 1
							break
						elif self.e_operador(caracter_atual):
							i -= 1
							break
						elif caracter_atual != "\n":
							sys.stderr.write("Erro lexico: identificador invalido, linha:%s col:%s\n" % (str(n_linha), str(i)))
							erro = True
						i += 1

					if erro:
						pass 
					else:
						if self.e_reservada(ident):
							self.tokens.append(ident+"´"+str(n_linha)+"|"+str(i))
						else:
							id += 1
							self.tab_simbs.append(["id"+str(id), ident, "tipo"])
							self.tokens.append("id"+str(id)+"_"+ident+"´"+str(n_linha)+"|"+str(i))
				elif caracter_atual != "\n" and caracter_atual != " " and caracter_atual != "\t":
					sys.stderr.write("Erro lexico: tamanho ou caracter invalido, linha:%s col:%s\n" % (str(n_linha), str(i)))
					sys.exit(1)	

				# incrementa leitura de caracter
				i += 1

			linha = arquivo.readline()
			n_linha += 1