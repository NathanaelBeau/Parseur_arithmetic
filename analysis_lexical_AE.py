class Lexical():

    def __init__(self, expr):
        self.expr = expr

    def lexicalAnalysis(self):
        ''' Recove a pile with an arithmetic expression
        Arg:
        expr (list): arithmetic expression
        Return:
        cleanExpression: well formed arithmetic expression'''
        cleanExpression = list()
        for char in self.expr:
            if not(self.whiteChar(char)):
                cleanExpression.append(self.charType(char))
        return cleanExpression

    def charType(self, char):
        ''' Find the type of a character
        Arg:
        char (str): token from arithmetic expression
        Return:
        tuple: character with its type'''
        if char == '+':
            return ('ADD', char)
        if char == '-':
            return('MINUS', char)
        if char == '*':
            return('DOT', char)
        if char == '/':
            return('DIVIDE', char)
        if self.is_number(char):
            return('NUMBER', char)
        if char == '(':
            return('LPAR', char)
        if char == ')':
            return('RPAR', char)
            
    def is_number(self, s):
        try:
            float(s)
            return True
        except ValueError:
            pass

    def whiteChar(self, char):
        ''' Verification of character
        Arg:
        expr (list): arithmetic expression
        Return:
        char: character on the left'''
        if char == ' ':
            return True
        else:
            return False


if __name__ == "__main__":
    test = Lexical('2 +     3 +5')
    print(test.lexicalAnalysis())
