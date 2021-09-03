import os

for i in range (1,128): 
    if i != 100: ## pois nao existe o 100
    os.system('./limpa <  publicoExtraction/Publico_extraction_portuguese_comments_' + str(i) +'.html > Limpos/publico_' + str(i) + '.html')
    
    os.system('root/CORPORA_JORNAIS_PT/conversores_html-json/plc20TP1Gr14-Pub/conversorPub < Limpos/publico_' + str(i) + '.html)

    if 