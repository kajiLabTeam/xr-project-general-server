FROM python:3.10

WORKDIR /spot-estimation-server

COPY ./docker/spot-estimation-server/requirements.txt /spot-estimation-server/requirements.txt

RUN pip install --upgrade pip && pip install --no-cache-dir --upgrade -r /spot-estimation-server/requirements.txt

COPY ./spot-estimation-server /spot-estimation-server
COPY /.env /spot-estimation-server/.env

CMD ["python", "src/main.py"]
