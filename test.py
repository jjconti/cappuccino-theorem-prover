import unittest

class TestStr(unittest.TestCase):
    '''Test string representation for the Sentence class'''

    def setUp(self):
        from yacc import yacc
        self.yacc = yacc

    def test1(self):
        s = "(P(x) -> G(x))"
        r = self.yacc.parse(s)
        self.assertEquals(s, str(r))

    def test2(self):
        s = "(A x)[(P(x) -> G(x))]"
        r = self.yacc.parse(s)
        self.assertEquals(s, str(r))

    def test3(self):
        s = "not (A x)[(P(x) -> G(x))]"
        r = self.yacc.parse(s)
        self.assertEquals(s, str(r))

    def test4(self):
        s = "(E x)[(P(x) -> G(x))]"
        r = self.yacc.parse(s)
        self.assertEquals(s, str(r))

    def test5(self):
        s = "not (E x)[(P(x) -> G(x))]"
        r = self.yacc.parse(s)
        self.assertEquals(s, str(r))

    def test6(self):
        s = "not (P(x) -> G(x))"
        r = self.yacc.parse(s)
        self.assertEquals(s,str(r))

    def test7(self):
        s = "(not (A x)[(P(x) -> G(x))] or not (E x)[G(x)])"
        r = self.yacc.parse(s)
        self.assertEquals(s,str(r))

    def test8(self):
        s = "Perro(x)"
        r = self.yacc.parse(s)
        self.assertEquals(s,str(r))

    def test9(self):
        s = "Hijo-de(x,y)"
        r = self.yacc.parse(s)
        self.assertEquals(s,str(r))

    def test10(self):
        s = "Hermanos(x,y,z)"
        r = self.yacc.parse(s)
        self.assertEquals(s,str(r))
    
class TestEq(unittest.TestCase):
    '''Test __eq__ operationsfor the Sentence family classes'''

    def setUp(self):
        from yacc import yacc
        self.yacc = yacc

    def test1(self):
        s = "(P(x) -> G(x))"
        r = self.yacc.parse(s)
        self.assertTrue(r == r)

    def test2(self):
        s = "(A x)[(P(x) -> G(x))]"
        r = self.yacc.parse(s)
        self.assertTrue(r == r)

    def test3(self):
        s = "not (A x)[(P(x) -> G(x))]"
        r = self.yacc.parse(s)
        self.assertTrue(r == r)

    def test4(self):
        s = "(E x)[(P(x) -> G(x))]"
        r = self.yacc.parse(s)
        self.assertTrue(r == r)

    def test5(self):
        s = "not (E x)[(P(x) -> G(x))]"
        r = self.yacc.parse(s)
        self.assertTrue(r == r)

    def test6(self):
        s = "not (P(x) -> G(x))"
        r = self.yacc.parse(s)
        self.assertTrue(r == r)

    def test7(self):
        s = "(not (A x)[(P(x) -> G(x))] or not (E x)[G(x)])"
        r = self.yacc.parse(s)
        self.assertTrue(r == r)

    def test8(self):
        s = "Perro(x)"
        r = self.yacc.parse(s)
        self.assertTrue(r == r)

    def test9(self):
        s = "Hijo-de(x,y)"
        r = self.yacc.parse(s)
        self.assertTrue(r == r)

    def test10(self):
        s = "Hermanos(x,y,z)"
        r = self.yacc.parse(s)
        self.assertTrue(r == r)

    def test11(self):
        s1 = "Hermanos(x,y,z)"
        s2 = "Hermanos(x, y, z)"
        r1 = self.yacc.parse(s1)
        r2 = self.yacc.parse(s2)
        self.assertTrue(r1 == r2)

