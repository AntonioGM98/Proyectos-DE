Lo primero que debemos realziar es la intalación del paquete awscli y boto3 para poder conectarnos a aws:

``` Bash
pip install awscli
pip install boto3
```

Una vez instalado, debemos crear la siguiente ruta dentro de nuestro ordenador si no se ha creado directamente al hacer la instalación:

``` Bash
sudo mkdir ~/.aws
```

Dentro de esta ruta debemos crear los siguientes ficheros (la información concreta se os proporcionará de forma privada):

- credentials
```
[data-academy]
aws_access_key_id = <access_key>
aws_secret_access_key = <secret_key>
region = eu-west-1
```

- config
```
[profile data-academy-aip]
role_arn=<iam_role>
source_profile=data-academy
region=eu-west-1
```

Con esta configuración ya deberíamos poder acceder al s3, para ver que la configuración es correcta podemos ejecutar el siguiente comando:

``` Bash
aws s3 ls --profile data-academy-aip s3://next-data-academy/ardillas/aip/
```

Esa será la ruta del s3 con la que vamos a trabajar, dentro encontraréis una carpeta con vuestro nombre donde podréis trabajar.