FROM python:3.8

WORKDIR /app

RUN pip install pandas
RUN pip install ncclient

COPY src/ /app

RUN pip install influxdb_client requests influxdb mdclogpy schedule

CMD ["python", "main2.py"]
