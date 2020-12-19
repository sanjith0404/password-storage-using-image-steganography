import numpy as np
from PIL import Image
import hashlib
from Crypto import Random
from Crypto.Cipher import AES
from base64 import b64encode, b64decode
import sys
import pathlib



class AESCipher(object):
    def __init__(self, key):
        self.block_size = AES.block_size
        self.key = hashlib.sha256(key.encode()).digest()

    def encrypt(self, plain_text):
        plain_text = self.__pad(plain_text)
        iv = Random.new().read(self.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        encrypted_text = cipher.encrypt(plain_text.encode())
        return b64encode(iv + encrypted_text).decode("utf-8")

    def decrypt(self, encrypted_text):
        encrypted_text = b64decode(encrypted_text)
        iv = encrypted_text[:self.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        plain_text = cipher.decrypt(encrypted_text[self.block_size:]).decode("utf-8")
        return self.__unpad(plain_text)

    def __pad(self, plain_text):
        number_of_bytes_to_pad = self.block_size - len(plain_text) % self.block_size
        ascii_string = chr(number_of_bytes_to_pad)
        padding_str = number_of_bytes_to_pad * ascii_string
        padded_plain_text = plain_text + padding_str
        return padded_plain_text

    @staticmethod
    def __unpad(plain_text):
        last_character = plain_text[len(plain_text) - 1:]
        return plain_text[:-ord(last_character)]





def toBinary(password):
    if type(password)==str:
        return ''.join([format(ord(i),"08b") for i in password])
    elif type(password)== bytes or type(password)==np.ndarray:
        return [format(i,"08b") for i in password]
    elif type(password)== int or type(password) == np.uint8:
        return format(password , "08b")
    else:
        raise TypeError("Input type not supported")




def ENCODE():

    try:
        imgName = input("enter the image name:")
#        imagepath = pathlib.Path.cwd() /imgName
        img = Image.open(imgName)
        img = img.convert("RGB")
        password = input("enter the password to encode:")
#        password = str(sys.argv[2])
        password = aessec.encrypt(password)
        password+="$$$"
#        print(password)
        passwordBin = toBinary(password)
        passwordBinLength = len(passwordBin) - 1
        passwordBinIndex = 0        
        width , height = img.size
        flag=0
        for x in range(10,20):
            for y in range(500):
                pixel = img.getpixel((x,y))
                r=toBinary(pixel[0])
                g=toBinary(pixel[1])
                b=toBinary(pixel[2])
                if(passwordBinLength >= passwordBinIndex):
                    r = r[:-1] + passwordBin[passwordBinIndex]                    
                    img.putpixel((x,y),(int(r,2),int(g,2),int(b,2)))
                    passwordBinIndex += 1                    
                else:
                    flag=1
                    break               
                if(passwordBinLength >= passwordBinIndex):                    
                    g = g[:-1] + passwordBin[passwordBinIndex]
                    img.putpixel((x,y),(int(r,2),int(g,2),int(b,2) ))
                    passwordBinIndex += 1                    
                else:
                    flag=1
                    break                  
                if(passwordBinLength >= passwordBinIndex):                    
                    b = b[:-1] + passwordBin[passwordBinIndex]
                    img.putpixel((x,y),(int(r,2),int(g,2),int(b,2) ))
                    passwordBinIndex += 1                    
                else:
                    flag=1
                    break
            if(flag==1):
                break
        return img
    except IOError:
        print("input errror.")
        
    
    
    
def DECODE():
    try:
        imgName = input("please enter the name of your image:") 
        img = Image.open(imgName)
        width , height = img.size
        binaryData = ""
        for x in range(10,20):
            for y in range(500):
                pixel = img.getpixel((x,y))            
                r=toBinary(pixel[0])
                g=toBinary(pixel[1])
                b=toBinary(pixel[2])
    #            print(r,g,b)
                binaryData += r[-1]
                binaryData += g[-1]
                binaryData += b[-1]            
        binarySplit = [binaryData[i : i+8] for i in range(0,len(binaryData),8)]
        decodedData = ""
        for val in binarySplit:        
            decodedData += chr(int(val,2))
            if(decodedData[-3:]=="$$$"):
                break    
        decodedData =  decodedData[:-3]
        print(decodedData)
        decryptedPassword = aessec.decrypt(decodedData)
        return decryptedPassword
        
    except IOError:
        print("input error")





if __name__ == "__main__" :
    
    while(1):
        ch = int(input("plaese enter the choice value:"))
        if(ch==1):
            key = input("please enter the key:")
            aessec=AESCipher(key)
            encodedImage =  ENCODE()
            filename = input("please enter the name of the encoded image:")
            encodedImage.save(filename)
           
        elif(ch==2):
            key = input("please enter the key used during encryption:")
            aessec=AESCipher(key)
            text = DECODE()
            print(text)
        elif(ch==3):
            break
    
    
    

