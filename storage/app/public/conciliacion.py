#!/usr/local/bin/python
# -*- coding: utf-8 -*-
from datetime import datetime
import xlsxwriter
import pandas as pd
import numpy as np
import sys

def fomulaSSValida(original, file, cols):
    for index0, row0 in file.iterrows():
        sumaSS = 0
        salud = 0
        value = original[cols[0]] == row0[cols[0]]
        value = original[value]
        suma = value[cols[1]].sum()
        for index1, row1 in file.iterrows():                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
            if(row0[cols[0]] == row1[cols[0]]):
                sumaSS = sumaSS + abs(row1[cols[1]])
        salud = round(sumaSS * porcentaje_salud,1)
        file.loc[index0, 'SS'] = salud
        file.loc[index0, 'valida'] = abs(row0['Formula']) - (suma + int(round(sumaSS * porcentaje_salud)))
        value['valida'] = abs(row0['Formula']) - (suma + int(round(sumaSS * porcentaje_salud)))
        original.update(value)

def valorFormulaDiferencia(fileOne, fileTwo):
    colC = fileOne.columns.tolist()
    colT = fileTwo.columns.tolist()
    for index, row in fileOne.iterrows():
        value = (fileTwo[colT[0]] == row[colC[0]]) & (fileTwo[colT[6]] == row[colC[6]])
        value = fileTwo[value]
        suma = value[colT[1]].sum()
        fileOne.loc[index,'Formula'] = suma
        dif = row[colC[1]] - abs(suma)
        fileOne.loc[index,'Diferencia'] = dif
        #Suma iguales valores del archivo base
        value = (fileOne[colC[0]] == row[colC[0]]) & (fileOne[colC[6]] == row[colC[6]])
        value = fileOne[value]
        value = value[colC[1]].sum()
        fileOne.loc[index, 'valida'] = abs(suma) - abs(value)

def style(item, row, col, worksheet, cont, format, seguridad, posgrados, posgradosPagos, enPos, negRecaudos, date, normal_valor):
    recaudo_positivo = workbook.add_format({'fg_color':'#FFE699'})
    recaudo_positivo_money = workbook.add_format({'fg_color':'#FFE699', 'num_format': '#,##0'})
    recaudo_positivo_date = workbook.add_format({'fg_color':'#FFE699', 'num_format': 'mm/dd/yyyy'})
    if(item == 1):
        if(float(row[col[1]])) > 0:
            worksheet.set_row(cont,None, recaudo_positivo)
            worksheet.write(cont, 1,  row[col[1]], recaudo_positivo_money)
            worksheet.write(cont, len(col)-4, '=SUMAR.SI.CONJUNTO(Ingresos_SIGEP!B:B,Ingresos_SIGEP!A:A,Recaudos_SAP!A'+str(cont+1)+',Ingresos_SIGEP!G:G,Recaudos_SAP!G:G)', recaudo_positivo_money)
            worksheet.write(cont, len(col)-3, '=ABS(B'+str(cont+1)+')-'+xlsxwriter.utility.xl_col_to_name(len(col)-4)+str(cont+1), recaudo_positivo_money)
            worksheet.write(cont, 5, datetime.strptime(row[col[5]], '%Y-%m-%d').date(), recaudo_positivo_date)
            worksheet.write(cont, 14, datetime.strptime(row[col[14]], '%Y-%m-%d').date(), recaudo_positivo_date)
        else:
            negRecaudos.append('B'+str(cont+1))
            worksheet.write(cont, 1,  row[col[1]], format)
            worksheet.write(cont, len(col)-4, '=SUMAR.SI.CONJUNTO(Ingresos_SIGEP!B:B,Ingresos_SIGEP!A:A,Recaudos_SAP!A'+str(cont+1)+',Ingresos_SIGEP!G:G,Recaudos_SAP!G:G)', format)
            worksheet.write(cont, len(col)-3, '=ABS(B'+str(cont+1)+')-'+xlsxwriter.utility.xl_col_to_name(len(col)-4)+str(cont+1), format)
            worksheet.write(cont, 4, row[col[4]], normal_valor)
            worksheet.write(cont, 5, datetime.strptime(row[col[5]], '%Y-%m-%d').date(), date)
            worksheet.write(cont, 14, datetime.strptime(row[col[14]], '%Y-%m-%d').date(), date)
        
        if(enPos == True):
            if(str(row[col[0]]).lower()[0:4] == '4200'):
                valueP = 0
                if(row[col[0]] in posgrados):
                    valueP = posgrados[row[col[0]]]
                    valueP = valueP + ['B'+str(cont+1)]
                    posgrados[row[col[0]]] = valueP
                    if(float(row[col[1]])) > 0:
                        worksheet.write(cont, len(col)-3, '', recaudo_positivo.set_num_format('#,##0'))
                    else:
                        worksheet.write(cont, len(col)-3, '', format)
    elif(item == 2):
        worksheet.write(cont, 11, '=SUMAR.SI.CONJUNTO(Recaudos_SAP!B:B,Recaudos_SAP!A:A,Ingresos_SIGEP!A'+str(cont+1)+',Recaudos_SAP!G:G,Ingresos_SIGEP!G:G)', format)
        worksheet.write(cont, 1, row[col[1]], format)
        worksheet.write(cont, 12, '=B'+str(cont+1)+'-ABS(L'+str(cont+1)+')', format)
        worksheet.write(cont, 5, datetime.strptime(row[col[5]], '%Y-%m-%d %H:%M:%S'), date)
    elif(item == 3):
        worksheet.write(cont, len(col)-5, '=SUMAR.SI.CONJUNTO(Egresos_SIGEP!B:B,Egresos_SIGEP!A:A,Pagos_SAP!A'+str(cont+1)+',Egresos_SIGEP!G:G,Pagos_SAP!G:G)', format)
        worksheet.write(cont, 1, row[col[1]], format)
        worksheet.write(cont, len(col)-4, '=B'+str(cont+1)+'-'+xlsxwriter.utility.xl_col_to_name(len(col)-5)+str(cont+1), format)
        worksheet.write(cont, 5, datetime.strptime(row[col[5]], '%Y-%m-%d').date(), date)
        worksheet.write(cont, 14, datetime.strptime(row[col[14]], '%Y-%m-%d').date(), date)
        value = 0
        if(str(row[col[12]]).lower() == 'salario'):
            value = seguridad[row[col[0]]]
            value = value + ['B'+str(cont+1)]
            seguridad[row[col[0]]] = value
        
        if(enPos == True):
            if(str(row[col[0]]).lower()[0:4] == '4200'):
                valuePP = 0
                if(row[col[0]] in posgradosPagos):
                    valuePP = posgradosPagos[row[col[0]]]
                    valuePP = valuePP + ['B'+str(cont+1)]
                    posgradosPagos[row[col[0]]] = valuePP
    elif(item == 4):
        worksheet.write(cont, 11, '=SUMAR.SI.CONJUNTO(Pagos_SAP!B:B,Pagos_SAP!A:A,Egresos_SIGEP!A'+str(cont+1)+',Pagos_SAP!G:G,Egresos_SIGEP!G:G)', format)
        worksheet.write(cont, 1, row[col[1]], format)
        worksheet.write(cont, 12, '=B'+str(cont+1)+'-L'+str(cont+1), format)
        worksheet.write(cont, 5, datetime.strptime(row[col[5]], '%Y-%m-%d %H:%M:%S'), date)

