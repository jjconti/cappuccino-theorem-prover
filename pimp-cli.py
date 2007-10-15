from yacc import yacc

# Use this if you want to build the parser using SLR instead of LALR
# yacc.yacc(method="SLR")

if __name__ == '__main__':

    import sys
    from classes import *

    if len(sys.argv) == 3:
        kb = KnowledgeBase()
        prem = open(sys.argv[1]).readlines()
        for n,p in enumerate(prem):
            s = yacc.parse(p)
            if s:
                kb.add_knowledge(s)
            else:
                print "Error en la linea %d de %s" % (n, sys.argv[1])
        goals = open(sys.argv[2]).readlines()
        for n,g in enumerate(goals):
            s = yacc.parse(g)
            if s:
                kb.add_goal(s)
            else:
                print "Error en la linea %d de %s" % (n, sys.argv[2])
        kb.search()

    else:

        while 1:
           try:
               s = raw_input('logic> ')
           except EOFError:
               print "See you soon.."
               break
           if not s: continue
           result = yacc.parse(s)
           print result
