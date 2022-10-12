FROM python:3.9

ADD requirements.txt /app/requirements.txt

RUN pip install -r /app/requirements.txt

ADD listsync /app/listsync/
ADD server.py /app/

WORKDIR /app

CMD [ "python3", "-u", "server.py", "--config", "config.ini", "--verbose" ]