class TestNoSentence(unittest.TestCase):
    '''Test the no method in Sentence.'''

    def setUp(self):
        from yacc import yacc
        self.yacc = yacc

    def test1(self):
        '''no 1'''
        s1 = "P(x)"
        r1 = self.yacc.parse(s1)
        s2 = "not P(x)"
        r2 = self.yacc.parse(s2)
        self.assertEquals(r1.negate(), r2)

    def test2(self):
        '''no 2'''
        s1 = "P(x)"
        r1 = self.yacc.parse(s1)
        s2 = "not P(x)"
        r2 = self.yacc.parse(s2)
        self.assertEquals(r1, r2.negate())

class TestPrenexiones(unittest.TestCase):
    '''Test prenexiones'''

    def setUp(self):
        from yacc import yacc
        self.yacc = yacc

    def test1(self):
        '''Prenexion 1'''
        s1 = "not (A x)[(P(x) -> G(x))]"
        r1 = self.yacc.parse(s1)
        s2 = "(E x)[not (P(x) -> G(x))]"
        r2 = self.yacc.parse(s2)
        r3 = r1.prenexion1()[0]
        self.assertEquals(r2, r3)

    def test2(self):
        '''Prenexion 1 simple'''
        s1 = "not (A x)[P(x)]"
        r1 = self.yacc.parse(s1)
        s2 = "(E x)[not P(x)]"
        r2 = self.yacc.parse(s2)
        r3 = r1.prenexion1()[0]
        self.assertEquals(r2, r3)

    def test3(self):
        '''Prenexion 2'''
        s1 = "not (E x)[(P(x) -> G(x))]"
        r1 = self.yacc.parse(s1)
        s2 = "(A x)[not (P(x) -> G(x))]"
        r2 = self.yacc.parse(s2)
        r3 = r1.prenexion2()[0]
        self.assertEquals(r2, r3)

    def test4(self):
        '''Prenexion 2 simple'''
        s1 = "not (E x)[P(x)]"
        r1 = self.yacc.parse(s1)
        s2 = "(A x)[not P(x)]"
        r2 = self.yacc.parse(s2)
        r3 = r1.prenexion2()[0]
        self.assertEquals(r2, r3)

    def test5(self):
        '''Prenexion 3'''
        s1 = "((A x)[(P(x) -> G(x))] or P(x))"
        r1 = self.yacc.parse(s1)
        s2 = "(A x)[((P(x) -> G(x)) or P(x))]"
        r2 = self.yacc.parse(s2)
        r3 = r1.prenexion3()[0]
        self.assertEquals(r2, r3)

    def test6(self):
        '''Prenexion 3 simple'''
        s1 = "((A x)[G(x)] or P(x))"
        r1 = self.yacc.parse(s1)
        s2 = "(A x)[(G(x) or P(x))]"
        r2 = self.yacc.parse(s2)
        r3 = r1.prenexion3()[0]
        self.assertEquals(r2, r3)   

    def test7(self):
        '''Prenexion 4'''
        s1 = "((A x)[(P(x) -> G(x))] and P(x))"
        r1 = self.yacc.parse(s1)
        s2 = "(A x)[((P(x) -> G(x)) and P(x))]"
        r2 = self.yacc.parse(s2)
        r3 = r1.prenexion3()[0]
        self.assertEquals(r2, r3)

    def test8(self):
        '''Prenexion 4 simple'''
        s1 = "((A x)[G(x)] and P(x))"
        r1 = self.yacc.parse(s1)
        s2 = "(A x)[(G(x) and P(x))]"
        r2 = self.yacc.parse(s2)
        r3 = r1.prenexion3()[0]
        self.assertEquals(r2, r3)      

    def test9(self):
        '''Prenexion 5'''
        s1 = "((E x)[(P(x) -> G(x))] or P(x))"
        r1 = self.yacc.parse(s1)
        s2 = "(E x)[((P(x) -> G(x)) or P(x))]"
        r2 = self.yacc.parse(s2)
        r3 = r1.prenexion5()[0]
        self.assertEquals(r2, r3)

    def test10(self):
        '''Prenexion 5 simple'''
        s1 = "((E x)[G(x)] or P(x))"
        r1 = self.yacc.parse(s1)
        s2 = "(E x)[(G(x) or P(x))]"
        r2 = self.yacc.parse(s2)
        r3 = r1.prenexion5()[0]
        self.assertEquals(r2, r3)   

    def test11(self):
        '''Prenexion 6'''
        s1 = "((E x)[(P(x) -> G(x))] and P(x))"
        r1 = self.yacc.parse(s1)
        s2 = "(E x)[((P(x) -> G(x)) and P(x))]"
        r2 = self.yacc.parse(s2)
        r3 = r1.prenexion6()[0]
        self.assertEquals(r2, r3)

    def test12(self):
        '''Prenexion 6 simple'''
        s1 = "((E x)[G(x)] and P(x))"
        r1 = self.yacc.parse(s1)
        s2 = "(E x)[(G(x) and P(x))]"
        r2 = self.yacc.parse(s2)
        r3 = r1.prenexion6()[0]
        self.assertEquals(r2, r3)     

    def test13(self):
        '''Can prenexion 6 1'''
        s1 = "((E x)[G(x)] and P(x))"
        r1 = self.yacc.parse(s1)
        self.assertTrue(r1.can_prenexion6())  

    def test14(self):
        '''Can prenexion 6 2'''
        s1 = "(G(x) and P(x))"
        r1 = self.yacc.parse(s1)
        self.assertFalse(r1.can_prenexion6())       

    def test15(self):
        '''Prenexion 7'''
        s1 = "((E x)[(P(x) -> G(x))] -> (A x)[P(x)])"
        r1 = self.yacc.parse(s1)
        s2 = "(A x)[((E x)[(P(x) -> G(x))] -> P(x))]"
        r2 = self.yacc.parse(s2)
        r3 = r1.prenexion7()[0]
        self.assertEquals(r2, r3)

    def test16(self):
        '''Prenexion 7 simple'''
        s1 = "(G(x) -> (A x)[P(x)])"
        r1 = self.yacc.parse(s1)
        s2 = "(A x)[(G(x) -> P(x))]"
        r2 = self.yacc.parse(s2)
        r3 = r1.prenexion7()[0]
        self.assertEquals(r2, r3)     

    def test17(self):
        '''Can prenexion 7 1'''
        s1 = "((E x)[G(x)] -> (A x)[P(x)])"
        r1 = self.yacc.parse(s1)
        self.assertTrue(r1.can_prenexion7())  

    def test18(self):
        '''Can prenexion 7 2'''
        s1 = "(G(x) -> P(x))"
        r1 = self.yacc.parse(s1)
        self.assertFalse(r1.can_prenexion7()) 

    def test19(self):
        '''Prenexion 8'''
        s1 = "((E x)[(P(x) -> G(x))] -> (E x)[P(x)])"
        r1 = self.yacc.parse(s1)
        s2 = "(E x)[((E x)[(P(x) -> G(x))] -> P(x))]"
        r2 = self.yacc.parse(s2)
        r3 = r1.prenexion8()[0]
        self.assertEquals(r2, r3)

    def test20(self):
        '''Prenexion 8 simple'''
        s1 = "(G(x) -> (E x)[P(x)])"
        r1 = self.yacc.parse(s1)
        s2 = "(E x)[(G(x) -> P(x))]"
        r2 = self.yacc.parse(s2)
        r3 = r1.prenexion8()[0]
        self.assertEquals(r2, r3)     

    def test21(self):
        '''Can prenexion 8 1'''
        s1 = "((E x)[G(x)] -> (E x)[P(x)])"
        r1 = self.yacc.parse(s1)
        self.assertTrue(r1.can_prenexion8())  

    def test22(self):
        '''Can prenexion 8 2'''
        s1 = "(G(x) -> P(x))"
        r1 = self.yacc.parse(s1)
        self.assertFalse(r1.can_prenexion8()) 

