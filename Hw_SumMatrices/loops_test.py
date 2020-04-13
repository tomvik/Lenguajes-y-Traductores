from Parser import Parser    # The code to test
import unittest   # The test framework

class Test_TestParserLoops(unittest.TestCase):
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

    def test_wrong_while(self):
        incorrect_texts = [
            '''
            while ()
                dunkelCls
            wend
            end
            ''',
            '''
            while (variable) then
                dunkelCls
            wend
            end
            ''',
            '''
            while
                dunkelCls
            wend
            end
            ''',
            '''
            while variable
                dunkelCls
            wend
            ''',
            '''
            while (variable)
                dunkelCls
            end
            end
            ''',
            '''
            while (variable)
                dunkelCls
            end
            ''',
            ]
        self.__incorrect_tests(incorrect_texts)
    
    def test_wrong_do_until(self):
        incorrect_texts = [
            '''
            do
                dunkelCls
            loop until ()
            end
            ''',
            '''
                dunkelCls
            loop until (variable)
            end
            ''',
            '''
            do
                dunkelCls
            loop (variable)
            end
            ''',
            '''
            do
                dunkelCls
            until (variable)
            end
            ''',
            '''
            do
                dunkelCls
            loop until variable
            end
            ''',
            '''
            do
                dunkelCls
            loop until
            end
            ''',
            ]
        self.__incorrect_tests(incorrect_texts)

    def test_wrong_for(self):
        incorrect_texts = [
            '''
            for counter value to limit step delta
                dunkelCls
            next counter
            end
            ''',
            '''
            for counter = to limit step delta
                dunkelCls
            next counter
            end
            ''',
            '''
            for counter = + to limit step delta
                dunkelCls
            next counter
            end
            ''',
            '''
            for counter = value to step delta
                dunkelCls
            next counter
            end
            ''',
            '''
            for counter = value limit step delta
                dunkelCls
            next counter
            end
            ''',
            '''
            for counter = value to limit step
                dunkelCls
            next counter
            end
            ''',
            '''
            for counter = value to limit step delta
                dunkelCls
            next
            end
            ''',
            '''
            for counter = value to limit step delta
                dunkelCls
            counter
            end
            '''
            ]
        self.__incorrect_tests(incorrect_texts)

    def test_correct_loops(self):
        correct_texts = [
            '''
            while (value)
                dunkelCls
            wend
            end
            ''',
            '''
            do
                dunkelCls
            loop until (value)
            end
            ''',
            '''
            for counter = value to limit step delta
                dunkelCls
            next counter
            end
            ''',
            ]
        self.__correct_tests(correct_texts)

if __name__ == '__main__':
    unittest.main()