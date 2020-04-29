from Parser import Parser    # The code to test
import unittest   # The test framework

class Test_TestParserConditions(unittest.TestCase):
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

    def test_wrong_if(self):
        incorrect_texts = [
            '''
            if() then
                dunkelCls
            end if
            end
            ''',
            '''
            if variable then
                dunkelCls
            end if
            end
            ''',
            '''
            if (variable)
                dunkelCls
            end if
            end
            ''',
            '''
            if (variable) then
                dunkelCls
            end
            ''',
            ]
        self.__incorrect_tests(incorrect_texts)
    
    def test_wrong_else(self):
        incorrect_texts = [
            '''
            if (variable) then
                dunkelCls
            els
                dunkelPrint "hola"
            end if
            end
            ''',
            '''
            else
                dunkelPrint "hola"
            end if
            end
            ''',
            '''
            if (variable) then
                dunkelCls
            else
                dunkelPrint "hola"
            if (variable) then
                dunkel Cls
            end if
            end
            '''
            ]
        self.__incorrect_tests(incorrect_texts)

    def test_wrong_elsif(self):
        incorrect_texts = [
            '''
            if (variable) then
                dunkelCls
            elsif () then
                dunkelPrint "hola"
            end if
            end
            ''',
            '''
            elsif (variable) then
                dunkelPrint "hola"
            end if
            end
            ''',
            '''
            if (variable) then
                dunkelCls
            else
                dunkelPrint "hola"
            elsif (variable) then
                dunkel Cls
            end if
            end
            '''
            ]
        self.__incorrect_tests(incorrect_texts)

    def test_correct_if(self):
        correct_texts = [
            '''
            if (variable) then
                dunkelPrint "in if"
            end if
            end
            ''',
            '''
            if (variable) then
                dunkelPrint "in if"
            else
                dunkelPrint "in else"
            end if
            end
            ''',
            '''
            if (variable) then
                dunkelPrint "in if"
            elsif (variable) then
                dunkelPrint "in elsif"
            else
                dunkelPrint "in else"
            end if
            end
            ''',
            '''
            if (variable) then
                dunkelPrint "in if"
            elsif (variable) then
                dunkelPrint "in first elsif"
            elsif (variable) then
                dunkelPrint "in second elsif"
            else
                dunkelPrint "in else"
            end if
            end
            ''',
            '''
            if (variable + 2 > 10) then
                dunkelPrint "in if"
            elsif (variable - 3 < 10 and not true) then
                dunkelPrint "in first elsif"
            elsif (variable == 15) then
                dunkelPrint "in second elsif"
            else
                dunkelPrint "in else"
            end if
            end
            '''
            ]
        self.__correct_tests(correct_texts)

if __name__ == '__main__':
    unittest.main()