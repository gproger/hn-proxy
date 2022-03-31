FROM python:3.10

WORKDIR /app

EXPOSE 8232

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY app app

WORKDIR /app/app

CMD [ "python3", "-m" , "app"]