# -*- coding: utf-8 -*-
from copy import deepcopy

DEBUG = True

# Classes for representing the sentences structure.

class Sentence(object):
    def __init__(self, no=False, cuant=None, scope=None, predicate=None, \
                 sentence=None, connector=None, csentence=None):
        self.no = no
        self.cuant = cuant
        self.scope = scope
        self.predicate = predicate
        self.sentence = sentence
        self.connector = connector
        self.csentence = csentence
        #self.atomic = not self.connector
        self.source = "Premisa"

    def __str__(self):
        if self.cuant and self.scope:
            return "%s%s" % (str(self.cuant), str(self.scope))
        elif self.predicate:
            return str(self.predicate)
        elif self.connector:
            return "(%s %s %s)" % (str(self.sentence), self.connector, str(self.csentence))
        else:
            if self.no:
                return "not (%s)" % str(self.sentence)
            else:
                return str(self.sentence)

    def __eq__(self, other):
        if other == None: return False
        return self.no == other.no and self.cuant == other.cuant and \
        self.scope == other.scope and self.predicate == other.predicate and \
        self.sentence == other.sentence and self.connector == other.connector \
        and self.csentence == other.csentence

    #def comparar(self, other): #solucion temporal
    #    return self.__str__() == other.__str__()
            

    def prenexion1(self):
        s = deepcopy(self)
        s.no = False
        s.sentence.scope.no()
        s.sentence.cuant.change()
        s.sentence.source = "Prenexión 1"
        return s.sentence

    def prenexion2(self):
        s = deepcopy(self)
        s.no = False
        s.sentence.scope.no()
        s.sentence.cuant.change()
        s.sentence.source = "Prenexión 2"
        return s.sentence

    def prenexion3(self):
        s = deepcopy(self)
        s.cuant = s.sentence.cuant
        s.scope = s.sentence.scope
        s.scope.add(s.connector, s.csentence)
        s.sentence = None
        s.connector = None
        s.csentence = None
        s.source = "Prenexión 3"
        return s

    def prenexion4(self):
        s = deepcopy(self)
        s.cuant = s.sentence.cuant
        s.scope = s.sentence.scope
        s.scope.add(s.connector, s.csentence)
        s.sentence = None
        s.connector = None
        s.csentence = None
        s.source = "Prenexión 4"
        return s

class Cuant(object):
    def __init__(self, cuant, var):
        self.cuant = cuant
        self.var = var

    def __str__(self):
        return "(%s %s)" % (self.cuant, self.var)

    def __eq__(self, other):
        if other == None: return False
        return self.cuant == other.cuant and self.var == other.var

    def all(self):
        return self.cuant == 'A'

    def exist(self):
        return self.cuant == 'E'

    def change(self):
        if self.cuant == 'A':
            self.cuant = 'E'
        elif self.cuant == 'E':
            self.cuant = 'A'


class Scope(object):
    def __init__(self, sentence):
        self.sentence = sentence

    def __str__(self):
        return "[%s]" % (str(self.sentence),)

    def __eq__(self, other):
        if other == None: return False
        return self.sentence == other.sentence

    def no(self):
        self.sentence = Sentence(no=True, sentence=self.sentence)

    def add(self, connector, sentence):
        self.sentence = Sentence(sentence=self.sentence, connector=connector, \
                                 csentence=sentence)

#class Expression(object):
#    def __init__(self, no, predicate=None, connector=None, expression=None):
#        self.no = no
#        self.predicate = predicate
#        self.connector = connector
#        self.expression = expression
#        self.simple = connector is None and predicate is not None
#
#    def __str__(self):
#        if self.simple:
#            return str(self.predicate)
#        else:
#            if self.no:
#                no = "not "
#            else:
#                no = ""
#            if not self.predicate:
#                return no + "(" + str(self.expression) + ")"
#            elif not self.connector:
#                return no + str(self.predicate)
#            else:
#                return no + "%s %s %s" % (str(self.predicate), \
#                str(self.connector), str(self.expression))
#
#    def __eq__(self, other):
#        if other == None: return False
#        return self.no == other.no and self.predicate == other.predicate and \
#        self.connector == other.connector and \
#        self.expression == other.expression 

class Predicate(object):
    def __init__(self, property, args):
        '''args is a list of constants or variables'''
        self.property = property
        self.args = args

    def __str__(self):
        return "%s(%s)" % (self.property, ",".join(self.args))

    def __eq__(self, other):
        if other == None: return False
        return self.property == other.property and self.args == self.args

# KnowledgeBase 

class KnowledgeBase(object):
    '''The KB has the actual knowledge and the goals. Is also is a node \
    in a search tree. The node has no son until the search method is called.'''

    def __init__(self):
        self.father = None
        self.level = 0
        self.sons = []
        self.knowledge = []
        self.goals = []

    def add_knowledge(self, s):
        if type(s) == type([]):
            self.knowledge += s
        else:
            self.knowledge.append(s)

    def add_goal(self, sentence):
        self.goals.append(sentence)

    def meta_proof(self):
        print "Prueba de meta"
        print "Goals"
        for p in self.goals:
            print p
        print "Prems"
        for p in self.knowledge:
            print p
        #return set(self.goals).issubset(set(self.knowledge))
        for g in self.goals:
            if g not in self.knowledge:
                print "No se cumplio la prueba"                    
                return False
        return True
    
    def search(self):

        if self.meta_proof():
            self.print_solution()
        else:
            can  = [m for m in dir(self) if m.startswith('can_')]
            prem_lists = [getattr(self, c)() for c in can] #some lists can be []
            do = ['do_'+d[4:] for d in can]
            # Pairs operator,list of sentences that can be operated
            do_prems = [dp for dp in zip(do, prem_lists) if dp[1] != []]
            
            # Create sons (or doughters :)
            print do_prems
            for d,p in do_prems:
                for i in p:
                    new = deepcopy(self)
                    new.father = self
                    new.level = self.level + 1
                    print "new nodo, nivel:", new.level
                    new.sons = []
                    s = getattr(self,d)(i)
                    if s not in self.knowledge:
                        new.add_knowledge(s)
                        self.sons.append(new)

            # Pick a son. It depends of the search method used.
            
            # Amplitud
            raw_input()
            if self.sons:
                son = self.sons.pop(0)
                print "Llamada recursiva"
                son.search()

            print "Final del metodo search"

    def print_solution(self):
        print "SOLUCION:"
        for n,k in enumerate(self.knowledge):
            print "%d) %s - %s" % (n + 1, k, k.source)

    def can_prenexion1(self):
        print self.knowledge
        return [p for p in self.knowledge if p.no and p.sentence.cuant.all()]

    def do_prenexion1(self, p):
        '''Prenexión 1'''
        return p.prenexion1()
      
    def can_prenexion2(self):
        return [p for p in self.knowledge if p.no and p.sentence.cuant.exist()]

    def do_prenexion2(self, p):
        '''Prenexión 2'''
        return p.prenexion2()

    def can_prenexion3(self):
        return [p for p in self.knowledge if p.connector in ('vel', 'VEL', 'or', 'OR')]  
        
    def do_prenexion3(self, p):
        '''Prenexion 3'''
        return p.prenexion3()

    def can_prenexion4(self):
        return [p for p in self.knowledge if p.connector in ('and', 'AND')]  
        
    def do_prenexion4(self, p):
        '''Prenexion 3'''
        return p.prenexion4()
