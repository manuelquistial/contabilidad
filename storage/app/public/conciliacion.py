#!/usr/local/bin/python
# -*- coding: utf-8 -*-
from datetime import datetime
import xlsxwriter
import pandas as pd
import numpy as np
import sys

class GeneralSigep():
    def __init__(self, sigep):
        self.sigep = sigep

    def get_general_sigep(self):
        general_sigep = self.sigep
        general_sigep_items = {1:'', 2:''}
        title_files =  {1:'Ingreso', 2:'Egreso'}
        for sigep in general_sigep_items:
            iqual_items = general_sigep['Unnamed: 2'] == title_files[sigep]
            general_sigep_items[sigep] = general_sigep[iqual_items]
            iqual_general_items = general_sigep_items[sigep]
            month_sigep = pd.DatetimeIndex(iqual_general_items['Unnamed: 3']).month
            iqual_general_items.loc[:,'Periodo'] = month_sigep
            cols = iqual_general_items.columns.tolist()
            cols = [cols[9]] + [cols[7]] + cols[0:4] + [cols[10]] + cols[4:7] + [cols[8]]
            iqual_general_items = iqual_general_items[cols]
            format_value = iqual_general_items[cols[0]].astype('int64')
            iqual_general_items.update(format_value)
            iqual_general_items.loc[:,'Formula'] = 0
            iqual_general_items.loc[:,'Diferencia'] = 0
            iqual_general_items.loc[:,'Observaciones'] = 0
            iqual_general_items.loc[:,'valida'] = 0
            general_sigep_items[sigep] = iqual_general_items
        return general_sigep_items[1], general_sigep_items[2]

class ElementosConciliacion(GeneralSigep):
    def __init__(self, files, centro_costo):
        GeneralSigep.__init__(self, files[1])
        self.pagos_sap = files[2]
        self.recaudos_sap = files[3]
        self.centro_costo = str(centro_costo)
    
    def get_col_pagos_sap(self):
        cols = self.pagos_sap.columns.tolist()
        columns_pagos_sap = [cols[7]] + [cols[5]] + cols[0:5]+ [cols[6]] + cols[8:]
        return columns_pagos_sap

    def get_col_recaudos_sap(self):
        cols = self.recaudos_sap.columns.tolist()
        columns_recaudos_sap = [cols[6]] + [cols[5]] + cols[0:5] + cols[7:]
        return columns_recaudos_sap

    def get_order_pagos_sap(self):
        cols = self.get_col_pagos_sap()
        pagos_sap = self.pagos_sap.sort_values(by=[cols[2]])
        pagos_sap = pagos_sap[cols]
        pagos_sap = pagos_sap[:-1]
        pagos_sap.loc[:,'Formula'] = 0
        pagos_sap.loc[:,'Diferencia'] = 0
        pagos_sap.loc[:,'SS'] = 0
        pagos_sap.loc[:,'Observaciones'] = 0
        pagos_sap.loc[:,'valida'] = 0
        return pagos_sap

    def get_pagos_sap(self):
        cols = self.get_col_pagos_sap()
        pagos_sap = self.get_order_pagos_sap()
        nan_values = pagos_sap.apply(lambda s: str(s[cols[0]]).lower() == 'nan', axis=1)
        nan_pagos_sap = pagos_sap[nan_values]
        for index, row in nan_pagos_sap.iterrows():
            item_doc = str(row[cols[4]])
            if(item_doc[0:2] == '81') | (item_doc[0:5] == '10000'):
                nan_pagos_sap.loc[index,cols[0]] = int(row[cols[4]])
            else:
                nan_pagos_sap.loc[index,cols[0]] = int(row[cols[2]])
        pagos_sap.update(nan_pagos_sap)
        return pagos_sap

    def get_order_recaudos_sap(self):
        cols = self.get_col_recaudos_sap()
        recaudos_sap = self.recaudos_sap.sort_values(by=[cols[2]])
        recaudos_sap = recaudos_sap[cols]
        recaudos_sap = recaudos_sap[:-1]
        return recaudos_sap
        
    def get_titles_posgrados_recaudos_sap(self):
        recaudos_sap = self.get_order_recaudos_sap()
        if(self.centro_costo == '21930003'):
            recaudos_sap.loc[:,'Total Ingresos'] = 0
            recaudos_sap.loc[:,'% Ingreso Sigep_66,667%'] = 0
            recaudos_sap.loc[:,'Pendiente registrar en proyecto ingresos_33,33%'] = 0
            recaudos_sap.loc[:,'Deducciones'] = 0
        return recaudos_sap

    def get_recaudos_sap(self):
        recaudos_sap = self.get_titles_posgrados_recaudos_sap()
        recaudos_sap.loc[:,'Formula'] = 0
        recaudos_sap.loc[:,'Diferencia'] = 0
        recaudos_sap.loc[:,'Observaciones'] = 0
        recaudos_sap.loc[:,'valida'] = 0
        return recaudos_sap

    def get_total_default_sap(self, cols, file_sap):
        total_default = file_sap.loc[file_sap.shape[0]-1,cols[1]]
        return total_default

