import ast
from time import sleep

from SymbolsElement import SymbolsElement

functions_stack = []

def execute(executables):
    '''
    This function executes the quadruplets generated from the lexer and parser
    '''
    quadruplets, symbols_table, temporal_variables, max_temporal_variables = executables
    #print_quadruplets_and_memory(quadruplets, symbols_table)
    for i in range (temporal_variables):
        symbols_table['temp_' + str(i)] = SymbolsElement('temp_' + str(i), 'temp', '#' + str(i), 0, 0, 0, 0)

    # Set address as new key.
    #print('################Change key and fix index')
    new_symbols_table = {}
    for key, value in symbols_table.items():
        new_symbols_table[value.address] = value
        if new_symbols_table[value.address].index != 0:
            #print('This could be changed', quadruplets[new_symbols_table[value.address].index].split())
            if quadruplets[new_symbols_table[value.address].index].split()[0] == 'goto':
                new_symbols_table[value.address].index += 1
            elif quadruplets[new_symbols_table[value.address].index].split()[0] == 'return':
                new_symbols_table[value.address].index += 2

    symbols_table = new_symbols_table
    #print_quadruplets_and_memory(quadruplets, symbols_table)
    
    current_quadruplet = 0
    while current_quadruplet < len(quadruplets):
        current_quadruplet = execute_single_quadruple(quadruplets[current_quadruplet].split(), current_quadruplet, symbols_table)
    #print_quadruplets_and_memory(quadruplets, symbols_table)

def execute_single_quadruple(single_quadruplet, current_quadruplet, symbols_table):
    #sleep(0.05)
    #print('Current quadruplet with index:', current_quadruplet, single_quadruplet)
    if single_quadruplet[0] == 'dunkelWrite':
        for data in single_quadruplet[1:]:
            if data[0] == '#' and len(data) > 1:
                if data in symbols_table:
                    print(symbols_table[data].value, end=' ')
                else:
                    raise Exception (f'dunkelWrite Error! variable {data} is not defined')
            elif '***-*' == data[0:5] or '**-*' == data[0:4] or '*-*' == data[0:3]:
                _, current_value, _ = parse_matrix(data, symbols_table)
                print(current_value, end=' ')
            else:
                print(data, end=' ')
        print()
    
    elif single_quadruplet[0] == 'dunkelRead':
        to_process_read = []
        for data in single_quadruplet[1:]:
            if data[0] == '#' and len(data) > 1:
                if data in symbols_table:
                    to_process_read.append(data)
                else:
                    raise Exception (f'dunkelWrite Error! variable {data} is not defined')
            elif '***-*' == data[0:5] or '**-*' == data[0:4] or '*-*' == data[0:3]:
                to_process_read.append(data)
            else:
                print(data, end=' ')
        
        for data in to_process_read:
            if data[0] == '#' and len(data) > 1:
                if data in symbols_table:
                    symbols_table[data].value = ast.literal_eval(input())
                else:
                    raise Exception (f'dunkelWrite Error! variable {data} is not defined')
            elif '***-*' == data[0:5] or '**-*' == data[0:4] or '*-*' == data[0:3]:
                parsed_matrix, _, _ = parse_matrix(data, symbols_table)
                symbols_table = set_matrix_value(parsed_matrix, symbols_table, ast.literal_eval(input()))

    elif single_quadruplet[0] in ['<', '<=', '>', '>=', '==', '<>', 'and', 'or', '+', '-', '/', '*', '^']:
        operation_result = arithmetic_operation(single_quadruplet[0], single_quadruplet[1], single_quadruplet[2], symbols_table)
        if '*' in single_quadruplet[-1]:
            parsed_matrix, _, _ = parse_matrix(single_quadruplet[-1], symbols_table)
            symbols_table = set_matrix_value(parsed_matrix, symbols_table, operation_result)
        else:
            #print("The result was:", operation_result)
            symbols_table[single_quadruplet[-1]].value = operation_result

    elif single_quadruplet[0] == '=' or single_quadruplet[0] == 'not':
        operand_value = 0
        #print("I will do a =")
        if '*' in single_quadruplet[1]:
            _, operand_value, _ = parse_matrix(single_quadruplet[1], symbols_table)
        elif '#' in single_quadruplet[1]:
            operand_value = symbols_table[single_quadruplet[1]].value
        else:
            operand_value = ast.literal_eval(single_quadruplet[1])
        
        #print('The operand is:', operand_value)
        if single_quadruplet[0] == 'not':
            operand_value = (operand_value == 0)

        if '*' in single_quadruplet[2]:
            parsed_matrix, _, _ = parse_matrix(single_quadruplet[2], symbols_table)
            symbols_table = set_matrix_value(parsed_matrix, symbols_table, operand_value)
        else:
            symbols_table[single_quadruplet[2]].value = operand_value

    elif single_quadruplet[0] == 'gotoF':
        if single_quadruplet[1] == 'L':
            if not ast.literal_eval(single_quadruplet[2]):
                return ast.literal_eval(single_quadruplet[3])
        else:
            if not symbols_table[single_quadruplet[1]].value:
                return ast.literal_eval(single_quadruplet[2])

    elif single_quadruplet[0] == 'gotoT':
        if single_quadruplet[1] == 'L':
            if ast.literal_eval(single_quadruplet[2]):
                return ast.literal_eval(single_quadruplet[3])
        else:
            if symbols_table[single_quadruplet[1]].value:
                return ast.literal_eval(single_quadruplet[2])

    elif single_quadruplet[0] == 'goto':
        return ast.literal_eval(single_quadruplet[1])

    elif single_quadruplet[0] == 'function_call' or single_quadruplet[0] == 'subroutine_call':
        functions_stack.append(current_quadruplet + 1)
        return symbols_table[single_quadruplet[1]].index

    elif single_quadruplet[0] == 'return':
        if functions_stack:
            return functions_stack.pop()
        


    return current_quadruplet + 1

