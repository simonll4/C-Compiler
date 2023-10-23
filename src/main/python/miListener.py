from antlr4 import *
from antlr4 import tree
if "." in __name__:
    from .compiladoresParser import compiladoresParser
else:
    from compiladoresParser import compiladoresParser

from compiladoresListener import compiladoresListener

from TS import TS
from Contexto import Contexto
from ID import *


class miListener(compiladoresListener):
    tablaSimbolos = TS()

    def enterPrograma(self, ctx: compiladoresParser.ProgramaContext):
        print("Iniciando Compilacion".center(50, "*"))
        # TS.agregarContexto() # agregar contexto global
        self.tablaSimbolos.agregarContexto()

    def exitPrograma(self, ctx: compiladoresParser.ProgramaContext):
        print("Compilacion Finalizada".center(50, "*"))
        print(self.tablaSimbolos._pilaContexto)

    def exitDeclaracion(self, ctx: compiladoresParser.DeclaracionContext):
        print("exitDeclaracion".center(50, "*"))

        # # agregar variable
        # nombre = str(ctx.getChild(1).getText())
        # tDato = str(ctx.getChild(0).getText())
        # inicializado = False
        # if str(ctx.getChild(2).getText()) != '':
        #     inicializado = True
        # identificador = Variable(nombre, tDato)
        # if self.tablaSimbolos.buscarIdLocal(identificador) == False:
        #     self.tablaSimbolos.agregarId(identificador)
        # else:
        #     print("IDENTIFICADOR YA DECLARADO".center(50, '*'))
        print(ctx.toStringTree())
        print(ctx.getText())
        print(type(ctx.definicion().opal()))
        
    def exitLlamada_funcion(self, ctx:compiladoresParser.Llamada_funcionContext):
        pass