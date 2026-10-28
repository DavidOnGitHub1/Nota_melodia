# Generated from lenguaje.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .lenguajeParser import lenguajeParser
else:
    from lenguajeParser import lenguajeParser

# This class defines a complete listener for a parse tree produced by lenguajeParser.
class lenguajeListener(ParseTreeListener):

    # Enter a parse tree produced by lenguajeParser#programa.
    def enterPrograma(self, ctx:lenguajeParser.ProgramaContext):
        pass

    # Exit a parse tree produced by lenguajeParser#programa.
    def exitPrograma(self, ctx:lenguajeParser.ProgramaContext):
        pass


    # Enter a parse tree produced by lenguajeParser#main.
    def enterMain(self, ctx:lenguajeParser.MainContext):
        pass

    # Exit a parse tree produced by lenguajeParser#main.
    def exitMain(self, ctx:lenguajeParser.MainContext):
        pass


    # Enter a parse tree produced by lenguajeParser#instruccion.
    def enterInstruccion(self, ctx:lenguajeParser.InstruccionContext):
        pass

    # Exit a parse tree produced by lenguajeParser#instruccion.
    def exitInstruccion(self, ctx:lenguajeParser.InstruccionContext):
        pass



del lenguajeParser