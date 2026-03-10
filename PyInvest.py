import math
import random
import datetime
import statistics
import locale

locate.setlocale(locale,LC_ALL, 'pt_BR.UTF-8')
#entradas
capital = float(input('Capital Inicial: '))
aporte = float(input('Aporte Mensal: '))
meses = int(input('Prazo(meses): '))
cdi_anual = float(input('CDI anual (%)'))/100
perc_cdb = float(input('Percentual do CDI (%)'))/100
perc_lci = float(input('Percentual do LCI (%)'))/100
taxa_fii = float()