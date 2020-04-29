import sys

from Lexer import Lexer
import ply.yacc as yacc
from SymbolsElement import SymbolsElement

class Parser:

    def __init__(self):
        self.__lexer = Lexer()
        self.tokens = self.__lexer.getTokens()
        self.__parser = yacc.yacc(module=self)
        self.__symbols_table = {}
        self.__symbols_table_index = 0
        self.__functions_table_index = 1
        self.__operands_stack = []
        self.__operators_stack = []
        self.__types_stack = []
        self.__jumps_stack = []
        self.__ifs_stack = []
        self.__quadruplets = []

    def Parse(self, s):
        self.__parser.parse(s)

    def add_symbol(self, name, data_type, index = 0, dimention_1 = 0, dimention_2 = 0, dimention_3 = 0):
        if (data_type == 'word_array' or data_type == 'bool_array' or data_type == 'double_array'):
            self.__symbols_table[name] = SymbolsElement(name, data_type, '*' + str(self.__symbols_table_index), index, dimention_1, dimention_2, dimention_3)
        else:
            self.__symbols_table[name] = SymbolsElement(name, data_type, '#' + str(self.__symbols_table_index), index, dimention_1, dimention_2, dimention_3)
        self.__symbols_table_index += 1

    def print_symbol_table(self):
        for key in self.__symbols_table:
            self.__symbols_table[key].print_element()

    def p_program(self, p):
        '''
        program : inside_logic end
        program : inside_logic end subroutines
        '''
        print('\nCorrecto\n')
        self.print_symbol_table()
        

    def p_inside_logic(self, p):
        '''
        inside_logic : variable inside_logic
        inside_logic : conditions inside_logic
        inside_logic : loops inside_logic
        inside_logic : calls inside_logic
        inside_logic : read_or_write inside_logic
        inside_logic : assign inside_logic
        |
        '''
    
    def p_variable(self, p):
        '''
        variable : dim id as variable_type
        variable : dim id as variable_type open_brackets word_value close_brackets
        variable : dim id as variable_type open_brackets word_value close_brackets open_brackets word_value close_brackets
        variable : dim id as variable_type open_brackets word_value close_brackets open_brackets word_value close_brackets open_brackets word_value close_brackets
        '''
        if(len(p) == 5):
            self.add_symbol(p[2], p[4])
        else:
            p[4] += '_array'
            dimention_1 = p[6]
            if(len(p) == 8):
                self.add_symbol(p[2], p[4], dimention_1=dimention_1)
            else:
                dimention_2 = p[9]
                if(len(p) == 11):
                    self.add_symbol(p[2], p[4], dimention_1=dimention_1, dimention_2=dimention_2)
                else:
                    dimention_3 = p[12]
                    self.add_symbol(p[2], p[4], dimention_1=dimention_1, dimention_2=dimention_2, dimention_3=dimention_3)

        #print('This variable is: ', len(p))
        #for i in range(len(p)):
        #    print(p[i], sep=' ', end=' ')
        #print(' ')
    
    def p_variable_type(self, p):
        '''
        variable_type : word
        variable_type : float
        variable_type : bool
        '''
        p[0] = p[1] # To have the variable_type back in p_variable()
    
    def p_conditions(self, p):
        '''
        conditions : if open_parenthesis logic_expression close_parenthesis then inside_logic end if
        conditions : if open_parenthesis logic_expression close_parenthesis then inside_logic else inside_logic end if
        conditions : if open_parenthesis logic_expression close_parenthesis then inside_logic else_ifs end if
        conditions : if open_parenthesis logic_expression close_parenthesis then inside_logic else_ifs else inside_logic end if
        '''
    
    def p_else_ifs(self, p):
        '''
        else_ifs : elsif open_parenthesis logic_expression close_parenthesis then inside_logic
        else_ifs : else_ifs else_ifs
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
        logic_expression : not logic_expression
        logic_expression : open_parenthesis logic_expression close_parenthesis
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
        compared_to_bool : bool_value
        '''

    def p_arithmetic_expression(self, p):
        '''
        arithmetic_expression : value
        arithmetic_expression : value arithmetic_operand value
        arithmetic_expression : arithmetic_expression arithmetic_operand arithmetic_expression
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
        calls : functions
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

        if len(p) >= 3:
            self.add_symbol(p[3], p[2], index=self.__functions_table_index)
            self.__functions_table_index += 1

    def p_assign(self, p):
        '''
        assign : let id equals logic_expression
        assign : let id equals arithmetic_expression
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
        read_or_write : dunkelCls
        '''

    def p_print(self, p):
        '''
        print : dunkelPrint multiple_print
        print : dunkelPrint open_parenthesis multiple_print close_parenthesis
        '''

    def p_multiple_print(self, p):
        '''
        multiple_print : string
        multiple_print : arithmetic_expression
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
        raise Exception('\nIncorrecto\n')