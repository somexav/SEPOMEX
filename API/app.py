

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

        return jsonify({'Estados':results, 'Mensaje':'Estados Listados'})
    except Exception as exp:
        return jsonify('Mensaje', 'ERROR')


@app.route('/estados/<codigo>', methods = ['GET'])
def buscar_estado(codigo):
    try:
        cur = mysql.connection.cursor()
        query = "SELECT C_ESTADO,D_ESTADO FROM estado WHERE C_ESTADO='{}'".format(codigo)
        cur.execute(query)
        result =  cur.fetchone()
        
        if result != None:
            row = {'ID':result[0],'Estado':result[1]}
            return jsonify({'Estado':result, 'Mensaje':'Estado encontrado'})
        else: 
            return jsonify({'Mensaje':'Estado NO encontrado '})
    except Exception as exp:
        return jsonify('Mensaje', 'ERROR')

@app.route('/estados', methods = ['POST'])
def registrar_estado():
    try:
        #print(request.json)
        cur = mysql.connection.cursor()
        query = """INSERT INTO estado (C_ESTADO, D_ESTADO) 
                    VALUES ({0},'{1}')""".format(request.json['C_ESTADO'],
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