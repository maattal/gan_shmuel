FROM python:3.9-alpine AS build-stage

WORKDIR /app

COPY requirements.txt ./
COPY ./one-db.sql ../docker-entrypoint-initdb.d/one-db.sql
RUN pip install --target=/app -r requirements.txt
COPY . ./

FROM python:3.9-alpine
COPY --from=build-stage /app .
ENTRYPOINT [ "python3" ]
CMD [ "app.py" ]