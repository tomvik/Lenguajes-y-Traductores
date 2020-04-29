from Parser import Parser    # The code to test
import unittest   # The test framework

class Test_TestParserVariablesLet(unittest.TestCase):
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

    def test_wrong_let(self):
        incorrect_texts = [
            "le variable = 5 end",
            "lt variable = 5 end",
            "et variable = 5 end",
            "l variable = 5 end",
            "e variable = 5 end",
            "t variable = 5 end",
            "variable = 5 end"
            ]
        self.__incorrect_tests(incorrect_texts)

    def test_wrong_equal(self):
        incorrect_texts = [
            "let variable 5 end",
            "let variable == 5 end",
            "let variable not 5 end",
            "let variable + 5 end",
            "let variable - 5 end"
            ]
        self.__incorrect_tests(incorrect_texts)

    def test_wrong_many_lets(self):
        incorrect_texts = [
            '''
            let variable_one = 5
            let variable_two = 
            end
            ''',
            '''
            let variable_one = 5
            let variable_two 7
            end
            ''',
            '''
            let variable_one = 5
            variable_two = 7
            end
            ''',
            '''
            let variable_one = 5
            let variable_two = 7 +
            end
            '''
        ]
        self.__incorrect_tests(incorrect_texts)

    def test_correct_let(self):
        correct_texts = [
            "let variable = 5 end",
            '''
            let variable_one = 5
            let variable_two = 7
            let variable_three = 9 + variable_one - variable_two
            end
            ''',
            '''
            let variable_one = 5
            let variable_two = variable_one
            end
            '''
        ]
        self.__correct_tests(correct_texts)


if __name__ == '__main__':
    unittest.main()