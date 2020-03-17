import sys
import os
import os.path
import re
from collections import Counter
from analysis_syntax_AE import Parser
from analysis_lexical_AE import Lexical

class ConsTree():
    '''That's your phrase structure tree.
    '''
    def __init__(self,label,children=None):
        self.label = label
        self.children = [] if children is None else children

    def is_leaf(self):
        return self.children == []
    
    def add_child(self, child_node):
        self.children.append(child_node)
        
    def arity(self):
        return len(self.children)

    def __str__(self):
        '''Pretty prints the tree
        '''
        return self.label if self.is_leaf() else '(%s %s)'%(self.label,' '.join([str(child) for child in self.children]))


class TreeConstruct():

    def __init__(self): 
        self.tree = list()
        self.stock = list()

    def construction(self, list_action, list_value):
        '''Construction of the arithmetic operation tree
        Arg:
        list_action: action shift/reduce for arithmetic operation
        list_value: value corresponding to each shift/reduce operation
        Return:
        arithmetic expression tree
        '''
        combined_action_value = [*zip(list_action, list_value)]
        for value in combined_action_value:
            if value[0] == 'SHIFT':
                self.stock.append(value[1])
            else:
                if value[1][1] == 'NUMBER':
                    self.tree.append(ConsTree(self.stock[-1][0], self.stock[-1][1]))
                    self.stock.pop(-1)
                else:
                    self.tree.append(ConsTree('EXPRESSION', [self.tree[-1], ConsTree(self.stock[-1][0],
                        self.stock[-1][1]), self.tree[-2]]))
                    self.stock.pop(-1)
                    if not(self.stock == []):
                        del self.tree[-3:-1]
        return self.tree[-1]

    def evaluate(self, tree):
        '''Evaluation of a arithmetic operation tree
        '''
        size = tree.arity()
        if size == 3:
            valeur_1 = self.evaluate(tree.children[0])
            valeur_2 = self.evaluate(tree.children[2])
            op = tree.children[1].label
            if op == 'ADD':
                return float(valeur_1) + float(valeur_2)
            if op == 'DOT':
                return float(valeur_1) * float(valeur_2)
            if op == 'DIVIDE':
                return float(valeur_1) / float(valeur_2)
            if op == 'MINUS':
                return float(valeur_1) - float(valeur_2)
        if size == 1:
            return tree.children[0]

    def oracle(self, tree):


if __name__ == "__main__":
    test = Lexical('2+2*3')
    testparse = Parser(test.lexicalAnalysis())
    testparse.parsing()
    action = testparse.action
    value = testparse.store
    construction_tree = TreeConstruct()
    tree = construction_tree.construction(action, value)
    print(tree)
    print(construction_tree.evaluate(tree))