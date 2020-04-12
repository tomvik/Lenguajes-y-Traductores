kReserved = {
    # Screen operands
    'dunkelRead' : 'dunkelRead',
    'dunkelPrint' : 'dunkelPrint',
    'dunkelCls' : 'dunkelCls',

    # Variable operands
    'let' : 'let',
    'dim' : 'dim',
    'as' : 'as',

    # Variable types
    'word' : 'word',
    'float' : 'float',
    'bool' : 'bool',

    # Conditional
    'if' : 'if',
    'then' : 'then',
    'else' : 'else',
    'elsif' : 'elsif',

    # Cycles
    'while' : 'while',
    'wend' : 'wend',
    'do' : 'do',
    'loop' : 'loop',
    'until' : 'until',
    'for' : 'for',
    'to' : 'to',
    'step' : 'step',
    'next' : 'next',
    'exit' : 'exit',

    # Functions and Subroutines
    'goto' : 'goto',
    'gosub' : 'gosub',
    'sub' : 'sub',
    'procedure' : 'procedure',
    'function' : 'function',
    'result' : 'result',
    'return' : 'return',
    'ByVal' : 'ByVal',
    'ByRef' : 'ByRef',

    # Logic operands and values
    'and' : 'and',
    'or' : 'or',
    'not' : 'not',
    'true' : 'true',
    'false' : 'false',

    # End program
    'end' : 'end'
}

kTokens = (
    # Screen operands
    'dunkelRead',
    'dunkelPrint',
    'dunkelCls',

    # Id for variables and functions
    'id',

    # Variable operands
    'let',
    'dim',
    'as',

    # Variable types and its values
    'word',
    'word_value',
    'float',
    'float_value',
    'bool',
    'bool_value',
    'string',

    # Conditional
    'if',
    'then',
    'end_if',
    'else',
    'elsif',

    # Cycles
    'while',
    'wend',
    'do',
    'loop',
    'until',
    'for',
    'to',
    'step',
    'next',
    'exit',

    # Functions and Subroutines
    'goto',
    'gosub',
    'sub',
    'procedure',
    'function',
    'result',
    'return',
    'ByVal',
    'ByRef',

    # Logic operators
    'and',
    'or',
    'not',
    'is_equal',
    'is_not_equal',
    'greater_than',
    'greater_or_equal_than',
    'less_than',
    'less_or_equal_than',
    'true',
    'false',

    # Arithmetic operators
    'equals',
    'sum',
    'substraction',
    'multiplication',
    'division',
    'exponent',

    # Syntax operators
    'comma',
    'colon',
    'semicolon',
    'open_parenthesis',
    'close_parenthesis',
    'open_brackets',
    'close_brackets',
    'open_braces',
    'close_braces',

    # End program
    'end'
)