from compiladoresParser import compiladoresParser
from compiladoresVisitor import compiladoresVisitor
from ManejoArchivo import *
from Temporales import *


class miVisitor(compiladoresVisitor):
    tmp = Temporales()
    with ManejoArchivo("output/codigo_intermedio.txt") as archivoCI:
        archivoCI.truncate(0)

    # borro todo lo que tenga el archivo en un principio
    with ManejoArchivo("output/codigo_intermedio.txt") as archivoTS:
        archivoTS.truncate(0)

    def visitPrograma(self, ctx: compiladoresParser.ProgramaContext):
        print("visitPrograma".center(50, '*'))
        return self.visitChildren(ctx)

    def visitDeclaracion(self, ctx: compiladoresParser.DeclaracionContext):
        print("visitDeclaracion".center(50, '*'))
        self.visitDefinicion(ctx.getChild(2))
        with ManejoArchivo("output/codigo_intermedio.txt") as archivoCI:
            archivoCI.write('\n' + ctx.getChild(1).getText() +
                            ' = ' + self.tmp.tActual)

    def visitDefinicion(self, ctx: compiladoresParser.DefinicionContext):
        print("visitDefinicion".center(50, '*'))
        return self.visitOpal(ctx.getChild(1))

    def visitAsignacion(self, ctx: compiladoresParser.AsignacionContext):
        print("visitAsignacion".center(50, '*'))
        self.visitOpal(ctx.getChild(2))
        with ManejoArchivo("output/codigo_intermedio.txt") as archivoCI:
            archivoCI.write('\n' + ctx.getChild(0).getText() +
                            ' = ' + self.tmp.tActual)

    def visitOpal(self, ctx: compiladoresParser.OpalContext):
        return self.visitExpresionl(ctx.getChild(0))

    def visitExpresionl(self, ctx: compiladoresParser.ExpresionlContext):
        return self.visitTerminol(ctx.getChild(0))

    def visitExpl(self, ctx: compiladoresParser.ExplContext):
        return self.visitChildren(ctx)

    def visitTerminol(self, ctx: compiladoresParser.TerminolContext):
        return self.visitExpresion(ctx.getChild(0))

    def visitTerml(self, ctx: compiladoresParser.TermlContext):
        return self.visitChildren(ctx)

    def visitFactor(self, ctx: compiladoresParser.FactorContext):
        if ctx.getChild(0).getText() == '(':
            return self.visitExpresionl(ctx.getChild(1))
        return self.visitChild(0).getText()

    def visitExpresion(self, ctx: compiladoresParser.ExpresionContext):
        print("visitExpresion".center(50, '*'))

        aux = self.visitTermino(ctx.getChild(0))
        if ctx.getChild(1).getText() != '':
            aux2 = self.visitExp(ctx.getChild(1))
            with ManejoArchivo("output/codigo_intermedio.txt") as archivoCI:
                archivoCI.write('\n' + self.tmp.t + ' = ' + aux + ' ' +
                                ctx.getChild(1).getChild(0).getText() + ' ' + aux2)
        return self.tmp.tActual

    # Visit a parse tree produced by compiladoresParser#exp.
    def visitExp(self, ctx: compiladoresParser.ExpContext):
        print("visitExp".center(50, '*'))

        aux1 = self.visitTermino(ctx.getChild(1))

        # caso base recursividad
        # si el hijo 3 no contiene nada, finaliza la recursividad
        if ctx.getChild(2).getText() == '':
            return self.tmp.tActual

        # se registra en archivo la suma o resta de los temporales que corresponde a
        # a cada expresion
        aux = self.visitExp(ctx.getChild(2))
        with ManejoArchivo("output/codigo_intermedio.txt") as archivoCI:
            archivoCI.write('\n' + self.tmp.t + ' = ' + aux1 +
                            ' ' + ctx.getChild(2).getChild(0).getText() + ' ' + aux)
        return self.tmp.tActual

        # return self.visitChildren(ctx)

    def visitTermino(self, ctx: compiladoresParser.TerminoContext):
        print("visitTermino".center(50, '*'))
        # corrobora si el factor es una expresion encerrada entre parentesis
        if ctx.getChild(0).getChild(0).getText() == '(':
            b = self.visitFactor(ctx.getChild(0))
            if ctx.getChild(1).getText() != '':
                a = self.visitTerm(ctx.getChild(1))
                with ManejoArchivo("output/codigo_intermedio.txt") as archivoCI:
                    archivoCI.write('\n' + self.tmp.t + ' = ' + b + ' ' +
                                    ctx.getChild(1).getChild(0).getText() + ' ' + a)

        else:
            with ManejoArchivo("output/codigo_intermedio.txt") as archivoCI:
                archivoCI.write('\n' + self.tmp.t + ' = ' +
                                str(ctx.getChild(0).getText()))
            if ctx.getChild(1).getText() != '':
                return self.visitTerm(ctx.getChild(1))
        return self.tmp.tActual

    def visitTerm(self, ctx: compiladoresParser.TermContext):
        # corrobora si el factor es una expresion encerrada entre parentesis
        if ctx.getChild(1).getChild(0).getText() == '(':
            self.visitFactor(ctx.getChild(1))

        # si no crea un temporal y hace la operacion temporal anterior y el nuevo numero
        # grabar en archivo tnuevo = tanterior + valor
        else:
            with ManejoArchivo("output/codigo_intermedio.txt") as archivoCI:
                archivoCI.write('\n' + self.tmp.t + ' = ' + self.tmp.tAnterior +
                                ' ' + ctx.getChild(0).getText() + ' ' + ctx.getChild(1).getText())
        # caso base recursividad
        # si el hijo 3 no contiene nada, finaliza la recursividad
        if ctx.getChild(2).getText() == '':
            return self.tmp.tActual
        return self.visitTerm(ctx.getChild(2))
