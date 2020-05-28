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
        self.__quadruplets_index = 0
        self.__max_available_in_memory = 50
        self.__current_available_used = 0
        self.__symbols_table_index = self.__max_available_in_memory + 1
        self.__function_id_stack = []
        self.__operands_stack = []
        self.__operators_stack = []
        self.__types_stack = []
        self.__jumps_stack = []
        self.__while_jump_stack = []
        self.__ifs_stack = []
        self.__for_increment_stack = []
        self.__for_id_stack = []
        self.__write_variables_stack = []
        self.__quadruplets = []
        self.add_symbol('result', 'bool')

    def Parse(self, s):
        self.__parser.parse(s)

        print('################################Print you cunt')        
        for key in self.__symbols_table:
            self.__symbols_table[key].print_element()

        for key in self.__symbols_table:
            for i in range(len(self.__quadruplets)):
                if(not ('dunkelWrite' in self.__quadruplets[i]) and not ('dunkelRead' in self.__quadruplets[i]) ):
                    new_quadruplet = ''
                    for splited in self.__quadruplets[i].split():
                        if(splited == self.__symbols_table[key].id):
                            splited = self.__symbols_table[key].address
                        new_quadruplet += splited + ' '
                    self.__quadruplets[i] = new_quadruplet
                    #if()
                    #self.__quadruplets[i] = self.__quadruplets[i].replace(self.__symbols_table[key].id, self.__symbols_table[key].address)  
        

        print('################################Print you cunt')        
        for key in self.__symbols_table:
            self.__symbols_table[key].print_element()

    def get_executable(self):
        return (self.__quadruplets, self.__symbols_table, self.__current_available_used)

    def add_symbol(self, name, data_type, index = 0, dimention_1 = 0, dimention_2 = 0, dimention_3 = 0):
        if not (name in self.__symbols_table):
            if (data_type == 'word_array' or data_type == 'bool_array' or data_type == 'double_array'):
                self.__symbols_table[name] = SymbolsElement(name, data_type, '*' + str(self.__symbols_table_index), index, dimention_1, dimention_2, dimention_3)
            else:
                self.__symbols_table[name] = SymbolsElement(name, data_type, '#' + str(self.__symbols_table_index), index, dimention_1, dimention_2, dimention_3)
        
        for i in range(len(self.__operands_stack)):
            if self.__operands_stack[i] == name:
                self.__operands_stack[i] = '#' + str(self.__symbols_table[name].index)
        
        self.__symbols_table_index += 1

    def update_symbol(self, name, data_type):
        self.__symbols_table[name].type = data_type

    def print_symbol_table(self):
        for key in self.__symbols_table:
            self.__symbols_table[key].print_element()

        for i in range(len(self.__quadruplets)):
            print(i+1, ':', self.__quadruplets[i])

    def add_operand_with_type(self, current_operand, current_type):
        self.__operands_stack.append(current_operand)
        self.__types_stack.append(current_type)
        print("I added the operand: ", current_operand, " With type: ", current_type)

    def fill_jump(self, empty_jump_quadruplet_index, goto_index, goto_str):
        # This loop is done because when the expression needs to be recalculated many times
        # as in a loop, the jump must be from it, and not from the gotoF.
        while(goto_str != self.__quadruplets[empty_jump_quadruplet_index].split()[0] or ((goto_str == 'goto') and len(self.__quadruplets[empty_jump_quadruplet_index].split()) > 1)):
            empty_jump_quadruplet_index += 1
        if(empty_jump_quadruplet_index == goto_index):
            goto_index += 1
        self.__quadruplets[empty_jump_quadruplet_index] += ' ' + str(goto_index)

    def is_valid_for_condition(self, operator):
        operators = ['<', '<=', '>', '>=', '==', '<>', 'and', 'or', 'not', '+', '-', '/', '*', '^']
        if (operator in operators):
            return True
        return False

    def common_write_action(self, dunkelWhat):
        cout_or_cin = ''
        while self.__write_variables_stack:
            current_write_variable = self.__write_variables_stack.pop()
            if current_write_variable[0] == '"':
                current_write_variable = current_write_variable.replace('"', "")
            cout_or_cin = current_write_variable + ' ' + cout_or_cin
        self.__quadruplets.append(dunkelWhat + cout_or_cin)
        self.__quadruplets_index += 1

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

    def p_base_if(self, p):
        '''
        base_if : if open_parenthesis logic_expression close_parenthesis then ACTION_ADD_QUADRUPLET_EMPTY_JUMP inside_logic ACTION_NEW_IF ACTION_QUADRUPLET_EMPTY_JUMP_END_IF
        '''
    
    def p_conditions(self, p):
        '''
        conditions : base_if ACTION_FILL_JUMP end if ACTION_FILL_JUMP_END_IF
        conditions : base_if else ACTION_FILL_JUMP inside_logic end if ACTION_FILL_JUMP_END_IF
        conditions : base_if else_ifs end if ACTION_FILL_JUMP_END_IF
        conditions : base_if else_ifs else ACTION_FILL_JUMP inside_logic end if ACTION_FILL_JUMP_END_IF
        '''
    
    def p_else_ifs(self, p):
        '''
        else_ifs : elsif ACTION_FILL_JUMP open_parenthesis logic_expression close_parenthesis ACTION_ADD_QUADRUPLET_EMPTY_JUMP then inside_logic ACTION_QUADRUPLET_EMPTY_JUMP_END_IF
        else_ifs : else_ifs elsif ACTION_FILL_JUMP open_parenthesis logic_expression close_parenthesis ACTION_ADD_QUADRUPLET_EMPTY_JUMP then inside_logic ACTION_QUADRUPLET_EMPTY_JUMP_END_IF
        '''

    def p_loops(self, p):
        '''
        loops : while open_parenthesis logic_expression close_parenthesis ACTION_ADD_WHILE_QUADRUPLET_EMPTY_JUMP inside_logic wend ACTION_WHILE_GOTO
        loops : do ACTION_DO_WHILE_INDEX inside_logic loop until open_parenthesis logic_expression close_parenthesis ACTION_QUADRUPLET_EMPTY_JUMP_DO_WHILE 
        loops : for id ACTION_ADD_FOR_VALUE equals arithmetic_expression ACTION_ASSIGN_VALUE to ACTION_FOR_JUMP_BACK arithmetic_expression ACTION_ADD_FOR_QUADRUPLET_EMPTY_JUMP step arithmetic_expression ACTION_FOR_INCREMENT inside_logic next id ACTION_FOR_GOTO
        '''
    
    def p_logic_expression(self, p):
        '''
        logic_expression : arithmetic_expression        
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
        arithmetic_expression : arithmetic_expression arithmetic_operator arithmetic_expression ACTION_ADD_QUADRUPLET
        arithmetic_expression : open_parenthesis arithmetic_expression close_parenthesis
        '''
    
    def p_arithmetic_operator(self, p):
        '''
        arithmetic_operator : sum ACTION_ADD_OPERATOR
        arithmetic_operator : substraction ACTION_ADD_OPERATOR
        arithmetic_operator : multiplication ACTION_ADD_OPERATOR
        arithmetic_operator : division ACTION_ADD_OPERATOR
        arithmetic_operator : exponent ACTION_ADD_OPERATOR
        '''

    def p_possible_values(self, p):
        '''
        possible_values : real_value
        possible_values : functions
        possible_values : ids_access
        '''

    def p_value(self, p):
        '''
        value : possible_values
        value : not possible_values ACTION_ADD_NOT_OPERAND
        value : open_parenthesis value close_parenthesis
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
        real_value : bool_value ACTION_ADD_BOOL_VALUE
        real_value : id ACTION_ADD_VAR_VALUE
        '''

    def p_calls(self, p):
        '''
        calls : gosub id ACTION_ADD_SUBROUTINE_CALL
        calls : functions
        '''

    def p_subroutines(self, p):
        '''
        subroutines : sub procedure id ACTION_ADD_PROCEDURE inside_logic return ACTION_ADD_END_FUNCTION subroutines 
        subroutines : sub function id ACTION_ADD_FUNCTION open_parenthesis close_parenthesis inside_logic end sub ACTION_ADD_END_FUNCTION subroutines
        subroutines : sub function id ACTION_ADD_FUNCTION open_parenthesis parameters close_parenthesis inside_logic end sub ACTION_ADD_END_FUNCTION subroutines
        subroutines : sub function id ACTION_ADD_FUNCTION open_parenthesis close_parenthesis as variable_type inside_logic end sub ACTION_ADD_END_FUNCTION subroutines
        subroutines : sub function id ACTION_ADD_FUNCTION open_parenthesis parameters close_parenthesis as variable_type inside_logic end sub ACTION_ADD_END_FUNCTION subroutines
        |
        '''

        if len(p) >= 3:
            close_parenthesis = len(p)
            for i in range(len(p)):
                if p[i] == ')':
                    close_parenthesis = i
                    break
            if(close_parenthesis < len(p) and p[close_parenthesis+1] == 'as'):
                self.update_symbol(p[3], p[2] + ' ' + p[close_parenthesis+2])

    def p_assign(self, p):
        '''
        assign : let ids_access equals logic_expression ACTION_ASSIGN_VALUE
        assign : let ids_access equals arithmetic_expression ACTION_ASSIGN_VALUE
        '''

    def p_parameters(self, p):
        '''
        parameters : variable
        parameters : parameters comma parameters
        '''
    
    def p_functions(self, p):
        '''
        functions : id ACTION_ADD_FUNCTION_CALL open_parenthesis close_parenthesis
        functions : id ACTION_ADD_FUNCTION_CALL open_parenthesis arguments ACTION_ADD_PARAMETERS close_parenthesis
        '''

    def p_arguments(self, p):
        '''
        arguments : ByVal value ACTION_ADD_FUNCTION_OPERAND
        arguments : ByRef id ACTION_ADD_FUNCTION_OPERAND
        arguments : arguments comma arguments
        '''

    def p_read_or_write(self, p):
        '''
        read_or_write : print
        read_or_write : read
        read_or_write : dunkelCls ACTION_ADD_CLS_QUADRUPLET
        '''

    def p_print(self, p):
        '''
        print : dunkelPrint multiple_print ACTION_CONSOLE_WRITE
        print : dunkelPrint open_parenthesis multiple_print close_parenthesis ACTION_CONSOLE_WRITE
        '''

    def p_multiple_print(self, p):
        '''
        multiple_print : string
        multiple_print : arithmetic_expression
        multiple_print : multiple_print comma multiple_print
        '''
        if(len(p) == 2):
            if(p[0] == None and p[1] == None):
                self.__write_variables_stack.append(self.__operands_stack.pop())
            else:
                self.__write_variables_stack.append(p[1])
    
    def p_read(self, p):
        '''
        read : dunkelRead possible_read ACTION_CONSOLE_READ
        '''

    def p_possible_read(self, p):
        '''
        possible_read : string comma multiple_read
        possible_read : multiple_read
        '''
        if len(p) == 4:
            self.__write_variables_stack.append(p[1])
    
    def p_multiple_read(self, p):
        '''
        multiple_read : ids_access 
        multiple_read : multiple_read comma ids_access
        '''
        if(len(p) == 2 or len(p) == 4):
            self.__write_variables_stack.append(self.__operands_stack.pop())

    def p_action_add_for_value(self, p):
        '''
        ACTION_ADD_FOR_VALUE :
        '''
        if not (p[-1] in self.__symbols_table):
            # If it's a new value
            self.add_symbol(p[-1], 'word')
        self.__operands_stack.append(self.__symbols_table[p[-1]].address)
        self.__types_stack.append(self.__symbols_table[p[-1]].type)
        self.__for_id_stack.append(self.__symbols_table[p[-1]].address)
        print("I added the FOR operand: ", self.__symbols_table[p[-1]].id, self.__symbols_table[p[-1]].address, " With type: ", self.__symbols_table[p[-1]].type)


    def p_action_add_var_value(self, p):
        '''
        ACTION_ADD_VAR_VALUE :
        '''
        self.__operands_stack.append(self.__symbols_table[p[-1]].address)
        self.__types_stack.append(self.__symbols_table[p[-1]].type)
        print("I added the operand: ", self.__symbols_table[p[-1]].id, self.__symbols_table[p[-1]].address, " With type: ", self.__symbols_table[p[-1]].type)

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
        self.__operators_stack.append(p[-1])

    def p_action_add_function_operand(self, p):
        '''
        ACTION_ADD_FUNCTION_OPERAND :
        '''
        real_operand = self.__operands_stack.pop()
        self.__operands_stack.append(p[-2] + ' ' + real_operand)
        print('I Added the function operand: ', self.__operands_stack[-1])
        
    def p_action_add_function_call(self, p):
        '''
        ACTION_ADD_FUNCTION_CALL :
        '''
        self.__operands_stack.append(p[-1])
        self.__quadruplets.append('function_call ' + p[-1])
        self.__quadruplets_index += 1
        print('I Added the function call: ', self.__quadruplets[-1])
        
    def p_action_add_subroutine_call(self, p):
        '''
        ACTION_ADD_SUBROUTINE_CALL :
        '''
        self.__operands_stack.append(p[-1])
        self.__quadruplets.append('subroutine_call ' + p[-1])
        self.__quadruplets_index += 1
        print('I Added the subroutine call: ', self.__quadruplets[-1])

    def p_action_add_function(self, p):
        '''
        ACTION_ADD_FUNCTION :
        '''
        self.__function_id_stack.append(p[-1])
        self.add_symbol(self.__function_id_stack[-1], 'function', index=self.__quadruplets_index)
        self.__quadruplets.append('goto ')
        self.__quadruplets_index += 1

    def p_action_add_procedure(self, p):
        '''
        ACTION_ADD_PROCEDURE :
        '''
        self.__function_id_stack.append(p[-1])
        self.add_symbol(self.__function_id_stack[-1], 'procedure', index=self.__quadruplets_index)
        self.__quadruplets.append('goto ')
        self.__quadruplets_index += 1

    def p_action_add_end_function(self, p):
        '''
        ACTION_ADD_END_FUNCTION :
        '''
        self.fill_jump(self.__symbols_table[self.__function_id_stack.pop()].index-1, self.__quadruplets_index+1, 'goto')
        self.__quadruplets.append('return')
        self.__quadruplets_index += 1

    def p_action_assign_value(self, p):
        '''
        ACTION_ASSIGN_VALUE : 
        '''
        value = self.__operands_stack.pop()
        address = self.__operands_stack.pop()

        self.__quadruplets.append('= ' + str(value) + ' ' + address)
        self.__quadruplets_index += 1
        print('The value: ', value, ' Will go to: ', address)
        
    def p_action_add_parameters(self, p):
        '''
        ACTION_ADD_PARAMETERS :
        '''
        current_quadruplet = self.__quadruplets.pop()
        operands_to_add = ''
        while(len(self.__operands_stack) > 0 and ('ByVal' in self.__operands_stack[-1] or 'ByRef' in self.__operands_stack[-1]) ):
            current_operand = self.__operands_stack.pop()
            operands_to_add += ' ' + current_operand
        self.__quadruplets.append(current_quadruplet + operands_to_add)
        print('I Added the function call with paremeters: ', self.__quadruplets[-1])

        
    def p_action_add_not_operand(self, p):
        '''
        ACTION_ADD_NOT_OPERAND :
        '''
        current_operand = self.__operands_stack.pop()

        if(self.__current_available_used > self.__max_available_in_memory):
            raise Exception('\nNot enough memory\n')
        result_stored_in = '#' + str(self.__current_available_used)
        self.__current_available_used += 1

        self.__quadruplets.append('not ' + str(current_operand) + ' ' + str(result_stored_in))
        self.__quadruplets_index += 1
        self.__operands_stack.append(result_stored_in)
        print('I added the not operand and quadruplet as: ', self.__quadruplets[-1])

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

        self.__operands_stack.append('*-' + str(matrix) + '-' + str(first_dim))
        print('I added the one dim operand: ', self.__operands_stack[-1])

    def p_action_add_two_dim_operand(self, p):
        '''
        ACTION_ADD_TWO_DIM_OPERAND :
        '''
        second_dim = self.__operands_stack.pop()
        first_dim = self.__operands_stack.pop()
        matrix = self.__operands_stack.pop()

        self.__operands_stack.append('**-' + str(matrix) + '-' + str(first_dim) + '-' + str(second_dim))
        print('I added the two dim operand: ', self.__operands_stack[-1])

    def p_action_add_three_dim_operand(self, p):
        '''
        ACTION_ADD_THREE_DIM_OPERAND :
        '''
        third_dim = self.__operands_stack.pop()
        second_dim = self.__operands_stack.pop()
        first_dim = self.__operands_stack.pop()
        matrix = self.__operands_stack.pop()

        self.__operands_stack.append('***-' + str(matrix) + '-' + str(first_dim) + '-' + str(second_dim) + '-' + str(third_dim))
        print('I added the three dim operand: ', self.__operands_stack[-1])

    def p_action_add_quadruplet_empty_jump(self, p):
        '''
        ACTION_ADD_QUADRUPLET_EMPTY_JUMP :
        '''
        logical_expression_result = str(self.__operands_stack.pop())
        if(logical_expression_result[0] != '#' and logical_expression_result[0] != '*'):
            logical_expression_result = 'L ' + logical_expression_result
        self.__quadruplets.append('gotoF ' + logical_expression_result)
        self.__jumps_stack.append(self.__quadruplets_index)

        self.__quadruplets_index += 1

        print('I added a jump and qudruplet with condition: ', logical_expression_result)

    def p_action_add_while_quadruplet_empty_jump(self, p):
        '''
        ACTION_ADD_WHILE_QUADRUPLET_EMPTY_JUMP :
        '''
        logical_expression_result = str(self.__operands_stack.pop())
        print('MY LAST QUADRUPLET IS: ', self.__quadruplets[-1])
        last_operator = (self.__quadruplets[-1].split())[0]
        no_condition = 0
        if(not self.is_valid_for_condition(last_operator)):
            print('IT WAS NOT VALID: ', last_operator)
            no_condition = 1
        if(logical_expression_result[0] != '#' and logical_expression_result[0] != '*'):
            logical_expression_result = 'L ' + logical_expression_result
        self.__quadruplets.append('gotoF ' + logical_expression_result)
        self.__jumps_stack.append(self.__quadruplets_index)
        self.__while_jump_stack.append(self.__quadruplets_index + no_condition)

        self.__quadruplets_index += 1

        print('I added a jump and qudruplet with condition: ', logical_expression_result)

    def p_action_new_if(self, p):
        '''
        ACTION_NEW_IF :
        '''
        self.__ifs_stack.append([])
        print('NEW IF ADDED')

    def p_action_quadruplet_empty_jump_end_if(self, p):
        '''
        ACTION_QUADRUPLET_EMPTY_JUMP_END_IF  :
        '''
        self.__ifs_stack[-1].append(self.__quadruplets_index)

        self.__quadruplets.append('goto ')
        self.__quadruplets_index += 1
        print('A jump finished, and I added a goto to quadruplet and this to if stack: ', self.__ifs_stack[-1])

    def p_action_fill_jump(self, p):
        '''
        ACTION_FILL_JUMP :
        '''
        jump_index = self.__jumps_stack.pop() - 1
        print('Before filling the jump: ', self.__quadruplets[jump_index])
        self.fill_jump(jump_index, self.__quadruplets_index, 'gotoF')
        print('After filling the jump: ', self.__quadruplets[jump_index])

    def p_action_fill_jump_end_if(self, p):
        '''
        ACTION_FILL_JUMP_END_IF :
        '''
        print('FILL ALL THE JUMPS')
        for goto_index in self.__ifs_stack[-1]:
            print('Before filling the jump: ', self.__quadruplets[goto_index])
            self.fill_jump(goto_index, self.__quadruplets_index, 'goto')
            print('Before filling the jump: ', self.__quadruplets[goto_index])
        self.__ifs_stack.pop()

    def p_action_for_jump_back(self, p):
        '''
        ACTION_FOR_JUMP_BACK :
        '''
        self.__jumps_stack.append(self.__quadruplets_index + 1)

        
    def p_action_add_for_quadruplet_empty_jump(self, p):
        '''
        ACTION_ADD_FOR_QUADRUPLET_EMPTY_JUMP :
        '''
        limit = self.__operands_stack.pop()
        address = self.__for_id_stack[-1]

        if(self.__current_available_used > self.__max_available_in_memory):
            raise Exception('\nNot enough memory\n')
        result_stored_in = '#' + str(self.__current_available_used)
        self.__current_available_used += 1

        self.__quadruplets.append('< ' + address + ' ' + str(limit) + ' ' + result_stored_in)
        self.__quadruplets_index += 1
        print('I added a FOR CONDITION: ', self.__quadruplets[-1])

        self.__quadruplets.append('gotoF ' + result_stored_in)
        self.__quadruplets_index += 1

        print('I added a FOR JUMP CONDITION: ', self.__quadruplets[-1])

    def p_action_for_increment(self, p):
        '''
        ACTION_FOR_INCREMENT :
        '''
        increment = self.__operands_stack.pop()
        address = self.__for_id_stack.pop()
        self.__for_increment_stack.append('+ ' + address + ' ' + str(increment) + ' ' + address)
        print('I added to the for stack: ', self.__for_increment_stack[-1])

    def p_action_for_goto(self, p):
        '''
        ACTION_FOR_GOTO :
        '''
        add_one = 0
        empty_jump_quadruplet_index = self.__jumps_stack.pop() - 1
        self.__quadruplets.append(self.__for_increment_stack.pop())
        self.__quadruplets_index += 1
        if(self.__quadruplets[empty_jump_quadruplet_index][0] == '='):
            add_one = 1
        self.__quadruplets.append('goto ' + str(empty_jump_quadruplet_index + add_one))
        self.__quadruplets_index += 1
        self.fill_jump(empty_jump_quadruplet_index, self.__quadruplets_index + add_one, 'gotoF')

    def p_action_while_goto(self, p):
        '''
        ACTION_WHILE_GOTO :
        '''
        empty_jump_quadruplet_index = self.__jumps_stack.pop() - 1
        empty_while_jump_quadruplet_index = self.__while_jump_stack.pop() - 1

        self.__quadruplets.append('goto ' + str(empty_while_jump_quadruplet_index))
        self.__quadruplets_index += 1

        self.fill_jump(empty_jump_quadruplet_index, self.__quadruplets_index, 'gotoF')

    def p_action_do_while_jump_index(self, p):
        '''
        ACTION_DO_WHILE_INDEX :
        '''
        self.__jumps_stack.append(self.__quadruplets_index)

    def p_action_quadruplet_empty_jump_do_while(self, p):
        '''
        ACTION_QUADRUPLET_EMPTY_JUMP_DO_WHILE :
        '''
        statement_result = str(self.__operands_stack.pop())
        if(statement_result[0] != '#' and statement_result[0] != '*'):
            statement_result = 'L ' + statement_result
        self.__quadruplets.append('gotoT ' + statement_result + ' ' + str(self.__jumps_stack.pop()))
        self.__quadruplets_index += 1

    def p_action_console_write(self, p):
        '''
        ACTION_CONSOLE_WRITE :
        '''
        self.common_write_action('dunkelWrite ')

    def p_action_console_read(self, p):
        '''
        ACTION_CONSOLE_READ :
        '''
        self.common_write_action('dunkelRead ')

    def p_action_add_cls_quadruplet(self, p):
        '''
        ACTION_ADD_CLS_QUADRUPLET :
        '''
        self.__quadruplets.append('dunkelCls')

    def p_error(self, p):
        raise Exception('\nIncorrecto\n')