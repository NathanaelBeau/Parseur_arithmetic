from .analysis_lexical_AE import Lexical

class Parser():

    def __init__(self, expr):
        self.expr = expr
        self.fenetre = self.expr.pop(0)
        self.pile = ''
        self.store = list()
        self.action = list()
        self.fenetre_stock = list()
        self.pile_stock = list()
        self.grammar = {'EXPRESSION': ['NUMBER', 'LPAR EXPRESSION RPAR',
                        'EXPRESSION MINUS EXPRESSION', 'EXPRESSION ADD EXPRESSION',
                        'EXPRESSION DIVIDE EXPRESSION', 'EXPRESSION DOT EXPRESSION']
                        }

    def parsing(self):
        """
        Function for parse arithmetic
        operation.
        """
        while self.pile != 'EXPRESSION' or self.expr != [] or self.fenetre != None:
            self.fenetre_stock.append(self.fenetre)
            self.pile_stock.append(self.pile.split())
            if not(self.unary_reduce_test(self.pile)):
                if not(self.binary_reduce_test(self.pile)):
                    if self.shift_test():
                        self.shift()  # shift si on peut rien faire
                else:  # on reduce une expression
                    if self.shift_test():  # voir si fenetre est None
                        words = self.pile.split()
                        if self.fenetre[0] in ('DOT', 'DIVIDE'):  # priorisation
                            if words[-2] in ('ADD', 'MINUS'):
                                self.shift()
                            else:
                                self.pile = self.binary_reduce(self.pile)
                        else:
                            self.pile = self.binary_reduce(self.pile)
                    else:
                        self.pile = self.binary_reduce(self.pile)
            else:  # on reduce NUMBER
                self.pile = self.unary_reduce(self.pile)
            if self.expr == [] and self.pile != 'EXPRESSION':
                if self.shift_test() == False:
                    if not(self.binary_reduce_test(self.pile)) and not(self.unary_reduce_test(self.pile)):
                        return print('L\'expression n\'est pas valide')
        return print('L\'expression est valide')

    def shift_test(self):
        """
        Verify if the window is empty
        """
        try:
            self.fenetre[0]
            return True
        except:
            return False

    def shift(self):
        """
        shift operation : moving the
        window and stack the pile
        """
        self.tree_construct(self.fenetre[0], self.fenetre[1])
        self.pile += ' ' + self.fenetre[0]
        self.action.append('SHIFT')
        try:
            self.fenetre = self.expr.pop(0)
        except:
            self.fenetre = None

    def unary_reduce_test(self, sentence):
        """
        Test if it is possible to reduce
        NUMBER
        """
        if sentence == '':
            return False
        words = sentence.split()
        last_word = self.reduce_test(words[-1])
        if not(last_word):
            return False
        else:
            return True

    def unary_reduce(self, sentence):
        """
        Reducing operation for NUMBER
        """
        words = sentence.split()
        last_word = self.reduce(words[-1])
        words[-1] = last_word
        self.action.append('REDUCE')
        self.tree_construct('EXPRESSION', 'NUMBER')
        return ' '.join(words)

    def binary_reduce_test(self, sentence):
        """
        Test if it is possible to reduce
        operation like *, /, -, +...
        """
        words = sentence.split()
        length_operation = len(words)
        if length_operation < 3:
            return False
        operation = words[-3:]
        if not(self.reduce_test(' '.join(operation))):
            return False
        else:
            return True

    def binary_reduce(self, pile):
        """Reducing operation for operation
        like *, /, -, +...
        """
        words = pile.split()
        length_operation = len(words)
        operation = words[-3:]
        if length_operation == 3:
            self.action.append('REDUCE')
            self.tree_construct('EXPRESSION', operation)
            return self.reduce(' '.join(operation))
        else:
            self.action.append('REDUCE')
            self.tree_construct('EXPRESSION', operation)
            return ' '.join(words[:-3]) + ' ' + self.reduce(' '.join(operation))

    def reduce_test(self, pile):
        """
        Test if it is possible to
        replace in the grammar
        """
        for valeurs in self.grammar.values():
            for valeur in valeurs:
                if pile == valeur:
                    return True
            return False

    def reduce(self, pile):
        """
        Replace the expression on top of
        the pile by the expression of the
        grammar
        """
        for cle, valeurs in self.grammar.items():
            for valeur in valeurs:
                if pile == valeur:
                    return cle

    def tree_construct(self, new_expr, last_value):
        self.store.append((new_expr, last_value))

if __name__ == "__main__":
    test = Lexical('2*2+2*2')
    testparse = Parser(test.lexicalAnalysis())
    testparse.parsing()
    print(testparse.action)
    print(len(testparse.fenetre_stock), testparse.fenetre_stock)
    print(len(testparse.pile_stock), testparse.pile_stock)
