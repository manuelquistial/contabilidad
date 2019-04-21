#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import xlsxwriter
import pandas as pd
import numpy as np
import sys

def fomulaSSValida(file, cols):
    for index0, row0 in file.iterrows():
        suma = 0
        salud = 0
        for index1, row1 in file.iterrows():
            if(row0[cols[0]] == row1[cols[0]]):
                suma = suma + abs(row1[cols[1]])
        salud = int(round(suma * 0.24023))
        file.loc[index0, 'SS'] = salud
        file.loc[index0, 'valida'] = abs(row0['Formula']) - (suma + salud)

def valorFormulaDiferencia(fileOne, fileTwo):
    colC = fileOne.columns.tolist()
    colT = fileTwo.columns.tolist()
    for index, row in fileOne.iterrows():
        value = (fileTwo[colT[0]] == row[colC[0]]) & (fileTwo[colT[6]] == row[colC[6]])
        value = fileTwo[value]
        suma = abs(value[colT[1]]).sum()
        fileOne.loc[index,'Formula'] = suma
        dif = abs(row[colC[1]]) - suma
        fileOne.loc[index,'Diferencia'] = dif
        #Suma iguales valores del archivo base
        value = (fileOne[colC[0]] == row[colC[0]]) & (fileOne[colC[6]] == row[colC[6]])
        value = fileOne[value]
        value = abs(value[colC[1]]).sum()
        fileOne.loc[index, 'valida'] = suma - value

def style(item, row, col, worksheet, cont, format, seguridad, negRecaudos):
    recaudo_positivo = workbook.add_format({'fg_color':'#FFE699'})
    recaudo_positivo_money = workbook.add_format({'fg_color':'#FFE699', 'num_format': '#,##0'})
    if(item == 1):
        if(row[col[1]]) > 0:
            worksheet.set_row(cont,None, recaudo_positivo)
            worksheet.write(cont, 1,  row[col[1]], recaudo_positivo_money)
            worksheet.write(cont, len(col)-4, '=SUMAR.SI.CONJUNTO(Ingresos_SIGEP!B:B,Ingresos_SIGEP!A:A,Recaudos_SAP!A'+str(cont+1)+',Ingresos_SIGEP!G:G,Recaudos_SAP!G:G)', recaudo_positivo_money)
            worksheet.write(cont, len(col)-3, '=ABS(B'+str(cont+1)+')-'+xlsxwriter.utility.xl_col_to_name(len(col)-4)+str(cont+1), recaudo_positivo_money)
        else:
            negRecaudos.append('B'+str(cont+1))
            worksheet.write(cont, 1,  row[col[1]], format)
            worksheet.write(cont, len(col)-4, '=SUMAR.SI.CONJUNTO(Ingresos_SIGEP!B:B,Ingresos_SIGEP!A:A,Recaudos_SAP!A'+str(cont+1)+',Ingresos_SIGEP!G:G,Recaudos_SAP!G:G)', format)
            worksheet.write(cont, len(col)-3, '=ABS(B'+str(cont+1)+')-'+xlsxwriter.utility.xl_col_to_name(len(col)-4)+str(cont+1), format)
    elif(item == 2):
        worksheet.write(cont, 11, '=SUMAR.SI.CONJUNTO(Recaudos_SAP!B:B,Recaudos_SAP!A:A,Ingresos_SIGEP!A'+str(cont+1)+',Recaudos_SAP!G:G,Ingresos_SIGEP!G:G)', format)
        worksheet.write(cont, 1, row[col[1]], format)
        worksheet.write(cont, 12, '=B'+str(cont+1)+'-L'+str(cont+1), format)
    elif(item == 3):
        worksheet.write(cont, len(col)-5, '=SUMAR.SI.CONJUNTO(Egresos_SIGEP!B:B,Egresos_SIGEP!A:A,Pagos_SAP!A'+str(cont+1)+',Egresos_SIGEP!G:G,Pagos_SAP!G:G)', format)
        worksheet.write(cont, 1, row[col[1]], format)
        worksheet.write(cont, len(col)-4, '=B'+str(cont+1)+'-'+xlsxwriter.utility.xl_col_to_name(len(col)-5)+str(cont+1), format)
        if(str(row[col[20]]).lower() == 'salario'):
            value = seguridad[row[col[0]]]
            value = value + ['B'+str(cont+1)]
            seguridad[row[col[0]]] = value
    elif(item == 4):
        worksheet.write(cont, 11, '=SUMAR.SI.CONJUNTO(Pagos_SAP!B:B,Pagos_SAP!A:A,Egresos_SIGEP!A'+str(cont+1)+',Pagos_SAP!G:G,Egresos_SIGEP!G:G)', format)
        worksheet.write(cont, 1, row[col[1]], format)
        worksheet.write(cont, 12, '=B'+str(cont+1)+'-L'+str(cont+1), format)