class AlgoritmoDiferenciaColumnas():
    def __init__(self, file_one, col_file_one, file_two, col_file_two):
        self.col_file_one = col_file_one
        self.col_file_two = col_file_two
        self.file_one = file_one
        self.file_two = file_two
    
    def calculo_diferencias(self):
        file_one = self.file_one
        file_two = self.file_two
        for index, row in file_one.iterrows():
            item_doc = (file_two[self.col_file_two[0]] == row[self.col_file_one[0]]) & (file_two[self.col_file_two[6]] == row[self.col_file_one[6]])
            item_doc = file_two[item_doc]
            suma = abs(item_doc[self.col_file_two[1]]).sum()
            file_one.loc[index,'Formula'] = suma
            dif = abs(row[self.col_file_one[1]]) - suma
            file_one.loc[index,'Diferencia'] = dif
            #Suma iguales valores del archivo base
            item_doc = (file_one[self.col_file_one[0]] == row[self.col_file_one[0]]) & (file_one[self.col_file_one[6]] == row[self.col_file_one[6]])
            item_doc = file_one[item_doc]
            item_doc = abs(item_doc[self.col_file_one[1]]).sum()
            file_one.loc[index,'valida'] = suma - item_doc
        return file_one

class AlgoritmoDiferenciaSeguridadSocial():
    def __init__(self, col_pagos_sap, col_egresos_sigep):
        self.col_pagos_sap = col_pagos_sap        
        self.col_egresos_sigep = col_egresos_sigep

    def get_calculo_diferencia_seguridad_social(self, pagos_sap, salario):
        calculo_pagos_sap = pagos_sap
        calculo_salario = salario
        for index0, row0 in salario.iterrows():
            suma_salario = 0
            seguridad_social = 0
            item_pagos = pagos_sap[self.col_pagos_sap[0]] == row0[self.col_pagos_sap[0]]
            item_pagos = pagos_sap[item_pagos]
            suma_pagos = item_pagos[self.col_pagos_sap[1]].sum()
            for index1, row1 in salario.iterrows():
                if(row0[self.col_pagos_sap[0]] == row1[self.col_pagos_sap[0]]):
                    suma_salario = suma_salario + abs(row1[self.col_pagos_sap[1]])
            seguridad_social = int(round(suma_salario * 0.24023))
            valida = abs(row0['Formula']) - (suma_pagos + seguridad_social)
            item_pagos.loc[:,'valida'] = valida
            calculo_pagos_sap.update(item_pagos)
            calculo_salario.loc[index0, 'SS'] = seguridad_social
            calculo_salario.loc[index0, 'valida'] = valida            
            calculo_pagos_sap.update(calculo_salario)
        return calculo_pagos_sap

    def get_validacion_diferencia_seguridad_social(self, salario, pagos_sap, egresos_sigep):
        validacion_egresos_sigep = egresos_sigep
        for item in salario:
            pago = pagos_sap[self.col_pagos_sap[0]] == item
            pago = pagos_sap[pago]
            egreso = validacion_egresos_sigep[self.col_egresos_sigep[0]] == item
            egreso = validacion_egresos_sigep[egreso]
            suma = abs(pago['valida']).sum()
            egreso.loc[:, 'valida'] = suma
            validacion_egresos_sigep.update(egreso)
        return validacion_egresos_sigep

class PagosEgresosEspecificaciones():
    def __init__(self, col_pagos_sap, col_egresos_sigep):
        self.col_pagos_sap = col_pagos_sap
        self.col_egresos_sigep = col_egresos_sigep

    def get_algoritmo_une_epm_bancolombia(self, pago, egreso):
        suma_pago = pago[self.col_pagos_sap[1]].sum()
        suma_egreso = egreso[self.col_egresos_sigep[1]].sum()
        if(suma_pago == suma_egreso):
            pago.loc[:,'valida'] = 0
            egreso.loc[:,'valida'] = 0
        return pago, egreso

    def get_une_epm(self, pagos_sap, egresos_sigep):
        une_epm_key_word = 'une epm telecomunicaciones'
        une_epm_pago = pagos_sap.apply(lambda s: une_epm_key_word in str(s[self.col_pagos_sap[23]]).lower(), axis=1)
        une_epm_pago = pagos_sap[une_epm_pago]
        une_epm_egreso = egresos_sigep.apply(lambda s: une_epm_key_word in str(s[self.col_egresos_sigep[8]]).lower(), axis=1)
        une_epm_egreso = egresos_sigep[une_epm_egreso]
        une_epm_pago, une_epm_egreso = self.get_algoritmo_une_epm_bancolombia(une_epm_pago, une_epm_egreso)
        pagos_sap.update(une_epm_pago) 
        egresos_sigep.update(une_epm_egreso)

    def get_bancolombia(self, pagos_sap, egresos_sigep):
        bancolombia_key_word = 'bancolombia s.a.'
        gastos_bancarios_key_word = 'gastos bancarios'
        bancolombia_pago = pagos_sap.apply(lambda s: bancolombia_key_word in str(s[self.col_pagos_sap[23]]).lower(), axis=1)
        bancolombia_pago = pagos_sap[bancolombia_pago]
        bancolombia_egreso = egresos_sigep.apply(lambda s: gastos_bancarios_key_word in str(s[self.col_egresos_sigep[9]]).lower(), axis=1)
        bancolombia_egreso = egresos_sigep[bancolombia_egreso]
        bancolombia_pago, bancolombia_egreso = self.get_algoritmo_une_epm_bancolombia(bancolombia_pago, bancolombia_egreso)
        pagos_sap.update(bancolombia_pago)
        egresos_sigep.update(bancolombia_egreso)

    def get_salario(self, pagos_sap):
        salario_key_word = 'salario'
        salario = pagos_sap.apply(lambda s: str(s[self.col_pagos_sap[20]]).lower() == salario_key_word, axis=1)
        salario = pagos_sap[salario]
        return salario

    def get_resume_salario(self, salario):
        resume_salario = salario[[self.col_pagos_sap[0]] + [self.col_pagos_sap[1]]]
        resume_salario = resume_salario.groupby([self.col_pagos_sap[0]]).sum()
        resume_salario = resume_salario.reset_index()
        resume_salario = dict.fromkeys(resume_salario[self.col_pagos_sap[0]], [])
        return resume_salario

