# SSL Exporter 

Prometheus exporter for ssl certificates, written in Python.

### Installation

```bash
pip install git+https://github.com/asteny/ssl-exporter

or

Get binary from releases 
https://github.com/asteny/ssl-exporter/releases

systemd files in contrib folder

```
### Env variables
```bash
ssl-exporter --help
usage: ssl-exporter [-h] [--host-address HOST_ADDRESS] [--port PORT]
                    [--cert-paths CERT_PATHS [CERT_PATHS ...]]
                    [--log-level LOG_LEVEL] [--log-format LOG_FORMAT]

optional arguments:
  -h, --help            show this help message and exit
  --host-address HOST_ADDRESS
                        [env var: APP_HOST_ADDRESS]
  --port PORT           [env var: APP_PORT]
  --cert-paths CERT_PATHS [CERT_PATHS ...]
                        [env var: APP_CERT_PATHS]
  --log-level LOG_LEVEL
                        [env var: APP_LOG_LEVEL]
  --log-format LOG_FORMAT
                        [env var: APP_LOG_FORMAT]
```
### Example metric

```bash
ssl_valid_days{domain="*.example.ru",serial_number="cert_serial_number"} 81.0
ssl_valid_days{domain="example.ru",serial_number="cert_serial_number"} 81.0
```
