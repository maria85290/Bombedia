# -*- coding: utf-8 -*-

import os
#os.system('python3 -m pip install tensorflow')
#import tensorflow as tf
#from tensorflow.keras.preprocessing.text import Tokenizer
#from tensorflow.keras.preprocessing.sequence import pad_sequences
#from tensorflow.keras.models import load_model
import numpy as np
import pandas as pd
import json
  


'''
json_file = open('model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
model = tf.keras.models.model_from_json(loaded_model_json)
# load weights into new model
model.load_weights("model.h5")

'''
def evaluation_tool(input_text):
    
	
	print("Inicio da avaliação")
	
	model = load_model(os.getcwd()+ '/Models/ltsm')
 
 
	df = pd.read_csv('data_train.txt', sep='\n')
	data_train = df['juntao irmao'].values.tolist()
	data_train.append('juntao irmao')

	#convert list to ndarray of 1D
	data_train = np.array(data_train)  

	tokenizer = Tokenizer(num_words = 5000)

	sentiment = ['Negativo','Positivo', 'Neutro']
 
	tokenizer.fit_on_texts(data_train)
	sequence = tokenizer.texts_to_sequences([input_text])
	test = pad_sequences(sequence, maxlen = 200)
	print(sentiment[np.around(model.predict(test), decimals = 0).argmax(axis = 1)[0]])
	return (sentiment[np.around(model.predict(test), decimals = 0).argmax(axis = 1)[0]])

def read_json():
	
    d = {}
	

    for n in range(1,112):
	# print()
        if (n==25 or n== 26 or n==29 or n==38 or n==42 or n==43 or n==45 or n== 60 or n==68 or n== 80 or n==91 ):
        	pass
        else:
			# Opening JSON file
            f = open('Youtube_Portuguese/Youtube_extraction_portuguese_' + str(n) + '.json', encoding='utf8')
            data = json.load(f)
            inputText = data['header']['title']
            d[n] = [data['header']['title'],inputText]    
                    
    return d

#d = read_json ()  ## Retorna um dicionario que associa ao nome de cada ficheiro do publico o texto associado ao subtitulo.

def avaliar(d):
    dic = {}

    for i in d:
        resultado = evaluation_tool (d[i][1])
        dic[i] = [d[i][0],resultado]  ## associa ao número de cada ficheiro o resultado da ferramenta de avaliação

    ## O proximo passo é: ler a tabela pdf com os resultados já extraidos do netLang

    import pdfplumber
    import pandas as pd


    pdf = pdfplumber.open('Resultados_NetAC_Youtube.pdf')

    tabela = [] # guarda a tabela numa lista.

    print(dic[1])

    for i in range(4):
        p1 = pdf.pages[i]
        table = p1.extract_table()

        for j in table:
            tabela.append(j)

    print(tabela)

    dic_final = {}

    for l in tabela[1:]:
            aux = l[0].split(".")[0].split("-")  ## aceder ao número
            if dic[int(aux[-1])][1]  == "Neutro":
                r = "Não"
            else:
                r = "Sim"

            dic_final[dic[int(aux[-1])][0]] = [l[1], r, l[3], dic[int(aux[-1])][1] ]
    print(dic_final)
    return 0

## d = read_json()
## dic_final = avaliar(d)



