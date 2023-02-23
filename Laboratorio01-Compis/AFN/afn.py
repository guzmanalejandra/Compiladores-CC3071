#Se define una variable global que representa el caracter epsilon
epsilon = 'ε'

#Función que valida que un caracter sea válido, es decir, que no sea un operador
def validChar(char):
    if char in ["*","?","|","_","+"]:
        return False

    elif char == "ε":
        return True

    elif char.isalpha():
        return True

    elif char.isnumeric():
        return True  

    else: 
        return False
    
#Algoritmo de Thompson que recibe como parámetro una expresión en notación postfix
def ThompsonAlgorithm(postfixexp):
    #Lista vacía que servirá de pila para guardar los autómatas que se vayan creando
    nfaStack = []
    #Variable que se utilizará para crear los nodos que conforman el autómata
    cont = 1
    
    #Se recorre la expresión postfix
    for i in postfixexp:
        #print("\nnueva vuelta ", i)
        #for s in nfaStack:
            #print(s.getDict())
        if (validChar(i)):
            #Si el caracter es válido se crea un autómata de un nodo
            #print("Se crea automata con etiqueta ", i, ":    ", cont, "---", i, "-->",cont+1)
            nfaStack.append(NFA(cont, cont+1,i))
            cont = cont + 2

        if i == "|":
            #Si se encuentra un operador OR, se sacan dos autómatas de la pila
            #y se crea un nuevo autómata que representa la unión de ambos
            temp = NFA(cont, cont+1, epsilon)
            second = nfaStack.pop()
            first = nfaStack.pop()
            #print("Se realiza la operación OR (|) entre el automata con el dict",first.getDict(), "y el automata con dict ", second.getDict())
            temp.unionOperator(first,second)
            nfaStack.append(temp)
            cont = cont + 2

        if i == "_":
            #Si se encuentra un operador concatenación, se sacan dos autómatas de la pila
            #y se crea un nuevo autómata que representa la concatenación de ambos
            second = nfaStack.pop()
            first = nfaStack.pop()
            #print("Se realiza la operación cocatenación (_) entre el automata con el dict",first.getDict(), "y el automata con dict ", second.getDict())
            first.concat(second)
            nfaStack.append(first)
        
        if i == "?":
         #Si se encuentra un operador de cero o una vez, se saca un autómata de la pila
         #y se crea un nuevo autómata que representa la operación de cero o una vez
            second = NFA(cont, cont+1, epsilon)
            cont = cont + 2
            first = nfaStack.pop()
            temp = NFA(cont, cont+1, epsilon)
            temp.unionOperator(first,second)
            nfaStack.append(temp)
            cont = cont + 2
            
        if i == "*":
            #Si se encuentra un operador de cerradura de Kleene, se saca un autómata de la pila
            #y se crea un nuevo autómata que representa la operación de cerradura de Kleene
            temp = nfaStack.pop()
            #print("Se realiza la operación closure (*) al automata con el dict",temp.getDict())
            temp.closure(cont,cont+1,epsilon)
            nfaStack.append(temp)
            cont = cont + 2
        
        if i == "+":
            #Si se encuentra un operador de una o más veces, se saca un autómata de la pila
            #y se crea un nuevo autómata que representa la operación de una o más veces       
            first = nfaStack.pop()
            finalNode = first.getFinal()
            firstNode = first.getInitial()
            second = NFA((finalNode+finalNode)-(finalNode-firstNode), finalNode+finalNode, first.getLabel())
            second.createCopy(first.getDict(),finalNode)
            cont = second.getFinal() + 1 
            second.closure(cont,cont+1, epsilon)
            cont = cont + 2
            first.concat(second)
            nfaStack.append(first)

    return nfaStack.pop()

