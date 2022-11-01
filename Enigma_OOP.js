//This was changed on desktop...
class Alphabet{
	constructor(alphabet){
		this.alphabet = alphabet;
		
	}
	
	rotate_left(list){
		let x = list;
		x.push(x[0]);
		x.shift();
		return x;
	}
	
	rotate_right(list){
		let x = list;
		x.unshift(x[x.length-1]);
		x.pop();
		return x
	}
	
	rotate_right_n(list,n){
		let x = list
		for(let i=0;i<n;i++){
			this.rotate_right(x);
		}
		return x;
	}
	
	rotate_left_n(list,n){
		let x = list
		for(let i=0;i<n;i++){
			this.rotate_left(x);
		}
		return x
	}
	
	offset(n,dir){
		
		let x = this.alphabet.split("");
		
		if(dir == true){
			this.rotate_left_n(x,n);
		}else{
			this.rotate_right_n(x,n);
		}
		x = x.join("");
		this.alphabet = x;
	}
	
	setAlpha(char){
		let x = this.alphabet.indexOf(char)
		this.offset(x, 1)
	}
	
	step(){
		this.offset(1,1);
	}	
};

class Rotor{
	constructor(plain, cipher, ringOffset, stepTrigger, setting){
		this.regAlpha= "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
		this.plaintext = new Alphabet(plain);
		this.ciphertext = new Alphabet(cipher);
		this.ringOffset = ringOffset;
		this.setting = setting;
		this.stepTrigger = this.setTriggers(stepTrigger);
		this.right_neighbor = null;
		this.left_neighbor = null;
		this.applyOffset(ringOffset);
		this.applyRotorSetting(setting);
	}
	
	setTriggers(stepTrigger){
		return this.regAlpha[this.regAlpha.indexOf(stepTrigger)+1];
	}
	
	getSetting(){
		return  this.plaintext.alphabet[0];
	}
	
	getSettingCT(){
		return this.ciphertext.alphabet[0];
	}
	
	applyOffset(offset){
		this.ciphertext.offset(this.ringOffset,1);
	}
	
	applyRotorSetting(setting){
		let indx = this.plaintext.alphabet.indexOf(setting);
		this.plaintext.offset(indx, 1);
		this.ciphertext.offset(indx,1);
	}
	
	inputA(inputIndex){
		let x = this.ciphertext.alphabet[inputIndex];
		let y = this.plaintext.alphabet.indexOf(x);
		return y;
		
	}
	
	inputB(inputIndex){
		let x = this.plaintext.alphabet[inputIndex];
		let y = this.ciphertext.alphabet.indexOf(x);
		return y;

	}
	
};


class Reflector {
	
	constructor(plain,cipher){
		
		this.plaintext = new Alphabet(plain);
		this.ciphertext =  new Alphabet(cipher);
		this.right_neighbor = null;
		this.left_neighbor = null;
	}
	
	inputReflector(inputIndex){
		let x = this.ciphertext.alphabet[inputIndex]
		let y = this.plaintext.alphabet.indexOf(x)
		return y
	}
	
};

class Plugboard{
	constructor(inAlpha, pairList){
		this.plaintext = inAlpha;
		this.pairList = pairList;
		this.ciphertext = this.swapPB();
	}
	swapPB(){
		let palpha = this.plaintext.split("");
		for(let i =0;i<26;i++){
			for(let j of this.pairList){
				
				if(j[0]==palpha[i]){
					palpha[i]=j[1];
				}else if (j[1]==palpha[i]) {
					palpha[i]=j[0];
				}
			}
		}
		return palpha.join("");
	}
	
	pbinput(inputIndex){
		let x = this.ciphertext[inputIndex]
		let y = this.plaintext.indexOf(x);
		return y;
	}
};



class Enigma{
	constructor(rotor1, rotor2, rotor3,reflector, plugboard, message){
		this.regAlpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
		this.groupLength = 5;
		this.rotor1=rotor1;
		this.rotor2=rotor2;
		this.rotor3=rotor3;
		this.reflector=reflector;
		this.plugboard=plugboard;
		
		let strippedMsg = message.replace(/[^a-zA-Z]/g,'');
		
		this.message = strippedMsg.replace(/ /g,'').toUpperCase();

		this.runMsg();
	}
	
