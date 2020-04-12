import ply.lex as lex
import Constants

class Lexer:
    def __init__(self):
        self.reserved = Constants.kReserved
        self.tokens = Constants.kTokens
        self.__initializeSimpleRegexRules()
        
        self.__lexer = lex.lex(module=self)

    def getTokens(self):
        return self.tokens

    def __initializeSimpleRegexRules(self):
        # Regular expression rules for simple tokens
        self.t_dim = r'dim'
        self.t_is_equal = r'\=\='
        self.t_is_not_equal = r'\<\>'
        self.t_greater_than = r'\>'
        self.t_greater_or_equal_than = r'\>\='
        self.t_less_than = r'\<'
        self.t_less_or_equal_than = r'\<\='
        self.t_equals = r'\='
        self.t_sum = r'\+'
        self.t_substraction = r'\-'
        self.t_multiplication = r'\*'
        self.t_division = r'\/'
        self.t_exponent = r'\^' 
        self.t_comma = r'\,'
        self.t_semicolon = r'\;'
        self.t_colon = r'\:'
        self.t_open_parenthesis = r'\('
        self.t_close_parenthesis = r'\)'
        self.t_open_brackets = r'\['
        self.t_close_brackets = r'\]'
        self.t_open_braces = r'\{'
        self.t_close_braces = r'\}'
        self.t_string = r'\"[a-zA-Z0-9 \.\?\:\t\r\n\f()\[\]\&\!\@\#\$\%\^\-\=\+\/\,]*\"'

        # A string containing ignored characters (spaces and tabs)
        self.t_ignore  =  ' \t\n'
        self.t_ignore_COMMENT = r'\/\/.*'

    def t_word_value(self, t):
        r'\d+'
        t.value = int(t.value)
        return t

    def t_float_value(self, t):
        r'\d+\.\d+'
        t.value = float(t.value)
        return t

    def t_bool_value(self, t):
        r'true | false'
        if t.value == 'true':
            t.value = True
        else:
            t.value = False
        return t

    def t_id(self, t):
        r'[a-zA-Z_][a-zA-Z_0-9]*'
        if t.value in self.reserved:
            t.type = self.reserved[ t.value ]
        else:  
            t.type = 'id'
        return t
    
    def t_error(self, t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)