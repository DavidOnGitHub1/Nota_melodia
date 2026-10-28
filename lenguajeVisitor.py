# Generated from lenguaje.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .lenguajeParser import lenguajeParser
else:
    from lenguajeParser import lenguajeParser

# This class defines a complete generic visitor for a parse tree produced by lenguajeParser.

class lenguajeVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by lenguajeParser#programa.
    def visitPrograma(self, ctx:lenguajeParser.ProgramaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by lenguajeParser#main.
    def visitMain(self, ctx:lenguajeParser.MainContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by lenguajeParser#instruccion.
    def visitInstruccion(self, ctx:lenguajeParser.InstruccionContext):
        return self.visitChildren(ctx)



del lenguajeParser