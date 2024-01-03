# Data Servicing practice

## Requisitos/Setup

1. Tener instalado [pipenv](https://pypi.org/project/pipenv/) + [docs](https://pipenv-fork.readthedocs.io/en/latest/basics.html)
2. Os daremos un entorno virtual (pipfile) con todos los paquetes necesarios. Sólo debereis instalarlo con `pipenv` y acceder al mismo:
    ```bash
    pipenv install
    pipenv shell
    ```
3. Para levantar la API en local, ejecutar el archivo `run-local.sh`:
    ```bash
    ./run-local.sh
    ```
4. Una vez levantada la API, acceder al swagger de FastAPI en el localhost: `http://127.0.0.1:8000/docs`
## Practice

### **Introducción**

El objetivo va a ser el desarrollo de un pequeño microservicio que levantaremos en local y consumiremos desde el swagger de FastAPI, framework con el que lo desarrollaremos. Para ello, vamos a implementar diferentes endpoints, de menos a más dificultad para que os vayais familiarizando con los microservicios. 

Los endpoints a desarrollar son los siguientes:

Nota: Todos los endpoints deberán estar definidos en la carpeta *routes.py*

1. endpoint "health". El enpoint Health se escribe en la ruta raiz "/" y devuelve un {OK} si la api está levantada. Para familiarizarse con el framework.

2. endpoint que reciba un string en el header URL de los siguientes 3 posibles:

    ```text
    ES - IT - FR
    ```
    - A continuación, se le hace match con el diccionario a importar en Python desde el path de `sources/markets.json` y devolver en la response la lista que haga match. Este endpoint deberá estar protegido con una API-KEY

    - Implementar control de errores. Para en el caso de introducir un market distinto a los establecidos devolver un código de error controlado con un mensaje que explique por qúe ha fallado.

3. Endpoint que recibe el json de `examples/request.json` en el body y lo parsea con un modelo de pydantic:
    - Definir modelo correctamente con los tipos de datos.

    - Devolver un código 204 si todo va OK.

### **Bundling Service**

### Contexto

Se va a implementar el microservicio **"BUNDLING"**. Un Blundle es un pack de varios ancillaries que se ofrecerán juntos al cliente con un descuento mayor que si lo compra por separado (por ejemplo si compras en pack un asiento y una maleta facturada). 
Ofreceremos los productos **"PRIORITY"** Y **"FLEXIBILITY ON DEMAND"**.

Un bundle se define a nivel de slice (origen-destino sin contar escala), que podreis encontrar en el campo **"slices"** de la request, dentro del campo "context" junto a los segmentos (escalas) del mismo.

Tras esto, hay que crear los siguientes endpoints:

4. Endpoint que recibe el json de `examples/request.json` y tras parsearlo con el modelo de Pydantic se deben de desarrollar los siguientes puntos:

    - En el ejercicio anterior, probamos a cargarnos un json en local para hacer las consultas. Para este ejercicio, vamos a cargar también en diccionarios en local los jsons de `sources/airports.json` y `sources/bundels.json`. 

    Una vez los tengais, debeis usarlos para sacar la siguiente información:

    - Sacar solo los Bundles cuyo origen sea el aeropuerto de `Madrid` y devolverlos en la response.

    - Sacar solo los Bundles cuyo destino sea `Bilbao` y devolverlos en la response

    Debeis devolver un json con con los bundles de origen `Madrid` y los bundles de destino `Bilbao` en dos keys separadas.

5. Hay que crear un Endpoint que recibe el json de ejemplo y tras parsearlo con el modelo de Pydantic, se deben de desarrollar los puntos anteriores(podeis reutilizar las funciones que ya teneis implementadas):
   
    - Obtener todos bundles disponibles en `sources/bundels.json` con el origen-destino indicado en el segmento correspondiente al slice.
    - Comprobar cuales de esos bundles aplican a nuestra request:
        - Para **Priority** tenemos que comprobar que aplica para todos los pasajeros de todos los segmentos del slice. Es decir, que todos los pasajeros (context.passengers) están contenidos en todos los segmentos del slice.
        - Para **Flexibility**, comprobar que todos los pasajeros están incluidos en la lista de flexibility y que a ambos se les ofrecen los mismos subtipos de flexibilidad.
    - Una vez comprobados que bundles aplican, debemos devolver ÚNICAMENTE los que contienen los subtipos que hemos marcado como válidos en el paso anterior. (En el caso de PRIORITY no hay subtipos)

6. Estas consultas que estamos haciendo contra los jsons en local, deben de hacerse normalmente contra una base de datos en realtime. En la mayoría de APIs que desarrollamos en Iberia solemos usar DynamoDB.

   Para simular este comportamiento, vamos a mockear una tabla de dynamo en local mediante la librería *moto* y trabajar desde ahí (sustituyendo a la carga de datos en local). Para ello tendréis que cargar en tablas los archivos `sources/airports.json` y `sources/bundels.json` completando el script de mock_dynamodb.py llamando a las tablas: `AIRPORT_CITY_CODES` y `ANCILLARIES_BUNDLES` (Puede que tengais que usar un [conversor](https://dynobase.dev/dynamodb-json-converter-tool/) de json a dynamo format)

    - Coger los valores de las ciudades de las request y obtener sus aeropuertos correspondientes de la tabla de DynamoDB: `AIRPORT_CITY_CODES`

    - Teniendo el valor de los aeropuertos de origen y destino del vuelo, consultar la tabla de DynamoDB: `ANCILLARIES_BUNDLES` para obtener los bundles.

    Podeis usar la documentación de boto3 para ver que métodos se pueden usar para extraer datos de tablas de DynamoDB.

Además de obtener la solución, es importante que:
- Los nombres elegidos para cada campo y endpoints sean claros y nos permitan analizar la información de manera intuitiva. Por ejemplo, el nombre nos debe permitir ver inmediatamente si un campo pertenece a la *request* o a la *response*.
- Dar cariño a la mantenibilidad, legibilidad, expresividad del código.
- Implementar status codes para control de errores, por ejemplo:
    - Un 500 es un internal server error (cuando falla algo que no tenemos controlado)
    - Un 412 es un precondition failed (si no se cumple una condición específica para continuar la ejecución del servicio)
