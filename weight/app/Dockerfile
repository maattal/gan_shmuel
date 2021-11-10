FROM python:3.9-alpine
WORKDIR /app/

RUN python -m pip install --upgrade pip
RUN pip install flask flask-restful mysql-connector-python

COPY . /app/
EXPOSE 5000

ENTRYPOINT [ "python3", "app.py" ]