## Funçao recebe o dicionario no formato: {nomeFicheiro: [percentagem hate, resultado avaliação app bombmedia]}
def gerarTabela(d):
   
    texfilename ="TabelaYoutube.tex"
     
    texfile = open(texfilename, 'w')
    
    texfile.write("\documentclass[11pt]{article}\n\\usepackage{graphicx}\n\\usepackage{multirow}\n\\usepackage[pdftex]{hyperref}\n\\usepackage{colortbl}")
    texfile.write("\n\\usepackage{longtable, array}\n\\usepackage[usenames,dvipsnames,svgnames,table]{xcolor}\n\\newlength\mylength")
    texfile.write("\n\\usepackage[legalpaper, landscape, margin=1in]{geometry}\n\\newcommand{\MinNumber}{0}")
    texfile.write("\\begin{document}")
    texfile.write( "\n\n")
    
    texfile.write("\\textbf {\\huge Youtube:}")
    texfile.write("\\newline")
    texfile.write("\\newline")
    texfile.write("\\newline")

    
   
    texfile.write("\n\n\\centering\\textbf{\\large Tabela  1: Síntese dos resultados por ficheiro \n}")

    texfile.write("\n\\newcommand{\MaxNumber}{0}%\n\\newcommand{\ApplyGradient}[1]{%\n\\pgfmathsetmacro{\PercentColor}{100.0*(#1-\MinNumber)/(\MaxNumber-\MinNumber)}\n\\xdef\PercentColor{\PercentColor}%\n\\cellcolor{LightSpringGreen!\PercentColor!LightRed}{#1}\n}")
    texfile.write("\n\\newcolumntype{C}[2]{>{\\centering\\arraybackslash}p{#1}}\n\\begin{center}\n\setlength")
    texfile.write("\mylength{\dimexpr\\textwidth - 1\\arrayrulewidth - 50\\tabcolsep}\n\\begin{longtable}{||C{.40\mylength}||C{.20\mylength}||C{.20\mylength}||C{.30\mylength}||C{.20\mylength}||}")
    texfile.write("\n\hline\n\\textbf{Título}   &  \\textbf{Nº de Comentários}   &  \\textbf{Hate Speech(\%) (Resultado NetAC)}  &  \\textbf{Resultado Bombedia}  &  \\textbf{Controverso} \\\\\n\hline")

    #para alternar as cores das linhas
    color2= "red!20" 	
    color22 = "red!30" 
    color1 = "green!27"
    color11 = "green!18"

    color = color2

    for title in d:

        ## Substituir a virgula da string por um ponto para puder ser interpretada como float

        perc_hate = d[title][2].split(",")
        per = perc_hate[0]

        # Definir as cores
        if ((float(d[title][0]) > 30 or float(per) >= 1) and d[title][1] == "Sim") or ((float(d[title][0]) < 30 or float(per) < 1) and d[title][1] == "Não"):
            if color == color1:
                color = color11 
            else:
                color = color1

        else:
            if color == color2:
                color = color22
            else:
                color = color2
        
        string =  '\cellcolor{' + color + '}' + title +  ' & ' + '\cellcolor{' + color + '}' + d[title][0]   + ' & ' + '\cellcolor{' + color + '}' + d[title][2] +  ' & ' + '\cellcolor{' + color + '}' + d[title][3] + ' & ' + '\cellcolor{' + color + '}' + d[title][1] + ' \\\\  \hline\n  '
        
        
        
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

#print(dic_final)

#### PARA RETIR ASSENTOS E Não DAR ERRO AO GERAR PDF LATEX DA TABELA
new_dic = {}