def totalesSheets(worksheet, shapes, format, item, total, negRecaudos, col, enPos):
    moneyTotalSap = workbook.add_format({'num_format': '#,##', 'fg_color':'#ffff00'})
    if(item == 2) | (item == 4):
        worksheet.write(shapes, 1, '=SUM(B2:B'+str(shapes)+')', format)
        worksheet.write(shapes, 11, '=SUM(L2:L'+str(shapes)+')', format)
        worksheet.write(shapes, 12, '=SUM(M2:M'+str(shapes)+')', format)
    elif(item == 3):
        worksheet.write(shapes, 1, total[1], moneyTotalSap)
        worksheet.write(shapes+1, 1, '=SUM(B2:B'+str(shapes)+')', format)
        worksheet.write(shapes, len(col)-5, '=SUM('+xlsxwriter.utility.xl_col_to_name(len(col)-5)+'2:'+xlsxwriter.utility.xl_col_to_name(len(col)-5)+str(shapes)+')', format)
        worksheet.write(shapes, len(col)-4, '=SUM('+xlsxwriter.utility.xl_col_to_name(len(col)-4)+'2:'+xlsxwriter.utility.xl_col_to_name(len(col)-4)+str(shapes)+')', format)
        worksheet.write(shapes, len(col)-3, '=SUM('+xlsxwriter.utility.xl_col_to_name(len(col)-3)+'2:'+xlsxwriter.utility.xl_col_to_name(len(col)-3)+str(shapes)+')', format)
    elif(item == 1):
        worksheet.write(shapes, 1, total[2], moneyTotalSap)
        worksheet.write(shapes+1, 1, '=('+('+'.join(negRecaudos))+')', format)
        if(enPos == True):
            worksheet.write(shapes, len(col)-8, '=SUM('+xlsxwriter.utility.xl_col_to_name(len(col)-8)+'2:'+xlsxwriter.utility.xl_col_to_name(len(col)-8)+str(shapes)+')', format)
            worksheet.write(shapes, len(col)-7, '=SUM('+xlsxwriter.utility.xl_col_to_name(len(col)-7)+'2:'+xlsxwriter.utility.xl_col_to_name(len(col)-7)+str(shapes)+')', format)
            worksheet.write(shapes, len(col)-6, '=SUM('+xlsxwriter.utility.xl_col_to_name(len(col)-6)+'2:'+xlsxwriter.utility.xl_col_to_name(len(col)-6)+str(shapes)+')', format)
            worksheet.write(shapes, len(col)-5, '=SUM('+xlsxwriter.utility.xl_col_to_name(len(col)-5)+'2:'+xlsxwriter.utility.xl_col_to_name(len(col)-5)+str(shapes)+')', format)
        worksheet.write(shapes, len(col)-4, '=SUM('+xlsxwriter.utility.xl_col_to_name(len(col)-4)+'2:'+xlsxwriter.utility.xl_col_to_name(len(col)-4)+str(shapes)+')', format)
        worksheet.write(shapes, len(col)-3, '=SUM('+xlsxwriter.utility.xl_col_to_name(len(col)-3)+'2:'+xlsxwriter.utility.xl_col_to_name(len(col)-3)+str(shapes)+')', format)

def verificaDataFrameVacio(worksheet, conciliar, fila, col, dato, tag):
    if(conciliar.empty):
        worksheet.write(fila, col, 0, tag)
    else:
        worksheet.write(fila, col, dato, tag)

def uneBancolombia(pago, egreso, colp, cole, rPago, rEgreso):
    sumP = rPago[colp[1]].sum()
    sumE = rEgreso[cole[1]].sum()
    if(sumP == sumE):
        rPago['valida'] = 0
        rEgreso['valida'] = 0
        pago.update(rPago)
        egreso.update(rEgreso)

currentPattern = [sys.argv[2],sys.argv[3],sys.argv[4]]
path = sys.argv[5]+"conciliacion\\"
porcentaje_salud = round(float(sys.argv[7]),5)
porcentaje_ingresos = round(float(sys.argv[8]),4)
dataFrames = {1:'',2:'',3:''}

for item in currentPattern:
    currentFile = item.split('\\').pop()
    if(str(currentFile).lower() == 'general_sigep_'+str(sys.argv[1])+'_'+sys.argv[6]+'.xlsx'):
        dataFrames[1]= pd.read_excel(path+currentFile, encoding="utf-8")
    elif(str(currentFile).lower() == 'pagos_sap_'+str(sys.argv[1])+'_'+sys.argv[6]+'.xlsx'):
        dataFrames[2]= pd.read_excel(path+currentFile, encoding="utf-8")
    elif(str(currentFile).lower() == 'recaudos_sap_'+str(sys.argv[1])+'_'+sys.argv[6]+'.xlsx'):
        dataFrames[3]= pd.read_excel(path+currentFile, encoding="utf-8")

