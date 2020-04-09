# SSL Exporter 

Prometheus exporter for ssl certificates, written in Python.

### Installation

#### pip

```bash
pip install git+https://github.com/asteny/ssl-exporter
```
#### Deb package for Ubuntu (16.04 - 18.04)

```bash
apt-get update
apt-get install gnupg2 apt-transport-https ca-certificates -y
apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 379CE192D401AB61
echo "deb https://dl.bintray.com/asten/ssl-exporter xenial main" | tee -a /etc/apt/sources.list.d/ssl-exporter.list
apt-get update
# For xenial
apt-get install ssl-exporter-xenial -y
# For bionic
apt-get install ssl-exporter-bionic -y```

#### Docker

```bash
docker pull asteny/ssl-exporter:v.0.4
docker run --rm -p 9001:9001 -e "APP_CERT_PATHS=/cert1.pem,/cert2.pem" -v "$(pwd)/cert1.pem:/cert1.pem" -v "$(pwd)/cert2.pem:/cert2.pem" asteny/ssl-exporter:v.0.4
```

Example `docker-compose.yml`:

```yaml
version: '2'
services:
  ssl-exporter:
    image: asteny/ssl-exporter:v.0.4
    hostname: ssl-exporter
    restart: always
    environment:
      APP_CERT_PATHS: /cert1.pem,/cert2.pem,/cert3.pem
      APP_LOG_LEVEL: DEBUG
      APP_LOG_FORMAT: json
      APP_SENTRY_DSN: "YOU DSN"
    ports:
      - "0.0.0.0:9001:9001"
    volumes:
      - "/etc/ssl/cert1.pem:/cert1.pem"
      - "/etc/ssl/cert2.pem:/cert2.pem"
      - "/etc/ssl/cert3.pem:/cert3.pem"
```

### Example metric

```bash
ssl_valid_days{domain="*.example.ru",serial_number="cert_serial_number"} 81.0
ssl_valid_days{domain="example.ru",serial_number="cert_serial_number"} 81.0
```
