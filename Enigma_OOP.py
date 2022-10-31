import re

class Alphabet:

	def __init__(self, alphabet):
		self.alphabet = alphabet
		
		
	def rotate_left(self,list):
			x = list
			x.extend(x[0])
			x.pop(0)
			return x
	
	def rotate_right(self,list):
			x = list
			x.insert(0,x[len(x)-1])
			x.pop()
			return x
	
	def rotate_right_n(self,list, n):
			x = list
			for i in range(n):
					self.rotate_right(x)
			return x
	
	def rotate_left_n(self,list, n):
			x = list
			for i in range(n):
					self.rotate_left(x)
			return x
	
	def offset(self,n, dir):
			#dir 0 for right, 1 for left
			x = list(self.alphabet)
			
			if dir == True:
					self.rotate_left_n(x,n)
			else:
					self.rotate_right_n(x,n)
			x = "".join(x)
			self.alphabet = x
			
	def setAlpha(self, char):
		x =self.alphabet.find(char)
		self.offset(x,1)
		
	def step(self):
		self.offset(1,1)
		
	
class Rotor: 
	
	# Each rotor has a plaintext and  ciphertext Alphabet Object as its first 2 initializing parameters.
	# The ringOffset is a numeric setting that sets the plaintext alphabet off from the ciphertext alphabet.
	# The stepTrigger is the character that trips the next rotor to step one position. Once this rotor has made
	# a full revolution past the stepTrigger the next rotor advances one step.
	# The Setting is the initial position of the both of the rotor's plaintext and ciphertext alphabets. A = 0 B = 1 etc.
	# Rotor_num identifies the rotor, so that it can recognise if it is rotor 1 or not. Rotor 1 steps with each letter of encryption
	# Other rotors are triggered by eachother to advance when their stepTrigger is activated.
	
	
	def __init__(self,plain,cipher, ringOffset, stepTrigger, setting):
		self.regAlpha= "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
		self.plaintext = Alphabet(plain)
		self.ciphertext = Alphabet(cipher)
		self.ringOffset = ringOffset
		self.setting = setting
		self.stepTrigger = self.setTriggers(stepTrigger)
		self.right_neighbor = None
		self.left_neighbor = None		
		self.applyOffset(ringOffset)
		self.applyRotorSetting(setting)
		
	def setTriggers(self,stepTrigger):
		return self.regAlpha[self.regAlpha.find(stepTrigger)+1]
		
	def getSetting(self):
		return self.plaintext.alphabet[0]
	def getSettingCT(self):
		return self.ciphertext.alphabet[0]
	
	def applyOffset(self, offset):
		self.ciphertext.offset(self.ringOffset, 1)
		
	def applyRotorSetting(self, setting):
		
		indx=self.plaintext.alphabet.find(setting)
		self.plaintext.offset(indx, 1)
		self.ciphertext.offset(indx, 1)

		
	#Because the signal in an enigma machine passes through a rotor in one direction and then back 
	#through the opposite direction two input functions should exist 
	#InputA are inputs before the reflector is used.
	#InputB are inputs to the rotor after the reflector is used.
	
	
	def inputA(self, inputIndex):
		
		x = self.ciphertext.alphabet[inputIndex]
		y = self.plaintext.alphabet.find(x)
		return y
	
	def inputB(self, inputIndex):
		
		x = self.plaintext.alphabet[inputIndex]
		y = self.ciphertext.alphabet.find(x)
		return y
	

	
	
	
#Reflector Class
class Reflector(Rotor):
	def __init__(self,plain,cipher):
		self.plaintext = Alphabet(plain)
		self.ciphertext = Alphabet(cipher)
		self.right_neighbor = None
		self.left_neighbor = None

	def inputReflector(self, inputIndex):
		x = self.ciphertext.alphabet[inputIndex]
		y = self.plaintext.alphabet.find(x)
		return y
	
#Plugboard Class
	#plugboard takes in an alphabetical string and sets it to swap characters in the alphabet according to a list of tupples.
	
class Plugboard:
	
	def __init__(self, inAlpha, pairList):
		self.plaintext = inAlpha
		self.pairList = pairList
		self.ciphertext = self.swapPB()
	def swapPB(self):
		palpha = list(self.plaintext)
		
		for i in range(0,26):
			for j in self.pairList:
			
				if j[0] == palpha[i]:
					palpha[i]=j[1]
				elif j[1]==palpha[i]:
					palpha[i]=j[0]
		
		return  "".join(palpha)
			
			
	def pbinput(self, inputIndex):
		
		x = self.ciphertext[inputIndex]
		y = self.plaintext.find(x)
		return y
	
		
