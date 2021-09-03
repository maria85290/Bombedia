import os

for i in range (1,128): 
    if i != 100: ## pois nao existe o 100
     os.system('./limpa <  publicoExtraction/Publico_extraction_portuguese_comments_' + str(i) +'.html > Limpos/publico_' + str(i) + '.html')