def get_matrix_value(matrix, symbols_table):
    if not (matrix[0] in symbols_table):
        raise Exception (f'Get Matrix Error! variable {matrix[0]} is not defined and it is part of the dimentions')

    if len(matrix) == 2:
        return symbols_table[matrix[0]].value[matrix[1]]
    elif len(matrix) == 3:
        return symbols_table[matrix[0]].value[matrix[1]][matrix[2]]
    elif len(matrix) == 4:
        return symbols_table[matrix[0]].value[matrix[1]][matrix[2]][matrix[3]]
    raise Exception (f'Get Matrix Error! The parsed matrix {matrix} has an incorrect lenght')

def set_matrix_value(matrix, symbols_table, value):
    if not (matrix[0] in symbols_table):
        raise Exception (f'Set Matrix Value Error! variable {matrix[0]} is not defined and it is part of the dimentions')

    if len(matrix) == 2:
        symbols_table[matrix[0]].value[matrix[1]] = value
    elif len(matrix) == 3:
        symbols_table[matrix[0]].value[matrix[1]][matrix[2]] = value
    elif len(matrix) == 4:
        symbols_table[matrix[0]].value[matrix[1]][matrix[2]][matrix[3]] = value
    else:
        raise Exception (f'Set Matrix Value Error! The parsed matrix {matrix} has an incorrect lenght')
    return symbols_table


def parse_matrix(matrix, symbols_table):
    '''
    This function parses the quadruplet string containing a matrix and returns a list with the matrix info
    Example:
    For a matrix mat[4][5][6] the quadruplet string will be: ***-*[address_mat]-4-5-6
    The returning list will be: [address_mat, 4, 5, 6]
    parsed_matrix = [adress of the matrix, dimention 1, dimention 2, dimention 3]
    '''
    parsed_matrix = []
    #print('Will begin parsing matrix:', matrix)
    matrix = matrix.split('-')
    #print('Splitted into:', matrix)
    parsed_matrix.append(matrix[1])
    possible_next_index = 2
    index_value = 0
    max_parsed_length = len(matrix[0]) + 1
    while possible_next_index < len(matrix) and len(parsed_matrix) < max_parsed_length:
        if '*' in matrix[possible_next_index]:
            matrix_to_parse = '-'.join(matrix[possible_next_index:])
            _, index_value, last_index = parse_matrix(matrix_to_parse, symbols_table)
            possible_next_index += last_index - 1
        elif '#' in matrix[possible_next_index]:
            if matrix[possible_next_index] in symbols_table:
                index_value = symbols_table[matrix[possible_next_index]].value
            else:
                raise Exception (f'Parse Matrix Error! variable {matrix[possible_next_index]} is not defined and it is part of the dimentions')
        else:
            index_value = ast.literal_eval(matrix[possible_next_index])
        parsed_matrix.append(index_value)
        possible_next_index += 1
    
    #print('Finished parsing the matrix. Result is:', parsed_matrix)

    return parsed_matrix, get_matrix_value(parsed_matrix, symbols_table), possible_next_index

def arithmetic_operation(operator, operand_1, operand_2, symbols_table):
    '''
    Execute arithmetic and boolean operations
    '''
    if operand_1[0] == '#':
        operand_1 = symbols_table[operand_1].value
    elif '*' in operand_1:
        _, operand_1, _ = parse_matrix(operand_1, symbols_table)
    else:
        operand_1 = ast.literal_eval(operand_1)

    if operand_2[0] == '#':
        operand_2 = symbols_table[operand_2].value
    elif '*' in operand_2:
        _, operand_2, _ = parse_matrix(operand_2, symbols_table)
    else:
        operand_2 = ast.literal_eval(operand_2)

    if operator == '<':
        return operand_1 < operand_2
    elif operator == '<=':
        return operand_1 <= operand_2
    elif operator == '>':
        return operand_1 > operand_2
    elif operator == '>=':
        return operand_1 >= operand_2
    elif operator == '==':
        return operand_1 == operand_2
    elif operator == '<>':
        return operand_1 != operand_2
    elif operator == 'and':
        return operand_1 and operand_2
    elif operator == 'or':
        return operand_1 or operand_2
    elif operator == '+':
        return operand_1 + operand_2
    elif operator == '-':
        return operand_1 - operand_2
    elif operator == '/':
        return operand_1 / operand_2
    elif operator == '*':
        return operand_1 * operand_2
    elif operator == '^':
        return pow(operand_1, operand_2)
    

def print_quadruplets_and_memory(quadruplets, symbols_table):
    '''
    Prints the program memory and the all quadruplets generated from the program
    '''
    print('\nMemory:')
    for key in symbols_table:
        symbols_table[key].print_element()
    print('\nQuadruplets:')
    for i in range (len(quadruplets)):
        print(str(i) + ':', quadruplets[i])
    print()