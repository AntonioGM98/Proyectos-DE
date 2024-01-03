# api-practice

API practice.

Follow practice on [`practice.md`](./practice.md).

You can execute `make help` to see all available commands on this repository.

## Requisites

- [pipenv](https://pypi.org/project/pipenv/)
- If you are using Visual Studio Code, you need to install [Python extension](https://marketplace.visualstudio.com/items?itemName=ms-python.python)

## Start

```bash
make start
```

- To run needed local infrastructure on Docker:

```bash
# Start local infra
make start-infra
# Stop local infra
make stop-infra
```

## Install dependencies

```bash
make install-deps
```

## Add/remove dependency

```bash
# Install dependency
make install dep=<dependency> ver=<dependency_version> # Example: make install dep=requests ver=2.26.0
make install-dev dep=<dependency> ver=<dependency_version> # Example: make install-dev dep=requests ver=2.26.0

# Uninstall dependency
make uninstall dep=<dependency> # Example: make uninstall dep=requests
```

## Run

```bash
make run
```

## Run tests

```bash
make run-tests
```

## Format code

```bash
make format
```
