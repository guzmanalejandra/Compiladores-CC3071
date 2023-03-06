
from graphviz import Digraph
class graphDirect:
    def __init__(self, acceptance, labelsDstates,name):
            dot = Digraph(name='Automata')
            dot.attr(rankdir = 'LR')
            for i in range (0,len(acceptance)):
                if acceptance[i]:
                    dot.node(str(i), str(i), shape='doublecircle')
                else:
                    dot.node(str(i), str(i))
            for i in range (0,len(labelsDstates)):
                dot.edge(str(labelsDstates[i][0]), str(labelsDstates[i][2]), str(labelsDstates[i][1]))
            dot.render('graficas/'+name+'.gv', view=True)