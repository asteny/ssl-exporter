FROM python:3.6-jessie

COPY requirements.txt /tmp/

RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY ssl_exporter/ssl_exporter.py /ssl_exporter.py

CMD ["python", "/ssl_exporter.py"]
