# DS4 Proyecto

Para ejecutar cualquiera de los siguientes comandos, se tiene que estar en el directorio de ds4_proyecto.

## Integrantes

| Nombre                       | Num. Expediente |
| ---------------------------- | --------------- |
| Pedro Alan Escobedo Salazar  | 221218948       |
| Alex Antonio Pacheco Becerra | 223218046       |
| Alejandro Leyva Sauceda      | 223219885       |

## Declaracion sobre uso de IA

Se utilizo IA para la realizacion del proyecto.

## Ejecutar desde proyecto.py

Este archivo permite ejecutar cada programa desde la consola.

```
python proyecto.py
```

## Ejecutar desde el app.py de cada programa

### 1. Programa generador de json

```
python ./json_gen/app.py --datos_dir_path ./datos --output_filename revistas_unison.json
```

Parámetros:
* --datos_dir_path: Ruta a la carpeta datos.
* --output_filename: Nombre del archivo de salida.

### 2. Programa web scrapper

```
python ./scraper/app.py --datos_dir_path ./datos --input_filename revistas_unison.json --output_filename revistas_scimagojr.json --workers 3
```

Parámetros:
* --datos_dir_path: Ruta a la carpeta datos.
* --input_filename: Nombre del archivo de entrada.
* --output_filename: Nombre del archivo de salida.
* --workers: Número de procesos paralelos.

### 3. Programa front-end

```
python ./frontend/app.py --json_dir_path ./datos/json --unison_json_filename revistas_unison.json --scimago_json_filename revistas_scimagojr.json
```

Parámetros:
* --json_dir_path: Directorio donde están los JSONs.
* --unison_json_filename: Nombre del JSON con los datos originales de la universidad.
* --scimago_json_filename: Nombre del JSON con los datos obtenidos desde SCImago.
