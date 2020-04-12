from Lexer import Lexer
import ply.yacc as yacc

class Parser:

    def __init__(self):
        self.__lexer = Lexer()
        self.tokens = self.__lexer.getTokens()
        self.__parser = yacc.yacc(module=self)

    def Parse(self, s):
        self.__parser.parse(s)

    def p_program(self, p):
        '''
        program : inside_logic end
        program : inside_logic end subroutines
        '''
        print('\nCorrecto\n')

    def p_inside_logic(self, p):
        '''
        inside_logic : variable inside_logic
        inside_logic : conditions inside_logic
        inside_logic : loops inside_logic
        inside_logic : calls inside_logic
        inside_logic : read_or_write inside_logic
        |
        '''
    
    def p_variable(self, p):
        '''
        variable : dim id as variable_type
        variable : dim id as variable_type open_brackets word_value close_brackets
        variable : dim id as variable_type open_brackets word_value close_brackets open_brackets word_value close_brackets
        variable : dim id as variable_type open_brackets word_value close_brackets open_brackets word_value close_brackets open_brackets word_value close_brackets
        '''
    
    def p_variable_type(self, p):
        '''
        variable_type : word
        variable_type : float
        variable_type : bool
        '''
    
    def p_conditions(self, p):
        '''
        conditions : if
        '''

    def p_loops(self, p):
        '''
        loops : while open_parenthesis logic_expression close_parenthesis inside_logic wend
        loops : do inside_logic loop until open_parenthesis logic_expression close_parenthesis
        loops : for id equals arithmetic_expression to arithmetic_expression step arithmetic_expression inside_logic next id
        '''
    
    def p_logic_expression(self, p):
        '''
        logic_expression : arithmetic_expression
        logic_expression : compared_to_bool
        logic_expression : arithmetic_expression logic_operand arithmetic_expression
        logic_expression : logic_expression logic_operand logic_expression
        '''
    
    def p_logic_operand(self, p):
        '''
        logic_operand : and
        logic_operand : or
        logic_operand : not
        logic_operand : is_equal
        logic_operand : is_not_equal
        logic_operand : greater_than
        logic_operand : greater_or_equal_than
        logic_operand : less_than
        logic_operand : less_or_equal_than
        '''

    def p_compared_to_bool(self, p):
        '''
        compared_to_bool : arithmetic_expression is_equal bool_value
        compared_to_bool : arithmetic_expression is_not_equal bool_value
        compared_to_bool : bool_value is_equal arithmetic_expression
        compared_to_bool : bool_value is_not_equal arithmetic_expression
        '''

    def p_arithmetic_expression(self, p):
        '''
        arithmetic_expression : value
        arithmetic_expression : value arithmetic_operand value
        '''
    
    def p_arithmetic_operand(self, p):
        '''
        arithmetic_operand : sum
        arithmetic_operand : substraction
        arithmetic_operand : multiplication
        arithmetic_operand : division
        arithmetic_operand : exponent
        '''

    def p_value(self, p):
        '''
        value : real_value
        value : functions
        value : open_parenthesis arithmetic_expression close_parenthesis
        value : ids_access
        '''

    def p_ids_access(self, p):
        '''
        ids_access : id
        ids_access : id open_brackets arithmetic_expression close_brackets 
        ids_access : id open_brackets arithmetic_expression close_brackets open_brackets arithmetic_expression close_brackets 
        ids_access : id open_brackets arithmetic_expression close_brackets open_brackets arithmetic_expression close_brackets open_brackets arithmetic_expression close_brackets
        ids_access : open_parenthesis ids_access close_parenthesis
        '''

    def p_real_value(self, p):
        '''
        real_value : word_value
        real_value : float_value
        real_value : id
        '''

    def p_calls(self, p):
        '''
        calls : gosub id
        calls : id open_parenthesis close_parenthesis
        '''

    def p_subroutines(self, p):
        '''
        subroutines : sub procedure id inside_logic return subroutines
        subroutines : sub function id open_parenthesis close_parenthesis inside_logic end sub subroutines
        subroutines : sub function id open_parenthesis parameters close_parenthesis inside_logic end sub subroutines
        subroutines : sub function id open_parenthesis close_parenthesis as variable_type inside_logic end sub subroutines
        subroutines : sub function id open_parenthesis parameters close_parenthesis as variable_type inside_logic end sub subroutines
        |
        '''

    def p_parameters(self, p):
        '''
        parameters : variable
        parameters : parameters comma parameters
        '''
    
    def p_functions(self, p):
        '''
        functions : id open_parenthesis close_parenthesis
        functions : id open_parenthesis arguments close_parenthesis
        '''

    def p_arguments(self, p):
        '''
        arguments : ByVal value
        arguments : ByRef id
        arguments : arguments comma arguments
        '''

    def p_read_or_write(self, p):
        '''
        read_or_write : print
        read_or_write : read
        '''

    def p_print(self, p):
        '''
        print : dunkelPrint multiple_print
        print : dunkelPrint open_parenthesis multiple_print close_parenthesis
        '''

    def p_multiple_print(self, p):
        '''
        multiple_print : string
        multiple_print : value
        multiple_print : multiple_print comma multiple_print
        '''
    
    def p_read(self, p):
        '''
        read : dunkelRead multiple_read
        read : dunkelRead string comma multiple_read
        '''
    
    def p_multiple_read(self, p):
        '''
        multiple_read : ids_access
        multiple_read : multiple_read comma multiple_read
        '''

    def p_error(self, p):
        print('\nIncorrecto\n')