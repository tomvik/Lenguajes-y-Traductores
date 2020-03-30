import ply.lex as lex
import ply.yacc as yacc
import sys


class Lexer:
    def __init__(self):
        self.tokens = ('HOLA',
              'COMA',
              'QUE',
              'TAL')
        self.t_HOLA = r'hola'
        self.t_COMA = r'\,'
        self.t_QUE = r'que'
        self.t_TAL = r'tal'
        self.t_ignore = r' '

        
        self.__lexer = lex.lex(module=self)

    def t_error(self, t):
        print("\nIllegal characters")
        t.lexer.skip(1)

    def GetTokens(self):
        return self.tokens

class Parser:

    def __init__(self):
        self.__lexer = Lexer()
        self.tokens = self.__lexer.GetTokens()
        self.__parser = yacc.yacc(module=self)

    def Parse(self, s):
        self.__parser.parse(s)

    def p_S(self, p):
        '''
        S : X QUE TAL
        '''
        print('\nCorrecto\n')

    def p_X(self, p):
        '''
        X : HOLA
        X : HOLA COMA X
        '''
    
    def p_error(self, p):
        print('\nIncorrecto\n')



if __name__ == "__main__":
    parser = Parser()

    while True:
        try:
            s = input('')
        except EOFError:
            break
        parser.Parse(s)
