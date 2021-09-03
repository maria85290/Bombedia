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
	

    for n in range(1,205):
	# print()
        if (n==35 or n== 3 or n==36 or n==90 or n==181 or n==183 or n==189 or n== 191 or n==197 or n==203 ):
        	pass
        else:
			# Opening JSON file
            f = open('Sol/Sol_extraction_portuguese_' + str(n) + '.json', encoding='utf8')
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


    pdf = pdfplumber.open('Resultados_NetAC_Sol.pdf')

    tabela = [] # guarda a tabela numa lista.

    print(dic)

    for i in range(7):
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

dic_final = {' Está solteira? Multimilionário britânico procura mulher para construir família e passar férias de luxo ': ['12', 'Não', '1,4433', 'Neutro'], ' Manuel Luís Goucha escreve carta aberta ao pai ': ['8', 'Não', '2,1672', 'Neutro'], " Marido de Goucha deixa provocação a Joacine Katar Moreira: 'Será que é xenofobia?' ": ['24', 'Não', '1,5421', 'Neutro'], ' \x93Ele não está na TVI e não estará mais\x94. Marido de Goucha \x91expulso\x92 da estação de Queluz de Baixo ': ['22', 'Não', '1,6746', 'Neutro'], ' Marido de Goucha indignado com alojamento de migrantes em Lisboa: "Portugueses sem-abrigo vagueiam ao frio" ': ['40', 'Sim', '0,5739', 'Positivo'], " Manuel Luís Goucha defende Judite Sousa: 'Tenho vergonha de seres humanos assim'": ['20', 'Sim', '0,0', 'Negativo'], " Goucha comenta piada do marido: 'Nem eu resisto a um arroz de pato ou a uma canja de pombo' ": ['10', 'Não', '0,0', 'Neutro'], ' Manuel Luís Goucha \x91brinca\x92 com telefonema de Marcelo a Cristina Ferreira ': ['3', 'Não', '0,0', 'Neutro'], " Cláudio Ramos responde a marido de Goucha: 'Tenho 46 anos, uma filha para criar e uma carreira maior que a tua, Rui' ": ['28', 'Não', '0,7989', 'Neutro'], ' Manuel Luís Goucha passa fim de semana na Holanda para assistir a provas de equitação ': ['16', 'Sim', '1,9608', 'Negativo'], ' Telespetador decidiu dizer a Goucha que estava farto dele e o apresentador respondeu à letra ': ['26', 'Sim', '1,1881', 'Negativo'], " Marido de Goucha partilha caricatura para 'atacar' Cláudio Ramos: 'Que me desculpem os canídeos de que gosto tanto": ['4', 'Não', '3,8462', 'Neutro'], ' Manuel Luís Goucha e Maria Cerqueira Gomes apresentam \x91Você na TV\x92... nus ': ['12', 'Sim', '0,0', 'Negativo'], " Goucha. 'Dizem que Bruno Caetano foi afastado do 'Você na TV'! Obrigado por me avisarem'": ['3', 'Não', '4,0', 'Neutro'], " Já o deram como morto. Goucha 'responde' a Cristina Ferreira com convidado surpresa ": ['14', 'Não', '0,3311', 'Neutro'], ' A próxima temporada do \x91Você na TV\x92 pode não contar com Manuel Luís Goucha ': ['6', 'Sim', '2,027', 'Negativo'], ' \x93Nunca digas adeus\x94, diz Goucha a Cristina Ferreira ': ['10', 'Não', '0,0', 'Neutro'],
 " 'O público continua com as pessoas em quem acredita', diz Goucha ": ['2', 'Não', '0,0', 'Neutro'], " 'Para mim, o Deus da televisão é o Manuel Luís Goucha' ": ['6', 'Sim', '0,0', 'Negativo'], ' Férias de Cristina Ferreira quase deram vitória a Manuel Luís Goucha ': ['8', 'Não', '0,0', 'Neutro'], ' Manuel Luís Goucha conta como assumiu homossexualidade perante a mãe ': ['16', 'Não', '0,6006', 'Neutro'], " Cristina Ferreira e Manuel Luís Goucha reencontram-se em almoço: 'Não se falou de televisão'": ['7', 'Não', '1,0204', 'Neutro'], 
 ' Maria Cerqueira Gomes assumiu programa sem Goucha e aproximou-se de Cristina Ferreira ': ['21', 'Não', '1,0526', 'Neutro'], " 'Este ano envelheci 10 anos'. Goucha não esquece saída de Cristina ": ['5', 'Não', '0,0', 'Neutro'], ' Goucha revela que fã se mudou dos EUA para o Alentejo por sua causa ': ['6', 'Sim', 
'1,8182', 'Negativo'], " 'Eu não quero ditadores no meu país', diz Manuel Luís Goucha ": ['52', 'Sim', '0,4237', 'Negativo'], ' Cristina Ferreira derrota Manuel Luís Goucha na estreia do seu programa na SIC ': ['28', 'Não', '0,2033', 'Neutro'], " Manuel Luís Goucha confirma 'traição' de Cristina Ferreira em direto ": ['6', 'Não', '0,8696', 'Neutro'], ' Manuel Luís Goucha não acredita nas Aparições de Fátima ': ['8', 'Sim', '0,7692', 'Negativo'], " Goucha confessa: 'quis suicidar-me há muitos anos' ": ['6', 'Não', '0,0', 'Neutro'], " Você na TV. 'Nunca mais vai ser como era'? Goucha responde a seguidora | FOTO ": ['4', 'Sim', '0,0', 'Negativo'], ' Manuel Luís Goucha e Cristina Ferreira iniciam programas de forma semelhante ': ['5', 'Não', '0,0', 'Neutro'], ' Goucha recorre ao Facebook para criticar revista ': ['5', 'Sim', '0,0', 'Negativo'], ' Manuel Luís Goucha não foi discriminado pelos tribunais ': ['9', 'Sim', '2,2124', 'Negativo'], " 'A Cristina Ferreira ganha tanto ou mais que eu', diz Goucha ": ['5', 'Não', '0,0', 'Neutro'], " Manuel Luís Goucha 'ataca' novo ministro no Facebook ": ['31', 'Sim', '0,3633', 'Negativo'], ' Goucha defende concorrente do Masterchef Júnior no Facebook ': ['12', 'Não', '0,5076', 'Neutro'], ' Terá a amizade entre Teresa Guilherme e Manuel Luís Goucha chegado ao fim? ': ['6', 'Não', '0,0', 'Neutro'], 
' Cristina Ferreira quis \x91roubar\x92 marido de Manuel Luís Goucha ': ['24', 'Não', '1,129', 'Neutro'], ' Goucha reage a acusações de agressão no Masterchef Júnior ': ['7', 'Sim', '0,2747', 'Positivo'], ' Goucha fala sobre novo programa. \x93Não vou andar lá no fornicanço\x94 ': ['8', 'Não', '0,0', 'Neutro'], " 'É muito claro na minha vida que eu já não quero fazer programas diários' ": ['26', 'Sim', '1,0116', 'Negativo'], ' Manuel Luís Goucha dá 1500 a jovem sobrevivente de cancro ': ['10', 'Não', '1,4493', 'Neutro'], ' Daniel Oliveira recorda momento em que Mário Machado o ameaçou de morte | VÍDEO ': ['38', 'Sim', '0,2412', 'Positivo'], 
' Cristina Ferreira põe fim a dúvidas sobre a sua amizade com Manuel Luís Goucha ': ['7', 'Não', '1,1111', 'Neutro'], " 'Odeio touradas e vivo há 20 anos com um homem que vai ver todas' ": ['13', 'Não', '0,4673', 'Neutro'], " Goucha. 'Bruno de Carvalho é um homem perturbado?'": ['6', 'Sim', '0,0', 'Negativo'], " Confissões de Verão de Manuel Luís Goucha: 'Não sou dado à praia' ": ['5', 'Sim', '1,0526', 'Negativo'], " 'É tudo a 7!'. A reposta de Goucha a Cristina Ferreira no Instagram ": ['5', 'Não', '0,5102', 'Neutro'], " Marinho Pinto chama 'sirigaita' a Cristina Ferreira ": ['11', 'Não', '0,6993', 'Neutro'], " Manuel Luís Goucha revela quem é o seu 'sucessor' ": ['12', 'Não', '1,6471', 'Neutro'], ' Manuel Luís Goucha partilha imagem do quarto de hospital ': ['5', 'Sim', '1,4925', 'Negativo'], ' Manuel Luís Goucha já reagiu à saída de Cristina Ferreira da TVI ': ['22', 'Não', '0,8333', 'Neutro'], ' Lesão condiciona presença de Manuel Luís Goucha ': ['4', 'Sim', '0,7576', 'Negativo'], ' Cristina Ferreira e Goucha atacados em direto ': ['7', 'Não', '0,3802', 'Neutro'], " 'Não está contente, vá para a SIC'. As 'bocas' de Manuel Luís Goucha ": ['13', 'Não', '0,8403', 'Neutro'], " Suzana Garcia volta a comentar polémica: 'A minha avó é negra e a minha mãe é mulata' ": ['24', 'Sim', '3,4351', 'Positivo'], " 'Ó senhores deixem-se de mariquices ridículas' ": ['6', 'Sim', '2,0134', 'Negativo'], " 'Esta é uma fase em que eu e o Manel precisamos deste silêncio' ": ['5', 'Sim', '0,0', 'Negativo'], " André Ventura critica mensagem de solidariedade de Costa para Marega: 'Era a esta hipocrisia que me referia' ": ['86', 'Sim', '1,7503', 'Positivo'], ' Marega e o racismo em Portugal ': ['19', 'Sim', '1,3767', 'Negativo'], ' Atitude de Bento Rodrigues no Primeiro Jornal está a tornar-se viral nas redes sociais ': ['40', 'Não', '1,2317', 'Neutro'], ' O Marega foi ao Dubai ser tratado pelo Fisioterapeuta através do medicamento infiltrado Meldonium ': ['26', 'Sim', '0,7082', 'Negativo'], ' André Ventura dá a entender que não há racismo nos ataques a Marega ': ['81', 'Sim', '1,9399', 'Positivo'],
 ' FCP. Marega abandona campo depois de insultos racistas ': ['35', 'Sim', '1,5184', 'Negativo'], ' Marega reage nas redes sociais e ataca o árbitro ': ['26', 'Sim', '1,5816', 'Positivo'], ' A fantochada do racismo ': ['104', 'Sim', '1,9879', 'Negativo'], " Moussa Marega. O jogador que fez história por dizer 'Basta!'' ao racismo ": ['24', 'Não', '3,4413', 'Neutro'], 
 " Catarina Martins: 'Adepta de Marega me confesso. Racismo não é opinião. É crime ": ['33', 'Sim', '2,8679', 'Positivo'], ' PSP diz já ter identificado dez pessoas no caso Marega ': ['71', 'Não', '1,3315', 'Neutro'], ' Marcelo condena insultos racistas a Marega ': ['73', 'Sim', '2,2989', 'Positivo'], ' PSP já identificou adeptos que dirigiram insultos racistas a Marega ': ['49', 'Sim', '1,4146', 'Negativo'], " Comportamento dos jogadores do FC Porto 'foi nojento' ": ['34', 'Não', '0,8705', 'Neutro'], " João Mário sobre o caso Marega: 'Fala-se muito e não se faz nada' ": ['21', 'Não', '2,2417', 'Neutro'], ' Caso Marega. Conselho de Disciplina abre processo ao Vitória de Guimarães ': ['15', 'Sim', '1,5385', 'Negativo'], ' Ministro e responsáveis do futebol vão ao Parlamento falar sobre Caso Marega ': ['17', 'Não', '1,8987', 'Neutro'], ' Hoje em dia falam muito de jogadores como Mbappé, Messi ou CR7 e esquecem-se de Marega ': ['21', 'Não', '0,8547', 'Neutro'], " 'Mais do que racismo, foi uma prova de estupidez', diz Pinto da Costa sobre caso Marega ": ['38', 'Não', '1,2903', 'Neutro'], ' Pepe e Marega alvo de processos disciplinares ': ['14', 'Não', '2,8391', 'Neutro'], " APCVD abre processo sobre caso Marega para 'averiguar responsabilidades' ": ['10', 'Sim', '0,5917', 'Negativo'], ' FC Porto. Marega recupera de lesão na China ': ['6', 'Sim', '0,0', 'Negativo'], " Rúben Amorim defende Marega: 'Está na hora de passar-se à ação e castigar' ": ['13', 'Não', '1,4535', 'Neutro'], 
 " Vitória SC reage a caso Marega e diz que não irá 'vestir a pele do lobo' por um problema 'de dimensão nacional' ": ['16', 'Sim', '1,5942', 'Positivo'], " José Carlos Malato sobre a eutanásia: 'Espero  que as pessoas possam decidir'": ['20', 'Não', '0,3356', 'Neutro'], ' No nono aniversário da legalização do casamento LGBT em Portugal, Malato deixa sugestão à Câmara de Lisboa ': ['6', 'Sim', '3,0', 'Negativo'], ' Eutanásia. Malato foi ao Parlamento e partilhou a sua opinião ': ['13', 'Sim', '0,9709', 'Negativo'], " José Carlos Malato: 'Devia ter morrido no ano passado. Não gosto nada do presente' ": ['18', 'Não', '1,6949', 'Neutro'], ' Apresentador José Carlos Malato operado de urgência ': ['10', 'Sim', '0,5376', 'Negativo'], 
 ' Redes sociais. Nuno Markl segue \x91conselho\x92 de José Carlos Malato ': ['4', 'Não', '0,0', 'Neutro'], ' José Carlos Malato deixa mensagem sobre homossexualidade nas redes sociais | Foto ': ['31', 'Não', '0,8782', 'Neutro'], ' Liliana Campos pede desculpa a José Carlos Malato após insinuar que este queria chamar a atenção ': ['8', 'Sim', '0,4762', 'Negativo'], ' Malato sofre problema cardÃ\xadaco ': ['8', 'Sim', '0,8032', 'Positivo'], ' União gay ainda não é permitida nos Casamentos de Santo António ': ['90', 'Não', '1,1825', 'Neutro'], " 'A minha mãe foi proibida de privar comigo porque sou gay' ": ['22', 'Sim', '0,3187', 'Negativo'], ' Cara Delevingne assume relação no mês do orgulho LGBT ': ['3', 'Sim', '0,0', 'Negativo'], ' Vaticano reconhece comunidade LGBT pela primeira vez ': ['8', 'Não', '1,3393', 'Neutro'], ' Bandeira LGBT hasteada na Câmara Municipal de Lisboa ': ['23', 'Sim', '0,4093', 'Negativo'], ' Associações de defesa dos direitos LGBT francesas criticam palavras do papa sobre homossexualidade ': ['18', 'Não', '0,3527', 'Neutro'], ' Estas são as melhores cidades LGBT do mundo ': ['11', 'Não', 
'4,3243', 'Neutro'], " Uma bandeira LGBT 'original' em Moscovo | FOTOS ": ['6', 'Sim', '1,3699', 'Negativo'], ' Turquia: manifestação LGBT acaba em confrontos com a polícia ': ['10', 'Sim', '2,0362', 'Negativo'], ' Marcha do Orgulho Gay nos Açores mobiliza pouco mais de dez pessoas '
: ['37', 'Não', '0,8574', 'Neutro'], ' Marcha LGBT. Centenas de pessoas desfilaram em Lisboa contra a discriminação ': ['5', 'Sim', 
'0,0', 'Negativo'], ' Escola cristã expulsa aluna por usar camisola com arco-irís nas redes sociais ': ['38', 'Não', '0,9371', 'Neutro'], ' Gay pride.  Todo o orgulho em ser o que se é ': ['18', 'Não', '1,7405', 'Neutro'], ' Por que razão Julianne Moore é um ícone gay? ': ['6', 'Não', '2,381', 'Neutro'], ' Editor de revista LGBT do Bangladesh agredido até à morte ': ['6', 'Sim', '3,7975', 'Positivo'], 
' Associação LGBT pede que insultos homofóbicos feitos a Ronaldo sejam investigados ': ['6', 'Não', '3,7975', 'Neutro'], ' Milhares na marcha LGBT no Porto ': ['3', 'Sim', '0,8721', 'Negativo'], ' Seja a família como for, o importante é haver amor ': ['19', 'Não', '0,3578', 'Neutro'], " Activistas querem abrir a primeira escola 'gay' do Reino Unido ": ['8', 'Não', '3,0822', 'Neutro'], ' Primeira série LGBT portuguesa começa a ser filmada quinta-feira ': ['6', 'Sim', '1,9737', 'Negativo'], " 'Eu era gay antes de me curar' ": ['25', 'Não', '2,0797', 'Neutro'], ' Casal homossexual agredido por grupo no Terreiro do Paço ': ['25', 'Sim', '1,9093', 'Negativo'], 
' Marcha do Orgulho Gay defende direitos de LGBT ': ['13', 'Não', '0,0', 'Neutro'], " Futura ministra de Bolsonaro defende que a mulher 'nasceu para ser mãe' ": ['39', 'Não', '1,0668', 'Neutro'], ' Campolide já tem duas passadeiras com as cores do arco-íris ': ['22', 'Sim', '1,1905', 'Negativo'], ' Brasil não pode ficar conhecido como paraíso do mundo gay ': ['64', 'Não', '0,8211', 'Neutro'], 
' Barreiro. Deputadas do Bloco apresentam queixa contra deputado do PSD ': ['25', 'Sim', '0,5708', 'Positivo'], ' Lisboa vai ter passadeiras com cores da bandeira LGBTI contra a homofobia ': ['64', 'Sim', '1,0645', 'Negativo'], ' Ricardo Araújo Pereira criticado por declarações feitas ao i [vídeo] ': ['12', 'Sim', '0,8696', 'Negativo'], ' Malta introduziu o divórcio há seis anos. Agora prepara-se para o casamento gay ': ['6', 'Não', '0,0', 'Neutro'], ' Adeptos do FC Porto detidos em Itália por agressão a agentes da autoridade ': ['37', 'Sim', '0,2994', 'Negativo'], ' Greta Thunberg poderá estar a caminho de Portugal ': ['50', 'Sim', '0,3028', 'Negativo'], ' Irmã mais nova de Greta Thunberg chama-se Beata e luta pelo feminismo e contra o bullying ': ['15', 'Sim', '2,4735', 'Negativo'], ' Mau tempo impede Greta de discursar no Parlamento ': ['71', 'Sim', '0,2328', 'Positivo'], ' Greta Ã© louca e perigosa. Acho que ela tem de voltar Ã\xa0 escola e calar-se ': ['83', 'Sim', '0,5747', 'Negativo'], ' Erro de atriz leva Greta Thunberg a mudar de nome nas redes sociais ': ['13', 'Sim', '1,1696', 'Positivo'], ' Depois de ataque de Trump, Michelle Obama deixa mensagem a Greta ': ['63', 'Sim', '1,4247', 'Positivo'], ' Greta Thunberg envolvida em polémica com empresa de comboios ': ['14', 'Sim', '0,738', 'Negativo'], ' Greta Thunberg está cada vez mais próxima de Portugal. Agora, em direção aos Açores ': ['16', 'Sim', '0,5848', 'Negativo'], ' Fernando Rocha testa positivo à covid-19 pela sexta vez ': ['21', 'Sim', '0,566', 'Negativo'], ' Após teste negativo, Fernando Rocha volta a testar positivo para covid-19 ': ['12', 'Não', '0,0', 'Neutro'], ' Fernando Rocha revela que está infetado com covid-19 ': ['30', 'Não', '0,2829', 'Neutro'], ' Após dois meses em casa, Fernando Rocha revela qual foi a primeira coisa que fez ': ['4', 'Não', '1,0309', 'Neutro'], ' Já morreram mais pessoas infetadas com covid-19 no Brasil do que na China ': ['57', 'Sim', '0,107', 'Negativo'], ' Bolsonaro visitou padaria e abraçou e tirou fotografias com funcionários  | Vídeo ': ['36', 'Sim', '0,5932', 'Negativo'], 
' Bolsonaro ameaça ministro da Saúde por defender isolamento: Nenhum ministro é indemissível ': ['23', 'Não', '0,4747', 'Neutro'], ' 17% dos eleitores que votaram em Bolsonaro estão arrependidos ': ['105', 'Sim', '0,7361', 'Negativo'], ' Sou Messias, mas não faço milagres. Bolsonaro sobre recorde de mortes no Brasil ': ['76', 'Sim', '0,467', 'Positivo'], ' Brasil volta a registar recorde de novos casos de infeção por covid-19 ': 
['14', 'Sim', '0,4747', 'Positivo'], ' Bolsonaro protagoniza mais um momento insólito ao ser questionado sobre mortes: Não sou coveiro': ['40', 'Sim', '0,2681', 'Positivo'], ' O dia mais negro do Brasil ': ['48', 'Sim', '0,1741', 'Positivo'], ' O Brasil é dirigido por um fantoche que é absolutamente ignorante, inimputável, incompetente e cruel ': ['36', 'Sim', '0,6923', 'Positivo'], ' Bolsonaro Messias não faz milagres, nem os seus discípulos o seguem ': ['13', 'Sim', '0,7273', 'Negativo'], ' Bolsonaro diz que não é uma gripezinha que o vai derrubar ': ['60', 'Sim', '0,2706', 'Negativo'], ' Brasil. A longa descida ao inferno do Governo  de Jair Bolsonaro ': ['33', 'Não', '0,2662', 'Neutro'], ' Toda a gente morre um dia. Foi assim que Bolsonaro reagiu às 20 mil mortes por covid-19 no país ': ['87', 'Sim', '0,5457', 'Positivo'], 
' Fiéis de Caminha manifestam-se contra saída de padre motard e sex symbol': ['38', 'Sim', '0,2817', 'Negativo'], ' Padre e falsas freiras escravizavam raparigas em Braga ': ['17', 'Sim', '0,7937', 'Positivo'], ' Padre de Pedrógão diz ser um maroto sem maldade ': ['18', 'Sim', '0,5272', 'Positivo'], ' Foi um descuido afirma padre após publicar fotografia em cuecas nas redes sociais ': ['7', 'Não', '0,0', 'Neutro'], ' Padre encontrado morto na praia de São Pedro de Moel ': ['39', 'Sim', '0,7194', 'Negativo'], ' Vaticano expulsa padre que revelou homossexualidade ': ['8', 'Sim', '0,2551', 'Negativo'], ' Convidada deixa Fátima Lopes estupefacta: A primeira vez que me prostituí foi com um padre ': ['26', 'Sim', '0,7547', 'Negativo'], ' Igreja encobriu padre que abusou sexualmente dos filhos ': ['6', 'Sim', '0,565', 'Negativo'], ' Crianças forçadas a puxar Porsche do padre | Vídeo ': ['15', 'Sim', '0,8351', 'Negativo'], 
' Padre expulsa maestro do coro por ser homossexual ': ['21', 'Sim', '0,5545', 'Negativo'], ' Padre culpa gays pelos sismos de Itália ': ['10', 'Sim', '0,6135', 'Negativo'], 
' Padre acusado de burlar o Estado ': ['15', 'Sim', '0,3409', 'Positivo'], ' Padre assume homossexualidade no final da missa ': ['28', 'Sim', '2,0408', 'Negativo'], ' Igreja: padre denuncia encontros gay em bares e ginásios ': ['5', 'Não', '0,4354', 'Neutro'], ' Padre gera polémica ao dizer que pedofilia não mata ninguém ao contrário do aborto ': ['29', 'Sim', '0,5231', 'Positivo'], ' Detido no Algarve padre que abusou de mais de 20 crianças ': ['13', 'Sim', '2,2785', 'Negativo'], ' Ex-padre casa com modelo 55 anos mais novo ': ['6', 'Não', '3,3898', 'Neutro'], ' Padre de Pedrógão Grande fotografado em roupa interior muda de religião ': ['14', 'Não', '0,3937', 'Neutro'], ' Cristina Ferreira mostra mais do que queria em fotografia ': ['16', 'Não', '0,0', 'Neutro'], ' Cristina Ferreira lanÃ§a livro com nome chocante. Saiba qual ': ['56', 'Não', '0,4115', 'Neutro'], ' Tens uma relaÃ§Ã£o amorosa com a Cristina Ferreira? Ruben Rua responde ': ['13', 'Não', '2,6316', 'Neutro'], " Costa 'despediu' presidente do TdC por telefone ": ['128', 'Não', '0,6305', 'Neutro'], ' AntÃ³nio Costa deseja as melhoras a Trump ': ['14', 'Sim', '2,0243', 'Positivo'], ' Donald Trump e Melania testaram positivo para a covid-19 ': ['88', 'Sim', '0,7235', 'Negativo'], ' AntÃ³nio Costa reage a entrevista de Ana Leal ao SOL: â\x80\x9cÃ\x89 mentiraâ\x80\x9d ': ['99', 'Sim', '0,4216', 'Positivo'], ' António Costa admite adotar medidas ainda mais restritivas nas próximas semanas ': ['47', 'Não', '0,3435', 'Neutro'], ' Bazuca de pÃ³lvora seca desespera UE ': ['32', 'Sim', '0,0677', 'Negativo'], 
' AntÃ³nio Costa diz que manifestaÃ§Ã£o no Porto foi legÃ\xadtima mas condena arremesso de garrafas ': ['56', 'Sim', '0,6382', 'Positivo'], ' AntÃ³nio Costa garante que Portugal nÃ£o vai usar emprÃ©stimos europeus enquanto situaÃ§Ã£o financeira do paÃ\xads nÃ£o o permitir ': ['59', 'Não', '0,8277', 'Neutro'], ' AntÃ³nio Costa pede aos portugueses que comprem mÃ¡scaras nacionais ': ['20', 'Não', '0,3311', 'Neutro'], ' AntÃ³nio Costa afirma que o paÃ\xads enfrenta gigantesca responsabilidade ': ['27', 'Não', '0,2336', 'Neutro'], ' AntÃ³nio Costa e Fernando Medina na comissÃ£o de honra de LuÃ\xads Filipe Vieira ': ['119', 'Não', '0,4036', 'Neutro'], ' Marcelo marca as presidenciais para dia 24 de janeiro ': ['30', 'Sim', '0,3929', 'Negativo'], ' Costa elogia comportamento exemplar dos portugueses no fim de semana ': ['44', 'Sim', '0,0747', 'Positivo'], ' Comunistas recusam adiar congresso ': ['58', 'Sim', '0,8661', 'Negativo'], ' ClÃ¡udio Ramos revela: â\x80\x9cOdiei trabalhar com a Joana Latino': ['22', 'Não', '1,0309', 'Neutro'], ' Cláudio Ramos confessa a Cristina que lhe custou ficar sem o Big Brother ': ['7', 'Não', '1,4493', 'Neutro'], ' ClÃ¡udio Ramos para Carolina Deslandes: EntÃ£o burra e quem nÃ£o lÃª Ã©s tu ': ['15', 'Sim', '0,6515', 'Negativo'], 
' Emocionado, Goucha revela em que momento se sentiu magoado com Cristina Ferreira ': ['9', 'Não', '1,3699', 'Neutro'], ' Acusado de discriminaÃ§Ã£o, Manuel LuÃ\xads Goucha responde a seguidora ': ['17', 'Sim', '2,3891', 'Positivo'], ' Goucha arrasa pessoas que nÃ£o cumpriram normas de seguranÃ§a na NazarÃ©: Imbecis e criminosos ': ['33', 'Sim', '1,6706', 'Negativo'], " Rita Blanco dÃ¡ que falar apÃ³s 'indiretas' a Cristina Ferreira: PÃµe lÃ¡ no canal da outra ": ['9', 'Não', '0,5051', 'Neutro'], ' Cristina Ferreira compra 2,5% da Media Capital ': ['32', 'Não', '0,5369', 'Neutro'], ' Marta Temido considera que votar contra OE Ã© desistir de melhorar os serviÃ§os pÃºblicos de saÃºde ': ['10', 'Sim', '0,0', 'Negativo']} 




