# -*- coding: utf-8 -*-
"""
Created on Sat Apr 30 19:08:33 2022

@author: Javier Martinez (Somexav)
"""
#---------------------------------------------------------------------
'''

pip install pymysql

'''

import pandas as pd
import openpyxl
import mysql.connector
from mysql.connector import errorcode
#---------------------------------------------------------------------
''''
Conexion a MySQL, considerando que la base de datos ya existe

'''


db = 'sepomex_v1'
try:
  mysql_connect = mysql.connector.connect(user='root',
                                          password = '12345',
                                          database = db)
  print("Se conectado a la base de datos {}".format(db))
except mysql.connector.Error as err:
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    print("Algo esta mal con tu usser o pass")
  elif err.errno == errorcode.ER_BAD_DB_ERROR:
    print("La Base de datos NO existe")
  else:
    print(err)
#else:
# mysql_connect.close()
  


#---------------------------------------------------------------------
#Lectura de los datos como los arroja SEPOMEX

#excel_document = openpyxl.load_workbook('CPdescarga.xlsx')

#Tabla de estados
#edos = excel_document.get_sheet_names()

#df = pd.read_excel('CPdescarga.xlsx', sheet_name = 'Tlaxcala')



# df_edos = pd.DataFrame(
#     {"estado":[i for i in edos[1:]],
#      }
#     )
    
'''
1.Tamaño de la hoja
2.Seleccionar un 1%
3.Agregar a las tablas sql
    3.1 Ver si el codigo (edo + mujnicipio + ciudad + asentamiento)
    no esta en uso
    3.2 Agregar a la tabla
        3.2.1 Agregar el estado
        3.2.2 Agregar el municipo
'''

#******************************************************************************
##### 1. Tamaño de la hoja

df = pd.read_excel('CPdescarga.xlsx', sheet_name = 'Tlaxcala')

### 2. Seleccion dle 1% de los datos

df_len = len(df) #Tamano de del df
   
df_sample = df.sample(n=round(df_len*0.01)) #Solo toma el 1% del total de los datos

### 3. Agregar a las tablas a MySQL

#-------ASENTAMIENTO-----------
asentamiento = {}
asentamiento = df_sample[['c_tipo_asenta','d_tipo_asenta']]
#-------CIUDAD-----------
ciudad = {}
ciudad = df_sample[['c_cve_ciudad','d_ciudad']]
#-------ESTADO-----------
estado = {}
estado = df_sample[['c_estado','d_estado']]
#-------Municipio-----------
municipio = {}
municipio = df_sample[['c_mnpio','D_mnpio']]
#-------SEPOMEX-----------
# sepomex = {}
# sepomex = df_sample[['c_tipo_asenta','d_tipo_asenta']]

#*******************************LLENADO***********************************
#ASENTAMIENTO

def Populate_w2(df_2_columns,table,key,info):
    
    df = df_2_columns.drop_duplicates()
    
    clave = list(df.iloc[:, 0])
    name = list(df.iloc[:, 1])
    cursor = mysql_connect.cursor()
    for i in range (len(clave)):
        try:
        
            query = ("INSERT INTO {} ({},{}) VALUES (%s, %s)".format(table,key,info))
            #print(query)
            entrada = [int(clave[i]),name[i]]
            
            cursor.execute(query,entrada)
            print ('Registro agregado en {}'.format(table))
            mysql_connect.cursor.close()
        except:
            mysql_connect.rollback()
            
    mysql_connect.commit()
    #mysql_connect.close()
    
Populate_w2(asentamiento,'asentamiento',
            'C_TIPO_ASENTAMIENTO',
            'D_TIPO_ASENTAMIENTO')


Populate_w2(ciudad,'ciudad',
            'C_CVE_CIUDAD',
            'D_CIUDAD')

Populate_w2(estado,'estado',
            'C_ESTADO',
            'D_ESTADO')

Populate_w2(municipio,'municipio',
            'C_MUNICIPIO',
            'D_MUNICIPIO')

mysql_connect.close()





