from Parser import Parser    # The code to test
import unittest   # The test framework

class Test_TestParserSubRoutinesAndFunctions(unittest.TestCase):
    def setUp(self):
        self.parser = Parser()
        pass

    def __incorrect_tests(self, incorrect_texts):
        for incorrect_text in incorrect_texts:
            with self.assertRaises(Exception, msg=incorrect_text) as context:
                self.parser.Parse(incorrect_text)
            self.assertTrue('\nIncorrecto\n' in str(context.exception), msg=incorrect_text)

    def __correct_tests(self, correct_texts):
        for correct_text in correct_texts:
            raised = False
            try:
                self.parser.Parse(correct_text)
            except:
                raised = True
            self.assertFalse(raised, msg='An exception was raised'+correct_text)

    def test_wrong_subroutines(self):
        incorrect_texts = [
            '''
            end
            sub procedure procedure_name
                dunkelCls
            ''',
            '''
            end
            sub procedure_name
                dunkelCls
            return
            ''',
            '''
            end
            procedure procedure_name
                dunkelCls
            return
            ''',
            '''
            end
            sub procedure procedure_name()
                dunkelCls
            return
            ''',
            '''
            gosub
            end
            ''',
            '''
            go sub procedure_name
            end
            ''',
            ]
        self.__incorrect_tests(incorrect_texts)
    
    def test_wrong_functions(self):
        incorrect_texts = [
            '''
            end
            sub procedure name(dim variable as word) as word
                let result = variable + 1
            end sub
            ''',
            '''
            end
            sub function name as word
                let result = variable + 1
            end sub
            ''',
            '''
            end
            sub function name(dim variable as word) word
                let result = variable + 1
            end sub
            ''',
            '''
            end
            function name(dim variable as word) as word
                let result = variable + 1
            end sub
            ''',
            '''
            end
            sub function name(dim variable as word) as word
                let result = variable + 1
            return
            ''',
            '''
            end
            sub function name(dim variable as word) as word
                let result = variable + 1
            end
            ''',
            '''
            function_name(variable)
            end
            ''',
            '''
            function_name(ByVal variable,)
            end
            ''',
            '''
            function_name(ByRef, variable)
            end
            ''',
            '''
            function_name
            end
            ''',
            ]
        self.__incorrect_tests(incorrect_texts)

    def test_correct_subroutines(self):
        correct_texts = [
            '''
            gosub procedure_name
            end

            sub procedure procedure_name
                dunkelCls
            return
            ''',
            '''
            function_name()
            end

            sub function function_name()
                dunkelCls
            end sub
            ''',
            '''
            function_name(ByVal variable_1, ByRef variable_2)
            end

            sub function function_name(dim variable_1 as word, dim variable_2 as word) as bool
                let result = variable_1 < variable_2
            end sub
            ''',
            ]
        self.__correct_tests(correct_texts)

if __name__ == '__main__':
    unittest.main()