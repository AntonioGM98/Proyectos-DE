
# Data Analytics practice

## Requisitos/Setup
1. Tener instalado [pyenv](https://brain2life.hashnode.dev/how-to-install-pyenv-python-version-manager-on-ubuntu-2004#heading-installation)
2. Tener instalado poetry ([poetry](https://python-poetry.org/docs/#installation))
3. Asegurate de tener en pyenv instalado una versión de python >=3.8
    ```bash
    pyenv install -v 3.8.10
    pyenv shell 3.8.10
    ```
4. Instala las dependencias y crea tu entorno virtual del proyecto:
    ```bash
        poetry install
        poetry shell
    ```
5. Para trabajar con `pyspark`, además de los paquetes de python que has instalado en el paso anterior, necesitarás tener `java` instalado en tu sistema:
   1. Instala sdkman para manejar diferentes versiones de java en tu sistema. Su función es similar a `pyenv`, que ya conoces, pero para java. ([sdkman](https://sdkman.io/install))
   2. Instala una versión de java compatible con spark. El siguiente comando instalará la versión `17.0.6-tem`, especificada en el fichero de configuración `.sdkmanrc` de este repo: `sdk env install`.
6. Ya puedes comprobar si todos los pasos anteriores han ido bien, por ejemplo lanzando una sesión interactiva de pyspark en tu terminal (`pyspark`).

## Enunciado
El objetivo será convertir los datos en formato json correspondientes a las respuestas de una API a formato tabular, para prepararlos para introducirlos en nuestra base de datos. Esto permitirá más adelante analizar y cruzar esta información usando nuestro lenguaje preferido para este tipo de tareas: SQL.

Los datos de esta práctica son los de una API que devuelve información sobre la cantidad de asientos que quedan pendientes por vender para cada clase tarifaria. Se ha dejado una muestra de los datos en el directorio `data/` del repositorio. El resultado del ejercicio deberá crear una tabla a partir de los json de este directorio con las siguientes columnas:
- La fecha y hora de la *request*.
- Los campos que identifican qué información se ha enviado en la *request* a la API.
- Los campos de la *response* desgranados hasta el nivel de `response.Journeys.Portions.Flights.Avalability`. Necesitamos que la tabla final contenta los siguientes campos de cada vuelo, el resto se pueden ignorar:
  - `DepartureAirport`
  - `ArrivalAirport`
  - `DepartureTime`
  - `Availability.Cabin`, `Availability.RBD` (que es el nombre de la clase tarifaria) y `Availability.State` en formato numérico (integer).

Además de obtener la solución, es importante que:
- Los nombres elegidos para cada campo sean intuitivos y nos permitan analizar la información de manera intuitiva. Por ejemplo, el nombre nos debe permitir ver inmediatamente si un campo pertenece a la *request* o a la *response*.
- La jerarquía que muestra el json se plasme de forma clara en la tabla de la solución.
- Dar cariño a la mantenibilidad, legibilidad, expresividad del código.
