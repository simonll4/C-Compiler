from antlr4 import *
if "." in __name__:
    from .compiladoresParser import compiladoresParser
else:
    from compiladoresParser import compiladoresParser

from compiladoresListener import compiladoresListener

from tabla_simbolos.TS import TS
from tabla_simbolos.Contexto import Contexto
from tabla_simbolos.ID import *
from util.Util import *
from util.ManejoArchivo import *


class miListener(compiladoresListener):
    tablaSimbolos = TS()

    # reiniciar archivo de tabla de simbolos
    with ManejoArchivo("output/listener/tablaSimbolos.txt") as archivoTS:
        archivoTS.truncate(0)
    # reiniciar archivo que contiene el informe del listener
    with ManejoArchivo("output/listener/informeListener.txt") as archivoInforme:
        archivoInforme.truncate(0)

    def enterPrograma(self, ctx: compiladoresParser.ProgramaContext):
        with ManejoArchivo("output/listener/informeListener.txt") as archivoInforme:
            archivoInforme.write('\n' + f'enterPrograma'.center(40, '*'))

    def exitPrograma(self, ctx: compiladoresParser.ProgramaContext):
        with ManejoArchivo("output/listener/informeListener.txt") as archivoInforme:
            archivoInforme.write('\n' + f'exitPrograma'.center(40, '*'))

        with ManejoArchivo("output/listener/tablaSimbolos.txt") as archivoTS:
            archivoTS.write(str(self.tablaSimbolos.obtenerUltimoContexto()))

    # Enter a parse tree produced by compiladoresParser#bloque.
    def enterBloque(self, ctx: compiladoresParser.BloqueContext):
        with ManejoArchivo("output/listener/informeListener.txt") as archivoInforme:
            archivoInforme.write(
                '\n' + f'enterBloque (nuevo contexto creado)'.center(40, '*'))
        self.tablaSimbolos.agregarContexto()

        if Util.implFuncion:
            for identificador in Util.listaArgs:
                # buscar localmente si existe el ID para declararlo en su contexto
                # si no existe se agrega a la tabla de simbolos del contexto
                if self.tablaSimbolos.buscarIdLocal(identificador.nombre):
                    with ManejoArchivo("output/listener/informeListener.txt") as archivoInforme:
                        archivoInforme.write(
                            '\n' + f'NO SE AGREGO EL IDENTIFICADOR {identificador.nombre}'.center(30, '-'))
                else:
                    self.tablaSimbolos.agregarId(identificador)
                    with ManejoArchivo("output/listener/informeListener.txt") as archivoInforme:
                        archivoInforme.write(
                            '\n' + f'SE AGREGO NUEVO IDENTIFICADOR {identificador.nombre}'.center(30, '-'))

    def exitBloque(self, ctx: compiladoresParser.BloqueContext):
        with ManejoArchivo("output/listener/informeListener.txt") as archivoInforme:
            archivoInforme.write(
                '\n' + f'exitBloque(contexto borrado)'.center(40, '*'))

        with ManejoArchivo("output/listener/tablaSimbolos.txt") as archivoTS:
            archivoTS.write(str(self.tablaSimbolos.obtenerUltimoContexto()))
        self.tablaSimbolos.borrarContexto()

    def exitDeclaracion(self, ctx: compiladoresParser.DeclaracionContext):
        with ManejoArchivo("output/listener/informeListener.txt") as archivoInforme:
            archivoInforme.write('\n' + f'exitDeclaracion'.center(40, '*'))

        # se guarda tipo de dato
        tDato = str(ctx.getChild(0).getText())
        # se obtiene lista de los ID declarados
        # se obitene lista de booleano que indican que id esta inicializado
        # el orden de las listas es el mismo para las dos

        listaId = Util.obtenerIdVariables(ctx.getText()[len(tDato):])
        listaInicializados = Util.verificarInicializado(
            ctx.getText()[len(tDato):])

        # agregar obejto ID a la tabla de simbolos
        for indice, id in enumerate(listaId):
            identificador = Variable(id, tDato)
            identificador.inicializado = listaInicializados[indice]
            # buscar localmente si existe el ID para declararlo en su contexto
            # si no existe se agrega a la tabla de simbolos del contexto
            if self.tablaSimbolos.buscarIdLocal(identificador.nombre):
                with ManejoArchivo("output/listener/informeListener.txt") as archivoInforme:
                    archivoInforme.write(
                        '\n' + f'NO SE AGREGO EL IDENTIFICADOR [{id}]'.center(30, '-'))
            else:
                self.tablaSimbolos.agregarId(identificador)
                with ManejoArchivo("output/listener/informeListener.txt") as archivoInforme:
                    archivoInforme.write(
                        '\n' + f'SE AGREGO NUEVO IDENTIFICADOR [{id}]'.center(30, '-'))

    def exitAsignacion(self, ctx: compiladoresParser.AsignacionContext):
        with ManejoArchivo("output/listener/informeListener.txt") as archivoInforme:
            archivoInforme.write('\n' + f'exitAsginacion'.center(40, '*'))
        # se obtiene ID al que se le asigna algo
        listaId = Util.obtenerIdVariables(ctx.getText())
        # buscar globalmente si esta declarada el ID para asignarle nuevo valor
        for nombreId in listaId:
            contexto = self.tablaSimbolos.buscarIdGlobal(nombreId)
            if contexto:
                with ManejoArchivo("output/listener/informeListener.txt") as archivoInforme:
                    archivoInforme.write('\n' + f'NUEVA ASIGNACION A [{nombreId}]'.center(
                        30, '-'))
                # buscar el ID en el contexto y poner en True la bandera inicializado
                for clave in contexto.simbolos:
                    if clave == nombreId:
                        contexto.simbolos[clave].inicializado = True
            else:
                with ManejoArchivo("output/listener/informeListener.txt") as archivoInforme:
                    archivoInforme.write('\n' + f'EL INDENTIFICADOR [{nombreId}] NO SE ENCUENTRA DECLARADO'.center(
                        50, '-'))

    def exitPrototipo_funcion(self, ctx: compiladoresParser.Prototipo_funcionContext):
        with ManejoArchivo("output/listener/informeListener.txt") as archivoInforme:
            archivoInforme.write(
                '\n' + f'exitPrototipo_funcion'.center(40, '*'))
        tDato = str(ctx.getChild(0).getText())
        datos = ctx.getText()[len(tDato):]
        nombre = Util.obtenerNombreFuncion(datos)
        listaArs = Util.obtenerArgumentoFuncion(datos)
        identificador = Funcion(nombre, tDato, listaArs)

        if self.tablaSimbolos.buscarIdLocal(identificador.nombre):
            with ManejoArchivo("output/listener/informeListener.txt") as archivoInforme:
                archivoInforme.write(
                    '\n' + f'IDENTIFICADOR [{identificador.nombre}] YA DECLARADO'.center(30, '-'))
        else:
            self.tablaSimbolos.agregarId(identificador)
            with ManejoArchivo("output/listener/informeListener.txt") as archivoInforme:
                archivoInforme.write(
                    '\n' + f'SE AGREGO IDENTIFICADOR [{nombre}]'.center(30, '-'))

    def enterFuncion(self, ctx: compiladoresParser.FuncionContext):
        with ManejoArchivo("output/listener/informeListener.txt") as archivoInforme:
            archivoInforme.write('\n' + f'enterFuncion'.center(40, '*'))
        Util.implFuncion = True

    # Exit a parse tree produced by compiladoresParser#funcion.
    def exitFuncion(self, ctx: compiladoresParser.FuncionContext):
        with ManejoArchivo("output/listener/informeListener.txt") as archivoInforme:
            archivoInforme.write('\n' + f'exitFuncion'.center(40, '*'))
        tDato = str(ctx.getChild(0).getText())
        nombre = Util.obtenerNombreFuncion(ctx.getText()[len(tDato):])
        listaArgs = Util.obtenerArgumentoFuncion(ctx.getText()[len(tDato):])
        identificador = Funcion(nombre, tDato, listaArgs)
        Util.implFuncion = False

        # buscar identifiacor en la tabla de simbolos
        if self.tablaSimbolos.buscarIdGlobal(identificador.nombre):
            # corroborar que la funcion corresponda con el prototipo
            if Util.verificarFuncionPrototipo(identificador):
                with ManejoArchivo("output/listener/informeListener.txt") as archivoInforme:
                    archivoInforme.write(
                        '\n ' + f'LA IMPLEMENTACION {identificador.nombre} CORRESPONDE CON EL PROTOTIPO'.center(30, '-'))
            else:
                with ManejoArchivo("output/listener/informeListener.txt") as archivoInforme:
                    archivoInforme.write(
                        '\n' + f'LA IMPLEMENTACION {identificador.nombre} NO CORRESPONDE CON EL PROTOTIPO'.center(30, '-'))
        # si no se encuentra en la tabla de simbolos agrego el identificador de la funcion
        else:
            self.tablaSimbolos.agregarId(identificador)
            with ManejoArchivo("output/listener/informeListener.txt") as archivoInforme:
                archivoInforme.write(
                    '\n' + f'SE AGREGO EL INDENTIFICADOR [{identificador.nombre}]'.center(30, '-'))

    def exitArgs_recibido(self, ctx: compiladoresParser.Args_recibidoContext):
        with ManejoArchivo("output/listener/informeListener.txt") as archivoInforme:
            archivoInforme.write('\n' + f'exitArgs_recibido'.center(40, '*'))
        Util.listaArgs = Util.obtenerArgumentoFuncion(ctx.getText())

    def exitLlamada_funcion(self, ctx: compiladoresParser.Llamada_funcionContext):
        with ManejoArchivo("output/listener/informeListener.txt") as archivoInforme:
            archivoInforme.write('\n' + f'exitLlamada_funcion'.center(40, '*'))
        datos = ctx.getText()
        nombreId = Util.obtenerNombreFuncion(datos)
        parametros = Util.obtenerParametrosFuncion(datos)
        # busco si esta declarada la funcion
        contextoF = self.tablaSimbolos.buscarIdGlobal(nombreId)

        # buscar el identificador de la funcion
        if contextoF:
            # puntero al objeto ID de la funcion
            identificadorF = Util.obtenerId(contextoF, nombreId)
            with ManejoArchivo("output/listener/informeListener.txt") as archivoInforme:
                archivoInforme.write(
                    '\n'+f'SE ECUENTRA DECLARADA LA FUNCION [{nombreId}]'.center(30, '-'))
            # comprobacion de la cantidad de identifcadores en argumento y parametro
            Util.verificarParametros(identificadorF, parametros)
        else:
            with ManejoArchivo("output/listener/informeListener.txt") as archivoInforme:
                archivoInforme.write(
                    f'LA FUNCION [{nombreId}] NO ESTA DECLARADA'.center(30, '-'))
