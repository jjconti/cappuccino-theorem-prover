from yacc import yacc

# Use this if you want to build the parser using SLR instead of LALR
# yacc.yacc(method="SLR")

if __name__ == '__main__':

    import sys
    
    if len(sys.argv) == 3:
        kb = KnowledgeBase()
        prem = open(sys.argv[1]).readlines()
        for p in prem:
            kb.add_knowledge(yacc.parse(p))
        goals = open(sys.argv[2]).readlines()
        for p in goals:
            kb.add_goal(yacc.parse(p))

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
