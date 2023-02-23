from infixpost.postfix import *
from AFN.afn import *
from Graph.graph import graph
from Simulaciones.simulaciones import simulationNFA


if __name__ == "__main__":
    correcta = False
    while not correcta:
        option = input("\nDesea: 1.Crear AFN .Salir\n>>")
        if not option == "2":
            expresion = input ("\nIngrese la expresión, por favor: ")
            if firstExpresion(expresion):
                if option == "1":
                    print("---------- CREACIÓN AFN  ----------")
                    nuevaexpresion = computableExpresion(expresion)
                    print("Expresion ingresada: ",expresion)
                    print("Expresion entendible para computadora: ",nuevaexpresion)
                    postfixexp = infixaPostfix(nuevaexpresion)
                    print("Expresion en Postfix:",postfixexp)
                    result = ThompsonAlgorithm(postfixexp)
                    nfaDict = result.getDict()
                    print("Dict con el NFA resultante:\n",nfaDict) 
                    prueba = graph(postfixexp,result)
                    transitions = prueba.createTransitions()
                    prueba.graphic(transitions,"Thompson")
                    s0 = result.getInitial()
                    sf = result.getFinal()
                    states = prueba.getStates()
                    print("Nodo inicial: ",s0,"\nNodo de aceptación/final: ",sf)
                    alphabet = getAlphabet(expresion)
                    dictTrans = result.getDict()
                    simulation = True
                    while simulation:
                        option = input ("¿Desea realizar otra simulacion?\n1.Sí   2.No\n>> ")
                        if option == "1":
                            simulation = False
                else:
                    print("Opcion equivocada")
            else: 
                print("La expresion tiene errores")
        else: 
            correcta = True
            print("Gracias por utilizarme. :D")