class NFA:

    def __init__(self,initial, final, label):
        # Inicialización de la clase NFA con un estado inicial, estado final y una etiqueta (label)
        self.initial = initial
        self.initial = initial
        self.final = final
        self.label = label
        
        # Se verifica si la etiqueta es válida y si el estado final es igual al estado inicial más uno
        # Si ambas condiciones se cumplen, se crea un diccionario con el estado inicial, la etiqueta y el estado final
        if self.validChar(label) and final == initial + 1:
            self.createDict()
    
    def validChar(self,char):
        # Función para verificar si una etiqueta es válida
        # Si la etiqueta es alfabética, numérica o ε (épsilon), se considera válida
        if char.isalpha():
            return True

        elif char.isnumeric():
            return True

        elif char == "ε":
            return True
            
        else: 
            return False

    def createCopy(self,dictionaryOriginal,lastNode):
        # Función para crear una copia de un diccionario y ajustar los valores para una concatenación
        # Se recibe el diccionario original y el último nodo del NFA anterior
        #print(interval)
        newDict = {}
        for i in dictionaryOriginal:
            firstKey = i
            subdict = dictionaryOriginal[firstKey]
            label = list(subdict.keys())[0]
            values = list(subdict.values())[0]
            nextValues =[]
            if type(values) == list:
                # Si los valores son una lista, se ajustan los valores a partir del último nodo del NFA anterior
                for j in values:
                    nextValues.append((lastNode+lastNode)-(lastNode-j))
                newKey = (lastNode+lastNode)-(lastNode-i)
                newDict[newKey] = {label: nextValues}
            else:
                # Si los valores no son una lista, se ajusta el valor a partir del último nodo del NFA anterior
                newKey = (lastNode+lastNode)-(lastNode-i)
                nextValues.append((lastNode+lastNode)-(lastNode-values))
                newDict[newKey] = {label: nextValues[0]}
            
        self.dict = newDict

    def createDict(self):
        # Función para crear un diccionario con el estado inicial, la etiqueta y el estado final
        self.dict = {
            self.initial : {self.label: self.final}
        }
    
    def closure(self,initial,final,label):
         # Función para agregar una operación de cierre (épsilon-cierre)
         # Se agrega un diccionario con el estado inicial, la etiqueta y el estado final
        self.dict.update({initial: {label : [self.initial,final]}}) 

        # Si el estado final no se encuentra en el diccionario, se agrega con la etiqueta y los valores correspondientes
        if not self.final in self.dict:
            self.dict.update({self.final : {label : [final,self.initial]}}) 
        else:
             # Si el estado final ya se encuentra en el diccionario, se actualiza la etiqueta y los valores correspondientes
            x = self.dict[self.final]
            #ESTO VA A TRONAR CUANDO NO SEAN LETRAS SI NO QUE PALABRAS O NUMEROS
            # PARA SOLUCIONAR UTILIZAR LIST()
            key = x.keys()
            value = x.values()
            for i in key:
                key = i
            for i in value:
                value = i
            self.dict.update({self.final : {label : [final,self.initial], key : value}})
        
        # Se actualizan los estados inicial y final
        self.initial = initial
        self.final = final       
         
    # Metodo para concatenar dos NFAs
    def concat(self,second):
        # Se agrega el diccionario del segundo NFA al diccionario del primer NFA
        self.dict.update(second.getDict())
        # Se cambia la clave del estado final del primer NFA al estado inicial del segundo NFA
        new_key = self.final
        old_key = second.getInitial()
        self.dict[new_key] = self.dict.pop(old_key)
         # Se actualiza el estado final del primer NFA al estado final del segundo NFA
        self.final = second.getFinal()
        return "hola"
    
    #Funcion para unir dos automatas 
    def unionOperator(self,first,second):
        dictFirst = first.getDict()
        # Obtenemos los diccionarios de cada autómata
        dictSecond = second.getDict()
        # Obtenemos los items de cada diccionario
        itemsFirst = dictFirst.items()
        itemsSecond = dictSecond.items()
        # Obtenemos los estados inicial y final de cada autómata
        firstInitial = first.getInitial()
        secondInitial = second.getInitial()
        # Creamos un nuevo diccionario con el estado inicial del nuevo autómata
        firstFinal = first.getFinal()
        secondFinal = second.getFinal()
        self.dict = {self.initial : {self.label:[firstInitial,secondInitial]}}
        # Agregamos los items de cada diccionario al nuevo diccionario
        for i in [itemsFirst,itemsSecond]:
            self.dict.update(i)
        # Agregamos los estados finales de los autómatas originales al estado final del nuevo autómata
        self.dict.update({firstFinal : {self.label : self.final}})
        self.dict.update({secondFinal : {self.label : self.final}})
        # Retornamos el nuevo diccionario
        return self.dict
    #Funciones para obtener información de un autómata
    def getInitial(self):
        return self.initial

    def getFinal(self):
        return self.final

    def getDict(self):
        return self.dict

    def getLabel(self):   
        return self.label
    
    #Función para imprimir un autómata
    def toString(self):
        return self.initial,"--",self.label,"->",self.final
