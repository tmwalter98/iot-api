FROM tiangolo/uvicorn-gunicorn:python3.8

LABEL maintainer="Timothy Walter <inbox@timothywalter.tech>"

RUN pip install --no-cache-dir fastapi phue rgbxy pydantic colour

COPY ./app /app