import numpy as np
import pandas as pd

from Parseur_AE_simple.analysis_syntax_AE import Parser
from Parseur_AE_simple.analysis_lexical_AE import Lexical

class parseur_data():

    def __init__(self, data):
        self.data = data






if __name__ == "__main__":
    test = Lexical('2 +     3 +5')
    print(test.lexicalAnalysis())