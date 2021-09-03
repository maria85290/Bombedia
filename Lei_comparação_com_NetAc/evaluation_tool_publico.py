# -*- coding: utf-8 -*-

import os
#os.system('python3 -m pip install tensorflow')
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
	for n in range(1,127):
	# print()
		if (n==100 or n ==101 or n == 2):
			pass
		else:
			# Opening JSON file
			f = open('Publico/Publico_extraction_portuguese_c_' + str(n) + '.json', encoding='utf8')
			data = json.load(f)
			
			if 'subtitle' in data["header"]:
				inputText = data['header']['subtitle']
			else:
				inputText = data['header']['title']
			d[n] = [data['header']['title'],inputText]
			f.close()
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


    pdf = pdfplumber.open('Classificação_netAC_publico.pdf')

    tabela = [] # guarda a tabela numa lista.

    print(dic[1])

    for i in range(5):
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

#d = read_json()
#dic_final = avaliar(d)


dic_final = {' Supremo Tribunal Federal do Brasil proíbe censura de BD com beijo gay ': ['10', 'Não', '0,3067', 'Neutro'], 
' O PiS tem tudo para ganhar na Polónia, mas a corrida está mais disputada do que parece ': ['9', 'Sim', '1,1682', 'Positivo'], 
' Como Tancos salva a direita de si própria ': ['85', 'Sim', '0,1044', 'Negativo'], 
' Casal sofre agressão homofóbica no Terreiro do Paço ': ['53', 'Não', '0,981', 'Neutro'], 
' Arábia Saudita abre-se ao turismo. Há vistos turísticos pela primeira vez ': ['9', 'Não', '0,0', 'Neutro'], 
' Eles puseram-se Na Pele Dela em nome da igualdade de género ': ['9', 'Não', '1,105', 'Neutro'], 
' Vamos meter medo no coração do homem branco e outras citações de Robert Mugabe ': ['12', 'Não', '1,3129', 'Neutro'], 
' Anti-gender, uma sombra que cobre a Europa ': ['88', 'Não', '0,5397', 'Neutro'], 
' A diversidade deve começar na escola? Sim. Caso contrário, vamos continuar a reproduzir estereótipos ': ['15', 'Não', '0,3979', 'Neutro'],
' Identidade de género: Estão em causa crianças e jovens que se sentem alvo de chacota': ['8', 'Não', '0,2053', 'Neutro'], ' Médicos vão ter guia para atender utentes transgénero e intersexo ': ['13', 'Não', '0,0', 'Neutro'], ' Parabéns insultuosos ': ['16', 'Sim', '0,1451', 'Negativo'], ' Esta é a 20ª marcha LGBTI+ em Lisboa. Lei mudou, falta a prática social ': ['42', 'Não', '1,735', 'Neutro'], 
' Milhares levam arco-íris pelas ruas de Lisboa em marcha de orgulho LGBTI+ ': ['43', 'Não', '0,3701', 'Neutro'], ' Investigadoras desmontam conjunto de mentiras  sobre  ideologia de género  ': ['31', 'Sim', '0,6524', 'Positivo'], ' Numa escola em Taiwan, os rapazes vão poder optar pela saia como uniforme ': ['6', 'Não', '1,3636', 'Neutro'], 
' Casamentos de Santo António ainda Não incluem matrimónios gay ': ['15', 'Não', '0,6547', 'Neutro'], ' Nem sexo, nem morte. Bruno Maia, o médico sem tabus a caminho da AR ': ['5', 'Não', '1,6949', 'Neutro'], ' EUA proíbe embaixadas de hastear bandeiras LGBT ': ['9', 'Sim', '1,6667', 'Negativo'], ' Polícias recebem formação para dar resposta a crimes de ódio contra pessoas LGBTI ': ['7', 'Sim', '1,4388', 'Positivo'], ' De norte a sul do país, o orgulho LGBTI+ volta a sair à rua ': ['3', 'Não', '0,0', 'Neutro'], ' Taiwan legaliza casamento entre pessoas do mesmo sexo, uma estreia na Ásia ': ['6', 'Não', '0,0', 'Neutro'], ' Clima social em Portugal ainda é homofóbico e transfóbico, denuncia ILGA ': ['6', 'Não', '0,0', 'Neutro'], ' Ser gay é genético ou deve-se a  conjunturas externas ? Colégio retira publicação de iniciativa do secundário ': ['52', 'Não', '0,458', 'Neutro'], ' Brunei pede  tolerância  com a decisão de punir sexo homossexual com apedrejamento até à morte ': ['18', 'Não', '0,4695', 'Neutro'], ' Como o Brasil está a contracenar com Bolsonaro ': ['7', 'Sim', '1,7143', 'Negativo'], ' Fado Bicha:  Isto é fado , mesmo que fale do Namorico do André e do Chico ': ['23', 'Sim', 
'1,4019', 'Negativo'], ' Uma resposta a Pacheco Pereira: o \#MeToo é uma revolução demasiado necessária e já vem tarde ': ['15', 'Sim', '0,4921', 'Positivo'], ' Lisboa recebe agora a missa Beyoncé   a pensar na Igreja e nas mulheres negras ': ['6', 'Não', '0,0', 'Neutro'], ' No Vaticano  quanto mais homofóbico alguém é, mais hipóteses haverá de ser gay  ': ['22', 'Não', '1,0989', 'Neutro'], ' LGBTI nas escolas? Quem está no terreno dispensa discursos apaixonados ': ['4', 'Sim', '0,6116', 'Negativo'], ' Associações LGBTI em escolas? Depende muito ': ['86', 'Sim', '0,7956', 'Negativo'], ' Jean Wyllys:  O que deu a vitória a Bolsonaro foi a homofobia  ': ['126', 'Não', '0,5071', 'Neutro'], ' PSP identificou dois homens que tentaram atirar ovos contra Jean Wyllys em Coimbra ': ['26', 'Não', '0,1953', 'Neutro'], ' Primeiro projecto no novo Congresso do Brasil é de "ex-gay" que quer que Bíblia seja património cultural ': ['11', 'Não', '0,5013', 'Neutro'], 
' Homem, mulher ou x? Os passageiros podem escolher a opção nas companhias aéreas ': ['3', 'Sim', '2,8986', 'Negativo'], '  Nunca haverá um tempo sem Deus ou religião  ': ['29', 'Não', '0,0', 'Neutro'], ' Transição social de género em ambiente escolar   atenuar o sofrimento de crianças e jovens ': ['12', 'Não', '0,0', 'Neutro'], ' Maioria da esquerda reduz poderes de Marcelo, dramatiza Cristas ': ['4', 'Sim', '2,4096', 'Negativo'], ' A crise da Direita ': ['5', 'Sim', '0,2611', 'Positivo'], ' O género foi à casa de banho ': ['5', 'Não', '0,0', 'Neutro'], ' Actor Ângelo Rodrigues terá injectado testosterona e foi hospitalizado. Quais os riscos desta hormona? ': ['29', 'Não', '0,0', 'Neutro'], ' Alerta para cidadãos confusos ': ['23', 'Não', '0,2562', 'Neutro'], ' Victoria s Secret cancela o desfile anual dos  anjos  ': ['9', 'Sim', '0,0', 'Negativo'], '  E se o seu filho namorasse uma pessoa do mesmo sexo?  42% dos portugueses assumem desconforto ': ['31', 'Não', '0,6595', 'Neutro'], ' O CDS é um partido transgénero ': ['19', 'Não', '0,1854', 'Neutro'], ' Alunos transgénero Não serão mais de 200, adianta secretário de Estado ': ['18', 'Não', '0,6593', 'Neutro'], ' Inventar uma casa de emergência para vítimas de violência doméstica LGBTI ': ['5', 'Não', '1,4423', 'Neutro'], ' A culpa e a reparação '
: ['22', 'Não', '0,5305', 'Neutro'], " Primeiro projecto no novo Congresso do Brasil é de 'ex-gay' que quer que Bíblia seja património cultural ": ['11', 'Não', '0,5013', 'Neutro'], ' Cristina Ferreira a Presidente? Apresentadora Não descarta candidatar-se a Belém ': ['45', 'Sim', '0,4902', 'Negativo'], 
' Crédito Agrícola vendeu imóvel a mãe de gestor da equipa de Licínio Pina ': ['20', 'Não', '0,2545', 'Neutro'], ' Cristina Ferreira troca TVI pela SIC e vai ocupar as manhãs ': ['23', 'Não', '0,9098', 'Neutro'], ' É o fim de uma era. SIC ultrapassa TVI nas audiências mensais pela primeira vez em mais de 12 anos ': ['45', 'Não', '0,3008', 'Neutro'], ' Joacine Katar Moreira recusa  paternalismo  dos deputados ': ['25', 'Sim', '0,6639', 'Positivo'], " Joacine Katar Moreira exige 'respeito' por parte dos jornalistas ": ['22', 'Não', '0,5859', 'Neutro'], " Joacine Katar Moreira: 'Fui eu que ganhei as eleições sozinha' ": ['67', 'Não', '0,6008', 'Neutro'], " 'Irei manter todas as minhas funções, a mensagem irá ser compreendida', diz Joacine Katar Moreira ": ['39', 'Não', '0,7386', 'Neutro'], ' Joacine Katar Moreira vs. Daniel Oliveira: polémica acesa nas redes sociais ': ['72', 'Sim', '0,5908', 'Negativo'], " Joacine Katar Moreira: 'Sem igualdade Não há liberdade nenhuma' ": ['164', 'Não', '0,6828', 'Neutro'], ' Livre elege Joacine Katar Moreira, uma activista negra ': ['44', 'Não', '0,9528', 'Neutro'], ' Joacine Katar Moreira: uma activista negra a caminho do Parlamento? ': ['27', 'Não', '1,625', 'Neutro'], ' Confronto sobe de tom: direcção do Livre desmente deputada Joacine Moreira ': ['18', 'Não', '0,0', 'Neutro'], " Os gritos de 'mentira' de Joacine: 'Senti a vergonha alheia' ": ['18', 'Não', '0,4323', 'Neutro'], 
' Livre  preocupado  com a sua deputada. Joacine Moreira diz-se apanhada de surpresa ': ['99', 'Não', '0,4457', 'Neutro'], " Joacine admite fazer 'cedências necessárias'. Direcção do Livre diz que será preciso 'milagre' ": ['35', 'Sim', '0,7225', 'Negativo'], ' Nova direcção do Livre   sem Joacine   eleita com 95 votos a favor e 15 brancos ': ['17', 'Não', '0,8565', 'Neutro'], ' O direito de resposta (mais moderado) que Joacine entregou ao congresso ': ['5', 'Sim', '1,9481', 'Negativo'], ' Congresso adia decisão sobre retirada da confiança política a Joacine ': ['39', 'Sim', '0,0', 'Negativo'], ' Joacine:  Elegeram uma mulher negra que gagueja e deu jeito para a subvenção  ': ['137', 'Sim', '1,2164', 'Positivo'], " Renunciar ao mandato de deputada? Joacine diz que 'está fora de questão' ": ['17', 'Sim', '0,3513', 'Positivo'], ' O que acontece a Joacine se o Livre aprovar retirada de confiança política? ': ['21', 'Sim', '0,2088', 'Positivo'], ' Orçamento foi a gota de água que levou Livre a propor retirada de confiança a Joacine ': ['88', 'Não', '0,0872', 'Neutro'], ' Peço desculpa: Joacine e o Livre discordam em quê? ': ['59', 'Não', '0,8722', 'Neutro'], " Escolta a Joacine na AR: GNR só pode intervir se estiver em causa a 'segurança física' de deputados ": ['29', 'Não', '0,1907', 'Neutro'], ' Joacine perdeu a graça ': ['25', 'Não', '0,4008', 'Neutro'], 
' Assessor de Joacine queixa-se de interrupções permanentes, cerco e mercantilização da informação ': ['31', 'Não', '0,189', 'Neutro'], 
' Joacine garante que tensões Não são por divergências programáticas ': ['29', 'Não', '0,578', 'Neutro'], ' O erro da escolha de Joacine pelo Livre ': ['43', 'Não', '0,5729', 'Neutro'], " Joacine diz que votou 'contra ela própria' e devolve responsabilidades da abstenção à direcção do Livre ": ['51', 'Não', '0,5141', 'Neutro'],  
' Polémica entre Joacine e Livre Não acaba aqui. Caso segue para conselho de jurisdição ': ['54', 'Não', '0,9667', 'Neutro'], 
' Joacine e direcção do Livre trocam acusações. Fundador Rui Tavares critica deputada ': ['28', 'Sim', '0,2364', 'Negativo'], ' Queixa ou carta aberta: Mulheres Socialistas repudiam programas da SIC e TVI ': ['15', 'Sim', '0,2525', 'Negativo'], ' Estão os concursos da SIC e da TVI a reproduzir estereótipos femininos? ': ['21', 'Não', '0,6526', 'Neutro'], ' Rui Pinto assume ser o denunciante do Luanda Leaks ': ['71', 'Sim', '0,1076', 'Positivo'], ' BE quer Isabel dos Santos impedida de vender participações compradas com  dinheiro roubado  ': ['28', 'Sim', '0,1938', 'Negativo'], ' Miguel Relvas rejeita ter ligações a Isabel dos Santos. BE corrige acusação, mas mantém suspeita ': ['10', 'Sim', '0,2326', 'Negativo'], ' Isabel dos Santos constituída arguida em Angola ': ['48', 'Sim', '0,3806', 'Positivo'], ' Isabel dos Santos muda de estratégia e negoceia devolução de dinheiro a Angola, noticia o Expresso ': ['21', 'Sim', '0,0', 'Negativo'], ' Advogado de Isabel dos Santos continua inscrito na Ordem, apesar de ter anunciado suspensão ': ['9', 'Não', '0,0', 'Neutro'], 
' Advogados portugueses cobram a offshore de Isabel dos Santos decreto presidencial do pai ': ['25', 'Não', '0,4334', 'Neutro'], ' Isabel dos Santos: como é que ela construiu um império ': ['35', 'Não', '0,2259', 'Neutro'], ' Isabel dos Santos terá transferido 115 milhões da Sonangol para o Dubai ': ['46', 'Não', '0,249', 'Neutro'], ' Isabel dos Santos admite candidatar-se à presidência de Angola ': ['35', 'Não', '0,4092', 'Neutro'], ' Isabel dos Santos Presidente de Angola?  Que em 2027 possa ser candidata é uma ideia  ': ['5', 'Sim', '1,2121', 'Negativo'], '  Lava que se farta! : Isabel dos Santos perde processo contra Ana Gomes ': ['52', 'Sim', '0,365', 'Negativo'], ' Conan Osiris já ganhou o Festival da Canção? ': ['19', 'Sim', '0,3947', 'Negativo'], ' Parem de pedir ao Conan para Não ir a Telavive ': ['50', 'Sim', '0,2051', 'Negativo'], ' Conan Osiris vence Festival da Canção ': ['15', 'Não', '0,0', 'Neutro'], " Isabel dos Santos: a empresária, a princesa, o império e 'os pés de barro do pai' ": ['19', 'Não', '0,2732', 'Neutro'], ' Isabel dos Santos diz que serviços de segurança angolanos lhe entraram nos computadores em Portugal ': ['8', 'Sim', '0,0', 'Positivo'], ' Divididos, Joacine e Livre já estão de olhos postos no futuro ': ['19', 'Não', '0,6908', 'Neutro'], ' Joacine Katar Moreira:  Vamos continuar a trabalhar com a confiança de uns e sem a confiança de outros  ': ['93', 'Sim', '0,9954', 'Negativo'], ' Livre convocou Joacine para reunião, mas deputada diz que Não recebeu nada ': ['27', 'Não', '0,7625', 'Neutro'], ' PS condena  declarações xenófobas  de André Ventura sobre Joacine Katar Moreira ': ['18', 'Não', '0,6631', 'Neutro'], ' André Ventura  propõe  que Joacine  seja devolvida ao seu país de origem . Livre acusa-o de racismo ': ['240', 'Sim', '0,9147', 
'Negativo'], ' Ventura levado ao colo ': ['142', 'Não', '0,3693', 'Neutro'], ' Assessor de Joacine retira  confiança política  ao Livre ': ['9', 'Sim', '1,2121', 'Negativo'], ' Livre aprova retirada de confiança política a Joacine por maioria ': ['147', 'Sim', '0,5434', 'Negativo'],
 ' Joacine deixa de representar o Livre e passa a deputada Não-inscrita a partir de hoje ': ['50', 'Não', '1,0436', 'Neutro'], ' As duas pestes de 2020: coronavírus e racismo ': ['27', 'Sim', '0,7448', 'Positivo'], ' Partidos Não vão condenar racismo de Ventura no plenário para Não prolongar polémica   basta-lhes as palavras de Ferro ': ['31', 'Sim', '0,6524', 'Negativo'], ' Anti-racismo. Antifascismo. Anticomunismo ': ['35', 'Sim', '1,6488', 'Negativo'], ' Novo director da PSP diz que há  tanto racismo  na polícia  como há na sociedade portuguesa  ': ['40', 'Não', '0,9877', 'Neutro'], ' Centenas marcham em Lisboa contra o racismo e a violência policial ': ['15', 'Sim', '1,4286', 'Negativo'], ' Líder das Mulheres Socialistas acusa deputado do Chega de  racismo  e  sexismo  ': ['26', 'Sim', '1,4472', 'Negativo'], ' Portugal instado a enfrentar racismo contra os ciganos ': ['9', 'Não', '1,8307', 'Neutro'], ' Até quando haverá racismo contra as mulheres negras em Portugal? ': ['21', 'Sim', '1,7488', 'Positivo'], ' Mulher acusa polícia de agressão e racismo. PSP chamou bombeiros e disse que era  uma queda  ': ['171', 'Sim', '0,9481', 'Positivo'], ' Presidente dos conselheiros das comunidades portuguesas demite-se por causa de André Ventura ': ['60', 'Não', '0,2612', 'Neutro'], ' Secretária de Estado diz que  ciganofobia  está no dia-a-dia da sociedade portuguesa ': ['6', 'Não', '0,3289', 'Neutro'], ' Contas de Isabel dos Santos em Portugal arrestadas a pedido de Angola ': ['24', 'Não', '0,197', 'Neutro']}



