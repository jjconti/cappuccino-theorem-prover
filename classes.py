# -*- coding: utf-8 -*-
from copy import copy, deepcopy

DEBUG = False
MAX = 7

# Classes for representing the sentences structure.

class Sentence(object):
    def __init__(self, no=False, quant=None, scope=None, predicate=None, \
                 sentence=None, connector=None, csentence=None):
        self.no = no
        self.quant = quant
        self.scope = scope
        self.predicate = predicate
        self.sentence = sentence
        self.connector = connector
        self.csentence = csentence
        #self.atomic = not self.connector
        self.source = "Premise"
        self.from_sentence = None

    def __str__(self):
        if self.quant and self.scope:
            return "%s%s" % (self.quant, self.scope)
        elif self.predicate:
            return str(self.predicate)
        elif self.connector:
            return "(%s %s %s)" % (self.sentence, self.connector, self.csentence)
        else:
            if self.no:
                return "not %s" % self.sentence
            else:
                return str(self.sentence)

    def __eq__(self, other):
        if other == None: return False
        return self.no == other.no and self.quant == other.quant and \
        self.scope == other.scope and self.predicate == other.predicate and \
        self.sentence == other.sentence and self.connector == other.connector \
        and self.csentence == other.csentence

    def negate(self):
        '''Returns a new sentence, negated.
        P(x) becames not P(x), but not (x) becames P(x).'''
        if self.no:
            return self.sentence
        else:
            s = Sentence(sentence=deepcopy(self))
            s.no = True
            return s
            
    def prenexion1(self):
        s = deepcopy(self)
        s.no = False
        s.sentence.scope.no()
        s.sentence.quant.change()
        s.sentence.source = "Prenexión 1"
        return [s.sentence]

    def prenexion2(self):
        s = deepcopy(self)
        s.no = False
        s.sentence.scope.no()
        s.sentence.quant.change()
        s.sentence.source = "Prenexión 2"
        return [s.sentence]

    def prenexion3(self):
        s = deepcopy(self)
        s.quant = s.sentence.quant
        s.scope = s.sentence.scope
        s.scope.add(s.connector, s.csentence)
        s.sentence = None
        s.connector = None
        s.csentence = None
        s.source = "Prenexión 3"
        return [s]

    def can_prenexion4(self):
        return self.connector in ('and', 'AND',) \
               and self.sentence.quant \
               and self.sentence.quant.all()

    def prenexion4(self):
        s = deepcopy(self)
        s.quant = s.sentence.quant
        s.scope = s.sentence.scope
        s.scope.add(s.connector, s.csentence)
        s.sentence = None
        s.connector = None
        s.csentence = None
        s.source = "Prenexión 4"
        return [s]

    def prenexion5(self):
        s = deepcopy(self)
        s.quant = s.sentence.quant
        s.scope = s.sentence.scope
        s.scope.add(s.connector, s.csentence)
        s.sentence = None
        s.connector = None
        s.csentence = None
        s.source = "Prenexión 5"
        return [s]

    def can_prenexion6(self):
        if self.connector in ('and', 'AND',):
            if self.sentence.quant:
                return self.sentence.quant.exist()
        return False

    def prenexion6(self):
        s = deepcopy(self)
        s.quant = s.sentence.quant
        s.scope = s.sentence.scope
        s.scope.add(s.connector, s.csentence)
        s.sentence = None
        s.connector = None
        s.csentence = None
        s.source = "Prenexión 6"
        return [s]

    def can_prenexion7(self):
        if self.connector in ('->',):
            if self.csentence.quant:
                return self.csentence.quant.all()
        return False

    def prenexion7(self):
        s = deepcopy(self)
        s.quant = s.csentence.quant
        s.scope = Scope(Sentence(sentence=s.sentence, connector=s.connector, \
                  csentence=s.csentence.scope.sentence))
        s.sentence = None
        s.connector = None
        s.csentence = None
        s.source = "Prenexión 7"
        return [s]

    def can_prenexion8(self):
        if self.connector in ('->',):
            if self.csentence.quant:
                return self.csentence.quant.exist()
        return False

    def prenexion8(self):
        s = deepcopy(self)
        s.quant = s.csentence.quant
        s.scope = Scope(Sentence(sentence=s.sentence, connector=s.connector, \
                  csentence=s.csentence.scope.sentence))
        s.sentence = None
        s.connector = None
        s.csentence = None
        s.source = "Prenexión 8"
        return [s]

    def can_modus_ponens(self, p2):
        return self.connector in ('->',) and self.sentence == p2

    def modus_ponens(self):
        s = deepcopy(self.csentence)
        s.source = "Modus Ponens"
        return [s]

    def can_modus_tollens(self, p2):
        return self.connector in ('->',) and self.csentence.negate() == p2

    def modus_tollens(self):
        s = self.sentence.negate()
        s.source = "Modus Tollens"
        return [s]   

    #HS: Hypothetic Syllogism
    def can_hs(self, p2):
        return self.connector in ('->',) and p2.connector in ('->',) and \
               self.csentence == p2.sentence

    def hs(self):
        s = Sentence(sentence=self.sentence, connector='->', csentnce=p2.csentence)
        s.source = "Hypothetic Syllogism"
        return [s]  
    
    #UG: Universal Generalization
    def can_ug(self):
        return True

    def ug(self):
        var = self.get_any_var()
        s = Sentence(quant=Quant('A', var), scope=Scope(deepcopy(self)))
        s.source = "Universal Generalization"
        return [s]

    def get_any_var(self):
        '''Returns the first variable found'''
        if self.predicate:
            return self.predicate.terms[0]
        elif self.scope:
            return self.scope.sentence.get_any_var()
        else: return self.sentence.get_any_var()

    #CE: Conjunction Elimination
    def can_ce(self):
        return self.connector == 'and'

    def ce(self):
        s1 = deepcopy(self.sentence)
        s1.source = "Conjuntion elimination"
        s2 = deepcopy(self.csentence)
        s2.source = "Conjuntion elimination"
        return [s1, s2]

