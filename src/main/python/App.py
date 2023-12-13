import sys
from antlr4 import *
from compiladoresLexer import compiladoresLexer
from compiladoresParser import compiladoresParser
from miListener import miListener
from miVisitor import miVisitor
from util.Util import Util


def main(argv):
    archivo = "input/decl.c"
    if len(argv) > 1:
        archivo = argv[1]
    input = FileStream(archivo)
    lexer = compiladoresLexer(input)
    stream = CommonTokenStream(lexer)
    parser = compiladoresParser(stream)
    # print(tree.toStringTree(recog=parser))
    listener = miListener()
    parser.addParseListener(listener)
    tree = parser.programa()

    if Util.Error != True:
        visitante = miVisitor()
        visitante.visit(tree)
    else:
        print(f'ERROR DE COMPILACION'.center(40, '-'))


if __name__ == '__main__':
    main(sys.argv)
