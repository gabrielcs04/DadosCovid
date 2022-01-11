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

# Estiliza o gráfico colocando o titulo, as legendas, os valores do eixo X e o tipo do layout
def formataGrafico(titulo, legendaX, legendaY, eixoX):
  plt.title(titulo)
  plt.xlabel(legendaX)
  plt.ylabel(legendaY)
  plt.xticks(np.arange(0, len(eixoX), 2))
  plt.tight_layout()

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

# Tamanho dos gráficos
largura = 17
altura = 8

# Cria o gráfico dos casos
plt.figure(figsize=(largura, altura))
graf1 = plt.bar(meses, casosMes, ec="k", alpha=.6, color="royalblue")
formataGrafico('Casos novos por mês', 'Data', 'Quantidade de casos', meses)
adicionaLegendaNasBarras(graf1)
plt.savefig('./graficos/casosMes.png', format='png', dpi=300)
# plt.show()

# Cria o gráfico dos óbitos
plt.figure(figsize=(largura, altura))
graf2 = plt.bar(meses, obitosMes, ec="k", alpha=.6, color="royalblue")
formataGrafico('Óbitos por mês', 'Data', 'Quantidade de óbitos', meses)
adicionaLegendaNasBarras(graf2)
plt.savefig('./graficos/obitosMes.png', format='png', dpi=300)
# plt.show()

# Tamanho do PDF
largura = 210
altura = 297

# Cria o PDF com as devidas formatações
pdf = FPDF('P', 'mm', 'A4')
pdf.add_page()
pdf.set_font('helvetica', '', 16)

# Insere as informações no PDF
pdf.image('./imagens/cabecalho.png', 0, 0, largura)
pdf.image('./graficos/casosMes.png', 0, 80, w=largura)

# Salva o PDF finalizado
pdf.output('relatório.pdf')