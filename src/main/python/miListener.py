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
from ManejoArchivo import *


class miListener(compiladoresListener):
    tablaSimbolos = TS()
    # borro todo lo que tenga el archivo en un principio
    with ManejoArchivo("output/tablaSimbolos.txt") as archivoTS:
        archivoTS.truncate(0)

    def enterPrograma(self, ctx: compiladoresParser.ProgramaContext):
        print("enterPrograma".center(80, "*"))

    def exitPrograma(self, ctx: compiladoresParser.ProgramaContext):
        print("exitPrograma".center(80, "*"))
        with ManejoArchivo("output/tablaSimbolos.txt") as archivoTS:
            archivoTS.write(str(self.tablaSimbolos.obtenerUltimoContexto()))

    # Enter a parse tree produced by compiladoresParser#bloque.
    def enterBloque(self, ctx: compiladoresParser.BloqueContext):
        print("enterBloque".center(80, "*"))
        self.tablaSimbolos.agregarContexto()

    # Exit a parse tree produced by compiladoresParser#bloque.
    def exitBloque(self, ctx: compiladoresParser.BloqueContext):
        print("exitBloque".center(80, "*"))
        with ManejoArchivo("output/tablaSimbolos.txt") as archivoTS:
            archivoTS.write(str(self.tablaSimbolos.obtenerUltimoContexto()))
        self.tablaSimbolos.borrarContexto()

    def exitDeclaracion(self, ctx: compiladoresParser.DeclaracionContext):
        print("exitDeclaracion".center(80, "*"))

        tDato = str(ctx.getChild(0).getText())
        datos = ctx.getText()[len(tDato):]
        listaId = Util.obtenerCantId(datos)

        # agregar ID a la tabla de simbolos
        for i in listaId:
            identificador = Variable(i, tDato)
            if Util.verificarInicializado(datos) == True:
                identificador.inicializado = True
            # buscar localmente si existe el ID
            if self.tablaSimbolos.buscarIdLocal(identificador.nombre) == False:
                self.tablaSimbolos.agregarId(identificador)
                print('SE AGREGO NUEVO IDENTIFICADOR'.center(50, '-'))
            else:
                print('NO SE AGREGO NUEVO IDENTIFICADOR'.center(50, '-'))
        print(self.tablaSimbolos._pilaContexto[0])

    # Exit a parse tree produced by compiladoresParser#asignacion.
    def exitAsignacion(self, ctx: compiladoresParser.AsignacionContext):
        print("exitAsignacion".center(80, '*'))
        datos = ctx.getText()
        listaId = Util.obtenerCantId(datos)

        # buscar globalmente si esta declarada el ID
        for nombreId in listaId:
            contexto = self.tablaSimbolos.buscarIdGlobal(nombreId)
            if contexto != False:
                print("EL INDENTIFICADOR SE ENCUENTRA DECLARADO".center(50, '-'))
                for clave in contexto.simbolos:
                    if clave == nombreId:
                        contexto.simbolos[clave].inicializado = True
            else:
                print("EL INDENTIFICADOR NO SE ENCUENTRA DECLARADO".center(50, '-'))

    # Exit a parse tree produced by compiladoresParser#prototipo_funcion.
    def exitPrototipo_funcion(self, ctx: compiladoresParser.Prototipo_funcionContext):
        print("exitPrototipo_funcion".center(80, '*'))
        tDato = str(ctx.getChild(0).getText())
        datos = ctx.getText()[len(tDato):]
        nombre = Util.obtenerNombreFuncion(datos)
        listaArs = Util.obtenerArgumentoFuncion(datos)
        identificador = Funcion(nombre, tDato, listaArs)
        if self.tablaSimbolos.buscarIdLocal(identificador.nombre) == False:
            self.tablaSimbolos.agregarId(identificador)
            print('SE AGREGO NUEVO IDENTIFICADOR'.center(50, '-'))
        else:
            print('NO SE AGREGO NUEVO IDENTIFICADOR'.center(50, '-'))

    # Exit a parse tree produced by compiladoresParser#funcion.
    def exitFuncion(self, ctx: compiladoresParser.FuncionContext):
        print("exitFuncion".center(80, '*'))
        tDato = str(ctx.getChild(0).getText())
        datos = ctx.getText()[len(tDato):]
        nombre = Util.obtenerNombreFuncion(datos)
        listaArgs = Util.obtenerArgumentoFuncion(datos)
        identificador = Funcion(nombre, tDato, listaArgs)

        # buscar identifiacor en la tabla de simbolos
        if self.tablaSimbolos.buscarIdGlobal(identificador.nombre) == True:
            # corroborar que la funcion corresponda con el prototipo
            if Util.verificarFuncionPrototipo(identificador) == True:
                print("LA IMPLEMENTACION CORRESPONDE CON EL PROTOTIPO".center(50, '-'))
            else:
                print(
                    "LA IMPLEMENTACION NO CORRESPONDE CON EL PROTOTIPO".center(50, '-'))
        # si no se encuentra en la tabla de simbolos la agrego
        else:
            self.tablaSimbolos.agregarId(identificador)
            print('SE AGREGO NUEVO IDENTIFICADOR'.center(50, '-'))

    # Exit a parse tree produced by compiladoresParser#llamada_funcion.
    def exitLlamada_funcion(self, ctx: compiladoresParser.Llamada_funcionContext):
        print("exitLlamada_funcion".center(50, '*'))
        datos = ctx.getText()
        nombreId = Util.obtenerNombreFuncion(datos)
        parametros = Util.obtenerParametrosFuncion(datos)
        # busco si esta declarada la funcion
        contextoF = self.tablaSimbolos.buscarIdGlobal(nombreId)
        # puntero al objeto ID de la funcion
        identificadorF = Util.obtenerId(contextoF, nombreId)

        # buscar el identificador de la funcion
        if contextoF != False:
            print("SE ECUENTRA EL PROTOTIPO DE LA FUNCION".center(50, '-'))
            # comprobacion de la cantidad de identifcadores en argumento y parametro
            if Util.verificarCantParametros(identificadorF, parametros):
                contador = 0
                for id in parametros:
                    contextoP = self.tablaSimbolos.buscarIdGlobal(id)
                    if contextoP != False:
                        print("SE ECUENTRA El ID DEL PARAMETRO".center(50, '-'))
                        identificadorParametro = Util.obtenerId(contextoP, id)
                        if identificadorParametro.tDato != identificadorF.args[contador].tDato:
                            print("EL TIPO DE DATO DEL PARAMETRO NO CORRESPONDE CON EL DEL ARGUMENTO DEL PROTOTIPO".center(
                                50, '-'))
                        contador += 1
                    else:
                        print("NO SE ECUENTRA El ID DEL PARAMETRO".center(50, '-'))
        else:
            print("NO SE ECUENTRA EL PROTOTIPO DE LA FUNCION".center(50, '-'))