def totalesSheets(worksheet, shapes, format, item, total, negRecaudos):
    moneyTotalSap = workbook.add_format({'num_format': '#,##', 'fg_color':'#ffff00'})
    if(item == 2) | (item == 4):
        worksheet.write(shapes, 1, '=SUM(B2:B'+str(shapes)+')', format)
        worksheet.write(shapes, 11, '=SUM(L2:L'+str(shapes)+')', format)
        worksheet.write(shapes, 12, '=SUM(M2:M'+str(shapes)+')', format)
    elif(item == 3):
        worksheet.write(shapes, 1, total[1], moneyTotalSap)
        worksheet.write(shapes+1, 1, '=SUM(B2:B'+str(shapes)+')', format)
        worksheet.write(shapes, 24, '=SUM(Y2:Y'+str(shapes)+')', format)
        worksheet.write(shapes, 25, '=SUM(Z2:Z'+str(shapes)+')', format)
        worksheet.write(shapes, 26, '=SUM(AA2:AA'+str(shapes)+')', format)
    elif(item == 1):
        worksheet.write(shapes, 1, total[2], moneyTotalSap)
        worksheet.write(shapes+1, 1, '=('+('+'.join(negRecaudos))+')', format)
        worksheet.write(shapes, 24, '=SUM(Y2:Y'+str(shapes)+')', format)
        worksheet.write(shapes, 25, '=SUM(Z2:Z'+str(shapes)+')', format)

def verificaDataFrameVacio(worksheet, conciliar, fila, col, dato, tag):
    if(conciliar.empty):
        worksheet.write(fila, col, 0, tag)
    else:
        worksheet.write(fila, col, dato, tag)

currentPattern = [sys.argv[2],sys.argv[3],sys.argv[4]]
dir = sys.argv[5]+"conciliacion/"
dataFrames = {1:'',2:'',3:''}

for item in currentPattern:
    currentFile = item.split('/').pop()
    if(str(currentFile).lower() == 'general_sigep_'+sys.argv[6]+'.xlsx'):
        dataFrames[1]= pd.read_excel(dir+currentFile)
    elif(str(currentFile).lower() == 'pagos_sap_'+sys.argv[6]+'.xlsx'):
        dataFrames[2]= pd.read_excel(dir+currentFile)
    elif(str(currentFile).lower() == 'recaudos_sap_'+sys.argv[6]+'.xlsx'):
        dataFrames[3]= pd.read_excel(dir+currentFile)

generalSigep = dataFrames[1]
pagosSap = dataFrames[2]
recaudosSap = dataFrames[3]

#generalSigep
generalSigepItems = {1:'',2:''}
items =  {1:'Ingreso',2:'Egreso'}
for sigep in generalSigepItems:
    values = generalSigep['Unnamed: 2'] == items[sigep]
    generalSigepItems[sigep] = generalSigep[values]
    values = generalSigepItems[sigep]
    month = pd.DatetimeIndex(values['Unnamed: 3'])
    values['Periodo'] = month.month
    cols = values.columns.tolist()
    cols = [cols[9]] + [cols[7]] + cols[0:4] + [cols[10]] + cols[4:7] + [cols[8]]
    values = values[cols]
    fecha = pd.to_datetime(values[cols[5]], format = '%m/%d/%Y')
    values.update(fecha)
    ref = values[cols[0]].astype('int64')
    values.update(ref)
    values['Formula'] = 0
    values['Diferencia'] = 0
    values['Observaciones'] = 0
    values['valida'] = 0
    generalSigepItems[sigep] = values

