from Parser import Parser    # The code to test
import unittest   # The test framework

class Test_TestParserReadAndPrint(unittest.TestCase):
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

    def test_wrong_read(self):
        incorrect_texts = [
            'dunkelRead "input the value", end',
            'dunkelRead end',
            'dunkelRead "input the value", variable_one variable_two end',
            'dunkelRead "input the value", variable_one, variable_two, end',
            'dunkelRead variable_one variable_two end',
            'dunkelRead variable_one, variable_two, end',
            'dunkelRead variable_one, "input the value", variable_two, end'
            ]
        self.__incorrect_tests(incorrect_texts)

    def test_correct_read(self):
        correct_texts = [
            'dunkelRead "input the value", variable end',
            'dunkelRead variable end',
            'dunkelRead "input the value", variable_one, variable_two end',
            'dunkelRead "variable_one", variable_two end'
            ]
        self.__correct_tests(correct_texts)

    def test_wrong_print(self):
        incorrect_texts = [
            '''
            dunkelPrint variable_one,
            end
            ''',
            '''
            dunkelPrint
            end
            ''',
            '''
            dunkelPrint "one_string" variable_one
            end
            '''
        ]
        self.__incorrect_tests(incorrect_texts)

    def test_correct_print(self):
        correct_texts = [
            '''
            dunkelPrint variable_one
            end
            ''',
            '''
            dunkelPrint "one_string", variable_one
            end
            ''',
            '''
            dunkelPrint variable_one, "one_string", variable_two
            end
            ''',
            '''
            dunkelPrint variable_one, "one_string", variable_two, "second_string"
            end
            ''',
            '''
            dunkelPrint variable_one, "one_string", 3 + 5, variable_two, "second_string"
            end
            '''
        ]
        self.__correct_tests(correct_texts)

    def test_correct_cls(self):
        correct_texts = [
            "dunkelCls end"
        ]
        self.__correct_tests(correct_texts)


if __name__ == '__main__':
    unittest.main()