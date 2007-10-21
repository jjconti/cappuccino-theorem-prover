# Yacc
# de http://es.wikipedia.org/wiki/L%C3%B3gica_proposicional

import ply.yacc as yacc
from classes import *

# Get the token map from the lexer.  This is required.
from lex import tokens

def p_sentence0(p):
    'sentence : NOT sentence'
    p[0] = Sentence(no=True, sentence=p[2]) 

def p_sentence1(p):
    'sentence : quant scope'
    p[0] = Sentence(quant=p[1], scope=p[2]) 

def p_sentence2(p):
    'sentence : predicate'
    p[0] = Sentence(predicate=p[1])

def p_sentence3(p):
    'sentence : LPAREN sentence connector sentence RPAREN'
    p[0] = Sentence(sentence=p[2], connector=p[3], csentence=p[4])

def p_scope(p):
    'scope : LBRAC sentence RBRAC'
    p[0] = Scope(p[2])

def p_predicate(p):
    'predicate : PROPERTY LPAREN terms RPAREN'
    p[0] = Predicate(p[1], p[3])

def p_terms1(p):
    'terms : term COMMA terms'
    p[0] = [p[1]] + p[3]

def p_terms2(p):
    'terms : term'
    p[0] = [p[1]]

def p_term1(p):
    'term : VAR'
    p[0] = p[1]

def p_term2(p):  
    'term : CONST'
    p[0] = p[1]

def p_quant1(p):
    'quant : LPAREN ALL VAR RPAREN'
    p[0] = Quant(p[2], p[3])

def p_quant2(p):
    'quant : LPAREN EXIST VAR RPAREN'
    p[0] = Quant(p[2], p[3])

def p_connectors1(p):
    'connector : AND'
    p[0] = p[1]

def p_connectors2(p):
    'connector : OR'
    p[0] = p[1]

def p_connectors3(p):
    'connector : IMP'
    p[0] = p[1]

def p_connectors4(p):
    'connector : BIMP'
    p[0] = p[1]

def p_connectors5(p):
    'connector : XOR'
    p[0] = p[1]

# Error rule for syntax errors
def p_error(p):
    print "Syntax error in input!"

# Build the parser
yacc.yacc()
