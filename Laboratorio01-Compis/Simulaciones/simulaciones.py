# Función eCerradura: implementa la operación de e-cerradura
# Recibe un diccionario (representación de un NFA), un nodo final, y un nodo
# Retorna los estados alcanzables desde el nodo dado, incluyendo transiciones ε


def eCerradura(dictionary, finalNode, node):
     # Si el nodo dado es el nodo final, no se realiza ninguna acción
    if not finalNode == node:
        falseStates = []
        # Si el nodo es una lista de estados, se agrega cada estado a falseStates
        if type(node) == list:
            for i in node:
                falseStates.append(i)
        else:
            falseStates.append(node)
        # Se itera sobre cada estado en falseStates
        for i in falseStates:
            if not i == finalNode:
                # Se obtiene el diccionario de transiciones para el estado i
                subDict = dictionary[i]
                key = list(subDict.keys())
                 # Si la primera clave es ε, se agrega cada valor como estado alcanzable
                if key[0] == "ε":
                    values = list(subDict.values())[0]
                    if type(values) == list:
                        for k in values:
                            if k not in falseStates:
                                falseStates.append(k)
                    else:
                        if values not in falseStates:
                            falseStates.append(values)
        # Retorna la lista de estados alcanzables desde el nodo dado
        return falseStates

# Función move: implementa la operación de mover
# Recibe un diccionario (representación de un NFA), un nodo final, un conjunto de estados,
# y una etiqueta de transición
# Retorna los estados alcanzables desde el conjunto de estados dado, utilizando la etiqueta dada
def move(dictionary,finalNode,states,label):
    #print("move con los estados ",states," y la etiqueta ", label)
    result=[]
      # Se itera sobre cada estado en el conjunto de estados dado
    for i in states:
        if not i == finalNode:
            # Se obtiene el diccionario de transiciones para el estado i
            subDict = dictionary[i]
            key = list(subDict.keys())[0]
            # Si la clave coincide con la etiqueta de transición, se agrega el valor a result
            if key == label:
                values = list(subDict.values())[0]
                if type(values) == list:
                    for k in values:
                        result.append(k)
                else:
                    result.append(values)
    # Se aplica e-cerradura a cada estado en result, y se agrega el resultado a un conjunto temporal
    temp = []
    #print("e-cerradura con los estados: ",result)
    for i in result:
        temp.append(eCerradura(dictionary,finalNode,i))
    for i in temp:
        if type(i) == list:
             # Si el resultado es una lista de estados, se itera sobre cada estado y se agrega a result
            for j in i:
                result.append(j)
        elif i == None:
            # Si el resultado es None, no se realiza ninguna acción
            pass
        else:
            # Si el resultado es un solo estado, se agrega a result
            result.append(i)
     # Retorna el conjunto de estados alcanzables desde el conjunto de estados dado, utilizando la etiqueta dada
    #print("Los estados resultantes fueron: ", result)
    return list(set(result))

# Función simulationNFA: implementa la simulación de un NFA
# Recibe un diccionario (representación de un NFA), un estado inicial, un estado final,

def simulationNFA(dictionary, initial, final, expresion, alphabet):
    S = []
    # Se inicializa la lista de estados
    S.append(sorted(eCerradura(dictionary,final,initial)))
    # Se agrega a la lista el estado inicial del NFA y su correspondiente e-cerradura
    #print("Se parte desde el estado ",S[0],"\nla expresion es: ",expresion)
    # Se inicializa un contador para ir agregando estados a la lista S
    cont = 0
    # Se recorre la cadena de entrada
    for i in expresion:
        # Si el caracter pertenece al alfabeto del NFA
        if i in alphabet:
            # Se agrega a la lista S el estado obtenido al hacer la transición con el caracter i y su correspondiente e-cerradura
            S.append(sorted(move(dictionary,final,S[cont],i)))
            cont = cont +1 
            # Si el caracter no pertenece al alfabeto del NFA, se devuelve "No"
        else: 
            return "No"