generalSigep = dataFrames[1]
colsInicial = generalSigep.columns.tolist()
pagosSap = dataFrames[2].astype(str)
recaudosSap = dataFrames[3].astype(str)
stringSigep = generalSigep[colsInicial[9]].apply(lambda s: type(s) == str)
stringSigep = generalSigep[stringSigep]
generalSigep.loc[stringSigep.index.tolist(),colsInicial[9]] = 0
generalSigep = generalSigep.astype(str)

#generalSigep
generalSigepItems = {1:'',2:''}
items =  {1:'Ingreso',2:'Egreso'}
for sigep in generalSigepItems:
    values = generalSigep[colsInicial[2]] == items[sigep]
    generalSigepItems[sigep] = generalSigep[values]
    values = generalSigepItems[sigep]
    mon = pd.DatetimeIndex(values[colsInicial[3]])
    values['Periodo'] = mon.month
    cols = values.columns.tolist()
    cols = [cols[9]] + [cols[7]] + cols[0:4] + [cols[10]] + cols[4:7] + [cols[8]]
    values = values[cols]
    ref = values[cols[0]].astype('int64')
    values.update(ref)
    values['Formula'] = 0
    values['Diferencia'] = 0
    values['Observaciones'] = 0
    values['valida'] = 0
    generalSigepItems[sigep] = values

colsInicialN = generalSigepItems[1].columns.tolist()
generalSigepItems[1][colsInicialN[0]] = generalSigepItems[1][colsInicialN[0]].astype(float)
generalSigepItems[1][colsInicialN[1]] = generalSigepItems[1][colsInicialN[1]].astype(float)
generalSigepItems[2][colsInicialN[0]] = generalSigepItems[2][colsInicialN[0]].astype(float)
generalSigepItems[2][colsInicialN[1]] = generalSigepItems[2][colsInicialN[1]].astype(float)

totaDetSap = {1:'', 2:''}
#pagosSap
cols = pagosSap.columns.tolist()
cols = [cols[7]] + [cols[5]] + cols[0:5]+ [cols[6]] + cols[8:]
totaDetSap[1] = float(pagosSap.loc[pagosSap.shape[0]-1,cols[1]])
pagosSap = pagosSap[cols]
pagosSap = pagosSap[:-1]
pagosSap['Formula'] = 0
pagosSap['Diferencia'] = 0
pagosSap['SS'] = 0
pagosSap['Observaciones'] = 0
pagosSap['valida'] = 0

#recaudosSap
enablePos = False
cols = recaudosSap.columns.tolist()
cols = [cols[6]] + [cols[5]] + cols[0:5] + cols[7:]
totaDetSap[2] = float(recaudosSap.loc[recaudosSap.shape[0]-1,cols[1]])
recaudosSap = recaudosSap[cols]
recaudosSap = recaudosSap[:-1]
if(str(sys.argv[1]) == '21930003'):
    enablePos = True
    recaudosSap['Total Ingresos'] = 0
    recaudosSap['% Ingreso Sigep_'+str(porcentaje_ingresos*100)+'%'] = 0
    recaudosSap['Pendiente registrar en proyecto ingresos_'+str(100-(porcentaje_ingresos*100))+'%'] = 0
    recaudosSap['Deducciones'] = 0
recaudosSap['Formula'] = 0
recaudosSap['Diferencia'] = 0
recaudosSap['Observaciones'] = 0
recaudosSap['valida'] = 0
recaudosSap[cols[0]] = recaudosSap[cols[0]].astype(float)
recaudosSap[cols[1]] = recaudosSap[cols[1]].astype(float)
recaudosSap[cols[6]] = recaudosSap[cols[6]].astype(float)
recaudosSap[cols[6]] = recaudosSap[cols[6]].astype(int)

#pagosSap
cols = pagosSap.columns.tolist()
nanValues = pagosSap.apply(lambda s: str(s[cols[0]]).lower() == 'nan', axis=1)
newPagosSap = pagosSap[nanValues]
for index, row in newPagosSap.iterrows():
    val = row[cols[4]]
    if(val[0:2] == '81') | (val[0:5] == '10000'):
        newPagosSap.loc[index,cols[0]] = float(row[cols[4]])
    else:
        newPagosSap.loc[index,cols[0]] = float(row[cols[2]])
pagosSap.update(newPagosSap)
pagosSap[cols[0]] = pagosSap[cols[0]].astype(float)
pagosSap[cols[1]] = pagosSap[cols[1]].astype(float)
pagosSap[cols[6]] = pagosSap[cols[6]].astype(float)
pagosSap[cols[6]] = pagosSap[cols[6]].astype(int)

#Formula y diferencia
valorFormulaDiferencia(generalSigepItems[1], recaudosSap)
valorFormulaDiferencia(recaudosSap, generalSigepItems[1])
valorFormulaDiferencia(generalSigepItems[2], pagosSap)
valorFormulaDiferencia(pagosSap, generalSigepItems[2])

