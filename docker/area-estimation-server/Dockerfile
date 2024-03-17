FROM python:3.10
USER root

RUN apt-get update
RUN apt-get -y install locales && \
    localedef -f UTF-8 -i ja_JP ja_JP.UTF-8

RUN mkdir /area-estimation-server

WORKDIR /area-estimation-server

ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP:ja
ENV LC_ALL ja_JP.UTF-8
ENV TZ JST-9
ENV TERM xterm

RUN apt-get install -y vim less
RUN pip install --upgrade pip
RUN pip install --upgrade setuptools

RUN python -m pip install python-dotenv
RUN python -m pip install boto3
RUN python -m pip install fastapi
RUN python -m pip install uvicorn
RUN python -m pip install python-ulid
RUN python -m pip install psycopg2-binary


CMD ["python", "src/main.py"]