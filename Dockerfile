FROM python:3.9
ADD . /home/app
WORKDIR /home/app
# Creates TZ soft link
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN pip install -r requirements.txt \
    && apt-get update \
    && apt-get install sqlite3
ENTRYPOINT ["python", "server.py"]