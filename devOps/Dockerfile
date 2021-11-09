FROM python:3.8
WORKDIR /app
COPY ./requirements.txt .
RUN apt update \
&& apt install -y git \
&& apt install -y docker \
&& apt install -y docker-compose 
RUN pip install -r requirements.txt
WORKDIR ./devOps
ENTRYPOINT [ "python3" ]
CMD ["application.py"] 