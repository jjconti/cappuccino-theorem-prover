# Yacc
# de http://es.wikipedia.org/wiki/L%C3%B3gica_proposicional

import ply.yacc as yacc
from classes import *

# Get the token map from the lexer.  This is required.
from lex import tokens

#def p_sentence_not(p):
#    'sentence : NOT sentence'
#    p[0] = Sentence(True, sentence=p[2])

def p_sentence0(p):
    'sentence : NOT cuant scope'
    p[0] = Sentence(True, cuant=p[2], scope=p[3]) 

def p_sentence1(p):
    'sentence : cuant scope'
    p[0] = Sentence(False, cuant=p[1], scope=p[2]) 

def p_sentence2(p):
    'sentence : expression'
    p[0] = Sentence(False, expression=p[1])

def p_scope(p):
    'scope : LBRAC expression RBRAC'
    p[0] = Scope(p[2])

def p_expression0(p):
    'expression : NOT expression'
    p[0] = Expression(True, expression=p[2])

def p_expression_paren(p):
    'expression : LPAREN expression RPAREN'
    p[0] = Expression(False, expression=p[2])

def p_expression1(p):
    'expression : predicate connector expression'
    p[0] = Expression(False, predicate=p[1], connector=p[2], expression=p[3])

def p_expression2(p):
    'expression : predicate'
    p[0] = Expression(False, predicate=p[1])

def p_predicate(p):
    'predicate : PROPERTY LPAREN args RPAREN'
    p[0] = Predicate(p[1], p[3])

def p_args1(p):
    'args : arg COMMA args'
    p[0] = [p[1]] + p[3]

def p_args2(p):
    'args : arg'
    p[0] = [p[1]]

def p_arg1(p):
    'arg : VAR'
    p[0] = p[1]

def p_arg2(p):  
    'arg : CONST'
    p[0] = p[1]

def p_cuant1(p):
    'cuant : LPAREN ALL VAR RPAREN'
    p[0] = Cuant(p[2], p[3])

def p_cuant2(p):
    'cuant : LPAREN EXIST VAR RPAREN'
    p[0] = Cuant(p[2], p[3])

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

# Error rule for syntax errors
def p_error(p):
    print "Syntax error in input!"

# Build the parser
yacc.yacc()
