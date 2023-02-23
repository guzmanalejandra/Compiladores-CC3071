from graphviz import Digraph

class graph:

    def __init__(self, expresion, nfa):
        self.operators = []
        self.alphabet = []
        self.states = []
        for i in expresion:
            if i in ['*','_','|'] and not i in self.operators:
                self.operators.append(i)
        self.dict = nfa.getDict()
        self.initialState = nfa.getInitial()
        self.finalState = nfa.getFinal()

    def createTransitions(self):
        self.transitions = []
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
    
    def getStates(self):
        return self.alphabet

    def graphic(self, info,name):
        dot = Digraph(name='Automata')
        dot.attr(rankdir = 'LR')
        for i in range (0,len(self.alphabet)):
            if i == len(self.alphabet)-1:
                dot.node(str(self.alphabet[i]), str(self.alphabet[i]), shape='doublecircle')
            else: 
                dot.node(str(self.alphabet[i]), str(self.alphabet[i]))
        for i in range (0,len(info)):
            infoNodo = info[i]
            dot.edge(str(infoNodo[0]), str(infoNodo[2]), str(infoNodo[1]))
        dot.render('graficas/'+name+'.gv', view=True)
    
