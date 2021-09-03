import pdfplumber
import pandas as pd


pdf = pdfplumber.open('Classificação_netAC_publico.pdf')

tabela = [] # guarda a tabela numa lista.

for i in range(5):
    p1 = pdf.pages[i]
    table = p1.extract_table()

    for j in table:
        tabela.append(j)

print(tabela)

for i in tabela:
    l = i[0].split(".")[0].split("-")
    print(len(l))
    print(l[-1])

