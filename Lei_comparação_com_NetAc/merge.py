import os

'''
1) Vamos juntar o json inicial (com a identificação da noticia) aos json com os comentarios.
'''


for i in range(4,275):
    print(i)

    f1data = f2data = "" 
    
    with open(os.getcwd() + '/solExtraction/Sol_extraction_portuguese_' + str(i)+'.json', encoding='utf-8', errors='replace') as f1: 
        f1data = f1.read() 
        
    with open(os.getcwd() + '/convertidos_solExtraction/Sol_extraction_portuguese_comments_' + str(i)+'.json', encoding='utf-8', errors='replace') as f2: 
        f2data = f2.read()
        f2data = f2data[2:]  ## Retira aquele { que esta a mais
        
    f1data += "\n"
    f1data += f2data
    with open (os.getcwd() + '/Sol/Sol_extraction_portuguese_' + str(i)+'.json', 'a' , encoding='utf-8' ) as f3: 
        f3.write(f1data)



