#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import sys

def styleReservas(item, row, col, worksheet, cont, format):
    if(item == 1):
        worksheet.write(cont, 5, row[col[5]], format)
    elif(item == 2):
        worksheet.write(cont, 1, row[col[1]], format)

currentPattern = [sys.argv[2],sys.argv[3]]
dir = sys.argv[4]+"reservas/"

dataFrames = {1:'',2:''}

for item in currentPattern:
    currentFile = item.split('/').pop()
    if(str(currentFile) == 'reservas_sap_'+sys.argv[5]+'.xlsx'):
        dataFrames[1]= pd.read_excel(dir+currentFile)
    elif(str(currentFile)== 'reservas_sigep_'+sys.argv[5]+'.xlsx'):
        dataFrames[2]= pd.read_excel(dir+currentFile)

reservasSap = dataFrames[1]
reservasSigep = dataFrames[2]

#ReservasSigep
reservasSigepItems = {1:'',2:''}
items =  {1:'Reserva',2:'Egreso'}
for sigep in reservasSigepItems:
    values = reservasSigep['Unnamed: 2'] == items[sigep]
    reservasSigepItems[sigep] = reservasSigep[values]
    values = reservasSigep[values]
    month = pd.DatetimeIndex(values['Unnamed: 3'])
    values.loc[values.index.tolist(),'Periodo'] = month.month
    cols = values.columns.tolist()
    cols = [cols[9]] + [cols[7]] + cols[0:4] + [cols[10]] + cols[4:7] + [cols[8]]
    values = values[cols]
    fecha = values[cols[5]].dt.strftime('%m/%d/%Y')
    values.update(fecha)
    values.loc[values.index.tolist(),'valida'] = 0
    reservasSigepItems[sigep] = values

string = reservasSigepItems[1][cols[1]].apply(lambda s: type(s) == str)
string = reservasSigepItems[1][string]
reservasSigepItems[1].loc[string.index.tolist(),cols[1]] = 0
string = reservasSigepItems[2][cols[1]].apply(lambda s: type(s) == str)
string = reservasSigepItems[2][string]
reservasSigepItems[2].loc[string.index.tolist(),cols[1]] = 0

#reservasSap
colRSa = reservasSap.columns.tolist()
colS = reservasSigepItems[1].columns.tolist()
reservasSap = reservasSap[:-1]
fecha = reservasSap[colRSa[3]].dt.strftime('%m/%d/%Y')
reservasSap.update(fecha)
fecha = reservasSap[colRSa[17]].dt.strftime('%m/%d/%Y')
reservasSap.update(fecha)
reservasSap.loc[reservasSap.index.tolist(),'valida'] = 0
iteration = reservasSap.groupby([colRSa[0]]).mean().reset_index()
reservasSapResumen = reservasSap[[colRSa[0]] + [colRSa[5]]]

sumReservaSap = reservasSapResumen.groupby([colRSa[0]]).sum()
sumReservaSap = sumReservaSap.reset_index()
ceroSumReservaSap = sumReservaSap.loc[sumReservaSap[colRSa[5]] == 0]

egreso = reservasSigepItems[2][[colS[0]]+ [colS[1]]]
egresoResumen = egreso.groupby([colS[0]]).sum()
egresoResumen = egresoResumen.reset_index()

positivoSap = reservasSapResumen.loc[reservasSapResumen[colRSa[5]] > 0]
positivoSapResumen = positivoSap.groupby([colRSa[0]]).sum()
positivoSapResumen = positivoSapResumen.reset_index()

filasCorrectas = pd.DataFrame()
for index, row in ceroSumReservaSap.iterrows():
    reserva = reservasSigepItems[1].loc[reservasSigepItems[1][colS[0]] == row[colRSa[0]]]
    sumaEgreso = egresoResumen[colS[0]] == row[colRSa[0]]
    sumaEgreso = egresoResumen[sumaEgreso]
    sumaEgreso = sumaEgreso[colS[1]].sum()
    sumaPositivoSap = positivoSapResumen[colRSa[0]] == row[colRSa[0]]
    sumaPositivoSap = positivoSapResumen[sumaPositivoSap]
    sumaPositivoSap = sumaPositivoSap[colRSa[5]].sum()
    if(sumaEgreso  == sumaPositivoSap) & (reserva.empty):
        filasCorrectas = filasCorrectas.append(ceroSumReservaSap.loc[index])

