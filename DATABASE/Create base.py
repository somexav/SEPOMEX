# -*- coding: utf-8 -*-
"""
Created on Sat Apr 30 20:51:25 2022

@author: Javier Martinez 
"""

'''Creacion  de la base de datos'''

import mysql.connector
from mysql.connector import errorcode


#********************CONENECT*******************

try:
  mysql_connect = mysql.connector.connect(user='root',
                                          password = '12345')
  print("Bienvenido!")
except mysql.connector.Error as err:
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    print("Algo esta mal con tu usser o pass")
  else:
    print(err)

  

    
#*****************TABLES*********************
#Nombre de las base
DB_NAME = 'sepomex_v1'
#Diccionionario de las tablas
TABLES = {} 
#Definicion de las tablas
TABLES['asentamiento'] = (
    '''CREATE TABLE asentamiento(
    C_TIPO_ASENTAMIENTO    DECIMAL(2, 0)    NOT NULL,
    D_TIPO_ASENTAMIENTO    VARCHAR(20)      NOT NULL,
    PRIMARY KEY (C_TIPO_ASENTAMIENTO)
    )ENGINE=MYISAM
    ;'''
    )
    
TABLES['ciudad'] = (
    '''CREATE TABLE ciudad(
    C_CVE_CIUDAD    DECIMAL(3, 0)    NOT NULL,
    D_CIUDAD        VARCHAR(40)      NOT NULL,
    PRIMARY KEY (C_CVE_CIUDAD)
    )ENGINE=MYISAM
    ;'''
    )

TABLES['estado'] = (
    '''CREATE TABLE estado(
    C_ESATDO    DECIMAL(2, 0)    NOT NULL,
    D_ESTADO    VARCHAR(40)      NOT NULL,
    PRIMARY KEY (C_ESATDO)
    )ENGINE=MYISAM
    ;'''
    )
    
TABLES['municipio'] = (
    '''CREATE TABLE municipio(
    C_MUNICIPIO    DECIMAL(3, 0)    NOT NULL,
    D_MUNICIPIO    VARCHAR(40)      NOT NULL,
    PRIMARY KEY (C_MUNICIPIO)
    )ENGINE=MYISAM
    ;'''
    )
    
TABLES['sepomex'] = (
    '''
    CREATE TABLE sepomex(
    SEPOMEX_ID             DECIMAL(10, 0)    NOT NULL,
    D_CODIGO               DECIMAL(7, 0)     NOT NULL,
    D_ASENTA               VARCHAR(20)       NOT NULL,
    D_CP                   DECIMAL(5, 0)     NOT NULL,
    ID_ASENTA_CPCONS       DECIMAL(5, 0)     NOT NULL,
    D_ZONA                 BIT(1)            NOT NULL,
    C_ESATDO               DECIMAL(2, 0)     NOT NULL,
    C_MUNICIPIO            DECIMAL(3, 0)     NOT NULL,
    C_CVE_CIUDAD           DECIMAL(3, 0),
    C_TIPO_ASENTAMIENTO    DECIMAL(2, 0)     NOT NULL,
    PRIMARY KEY (SEPOMEX_ID), 
    CONSTRAINT RefESTADO51 FOREIGN KEY (C_ESATDO)
    REFERENCES ESTADO(C_ESATDO),
    CONSTRAINT RefMUNICIPIO61 FOREIGN KEY (C_MUNICIPIO)
    REFERENCES MUNICIPIO(C_MUNICIPIO),
    CONSTRAINT RefCIUDAD71 FOREIGN KEY (C_CVE_CIUDAD)
    REFERENCES CIUDAD(C_CVE_CIUDAD),
    CONSTRAINT RefASENTAMIENTO81 FOREIGN KEY (C_TIPO_ASENTAMIENTO)
    REFERENCES ASENTAMIENTO(C_TIPO_ASENTAMIENTO)
    )ENGINE=MYISAM
    ;'''
    )
    
#*****************CREATE DATABASE*********************   
cursor = mysql_connect.cursor()

def create_database(cursor):
    try:
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
    except mysql.connector.Error as err:
        print("FALLO LA CREACION DE LA BASE: {}".format(err))
        exit(1)

try:
    cursor.execute("USE {}".format(DB_NAME))
    print("Se ha entrado a la base >>{}<<".format(DB_NAME))
except mysql.connector.Error as err:
    print("La base {} no existe...".format(DB_NAME))
    if err.errno == errorcode.ER_BAD_DB_ERROR:
        create_database(cursor)
        print('***********************')
        print("LA BASE {} FUE CREADA!".format(DB_NAME))
        print('***********************')
        mysql_connect.database = DB_NAME
    else:
        print(err)
        exit(1)
#*****************CREATE TABLES*********************    
      
for table_name in TABLES:
    table_description = TABLES[table_name]
    try:
        print("Creando tabla {}...".format(table_name), end='')
        cursor.execute(table_description)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("la tabla {} ya existe.".format(table_name))
        else:
            print(err.msg)
    else:
        print("LISTO!!")
        print('***********************')

mysql_connect.commit()
cursor.close()
mysql_connect.close()
