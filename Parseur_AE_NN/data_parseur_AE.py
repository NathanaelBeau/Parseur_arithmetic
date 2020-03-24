import sys
sys.path.append('/Users/n.beau/Desktop/Parseur_arithmetic/parseur_AE_simple')

import numpy as np
import pandas as pd

from analysis_syntax_AE import Parser
from analysis_lexical_AE import Lexical

class Parseur_data():

    def __init__(self, data):
        self.data = data






if __name__ == "__main__":
    test = Lexical('2 +     3 +5')
    print(test.lexicalAnalysis())