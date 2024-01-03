# Data Analytics practice

## Requisitos/Setup

1. Tener instalado [pyenv](https://brain2life.hashnode.dev/how-to-install-pyenv-python-version-manager-on-ubuntu-2004#heading-installation)
2. Instala tu herramienta favorita para gestionar dependencias de python:
    - [poetry](https://python-poetry.org/docs/#installation)
    - [pipenv](https://pipenv.pypa.io/en/latest/installation/)
3. Asegurate de tener en pyenv instalado una versión de python >=3.8

    ```bash 
    pyenv install -v 3.8.10
    pyenv shell 3.8.10
    ```
4. Instala las dependencia y crea tu entorno virual con tu herramienta favorita _(poetry mas mola)_
    - Poetry:

        ```bash
            poetry install
            poetry shell
        ```
    - Pipenv:

        ```bash
            pipenv install
            pipenv shell
        ```
5. Una vez dentro de tu _fresh_ entorno virtual, ya puedes arrancar un jupyter notebook

    ```bash
        jupyter notebook notebooks/
    ```

## Practice

Se requerirá responder una serie de preguntas sobre un dataset. Pero no solo trata de dar la solución, además se tiene que:

- Aplicar las buenas prácticas que has aprendido.
- Contar tus conclusiones de la forma más clara y concisa.
- Utiliza todas las herramientas que necesites para que solución seá espectacular (matplotlib, seaborn...)