## Funçao recebe o dicionario no formato: {nomeFicheiro: [percentagem hate, resultado avaliação app bombmedia]}
def gerarTabela(d):
   
    texfilename ="TabelaSol.tex"
     
    texfile = open(texfilename, 'w')
    
    texfile.write("\documentclass[11pt]{article}\n\\usepackage{graphicx}\n\\usepackage{multirow}\n\\usepackage[pdftex]{hyperref}\n\\usepackage{colortbl}")
    texfile.write("\n\\usepackage{longtable, array}\n\\usepackage[usenames,dvipsnames,svgnames,table]{xcolor}\n\\newlength\mylength")
    texfile.write("\n\\usepackage[legalpaper, landscape, margin=1in]{geometry}\n\\newcommand{\MinNumber}{0}")
    texfile.write("\\begin{document}")
    texfile.write( "\n\n")
    
    texfile.write("\\textbf {\\huge Jornal Sol:}")
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
    color11 = "green!21"

    color = color2

    for title in d:

        ## Substituir a virgula da string por um ponto para puder ser interpretada como float

        perc_hate = d[title][2].split(",")
        per = perc_hate[0]

        # Definir as cores
        ## Verde se tiver bem classificado
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


#### PARA RETIR ASSENTOS E Não DAR ERRO AO GERAR PDF LATEX DA TABELA
new_dic = {}


from unidecode import unidecode

for title in dic_final:
    new_dic[(unidecode(title))] = dic_final[title]
    

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

