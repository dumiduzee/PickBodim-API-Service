FROM python:3.12.2-slim

WORKDIR /app/

EXPOSE 8000


COPY  requirements.txt .

RUN pip3 install -r requirements.txt

COPY . .

WORKDIR /app/src/


CMD [ "fastapi","dev","main.py","--host","0.0.0.0" ]