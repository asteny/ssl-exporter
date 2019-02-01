FROM python:3.6-jessie

COPY requirements.txt /tmp/

RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY ssl-exporter.py /ssl-exporter.py

CMD ["python", "/ssl-exporter.py"]
