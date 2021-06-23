FROM python:3
ENV PYTHONBUFFERED 1

RUN mkdir /app
WORKDIR /app
COPY requirements.txt /app/
COPY . /app/
EXPOSE 8000
RUN pip install -r requirements.txt
