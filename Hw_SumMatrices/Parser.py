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
        self.__functions_table_index = 1
        self.__quadruplets_index = 1
        self.__max_available_in_memory = 50
        self.__current_available_used = 0
        self.__symbols_table_index = self.__max_available_in_memory + 1
        self.__operands_stack = []
        self.__operators_stack = []
        self.__types_stack = []
        self.__jumps_stack = []
        self.__ifs_stack = []
        self.__quadruplets = []
        self.add_symbol('result', 'bool')

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

    def add_operand_with_type(self, current_operand, current_type):
        self.__operands_stack.append(current_operand)
        self.__types_stack.append(current_type)
        print("I added the operand: ", current_operand, " With type: ", current_type)

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
        loops : for id ACTION_ADD_FOR_VALUE equals arithmetic_expression to arithmetic_expression step arithmetic_expression inside_logic next id
        '''
    
    def p_logic_expression(self, p):
        '''
        logic_expression : arithmetic_expression
        logic_expression : bool_value ACTION_ADD_BOOL_VALUE
        logic_expression : not ACTION_ADD_OPERATOR logic_expression
        logic_expression : logic_expression logic_operator logic_expression ACTION_ADD_QUADRUPLET
        logic_expression : open_parenthesis logic_expression close_parenthesis
        '''
    
    def p_logic_operator(self, p):
        '''
        logic_operator : and ACTION_ADD_OPERATOR
        logic_operator : or ACTION_ADD_OPERATOR
        logic_operator : is_equal ACTION_ADD_OPERATOR
        logic_operator : is_not_equal ACTION_ADD_OPERATOR
        logic_operator : greater_than ACTION_ADD_OPERATOR
        logic_operator : greater_or_equal_than ACTION_ADD_OPERATOR
        logic_operator : less_than ACTION_ADD_OPERATOR
        logic_operator : less_or_equal_than ACTION_ADD_OPERATOR
        '''

    def p_arithmetic_expression(self, p):
        '''
        arithmetic_expression : value
        arithmetic_expression : value arithmetic_operator value ACTION_ADD_QUADRUPLET
        arithmetic_expression : arithmetic_expression arithmetic_operator arithmetic_expression ACTION_ADD_QUADRUPLET
        '''
    
    def p_arithmetic_operator(self, p):
        '''
        arithmetic_operator : sum ACTION_ADD_OPERATOR
        arithmetic_operator : substraction ACTION_ADD_OPERATOR
        arithmetic_operator : multiplication ACTION_ADD_OPERATOR
        arithmetic_operator : division ACTION_ADD_OPERATOR
        arithmetic_operator : exponent ACTION_ADD_OPERATOR
        '''


    def p_value(self, p):
        '''
        value : real_value
        value : functions
        value : ids_access
        '''

    def p_ids_access(self, p):
        '''
        ids_access : id ACTION_ADD_VAR_VALUE
        ids_access : id ACTION_ADD_VAR_VALUE open_brackets arithmetic_expression close_brackets ACTION_ADD_ONE_DIM_OPERAND
        ids_access : id ACTION_ADD_VAR_VALUE open_brackets arithmetic_expression close_brackets open_brackets arithmetic_expression close_brackets ACTION_ADD_TWO_DIM_OPERAND
        ids_access : id ACTION_ADD_VAR_VALUE open_brackets arithmetic_expression close_brackets open_brackets arithmetic_expression close_brackets open_brackets arithmetic_expression close_brackets ACTION_ADD_THREE_DIM_OPERAND
        ids_access : open_parenthesis ids_access close_parenthesis
        '''

    def p_real_value(self, p):
        '''
        real_value : word_value ACTION_ADD_WORD_VALUE
        real_value : float_value ACTION_ADD_FLOAT_VALUE
        real_value : id ACTION_ADD_VAR_VALUE
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
        assign : let ids_access equals logic_expression
        assign : let ids_access equals arithmetic_expression
        '''
        value = self.__operands_stack.pop()
        address = self.__operands_stack.pop()

        self.__quadruplets.append('= ' + str(value) + ' ' + address)
        self.__quadruplets_index += 1
        print('The value: ', value, ' Will go to: ', address)


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
        multiple_read : multiple_read comma ids_access
        '''

    def p_action_add_for_value(self, p):
        '''
        ACTION_ADD_FOR_VALUE :
        '''
        if not (p[-1] in self.__symbols_table):
            # If it's a new value
            self.add_symbol(p[-1], 'word')
        self.add_operand_with_type(p[-1], 'word')


    def p_action_add_var_value(self, p):
        '''
        ACTION_ADD_VAR_VALUE :
        '''
        self.__operands_stack.append(self.__symbols_table[p[-1]].address)
        self.__types_stack.append(self.__symbols_table[p[-1]].type)
        print("I added the operand: ", self.__symbols_table[p[-1]].address, " With type: ", self.__symbols_table[p[-1]].type)

    def p_action_add_word_value(self, p):
        '''
        ACTION_ADD_WORD_VALUE :
        '''
        self.add_operand_with_type(p[-1], 'word')

    def p_action_add_float_value(self, p):
        '''
        ACTION_ADD_FLOAT_VALUE :
        '''
        self.add_operand_with_type(p[-1], 'float')

    def p_action_add_bool_value(self, p):
        '''
        ACTION_ADD_BOOL_VALUE :
        '''
        self.add_operand_with_type(p[-1], 'bool')

    def p_action_add_operator(self, p):
        '''
        ACTION_ADD_OPERATOR :
        '''
        #print("Added operator: ", p[-1])
        self.__operators_stack.append(p[-1])

    def p_action_add_quadruplet(self, p):
        '''
        ACTION_ADD_QUADRUPLET :
        '''
        current_operator = self.__operators_stack.pop()
        current_right_operand = self.__operands_stack.pop()
        current_left_operand = self.__operands_stack.pop()

        if(self.__current_available_used > self.__max_available_in_memory):
            raise Exception('\nNot enough memory\n')
        result_stored_in = '#' + str(self.__current_available_used)
        self.__current_available_used += 1
        
        self.__quadruplets.append(str(current_operator) + ' ' + str(current_left_operand) + ' ' + str(current_right_operand) + ' ' + str(result_stored_in))
        self.__quadruplets_index += 1

        self.__operands_stack.append(result_stored_in)

        print('I added the quadruplet: ', self.__quadruplets[-1], ' and stored it in: ', self.__operands_stack[-1])

    def p_action_add_one_dim_operand(self, p):
        '''
        ACTION_ADD_ONE_DIM_OPERAND :
        '''
        first_dim = self.__operands_stack.pop()
        matrix = self.__operands_stack.pop()

        self.__operands_stack.append('* ' + str(matrix) + ' ' + str(first_dim))
        print('I added the one dim operand: ', self.__operands_stack[-1])

    def p_action_add_two_dim_operand(self, p):
        '''
        ACTION_ADD_TWO_DIM_OPERAND :
        '''
        second_dim = self.__operands_stack.pop()
        first_dim = self.__operands_stack.pop()
        matrix = self.__operands_stack.pop()

        self.__operands_stack.append('** ' + str(matrix) + ' ' + str(first_dim) + ' ' + str(second_dim))
        print('I added the two dim operand: ', self.__operands_stack[-1])

    def p_action_add_three_dim_operand(self, p):
        '''
        ACTION_ADD_THREE_DIM_OPERAND :
        '''
        third_dim = self.__operands_stack.pop()
        second_dim = self.__operands_stack.pop()
        first_dim = self.__operands_stack.pop()
        matrix = self.__operands_stack.pop()

        self.__operands_stack.append('*** ' + str(matrix) + ' ' + str(first_dim) + ' ' + str(second_dim) + ' ' + str(third_dim))
        print('I added the three dim operand: ', self.__operands_stack[-1])

    def p_error(self, p):
        raise Exception('\nIncorrecto\n')