totaDetSap = {1:'', 2:''}
#pagosSap
cols = pagosSap.columns.tolist()
cols = [cols[7]] + [cols[5]] + cols[0:5]+ [cols[6]] + cols[8:]
totaDetSap[1] = pagosSap.loc[pagosSap.shape[0]-1,cols[1]]
pagosSap = pagosSap[cols]
pagosSap = pagosSap[:-1]
fecha = pagosSap[cols[5]].dt.strftime('%m/%d/%Y')
pagosSap.update(fecha)
fecha = pagosSap[cols[17]].dt.strftime('%m/%d/%Y')
pagosSap.update(fecha)
pagosSap['Formula'] = 0
pagosSap['Diferencia'] = 0
pagosSap['SS'] = 0
pagosSap['Observaciones'] = 0
pagosSap['valida'] = 0

#recaudosSap
cols = recaudosSap.columns.tolist()
cols = [cols[6]] + [cols[5]] + cols[0:5] + cols[7:]
totaDetSap[2] = recaudosSap.loc[recaudosSap.shape[0]-1,cols[1]]
recaudosSap = recaudosSap[cols]
recaudosSap = recaudosSap[:-1]
fecha = recaudosSap[cols[5]].dt.strftime('%m/%d/%Y')
recaudosSap.update(fecha)
fecha = recaudosSap[cols[17]].dt.strftime('%m/%d/%Y')
recaudosSap.update(fecha)
recaudosSap['Formula'] = 0
recaudosSap['Diferencia'] = 0
recaudosSap['Observaciones'] = 0
recaudosSap['valida'] = 0

#pagosSap
cols = pagosSap.columns.tolist()
nanValues = pagosSap.apply(lambda s: str(s[cols[0]]).lower() == 'nan', axis=1)
newPagosSap = pagosSap[nanValues]
for index, row in newPagosSap.iterrows():
    val = str(row[cols[4]])
    if(val[0:2] == '81') | (val[0:5] == '10000'):
        newPagosSap.loc[index,cols[0]] = int(row[cols[4]])
    else:
        newPagosSap.loc[index,cols[0]] = int(row[cols[2]])
pagosSap.update(newPagosSap)

#Formula y diferencia
valorFormulaDiferencia(generalSigepItems[1], recaudosSap)
valorFormulaDiferencia(recaudosSap, generalSigepItems[1])
valorFormulaDiferencia(generalSigepItems[2], pagosSap)
valorFormulaDiferencia(pagosSap, generalSigepItems[2])

#Calculo seguridad
salario = pagosSap.apply(lambda s: str(s[cols[20]]).lower() == 'salario', axis=1)
newPagosSap = pagosSap[salario]

salarioEps = newPagosSap[[cols[0]] + [cols[1]]]
salarioEps = salarioEps.groupby([cols[0]]).sum()
salarioEps = salarioEps.reset_index()
salarioEps = dict.fromkeys(salarioEps[cols[0]], [])

fomulaSSValida(newPagosSap, cols)
pagosSap.update(newPagosSap)

#seguridad
colP = pagosSap.columns.tolist()
colR = generalSigepItems[2].columns.tolist()
ssSap = pagosSap.apply(lambda s: str(s[colP[4]]).lower()[0:6] == 'automn', axis=1)
ssSigep = generalSigepItems[2].apply(lambda s: str(s[colR[9]]).lower()[0:2] == 'ss', axis=1)
ssSap = pagosSap[ssSap]
ssSigep = generalSigepItems[2][ssSigep]

''' TITULOS SIGEP '''
titulosSigep=['Número de Soporte','Valor','Proyecto','Codigo','Tipo','Fecha','Periodo','Referencia','Nit/Cédula','Observación','Tipo de Soporte',' Formula','Diferencia','Observaciones','valida']
generalSigepItems[1].columns = titulosSigep
generalSigepItems[2].columns = titulosSigep
ssSigep.columns = titulosSigep

