import pdfplumber

d = {}   #Dicionario onde será guardado o conteudo

for n in range(1,112):
   # print()
    if (n==25 or n== 26 or n==29 or n==38 or n==42 or n==43 or n==45 or n== 60 or n==68 or n== 80 or n==91):
        pass
    else:
    

        pdf = pdfplumber.open('Youtube/TabelaFreq_Youtube_extraction_portuguese_' + str(n) + '.pdf')
        print(str(n))
        pages = pdf.pages
        page = pdf.pages[len(pages)-1]   #acede a ultima linha

        text = page.extract_text()

        palavras = text.split()
        
        #######     ---------------------------         Extrair a pencentagem -----------------
        j = 0
        for i in palavras:
            if i == "is":
                break
    
            j = j+ 1
       
        if (j == len(palavras)):
          
            page = pdf.pages[len(pages)-2]   #acede a pnultima ultima linha

            text = page.extract_text()

            palavras = text.split()
            
            j = 0

            #Extrair a pencentagem
            for i in palavras:
                if i == "is":
                    break

                j = j+ 1
           
              
        perc = palavras[j + 1]
        
        if perc == "the":
            
            page = pdf.pages[len(pages)-2]   #acede a ultima linha

            text = page.extract_text()

            palavras = text.split()
            
            j = 0

            #Extrair a pencentagem
            for i in palavras:
                if i == "is":
                    break

                j = j+ 1
           
            perc = palavras[j + 1]
        
    
        p = perc.split(".")
        percentagem = p[0]+ "," + p[1]
       
        ## -------------------------------        Extrair a fração ------------------------------
        page = pdf.pages[len(pages)-1]
        text = page.extract_text()

        palavras = text.split()
        n_ocorrencia = palavras[-8:-7][0].split('/')[0]
        n_comentarios = palavras[-8:-7][0].split('/')[1]
        
        ##Adicionar ao diconario

        d["Youtube-extraction-portuguese-" + str(n) + '.pdf'] = [n_comentarios,n_ocorrencia,percentagem]
        pdf.close()
    

import os


## Funçao recebe o dicionario no formato: {nomeFicheiro: [Nºocorrencias,percentagem]}
def gerarTabela(d):
   
    texfilename ="Resultados_NetAC_Youtube.tex"
     
    texfile = open(texfilename, 'w')
    
    texfile.write("\documentclass[11pt]{article}\n\\usepackage{graphicx}\n\\usepackage{multirow}\n\\usepackage[pdftex]{hyperref}\n\\usepackage{colortbl}")
    texfile.write("\n\\usepackage{longtable, array}\n\\usepackage[usenames,dvipsnames,svgnames,table]{xcolor}\n\\newlength\mylength")
    texfile.write("\n\\usepackage[legalpaper, landscape, margin=1in]{geometry}\n\\newcommand{\MinNumber}{0}")
    texfile.write("\\begin{document}")
    texfile.write( "\n\n")
    
    texfile.write("\\textbf {\\huge Jornal publico:}")
    texfile.write("\\newline")
    texfile.write("\\newline")
    texfile.write("\\newline")

    
   
    texfile.write("\n\n\\centering\\textbf{\\large Table  1: Sintese dos resultados por ficheiro \n}")

    texfile.write("\n\\newcommand{\MaxNumber}{0}%\n\\newcommand{\ApplyGradient}[1]{%\n\\pgfmathsetmacro{\PercentColor}{100.0*(#1-\MinNumber)/(\MaxNumber-\MinNumber)}\n\\xdef\PercentColor{\PercentColor}%\n\\cellcolor{LightSpringGreen!\PercentColor!LightRed}{#1}\n}")
    texfile.write("\n\\newcolumntype{C}[2]{>{\\centering\\arraybackslash}p{#1}}\n\\begin{center}\n\setlength")
    texfile.write("\mylength{\dimexpr\\textwidth - 1\\arrayrulewidth - 50\\tabcolsep}\n\\begin{longtable}{||C{.40\mylength}||C{.30\mylength}||C{.30\mylength}||C{.30\mylength}||}")
    texfile.write("\n\hline\n\\textbf{Nome} & \\textbf{N de Comentarios}  & \\textbf{N de ocorrencias de hate Speech} & \\textbf{Percentagem de hate Speech(\%)} \\\\\n\hline")

    #para alternar as cores das linhas
    color1 = "green!27" 			
    color2 = "green!5"
    color = color1
    
    for file in d:
        
        

        string =  '\cellcolor{' + color + '}' + file +  ' & ' + '\cellcolor{' + color + '}' + d[file][0]   + ' & ' + '\cellcolor{' + color + '}' + d[file][1] + ' & ' + '\cellcolor{' + color + '}' + d[file][2] +  ' \\\\  \hline\n  '
        
    
        #alternar as cores
        if color == color1:
            color = color2
        else:
            color = color1
        
        #escrever as linhas da tabela
        texfile.write("%s" % (string))
     

    #termina a primeira tabela
    texfile.write("\n\end{longtable}\n\end{center}\n")


    texfile.write("\end{document}")

    texfile.close()
    
    command = 'pdflatex ' + texfilename #gerar o ficheiro pdf a partir do .tex
    
    os.system(command)
    
    pdffilename = texfilename.split(".")[0] + ".pdf"
    
    return pdffilename


print(d)
#Gerar a tabela
gerarTabela(d)