'''Sigue aqui'''
ccPosgrados = dict()
ccPosgradosPagos = dict()
#Calculos CC 21930003 POSGRADOS
if(enablePos == True):
    principal = -1

    colI = generalSigepItems[1].columns.tolist()
    ccPSigep = generalSigepItems[1].apply(lambda s: str(s[colI[0]]).lower()[0:4] == '4200', axis=1)
    ccPSigep = generalSigepItems[1][ccPSigep]
    ccPSigepD = ccPSigep[ccPSigep[colI[0]].duplicated() == True]
    if(~ccPSigepD.empty):
        if(ccPSigepD.shape[0] == 1):
            principal = ccPSigepD.iloc[0][colI[0]]
    ingresoPosPrin = ccPSigep[colI[0]] == principal
    ingresoPosPrin = ccPSigep[ingresoPosPrin]

    cols = pagosSap.columns.tolist()
    pagosPosSap = pagosSap.apply(lambda s: (str(s[cols[4]]).lower()[0:4] == '4200') | (str(s[cols[4]]).lower()[0:4] == '5300'), axis=1)
    pagosPosSapD = pagosSap[pagosPosSap]
    for index, row in pagosPosSapD.iterrows():
        pagosPosSapD.loc[index,cols[0]] = int(row[cols[4]])
    pagosSap.update(pagosPosSapD)

    pagosPosSap = pagosSap.apply(lambda s: str(s[cols[4]]).lower()[0:4] == '4200', axis=1)
    pagosPosSap = pagosSap[pagosPosSap]
    totalPosgradosPagos = abs(pagosPosSap[cols[1]]).sum()
    prinEgre = generalSigepItems[2][colI[0]] == principal
    prinEgre = generalSigepItems[2][prinEgre]
    if(~prinEgre.empty):
        if(prinEgre.shape[0] == 1):
            if(prinEgre.iloc[0][colI[1]] == totalPosgradosPagos):
                pagosPosSap['valida'] = 0
                prinEgre['valida'] = 0
                generalSigepItems[2].update(prinEgre)
                pagosSap.update(pagosPosSap)

    cols = recaudosSap.columns.tolist()
    ccPosgradosC = recaudosSap.apply(lambda s: str(s[cols[0]]).lower()[0:4] == '4200', axis=1)
    ccPosgradosC = recaudosSap[ccPosgradosC]

    ccPosgradosF = ccPosgradosC[[cols[0]] + [cols[1]]]
    ccPosgradosF = ccPosgradosF.groupby([cols[0]]).sum()
    ccPosgradosF = ccPosgradosF.reset_index()
    ccPosgrados = dict.fromkeys(ccPosgradosF[cols[0]], [])
    ccPosgradosPagos = dict.fromkeys(ccPosgradosF[cols[0]], [])

    valueProyeIngre = 0
    for item in ccPosgrados:
        valueR = ccPosgradosC[cols[0]] == item
        valueI = generalSigepItems[1][colI[0]] == item
        valueR = ccPosgradosC[valueR]
        valueI = generalSigepItems[1][valueI]
        valueT = abs(valueR[cols[1]]).sum()
        sumaR = int(round(valueT*porcentaje_ingresos))  #FALTA PORCENTAJE
        valueProyeIngre += (valueT - sumaR)
        sumaI = int(abs(valueI[colI[1]]).sum())
        if(sumaR == sumaI):
            valueR['valida'] = 0
            valueI['valida'] = 0
            recaudosSap.update(valueR)
            generalSigepItems[1].update(valueI)

    fecha = generalSigepItems[1][colI[5]]

    for index, row in ingresoPosPrin.iterrows():
        updRecaudo = ccPosgradosC[cols[0]] == row[colI[0]]
        updRecaudo = ccPosgradosC[updRecaudo]
        if(updRecaudo.empty == False):
            valueT = abs(updRecaudo[cols[1]]).sum()
            sumaR = int(round(valueT*porcentaje_ingresos))
            if(sumaR == int(float(row[colI[1]]))):
                updRecaudo['valida'] = 0
                ingresoPosPrin.loc[index,'valida'] = 0
                generalSigepItems[1].update(ingresoPosPrin)
                recaudosSap.update(updRecaudo)

        if int(row[colI[1]]) == valueProyeIngre:
            ingresoPosPrin.loc[index,'valida'] = 0
            generalSigepItems[1].update(ingresoPosPrin)

    generalSigepItems[1][colI[5]] = fecha

cols = pagosSap.columns.tolist()
pagosSap = pagosSap.sort_values(by=[cols[0]])
colRS = recaudosSap.columns.tolist()
recaudosSap = recaudosSap.sort_values(by=[colRS[0]])

colP = pagosSap.columns.tolist()
colE = generalSigepItems[2].columns.tolist()

#UNE EPM PAGOS - EGRESOS
uneEpm = 'une epm telecomunicaciones'
uneEpmP = pagosSap.apply(lambda s: uneEpm in str(s[colP[17]]).lower(), axis=1)
uneEpmP = pagosSap[uneEpmP]
if(uneEpmP.empty == False):
    uneEpmE = generalSigepItems[2].apply(lambda s: uneEpm in str(s[colE[8]]).lower(), axis=1)
    uneEpmE = generalSigepItems[2][uneEpmE]
    uneBancolombia(pagosSap, generalSigepItems[2], colP, colE, uneEpmP, uneEpmE)

#BANCOLOMBIA PAGOS - EGRESOS
bancolombiaP = pagosSap.apply(lambda s: 'bancolombia s.a.' in str(s[colP[17]]).lower(), axis=1)
bancolombiaP = pagosSap[bancolombiaP]
if(bancolombiaP.empty == False):
    bancolombiaE = generalSigepItems[2].apply(lambda s: 'gastos bancarios' in str(s[colE[9]]).lower(), axis=1)
    bancolombiaE = generalSigepItems[2][bancolombiaE]
    uneBancolombia(pagosSap, generalSigepItems[2], colP, colE, bancolombiaP, bancolombiaE)

#APORTES POR DED CONV
cols = pagosSap.columns.tolist()
aportesPDC = pagosSap.apply(lambda s: str(s[cols[12]]).lower() == 'aportes por ded conv', axis=1)
aportesPDC = pagosSap[aportesPDC]
if(aportesPDC.empty == False):
    aportesPDCValue = aportesPDC.iloc[0][cols[0]]
    aportes = generalSigepItems[2][colE[0]] == aportesPDCValue
    aportes = generalSigepItems[2][aportes]
    if(aportes.empty == False):
        aportesPDCSum = aportesPDC[cols[1]].sum()
        if(int(aportesPDCSum) == int(float(aportes.iloc[0][colE[1]]))):
            aportes['valida'] = 0
            aportesPDC['valida'] = 0
            generalSigepItems[2].update(aportes)
            pagosSap.update(aportesPDC)