cols = recaudosSap.columns.tolist()
ingreso = generalSigepItems[1]
egreso = generalSigepItems[2]
seguridadSap = ssSap
seguridadSigep = ssSigep
pagos = pagosSap
recaudos = recaudosSap

positivosRecaudos = recaudos.apply(lambda s: s[cols[1]] > 0, axis=1)
positivosRecaudos = recaudos[positivosRecaudos]

recaudosValidar = recaudos.apply(lambda s: (s['valida'] != 0) & (s[cols[1]] <= 0), axis=1)
recaudosValidar = recaudos[recaudosValidar]
cols = recaudosValidar.columns.tolist()
recaudosValidar = recaudosValidar[[cols[0]]+ [cols[1]]]
recaudosValidar = recaudosValidar.groupby([cols[0]]).sum()
recaudosValidar = recaudosValidar.reset_index()

pagosValidar = pagos.apply(lambda s: (s['valida'] != 0) & (s['Diferencia'] != 0) & (str(s[cols[4]]).lower()[0:6] != 'automn'), axis=1)
pagosValidar = pagos[pagosValidar]
cols = pagosValidar.columns.tolist()
pagosValidar = pagosValidar[[cols[0]]+ [cols[1]]]
pagosValidar = pagosValidar.groupby([cols[0]]).sum()
pagosValidar = pagosValidar.reset_index()

''' SE CREA EL ARCHIVO DE EXCEL'''
writer = pd.ExcelWriter(sys.argv[5]+'files_out/Centro_de_Costos_'+str(sys.argv[1])+'_'+sys.argv[6]+'.xlsx', engine='xlsxwriter')

sheets = {1:'Recaudos_SAP',2:'Ingresos_SIGEP',3:'Pagos_SAP',4:'Egresos_SIGEP'}

#Se crea conciliacion de recaudos
pd.DataFrame().to_excel(writer, sheet_name='Conciliación', index=False)

recaudosV = recaudos.drop('valida', 1)
recaudosV.to_excel(writer, index=False, sheet_name=sheets[1])
ingresoV = ingreso.drop('valida', 1)
ingresoV.to_excel(writer, index=False, sheet_name=sheets[2])
pagosV = pagos.drop('valida', 1)
pagosV.to_excel(writer, index=False, sheet_name=sheets[3])
egresoV = egreso.drop('valida', 1)
egresoV.to_excel(writer, index=False, sheet_name=sheets[4])

''' ESTILOS '''
workbook = writer.book
merge_center = workbook.add_format({
    'align': 'center',
    'valign': 'vcenter'})
merge_format = workbook.add_format({
    'bold': 1,
    'align': 'center',
    'valign': 'vcenter',
    'fg_color': '#acb9ca'})
merge_bold = workbook.add_format({
    'bold': 1,
    'align': 'center',
    'valign': 'vcenter'})
merge_bold_color = workbook.add_format({
    'bold': 1,
    'align': 'center',
    'valign': 'vcenter',
    'fg_color': '#ededed'})

cell_size = 20
bold = workbook.add_format({'bold': 1})
bold_money = workbook.add_format({'bold': 1, 'num_format': '#,##0'})
money = workbook.add_format({'num_format': '#,##0'})
title = workbook.add_format({'fg_color': '#C6E0B4'})
titleConciliacion = workbook.add_format({'bold': 1, 'fg_color': '#FCE4D6'})

''' Conciliacion '''
worksheet = writer.sheets['Conciliación']
worksheet.set_column('A:E', cell_size, None)
worksheet.merge_range('A1:E2', 'CONCILIACIÓN CENTRO DE COSTOS '+str(sys.argv[1]), merge_format)
worksheet.merge_range('A4:C4', 'Ingresos', merge_bold_color)
worksheet.write(3, 3, 'SAP', merge_bold_color)
worksheet.write(3, 4, 'SIGEP', merge_bold_color)

