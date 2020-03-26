#import sys
#sys.path.append('/Users/n.beau/Desktop/Parseur_arithmetic')

#import numpy as np
#import pandas as pd

#from sklearn import preprocessing

from parseur_AE_simple.analysis_syntax_AE import Parser
from parseur_AE_simple.analysis_lexical_AE import Lexical 

class Create_Parseur_Dataset():

    def __init__(self, data):
        self.data = data





if __name__ == "__main__":
    #test = Lexical('2 +     3 +5')
    #print(test.lexicalAnalysis())
    data = Create_Parseur_Dataset('2 + 3 +2')
