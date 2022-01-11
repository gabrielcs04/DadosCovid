# Importações das bibliotecas necessárias
import os
import wget
import math
import pandas as pd
import calendar
import numpy as np
import matplotlib.pyplot as plt
from fpdf import FPDF

# Verifica se a váriavel é do tipo inteiro
def checaInt(str):
  try:
    int(str)
    return True
  except ValueError:
    return False

# Converte o número do mês em seu nome
def converteMes(mes):
    meses = ['jan', 'fev', 'mar', 'abr', 'mai', 'jun', 'jul', 'ago', 'set', 'out', 'nov', 'dez']
    return meses[int(mes)-1]

# Formata casas decimais de um número
def formataNum(num, sep='.'):
  return num if len(num) <= 3 else formataNum(num[:-3], sep) + sep + num[-3:]

# Adiciona legenda nas barras dos gráficos
def adicionaLegendaNasBarras(grafico):
  for reta in grafico:
    altura = reta.get_height()
    largura = reta.get_width()
    plt.text(reta.get_x() + largura/2, altura, formataNum(str(int(altura))), ha='center', va='bottom')



# Link e nome do arquivo CSV utilizado
linkArq = 'https://www.seade.gov.br/wp-content/uploads/coronavirus-files/Dados-covid-19-estado.csv'
nomeArq = 'dadosCovidEstadoSP.csv'

# Remove o CSV caso exista
try:
  os.remove(nomeArq)
except OSError as e:
  print(f"Erro: {e.strerror}")

# Baixa o CSV 
wget.download(linkArq, nomeArq, False)

# Lê o arquivo e extrai as colunas
tabela = pd.read_csv(nomeArq, delimiter=";", encoding='ISO-8859-1')
data = tabela['Data']
totalCasos = tabela['Total de casos']
casosDia = tabela['Casos por dia']
obitosDia = tabela['Óbitos por dia']

# Transforma a data diária em mensal
meses = []
for i in range(len(data)):
  [dia, mes, ano] = data[i].split('/')
  if checaInt(mes):
    mes = converteMes(mes)
  dado = f'{mes} {ano}'
  if dado not in meses:
    meses.append(dado)

# Coleta os casos de covid mensais
casosMes = []
quantCasos = 0
for i in range(len(meses)):
  for j in range(len(data)):
    [dia, mes, ano] = data[j].split('/')
    if checaInt(mes):
      mes = converteMes(mes)
    dado = f'{mes} {ano}'
    if dado == meses[i]:
      quantCasos += casosDia[j]
  if math.isnan(quantCasos):
    quantCasos = 0
  casosMes.append(quantCasos)
  quantCasos = 0

# Coleta os óbitos de covid mensais
obitosMes = []
quantObitos = 0
for i in range(len(meses)):
  for j in range(len(data)):
    [dia, mes, ano] = data[j].split('/')
    if checaInt(mes):
      mes = converteMes(mes)
    dado = f'{mes} {ano}'
    if dado == meses[i]:
      quantObitos += obitosDia[j]
  if math.isnan(quantObitos):
    quantObitos = 0
  obitosMes.append(quantObitos)
  quantObitos = 0

# Variavel da pasta para colocar os gráficos feitos
pastaGraficos = 'graficos'

# Cria o gráfico dos casos
plt.figure(figsize=(16, 7))
fig1 = plt.bar(meses, casosMes, ec="k", alpha=.6, color="royalblue")
plt.xticks(np.arange(0, len(meses), 2))
plt.title('Casos novos por mês')
plt.xlabel('Mês')
plt.ylabel('Quantidade de casos')
plt.tight_layout()
adicionaLegendaNasBarras(fig1)
plt.savefig(f'./{pastaGraficos}/casosMes.png', format='png', dpi=300)
# plt.show()

# Cria o gráfico dos óbitos
plt.figure(figsize=(16, 7))
fig2 = plt.bar(meses, obitosMes, ec="k", alpha=.6, color="royalblue")
plt.xticks(np.arange(0, len(meses), 2))
plt.title('Óbitos por mês')
plt.xlabel('Mês')
plt.ylabel('Quantidade de óbitos')
plt.tight_layout()
adicionaLegendaNasBarras(fig2)
plt.savefig(f'./{pastaGraficos}/obitosMes.png', format='png', dpi=300)
# plt.show()

# Cria o PDF com as devidas formatações
pdf = FPDF('P', 'mm', 'A4')
pdf.add_page()
pdf.set_font('helvetica', '', 16)

# Insere as informações
pdf.cell(80,10, "Teste")

# Salva o PDF pronto
pdf.output('relatório.pdf')