cols = positivosRecaudos.columns.tolist()
shapePositivos = positivosRecaudos.shape
if(positivosRecaudos.empty):
    inicial = 6
else:
    inicial = 5
cont = inicial
for index, row in positivosRecaudos.iterrows():
    worksheet.merge_range('A'+str(cont+1)+':C'+str(cont+1), 'Menos ingreso '+str(int(row[cols[0]]))+' (en positivo no se registra)', merge_center)
    worksheet.write(cont, 3, row[cols[1]], money)
    cont = cont + 1

cols = recaudosValidar.columns.tolist()
shapeRecaudosV = recaudosValidar.shape
cont = shapePositivos[0] + 5
for index, row in recaudosValidar.iterrows():
    worksheet.merge_range('A'+str(cont+1)+':C'+str(cont+1), int(row[cols[0]]), merge_center)
    worksheet.write(cont, 4, row[cols[1]], money)
    cont = cont + 1

worksheet.merge_range('A'+str(shapePositivos[0]+shapeRecaudosV[0]+7)+':C'+str(shapePositivos[0]+shapeRecaudosV[0]+7), 'Total', merge_bold)
worksheet.write(shapePositivos[0]+shapeRecaudosV[0]+6, 3, '=D5-SUM(D6:D'+str(shapePositivos[0]+inicial)+')', money)
worksheet.write(shapePositivos[0]+shapeRecaudosV[0]+6, 4, '=E5-SUM(E'+str(shapePositivos[0]+inicial)+':E'+str(shapePositivos[0]+shapeRecaudosV[0]+inicial)+')', money)
worksheet.merge_range('A'+str(shapePositivos[0]+shapeRecaudosV[0]+8)+':C'+str(shapePositivos[0]+shapeRecaudosV[0]+8), 'Diferencias', merge_bold)
worksheet.write(shapePositivos[0]+shapeRecaudosV[0]+7, 4, '=D'+str(shapePositivos[0]+shapeRecaudosV[0]+7)+'-E'+str(shapePositivos[0]+shapeRecaudosV[0]+7), bold_money)

cols = pagosValidar.columns.tolist()
shapePagosValida = pagosValidar.shape
worksheet.merge_range('A'+str(shapePositivos[0]+shapeRecaudosV[0]+10)+':C'+str(shapePositivos[0]+shapeRecaudosV[0]+10), 'Egresos', merge_bold_color)
worksheet.write(shapePositivos[0]+shapeRecaudosV[0]+9, 3, 'SAP', merge_bold_color)
worksheet.write(shapePositivos[0]+shapeRecaudosV[0]+9, 4, 'SIGEP', merge_bold_color)

cont = shapePositivos[0]+shapeRecaudosV[0]+12
for index, row in pagosValidar.iterrows():
    worksheet.merge_range('A'+str(cont+1)+':C'+str(cont+1), int(row[cols[0]]), merge_center)
    worksheet.write(cont, 4, row[cols[1]], money)
    cont = cont + 1


worksheet.merge_range('A'+str(shapePagosValida[0]+shapePositivos[0]+shapeRecaudosV[0]+14)+':C'+str(shapePagosValida[0]+shapePositivos[0]+shapeRecaudosV[0]+14), 'Total', merge_bold)
worksheet.write(shapePagosValida[0]+shapePositivos[0]+shapeRecaudosV[0]+13, 3, '=D'+str(shapePositivos[0]+shapeRecaudosV[0]+11), money)
worksheet.write(shapePagosValida[0]+shapePositivos[0]+shapeRecaudosV[0]+13, 4, '=SUM(E'+str(shapePositivos[0]+shapeRecaudosV[0]+11)+':E'+str(shapePagosValida[0]+shapeRecaudosV[0]+shapePositivos[0]+12)+')', money)
worksheet.merge_range('A'+str(shapePagosValida[0]+shapePositivos[0]+shapeRecaudosV[0]+15)+':C'+str(shapePagosValida[0]+shapePositivos[0]+shapeRecaudosV[0]+15), 'Diferencias', merge_bold)
worksheet.write(shapePagosValida[0]+shapePositivos[0]+shapeRecaudosV[0]+14, 4, '=D'+str(shapePagosValida[0]+shapePositivos[0]+shapeRecaudosV[0]+14)+'-E'+str(shapePagosValida[0]+shapePositivos[0]+shapeRecaudosV[0]+14), bold_money)

