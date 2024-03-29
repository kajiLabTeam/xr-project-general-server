FROM python:3.10

WORKDIR /area-estimation-server

COPY ./docker/area-estimation-server/requirements.txt /area-estimation-server/requirements.txt

RUN pip install --upgrade pip && pip install --no-cache-dir --upgrade -r  /area-estimation-server/requirements.txt

COPY /server/area-estimation-server /area-estimation-server
COPY /.env /area-estimation-server/.env

CMD ["python", "src/main.py"]
