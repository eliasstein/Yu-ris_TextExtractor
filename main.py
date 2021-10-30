import io,time,json
from json import encoder
import struct
import glob
import os

#key=[0xD3,0x6F,0xAC,0x96]   #Eroge
key=[0x78,0x1B,0x73,0x30]   #Euphoria

#second_xor=2                #Eroge
second_xor=4                 #Euphoria
file_root = []
ybn_bytes=[]
filebytes=[]
buffer=[]
blacklist=["es.",""]

def comprobation():
    dec=False
    for x in glob.glob("Decrypted/*.ybn"):
        filer=open(x,'rb')
        buffer=filer.read()
        for y in range(len(buffer)):
            if buffer[y]==34 and buffer[y-3]==77 and dec==False:
                print(x+" Esta bien desencriptado")
                dec=True
        if dec==False:
          filer.close()
          os.remove(x)
        dec=False
        
    xor(second_xor)

def xor(pos):
  keycont=0
  for x in glob.glob("ysbin/*.ybn"):
    if os.path.exists("Decrypted/"+x[6:])==False:
      filer=open(x,'rb')
      if filer.read(4) == b'YSTB':
          print(x) #Files ystb
          filer.seek(0)
          buffer=filer.read()
          filer.seek(0)
          for y in range(0,pos):
            filebytes.append(buffer[y])
          for y in range(pos,len(filer.read())):
              if keycont==4:
                  keycont=0
              filebytes.append(buffer[y]^key[keycont])
              keycont+=1
          keycont=0
          filew=open("Decrypted/"+x[6:],'wb+')
          filew.write(bytes(filebytes[:]))
          filew.close()
          filebytes.clear()
    
  if pos==second_xor:
    CreateJSON()
     
  comprobation()

def CreateJSON():
  data_set={}
  texts=[]
  text=""
  jpchar=[]
  error=False
  for x in glob.glob("Decrypted/*.ybn"):    #Get files from Decryped
    filer=open(x,'rb')
    buffer=filer.read()
    filer.seek(0)
    for y in range(0,len(filer.read())):    #Read File by file and byte for byte
      if buffer[y]==34 and buffer[y-1]==0 and buffer[y-3]==77:  #if find a text in the file
        y+=1
        while(buffer[y]!=34):
          #print(buffer[y])
          if ((buffer[y] >= 0x81 and buffer[y] <= 0x84) or (buffer[y] >= 0x87 and buffer[y] <= 0x9F) or (buffer[y] >= 0xE0 and buffer[y] <= 0xEA) or (buffer[y] >= 0xED and buffer[y] <= 0xEE) or (buffer[y] >= 0xFA) and buffer[y] <= 0xFC):   #Detect if is a japanese character 
            if (buffer[y+1] >= 0x40 and buffer[y+1] <= 0xFC and buffer[y+1] != 0x7F):
                jpchar.append(buffer[y])
                jpchar.append(buffer[y+1])
                #print(hex(jpchar[0])+hex(jpchar[1]))
                text+=bytearray(jpchar).decode("shift_jisx0213")          #Decode the japanese character  
                y+=1
                jpchar.clear()

          else:
            if buffer[y]<0x20:                            #if text can't be decoded add as hexadecimal
              text+=hex(buffer[y])+"||"
            else:
              text+=chr(buffer[y])
          y+=1

        if text.startswith(blacklist[0]):                 #Delete words from the blacklist
          text=""

        if error==True:                                   #Just in case
          text="ERROR_IN_THE_LINE"
          error=False


        if text!="":                                    #if text is diferent to null then add the text                                              
          texts.append(text)
          text=""
        

    data_set[x[10:]]=[texts[:]]                           #Create a dictionary with the filename like a key and the texts like the content
    texts.clear()
  file=open("Text.json",'w',encoding='shift_jisx0213')                             #Open the file .json
  json.dump(data_set,file,indent=4,ensure_ascii=False)    #Save the file
  file.close()                                            #close the json file
  menu()                                                  #load the menu again


def ReinsertText():
  f = open("Text.json",'r')
  data_set=json.load(f)
  #for x in data_set:
    #print(data_set[x][0][0:4])
  print(data_set["yst00125.ybn"][0][0])
  
  menu()
 


  

def menu():
    opcion=0
    print("1_Extract text")
    print("2_Reinsert text")

    opcion=int(input())
    if opcion==1:
        print("Extracting...")
        xor(4)
    if opcion==95:
        comprobation()
    if opcion==96:
        CreateJSON()
    if opcion==2:
        ReinsertText()




menu()