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

    # Visit a parse tree produced by compiladoresParser#definicion.
    def visitDefinicion(self, ctx: compiladoresParser.DefinicionContext):
        print("visitDefinicion".center(50, '*'))
        return self.visitOpal(ctx.getChild(1))

    # Visit a parse tree produced by compiladoresParser#asignacion.
    def visitAsignacion(self, ctx: compiladoresParser.AsignacionContext):
        print("visitAsignacion".center(50, '*'))
        self.visitOpal(ctx.getChild(2))
        with ManejoArchivo("output/codigo_intermedio.txt") as archivoCI:
            archivoCI.write('\n' + ctx.getChild(0).getText() +
                            ' = ' + self.tmp.tActual)

    # Visit a parse tree produced by compiladoresParser#opal.
    def visitOpal(self, ctx: compiladoresParser.OpalContext):
        return self.visitExpresionl(ctx.getChild(0))

    # Visit a parse tree produced by compiladoresParser#expresionl.
    def visitExpresionl(self, ctx: compiladoresParser.ExpresionlContext):
        return self.visitTerminol(ctx.getChild(0))

    # Visit a parse tree produced by compiladoresParser#expl.
    def visitExpl(self, ctx: compiladoresParser.ExplContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by compiladoresParser#terminol.
    def visitTerminol(self, ctx: compiladoresParser.TerminolContext):
        return self.visitExpresion(ctx.getChild(0))

    # Visit a parse tree produced by compiladoresParser#terml.
    def visitTerml(self, ctx: compiladoresParser.TermlContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by compiladoresParser#expresion.

    def visitExpresion(self, ctx: compiladoresParser.ExpresionContext):
        print("visitExpresion".center(50, '*'))

        aux = self.visitTermino(ctx.getChild(0))
        aux2 = self.visitExp(ctx.getChild(1))
        with ManejoArchivo("output/codigo_intermedio.txt") as archivoCI:
            archivoCI.write('\n' + self.tmp.t + ' = ' + aux + ' ' +
                            ctx.getChild(1).getChild(0).getText() + ' ' + aux2)

        return self.tmp.tActual

    # Visit a parse tree produced by compiladoresParser#exp.
    def visitExp(self, ctx: compiladoresParser.ExpContext):
        print("visitExp".center(50, '*'))

        aux1 = self.visitTermino(ctx.getChild(1))
        # si el hijo 3 no contiene nada, finaliza la recursividad
        if ctx.getChild(2).getText() == '':
            return self.tmp.tActual

        aux = self.visitExp(ctx.getChild(2))
        with ManejoArchivo("output/codigo_intermedio.txt") as archivoCI:
            archivoCI.write('\n' + self.tmp.t + ' = ' + aux1 +
                            ' ' + ctx.getChild(2).getChild(0).getText() + ' ' + aux)
        return self.tmp.tActual

        # return self.visitChildren(ctx)

    # Visit a parse tree produced by compiladoresParser#opal.

    def visitOpal(self, ctx: compiladoresParser.OpalContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by compiladoresParser#expl.
    def visitExpl(self, ctx: compiladoresParser.ExplContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by compiladoresParser#termino.
    def visitTermino(self, ctx: compiladoresParser.TerminoContext):
        print("visitTermino".center(50, '*'))
        with ManejoArchivo("output/codigo_intermedio.txt") as archivoCI:
            archivoCI.write('\n' + self.tmp.t + ' = ' +
                            str(ctx.getChild(0).getText()))
        return self.visitTerm(ctx.getChild(1))

    # Visit a parse tree produced by compiladoresParser#term.
    def visitTerm(self, ctx: compiladoresParser.TermContext):

        with ManejoArchivo("output/codigo_intermedio.txt") as archivoCI:
            archivoCI.write('\n'+self.tmp.t + ' = ' + self.tmp.tAnterior +
                            ' ' + ctx.getChild(0).getText() + ' ' + ctx.getChild(1).getText())
        # si el hijo 3 no contiene nada, finaliza la recursividad
        if ctx.getChild(2).getText() == '':
            return self.tmp.tActual
        return self.visitTerm(ctx.getChild(2))

    # def visitLista_var(self, ctx:compiladoresParser.Lista_varContext):
    #     print("visitLista_var".center(50,'*'))
    #     #print("  -->  --> lista var - " + ctx.getText())
    #     return self.visitChildren(ctx)

    # # Visit a parse tree produced by compiladoresParser#factor.
    # def visitFactor(self, ctx:compiladoresParser.FactorContext):
    #     return self.visitChildren(ctx)
