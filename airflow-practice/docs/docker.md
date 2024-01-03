Para poder simular un SFTP en local, vamos a utilizar Docker.

Para los que no lo conozcáis, Docker es una plataforma de código abierto que permite a los desarrolladores crear, implementar, ejecutar, actualizar y administrar contenedores: componentes ejecutables estandarizados que combinan el código fuente de la aplicación con las bibliotecas del sistema operativo (SO) y las dependencias necesarias para ejecutar ese código en cualquier entorno.

Básicamente es una máquina aislada donde instalar las dependencias necesarias para un proyecto y ejecutar el mismo. 
De esta manera, tenemos un componente totalmente aislado, y el cual podemos gestionar de forma más avanzada con Kubernetes, por ejemplo (un orquestador).

Para simular un SFTP en local no necesitaremos llegar a tanto, puesto que los únicos requisitos que tendremos son:

1. Instalar Docker
2. Descargar la imagen adjunta en esta página.
3. Uso de comandos simples para levantar esta imagen, ver las imágenes actuales y su estado, pararlas, etc.

## 1. Instalar Docker

Para quienes no tengáis instalado Docker, la forma más sencilla es la que se describe en la [web oficial](https://docs.docker.com/engine/install/ubuntu/#prerequisites), y vamos a usar de referencia Ubuntu como distribución. En el caso de que tengáis una distribución distinta o un SO distinto, buscad en la documentación la guía de instalación correspondiente.

### Configuración inicial

1. Actualizar apt e instalar los paquetes correspondientes para permitir a apt usar un repositorio via HTTPS. 

```bash
sudo apt-get update
sudo apt-get install ca-certificates curl gnupg
```

1. Añadir la clave GPG oficial de Docker.

```bash
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg
```

1. Usar el siguiente comando para configurar el repositorio.

```bash
echo \
  "deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

### Instalar Docker Engine

1. Actualizar apt

```bash
sudo apt-get update
```

1. Instalar Docker Engine, containerd y Docker Compose

```bash
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

1. Podéis verificar que la instalación ha ido bien lanzando la imagen ***hello-world.***

```bash
sudo docker run hello-world
```
