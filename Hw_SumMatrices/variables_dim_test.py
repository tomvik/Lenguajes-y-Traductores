from Parser import Parser    # The code to test
import unittest   # The test framework

class Test_TestParserVariablesDim(unittest.TestCase):
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

    def test_wrong_dim(self):
        incorrect_texts = [
            "di variable as word end", 
            "dm variable as word end",
            "im variable as word end",
            "d variable as word end",
            "m variable as word end",
            "i variable as word end",
            "variable as word end"
            ]
        self.__incorrect_tests(incorrect_texts)

    def test_wrong_as(self):
        incorrect_texts = [
            "dim variable a word end",
            "dim variable s word end",
            "dim variable word end"
            ]
        self.__incorrect_tests(incorrect_texts)

    def test_wrong_type(self):
        incorrect_texts = [
            "dim variable as end",
            "dim variable as wor end",
            "dim variable as d end",
            "dim variable as floa end",
            "dim variable as boo end",
            "dim variable as bol end",
            "dim variable as int end",
            ]
        self.__incorrect_tests(incorrect_texts)

    def test_wrong_dimensions(self):
        incorrect_texts = [
            "dim variable as word[] end",
            "dim variable as word[a] end",
            "dim variable as float[1 end",
            "dim variable as bool[2][a] end",
            "dim variable as word[2][3][b] end",
        ]
        self.__incorrect_tests(incorrect_texts)

    def test_wrong_many_dims(self):
        incorrect_texts = [
            '''
            dim variable as word
            di variable_1 as word
            end
            ''',
            '''
            dim variable as word
            dim variable_1 as float[1
            end
            ''',
            '''
            dim variable as word
            dim variable_1 float
            end
            '''
        ]
        self.__incorrect_tests(incorrect_texts)

    def test_correct_dim(self):
        correct_texts = [
            "dim variable as word end",
            "dim variable as float end",
            "dim variable as bool end",
            "dim variable as word[1] end",
            "dim variable as float[2] end",
            "dim variable as bool[3] end",
            "dim variable as word[1][2] end",
            "dim variable as float[2][3] end",
            "dim variable as bool[3][4] end",
            "dim variable as word[1][2][3] end",
            "dim variable as float[2][3][4] end",
            "dim variable as bool[3][4][5] end",
            '''
            dim variable as word
            dim variable_1 as float
            end
            ''',
            '''
            dim variable as word
            dim variable_1 as float[1][2][3]
            end
            '''
        ]
        self.__correct_tests(correct_texts)


if __name__ == '__main__':
    unittest.main()