FROM python:3.6

WORKDIR /code/

RUN pip install nltk
RUN python -m nltk.downloader all

ADD requirements.txt .

RUN pip install -r requirements.txt

ADD server server

CMD gunicorn -w 4 -b 0.0.0.0:8000 server:application
