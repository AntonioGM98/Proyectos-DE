Para el uso de una instancia de Postgres en local los únicos requisitos que tendremos son:

1. Descargar la imagen, como se especifica en esta página.
2. Uso de comandos simples para levantar esta imagen, ver las imágenes actuales y su estado, pararlas, etc.

Es **MUY IMPORTANTE** tener en cuenta que en caso de parar la imagen, cualquier esquema creado, tabla, inserción de datos, etc no se reflejará al levantar otra vez la imagen.
Se recomienda tener un script `.sql` en el que vayáis guardando todo el trabajo que vayáis realizando.

## 1. Imagen

El primer paso es descargar la imagen. 
Existe una imagen pública en la cual se levanta una instancia de Postgre, que es la que utilizaremos a continuación.

```bash
docker pull postgres
```

Una vez descargada la imagen el siguiente paso es levantar un contenedor con la misma. Para ello utilizaremos el comando `docker run` pero con una serie de parámetros extra.

```bash
docker run
    --name myPostgresDb
    -p 5455:5432
    -e POSTGRES_USER=postgresUser
    -e POSTGRES_PASSWORD=postgresPW
    -e POSTGRES_DB=postgresDB
    -d
    postgres
```

Todos estos parámetros extra son configurables. Vamos a detallarlos poco a poco:

- `--name myPostgresDb`: Nombre del contenedor
- `-p 5455:5432`: Mapeo de vuestro puerto 5455 al 5432 del contenedor, que es el puerto por defecto que utiliza Postgres.
- `-e POSTGRES_USER=postgresUser`: Nombre del usuario de la BBDD.
- `-e POSTGRES_PASSWORD=postgresPW`: Contraseña del usuario de la BBDD.
- `-e POSTGRES_DB=postgresDB`: Nombre de la BBDD.

Una vez ejecutado este comando, la instancia de Postgres estaría levantada y se podría conectar a la misma por consola, con DBeaver, Airflow...


## 2.Conexión desde DBeaver

Para añadir la conexión desde DBeaver, tenemos que abrir el editor y clicar en el símbolo del conector arriba a la izquierda, que tiene indicado un símbolo `+`.
Se abrirá un desplegable donde tendréis que indicar el tipo de conexión que se va a utilizar, en este caso, PostgreSQL.

Esto llevará a una nueva pestaña donde se indicará la info que hemos proporcionado en el comando que levantaba el contenedor con la imagen de Postgre.

En el caso de no recordar la info indicada, siempre podéis comprobarlo con el siguiente comando. En el caso de no tener el nombre de contenedor por defecto, utilizad `docker ps` para checkearlo.

```bash
docker exec myPostgresDb env
```

Una vez rellenada la información (recordad que el host va a ser localhost o 127.0.0.1) clicad en `Probar conexión`.
En caso de que todo esté correcto, dadle a aceptar y se añadirá la conexión al panel.

Para acceder a ella, doble clic. Una vez conectados ya podéis abrir consolas, ejecutar scripts `.sql` etc.

## 3.Problemas comunes

El problema principal que os puede surgir al usar esto viene de cuando se mata el proceso, ya sea con un `docker stop` o con un `docker kill`.
Os va a funcionar correctamente, pero para la próxima vez que levantéis la imagen, va a salir lo siguiente:

`docker: Error response from daemon: Conflict. The container name "/myPostgresDb" is already in use by container "c4e5eefdde0797807c363dce830057c6c45886806848273022598c26ab238265". You have to remove (or rename) that container to be able to reuse that name.
See 'docker run --help'.`

Para solucionar esto, reiniciamos el servicio de Docker y removemos el contenedor.

```bash
sudo systemctl restart docker.socket docker.service
docker rm -f <container id>
```