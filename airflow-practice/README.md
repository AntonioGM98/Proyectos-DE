# Airflow Practice


## Requisitos/Setup

1. Necesitaremos tener instalado [Airflow](https://academy.astronomer.io/astronomer-certification-apache-airflow-fundamentals-preparation/728134). Si habéis seguido los vídeos del curso de Airflow Fundamentals, ya lo tenéis instalado.

2. Ahora debemos instalar [Docker](docs/docker.md). Usaremos docker para tener un SFTP que utilizaremos para transferir archivos.

3. Si todo ha ido bien: ¡Enhorabuena! Ya lo tienes todo listo, ahora puedes continuar con la práctica :)

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

## Practice

El objetivo de esta práctica es crear un DAG en Airflow que manipule un archivo y suba el fichero resultante a un SFTP.

No se comentan explícitamente los operadores que hay que utilizar (hay ocasiones en las que puede que haya más de una opción posible), pero con una pequeña investigación (buscando en google, vaya) se pueden deducir algunas de las opciones.

1. Crear el SFTP. Para ello, únicamente hay que seguir este [link](docs/sftp.md).

2. Crear un DAG en Airflow que se ejecute todos los días a las 12:15 y que tenga de start_date el 2023-01-01, pero que no ejecute el histórico de los Dag runs.

3. Añadir una tarea que se ejecute al principio y que no haga nada. Su task_id será *start*.

4. Añadir una tarea que se ejecute al final y que no haga nada. Su task_id será *end*.

5. Añadir una tarea que, en función del día de la semana, especifique el flujo siguiente de tareas. En caso de ser fin de semana, la tarea que se ejecutará después de esta será la tarea *end*. Su task_id será *branch_weekend*.

6. Añadir una tarea (que irá después de branch_weekend si no es fin de semana), que espere hasta que haya un archivo vacío de nombre practica1_ardillas_YYYY_MM_DD.csv (siendo YYYY_MM_DD la fecha del día anterior a la fecha en la que se ejecuta el DAG, por ejemplo 2023_07_15) en la carpeta uploads del sftp. Su task_id será *wait_for_sftp_file*.

7. Añadir una tarea (o varias, hay más de una solución posible), que:
    1. Descargue el archivo, y en él escriba:
        * La fecha en la que se ejecuta el proceso en formato DDMONYY, por ejemplo 15JUL23.
        * El nombre de los integrantes del grupo de la práctica.
        * La fecha del siguiente sábado en formato DD/MM/YYYY.
    2. Cambie el nombre del fichero a practica1_ardillas_YYYY_MM_DD_DAYOFWEEK.csv, donde DAYOFWEEK es el día de la semana en inglés.
    3. Suba el fichero modificado al SFTP

8. Crear un task group que contenga todas las tareas creadas en los puntos 6 y 7 (pueden ser 2 o más tareas las que se hayan creado en esos dos puntos).

9. Crear el flujo de tareas como se ha descrito.

10. Bonus track. Si os ha sobrado tiempo hay varias cosas que se pueden hacer:
    * Comprobad que el DAG es limpio y seguís lo que se explica en el curso (¿Usáis decoradores cuándo se puede?)
    * Haced que el DAG se ejecute 2 veces al día, una a las 12:15 y otra a las 15:15. En función de cómo hayáis planteado la solución esto puede obligaros a cambiar un poco varias tareas. Hacedlo en otro DAG aparte.
    * Haced que el DAG se ejecute a las 12:15 hora española. Hay que tener en cuenta el cambio de hora, no basta con restar 2 horas a la hora de ejecución.
