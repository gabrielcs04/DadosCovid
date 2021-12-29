import os
import wget
import math
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

obitosMes = []
quantObitos = 0

for i in range(len(meses)):
  for j in range(len(data)):
    [dia, mes, ano] = data[j].split('/')
    dado = f'{mes} {ano}'
    if dado == meses[i]:
      quantObitos += obitosDia[j]
  if math.isnan(quantObitos):
    quantObitos = 0
  obitosMes.append(quantObitos)
  quantObitos = 0

# print(meses)
# print(casosMes)
# print(len(meses))
# print(len(casosMes))
# print(obitosMes)

plt.figure(figsize=(14, 6))
plt.bar(meses, casosMes, ec = "k", alpha = .6, color = "royalblue")
plt.xticks(np.arange(0, len(meses), 2))
plt.title('Casos novos por mês')
plt.xlabel('Mês')
plt.ylabel('Quantidade de casos')
plt.savefig('CasosMes.png', format='png', dpi=300)
plt.show()

plt.figure(figsize=(14, 6))
plt.bar(meses, obitosMes, ec = "k", alpha = .6, color = "royalblue")
plt.xticks(np.arange(0, len(meses), 2))
plt.title('Óbitos por mês')
plt.xlabel('Mês')
plt.ylabel('Quantidade de óbitos')
plt.savefig('ObitosMes.png', format='png', dpi=300)
plt.show()