#------------------------------------------------------------
# lex.py
#
# tokenizer
# ------------------------------------------------------------

import ply.lex as lex

# List of token names.   This is always required
tokens = ('AND', 'OR', 'NOT', 'IMP', 'BIMP', 'XOR', 'VAR', 'CONST',
'PROPERTY', 'LPAREN', 'RPAREN', 'LBRAC', 'RBRAC', 'ALL', 'EXIST', 'COMMA')

# Reserved words
reserved = {
    'and' : 'AND',
    'AND' : 'AND',
    'vel' : 'OR',
    'VEL' : 'OR',
    'or' : 'OR',
    'OR' : 'OR',
    'aut' : 'XOR',
    'AUT' : 'XOR',
    'xor' : 'XOR',
    'XOR' : 'XOR',
    'not' : 'NOT',
    'NOT' : 'NOT',
    'E' : 'EXIST',
    'A' : 'ALL'    
}

# Regular expression rules for simple tokens
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRAC = r'\['
t_RBRAC = r'\]'
t_COMMA = r','
t_IMP  = r'->'
t_BIMP  = r'<->'

def t_VAR(t):
    r'[a-z]+'
    t.type = reserved.get(t.value,'VAR')    # Check for reserved words
    return t

def t_CONST(t):
    r'[A-B]+'
    t.type = reserved.get(t.value,'CONST')    # Check for reserved words
    return t

def t_PROPERTY(t):
    r'[A-Z][a-zA-Z0-9_\-]*'
    t.type = reserved.get(t.value,'PROPERTY')    # Check for reserved words
    return t

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

# To discard a token, such as a comment, simply define a token 
# rule that returns no value.


# Also C or C++ comments 
def t_CCOMMENT(t):
    r'(/\*(.|\n)*\*/)|(//.*)'
    pass

# Error handling rule
def t_error(t):
    print "Illegal character '%s'" % t.value[0]
    t.lexer.skip(1)

# Build the lexer
lex.lex()

if __name__ == '__main__':
    import sys
    if len(sys.argv) == 2:
        if sys.argv[1] == '--test':
            test()
        else:
            try:
                data = open(sys.argv[1]).read()
            except:
                data = ""
                print "No existe el archivo %s." % sys.argv[1]
            lex.input(data)
            # Tokenize
            while 1:
                tok = lex.token()
                if not tok: break      # No more input
                print tok
    elif len(sys.argv) == 1:
        lex.runmain()
    else:
        print "Uso: lex.py [--test|filename]"


    # Tokenize
    while 1:
        tok = lex.token()
        if not tok: break      # No more input
        print tok

