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
from Util import *


class miListener(compiladoresListener):
    tablaSimbolos = TS()

    def enterPrograma(self, ctx: compiladoresParser.ProgramaContext):
        print("Iniciando Compilacion".center(50, "*"))
        print(self.tablaSimbolos._pilaContexto[0]._simbolos)

    def exitPrograma(self, ctx: compiladoresParser.ProgramaContext):
        print("Compilacion Finalizada".center(50, "*"))
        print(self.tablaSimbolos._pilaContexto[0]._simbolos)

    def exitDeclaracion(self, ctx: compiladoresParser.DeclaracionContext):
        print("exitDeclaracion".center(50, "*"))

        tDato = str(ctx.getChild(0).getText())
        datos = ctx.getText()[len(tDato):]
        listaId = Util.verificarCantId(datos)
        print(listaId)

        # agregar variable a la tabla de simbolos
        for i in listaId:
            identificador = Variable(i, tDato)
            if Util.verificarInicializado(datos):
                identificador.inicializado = True
            # buscar localmente si existe la variable
            if self.tablaSimbolos.buscarIdLocal(identificador) == False:
                self.tablaSimbolos.agregarId(identificador)
                print('SE AGREGO NUEVO IDENTIFICADOR'.center(50, '-'))
            else:
                print('NO SE AGREGO NUEVO IDENTIFICADOR'.center(50, '-'))

    # Enter a parse tree produced by compiladoresParser#bloque.
    def enterBloque(self, ctx: compiladoresParser.BloqueContext):
        print(f"Iniciando PILA DE CONTEXTOS = : {TS._pilaContexto}")
        self.tablaSimbolos.agregarContexto()

    # Exit a parse tree produced by compiladoresParser#bloque.
    def exitBloque(self, ctx: compiladoresParser.BloqueContext):
        self.tablaSimbolos.borrarContexto()
        print(f"contexto borrado: {TS._pilaContexto}")

    # Exit a parse tree produced by compiladoresParser#asignacion.
    def exitAsignacion(self, ctx: compiladoresParser.AsignacionContext):
        pass

    # Exit a parse tree produced by compiladoresParser#asignacion.
    def exitAsignacion(self, ctx: compiladoresParser.AsignacionContext):
        pass
