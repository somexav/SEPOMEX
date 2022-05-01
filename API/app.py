

from flask import Flask, jsonify, request
from config import config
from flask_mysqldb import MySQL


app = Flask(__name__)

#*********************CONNECT TO DB**************************
'''def ObtenerConexion():
    print('Conectado!')
    return MySQL(app)'''
mysql = MySQL(app)

#*********************ERROR 404******************************
def Error404(error):
    return "<h1>La pagina no existe</h1>",404

'''//////////////////////RUTAS/////////////////////////'''


@app.route('/')
def index():

    return "<h1> HELLO </h1>"

#######-----------BUSQUEDA DE  COLONIAS POR CP
@app.route('/busqueda/colonias/CP:<CP>', methods = ['GET'])
def colonias_seacrh(CP):
    try:
        cur = mysql.connection.cursor()
        query = "SELECT D_ASENTA FROM sepomex WHERE D_CODIGO ='{}'".format(CP)
        cur.execute(query)
        results =  cur.fetchall()
        lista  = []
        i = 0
        for fila in results:
            i = i + 1
            row = {'No: {}'.format(i):fila[0]}
            
            lista.append(row)
        return jsonify({'Colonias por CP':lista})
    except Exception as exp:
        return jsonify('Mensaje', 'ERROR, no hay colonias en ese CP')


#######-----------Despliegue de MUNICIPIOS por ESTADO

@app.route('/busqueda/municipios/<name>', methods = ['GET'])
def Municipios_Estado(name):
    try:
        cur = mysql.connection.cursor()
        query = "SELECT C_ESTADO FROM estado WHERE D_ESTADO ='{}'".format(name)
        cur.execute(query)
        result =  cur.fetchone() #En estado se espera resultado unico
        if result != None: 
            codigo = result[0]
            #row = {'ID':result[0]}
            #return jsonify({'Estado':result, 'Mensaje':'Estado encontrado'})
            subquery = "SELECT D_ASENTA FROM sepomex WHERE C_ESTADO ='{}'".format(codigo)
            cur.execute(subquery)
            results =  cur.fetchall()
            lista  = []
            i=0
            for fila in results:
                i = i + 1
                row = {'No: {}'.format(i):fila[0]}
                lista.append(row)
            return jsonify({'Municipios encontrados en {}'.format(name):lista})
        else: 
            return jsonify({'Mensaje':'Estado {} encontrado '.format(name)})
    except Exception as exp:
        return jsonify('Mensaje', 'ERROR DESCONOCIDO')

#######-----------Despliegue de COLONIAS por MUNICIPIO

@app.route('/busqueda/colonias/<name>', methods = ['GET'])
def Colonias_Municipio(name):
    try:
        cur = mysql.connection.cursor()
        query = "SELECT C_MUNICIPIO FROM municipio WHERE D_MUNICIPIO ='{}'".format(name)
        cur.execute(query)
        result =  cur.fetchone() #En estado se espera resultado unico
        if result != None: 
            codigo = result[0]
            #row = {'ID':result[0]}
            #return jsonify({'Municipio':result, 'Mensaje':'Municipio encontrado'})
            subquery = "SELECT SEPOMEX_ID,D_ASENTA,C_ESTADO FROM sepomex WHERE C_MUNICIPIO ='{}'".format(codigo)
            
            cur.execute(subquery)
            results =  cur.fetchall()
            lista  = []
            i = 0
            for fila in results:
                i = i+1
                edos_query = "SELECT D_ESTADO FROM estado WHERE C_ESTADO ={}".format(fila[2])
                cur.execute(edos_query)
                edo = cur.fetchone()
                row = {'ID':fila[0],'Edo:':edo[0],'Colonia {}'.format(i):fila[1]}
                lista.append(row)
            return jsonify({'Colonias encontrados en el Municipio {}'.format(name):lista})
        else: 
            return jsonify({'Mensaje':'Municipio NO encontrado '})
    except Exception as exp:
        return jsonify('Mensaje', 'ERROR DESCONOCIDO')


#------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------
#######-----------Despliegue de ESTADOS

@app.route('/estados', methods = ['GET'])
def listar_estados():
    try:
        cur = mysql.connection.cursor()
        query = 'SELECT C_ESTADO, D_ESTADO FROM estado'
        cur.execute(query)
        results =  cur.fetchall()
        lista  = []
        for fila in results:
            row = {'ID':fila[0],'Estado':fila[1]}
            lista.append(row)
        return jsonify({'Estados Listados':lista})
    except Exception as exp:
        return jsonify('Mensaje', 'ERROR')

#######-----------Despliegue de por codigo

@app.route('/estados/<codigo>', methods = ['GET'])
def buscar_estado(codigo):
    try:
        cur = mysql.connection.cursor()
        query = "SELECT C_ESTADO,D_ESTADO FROM estado WHERE C_ESTADO='{}'".format(codigo)
        cur.execute(query)
        result =  cur.fetchone()
        
        if result != None:
            row = {'ID':result[0],'Estado':result[1]}
            return jsonify({'Estado Encontrado':row})
        else: 
            return jsonify({'Mensaje':'Estado NO encontrado '})
    except Exception as exp:
        return jsonify('Mensaje', 'ERROR')

#---------------NO SE QUE PASA CON POST :( -------------------------------

@app.route('/estados', methods = ['POST'])
def registrar_estado():
    try:
        #print(request.json)
        cur = mysql.connection.cursor()
        query = """INSERT INTO estado (C_ESTADO, D_ESTADO) 
                    VALUES ({0},{1})""".format(request.json['C_ESTADO'],
                                                request.json['D_ESTADO'])
        cur.execute(query)
        mysql.connection.commit()
        return jsonify({'Mensaje':'Estado Agregado '})
    except Exception as exp:
        return jsonify('Mensaje', 'ERROR')        



#***********************************************************
if __name__ == '__main__':
    #Se lee la configuracion importada
    app.config.from_object(config['development'])
    app.register_error_handler(404,Error404)
    app.run()