class Quant(object):
    def __init__(self, quant, var):
        self.quant = quant
        self.var = var

    def __str__(self):
        return "(%s %s)" % (self.quant, self.var)

    def __eq__(self, other):
        if other == None: return False
        return self.quant == other.quant and self.var == other.var

    def all(self):
        return self.quant == 'A'

    def exist(self):
        return self.quant == 'E'

    def change(self):
        if self.quant == 'A':
            self.quant = 'E'
        elif self.quant == 'E':
            self.quant = 'A'


class Scope(object):
    def __init__(self, sentence):
        self.sentence = sentence

    def __str__(self):
        return "[%s]" % (self.sentence,)

    def __eq__(self, other):
        if other == None: return False
        return self.sentence == other.sentence

    def no(self):
        self.sentence = Sentence(no=True, sentence=self.sentence)

    def add(self, connector, sentence):
        self.sentence = Sentence(sentence=self.sentence, connector=connector, \
                                 csentence=sentence)


class Predicate(object):
    def __init__(self, property, terms):
        '''terms is a list of constants or variables'''
        self.property = property
        self.terms = terms

    def __str__(self):
        return "%s(%s)" % (self.property, ",".join(self.terms))

    def __eq__(self, other):
        if other == None: return False
        return self.property == other.property and self.terms == self.terms

# KnowledgeBase 

