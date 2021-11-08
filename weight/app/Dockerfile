FROM python:3.9-alpine
WORKDIR /app/
COPY requirements.txt .

RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

COPY app.py .
EXPOSE 5000

ENTRYPOINT [ "python3", "app.py" ]