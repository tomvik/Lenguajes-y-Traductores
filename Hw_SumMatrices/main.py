import sys
from Parser import Parser
from Executer import execute

if __name__ == "__main__":
    parser = Parser()

    if (len(sys.argv) > 1):
        program_name = sys.argv[1]
        program_file = open(program_name, "r")
        program = program_file.read().replace('\\n', '\n')
        program_file.close()
        parser.Parse(program)

        execute(parser.get_executable())
    else:
        print('''Test file not provided''')
