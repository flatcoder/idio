FROM python:3.7
ENV PYTHONUNBUFFERED 1
ENV FLASK_ENV production
RUN mkdir /code
WORKDIR /code
COPY . /code/
RUN pip install -r requirements.txt