## Funçao recebe o dicionario no formato: {nomeFicheiro: [percentagem hate, resultado avaliação app bombmedia]}
def gerarTabela(d):
   
    texfilename ="TabelaPublico.tex"
     
    texfile = open(texfilename, 'w')
    
    texfile.write("\documentclass[11pt]{article}\n\\usepackage{graphicx}\n\\usepackage{multirow}\n\\usepackage{colortbl}\n\\usepackage{fontspec}")
    texfile.write("\n\\usepackage{longtable, array}\n\\usepackage[usenames,dvipsnames,svgnames,table]{xcolor}\n\\newlength\mylength")
    texfile.write("\n\\usepackage[legalpaper, landscape, margin=1in]{geometry}\n\\newcommand{\MinNumber}{0}")
    texfile.write("\\begin{document}")
    texfile.write( "\n\n")
    
    texfile.write("\\textbf {\\huge Jornal Público:}")
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
    color1 = "green!21"
    color11 = "green!27"

    color = color2

    for title in d:

        ## Substituir a virgula da string por um ponto para puder ser interpretada como float

        perc_hate = d[title][2].split(",")
        per = perc_hate[0]

        # Definir as cores
        if ((float(d[title][0]) > 30 or float(per) >= 1) and d[title][1] == "Sim") or ((float(d[title][0]) < 30 or float(per) < 1 )and d[title][1] == "Não"):
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
    
    command = 'xelatex ' + texfilename #gerar o ficheiro pdf a partir do .tex
    
    os.system(command)
    
    pdffilename = texfilename.split(".")[0] + ".pdf"
    
    return pdffilename


#### PARA RETIR ASSENTOS E Não DAR ERRO AO GERAR PDF LATEX DA TABELA
new_dic = {}

#from unidecode import unidecode

#for title in dic_final:
 #   new_dic[(unidecode(title))] = dic_final[title]
new_dic = dic_final
gerarTabela (dic_final)
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
