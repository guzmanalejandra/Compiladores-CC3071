from infixpost.postfix import *
from AFN.afn import *
from Graph.graph import graph
from Graph.Direct import graphDirect
from Simulaciones.simulaciones import simulationNFA, simulationFDA
from subconjuntos.subsets import eCerradura, subsetsBuilder
from afddirect.statesafd import buildAFD 

#definir el simbolo epsilon
EPSILON = 'ε' 
#Definir la precedencia de operadores 
precedence = {'(':0, '|':1, '_':2,'*':3,'?':3, '+':3} 
#Definir la lista de operadores
operatorsVal = ["*","_","|","?","+"]
#Definir la lista de argumentos que no son parte del alfabeto
notAlphabet = ["*","_","|","(",")","?"]
# Definir el conjunto de elementos del alfabeto permitidos
allowed = set([chr(i) for i in range(ord('a'), ord('z')+1)] + [chr(i) for i in range(ord('A'), ord('Z')+1)] + [str(i) for i in range(10)] + [' '] + operatorsVal + notAlphabet)



if __name__ == "__main__":
    correcta = False
    while not correcta:
        
        option = input("\nSeleccione una opción:\n1. Crear AFN y luego AFD.\n2. AFD directo.\n3. Salir.\n>> ")
        if option == "3":
            print("¡Hasta luego!")
            break

        expresion = input("\nIngrese la expresión regular: ")
        if not set(expresion).issubset(allowed):
            print("Error: la expresión contiene elementos no permitidos.")
            continue
        
        if expresion == "":
            print("Error: no se ingresó ninguna expresión.")
            continue
        
                # Verificar que los paréntesis estén balanceados
        count = 0
        for char in expresion:
            if char == "(":
                count += 1
            elif char == ")":
                count -= 1
            if count < 0:
                break
        if count != 0:
            print("Error: los paréntesis no están balanceados.")
            continue
            



        if option == "1":
            print("---------- CREACIÓN AFN Y AFD ----------")
            nuevaexpresion = computableExpresion(expresion)
            postfixexp = infixaPostfix(nuevaexpresion)
            result = ThompsonAlgorithm(postfixexp)
            nfaDict = result.getDict()

            print("Expresión ingresada: ", expresion)
            print("Expresión entendible para la computadora: ", nuevaexpresion)
            print("Expresión en Postfix: ", postfixexp)
            print("Dict con el NFA resultante:\n", nfaDict)

            prueba = graph(postfixexp, result)
            transitions = prueba.createTransitions()
            prueba.graphic(transitions, "Thompson")

            s0 = result.getInitial()
            sf = result.getFinal()
            states = prueba.getStates()

            print("Nodo inicial: ", s0, "\nNodo de aceptación/final: ", sf)

            alphabet = getAlphabet(expresion)
            subsets, numberSubsets, subsetsInfo, finalNodeInside = subsetsBuilder(alphabet, states, nfaDict, s0, sf)

            prueba.graphSubsets(subsets, numberSubsets, "Subconjuntos", finalNodeInside)

        elif option == "2":
            print("---------- CREACIÓN AFD DIRECTO ----------")
            expresion = convertOperators(expresion)
            nuevaExpresionComputable = computableExpresion(expresion)
            postfixexpNueva = infixaPostfix(nuevaExpresionComputable) + ["#", "_"]
            labelsDstates, acceptance = buildAFD(postfixexpNueva)
            prueba = graphDirect(acceptance, labelsDstates, "AFD directo")
            
            print(expresion)
            print("Expresión entendible para la computadora: ", nuevaExpresionComputable)
            print("Expresion que con la que se hará el arbol sintactico ",postfixexpNueva)
            
            w = input("Ingrese la cadena a verificar si pertenece al lenguaje: ")
            if simulationFDA(w, labelsDstates, acceptance, getAlphabet(expresion)):
                print("La cadena es aceptada por el AFD.")
            else:
                print("La cadena NO es aceptada por el AFD.")
            
            
        else:
            print("Opción inválida.") 