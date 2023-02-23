#definir el simbolo epsilon
EPSILON = 'ε' 
#Definir la precedencia de operadores 
precedence = {'(':0, '|':1, '_':2,'*':3,'?':3, '+':3} 
#Definir la lista de operadores
operatorsVal = ["*","_","|","?","+"]
#Definir la lista de argumentos que no son parte del alfabeto
notAlphabet = ["*","_","|","(",")","?"]

#Convertir ? y + operadores a | y *
def convertOperators(expresion):
  newExpresion=""
  for i in range(0,len(expresion)):
    if expresion[i] in ["?","+"]:
      if expresion[i] == "?":
        newExpresion = newExpresion +"|ε"
      else:
        if expresion[i-1] == ")":
              # Encontrar la operacion dentro de los parentesis que el operador * se aplica
          count = 1
          reverse = i-2
          temp = ")"
          while reverse >= 0 and count > 0:
            if expresion[reverse] == "(":
              temp = temp + "("
              count = count - 1
            elif expresion[reverse] == ")":
              temp = temp + ")"
              count = count + 1
            else:
              temp = temp + expresion[reverse]
            reverse = reverse - 1
            # Le aplica reversa a la expresion dentro de los parentesis y agrega el * operador
          tempReverse = temp [::-1]
          
          newExpresion = newExpresion + tempReverse + "*"
        else: 
          newExpresion = newExpresion + expresion[i-1] + "*"
    else:
      newExpresion = newExpresion + expresion[i]
  #si el operador ? sigue existiendo, se llama una funcion recursiva y para convertirlo
  if "?" in newExpresion:
    return convertOperators(newExpresion)
  else:
    return newExpresion

#Chequea si la expresion es válida y tiene parentesis balanceados
def firstExpresion(expresion):
  if "(" in expresion:
    if expresion.count("(") == expresion.count(")"):
      return True
    else:
      return False
  else:
    return True

# Valida que el cáracter es valido para el alfabeto 
def validChar(char):
  if char.isalpha():
    return True
  elif char.isnumeric():
    return True
  elif char == "ε":
    return True
  elif char == "#":
    return True
  else: 
    return False

#Obtiene el alfabeto de la expresión
def getAlphabet(expresion):
  alphabet = []
  for i in expresion:
    if i not in alphabet:
      if i not in operatorsVal and i not in ["(",")","ε"]:
        alphabet.append(i)
  return alphabet

# Agregue un guión bajo '_' entre caracteres y operadores para evitar la ambigüedad
def computableExpresion(expresion):
  nuevaexpresion = ""
  for i in range(0,len(expresion)):
    if i == 0:
      nuevaexpresion = nuevaexpresion + expresion[i]
    else:
      #print("toca ",expresion[i]," anterior ",expresion[i-1])
      if validChar(expresion[i-1]) and validChar(expresion[i]):
        #print("se agrega _",expresion[i])
        nuevaexpresion = nuevaexpresion + "_" + expresion[i]
      elif validChar(expresion[i-1]) and expresion[i] == "(":
        #print("se agrega _",expresion[i])
        nuevaexpresion = nuevaexpresion + "_" + expresion[i]
      elif validChar(expresion[i]) and expresion[i-1] == ")":
        #print("se agrega _",expresion[i])
        nuevaexpresion = nuevaexpresion + "_" + expresion[i]
      elif expresion[i-1] == "*" and validChar(expresion[i]):
        #print("se agrega _",expresion[i])
        nuevaexpresion = nuevaexpresion + "_" + expresion[i]
      elif expresion[i-1] == "*" and expresion[i] == "(":
        #print("se agrega _",expresion[i])
        nuevaexpresion = nuevaexpresion + "_" + expresion[i]
      elif expresion[i-1] == ")" and expresion[i] == "(":
        #print("se agrega _",expresion[i])
        nuevaexpresion = nuevaexpresion + "_" + expresion[i]
      elif expresion[i] == "?":
        nuevaexpresion = nuevaexpresion + "?"
      else:
        #print("se agrega ",expresion[i])
        nuevaexpresion = nuevaexpresion + expresion[i]
  return nuevaexpresion     
    
def isEmpty(arrayContent):
  return True if len(arrayContent) == 0 else False

def lastElement(arrayContent):
  return arrayContent[len(arrayContent)-1]

def lessThan(arrayContent,character): 
  try: 
    a = precedence[character]
    b = precedence[lastElement(arrayContent)]
    if a < b:
      return True
    elif a == b:
      return True
    else:
      return False
  except KeyError:
    return False

def infixaPostfix(exp):
  output = []
  operators = []
  for i in exp:
    #print(i)
    #print(operators)
    if validChar(i):
      output.append(i)
    else:
      if i in operatorsVal:
        while( (not isEmpty(operators)) and lessThan(operators,i)):
          output.append(operators.pop())
        operators.append(i)
      elif i == "(": 
        operators.append(i)
      elif i == ")":
        quantity = operators.count("(")
        flag = quantity
        while(not isEmpty(operators) and "(" in operators and quantity == flag):
          if ("(" == lastElement(operators)):
            operators.pop()
            flag = flag - 1
          else: 
            output.append(operators.pop())
      else:
        #print(operators)
        #print(output)
        #print(i)
        return "Error"     
  while( (not isEmpty(operators))):
    output.append(operators.pop())
  return output

def expresionParaArbol(expresion):
  nuevaexpresion = ""
  for i in range(0,len(expresion)):
    if i == 0:
      nuevaexpresion = nuevaexpresion + expresion[i]
    else:
      #print("toca ",expresion[i]," anterior ",expresion[i-1])
      if expresion[i] == "?":
        nuevaexpresion = nuevaexpresion + "|ε"
      else:
        #print("se agrega ",expresion[i])
        nuevaexpresion = nuevaexpresion + expresion[i]
  return nuevaexpresion