#Calculo seguridad
cols = pagosSap.columns.tolist()
salario = pagosSap.apply(lambda s: str(s[cols[12]]).lower() == 'salario', axis=1)
newPagosSap = pagosSap[salario]
salarioEps = newPagosSap[[cols[0]] + [cols[1]]]
salarioEps = salarioEps.groupby([cols[0]]).sum()
salarioEps = salarioEps.reset_index()
salarioEps = dict.fromkeys(salarioEps[cols[0]], [])

fomulaSSValida(pagosSap, newPagosSap, cols)
pagosSap.update(newPagosSap)

colE = generalSigepItems[2].columns.tolist()
for item in salarioEps:
    pago = pagosSap[cols[0]] == item
    pago = pagosSap[pago]
    egreso = generalSigepItems[2][colE[0]] == item
    egreso = generalSigepItems[2][egreso]
    if(pago.shape[0] == 1):
        unsoloMEN = pago.apply(lambda s: str(s[cols[4]]).lower()[0:3] == 'men', axis=1)
        unsoloMEN = pago[unsoloMEN]
        if(unsoloMEN.empty == False):
            if(unsoloMEN.iloc[0][cols[1]] == egreso.iloc[0][colE[1]]):
                pago['valida'] = 0
                egreso['valida'] = 0
                pagosSap.update(pago)

    suma = abs(pago['valida']).sum()
    egreso['valida'] = suma
    generalSigepItems[2].update(egreso)

#QUI
qui = pagosSap.apply(lambda s: str(s[cols[4]]).lower()[0:3] == 'qui', axis=1)
qui = pagosSap[qui]
if(qui.empty == False):
    cols = qui.columns.tolist()
    quiSalario = qui.apply(lambda s: str(s[cols[12]]).lower() == 'salario', axis=1)
    quiSalario = qui[quiSalario]
    quiSalario = quiSalario[cols[0]]
    quiSalario = quiSalario.loc[0]

    quiEPagos = generalSigepItems[2][colE[0]] == quiSalario
    quiEPagos = generalSigepItems[2][quiEPagos]
    quiEPagosTotal = abs(quiEPagos[colE[1]]).sum()

    quiN = qui[[cols[0]] + [cols[1]] + ['SS']]
    quiPre = abs(quiN[cols[1]]).sum()
    quiSS = abs(quiN['SS']).sum()
    totalQui = quiPre + int(round(quiSS))
    if(quiEPagosTotal == totalQui):
        qui['valida'] = 0
        quiEPagos['valida'] = 0
        pagosSap.update(qui)
        generalSigepItems[2].update(quiEPagos)

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

positivosRecaudos = recaudos.apply(lambda s: float(s[cols[1]]) > 0, axis=1)
positivosRecaudos = recaudos[positivosRecaudos]

recaudosValidar = recaudos.apply(lambda s: (s['valida'] != 0) & (float(s[cols[1]]) <= 0), axis=1)
recaudosValidar = recaudos[recaudosValidar]
cols = recaudosValidar.columns.tolist()
recaudosValidar = recaudosValidar[[cols[0]]+ [cols[1]]]
recaudosValidar = recaudosValidar.groupby([cols[0]]).sum()
recaudosValidar = recaudosValidar.reset_index()

'''aqui'''
ingresosValidar = ingreso.apply(lambda s: (s['valida'] != 0), axis=1)
ingresosValidar = ingreso[ingresosValidar]
colsI = ingresosValidar.columns.tolist()
ingresosValidar = ingresosValidar[[colsI[0]]+ [colsI[1]]]
ingresosValidar = ingresosValidar.groupby([colsI[0]]).sum()
ingresosValidar = ingresosValidar.reset_index()
#& (s['Diferencia'] != 0)
pagosValidar = pagos.apply(lambda s: (s['valida'] != 0) & (str(s[cols[4]]).lower()[0:6] != 'automn'), axis=1)
pagosValidar = pagos[pagosValidar]
cols = pagosValidar.columns.tolist()
pagosValidar = pagosValidar[[cols[0]]+ [cols[1]]]
pagosValidar = pagosValidar.groupby([cols[0]]).sum()
pagosValidar = pagosValidar.reset_index()
'''aqui'''
colE = egreso.columns.tolist()
egresoValidar = egreso.apply(lambda s: (s['valida'] != 0) & (str(s[colE[9]]).lower()[0:2] != 'ss'), axis=1)
egresoValidar = egreso[egresoValidar]
cols = egresoValidar.columns.tolist()
egresoValidar = egresoValidar[[cols[0]]+ [cols[1]]]
egresoValidar = egresoValidar.groupby([cols[0]]).sum()
egresoValidar = egresoValidar.reset_index()

''' SE CREA EL ARCHIVO DE EXCEL'''
writer = pd.ExcelWriter(sys.argv[5]+'files_out/Centro_de_Costos_'+str(sys.argv[1])+'_'+sys.argv[6]+'.xlsx', 
                        engine='xlsxwriter', 
                        options={'nan_inf_to_errors': True})

sheets = {1:'Recaudos_SAP',2:'Ingresos_SIGEP',3:'Pagos_SAP',4:'Egresos_SIGEP'}

#Se crea conciliacion de recaudos
pd.DataFrame().to_excel(writer, sheet_name='Conciliación', index=False)

recaudosV = recaudos.drop('valida', 1)
recaudosV.to_excel(writer, index=False, sheet_name=sheets[1])

ingresoV = ingreso.drop('valida', 1)
ingresoVAjuste = ingresoV[colE[0]].apply(lambda s: s == 0)
ingresoVAjuste = ingresoV[ingresoVAjuste]
ingresoAjuste = stringSigep[colsInicial[2]] == 'Ingreso'
ingresoAjuste = stringSigep[ingresoAjuste]
ingresoVAjuste.loc[:,colE[0]] = ingresoAjuste[colsInicial[9]]
ingresoV.update(ingresoVAjuste)
ingresoV.to_excel(writer, index=False, sheet_name=sheets[2])

pagosV = pagos.drop('valida', 1)
pagosV.to_excel(writer, index=False, sheet_name=sheets[3])

