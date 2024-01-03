# -*-coding:utf8-*-
from fastapi import FastAPI
from practice import routes

app = FastAPI(
    title="Data Academy REST API",
    description="Data Academy Pandas REST API endpoints",
    docs_url="/docs",
    openapi_url="/openapi.json"
)

app.include_router(routes.router)