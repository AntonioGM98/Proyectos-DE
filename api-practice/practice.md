# API practice 👩🏼‍🔧 🧑🏼‍🔧

**¡Haz un _fork_ de este repositorio para hacer la práctica!**

En esta práctica vamos a aplicar los siguientes conceptos:

- Uso de principios SOLID y Arquitectura Hexagonal: aplicar esta arquitectura a la hora de diseñar la solución.
- Tests unitarios con `pytest`.
- Uso de BBDD relacionales (PostgreSQL) y no SQL (DynamoDB)
- Tests de estrés con `locust`.
- (TBD) Monitorización con Prometheus y Grafana.

## Requisitos

Hay que tener instalado lo siguiente:

- Docker y docker compose
- `pipenv`
- `aws` CLI

## Paso a paso

### PASO 0: Requisitos funcionales de la API ✈️

En esta práctica vamos a crear una API que gestione información de vuelos y pasajeros.

Un vuelo tiene la siguiente estructura:

```json
{
    "id": 24637,
    "company": "IB", # puede ser IB,I2,YW,LV
    "flight_number": 6500,
    "origin": "MAD",
    "destination": "BCN",
    "flight_date": "2023-05-01"
}
```

Y un pasajero tiene la siguiente estructura:

```json
{
    "id": 70546,
    "flight_id": 24637, # hace referencia al vuelo del pasajero
    "status": "BOARDED", # puede ser CHECKEDIN, BOARDED, CANCELLED
    "name": "Pepita",
    "surname": "Martínez",
    "class": "ECONOMY", # puede ser FIRST, BUSINESS, ECONOMY
}
```

En esta API, se tiene que poder:

- Consultar los vuelos de 1 día concreto.
- Consultar un vuelo por su id. En este caso, tiene que devolver la información del vuelo, un array con los pasajeros que estén BOARDED, y unos contadores por _class_ de pasajeros con _status_ BOARDED.
- Crear un pasajero. Hay que validar que los formatos de entrada sean correctos:
  - Que el vuelo al que hace referencia exista.
  - Que tenga todos los campos rellenos.
  - Que el _status_ y _class_ sean correctos.
- Borrar un pasajero. Hay que validar que los formatos de entrada sean correctos.

### PASO 1: Diseño API first