egresoV = egreso.drop('valida', 1)
egresoVAjuste = egresoV[colE[0]].apply(lambda s: s == 0)
egresoVAjuste = egresoV[egresoVAjuste]
egresoAjuste = stringSigep[colsInicial[2]] == 'Egreso'
egresoAjuste = stringSigep[egresoAjuste]
egresoVAjuste.loc[:,colE[0]] = egresoAjuste[colsInicial[9]]
egresoV.update(egresoVAjuste)
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

cell_size = 12.5
bold = workbook.add_format({'bold': 1})
bold_money = workbook.add_format({'bold': 1, 'num_format': '#,##0'})
money = workbook.add_format({'num_format': '#,##0'})
title = workbook.add_format({'fg_color': '#C6E0B4'})
titleConciliacion = workbook.add_format({'bold': 1, 'fg_color': '#FCE4D6'})
date = workbook.add_format({'num_format': 'mm/dd/yyyy'})

''' Conciliacion '''
worksheet = writer.sheets['Conciliación']
worksheet.set_column('A:E', cell_size, None)
worksheet.merge_range('A1:E2', 'CONCILIACIÓN CENTRO DE COSTOS '+str(sys.argv[1]), merge_format)
worksheet.merge_range('A4:C4', 'Ingresos', merge_bold_color)
worksheet.write(3, 3, 'SAP', merge_bold_color)
worksheet.write(3, 4, 'SIGEP', merge_bold_color)

cols = positivosRecaudos.columns.tolist()
shapePositivos = positivosRecaudos.shape

cont = 5
for index, row in positivosRecaudos.iterrows():
    worksheet.merge_range('A'+str(cont+1)+':C'+str(cont+1), 'Menos ingreso '+str(int(row[cols[0]]))+' (en positivo no se registra)', merge_center)
    worksheet.write(cont, 3, row[cols[1]], money)
    cont = cont + 1

cols = recaudosValidar.columns.tolist()
shapeRecaudosV = recaudosValidar.shape
cont = shapePositivos[0] + 5
for index, row in recaudosValidar.iterrows():
    worksheet.merge_range('A'+str(cont+1)+':C'+str(cont+1), int(row[cols[0]]), merge_center)
    worksheet.write(cont, 4, abs(row[cols[1]]), money)
    cont = cont + 1

if(positivosRecaudos.empty):
    inicial = 6
else:
    inicial = 5

cols = ingresosValidar.columns.tolist()
shapeIngresoV = ingresosValidar.shape
cont = shapePositivos[0] + shapeRecaudosV[0] + 5
for index, row in ingresosValidar.iterrows():
    worksheet.merge_range('A'+str(cont+1)+':C'+str(cont+1), int(row[cols[0]]), merge_center)
    if(row[cols[0]] == 0):
        worksheet.write(cont, 0, 'Ajustes', merge_center)
    worksheet.write(cont, 4, abs(row[cols[1]]), money)
    cont = cont + 1

worksheet.merge_range('A'+str(shapePositivos[0]+shapeRecaudosV[0]+shapeIngresoV[0]+7)+':C'+str(shapePositivos[0]+shapeRecaudosV[0]+shapeIngresoV[0]+7), 'Total', merge_bold)
worksheet.write(shapePositivos[0]+shapeRecaudosV[0]+shapeIngresoV[0]+6, 3, '=D5-SUM(D6:D'+str(shapePositivos[0]+inicial)+')', money)
worksheet.write(shapePositivos[0]+shapeRecaudosV[0]+shapeIngresoV[0]+6, 4, '=SUM(E5:E'+str(shapePositivos[0]+shapeRecaudosV[0]+5)+')-SUM(E'+str(shapePositivos[0]+shapeRecaudosV[0]+6)+':E'+str(shapePositivos[0]+shapeRecaudosV[0]+shapeIngresoV[0]+inicial)+')', money)
worksheet.merge_range('A'+str(shapePositivos[0]+shapeRecaudosV[0]+shapeIngresoV[0]+8)+':C'+str(shapePositivos[0]+shapeRecaudosV[0]+shapeIngresoV[0]+8), 'Diferencias', merge_bold)
worksheet.write(shapePositivos[0]+shapeRecaudosV[0]+shapeIngresoV[0]+7, 4, '=D'+str(shapePositivos[0]+shapeRecaudosV[0]+shapeIngresoV[0]+7)+'-E'+str(shapePositivos[0]+shapeRecaudosV[0]+shapeIngresoV[0]+7), bold_money)

cols = pagosValidar.columns.tolist()
worksheet.merge_range('A'+str(shapePositivos[0]+shapeRecaudosV[0]+shapeIngresoV[0]+10)+':C'+str(shapePositivos[0]+shapeRecaudosV[0]+shapeIngresoV[0]+10), 'Egresos', merge_bold_color)
worksheet.write(shapePositivos[0]+shapeRecaudosV[0]+shapeIngresoV[0]+9, 3, 'SAP', merge_bold_color)
worksheet.write(shapePositivos[0]+shapeRecaudosV[0]+shapeIngresoV[0]+9, 4, 'SIGEP', merge_bold_color)

cont = shapePositivos[0]+shapeRecaudosV[0]+shapeIngresoV[0]+12
shapePagosV = pagosValidar.shape
for index, row in pagosValidar.iterrows():
    worksheet.merge_range('A'+str(cont+1)+':C'+str(cont+1), int(row[cols[0]]), merge_center)
    worksheet.write(cont, 4, row[cols[1]], money)
    cont = cont + 1

if(pagosValidar.empty):
    pV = 1
else:
    pV = 0

cols = egresoValidar.columns.tolist()
shapeEgresoV = egresoValidar.shape
cont = shapePositivos[0]+shapeRecaudosV[0]+shapeIngresoV[0]+shapePagosV[0]+12
for index, row in egresoValidar.iterrows():
    worksheet.merge_range('A'+str(cont+1)+':C'+str(cont+1), int(row[cols[0]]), merge_center)
    if(row[cols[0]] == 0):
        worksheet.write(cont, 0, 'Ajustes', merge_center)
    worksheet.write(cont, 4, abs(row[cols[1]]), money)
    cont = cont + 1

