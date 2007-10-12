# -*- coding: utf-8 -*-
from copy import deepcopy

# Classes for representing the sentences structure.

class Sentence(object):
    def __init__(self, no, cuant=None, scope=None, expression=None, sentence=None):
        self.no = no
        self.cuant = cuant
        self.scope = scope
        self.expression = expression
        self.sentence = sentence

    def __str__(self):
        if self.cuant:
            if self.no:
                no = "not "
            else:
                no = ""
            return no + "%s %s" % (str(self.cuant), str(self.scope))
        else:
            return str(self.expression)

    def comparar(self, other): #solucion temporal
        return self.__str__() == other.__str__()
            

    def prenexion1(self):
        s = deepcopy(self)
        s.no = False
        s.scope.no()
        s.cuant.change()
        return s

    def prenexion2(self):
        s = deepcopy(self)
        s.no = False
        s.scope.no()
        s.cuant.change()
        return s

class Cuant(object):
    def __init__(self, cuant, var):
        self.cuant = cuant
        self.var = var

    def __str__(self):
        return "(%s %s)" % (self.cuant, self.var)

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
    def __init__(self, expression):
        self.expression = expression

    def __str__(self):
        return "[%s]" % (str(self.expression),)

    def no(self):
        self.expression.no = True

class Expression(object):
    def __init__(self, no, predicate=None, connector=None, expression=None):
        self.no = no
        self.predicate = predicate
        self.connector = connector
        self.expression = expression
        self.simple = connector is None and predicate is not None

    def __str__(self):
        if self.simple:
            return str(self.predicate)
        else:
            if self.no:
                no = "not "
            else:
                no = ""
            if not self.predicate:
                return no + str(self.expression)
            elif not self.connector:
                return no + str(self.predicate)
            else:
                return no + "%s %s %s" % (str(self.predicate), str(self.connector), \
str(self.expression))

class Predicate(object):
    def __init__(self, property, args):
        '''args is a list of constants or variables'''
        self.property = property
        self.args = args

    def __str__(self):
        return "%s(%s)" % (self.property, ", ".join(self.args))

# KnowledgeBase 

class KnowledgeBase(object):
    def __init__(self):
        self.knowledge = []
        self.goals = []

    def add_knowledge(self, sentence):
        self.knowledge.append(sentence)

    def add_goal(self, sentence):
        self.goals.append(sentence)
    
    def search(self):
        prem = self.can_prenexion1()
        for p in self.prenexion1(prem):
            self.add_knowledge(p)
        for k in self.knowledge:
            if k.comparar(self.goals[0]):
                print "LLEGAMOS!"
        print "Knowledge"
        for p in self.knowledge:
            print p
        print "Goals"
        for p in self.goals:
            print p

    def can_prenexion1(self):
        return [p for p in self.knowledge if p.no and p.cuant.all()]

    def do_prenexion1(self, knowledge):
        '''Prenexión 1'''
        return [p.prenexion1() for p in knowledge]  
      
    def can_prenexion2(self):
        return [p for p in self.knowledge if p.no and p.cuant.exist()]

    def do_prenexion2(self, knowledge):
        '''Prenexión 2'''
        [p.prenexion2() for p in knowledge]        
        

