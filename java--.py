#!/usr/bin/env python3

#from lexico import *
from sintatico import *

nome_arquivo = sys.argv[1]
arquivo = open(nome_arquivo, "r")

#lex = AnalisadorLexico()
#lex.analisador(arquivo)
#print(*lex.tokens, sep = "\n")
#print (np.matrix(lex.tab_simbs))

sintax = AnalisadorSintatico()
sintax.analisador(arquivo)
sintax.compilation_unit()
print(*sintax.tokens, sep = "\n")
print(np.matrix(sintax.tab_simbs))
print(sintax.linha)
print(sintax.coluna)