# TVTime
Esta aplicación te muestra cuanto tiempo te ha llevado ver una serie o todas tus series favoritas

## Requisitos

* [Python3](https://www.python.org/downloads/).

* Librerias : ```python -m pip install -r requirements.txt``` (En el directorio del codigo)
  
* API IMDB: puedes obtenerla mediante: https://rapidapi.com/apidojo/api/imdb8 , te registras y te suscribes a la api, luego copias la ```x-rapidapi-key``` en la sección ```__headers``` al comienzo del código.


## Configuración 🔧

Se requiere un archivo ```series.txt``` en el directorio raiz de la aplicación con la lista de series a procesar.
Estas volcarán los resultados en un archivo xlsx, ademas los errores de incompatibilidad a la hora de buscar la serie se volcarán en el archivo ```errores.txt```.

#Diseño

* Se utilizo *Pandas* para la exportación del dataframe con los datos.

* *Requests* para las peticiones.

* *openpyxl* para la entrada/salida de archivos xlsx.


## Ejecución

 * Puede usar el comando y `` `py -u" Ruta del archivo py "` ``, Es necesario tener la ruta de Python definida en las variables de entorno del sistema.

* Si está utilizando un IDE o un editor de código configurado, simplemente compile y ejecute el código.

##Vistas a futuro

* Utilizar otra API que permita más peticiones para asi poder procesar una cantidad superior de series, sin agotar peticiones.

* No depender de una API y utilizar *Selenium* con *BeautifulSoap*


## Autor ✒️

* **Jorge Manuel Lozano Gómez**
