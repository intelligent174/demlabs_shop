#!/bin/bash


alembic upgrade head

#gunicorn app.asgi:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000
uvicorn app.asgi:app --host=0.0.0.0 --port=8000 --reload --lifespan="on"