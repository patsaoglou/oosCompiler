import sys
from antlr4 import *
from oosLexer import oosLexer
from oosParser import oosParser
from oosListenerImplementation import oosListenerImplementation

def oos_compile(oss_src_f):

    input_stream = FileStream(oss_src_f)

    lexer = oosLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = oosParser(stream)

    tree = parser.startRule()

    oss_listener = oosListenerImplementation()
    walker = ParseTreeWalker()
    walker.walk(oss_listener, tree)

    source = oss_listener.get_oos_compiled()
    oss_listener.get_symb_structure() 
    print(source)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Invalid arguments for OSS compliler")
    else:
        oos_compile(sys.argv[1])