class KnowledgeBase(object):
    '''The KB has the actual knowledge and the goals. Is also is a node \
    in a search tree. The node has no son until the search method is called.'''

    def __init__(self):
        self.father = None
        self.level = 0
        self.nson = 0
        self.sons = []
        self.knowledge = []
        self.goals = []
        self.solutions = [] #same list for all the nodes

    def __eq__(self, kb):
        return self.solutions.__eq__(kb.solutions)

    def add_knowledge(self, s):
        if type(s) == type([]):
            self.knowledge += s
        else:
            self.knowledge.append(s)

    def add_goal(self, sentence):
        self.goals.append(sentence)

    def meta_proof(self):
        #return set(self.goals).issubset(set(self.knowledge))
        for g in self.goals:
            if g not in self.knowledge:
                return False
        return True

    def search(self):
        print "Solución más corta:"
        self.__search()
        min_sol = min(self.solutions)
        min_sol.print_solution()
    
    def __search(self):

        if self.meta_proof():
            if self not in self.solutions:
                self.solutions.append(self)

        elif self.level >= MAX:
            if DEBUG: print "Maximo nivel de profundidad alcanzado: %s" % (MAX,)
        else:
            can  = [m for m in dir(self) if m.startswith('can_')]
            prem_lists = [getattr(self, c)() for c in can] #some lists can be []
            do = ['do_'+d[4:] for d in can]
            # Pairs operator,list of sentences that can be operated
            do_prems = [dp for dp in zip(do, prem_lists) if dp[1] != []]
            if DEBUG: print "Se crearan %s nodos. Nivel: %s" % \
                      (len(do_prems), self.level)
            
            # Create sons (or doughters :)
            nson = 1
            for d,p in do_prems:
                for i in p:
                    new = copy(self)
                    new.knowledge = copy(self.knowledge)
                    new.father = self
                    new.level = self.level + 1
                    new.nson = nson
                    nson += 1
                    new.sons = []
                    sl = getattr(self,d)(i)
                    for s in sl:
                        if s not in self.knowledge:
                            if DEBUG: print getattr(self, d).__doc__
                            s.from_sentence = i #WARN: heavy copies?
                            new.add_knowledge(s)
                            self.sons.append(new)
                
            # Profundidad acotada
            for s in self.sons:
                s.__search()

    def print_solution(self):
        print "SOLUCION: nodo %d del nivel %d" % (self.nson, self.level)
        for n,k in enumerate(self.knowledge):
            k.index = n + 1
            if k.from_sentence:
                print "%d) %s - %s on %s" % (n + 1, k, k.source, k.from_sentence.index)
            else:
                print "%d) %s - %s" % (n + 1, k, k.source)

    def can_prenexion1(self):
        return [p for p in self.knowledge if p.no and p.sentence.quant.all()]

    def do_prenexion1(self, p):
        '''Prenexión 1'''
        return p.prenexion1()
      
    def can_prenexion2(self):
        return [p for p in self.knowledge if p.no and p.sentence.quant.exist()]

    def do_prenexion2(self, p):
        '''Prenexión 2'''
        return p.prenexion2()

    def can_prenexion3(self):
        return [p for p in self.knowledge if p.connector \
               in ('vel', 'VEL', 'or', 'OR',) and p.sentence.quant.all()]  
        
    def do_prenexion3(self, p):
        '''Prenexion 3'''
        return p.prenexion3()

    def can_prenexion4(self):
        return [p for p in self.knowledge if p.can_prenexion4()]  
        
    def do_prenexion4(self, p):
        '''Prenexion 4'''
        return p.prenexion4()

    def can_prenexion5(self):
        return [p for p in self.knowledge if p.connector \
               in ('vel', 'VEL', 'or', 'OR',) and p.sentence.quant.exist()]  
        
    def do_prenexion5(self, p):
        '''Prenexion 5'''
        return p.prenexion5()

    def can_prenexion6(self):
        return [p for p in self.knowledge if p.can_prenexion6()]  
        
    def do_prenexion6(self, p):
        '''Prenexion 6'''
        return p.prenexion6()

    def can_prenexion7(self):
        return [p for p in self.knowledge if p.can_prenexion7()]  
        
    def do_prenexion7(self, p):
        '''Prenexion 7'''
        return p.prenexion7()

    def can_prenexion8(self):
        return [p for p in self.knowledge if p.can_prenexion8()]  
        
    def do_prenexion8(self, p):
        '''Prenexion 8'''
        return p.prenexion8()

    def can_modus_ponens(self):
        return [p1 for p1 in self.knowledge for p2 in self.knowledge \
               if p1.can_modus_ponens(p2)]  
        
    def do_modus_ponens(self, p):
        '''Modus ponens'''
        return p.modus_ponens()

    def can_modus_tollens(self):
        return [p1 for p1 in self.knowledge for p2 in self.knowledge \
               if p1.can_modus_tollens(p2)]  
        
    def do_modus_tollens(self, p):
        '''Modus tollens'''
        return p.modus_tollens()

    def can_hs(self):
        return [p1 for p1 in self.knowledge for p2 in self.knowledge \
               if p1.can_hs(p2)]  
        
    def do_hs(self, p):
        '''Modus tollens'''
        return p.hs()

    def can_ug(self):
        return [p for p in self.knowledge if p.can_ug()]  
        
    def do_ug(self, p):
        '''Universal Generalization'''
        return p.ug()

    def can_ce(self):
        return [p for p in self.knowledge if p.can_ce()]

    def do_ce(self, p):
        '''Conjuntion elimination'''
        return p.ce()