dic_final ={'  O Interrogatório a Fernanda Câncio Ex Namorada de José Sócrates - Especial CMTV - 22 Abril 2018 ': ['59', 'Não', '0,9921', 'Neutro'], 
' A seguir aos ciganos, Brasileiros são o maior alvo de descriminação em Portugal ': ['155', 'Sim', '1,4893', 'Negativo'], ' André Ventura visita Quinta da Fonte e ignora os ciganos... ': ['319', 'Sim', '1,8509', 'Negativo'], ' FAMILIA CIGANA IMPEDIDA DE JANTAR NUM RESTAURANTE ': ['139', 'Não', '1,667', 'Neutro'], ' Almeirim - Este concelho não é para ciganos ': ['77', 'Sim', '2,4209', 'Negativo'], ' Racismo em Portugal ': ['426', 'Sim', '1,9299', 'Negativo'], ' Os Pretos Todos Daqui Para Fora! ': ['451', 'Sim', '1,8257', 'Negativo'], ' Tabu Brasil: Mudança de Sexo (Dublado) - Documentário National Geographic ': ['277', 'Não', '1,3985', 'Neutro'], ' Mulher faz cirurgia para virar homem ': ['310', 'Sim', '1,4461', 'Positivo'], '  Mesquita Nunes desmascarou as mentiras do Bloco e Mariana Mortágua entrou em desespero ': ['108', 'Sim', '1,2544', 'Positivo'], ' Maria Capaz entrevista Fernanda Câncio ': ['40', 'Sim', '2,0765', 'Negativo'], 'Fernanda Câncio TVI Jornal das 8 12-05-16 ': ['7', 'Sim', '3,4653', 'Negativo'],
 'Mariana Mortagua perde as estribeiras quando Mesquita Nunes compara o Bloco a Marine Le Pen ': ['382', 'Sim', '0,5618', 'Positivo'], 'ÁRABE PORCO E COVARDE BATENDO NA NOIVA': ['429', 'Sim', 
'1,5164', 'Positivo'], 'Crianças Transgênero DE SUA OPINIÃO': ['333', 'Sim', '0,8992', 'Negativo'], 
'Você decidiu ser menina? - Transgênero na infância (OFICIAL)': ['10442', 'Não', '0,9384', 'Neutro'], 'SOU TRANS, MAS A CIRURGIA NÃO ME FEZ MAIS MULHER | PAPO KABELO COM KAROL PINHEIRO | Salon Line': ['1312', 'Sim', '1,4085', 'Negativo'], 
'O casal transgênero em que o pai deu à luz um menino': ['211', 'Não', '3,2193', 'Neutro'], 'A saga de ter um filho transgênero': ['54', 'Sim', '0,793', 'Negativo'], "Ex-gay que tirou o pênis explica por que foi fácil se tornar 'homem hétero'": ['5391', 'Não', '1,6146', 'Neutro'], 'Domingo Espetacular conta o drama de quem se arrependeu de mudar de sexo': ['4655', 'Não', '1,0523', 'Neutro'], "Menino que mudará de gênero e nome faz planos: 'Quero ter marido e 3 filhas'": ['314', 'Não', '0,7344', 'Neutro'], 'Profissão Repórter - Transgêneros - 01 08 2018': ['114', 'Sim', '1,385', 'Negativo'], ' Miguel Neto no bairro da Jamaica, Portugal [Webnivel 95] ': ['357', 'Não', '0,7711', 'Neutro'],
 ' Em Portugal não há racismo, há racismozinho :: Inferno T4 Ep.5 ': ['1125', 'Sim', '2,0671', 'Negativo'], ' Racista fala que homem nenhum gosta de Negra. ': ['1367', 'Sim', '3,2168', 'Negativo'], ' Mulher é presa em flagrante por racismo. ': ['1572', 'Sim', '3,9361', 'Positivo'], ' BALANÇO GERAL - Racismo e prisão! PM negro é chamado de macaco ': ['543', 'Sim', '4,3715', 'Positivo'], 
 ' Mulher racista pratica atos de racismo contra os Africanos durante a manifestação ': ['39', 'Sim', '2,6114', 'Positivo'], ' Racismo cigano no você na TV  quintino Aires rassita cristina ferreira racista ': ['158', 'Sim', '1,9827', 'Positivo'], ' Racismo de ciganos no Lumiar ': ['69', 'Sim', '1,8484', 'Negativo'], ' Negra vai em protesto Neonazista e se encontra com membro da Klu Klux Klan [Legendado Português] ': ['899', 'Sim', '1,9975', 'Positivo'], 
 " 'Se for negro, não entra': Polícia italiana impede refugiados de embarcar em trem para Alemanha ": ['574', 'Sim', '1,2255', 'Positivo'], ' Adolf Hitler fala sobre os Judeus e os Aliados. ': ['1163', 'Sim', '0,667', 'Negativo'], ' 5 Frases de Adolf Hitler ': ['2511', 'Sim', '0,5226', 'Positivo'], 
 ' Mulher é presa em flagrante após usar termos racistas contra gerente de supermercado ': ['3861', 'Sim', '4,1268', 'Positivo'], ' O anti-Papa: Governo Bolsonaro quer espionar igrejas católicas ': ['228', 'Sim', '0,9688', 'Negativo'], ' A apresentadora de rádio Katie Hopkins humilha protestantes anti-Trump ': ['62', 'Sim', '0,5324', 'Negativo'], ' Preconceito contra Pobre!!! Absurdo dos absurdos!!! ': ['147', 'Sim', '0,7468', 'Positivo'], ' Comentário RACISTA de Lula. ': ['216', 'Sim', '4,2659', 'Negativo'], ' Ciganos portugueses no Brasil ': ['32', 'Sim', '1,6293', 'Negativo'], ' bairro sao joao de deus...tarrafal ': ['99', 'Não', '0,8828', 'Neutro'], ' Desacatos entre CIGANOS e PRETOS 2010 08 28 ': ['20', 'Sim', '1,0753', 'Negativo'], ' Dois ciganos são executados na porta de casa no bairro Soledade - BALANÇO GERAL ': ['70', 'Não', '2,4062', 'Neutro'], ' CMTV mostra vídeo do tiroteio em Lisboa ': ['48', 'Sim', '2,1088', 'Negativo'], ' Mais uma criança retirada a família de etnia cigana ': ['16', 'Sim', '2,8205', 'Negativo'], ' Zézinho só estava a fazer uma ganza, levou na boca (Ameixoeira) ': ['1016', 'Sim', '1,6603', 'Negativo'], ' José Berardo mudou estatutos da associação à revelia dos credores para defender interesses pessoais ': ['97', 'Não', '0,5004', 'Neutro'], ' Mariana Mortágua mais uma vez humilhada por Leitão Amaro ': ['51', 'Sim', '0,5249', 'Negativo'], 
 ' Cláudio Ramos PASSA-SE DA CABEÇA COM COLEGAS EM DIRETO - Junho 2018 ': ['104', 'Não', '0,8543', 'Neutro'], ' Cláudio Ramos Arrasa famosos que defenderam Júlia Palha ': ['67', 'Sim', '0,6757', 'Negativo'], ' Maria Leal hoje aqui só para ti- Você na TV ': ['220', 'Sim', '1,1324', 'Negativo'], ' Maria Leal e o desafio de cultura geral - 5 Para a Meia Noite ': ['300', 'Sim', '0,6114', 'Negativo'], ' DENTISTA DROGADA, BÊBADA, RACISTA E HOMOFÓBICA ': ['12', 'Sim', '3,3473', 'Negativo'], ' Maria Leal acusada de roubo Responde e é Arrasada ': ['59', 'Sim', '1,9745', 'Positivo'], ' Sérgio Henriques Responde a Acusações de Maria Leal (Ex Namorada) no Manhã CMTV 04.01.2017 ': ['70', 'Sim', '2,2046', 'Negativo'], 
 ' MARIA LEAL | O AMOR É CEGO...SURDO E DESDENTADO ': ['67', 'Não', '1,3975', 'Neutro'], ' Briga no autocarro em Portugal com um velho racista ': ['65', 'Sim', '3,9568', 'Positivo'], 'Portuguese fights /police fights/ range Portuguese compilation 🇵🇹': ['105', 'Reati  vo', '1,6958', 'Negativo'], ' TOUR PELO MEU CORPO TRANS + antes e depois ': ['1831', 'Sim', '0,9323', 'Negativo'], 
 ' Mudanças de sexo que ficaram INCRÍVEIS ': ['3167', 'Não', '1,9726', 'Neutro'], ' Racismo entre Portugal e Angola,a 3ª guerra mundial vai começar ': ['658', 'Sim', '1,7485', 'Positivo'], ' SIC - Bairros Sociais e violência em Portugal ': ['33', 'Sim', '0,2805', 'Negativo'], ' PORTUGAL FUNDADOR MUNDIAL DO RACISMO E COMERCIO DE ESCRAVO -ANGOLANOS DAM RESPOSTA A PORTUGAL ': ['296', 'Não', '1,3373', 'Neutro'], " 'Somos negros. Portugal ainda não dá valor como gente' ": ['256', 'Sim', '1,0941', 'Negativo'], ' O Racismo em Portugal existe? Como enfrentá lo? ': ['51', 'Sim', '0,9989', 'Negativo'], ' Racismo ao vivo em plena televisão portuguesa SIC ': ['14', 'Não', '2,0548', 'Neutro'], ' Ataque racista dentro de avião gera críticas à companhia aérea ': ['140', 'Sim', '3,7453', 'Positivo'], " Piruka: 'Não acho as ganzas o lado negro! Mas nunca dei um risco de coca!' ": ['89', 'Sim', '0,5691', 'Positivo'], ' TOY FUMA UM CHARRO NA TVI ': ['217', 'Sim', '0,511', 'Negativo'], ' travesti e abusado e deixado na mão ': ['5280', 'Sim', '1,0535', 'Negativo'], ' Sensivelmente Idiota - Concorda com o acolhimento de refugiados em Portugal? ': ['379', 'Sim', '0,584', 'Positivo'], ' Imigrante brasileiro é contra a vinda de refugiados para Portugal ': ['294', 'Sim', '0,6618', 'Negativo'], ' A feia verdade sobre os Refugiados em Portugal ': ['171', 'Sim', '0,5094', 'Negativo'], ' Refugiados venezuelanos deixam Roraima e chegam a São Paulo ': ['1971', 'Não', '0,4789', 'Neutro'], ' Refugiados em Portugal ': ['5', 'Sim', '3,6036', 'Negativo'], ' Refugiado$ ganham mai$ que os Portugueses ': ['7', 'Não', '0,3846', 'Neutro'], " 'refugiados' fogem de Portugal ": ['18', 'Sim', '0,4975', 'Negativo'], ' PNR - CONTRA CHEGADA DE REFUGIADOS A PORTUGAL ': ['152', 'Sim', '0,5234', 'Negativo'], 'Refugiados em Portugal': ['4', 'Sim', '0,0', 'Negativo'], ' REFUGIADO EM PORTUGAL ': ['7', 'Sim', '0,8333', 'Negativo'], " 'Refugiados' Vs Portugueses (reformados, sem-abrigo, etc) ": ['29', 'Sim', '0,3727', 'Negativo'], " 'refugiados' fogem, mas os Portugueses PAGAM regresso ": ['13', 'Sim', '0,6006', 'Negativo'], 
 ' refugiado viola Portuguesa ': ['23', 'Sim', '1,1096', 'Negativo'], ' Refugiados reconstroem a vida em Portugal ': ['22', 'Sim', '0,0', 'Negativo'], ' A questão dos refugiados na Europa ': ['29', 'Sim', '0,5476', 'Negativo'], ' O drama dos refugiados sírios e africanos que chegam a Calais, França ': ['6', 'Não', '0,0', 'Neutro'], ' Refugiados em Portugal - Muçulmanos, Informações, Árabes, Abandono e nova vida ': ['245', 'Sim', '0,442', 'Negativo'], ' A crise de refugiados: Amnistia Portugal @RTP1 ': ['26', 'Sim', 
'0,2352', 'Positivo'], ' Portugal refugiados a chegar ': ['7', 'Não', '0,7812', 'Neutro'], " Em Portugal: 'refugiado' eritreu violou uma mulher sem-abrigo de 67 anos ": ['38', 'Sim', '0,6897', 'Negativo'], ' Na Europa, Jean Wyllys está dizendo que é Refugiado do Brasil. ': ['488', 'Sim', '1,1894', 'Negativo'], " Estes são os 'refugiados' que a Europa recebe diariamente ": ['193', 'Sim', '0,4984', 'Negativo'], ' Muçulmanos de segunda geração estão completamente integrados em Portugal ': ['77', 'Sim', '0,5199', 'Negativo'], ' Pedidos de asilo aumentam em Portugal ': ['54', 'Sim', '0,927', 'Negativo'], 
' Portugueses em Angola vivem bem mas não gostam dos pretos no país deles ': ['2928', 'Não', '0,9834', 'Neutro'], ' NA SOMBRA DO PECADO - As Testemunhas de Jeová no documentário da TV de Portugal ': ['51', 'Sim', '0,2237', 'Positivo'], ' Os portugueses são racista? (xenófobo) (Brazucas em Portugal) ': ['67', 'Sim', '0,9893', 'Negativo'], ' COMO AS MULHERES BRASILEIRAS SÃO VISTAS EM PORTUGAL? ': ['493', 'Sim', '1,0802', 'Negativo']}

#from unidecode import unidecode

#for title in dic_final:
 #   new_dic[(unidecode(title))] = dic_final[title]

new_dic = dic_final    

gerarTabela (new_dic)

### Para contar o número de posts bem e mal classificados

bem = 0
mal = 0

for l in new_dic:
    perc_hate = new_dic[l][2].split(",")
    per = perc_hate[0]
    
    if ((float(new_dic[l][0]) > 30 or float(per) >= 1) and new_dic[l][1] == "Sim") or ((float(new_dic[l][0]) < 30 or float(per) < 1) and new_dic[l][1] == "Não"):
        bem = bem + 1
    else:
        mal = mal + 1

print("Jornal Sol: ")
print("Número noticias Bem classificadas " + str(bem))
print("Número noticias MAL classificadas " + str(mal))
