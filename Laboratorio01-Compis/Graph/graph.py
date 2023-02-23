#importar la clase digraph de la libreria graphviz
from graphviz import Digraph

#definir la clase grafo
class graph:

    #definir un inicializador que reciba la expresion y un objeto NFA
    def __init__(self, expresion, nfa):
        #Inicializar instancia de las variables
        self.operators = [] #Lista de los operadores usados en la expresion
        self.alphabet = [] #Lista de simbolos usados en las transiciones
        self.states = [] #Lista de estados en el Nfa
        #For para identificar operadores usados en la expresion
        for i in expresion:
            if i in ['*','_','|'] and not i in self.operators:
                self.operators.append(i)
        # Obtener el diccionadio de transiciones, estado inicial y final del Nfa 
        self.dict = nfa.getDict()
        self.initialState = nfa.getInitial()
        self.finalState = nfa.getFinal()

    #Definir un metodo para crear la lista de transiciones basada en el diccionario del NFA
    def createTransitions(self):
        self.transitions = [] #lista de transiciones en el NFA
        for i in self.dict:
            subDict = self.dict[i]
            key = list(subDict.keys())
            values = list(subDict.values())
            for j in values:
                if type(j) == list:
                    for k in j:
                        self.transitions.append([i,key[0],k])
                else:
                    self.transitions.append([i,key[0],j])
        # Identificar los estados y simbolos usados en las transiciones
        for i in self.transitions:
            if i[0] not in self.states:
                self.states.append(i[0])
            if i[2] not in self.states:
                self.states.append(i[2])
        for i in self.transitions:
            if not i[0] in self.alphabet:
                self.alphabet.append(i[0])
            if not i[2] in self.alphabet:
                self.alphabet.append(i[2])
        return self.transitions
    
    #definir un metodo para obtener la lista de estados
    def getStates(self):
        return self.alphabet

    #Metodo para crear una representacion del NFA usando graphviz
    def graphic(self, info,name):
        dot = Digraph(name='Automata') #crear un nuevo objeto graph
        dot.attr(rankdir = 'LR') #Establecer la orientación del gráfico de izquierda a derecha
        #Agregar nodos a la gráfica y los estados aceptados tienen doble circulo
        for i in range (0,len(self.alphabet)):
            if i == len(self.alphabet)-1:
                dot.node(str(self.alphabet[i]), str(self.alphabet[i]), shape='doublecircle')
            else: 
                dot.node(str(self.alphabet[i]), str(self.alphabet[i]))
        #Agregar border al gráfico según la información de la lista
        for i in range (0,len(info)):
            infoNodo = info[i]
            dot.edge(str(infoNodo[0]), str(infoNodo[2]), str(infoNodo[1]))
        # Representar el gráfico como un archivo .gv y mostrarlo    
        dot.render('graficas/'+name+'.gv', view=True)