worksheet.merge_range('A'+str(cont+2)+':C'+str(cont+2), 'Total', merge_bold)
worksheet.write(cont+1, 3, '=D'+str(shapePositivos[0]+shapeRecaudosV[0]+shapeIngresoV[0]+11), money)
worksheet.write(cont+1, 4, '=SUM(E'+str(shapePositivos[0]+shapeRecaudosV[0]+shapeIngresoV[0]+11)+':E'+str(shapePositivos[0]+shapeRecaudosV[0]+shapeIngresoV[0]+shapePagosV[0]+12)+')-SUM(E'+str(shapePositivos[0]+shapeRecaudosV[0]+shapeIngresoV[0]+shapePagosV[0]+13)+':E'+str(cont+pV)+')', money)
worksheet.merge_range('A'+str(cont+3)+':C'+str(cont+3), 'Diferencias', merge_bold)
worksheet.write(cont+2, 4, '=D'+str(cont+2)+'-E'+str(cont+2), bold_money)

''' HOJA DE SEGURIDAD SOCIAL SS '''
cols = seguridadSap.columns.tolist()
cols = [cols[0]] + [cols[1]] + cols[4:7] + [cols[9]] + cols[20:22]
seguridadSap = seguridadSap[cols]
shapeSAP = seguridadSap.shape
seguridadSap.to_excel(writer, sheet_name='SS', startrow=1, header=False, index=False)

if(seguridadSap.empty):
    ssSS = 1
else:
    ssSS = 2

worksheet = writer.sheets['SS']
worksheet.write(shapeSAP[0]+1, 1, '=SUM(B'+str(ssSS)+':B'+str(shapeSAP[0]+1)+')', bold_money)
worksheet.write(0, 0, 'SS SAP', bold)
worksheet.set_column('A:AB', cell_size, None)
worksheet.set_column('B:B', None, money)

contSS = 1
for index, row in seguridadSap.iterrows():
    worksheet.write(contSS, 3, datetime.strptime(row[cols[3]], '%Y-%m-%d').date(), date)
    contSS += 1 

cols = seguridadSigep.columns.tolist()
seguridadSigep = seguridadSigep[cols[0:11]]
shapeSIGEP = seguridadSigep.shape

seguridadSigep.to_excel(writer, sheet_name='SS', startrow=shapeSAP[0]+5, header=False, index=False)

contSS = contSS + 4
for index, row in seguridadSigep.iterrows():
    worksheet.write(contSS, 5, datetime.strptime(row[cols[5]], '%Y-%m-%d %H:%M:%S'), date)
    
    contSS += 1 

if(seguridadSigep.empty):
    ssSI = 5
else:
    ssSI = 6
worksheet = writer.sheets['SS']
worksheet.write(shapeSAP[0]+shapeSIGEP[0]+5, 1, '=SUM(B'+str(shapeSAP[0]+ssSI)+':B'+str(shapeSAP[0]+shapeSIGEP[0]+5)+')', bold_money)
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
        if(item == 1):
            if(enablePos == True):
                worksheet.set_column('A:'+xlsxwriter.utility.xl_col_to_name(recaudos.shape[1]-2), cell_size, None)
                worksheet.autofilter('A1:'+xlsxwriter.utility.xl_col_to_name(recaudos.shape[1]-2)+'1')
            else:
                worksheet.set_column('A:'+xlsxwriter.utility.xl_col_to_name(recaudos.shape[1]-2), cell_size, None)
                worksheet.autofilter('A1:'+xlsxwriter.utility.xl_col_to_name(recaudos.shape[1]-2)+'1')
        else:
            worksheet.set_column('A:'+xlsxwriter.utility.xl_col_to_name(pagos.shape[1]-2), cell_size, None)
            worksheet.autofilter('A1:'+xlsxwriter.utility.xl_col_to_name(pagos.shape[1]-2)+'1')
        worksheet.set_column('C:D', None, None, {'hidden': True})
        worksheet.set_column('H:L', None, None, {'hidden': True})
        worksheet.set_column('N:Q', None, None, {'hidden': True})
        worksheet.set_column('S:T', None, None, {'hidden': True})
        worksheet.set_column('U:U', None, None, {'hidden': True})
        
        #if(xlsxwriter.utility.xl_col_to_name(pagos.shape[1]-5) != 'Y'):
        #    worksheet.set_column('Y:'+xlsxwriter.utility.xl_col_to_name(pagos.shape[1]-1), None, None, {'hidden': True})
    elif(item % 2) == 0:
        worksheet = writer.sheets[sheets[item]]
        worksheet.set_column('A:N', cell_size, None)
        worksheet.autofilter('A1:N1')

correct_info = workbook.add_format({'fg_color': '#C6E0B4'})
correct_info_money = workbook.add_format({'fg_color': '#C6E0B4', 'num_format': '#,##0'})
ss_info = workbook.add_format({'fg_color': '#FFFF00'})
ss_info_money = workbook.add_format({'fg_color': '#FFFF00', 'num_format': '#,##0'})
wrong_info = workbook.add_format({'fg_color': '#F8CBAD'})
wrong_info_money = workbook.add_format({'fg_color': '#F8CBAD', 'num_format': '#,##0'})
correct_info_date = workbook.add_format({'fg_color': '#C6E0B4', 'num_format': 'mm/dd/yyyy'})
ss_info_date = workbook.add_format({'fg_color': '#FFFF00', 'num_format': 'mm/dd/yyyy'})
wrong_info_date = workbook.add_format({'fg_color': '#F8CBAD', 'num_format': 'mm/dd/yyyy'})
deducciones_color = workbook.add_format({'fg_color': '#bdd7ee', 'num_format': '#,##0'})
correct_normal_format = workbook.add_format({'fg_color': '#C6E0B4', 'num_format': '###'})
wrong_normal_format = workbook.add_format({'fg_color': '#F8CBAD', 'num_format': '###'})

