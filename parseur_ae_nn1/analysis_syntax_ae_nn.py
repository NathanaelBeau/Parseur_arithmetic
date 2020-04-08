from parseur_ae_simple.analysis_lexical_ae import Lexical
from parseur_ae_nn1.nn_parseur_ae import Net

import numpy as np

import torch
import torch.nn as nn


class Parser:

    def __init__(self, expr):
        self.expr = expr
        self.fenetre = self.expr.pop(0)
        self.pile = ''
        self.fenetre_stock = list()
        self.PATH = './modelparameters/model.pt'
        self.grammar = {'EXPRESSION': ['NUMBER', 'LPAR EXPRESSION RPAR',
                                       'EXPRESSION MINUS EXPRESSION', 'EXPRESSION ADD EXPRESSION',
                                       'EXPRESSION DIVIDE EXPRESSION', 'EXPRESSION DOT EXPRESSION']
                        }

    def parsing(self):
        """
        Function for parse arithmetic
        operation.
        """
        model = torch.load(self.PATH)
        model.eval()
        while self.pile != 'EXPRESSION' or self.expr != [] or self.fenetre is not None:
            try:
                buffer = self.transform_buffer(self.fenetre[0])
            except:
                buffer = self.transform_buffer('None')
            stack = self.preprocess_stack(self.transform_stack(self.pile))
            X = torch.from_numpy(np.concatenate([buffer, stack])).float()
            action = self.action_reconstruct(torch.argmax(model(X)))
            if action == 'SHIFT':
                self.shift()
            else:
                try:
                    try:
                        self.pile = self.unary_reduce(self.pile)
                    except:
                        self.pile = self.binary_reduce(self.pile)
                except:
                    return print('L\'expression est invalide')
        return print('L\'expression est valide')

    def transform_buffer(self, buffer):
        if buffer == 'NUMBER':
            return np.array([1, 0, 0, 0, 0, 0, 0])
        elif buffer == 'EXPRESSION':
            return np.array([0, 1, 0, 0, 0, 0, 0])
        elif buffer == 'DOT':
            return np.array([0, 0, 1, 0, 0, 0, 0])
        elif buffer == 'DIVIDE':
            return np.array([0, 0, 0, 1, 0, 0, 0])
        elif buffer == 'ADD':
            return np.array([0, 0, 0, 0, 1, 0, 0])
        elif buffer == 'MINUS':
            return np.array([0, 0, 0, 0, 0, 1, 0])
        elif buffer == 'None':
            return np.array([0, 0, 0, 0, 0, 0, 1])

    def transform_stack(self, stack):
        stack_list = list()
        stack = stack.split()
        for value in stack:
            if value == 'NUMBER':
                stack_list.append(np.array([1, 0, 0, 0, 0, 0, 0]))
            elif value == 'EXPRESSION':
                stack_list.append(np.array([0, 1, 0, 0, 0, 0, 0]))
            elif value == 'DOT':
                stack_list.append(np.array([0, 0, 1, 0, 0, 0, 0]))
            elif value == 'DIVIDE':
                stack_list.append(np.array([0, 0, 0, 1, 0, 0, 0]))
            elif value == 'ADD':
                stack_list.append(np.array([0, 0, 0, 0, 1, 0, 0]))
            elif value == 'MINUS':
                stack_list.append(np.array([0, 0, 0, 0, 0, 1, 0]))
        if not stack_list:
            stack_list.append(np.array([0, 0, 0, 0, 0, 0, 1]))
        return stack_list

    def preprocess_stack(self, stack_list):
        size = len(stack_list)
        concatenation = np.concatenate([stack_list[i] for i in range(size)])
        while size < 5:
            # mettre element nul
            concatenation = np.concatenate((concatenation, np.array([0, 0, 0, 0, 0, 0, 0])))
            size += 1
        return np.array(concatenation)

    def action_reconstruct(self, action_tenseur):
        if action_tenseur.item() == 1:
            return 'SHIFT'
        else:
            return 'REDUCE'

    def shift(self):
        """
        shift operation : moving the
        window and stack the pile
        """
        self.pile += ' ' + self.fenetre[0]
        try:
            self.fenetre = self.expr.pop(0)
        except:
            self.fenetre = None

    def unary_reduce(self, pile):
        """
        Reducing operation for NUMBER
        """
        words = pile.split()
        last_word = self.reduce(words[-1])
        words[-1] = last_word
        return ' '.join(words)

    def binary_reduce(self, pile):
        """Reducing operation for operation
        like *, /, -, +...
        """
        words = pile.split()
        length_operation = len(words)
        operation = words[-3:]
        if length_operation == 3:
            return self.reduce(' '.join(operation))
        else:
            return ' '.join(words[:-3]) + ' ' + self.reduce(' '.join(operation))

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


if __name__ == "__main__":
    test = Lexical('2*2+2*')
    testparse = Parser(test.lexicalAnalysis())
    testparse.parsing()
