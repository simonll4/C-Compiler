from compiladoresParser import compiladoresParser
from compiladoresVisitor import compiladoresVisitor
from util.ManejoArchivo import *
from util.Etiquetas import *


class miVisitor(compiladoresVisitor):
    tmp = Etiquetas()
    with ManejoArchivo("output/codigo_intermedio.txt") as archivoCI:
        archivoCI.truncate(0)

    def visitPrograma(self, ctx: compiladoresParser.ProgramaContext):
        print("visitPrograma".center(50, '*'))
        return self.visitChildren(ctx)

    def visitInstruccion(self, ctx: compiladoresParser.InstruccionContext):
        return self.visitChildren(ctx)

    def visitDeclaracion(self, ctx: compiladoresParser.DeclaracionContext):
        print("visitDeclaracion".center(50, '*'))

        if ctx.getChild(2).getText() != '':
            self.visitDefinicion(ctx.getChild(2))
            with ManejoArchivo("output/codigo_intermedio.txt") as archivoCI:
                archivoCI.write(
                    '\n' + ctx.getChild(1).getText() + ' = ' + self.tmp.tActual())

        if ctx.getChild(3).getText() != '':
            self.visitLista_var(ctx.getChild(3))

    def visitDefinicion(self, ctx: compiladoresParser.DefinicionContext):
        print("visitDefinicion".center(50, '*'))
        return self.visitOpal(ctx.getChild(1))

    def visitAsignacion(self, ctx: compiladoresParser.AsignacionContext):
        print("visitAsignacion".center(50, '*'))
        self.visitOpal(ctx.getChild(2))
        with ManejoArchivo("output/codigo_intermedio.txt") as archivoCI:
            archivoCI.write('\n' + ctx.getChild(0).getText() +
                            ' = ' + self.tmp.tActual())

    def visitLista_var(self, ctx: compiladoresParser.Lista_varContext):
        print("visitLista_var".center(50, '*'))

        # si la variable tiene definicion, escribir el codigo intermedio
        if ctx.getChild(2).getText() != '':
            self.visitDefinicion(ctx.getChild(2))
            with ManejoArchivo("output/codigo_intermedio.txt") as archivoCI:
                archivoCI.write(
                    '\n' + ctx.getChild(1).getText() + ' = ' + self.tmp.tActual())

        # chequeo si hay mas variables en lista
        if ctx.getChild(3).getText() != '':
            self.visitLista_var(ctx.getChild(3))

    def visitIf_stmt(self, ctx: compiladoresParser.If_stmtContext):
        aux = self.visitOpal(ctx.getChild(2))
        with ManejoArchivo("output/codigo_intermedio.txt") as archivoCI:
            archivoCI.write(
                f'\n{ctx.getChild(0).getText()} {aux} jmp {self.tmp.l()}')
            archivoCI.write(f'\njmp {self.tmp.l()}')
            archivoCI.write(f'\nlabel {self.tmp.lAnterior()}')
        self.visitInstruccion(ctx.getChild(4))

        # en caso de que haya else
        if ctx.getChildCount() == 6:
            with ManejoArchivo("output/codigo_intermedio.txt") as archivoCI:
                archivoCI.write(f'\njump {self.tmp.l()}')
            self.visitElse_stmt(ctx.getChild(5))

        with ManejoArchivo("output/codigo_intermedio.txt") as archivoCI:
            archivoCI.write(f'\nlabel {self.tmp.lActual()}')

    def visitElse_stmt(self, ctx: compiladoresParser.Else_stmtContext):
        with ManejoArchivo("output/codigo_intermedio.txt") as archivoCI:
            archivoCI.write(f'\nlabel {self.tmp.lAnterior()}:')
        return self.visitBloque(ctx.getChild(1))

    def visitFor_stmt(self, ctx: compiladoresParser.For_stmtContext):

        # se resuelve la asignacion de la variable de iteracion del bucle
        self.visitAsignacion(ctx.getChild(2))

        # se escribe la etiqueta para mantenerse en bucle
        with ManejoArchivo("output/codigo_intermedio.txt") as archivoCI:
            archivoCI.write(f'\nlabel {self.tmp.l()}')

        # se obtiene el temporal que tiene la condicion del ciclo
        condicion = self.visitOpal(ctx.getChild(4))

        with ManejoArchivo("output/codigo_intermedio.txt") as archivoCI:
            archivoCI.write(f'\nifnot {condicion} jmp {self.tmp.l()}')

        # se resuelve el bloque de codigo del bucle
        self.visitInstruccion(ctx.getChild(8))
        # se resuelve el incremento del bucle
        self.visitAsignacion(ctx.getChild(6))

        # etiqueta de salto para volver a tomar el bucle
        # etiqueta de salteo de bucle
        with ManejoArchivo("output/codigo_intermedio.txt") as archivoCI:
            archivoCI.write(f'\njmp {self.tmp.lAnterior()}')
            archivoCI.write(f'\nlabel {self.tmp.lActual()}')

    def visitWhile_stmt(self, ctx: compiladoresParser.While_stmtContext):
        # se escribe la etiqueta para mantenerse en bucle
        with ManejoArchivo("output/codigo_intermedio.txt") as archivoCI:
            archivoCI.write(f'\nlabel {self.tmp.l()}')

        # se obtiene el temporal que tiene la condicion del ciclo
        condicion = self.visitOpal(ctx.getChild(2))

        with ManejoArchivo("output/codigo_intermedio.txt") as archivoCI:
            archivoCI.write(f'\nifnot {condicion} jmp {self.tmp.l()}')

        # se resuelve el bloque de codigo del bucle
        self.visitInstruccion(ctx.getChild(4))

        # etiqueta de salto para volver a tomar el bucle
        # etiqueta de salteo de bucle
        with ManejoArchivo("output/codigo_intermedio.txt") as archivoCI:
            archivoCI.write(f'\njmp {self.tmp.lAnterior()}')
            archivoCI.write(f'\nlabel {self.tmp.lActual()}')

    def visitRetornar(self, ctx: compiladoresParser.RetornarContext):
        return self.visitChildren(ctx)

    def visitLlamada_funcion(self, ctx: compiladoresParser.Llamada_funcionContext):
        return self.visitChildren(ctx)

    def visitArgs_recibido(self, ctx: compiladoresParser.Args_recibidoContext):
        return self.visitChildren(ctx)

    def visitLista_args_recibido(self, ctx: compiladoresParser.Lista_args_recibidoContext):
        return self.visitChildren(ctx)

    def visitArgs_enviado(self, ctx: compiladoresParser.Args_enviadoContext):
        return self.visitChildren(ctx)

    def visitLista_args_enviado(self, ctx: compiladoresParser.Lista_args_enviadoContext):
        return self.visitChildren(ctx)

    def visitFuncion(self, ctx: compiladoresParser.FuncionContext):
        return self.visitChildren(ctx)

    def visitOpal(self, ctx: compiladoresParser.OpalContext):
        print("visitOpal".center(50, '*'))
        return self.visitExpresionl(ctx.getChild(0))

    def visitExpresionl(self, ctx: compiladoresParser.ExpresionlContext):
        print("visitExpresionl".center(50, '*'))

        aux1 = self.visitTerminol(ctx.getChild(0))
        if ctx.getChild(1).getText() != '':
            aux2 = self.visitExpl(ctx.getChild(1))
            with ManejoArchivo("output/codigo_intermedio.txt") as archivoCI:
                archivoCI.write('\n' + self.tmp.t() + ' = ' + aux1 + ' ' +
                                ctx.getChild(1).getChild(0).getText() + ' ' + aux2)
        return self.tmp.tActual()

    def visitExpl(self, ctx: compiladoresParser.ExplContext):
        print("visitExpl".center(50, '*'))

        aux1 = self.visitTerminol(ctx.getChild(1))
        # caso base recursividad
        # si el hijo 3 no contiene nada, finaliza la recursividad
        if ctx.getChild(2).getText() == '':
            return self.tmp.tActual()

        # se registra en archivo la suma o resta de los temporales que corresponde a
        # a cada expresion
        aux = self.visitExpl(ctx.getChild(2))
        with ManejoArchivo("output/codigo_intermedio.txt") as archivoCI:
            archivoCI.write('\n' + self.tmp.t + ' = ' + aux1 +
                            ' ' + ctx.getChild(2).getChild(0).getText() + ' ' + aux)
        return self.tmp.tActual()

    def visitTerminol(self, ctx: compiladoresParser.TerminolContext):
        print("visitTerminol".center(50, '*'))

        if ctx.getChildCount() == 4:
            aux1 = self.visitExpresion(ctx.getChild(0))
            aux2 = self.visitExpresion(ctx.getChild(2))
            aux3 = self.tmp.t()
            with ManejoArchivo("output/codigo_intermedio.txt") as archivoCI:
                archivoCI.write('\n' + aux3 + ' = ' + aux1 + ' ' +
                                ctx.getChild(1).getChild(0).getText() + ' ' + aux2)
            if ctx.getChild(3).getText() != '':
                aux4 = self.visitTerml(ctx.getChild(3))
                with ManejoArchivo("output/codigo_intermedio.txt") as archivoCI:
                    archivoCI.write('\n' + self.tmp.t() + ' = ' + aux3 + ' ' +
                                    ctx.getChild(3).getChild(0).getText() + ' ' + aux4)
            return self.tmp.tActual()

        elif ctx.getChildCount() == 2:
            aux1 = self.visitExpresion(ctx.getChild(0))
            if ctx.getChild(1).getText() != '':
                aux2 = self.visitTerml(ctx.getChild(1))
                with ManejoArchivo("output/codigo_intermedio.txt") as archivoCI:
                    archivoCI.write('\n' + self.tmp.t() + ' = ' + aux1 + ' ' +
                                    ctx.getChild(1).getChild(0).getText() + ' ' + aux2)
            return self.tmp.tActual()
        return self.visitExpresion(ctx.getChild(0))

    def visitTerml(self, ctx: compiladoresParser.TermlContext):
        print("visitTerml".center(50, '*'))
        return self.visitExpresionl(ctx.getChild(1))

    def visitFactor(self, ctx: compiladoresParser.FactorContext):
        print("visitFactor".center(50, '*'))
        if ctx.getChild(0).getText() == '(':
            return self.visitExpresionl(ctx.getChild(1))
        return self.visitChild(0).getText()

    def visitExpresion(self, ctx: compiladoresParser.ExpresionContext):
        print("visitExpresion".center(50, '*'))

        aux = self.visitTermino(ctx.getChild(0))
        if ctx.getChild(1).getText() != '':
            aux2 = self.visitExp(ctx.getChild(1))
            with ManejoArchivo("output/codigo_intermedio.txt") as archivoCI:
                archivoCI.write('\n' + self.tmp.t() + ' = ' + aux + ' ' +
                                ctx.getChild(1).getChild(0).getText() + ' ' + aux2)
        return self.tmp.tActual()

    # Visit a parse tree produced by compiladoresParser#exp.
    def visitExp(self, ctx: compiladoresParser.ExpContext):
        print("visitExp".center(50, '*'))
        aux1 = self.visitTermino(ctx.getChild(1))
        # caso base recursividad
        # si el hijo 3 no contiene nada, finaliza la recursividad
        if ctx.getChild(2).getText() == '':
            return self.tmp.tActual()
        # se registra en archivo la suma o resta de los temporales que corresponde a
        # a cada expresion
        aux = self.visitExp(ctx.getChild(2))
        with ManejoArchivo("output/codigo_intermedio.txt") as archivoCI:
            archivoCI.write('\n' + self.tmp.t() + ' = ' + aux1 +
                            ' ' + ctx.getChild(2).getChild(0).getText() + ' ' + aux)
        return self.tmp.tActual()

    def visitTermino(self, ctx: compiladoresParser.TerminoContext):
        print("visitTermino".center(50, '*'))
        # corrobora si el factor es una expresion encerrada entre parentesis
        if ctx.getChild(0).getChild(0).getText() == '(':
            b = self.visitFactor(ctx.getChild(0))
            if ctx.getChild(1).getText() != '':
                a = self.visitTerm(ctx.getChild(1))
                with ManejoArchivo("output/codigo_intermedio.txt") as archivoCI:
                    archivoCI.write('\n' + self.tmp.t() + ' = ' + b + ' ' +
                                    ctx.getChild(1).getChild(0).getText() + ' ' + a)
        else:
            with ManejoArchivo("output/codigo_intermedio.txt") as archivoCI:
                archivoCI.write('\n' + self.tmp.t() + ' = ' +
                                str(ctx.getChild(0).getText()))
            if ctx.getChild(1).getText() != '':
                return self.visitTerm(ctx.getChild(1))
        return self.tmp.tActual()

    def visitTerm(self, ctx: compiladoresParser.TermContext):
        print("visitTerm".center(50, '*'))

        # corrobora si el factor es una expresion encerrada entre parentesis
        if ctx.getChild(1).getChild(0).getText() == '(':
            self.visitFactor(ctx.getChild(1))
        # si no crea un temporal y hace la operacion temporal anterior y el nuevo numero
        # grabar en archivo tnuevo = tanterior + valor
        else:
            with ManejoArchivo("output/codigo_intermedio.txt") as archivoCI:
                archivoCI.write('\n' + self.tmp.t() + ' = ' + self.tmp.tAnterior() +
                                ' ' + ctx.getChild(0).getText() + ' ' + ctx.getChild(1).getText())
        # caso base recursividad
        # si el hijo 3 no contiene nada, finaliza la recursividad
        if ctx.getChild(2).getText() == '':
            return self.tmp.tActual()
        return self.visitTerm(ctx.getChild(2))