	runMsg(){
		let M = this.messageToCharIndex(this.message);
		
		let out = [];
		
		for (let i of M){
			this.stepRotors();
			let mesgChar = this.plugboard.pbinput(i);
			let p1 = this.reflector.inputReflector(this.rotor3.inputA(this.rotor2.inputA(this.rotor1.inputA(mesgChar))));
			let p2 = this.rotor1.inputB(this.rotor2.inputB(this.rotor3.inputB(p1)))
			out.push(this.plugboard.pbinput(p2));
			
			this.output = this.indextoMsg(out);
		}
	}
	
	printSettings(){
		console.log(`Setting: ${this.rotor3.getSetting()} ${this.rotor2.getSetting()} ${this.rotor1.getSetting()}`);
	}
	
	stepRotors(){
		this.rotor1.plaintext.step();
		this.rotor1.ciphertext.step();
		
		if(this.rotor1.stepTrigger == this.rotor1.getSetting()){
			this.rotor2.plaintext.step();
			this.rotor2.ciphertext.step();
		}
		
		if(this.rotor1.stepTrigger == this.rotor1.getSetting() & this.rotor2.stepTrigger == this.rotor2.getSetting()){
			this.rotor3.plaintext.step();
			this.rotor3.ciphertext.step();
		}
	}
	
	messageToCharIndex(msg){
		this.regAlpha;
		let msglst = [];
		for(let i of msg){
			msglst.push(this.regAlpha.indexOf(i));
		}
		return msglst;
	}
	
	indextoMsg(lst){
		this.regAlpha;
		
		let msg = "";
		let count = 0;
		
		for(let i of lst){
			
			if(count % this.groupLength == 0 & count >0){
				msg+=" "
			}
			msg += this.regAlpha[i];
			count+=1;
			
		}
		return msg;
	}
};


//////////////////

let regAlpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";

let pblst =[["A","Z"],["E","C"],["G","S"],["Q","I"],["X","T"],["U","F"],["L","O"]];
let PB = new Plugboard(regAlpha, pblst);

//Rotor settings (plain, cipher, ringOffset, stepTrigger, setting)
let I =  new Rotor(regAlpha,"EKMFLGDQVZNTOWYHXUSPAIBRCJ",0, "Q","T");
let II = new Rotor(regAlpha,"AJDKSIRUXBLHWTMCQGZNPYFVOE",0, "E","D");
let III = new Rotor(regAlpha,"BDFHJLCPRTXVZNYEIWGAKMUSQO",0, "V","K");

let IV = new Rotor(regAlpha,"ESOVPZJAYQUIRHXLNFTGKDCMWB",0, "J","A");
let V =  new Rotor(regAlpha,"VZBRGITYUPSDNHLXAWMJQOFECK",0, "A","A");
let VI =  new Rotor(regAlpha,"JPGVOUMFYQBENHZRDKASXLICTW",0, "A","A");
let VII = new  Rotor(regAlpha,"NZJHGRCXMYSWBOUFAIVLPEKQDT",0, "A","A");
let VIII = new  Rotor(regAlpha,"FKQHTLXOCBJSPDZRAMEWNIUYGV",0, "A","K");
let BETA =  new Rotor(regAlpha,"LEYJVCNIXWPBQMDRTAKZGFUHOS",0, "A","A");
let GAMMA = new  Rotor(regAlpha,"FSOKANUERHMBTIYCWLQPZXVGJD",0, "A","A");


let RefA= new Reflector(regAlpha,"EJMZALYXVBWFCRQUONTSPIKHGD");
let RefB= new Reflector(regAlpha,"YRUHQSLDPXNGOKMIEBFZCWVJAT");
let RefC= new  Reflector(regAlpha,"FVPJIAOYEDRZXWGCTKUQSBNMHL");
let RefBTH=new  Reflector(regAlpha,"ENKQAUYWJICOPBLMDXZVFTHRGS");
let RefCTH= new Reflector(regAlpha,"RDOBJNTKVEHMLFCWZAXGYIPSU");

let Message = "I LOVE CRYPTOGRAPHY I REALLY DO";

let enigma = new Enigma(I,II,III,RefB,PB,Message);

console.log(`ENCRYPTED TEXT: ${enigma.output}`);



I.applyRotorSetting("T");
II.applyRotorSetting("D");
III.applyRotorSetting("K");

let msg2=enigma.output;

let enigma2 = new Enigma(I,II,III, RefB, PB, msg2);

console.log(`DECRYPTED TEXT: ${enigma2.output}`);
enigma2.printSettings();





