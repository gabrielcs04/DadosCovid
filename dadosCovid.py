import os
import wget
import pandas as pd
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
casosMes = []

for i in range(len(data)):
  [dia, mes, ano] = data[i].split('/')
  dado = f'{mes} {ano}'

  if dado not in meses:
    meses.append(dado)

print(meses)
print(casosMes)

print(len(meses))
print(len(casosMes))
# plt.bar(meses, casosMes)
# plt.show()