#ESTILO DE RECAUDOS - INGRESOS- PAGOS - EGRESOS
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
        if (float(row['valida']) == 0):# | (row['Diferencia'] == 0):
            worksheet.set_row(cont,None, correct_info)
            style(item, row, col, worksheet, cont, correct_info_money, salarioEps, ccPosgrados, ccPosgradosPagos, enablePos, posNegRecaudos, correct_info_date, correct_normal_format)
        else:
            worksheet.set_row(cont,None, wrong_info)
            style(item, row, col, worksheet, cont, wrong_info_money, salarioEps, ccPosgrados, ccPosgradosPagos, enablePos, posNegRecaudos, wrong_info_date, wrong_normal_format)

        if (str(row[col[4]]).lower()[0:6] == 'automn') | (str(row[col[9]]).lower()[0:2] == 'ss'):
            worksheet.set_row(cont,None, ss_info)
            style(item, row, col, worksheet, cont, ss_info_money, salarioEps, ccPosgrados, ccPosgradosPagos, enablePos, posNegRecaudos, ss_info_date, None)
        cont = cont + 1
    if(dataFrames[item].empty):
        shapes = 3
    totalesSheets(worksheet, shapes-1, money, item, totaDetSap, posNegRecaudos, col, enablePos)
    worksheet.set_row(0, 30, title)

# Formato en excel para calculo de salud en pagos sap
col = dataFrames[3].columns.tolist()
worksheet = writer.sheets[sheets[3]]
salud = workbook.add_format({'num_format': '#,##0'})
cont = 1
for index, row in dataFrames[3].iterrows():
    if(str(row[col[12]]).lower() == 'salario'):
        value = salarioEps[row[col[0]]]
        if (float(row['valida']) == 0):# | (row['Diferencia'] == 0):
            worksheet.write(cont, len(col)-3, '=('+('+'.join(value))+')*'+str(porcentaje_salud*100)+'%', correct_info_money)  
        else:
            worksheet.write(cont, len(col)-3, '=('+('+'.join(value))+')*'+str(porcentaje_salud*100)+'%', wrong_info_money)  
    cont = cont + 1

# Formato en excel para calculo de porcentajes en recaudos sap
if(enablePos == True):
    col = dataFrames[1].columns.tolist()
    worksheet = writer.sheets[sheets[1]]
    formato = workbook.add_format({'num_format': '#,##0'})
    cont = 1
    rowCont = 0
    anterior = 0
    for index, row in dataFrames[1].iterrows():
        if(str(row[col[0]]).lower()[0:4] == '4200'):
            if(row[col[0]] != anterior):
                rowCont = 1
            else:
                worksheet.write(cont, len(col)-5, 0, deducciones_color)
                rowCont = 0

            if(rowCont == 1):
                valueCCP = ccPosgrados[row[col[0]]]
                if (float(row['valida']) == 0):
                    worksheet.write(cont, len(col)-8, '=abs('+('+'.join(valueCCP))+')', correct_info_money)
                    worksheet.write(cont, len(col)-7, '=('+xlsxwriter.utility.xl_col_to_name(len(col)-8)+str(cont+1)+')*'+str(porcentaje_ingresos*100)+'%', correct_info_money)   
                    worksheet.write(cont, len(col)-6, '=('+xlsxwriter.utility.xl_col_to_name(len(col)-8)+str(cont+1)+'-'+xlsxwriter.utility.xl_col_to_name(len(col)-7)+str(cont+1)+')', correct_info_money)
                else:
                    worksheet.write(cont, len(col)-8, '=abs('+('+'.join(valueCCP))+')', wrong_info_money)
                    worksheet.write(cont, len(col)-7, '=('+xlsxwriter.utility.xl_col_to_name(len(col)-8)+str(cont+1)+')*'+str(porcentaje_ingresos*100)+'%', wrong_info_money)   
                    worksheet.write(cont, len(col)-6, '=('+xlsxwriter.utility.xl_col_to_name(len(col)-8)+str(cont+1)+'-'+xlsxwriter.utility.xl_col_to_name(len(col)-7)+str(cont+1)+')', wrong_info_money)
                rowCont = 0

                valueCCPP = ('=Pagos_SAP!'+ccPosgradosPagos[row[col[0]]][0]) if(ccPosgradosPagos[row[col[0]]][:] != []) else 0
                worksheet.write(cont, len(col)-5, valueCCPP, deducciones_color)
            anterior = row[col[0]]
        cont = cont + 1
        
# TOTALES EN CONCILIACION
worksheet = writer.sheets['Conciliación']
#Ingresos
worksheet.merge_range('A5:C5', 'Notas', merge_center)
worksheet.merge_range('A'+str(shapePositivos[0]+shapeRecaudosV[0]+shapeIngresoV[0]+11)+':C'+str(shapePositivos[0]+shapeRecaudosV[0]+shapeIngresoV[0]+11), 'Notas', merge_center)
worksheet.merge_range('A'+str(shapePositivos[0]+shapeRecaudosV[0]+shapeIngresoV[0]+12)+':C'+str(shapePositivos[0]+shapeRecaudosV[0]+shapeIngresoV[0]+12), 'Más SS Social Cobrada de Mas al CC', merge_center)
verificaDataFrameVacio(worksheet, dataFrames[3], 4, 3, '=abs(Recaudos_SAP!B'+str(totales[1])+')', money)
verificaDataFrameVacio(worksheet, generalSigepItems[1], 4, 4, '=Ingresos_SIGEP!B'+str(totales[2]), money)
verificaDataFrameVacio(worksheet, dataFrames[2], shapePositivos[0]+shapeRecaudosV[0]+shapeIngresoV[0]+10, 3, '=Pagos_SAP!B'+str(totales[3]+1), money)
verificaDataFrameVacio(worksheet, generalSigepItems[2], shapePositivos[0]+shapeRecaudosV[0]+shapeIngresoV[0]+10, 4, '=Egresos_SIGEP!B'+str(totales[4]), money)
worksheet.write(shapePositivos[0]+shapeRecaudosV[0]+shapeIngresoV[0]+11, 4, '=SS!B'+str(shapeSAP[0]+shapeSIGEP[0]+10), money)

# Close the Pandas Excel writer and output the Excel file.
writer.save()
