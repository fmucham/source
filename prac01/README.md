
# Práctica 1: M2.851 - Tipología y ciclo de vida de los datos

Desarrollado por Félix Mucha y José Enriquez


## Instalación y Ejecución

El proyecto usa librerías que pueden ser instaladas ejecutando el siguiente comando:

```bash
  pip install -r requirements.txt
```
Para ejecutar el proyecto, se debe ejecutar de manera secuencial la siguiente sentencia:

```bash
scrapy crawl alquilerdpto -o alquilerdpto.json
scrapy crawl alquilerdptodet -o alquilerdptodet.csv
```


## Descripción

El proyecto desarrollado se conecta a un portal inmobiliario, que contiene características de inmuebles disponibles para alquiler. La información por recuperar contendrá, ubicación, precios y número de habitaciones como variables principales. Después de realizar el scraper del portal se almacenará en formato CSV, para que después se realice el análisis.



## Datos extraídos
Por cada inmueble se tendrá los datos siguientes:
- title: título del anunció de alquiler.
- location: dirección del inmueble.
- price: pecio de alquiler.
- bedroom: número de habitaciones.
- bathroom: número de baños.
- area: área del inmueble.
- year_contruction: año de construcción.
- maintenance: costo de mantenimiento en el edificio del inmueble.
- housing_type: tipo de inmueble.
- operation_type: tipo de operación alquiler o venta. En nuestro caso solo es alquiler.
- date_pub: fecha de publicación del anuncio.
- url: link para acceder al inmueble.


## Dataset

[La información en formato CSV se ha publicado en Zenodo para su visualización y descarga, acotando que su uso no vaya en contra de las disposiciones legales vigentes.](https://doi.org/10.5281/zenodo.7846211)

