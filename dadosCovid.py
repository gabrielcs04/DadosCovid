import os
import wget
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from fpdf import FPDF

linkArq = 'https://www.seade.gov.br/wp-content/uploads/coronavirus-files/Dados-covid-19-estado.csv'
nomeArq = 'dadosCovidEstado.csv'

try:
  os.remove(nomeArq)
except OSError as e:
  print(f"Erro: {e.strerror}")

wget.download(linkArq, nomeArq, False)

tabela = pd.read_csv(nomeArq, delimiter=";", encoding='ISO-8859-1')

data = tabela['Data']
totalCasos = tabela['Total de casos']
casosDia = tabela['Casos por dia']
obitosDia = tabela['Óbitos por dia']

meses = []

for i in range(len(data)):
  [dia, mes, ano] = data[i].split('/')
  dado = f'{mes} {ano}'
  if dado not in meses:
    meses.append(dado)

casosMes = []
quantCasos = 0

for i in range(len(meses)):
  for j in range(len(data)):
    [dia, mes, ano] = data[j].split('/')
    dado = f'{mes} {ano}'
    if dado == meses[i]:
      quantCasos += casosDia[j]
  
  casosMes.append(quantCasos)
  quantCasos = 0

# print(meses)
# print(casosMes)
# print(len(meses))
# print(len(casosMes))

plt.bar(meses, casosMes, ec = "k", alpha = .6, color = "royalblue")
plt.xticks(np.arange(0, len(meses), 2))
plt.title('Casos novos por mês no Estado de São Paulo')
plt.xlabel('Mês')
plt.ylabel('Quantidade de casos')

plt.show()
