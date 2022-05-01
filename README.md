# SEPOMEX
Prueba Back End

La elaboracion de la prueba se hizo de la siguiente manera:
1. Primero se realisó el modelo relacional de la base de datos. Para ello se hizo un análisis de la tablas arrojadas por SEPOMEX.  Esto me llevó a realizar una normalización en segunda forma lo que dio como resultado 5 tablas. 
<img src="Modelo-Relacional/Modelo Relacional.jpg" alt="Modelo relacional"/>
2. Posteriorimente se hizo la base de datos por medio de un **Seed Script** ubicado en la carpeta API. En ella también se encuntra el codigo para crear la base de datos en algún majedaro de SQL.
**Nota** Es importante mencionar que la llave primeraria de la tabla SEPOMEX es una combinación de: *estado, municipio, colonia y CP* ya que la combinación de estos números nos crea un único identificador para cada registro. También, el llenado de la base de datos es solo del 1% ya que son miles de registros, sin embargo, esto se puede modificar y poner el porcentaje que se requiera.
3. 