for index, row in filasCorrectas.iterrows():
    egreso = reservasSigepItems[2].loc[reservasSigepItems[2][colS[0]] == row[colRSa[0]]]
    value = reservasSap.loc[reservasSap[colRSa[0]] == row[colRSa[0]]]
    reservasSigepItems[2].loc[egreso.index.tolist(),'valida'] = 1
    reservasSap.loc[value.index.tolist(),'valida'] = 1

''' SE CREA EL ARCHIVO DE EXCEL'''
writer = pd.ExcelWriter(sys.argv[4]+'files_out/Reservas_'+str(sys.argv[1])+'_'+sys.argv[5]+'.xlsx', engine='xlsxwriter')
''' ESTILOS '''
workbook = writer.book
cell_size = 20
money = workbook.add_format({'num_format': '#,##0'})
title = workbook.add_format({'fg_color': '#C6E0B4'})

''' RESERVAS '''
sheetsReservas = {1:'Reservas_SAP',2:'Reservas_SIGEP'}
#Reservas SAP
reservasSapV = reservasSap.drop('valida', 1)
reservasSapV.to_excel(writer, index=False, sheet_name=sheetsReservas[1])
worksheet = writer.sheets[sheetsReservas[1]]
worksheet.set_column('A:X', cell_size, None)
worksheet.set_column('F:F', None, money)
worksheet.autofilter('A1:X1')

''' TITULOS SIGEP '''
titulosSigep=['Número de Soporte','Valor','Proyecto','Codigo','Tipo','Fecha','Periodo','Referencia','Nit/Cédula','Observación','Tipo de Soporte',' Formula','Diferencia','Observaciones','valida']

#Reservas SIGEP
reservasSigep = reservasSigepItems[1]
reservasSigep = reservasSigep.append(reservasSigepItems[2], ignore_index=True)
reservasSigep.columns = titulosSigep[0:11] + [titulosSigep[14]]
reservaSigepV = reservasSigep.drop('valida', 1)
reservaSigepV.to_excel(writer, sheet_name=sheetsReservas[2], index=False)
worksheet = writer.sheets[sheetsReservas[2]]
worksheet.set_row(0, 30, title)
worksheet.set_column('A:K', cell_size, None)
worksheet.set_column('B:B', None, money)
worksheet.autofilter('A1:K1')

correct_info = workbook.add_format({'fg_color': '#C6E0B4'})
correct_info_money = workbook.add_format({'fg_color': '#C6E0B4', 'num_format': '#,##0'})
wrong_info  = workbook.add_format({'fg_color': '#F8CBAD'})
wrong_info_money  = workbook.add_format({'fg_color': '#F8CBAD', 'num_format': '#,##0'})

''' ESTILO DE RESERVAS SIGEP Y SAP'''
dataFrames = {1:'',2:''}
dataFrames[1] = reservasSap
dataFrames[2] = reservasSigep
totalReserva = {1:'',2:''}
for item in dataFrames:
    worksheet = writer.sheets[sheetsReservas[item]]
    shapes = dataFrames[item].shape
    shapes = shapes[0] + 1
    totalReserva[item] = shapes
    col = dataFrames[item].columns.tolist()
    for index, row in dataFrames[item].iterrows():
        index = index + 1
        if (row['valida'] == 0):
            worksheet.set_row(index,None, wrong_info)
            styleReservas(item, row, col, worksheet, index, wrong_info_money)
        else:
            worksheet.set_row(index,None,correct_info)
            styleReservas(item, row, col, worksheet, index, correct_info_money)
    worksheet.set_row(0, 30, title)

worksheet.write(totalReserva[1], 5, '=SUM(F2:F'+str(totalReserva[1])+')', money)
worksheet.write(totalReserva[2], 1, '=SUM(B2:B'+str(totalReserva[2])+')', money)

# Close the Pandas Excel writer and output the Excel file.
writer.save()