''' HOJA DE SEGURIDAD SOCIAL SS '''
cols = seguridadSap.columns.tolist()
cols = [cols[0]] + [cols[1]] + cols[4:7] + [cols[9]] + cols[20:22]
seguridadSap = seguridadSap[cols]
shapeSAP = seguridadSap.shape
seguridadSap.to_excel(writer, sheet_name='SS', startrow=1, header=False, index=False)
worksheet = writer.sheets['SS']
worksheet.write(shapeSAP[0]+1, 1,  '=SUM(B2:B'+str(shapeSAP[0]+1)+')', bold_money)
worksheet.write(0, 0, 'SS SAP', bold)
worksheet.set_column('A:AB', cell_size, None)
worksheet.set_column('B:B', None, money)

cols = seguridadSigep.columns.tolist()
seguridadSigep = seguridadSigep[cols[0:11]]
shapeSIGEP = seguridadSigep.shape

seguridadSigep.to_excel(writer, sheet_name='SS', startrow=shapeSAP[0]+5, header=False, index=False)

worksheet = writer.sheets['SS']
worksheet.write(shapeSAP[0]+shapeSIGEP[0]+5, 1,  '=SUM(B'+str(shapeSAP[0]+6)+':B'+str(shapeSAP[0]+shapeSIGEP[0]+5)+')', bold_money)
worksheet.write(shapeSAP[0]+4, 0, 'SS SIGEP', bold)

worksheet.write(shapeSAP[0]+shapeSIGEP[0]+7, 0, 'SAP')
verificaDataFrameVacio(worksheet, seguridadSap, shapeSAP[0]+shapeSIGEP[0]+7, 1, '=B'+str(shapeSAP[0]+2), money)
worksheet.write(shapeSAP[0]+shapeSIGEP[0]+8, 0, 'SIGEP')
verificaDataFrameVacio(worksheet, seguridadSigep, shapeSAP[0]+shapeSIGEP[0]+8, 1, '=B'+str(shapeSAP[0]+shapeSIGEP[0]+6), money)
worksheet.write(shapeSAP[0]+shapeSIGEP[0]+9, 0, 'Diferencia')
worksheet.write(shapeSAP[0]+shapeSIGEP[0]+9, 1, '=B'+str(shapeSAP[0]+shapeSIGEP[0]+8)+'-B'+str(shapeSAP[0]+shapeSIGEP[0]+9), bold_money)

for item in sheets:
    if(item % 2) != 0:
        worksheet = writer.sheets[sheets[item]]
        worksheet.set_column('A:'+xlsxwriter.utility.xl_col_to_name(pagos.shape[1]-2), cell_size, None)
        worksheet.autofilter('A1:'+xlsxwriter.utility.xl_col_to_name(pagos.shape[1]-2)+'1')
        worksheet.set_column('C:D', None, None, {'hidden': True})
        worksheet.set_column('H:I', None, None, {'hidden': True})
        worksheet.set_column('K:T', None, None, {'hidden': True})
        worksheet.set_column('W:W', None, None, {'hidden': True})
        if(xlsxwriter.utility.xl_col_to_name(pagos.shape[1]-5) != 'Y'):
            worksheet.set_column('Y:'+xlsxwriter.utility.xl_col_to_name(pagos.shape[1]-6), None, None, {'hidden': True})

    elif(item % 2) == 0:
        worksheet = writer.sheets[sheets[item]]
        worksheet.set_column('A:N', cell_size, None)
        worksheet.autofilter('A1:N1')

correct_info = workbook.add_format({'fg_color': '#C6E0B4'})
correct_info_money = workbook.add_format({'fg_color': '#C6E0B4', 'num_format': '#,##0'})
ss_info  = workbook.add_format({'fg_color': '#FFFF00'})
ss_info_money  = workbook.add_format({'fg_color': '#FFFF00', 'num_format': '#,##0'})
wrong_info  = workbook.add_format({'fg_color': '#F8CBAD'})
wrong_info_money  = workbook.add_format({'fg_color': '#F8CBAD', 'num_format': '#,##0'})

