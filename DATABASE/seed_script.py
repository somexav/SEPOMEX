# -*- coding: utf-8 -*-
"""
Created on Sat Apr 30 19:08:33 2022

@author: Javier Martinez (Somexav)
"""
#---------------------------------------------------------------------

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

  


#---------------------------------------------------------------------

    
'''
        METODOLOGIA DEL LLENADO DE LA BASE DE DATOS
        
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

'''AQUI SE ENCUNTRAN LOS ESTADOS'''

#----Lectura de los datos como los arroja SEPOMEX

#excel_document = openpyxl.load_workbook('CPdescarga.xlsx')

#---Tabla de estados

#edos = excel_document.get_sheet_names()
#edos = edos[1:]

'''NOTA: Esta carga quita mucho tiempo, por lo que se hizo un array 
         con el nombre de los estados y asi no cargar todos los datos, sin embargo, 
         se puede hacer de ambas formas
         '''
edos = ['Aguascalientes', 'Baja_California', 'Baja_California_Sur', 'Campeche', 'Coahuila_de_Zaragoza', 'Colima', 'Chiapas', 'Chihuahua', 'Distrito_Federal', 'Durango', 'Guanajuato', 'Guerrero', 'Hidalgo', 'Jalisco', 'México', 'Michoacán_de_Ocampo', 'Morelos', 'Nayarit', 'Nuevo_León', 'Oaxaca', 'Puebla', 'Querétaro', 'Quintana_Roo', 'San_Luis_Potosí', 'Sinaloa', 'Sonora', 'Tabasco', 'Tamaulipas', 'Tlaxcala', 'Veracruz_de_Ignacio_de_la_Llave', 'Yucatán', 'Zacatecas']

#clave_municipio = [int(str() + str())]
#**************************FUNCION DE LLENADO**********************************
#**************************PARA LAS RELACIONES PARCIALES **********************


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
#********************************LLENADO TOTAL POR ESTADO***********************

##### 1. Tamaño de la hoja

def POPULATE_DATADABE(edos):
    for edo in edos:
        df = pd.read_excel('CPdescarga.xlsx', sheet_name = edo)
        
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
        
        
        
        #**************************LLENADO DE SEPOMEX***********************************
        ''' SEPOMEX_ID             DECIMAL(10, 0)    NOT NULL,
            D_CODIGO               DECIMAL(7, 0)     NOT NULL,
            D_ASENTA               VARCHAR(20)       NOT NULL,
            D_OFICINA              DECIMAL(5, 0)     NOT NULL,
            ID_ASENTA_CPCONS       DECIMAL(5, 0)     NOT NULL,
            D_ZONA                 BIT(1)            NOT NULL,
            C_ESTADO               DECIMAL(2, 0)     NOT NULL,
            C_MUNICIPIO            DECIMAL(3, 0)     NOT NULL,
            C_CVE_CIUDAD           DECIMAL(3, 0),
            C_TIPO_ASENTAMIENTO    DECIMAL(2, 0)     NOT NULL,'''
            
        sepomex = {}
        sepomex = df_sample[['d_codigo',
                             'd_asenta',
                             'c_oficina',
                             'id_asenta_cpcons',
                             'd_zona']]
        
        codigo = list(sepomex.iloc[:,0])
        colonia = list(sepomex.iloc[:,1])
        oficina = list(sepomex.iloc[:,2])
        id_asent = list(sepomex.iloc[:,3])
        zona = list(sepomex.iloc[:,4].replace({'Rural': 0, 'Urbano': 1})) #transformar a bit
        
        ##--------------LLENADO SEOMEX-----------------------
        
        #Se asume que no puede haber registros duplicados
        
        
        estado = list(estado.iloc[:,0])
        municipio = list(municipio.iloc[:,0])
        ciudad = list(ciudad.iloc[:,0].fillna(0))
        asentamiento = list(asentamiento.iloc[:,0])
        
        cursor = mysql_connect.cursor()
        
        for i in range (len(sepomex)):
            ID = int(str(estado[i]) + str(municipio[i])+ str(id_asent[i]))
            print(ID) #SE crea un unico identificador compuesto de :
                 #Estado, Municiipio y el numero del asentamiento.
            try:
            
                query = ("INSERT INTO sepomex" 
                         "(SEPOMEX_ID, D_CODIGO, D_ASENTA,C_OFICINA,ID_ASENTA_CPCONS,D_ZONA,"
                          "C_ESTADO,C_MUNICIPIO,C_CVE_CIUDAD,C_TIPO_ASENTAMIENTO) "
                         "VALUES (%s, %s,%s, %s,%s, %s,%s, %s,%s, %s)")
                          
                #print(query)
                entrada = (ID, 
                           codigo[i], 
                           colonia[i], 
                           oficina[i], 
                           id_asent[i], 
                           zona[i],
                           #Coidgos
                           estado[i],
                           municipio[i],
                           (ciudad[i]),
                           asentamiento[i])
                #print(entrada)
                cursor.execute(query,entrada)
                print ('Registro agregado en sepomex')
                mysql_connect.cursor.close()
            except:
                mysql_connect.rollback()
                
                
        mysql_connect.commit()
        
        
    
#------------------------------------INSTANCIA DE LA DB-------------------------
POPULATE_DATADABE(edos)
mysql_connect.close()