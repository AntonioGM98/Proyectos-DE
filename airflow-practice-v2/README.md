# Airflow Practice

## Requisitos/Setup

1. Necesitaremos tener instalado [Airflow](https://academy.astronomer.io/astronomer-certification-apache-airflow-fundamentals-preparation/728134). Si habéis seguido los vídeos del curso de Airflow Fundamentals, ya lo tenéis instalado.

2. Necesitaremos tener instalado [Docker](docs/docker.md), el cual usaremos a lo largo de la práctica.

3. Necesitamos una Database Tool, recomendamos la instalación de [DBeaver](https://dbeaver.io/)

4. Configurar AWS en nuestro equipo, podéis seguir las instrucciones de este [link](docs/aws.md)

5. Si todo ha ido bien: ¡Enhorabuena! Ya lo tienes todo listo, ahora puedes continuar con la práctica :)

## Iniciar Airflow

Para iniciar Airflow tenemos que llevar a cabo los siguientes pasos:

1. Creamos un usuario para acceder:
``` Bash
airflow users create
```

2. Iniciamos el webserver para poder acceder a la interfaz de Airflow:
``` Bash
airflow webserver
```

3. Lanzamos el scheduler:
``` Bash
airflow scheduler
```

4. Para conocer la ruta donde tienes que crear los dags, puedes ejecutar el siguiente comando:
``` Bash
airflow config list | grep dags_folder
```

5. Para poder usar los operadores de SFTP, hay que ejecutar el siguiente comando:
``` Bash
pip install apache-airflow-providers-sftp
```

## Enunciado

El objetivo de esta práctica es crear un DAG en Airflow en el que hagamos un flujo completo de tratamiento de datos, poniendo un caso teórico simplificado.

Para ello, en el directorio [data](data) nos encontraremos con una serie de ficheros con datos de ejemplo con los que trabajar.

La primera parte de la práctica consistirá en crear un script `.sql` donde se detalle la creación de las tablas en PostgreSQL.
Para ello, el contenedor de [docker](docs/postgres.md) tiene que estar levantado. 
La ingesta de información tendrá que hacerse de manera manual (clicando en DBeaver con el botón derecho en cada una de las tablas y eligiendo la opción `Import Data`) puesto que al estar usando la distribución de server, no se puede utilizar el comando `COPY` de forma local.

Además, se tendrá que crear una tabla final que contenga la siguiente información:

- Nombre del cliente
- Apellido del cliente
- Email del cliente
- Marketing Permission del cliente (si está de acuerdo en recibir comunicaciones comerciales) con valor `booleano`
- Carrier code del vuelo
- Código de operador del vuelo. Tiene que ser de cuatro letras (ejemplo: `0000`)
- Código de registro del vuelo (matrícula)
- Origen del vuelo
- Código de ciudad del origen del vuelo
- Código de país del origen del vuelo
- Destino del vuelo
- Código de ciudad del destino del vuelo
- Código de país del destino del vuelo
- Estado del vuelo, en formato de dos letra (`CL` para los cancelados, `OS` para los que están en schedule)
- Capacidad del vuelo
- Fecha de salida del vuelo (formato timestamp)
- Fecha de llegada del vuelo (formato timestamp)
- Si el vuelo ha sido retrasado o no
- Ticket
- PNR
- Asiento

De forma adicional, se puede empezar a investigar en las tablas, os indicamos a continuación una serie de consultas a realizar:

- Calcular el porcentaje de ocupación de los vuelos con destino IBZ.
- Calcular el porcentaje de ocupación de los vuelos no cancelados con origen Londres (LON) o París (PAR).
- Obtener la información de los vuelos no cancelados que estén en los 3 días con más afluencia de vuelos para el carrier I2 (Iberia Express).
- Obtener la información de clientes con mkt permission que tengan el vuelo cancelado cuyo asiento esté en la parte delantera del avión (primeras 15 filas de asientos).

La segunda parte de la práctica consiste en realizar el flujo completo utilizando Airflow, para automatizar el proceso.

No se comentan explícitamente los operadores que hay que utilizar (hay ocasiones en las que puede que haya más de una opción posible), pero con una pequeña investigación (buscando en google, vaya) se pueden deducir algunas de las opciones.

1. Crear el SFTP. Para ello, únicamente hay que seguir este [link](docs/sftp.md).

2. Crear un DAG en Airflow que se ejecute cada hora y que lea del SFTP los datos iniciales, guarde una copia de seguridad en s3 y los cargue en las tablas para, posteriormente, hacer una consulta (la última de los ejemplos previos, relacionada con el mkt permission).
Una vez realziada la consulta, se guardarán los datos en S3 y tendrán que subirse a un segundo SFTP.

3. Bonus track
    * En caso de terminar el DAG, se pueden implementar nuevos casos de uso, como por ejemplo, añadir tareas que manden un correo electrónico si el DAG termina correctamente o tiene algún fallo, etc.

En caso de no poder acceder a S3, una solución al problema sería utilizar Python junto a `pysocpg2` para realizar tanto la ingesta como la extracción a vuestro directorio local.