''' ESTILO DE RECAUDOS - INGRESOS- PAGOS - EGRESOS '''
dataFrames = {1:'',2:'',3:'',4:''}
dataFrames[1] = recaudos
dataFrames[2] = ingreso
dataFrames[3] = pagos
dataFrames[4] = egreso
totales = {1:'',2:'',3:'',4:''}

for item in dataFrames:
    posNegRecaudos = []
    worksheet = writer.sheets[sheets[item]]
    shapes = dataFrames[item].shape
    shapes = shapes[0] + 2
    totales[item] = shapes
    col = dataFrames[item].columns.tolist()
    cont = 1
    for index, row in dataFrames[item].iterrows():
        if (row['valida'] == 0) | (row['Diferencia'] == 0):
            worksheet.set_row(cont,None,correct_info)
            style(item, row, col, worksheet, cont, correct_info_money, salarioEps, posNegRecaudos)
        else:
            worksheet.set_row(cont,None, wrong_info)
            style(item, row, col, worksheet, cont, wrong_info_money, salarioEps, posNegRecaudos)

        if (str(row[col[4]]).lower()[0:6] == 'automn') | (str(row[col[9]]).lower()[0:2] == 'ss'):
            worksheet.set_row(cont,None, ss_info)
            style(item, row, col, worksheet, cont, ss_info_money, salarioEps, posNegRecaudos)
        cont = cont + 1
    totalesSheets(worksheet, shapes-1, money, item, totaDetSap, posNegRecaudos)
    worksheet.set_row(0, 30, title)

col = dataFrames[3].columns.tolist()
worksheet = writer.sheets[sheets[3]]
salud = workbook.add_format({'num_format': '#,##0'})
cont = 1
for index, row in dataFrames[3].iterrows():
    if(str(row[col[20]]).lower() == 'salario'):
        value = salarioEps[row[col[0]]]
        if (row['valida'] == 0) | (row['Diferencia'] == 0):
            worksheet.write(cont, len(col)-3, '=('+('+'.join(value))+')*24.023%', correct_info_money)  
        else:
            worksheet.write(cont, len(col)-3, '=('+('+'.join(value))+')*24.023%', wrong_info_money)  
    cont = cont + 1

''' TOTALES EN CONCILIACION'''
worksheet = writer.sheets['Conciliación']
#Ingresos
worksheet.merge_range('A5:C5', 'Notas', merge_center)
worksheet.merge_range('A'+str(shapePositivos[0]+shapeRecaudosV[0]+11)+':C'+str(shapePositivos[0]+shapeRecaudosV[0]+11), 'Notas', merge_center)
worksheet.merge_range('A'+str(shapePositivos[0]+shapeRecaudosV[0]+12)+':C'+str(shapePositivos[0]+shapeRecaudosV[0]+12), 'Más SS Social Cobrada de Mas al CC', merge_center)
verificaDataFrameVacio(worksheet, dataFrames[3], 4, 3, '=Recaudos_SAP!B'+str(totales[1]+1), money)
verificaDataFrameVacio(worksheet, generalSigepItems[1], 4, 4, '=Ingresos_SIGEP!B'+str(totales[2]), money)
verificaDataFrameVacio(worksheet, dataFrames[2], shapePositivos[0]+shapeRecaudosV[0]+10, 3, '=Pagos_SAP!B'+str(totales[3]+1), money)
verificaDataFrameVacio(worksheet, generalSigepItems[2], shapePositivos[0]+shapeRecaudosV[0]+10, 4, '=Egresos_SIGEP!B'+str(totales[4]), money)
worksheet.write(shapePositivos[0]+shapeRecaudosV[0]+11, 4, '=SS!B'+str(shapeSAP[0]+shapeSIGEP[0]+10), money)

# Close the Pandas Excel writer and output the Excel file.
writer.save()