class TestModus(unittest.TestCase):
    '''Test modus ponens and tollens'''

    def setUp(self):
        from yacc import yacc
        self.yacc = yacc

    def test1(self):
        '''can mp 1'''
        s1 = "(P(x) -> G(x))"
        s2 = "P(x)"
        r1 = self.yacc.parse(s1)
        r2 = self.yacc.parse(s2)
        self.assertTrue(r1.can_modus_ponens(r2))

    def test2(self):
        '''can mp 2'''
        s1 = "((P(x) or T(x)) -> G(x))"
        s2 = "(P(x) or T(x))"
        r1 = self.yacc.parse(s1)
        r2 = self.yacc.parse(s2)
        self.assertTrue(r1.can_modus_ponens(r2))

    def test3(self):
        '''can mp 3'''
        s1 = "((A x)[P(x)] -> G(x))"
        s2 = "(A x)[P(x)]"
        r1 = self.yacc.parse(s1)
        r2 = self.yacc.parse(s2)
        self.assertTrue(r1.can_modus_ponens(r2))

    def test4(self):
        '''can mp 4'''
        s1 = "(A x)[(P(x) -> G(x))]"
        s2 = "(A x)[P(x)]"
        r1 = self.yacc.parse(s1)
        r2 = self.yacc.parse(s2)
        self.assertFalse(r1.can_modus_ponens(r2))

    def test5(self):
        '''do mp 1'''
        s1 = "(G(x) -> P(x))"
        s2 = "P(x)"
        r1 = self.yacc.parse(s1)
        r2 = self.yacc.parse(s2)
        self.assertEquals(r1.modus_ponens()[0], r2)

    def test6(self):
        '''do mp 2'''
        s1 = "(G(x) -> (P(x) or T(x)))"
        s2 = "(P(x) or T(x))"
        r1 = self.yacc.parse(s1)
        r2 = self.yacc.parse(s2)
        self.assertEquals(r1.modus_ponens()[0], r2)

    def test7(self):
        '''do mp 3'''
        s1 = "(G(x) -> (A x)[P(x)])"
        s2 = "(A x)[P(x)]"
        r1 = self.yacc.parse(s1)
        r2 = self.yacc.parse(s2)
        self.assertEquals(r1.modus_ponens()[0], r2)

    def test8(self):
        '''can mt 1'''
        s1 = "(G(x) -> P(x))"
        s2 = "not P(x)"
        r1 = self.yacc.parse(s1)
        r2 = self.yacc.parse(s2)
        self.assertTrue(r1.can_modus_tollens(r2))

    def test9(self):
        '''can mt 2'''
        s1 = "(G(x) -> (P(x) or T(x)))"
        s2 = "not (P(x) or T(x))"
        r1 = self.yacc.parse(s1)
        r2 = self.yacc.parse(s2)
        self.assertTrue(r1.can_modus_tollens(r2))

    def test10(self):
        '''can mt 3'''
        s1 = "(G(x) -> (A x)[P(x)])"
        s2 = "not (A x)[P(x)]"
        r1 = self.yacc.parse(s1)
        r2 = self.yacc.parse(s2)
        self.assertTrue(r1.can_modus_tollens(r2))

    def test11(self):
        '''can mt 4'''
        s1 = "(A x)[(P(x) -> G(x))]"
        s2 = "not G(x)"
        r1 = self.yacc.parse(s1)
        r2 = self.yacc.parse(s2)
        self.assertFalse(r1.can_modus_tollens(r2))

    def test12(self):
        '''do mt 1'''
        s1 = "(G(x) -> P(x))"
        s2 = "not G(x)"
        r1 = self.yacc.parse(s1)
        r2 = self.yacc.parse(s2)
        self.assertEquals(r1.modus_tollens()[0], r2)

    def test13(self):
        '''do mp 2'''
        s1 = "(G(x) -> (P(x) or T(x)))"
        s2 = "not G(x)"
        r1 = self.yacc.parse(s1)
        r2 = self.yacc.parse(s2)
        self.assertEquals(r1.modus_tollens()[0], r2)

    def test14(self):
        '''do mp 3'''
        s1 = "(G(x) -> (A x)[P(x)])"
        s2 = "not G(x)"
        r1 = self.yacc.parse(s1)
        r2 = self.yacc.parse(s2)
        self.assertEquals(r1.modus_tollens()[0], r2)

