#!/bin/bash

alembic upgrade head

cd src

uvicorn main:app --host 0.0.0.0 --reload