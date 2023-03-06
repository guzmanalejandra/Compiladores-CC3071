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

class leaf:
  def __init__(self,character,pos = None,c1 = None,c2=None):
    if validChar(character):
      if character =="ε":
        self.typeLeaf = "e"
        self.primerapos = []
        self.ultimapos = []
        self.anulable = True
      else:
        self.typeLeaf = "c"
        self.pos = pos
        self.primerapos = [pos]
        self.ultimapos = [pos]
        self.anulable = False
    else:
      self.typeLeaf = "o"
      self.c1 = c1
      self.c2 = c2
    self.label = character
      
  
  def setAnulable(self, flag):
    self.anulable = flag

  def setPrimeraPos (self, primerapos):
    self.primerapos = primerapos

  def setUltimaPos (self, ultimapos):
    self.ultimapos = ultimapos

  def getLabel(self):
    return self.label
  
  def getPos(self):
    return self.pos
  
  def getAnulable(self):
    return self.anulable
  
  def getUltimaPos(self):
    return self.ultimapos
  
  def getPrimeraPos(self):
    return self.primerapos
  
  def getType(self):
    return self.typeLeaf

  def getC1(self):
    return self.c1
  
  def getC2(self):
    return self.c2
  
  def toString(self):
    try:
      return "Nodo con pos ",self.pos," tiene la etiqueta ", self.label, " y anulable ",self.anulable
    except:
      return "Nodo con etiqueta ",self.label," tiene primerapos ","vacio" if len(self.primerapos) == 0 else self.primerapos, " y tiene ultimapos ","vacio" if len(self.ultimapos) == 0 else self.ultimapos, " y anulable ",self.anulable
