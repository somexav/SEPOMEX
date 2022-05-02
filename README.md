# SEPOMEX
>Prueba Backend por Javier Martinez

La elaboración de la prueba se hizo de la siguiente manera:
1. Primero se realizó el modelo relacional de la base de datos. Para ello se hizo un análisis de las tablas arrojadas por SEPOMEX.  Esto me llevó a realizar una normalización en segunda forma lo que dio como resultado 5 tablas. 

<img src="Modelo-Relacional/Modelo Relacional.jpg" alt="Modelo relacional"/>

2. La creación de la base se puede hacer desde el script _create base.py_
3. Posteriormente se hizo la base de datos por medio de un **Seed Script** ubicado en la carpeta API. En ella también se encuentra el código para crear la base de datos en algún manejador de SQL.


**Nota** Es importante mencionar que la llave primaria de la tabla SEPOMEX es una combinación de: *estado, municipio, colonia y CP* ya que la combinación de estos números nos crea un único identificador para cada registro. También, el llenado de la base de datos es solo del 1% ya que son miles de registros, sin embargo, esto se puede modificar y poner el porcentaje que se requiera.


4. La API se hizo para los siguientes casos (es la carpeta src). 

-Error404

-BUSQUEDA DE COLONIAS POR CP

-BUSQUEDA de MUNICIPIOS por ESTADO

-BUSQUEDA de COLONIAS por MUNICIPIO

-Despliegue de ESTADOS

-BUSQUEDA de estado por código

-Agregar nuevos registros (está el código base, pero tengo un error)
 
Todo fue realizado mediantes **FLASK** y ***PYTHON3**

5. El website fue realizado mediante Bootstrap, en este momento (6:56 PM) no lo he terminado, espero terminarlo en unas horas.
Este Se encuentra en src/templates

UPDATE:

## ESCRITORIO:

images_reedme/1.PNG
<img src="images_reedme/1.PNG" alt="Website_1/">
<img src="images_reedme/2.PNG" alt="Website_2/">

## MOBILE:

images_reedme/1.PNG
<img src="images_reedme/3.PNG" alt="Website_3/">
<img src="images_reedme/4.PNG" alt="Website_4/">


