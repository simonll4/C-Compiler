import sys
from antlr4 import *
from compiladoresLexer import compiladoresLexer
from compiladoresParser import compiladoresParser
from miListener import miListener
from miVisitor import miVisitor
from util.Util import Util
import re


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

    codigoFuente = tree.getPayload().getText()
    error = re.finditer(r"missing '(.*?)'", codigoFuente)
    resultados = []
    for coincidencia in error:
        aux = coincidencia.group(1)
        resultados.append(aux)

    if Util.Error != True and len(resultados) == 0:
        visitante = miVisitor()
        visitante.visit(tree)
    elif Util.Error == True:
        print(f'ERROR SEMANTICO (ver informe listener)'.center(40, '-'))
    elif len(resultados) > 0:
        print(f'ERROR DE COMPILACION'.center(40, '-'))


if __name__ == '__main__':
    main(sys.argv)