class TestHypotheticSyllogism(unittest.TestCase):
    '''Test hypothetic syllogism'''

    def setUp(self):
        from yacc import yacc
        self.yacc = yacc

    def test1(self):
        '''hs 1'''
        s1 = "(P(x) -> G(x))"
        s2 = "(G(x) -> Q(x))"
        r1 = self.yacc.parse(s1)
        r2 = self.yacc.parse(s2)
        self.assertTrue(r1.can_hs(r2))

    def test2(self):
        '''hs 2'''
        s1 = "(P(x) -> not G(x))"
        s2 = "(not G(x) -> Q(x))"
        r1 = self.yacc.parse(s1)
        r2 = self.yacc.parse(s2)
        self.assertTrue(r1.can_hs(r2))

    def test3(self):
        '''hs 3'''
        s1 = "(P(x) -> not G(x))"
        s2 = "(G(x) -> Q(x))"
        r1 = self.yacc.parse(s1)
        r2 = self.yacc.parse(s2)
        self.assertFalse(r1.can_hs(r2))

    def test4(self):
        '''hs 4'''
        s1 = "(P(x) -> not G(x))"
        s2 = "(G(x) -> Q(x))"
        r1 = self.yacc.parse(s1)
        r2 = self.yacc.parse(s2)
        self.assertFalse(r1.can_hs(r2))


