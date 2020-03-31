import numpy as np
import pandas as pd

import random

from parseur_AE_simple.analysis_syntax_AE import Parser


class Create_Parseur_Dataframe():

    def __init__(self):
        self.operations = [('ADD', '+'), ('DOT', '*'), ('DIVIDE', '/'), ('MINUS', '-')]
        self.number = [('NUMBER', str(i)) for i in range(10)]
        self.data = pd.DataFrame(columns=['fenetre', 'pile', 'label'])

    def generator(self, size):
        """ Create a lexical arithmetic expression
        Arg:
        size (int): arithmetic expression's size
        Return:
        arith_expr (list): lexical arithmetic expression """
        arith_expr = list()
        for i in range(size):
            arith_expr.append(random.choice(self.number))
            arith_expr.append(random.choice(self.operations))
        arith_expr.append(random.choice(self.number))
        return arith_expr

    def fenetre_test(self, fenetre):
        """ Verification of buffer value
        Arg:
        fenetre (str): value of buffer """
        fenetre_return = list()
        for element in fenetre:
            if element == None:
                fenetre_return.append('None')
            else:
                fenetre_return.append(element[0])
        return np.array(fenetre_return)

    def create_dataframe(self, number_example, size_example):
        """ Create a dataframe of (buffer, stack, action) columns
        Arg:
        number_example (int): number of arithmetic expression
        size_example (int): size of each arithmetic expression
        Return:
        self.data (DataFrame) """
        for i in range(number_example):
            parse_example = Parser(self.generator(size_example))
            parse_example.parsing()
            example = pd.DataFrame({'fenetre': np.array(self.fenetre_test(parse_example.fenetre_stock)),
                                    'pile': np.array(parse_example.pile_stock),
                                    'label': np.array(parse_example.action)})
            self.data = self.data.append(example)
        return self.data


class Create_Parseur_Dataset():

    def __init__(self):
        pass

    def data_collect_fenetre(self, series_object):
        """ Collect the value from DataFrame's buffer column
        and vectorize it (One Hot Encoding)
        Arg:
        series_object (Series): buffer's column value
        Return:
        series_fenetre (list): vectorized values from
        the buffer column """
        series_fenetre = list()
        for i, x in enumerate(series_object):
            if x == 'NUMBER':
                series_fenetre.append(np.array([1, 0, 0, 0, 0, 0, 0]))
            elif x == 'EXPRESSION':
                series_fenetre.append(np.array([0, 1, 0, 0, 0, 0, 0]))
            elif x == 'DOT':
                series_fenetre.append(np.array([0, 0, 1, 0, 0, 0, 0]))
            elif x == 'DIVIDE':
                series_fenetre.append(np.array([0, 0, 0, 1, 0, 0, 0]))
            elif x == 'ADD':
                series_fenetre.append(np.array([0, 0, 0, 0, 1, 0, 0]))
            elif x == 'MINUS':
                series_fenetre.append(np.array([0, 0, 0, 0, 0, 1, 0]))
            elif x == 'None':
                series_fenetre.append(np.array([0, 0, 0, 0, 0, 0, 1]))
        return series_fenetre

    def data_collect_pile(self, series_object):
        """ Collect the value from DataFrame's stack column
        and vectorize it (One Hot Encoding)
        Arg:
        series_object (Series): stack's column value
        Return:
        series_pile (list): vectorized values from
        the buffer column """
        series_pile = list()
        for x in series_object:
            series_subpile = list()
            for y in x:
                if y == 'NUMBER':
                    series_subpile.append(np.array([1, 0, 0, 0, 0, 0, 0]))
                elif y == 'EXPRESSION':
                    series_subpile.append(np.array([0, 1, 0, 0, 0, 0, 0]))
                elif y == 'DOT':
                    series_subpile.append(np.array([0, 0, 1, 0, 0, 0, 0]))
                elif y == 'DIVIDE':
                    series_subpile.append(np.array([0, 0, 0, 1, 0, 0, 0]))
                elif y == 'ADD':
                    series_subpile.append(np.array([0, 0, 0, 0, 1, 0, 0]))
                elif y == 'MINUS':
                    series_subpile.append(np.array([0, 0, 0, 0, 0, 1, 0]))
            if series_subpile == []:
                series_pile.append([np.array([0, 0, 0, 0, 0, 0, 1])])
            else:
                series_pile.append(series_subpile)
        return series_pile

    def data_preprocessing_pile(self, list_pile):
        """ Concatenation and completion of the stack
        values
        Arg:
        list_pile (array): separate vectorized values of
        the stack
        Return:
        list_pile (array): concatenation of the different
        values from the stack """
        for index in range(len(list_pile)):
            size = len(list_pile[index])
            concatenation = np.concatenate([list_pile[index][i] for i in range(size)])
            while size < 5:
                concatenation = np.concatenate((concatenation, np.array([0, 0, 0, 0, 0, 0, 0])))
                size += 1
            list_pile[index] = concatenation
        return list_pile

    def create_dataset(self, dataframe):
        """ Create input of arithmetic expressions
        Arg:
        dataframe : DataFrame with (buffer, stack, action) values
        Return:
        concatenation (list[array]): input X of Neural Network"""
        concatenation = list()
        fenetre = self.data_collect_fenetre(dataframe['fenetre'])
        pile = self.data_preprocessing_pile(self.data_collect_pile(dataframe['pile']))
        for i in range(len(fenetre)):
            concatenation.append(np.concatenate([fenetre[i], pile[i]]))
        return concatenation

if __name__ == "__main__":
    dataframe = Create_Parseur_Dataframe().create_dataframe(number_example=100, size_example=11)
    X = Create_Parseur_Dataset().create_dataset(dataframe)
    print(X)
