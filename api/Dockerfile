FROM python:3.6

WORKDIR /code/

RUN pip install nltk
RUN python -m nltk.downloader twitter_samples

ADD requirements.txt .

RUN pip install -r requirements.txt

ADD server server