class TestQuantRules(unittest.TestCase):
    '''Test rules related to quantifiers'''

    def setUp(self):
        from yacc import yacc
        self.yacc = yacc

    def test1(self):
        '''ug 1'''
        s1 = "P(x)"
        s2 = "(A x)[P(x)]"
        r1 = self.yacc.parse(s1)
        r2 = self.yacc.parse(s2)
        self.assertEquals(r1.ug()[0], r2)

    def test2(self):
        '''ug 2'''
        s1 = "(P(x) or G(x))"
        s2 = "(A x)[(P(x) or G(x))]"
        r1 = self.yacc.parse(s1)
        r2 = self.yacc.parse(s2)
        self.assertEquals(r1.ug()[0], r2)

    def test3(self):
        '''ug 3'''
        s1 = "(P(y) or G(x))"
        s2 = "(A y)[(P(y) or G(x))]"
        r1 = self.yacc.parse(s1)
        r2 = self.yacc.parse(s2)
        self.assertEquals(r1.ug()[0], r2)

class TestConjuntionEliminatio(unittest.TestCase):
    '''Test Conjuntion Elimination'''

    def setUp(self):
        from yacc import yacc
        self.yacc = yacc

    def test1(self):
        '''can ce ok'''
        s1 = "(P(x) and G(x))"
        r1 = self.yacc.parse(s1)
        self.assertTrue(r1.can_ce())

    def test2(self):
        '''can ce wrong'''
        s1 = "(P(x) or G(x))"
        r1 = self.yacc.parse(s1)
        self.assertFalse(r1.can_ce())

    def test3(self):
        '''ce 1'''
        s1 = "(P(x) and G(x))"
        s1a = "P(x)"
        s1b = "G(x)"
        r1 = self.yacc.parse(s1)
        r1a = self.yacc.parse(s1a)
        r1b = self.yacc.parse(s1b)
        l = r1.ce()
        self.assertEquals(l[0], r1a)
        self.assertEquals(l[1], r1b)
        self.assertEquals(len(l), 2)

if __name__ == '__main__':
    unittest.main()