Vamos a seguir un enfoque [API First](https://medium.com/@emilianozublena/api-first-development-c202a61cf3b2) para el desarrollo de esta API.

Por lo tanto, haciendo uso del [Swagger Editor](https://editor.swagger.io/) hay que crear una especificación OpenAPI de la API que incluya toda la información especificada en el PASO 0. Antes de empezar a desarrollar, esta especificación ha tenido que ser entregada para su validación.

### PASO 2: v1.0.0 de la API: guardado en memoria

Hay que haber visto los siguientes cursos y leído los siguientes artículos:

- Principios SOLID y Arquitectura Hexagonal:
  - [Curso CodelyTV: Principios SOLID aplicados](https://pro.codely.com/library/principios-solid-aplicados-36875/77070/path/)
  - [Curso CodelyTV: Arquitectura Hexagonal](https://pro.codely.com/library/arquitectura-hexagonal-31201/66748/path/)
  - [Pintxo Arquitectura Hexagonal](https://drive.google.com/drive/folders/1CwgBu4vnYOpL3_7oE6r0wUtraQvuAxFP)
- Testing:
  - (Opcional) [Curso CodelyTV: Testing: Introducción y buenas prácticas](https://pro.codely.com/library/testing-introduccion-y-buenas-practicas-44653/90916/path/)
  - (Opcional) [CodelyTV: Mi primera vez haciendo tests (todo mal)](https://www.youtube.com/watch?v=VlFDlpP_cGc)
- Testing en Python con `pytest`:
  - [Getting Started With Testing in Python](https://realpython.com/python-testing/)
  - [Effective Python Testing with Pytest](https://realpython.com/pytest-python-testing/)

En una primera versión, la API usará un repositorio en memoria para guardar y consultar los datos, tanto de vuelos como pasajeros.

Como requisitos, la API tiene que cumplir:

- Los requisitos funcionales definidos en el PASO 0, incluidas las validaciones (mira en la documentación de FastAPI, hay utilidades para hacer validaciones!)
- La especificación resultante del PASO 1.
- La API tiene que tener autenticación mediante [`api key`](https://fastapi.tiangolo.com/tutorial/security/#openapi)
- Se debe intentar aplicar los principios SOLID y conceptos de arquitectura hexagonal en la medida de lo posible.

En cuanto a tests, debería incluir los siguientes:

- Como mínimo, la lógica de cálculo de contadores de pasajeros debería tener tests unitarios, usando `pytest`.
- Incluir [tests de aceptación](https://fastapi.tiangolo.com/tutorial/testing/) con las utilidades de FastAPI para validar que la especificación en OpenAPI se cumple.

### PASO 3: v2.0.0 de la API: guardado en DynamoDB

Hay que haber visto los siguientes cursos y leído los siguientes artículos:

- DynamoDB:
  - [DynamoDB cheatsheet](https://www.notion.so/DynamoDB-Cheatsheet-f5d280304f8f49b9941c394addb63c51)
  - (Opcional) [DynamoDB documentación oficial](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/GettingStartedDynamoDB.html)

En esta versión, la API usará DynamoDB como base de datos para almacenar los datos tanto de vuelos como pasajeros.

Como requisitos, la API tiene que cumplir:

- Los mismos requisitos que en el paso anterior.
- Se usará `dependency-injector` para gestionar la inyección de dependencias.

En cuanto a tests, debería incluir los siguientes:

- Los tests unitarios del paso anterior se deberían mantener.
- Los tests de aceptación usarán la librería [`moto`](https://github.com/getmoto/moto) para mockear las consultas sobre DynamoDB.

Para crear las tablas en el DynamoDB local, hay que usar el CLI de `aws` de esta forma:

```sh
# OJO! esta sentencia es de ejemplo, para el caso de la práctica le falta algo...
aws dynamodb create-table --table-name FLIGHT --attribute-definitions AttributeName=id,AttributeType=S --key-schema AttributeName=id,KeyType=HASH --billing-mode PAY_PER_REQUEST --endpoint-url http://localhost:8042 --region eu-west-1
```

Para conectar con DynamoDB, hay que usar la librería `boto3` ya instalada como dependencia del proyecto.

Deja el código resultante en una rama de git que se llame `v2.0.0`.

### PASO 4: v2.1.0 de la API: cambio de BBDD!

Ups! resulta que ya no podemos usar DynamoDB 😦, por lo que tenemos que cambiar de sistema de base de datos.

Por suerte, tenemos disponible una base de datos PostgreSQL, así que tenemos que cambiar el código para que ahora nos integremos con PostgreSQL en vez de DynamoDB. Si hemos aplicado bien los conceptos SOLID y de Arquitectura Hexagonal... ¿no debería ser tan complicado?.

Para conectarte a la base de datos desde un cliente gráfico, usa el [DBeaver](https://dbeaver.io/), y conéctate con esta conexión:

- Host: `localhost`
- Database: `operations`
- Port: 5432
- User: `operations`
- Pass: `operations`

Como requisitos, la API tiene que cumplir:

- Los mismos requisitos que en el paso anterior.

En cuanto a tests, debería incluir los siguientes:

- Los tests unitarios del paso anterior se deberían mantener.
- Los tests de aceptación usarán la librería [`testcontainers`](https://testcontainers.com/) para arrancar una base de datos PostgreSQL como parte de los tests.

Deja el código resultante en una rama de git que se llame `v2.1.0`.

### PASO 5: Tests de estrés

Nuestra API está lista, pero realmente no sabemos qué tal se va a comportar en una situación real. ¿Hasta dónde puede aguantar? ¿qué fallará primero, la API, la base de datos?.
Para esto se suelen crear test de estrés o pruebas de carga. En este paso, hay que crear tests de estrés usando [Locust](https://locust.io/) para ver qué tal se comporta nuestro servicio ante diferentes situaciones de carga.
Los tests hay que crearlos en el fichero `./app/test/stress/locustfile.py`.

Deja el código resultante en una rama de git que se llame `stress_tests`. Esta rama puede partir de cualquiera entre `v2.0.0` o `v2.1.0`.

### PASO 6: Monitorización con Prometheus y Grafana

Hay que haber visto los siguientes cursos y leído los siguientes artículos:

- Prometheus y Grafana:

  - [Curso CodelyTV: Monitoring con Prometheus](https://pro.codely.com/library/monitoring-con-prometheus-52668/115108/about/)
  - [Curso CodelyTV: Visualiza métricas de Prometheus con Grafana](https://pro.codely.com/library/visualiza-metricas-de-prometheus-con-grafana-60259/174055/path/)
  - (Opcional) [Curso CodelyTV: Grafana](https://pro.codely.com/library/grafana-203964/523387/about/)

En este paso vamos a crear un dashboard en Grafana, que lea de las métricas que expone la API para Prometheus.

- Grafana: `http://localhost:3000`
- Prometheus: `http://localhost:9090`

La API ya tiene instalada y configurada la dependencia [`starlette-exporter`](https://github.com/stephenhillier/starlette_exporter), que va a generar métricas de forma automática, que muestran qué consultas se hacen en la API, cuánto tiempo le lleva a la API resolverlas, y el código HTTP de resultado.

Si vais a la URL `http://locahost:8000/metrics` de la API, esta librería ya está dejando todas estas métricas escritas en este `/metrics`, para que Prometheus las vaya recolectando o _scrapeando_ cada 5 segundos. En concreto, las métricas que empiezan por `starlette_*` son las que genera la librería `starlette-exporter`.

Con estas métricas, desde Grafana hay que crear las siguientes gráficas:

- Una gráfica temporal que muestre qué peticiones se están realizando.
- Una gráfica que muestre el porcentaje de códigos HTTP de respuesta.
- Una gráfica temporal que muestre el tiempo que tarda cada petición.

Os aconsejamos exportar el dashboard según vayáis creando gráficas, ya que pueden perderse las gráficas al estar usando contenedores de Docker.

Además, aparte de estas métricas generadas por `starlette-exporter`, usando la librería [`prometheus-client`](https://github.com/prometheus/client_python) (ya instalada en el proyecto) se puede generar una métrica a medida de lo que necesitemos.

Usando `prometheus-client`, hay que generar:

- Una métrica que genere información de la IP con la que el cliente ha hecho la petición a la API y cuántas peticiones ha hecho cada IP.
- Un dashboard en Grafana que muestre cuántas peticiones se ha hecho con cada IP.

Como entregables de este paso, bastaría con capturas de imagen de las gráficas.
