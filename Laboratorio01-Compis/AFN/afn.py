epsilon = 'ε'

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

def ThompsonAlgorithm(postfixexp):
    nfaStack = []
    cont = 1
    
    for i in postfixexp:
        #print("\nnueva vuelta ", i)
        #for s in nfaStack:
            #print(s.getDict())
        if (validChar(i)):
            #print("Se crea automata con etiqueta ", i, ":    ", cont, "---", i, "-->",cont+1)
            nfaStack.append(NFA(cont, cont+1,i))
            cont = cont + 2

        if i == "|":
            temp = NFA(cont, cont+1, epsilon)
            second = nfaStack.pop()
            first = nfaStack.pop()
            #print("Se realiza la operación OR (|) entre el automata con el dict",first.getDict(), "y el automata con dict ", second.getDict())
            temp.unionOperator(first,second)
            nfaStack.append(temp)
            cont = cont + 2

        if i == "_":
            second = nfaStack.pop()
            first = nfaStack.pop()
            #print("Se realiza la operación cocatenación (_) entre el automata con el dict",first.getDict(), "y el automata con dict ", second.getDict())
            first.concat(second)
            nfaStack.append(first)
        
        if i == "?":
            second = NFA(cont, cont+1, epsilon)
            cont = cont + 2
            first = nfaStack.pop()
            temp = NFA(cont, cont+1, epsilon)
            temp.unionOperator(first,second)
            nfaStack.append(temp)
            cont = cont + 2
            
        if i == "*":
            temp = nfaStack.pop()
            #print("Se realiza la operación closure (*) al automata con el dict",temp.getDict())
            temp.closure(cont,cont+1,epsilon)
            nfaStack.append(temp)
            cont = cont + 2
        
        if i == "+":       
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
        self.initial = initial
        self.final = final
        self.label = label
        if self.validChar(label) and final == initial + 1:
            self.createDict()
    
    def validChar(self,char):
        if char.isalpha():
            return True

        elif char.isnumeric():
            return True

        elif char == "ε":
            return True
            
        else: 
            return False

    def createCopy(self,dictionaryOriginal,lastNode):
        #print(interval)
        newDict = {}
        for i in dictionaryOriginal:
            firstKey = i
            subdict = dictionaryOriginal[firstKey]
            label = list(subdict.keys())[0]
            values = list(subdict.values())[0]
            nextValues =[]
            if type(values) == list:
                for j in values:
                    nextValues.append((lastNode+lastNode)-(lastNode-j))
                newKey = (lastNode+lastNode)-(lastNode-i)
                newDict[newKey] = {label: nextValues}
            else:
                newKey = (lastNode+lastNode)-(lastNode-i)
                nextValues.append((lastNode+lastNode)-(lastNode-values))
                newDict[newKey] = {label: nextValues[0]}
            
        self.dict = newDict

    def createDict(self):
        self.dict = {
            self.initial : {self.label: self.final}
        }
    
    def closure(self,initial,final,label):
        self.dict.update({initial: {label : [self.initial,final]}}) #X to start state and Y

        if not self.final in self.dict:
            self.dict.update({self.final : {label : [final,self.initial]}}) #accept state to Y
        else:
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
        self.initial = initial
        self.final = final        

    def concat(self,second):
        self.dict.update(second.getDict())
        new_key = self.final
        old_key = second.getInitial()
        self.dict[new_key] = self.dict.pop(old_key)
        self.final = second.getFinal()
        return "hola"
    
    def unionOperator(self,first,second):
        dictFirst = first.getDict()
        dictSecond = second.getDict()
        itemsFirst = dictFirst.items()
        itemsSecond = dictSecond.items()
        firstInitial = first.getInitial()
        secondInitial = second.getInitial()
        firstFinal = first.getFinal()
        secondFinal = second.getFinal()
        self.dict = {self.initial : {self.label:[firstInitial,secondInitial]}}
        for i in [itemsFirst,itemsSecond]:
            self.dict.update(i)
        self.dict.update({firstFinal : {self.label : self.final}})
        self.dict.update({secondFinal : {self.label : self.final}})
        return self.dict
    
    def getInitial(self):
        return self.initial

    def getFinal(self):
        return self.final

    def getDict(self):
        return self.dict

    def getLabel(self):   
        return self.label
    
    def toString(self):
        return self.initial,"--",self.label,"->",self.final