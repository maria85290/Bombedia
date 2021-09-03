#
#!/usr/bin/python3

import fileinput
from os import walk
from os import system
import re

mypath="."
for (dirpath,dirnames,filenames) in walk(mypath):
   for fich in filenames:
      print(fich )
      #ao mudar de pasta pode ser necessário mudar o PREFIXO do Nome dos ficheiros a converter
      if (fich.endswith("html") and (re.match(r'Sol_extraction',fich))):
          nomeBase=re.split(r'\.',fich)
          num = re.split(r'\_',nomeBase[0])
          #print(i," ",nomeBase[0],"  -- ", num[4])
          #pode ter que se adaptado ao Nome do ficheiro (pode não ser o 4 
          #Prefixo SOL pode ser ajustado a Fonte da Extracao
          out = "SOL"+num[4]+".html"
          #print(f'/root/TOOLS/embeleza <{fich} >{out}')
          system(f'/root/TOOLS/embeleza <{fich} >{out}')
          outJ = nomeBase[0]+".json"
          #é preciso adaptar o PREFIXO a pasta destino
          #outJ = "/root/CORPORA-CRISTIANA/" + outJ
          #print(f'/root/TOOLS/Sol2NetLang  <{out} >{outJ}')
          #o Nome do  CONVERSOR tem mesmo de ser mudado
          system(f'/root/TOOLS/Sol2NetLang  <{out} >{outJ}')


