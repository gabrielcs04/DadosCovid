# Importações das bibliotecas necessárias
import os
import wget
import math
import pandas as pd
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

# Retorna os meses relacionados aos maiores dados passados
def mesesMaioresDados(maioresDados, dadosMes, meses):
  mesesDosDados = []
  for i in range(len(maioresDados)):
    for j in range(len(dadosMes)):
      if maioresDados[i] == dadosMes[j]:
        mesesDosDados.append(meses[j])
  return mesesDosDados

# Estiliza os gráficos que possuem barras horizontais
def formataGraficoHoriz(titulo, legendaX, legendaY):
  plt.title(titulo, fontsize=22)
  plt.xlabel(legendaX, fontsize=16)
  plt.ylabel(legendaY, fontsize=16)
  plt.gca().invert_yaxis()
  plt.xticks(fontsize=14)
  plt.yticks(fontsize=14)
  plt.tight_layout()

# Estiliza os gráficos que possuem barras verticais
def formataGraficoVerti(titulo, legendaX, legendaY, eixoX):
  plt.title(titulo, fontsize=44)
  plt.xlabel(legendaX, fontsize=32)
  plt.ylabel(legendaY, fontsize=32)
  plt.xticks(fontsize=28)
  plt.yticks(fontsize=28)
  plt.tight_layout()

# Formata casas decimais de um número
def formataNum(num, sep='.'):
  return num if len(num) <= 3 else formataNum(num[:-3], sep) + sep + num[-3:]

# Adiciona legenda nas barras horizontais dos gráficos 
def adicionaLegendaNasBarrasHoriz(grafico, soma):
  for reta in grafico:
    altura = reta.get_height()
    largura = reta.get_width()
    plt.text(largura+soma, reta.get_y()+0.6, formataNum(str(int(largura))), fontsize=12)

# Adiciona legenda nas barras verticais dos gráficos 
def adicionaLegendaNasBarrasVerti(grafico):
  for reta in grafico:
    altura = reta.get_height()
    largura = reta.get_width()
    plt.text(reta.get_x()+largura/2, altura, formataNum(str(int(altura))), ha='center', va='bottom', fontsize=24)

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

maioresCasos = sorted(casosMes)[-5:]
mesesMaisCasos = mesesMaioresDados(maioresCasos, casosMes, meses)

maioresObitos = sorted(obitosMes)[-5:]
mesesMaisObitos = mesesMaioresDados(maioresObitos, obitosMes, meses)


# Tamanho dos gráficos
largura = 17
altura = 11

# Cria o gráfico dos casos
plt.figure(figsize=(largura, altura))
graf1 = plt.barh(meses, casosMes, ec="k", alpha=.6, color="royalblue")
formataGraficoHoriz('Casos novos por mês', 'Quantidade de casos', 'Data')
adicionaLegendaNasBarrasHoriz(graf1, 1000)
plt.savefig('./graficos/casosMes.png', format='png', dpi=300)

# Cria o gráfico dos óbitos
plt.figure(figsize=(largura, altura))
graf2 = plt.barh(meses, obitosMes, ec="k", alpha=.6, color="royalblue")
formataGraficoHoriz('Óbitos por mês', 'Quantidade de óbitos', 'Data')
adicionaLegendaNasBarrasHoriz(graf2, 60)
plt.savefig('./graficos/obitosMes.png', format='png', dpi=300)

# Cria o gráfico dos meses com mais casos
plt.figure(figsize=(largura, altura))
graf3 = plt.bar(mesesMaisCasos, maioresCasos, width=0.5, ec="k", alpha=.6, color="royalblue")
formataGraficoVerti('Meses com mais casos', 'Data', 'Quantidade de casos', mesesMaisCasos)
adicionaLegendaNasBarrasVerti(graf3)
plt.savefig('./graficos/mesesComMaisCasos.png', format='png', dpi=300)

plt.figure(figsize=(largura, altura))
graf4 = plt.bar(mesesMaisObitos, maioresObitos, width=0.5, ec="k", alpha=.6, color="royalblue")
formataGraficoVerti('Meses com mais óbitos', 'Data', 'Quantidade de óbitos', mesesMaisObitos)
adicionaLegendaNasBarrasVerti(graf4)
plt.savefig('./graficos/mesesComMaisObitos.png', format='png', dpi=300)

# Tamanho do PDF
largura = 210
altura = 297

# Cria o PDF
pdf = FPDF('P', 'mm', 'A4')

# Cria a capa do relatório
pdf.add_page()
pdf.image('./imagens/fundoPrincipal.png', 0, 0, largura)

pdf.set_font('helvetica', 'B', 54)
pdf.set_text_color(255, 255, 255)
pdf.cell(0, 50, '', ln=1)
pdf.multi_cell(0, 25, 'Covid-19\nno Estado de\nSão Paulo', align='C', ln=1)

pdf.set_font('helvetica', 'B', 20)
pdf.set_text_color(0, 0, 0)
pdf.cell(0, 125, '', ln=1)
pdf.multi_cell(0, 8, 'Criado por:\nGabriel Costa da Silva', align='C', ln=1)

# Insere o titulo da segunda página
pdf.add_page()
pdf.image('./imagens/fundoSecundario.png', 0, 0, largura)
pdf.set_font('helvetica', 'B', 32)
pdf.set_text_color(255, 255, 255)
pdf.cell(0, 15, 'DADOS GERAIS', ln=1)

# Insere os gráficos dos óbitos e casos mensais
pdf.image('./graficos/casosMes.png', 5, 33, largura-10)
pdf.image('./graficos/obitosMes.png', 5, 163, largura-10)

# Insere o titulo da terceira página
pdf.add_page()
pdf.image('./imagens/fundoSecundario.png', 0, 0, largura)
pdf.set_font('helvetica', 'B', 32)
pdf.set_text_color(255, 255, 255)
pdf.cell(0, 15, 'DADOS ESPECÍFICOS', ln=1)

# Insere os gráficos dos meses com mais casos e óbitos
pdf.image('./graficos/mesesComMaisCasos.png', 5, 33, (largura/2)-10)
pdf.image('./graficos/mesesComMaisObitos.png', (largura/2)+5, 33, (largura/2)-10)

pdf.set_font('helvetica', 'B', 16)
pdf.set_text_color(0, 0, 0)

# Insere uma linha em branco para dar espaço dos gráficos acima
pdf.cell(0, 73, '', ln=1)

# Insere a frase do problema observado
pdf.cell(0, 15, 'Problema observado:', ln=1)
pdf.set_font('helvetica', '', 12)
analise = 'O surgimento de variantes é um grande contratempo para superar a pandemia, visto que os meses que registraram mais casos e mortes foram os quais houve o surgimento de uma determinada variante do vírus da Covid-19.'
pdf.multi_cell(0, 8, analise, align='L')

# Salva o PDF finalizado
pdf.output('Covid-19 no Estado de SP.pdf')