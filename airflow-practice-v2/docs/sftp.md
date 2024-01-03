Para simular un SFTP en local los únicos requisitos que tendremos son:

1. Descargar la imagen adjunta en esta página.
2. Uso de comandos simples para levantar esta imagen, ver las imágenes actuales y su estado, pararlas, etc.


## 1. Imagen

El código de la imagen está a continuación.
Podéis descargaros el archivo directamente  o copiar el código en un archivo denominado Dockerfile.

Lo único que hay que modificar es la contraseña, donde pone SFTPUSERPASSWORDHERE.

[Dockerfile](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/4f8d7940-aa53-4b95-a42f-1211f08541f7/Dockerfile.txt)

```docker
FROM ubuntu:22.10

RUN apt-get update 
RUN apt-get install -y --fix-missing openssh-server

# configure sftp user
RUN useradd -rm -d /home/sftp_user -s /bin/bash -G sudo -u 998 sftp_user 
RUN echo "sftp_user:SFTPUSERPASSWORDHERE" | chpasswd 

# necessary sshd file
#RUN mkdir /var/run/sshd

# SSH login fix (Keeping Session Alive). If not, user will be kick off after ssh
RUN sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd

ENV NOTVISIBLE "in users profile"
RUN echo "export VISIBLE=now" >> /etc/profile

EXPOSE 22
CMD ["/usr/sbin/sshd", "-D"]

#setup directory for sftp
RUN mkdir -p /var/sftp/uploads
RUN chown root:root /var/sftp
RUN chmod 755 /var/sftp
RUN chown sftp_user:sftp_user /var/sftp/uploads

# update to only allow sftp and not ssh tunneling to limit the non-necessary activity 
RUN echo '\n\
Match User sftp_user  \n\
ForceCommand internal-sftp \n\ 
PasswordAuthentication yes \n\ 
ChrootDirectory /var/sftp \n\ 
PermitTunnel no  \n\ 
AllowAgentForwarding no \n\ 
AllowTcpForwarding no \n\ 
X11Forwarding no ' >> /etc/ssh/sshd_config
```

## 2. Ejecutar la imagen

Para utilizar la imagen, lo primero que hay que utilizar es el comando build sobre el código para crearla.

```bash
docker build -t sftp-container .
```

Si finaliza sin errores, ya está la imagen disponible para ser levantada. Para ello usamos lo siguiente

```bash
docker run -d -p 2036:22 sftp-container
```

Donde estamos arrancando la imagen y vinculando el puerto 2036 de nuestra máquina (uno random libre, cualquiera libre que tengáis sirve) al puerto 22 de la imagen.

Por último podemos probar, ya sea por consola o con Filezilla que conecta correctamente.
Por consola sería algo así:

```bash
sftp -oPort=2036 sftp_user@127.0.0.1
```

Para parar de usar el contenedor, podemos usar docker stop o docker kill.

```bash
docker stop sftp-container
```