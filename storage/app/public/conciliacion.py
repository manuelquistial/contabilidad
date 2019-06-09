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

    def get_files_general_sigep(self):
        general_sigep = self.sigep
        general_sigep_items = {1:'',2:''}
        title_files =  {1:'Ingreso',2:'Egreso'}
        for sigep in general_sigep_items:
            iqual_items = general_sigep['Unnamed: 2'] == title_files[sigep]
            general_sigep_items[sigep] = general_sigep[iqual_items]
            iqual_general_items = general_sigep_items[sigep]
            month_sigep = pd.DatetimeIndex(iqual_general_items['Unnamed: 3']).month
            iqual_general_items['Periodo'] = month_sigep
            cols = iqual_general_items.columns.tolist()
            cols = [cols[9]] + [cols[7]] + cols[0:4] + [cols[10]] + cols[4:7] + [cols[8]]
            iqual_general_items = iqual_general_items[cols]
            format_value = iqual_general_items[cols[0]].astype('int64')
            iqual_general_items.update(format_value)
            iqual_general_items['Formula'] = 0
            iqual_general_items['Diferencia'] = 0
            iqual_general_items['Observaciones'] = 0
            iqual_general_items['valida'] = 0
            general_sigep_items[sigep] = iqual_general_items
        return general_sigep_items[1], general_sigep_items[2]


class Conciliacion(GeneralSigep):
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

    def get_pagos_sap(self):
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

    def get_order_recaudos_sap(self):
        cols = self.get_col_recaudos_sap()
        recaudos_sap = self.recaudos_sap.sort_values(by=[cols[2]])
        recaudos_sap = recaudos_sap[cols]
        recaudos_sap = recaudos_sap[:-1]
        return recaudos_sap
        
    def get_titles_posgrados_recaudos_sap(self):
        recaudos_sap = self.get_order_recaudos_sap()
        if(self.centro_costo == '21930003'):
            recaudos_sap['Total Ingresos'] = 0
            recaudos_sap['% Ingreso Sigep_66,667%'] = 0
            recaudos_sap['Pendiente registrar en proyecto ingresos_33,33%'] = 0
            recaudos_sap['Deducciones'] = 0
        return recaudos_sap

    def get_recaudos_sap(self):
        recaudos_sap = self.get_titles_posgrados_recaudos_sap()
        recaudos_sap['Formula'] = 0
        recaudos_sap['Diferencia'] = 0
        recaudos_sap['Observaciones'] = 0
        recaudos_sap['valida'] = 0
        return recaudos_sap

    def get_total_default_sap(self, cols, file_sap):
        total_default = file_sap.loc[file_sap.shape[0]-1,cols[1]]
        return total_default

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
    
    Conciliacion(conciliacion_files, sys.argv[1])