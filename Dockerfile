FROM python:3.10

WORKDIR /app

EXPOSE 8232

COPY requirements.txt requirements.txt
COPY proxy.py proxy.py
RUN pip3 install -r requirements.txt

COPY app app

CMD [ "python3", "proxy.py"]