class Enigma:
	
	def __init__(self,rotor1,rotor2,rotor3, reflector, plugboard, message):
		self.regAlpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
		self.groupLength = 5
		self.rotor1=rotor1
		self.rotor2=rotor2
		self.rotor3=rotor3
		#self.rotor4=rotor4
		self.reflector=reflector
		self.plugboard= plugboard
		strippedMsg = re.sub(r"[^a-zA-Z ]", r"", message)
		
		self.message = strippedMsg.replace(" ","").upper()
		
		self.runMsg()
		
	
	def runMsg(self):
		
		M = self.messageToCharIndex(self.message)
		
		out = []
		for i in M:
			self.stepRotors()
			mesgChar = self.plugboard.pbinput(i)
			#4 Rotors
			#p1 = self.reflector.inputReflector(self.rotor4.inputA(self.rotor3.inputA(self.rotor2.inputA(self.rotor1.inputA(mesgChar)))))
			#p2 = self.rotor1.inputB(self.rotor2.inputB(self.rotor3.inputB(self.rotor4.inputB(p1))))
			#3rotors
			p1 = self.reflector.inputReflector(self.rotor3.inputA(self.rotor2.inputA(self.rotor1.inputA(mesgChar))))
			p2 = self.rotor1.inputB(self.rotor2.inputB(self.rotor3.inputB(p1)))
			#self.printSettings()
			out.append(self.plugboard.pbinput(p2))
		
		self.output = self.indextoMsg(out)
	def printSettings(self):
		print(f"Setting: {self.rotor3.getSetting()} {self.rotor2.getSetting()} {self.rotor1.getSetting()}")
		
	
	def stepRotors(self):
		
		self.rotor1.plaintext.step()
		self.rotor1.ciphertext.step()
		
		
		if self.rotor1.stepTrigger == self.rotor1.getSetting():
			self.rotor2.plaintext.step()
			self.rotor2.ciphertext.step()

		if self.rotor1.stepTrigger == self.rotor1.getSetting() and self.rotor2.stepTrigger == self.rotor2.getSetting():
		
			self.rotor3.plaintext.step()
			self.rotor3.ciphertext.step()

			
	def messageToCharIndex(self,msg):
		self.regAlpha
		msglst =[]
		for i in msg:
			msglst.append(self.regAlpha.find(i))
		return msglst
	
	def indextoMsg(self, lst):
		self.regAlpha
		
		msg =""
		count = 0
		for i in lst:
		
			if count % self.groupLength == 0 and count>0:
				msg+=" "
			msg += self.regAlpha[i]
			count+=1
	
		return msg
	
#-----------------------------BELOW-ENIGMA-IMPLIMENTATION-AND-INITIALIZATION-------------------------------------	
regAlpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
pblst =[["A","Z"],["E","C"],["G","S"],["Q","I"],["X","T"],["U","F"],["L","O"]];
PB= Plugboard(regAlpha, pblst)		

#Rotor settings (plain, cipher, ringOffset, stepTrigger, setting)
I =  Rotor(regAlpha,"EKMFLGDQVZNTOWYHXUSPAIBRCJ",0, "Q","T")
II = Rotor(regAlpha,"AJDKSIRUXBLHWTMCQGZNPYFVOE",0, "E","D")
III =Rotor(regAlpha,"BDFHJLCPRTXVZNYEIWGAKMUSQO",0, "V","K")

IV = Rotor(regAlpha,"ESOVPZJAYQUIRHXLNFTGKDCMWB",0, "J","A")
V =  Rotor(regAlpha,"VZBRGITYUPSDNHLXAWMJQOFECK",0, "A","A")
VI =  Rotor(regAlpha,"JPGVOUMFYQBENHZRDKASXLICTW",0, "A","A")
VII =  Rotor(regAlpha,"NZJHGRCXMYSWBOUFAIVLPEKQDT",0, "A","A")
VIII =  Rotor(regAlpha,"FKQHTLXOCBJSPDZRAMEWNIUYGV",0, "A","K")
BETA =  Rotor(regAlpha,"LEYJVCNIXWPBQMDRTAKZGFUHOS",0, "A","A")
GAMMA =  Rotor(regAlpha,"FSOKANUERHMBTIYCWLQPZXVGJD",0, "A","A")


RefA= Reflector(regAlpha,"EJMZALYXVBWFCRQUONTSPIKHGD")
RefB= Reflector(regAlpha,"YRUHQSLDPXNGOKMIEBFZCWVJAT")
RefC= Reflector(regAlpha,"FVPJIAOYEDRZXWGCTKUQSBNMHL")
RefBTH= Reflector(regAlpha,"ENKQAUYWJICOPBLMDXZVFTHRGS")
RefCTH= Reflector(regAlpha,"RDOBJNTKVEHMLFCWZAXGYIPSU")

Message = "I LOVE CRYPTOGRAPHY I REALLY DO"

enigma = Enigma(I,II,III,RefB,PB,Message)

print(f"ENCRYPTED TEXT: {enigma.output}")

I.applyRotorSetting("T")
II.applyRotorSetting("D")
III.applyRotorSetting("K")

msg2=enigma.output

enigma2 = Enigma(I,II,III, RefB, PB, msg2)

print(f"DECRYPTED TEXT: {enigma2.output}")
enigma2.printSettings()