if __name__ == "__main__":
    currentPattern = [sys.argv[2], sys.argv[3], sys.argv[4]]
    path = sys.argv[5]+"conciliacion\\"
    conciliacion_files = {1:'',2:'',3:''}
    for pattern in currentPattern:
        current_file = pattern.split('\\').pop()
        file_path = path + current_file
        if(str(current_file).lower() == 'general_sigep_'+str(sys.argv[1])+'_'+sys.argv[6]+'.xlsx'):
            conciliacion_files[1]= pd.read_excel(file_path)
        elif(str(current_file).lower() == 'pagos_sap_'+str(sys.argv[1])+'_'+sys.argv[6]+'.xlsx'):
            conciliacion_files[2]= pd.read_excel(file_path)
        elif(str(current_file).lower() == 'recaudos_sap_'+str(sys.argv[1])+'_'+sys.argv[6]+'.xlsx'):
            conciliacion_files[3]= pd.read_excel(file_path)
    
    elementos_conciliacion = ElementosConciliacion(conciliacion_files, sys.argv[1])
    pagos_sap = elementos_conciliacion.get_pagos_sap()
    recaudos_sap = elementos_conciliacion.get_recaudos_sap()
    ingresos_sigep, egresos_sigep = elementos_conciliacion.get_general_sigep()

    col_pagos_sap = pagos_sap.columns.tolist()
    col_recaudos_sap = recaudos_sap.columns.tolist()
    col_ingresos_sigep = ingresos_sigep.columns.tolist()
    col_egresos_sigep = egresos_sigep.columns.tolist()

    pagos_sap = AlgoritmoDiferenciaColumnas(pagos_sap, col_pagos_sap, egresos_sigep, col_egresos_sigep).calculo_diferencias()
    recaudos_sap = AlgoritmoDiferenciaColumnas(recaudos_sap, col_recaudos_sap, ingresos_sigep, col_ingresos_sigep).calculo_diferencias()
    ingresos_sigep = AlgoritmoDiferenciaColumnas(ingresos_sigep, col_ingresos_sigep, recaudos_sap, col_recaudos_sap).calculo_diferencias()
    egresos_sigep = AlgoritmoDiferenciaColumnas(egresos_sigep, col_egresos_sigep, pagos_sap, col_pagos_sap,).calculo_diferencias()
    
    pagos_egresos_especificaciones = PagosEgresosEspecificaciones(col_pagos_sap, col_egresos_sigep)
    pagos_egresos_especificaciones.get_une_epm(pagos_sap, egresos_sigep)
    pagos_egresos_especificaciones.get_bancolombia(pagos_sap, egresos_sigep)
    salario = pagos_egresos_especificaciones.get_salario(pagos_sap)
    resumen_salario = pagos_egresos_especificaciones.get_resume_salario(salario)
    
    algoritmo_diferencia_seguridad_social = AlgoritmoDiferenciaSeguridadSocial(col_pagos_sap, col_egresos_sigep)
    #writer = pd.ExcelWriter('test.xlsx', engine='xlsxwriter')
    #pagos_sap.to_excel(writer, index=False, sheet_name='pago1')
    pagos_sap = algoritmo_diferencia_seguridad_social.get_calculo_diferencia_seguridad_social(pagos_sap, salario)
    #pagos_sap.to_excel(writer, index=False, sheet_name='pago2')
    #writer.save()
    egresos_sigep = algoritmo_diferencia_seguridad_social.get_validacion_diferencia_seguridad_social(resumen_salario, pagos_sap, egresos_sigep)