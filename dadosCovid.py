import os
import wget
import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF


linkCSV = 'https://www.seade.gov.br/wp-content/uploads/coronavirus-files/Dados-covid-19-estado.csv'
nomeCSV = 'dadosCovidEstado.csv'

try:
  os.remove(nomeCSV)
except OSError as e:
  print(f"Erro: {e.strerror}")

wget.download(linkCSV, nomeCSV)