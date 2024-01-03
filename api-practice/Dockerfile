FROM python:3.8-slim

LABEL VERSION=0.1.0

# FastAPI stuff:
# https://github.com/pypa/pipenv/issues/4220
RUN pip install pipenv==2018.11.26
COPY env env
COPY app app
COPY Dockerfile Dockerfile
COPY Pipfile.lock Pipfile.lock
COPY Pipfile Pipfile
RUN pipenv install --deploy --system

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]