import numpy as np

class SymbolsElement:
    '''
    Symbol element for the Symbols Table.
    '''
    def __init__(self, variable_id, variable_type, variable_address, function_index, dimention_1, dimention_2, dimention_3):
        self.id = variable_id
        self.type = variable_type
        self.address = variable_address
        self.index = function_index
        self.value = self.__set_initial_value(variable_type, dimention_1, dimention_2, dimention_3)

    def __set_initial_value(self, variable_type, dimention_1, dimention_2, dimention_3):
        if variable_type == 'word' or variable_type == 'bool':
            return 0
        elif variable_type == 'float':
            return 0.0
        elif variable_type == 'word_array' or variable_type == 'bool_array':
            if dimention_2 != 0:
                if dimention_3 != 0:
                    return np.zeros((dimention_1, dimention_2, dimention_3), dtype=int)
                else:
                    return np.zeros((dimention_1, dimention_2), dtype=int)
            else:
                return np.zeros(dimention_1, dtype=int)
        elif variable_type == 'float_array':
            if dimention_2 != 0:
                if dimention_3 != 0:
                    return np.zeros((dimention_1, dimention_2, dimention_3))
                else:
                    return np.zeros((dimention_1, dimention_2))
            else:
                return np.zeros(dimention_1)

    def print_element(self):
        print('Id:', (self.id).ljust(35), 'Type:', (self.type).ljust(25), 'Address:', (self.address).ljust(15), 'Index:', (str(self.index)).ljust(15), 'Value:', self.value)