import logging
import time
from datetime import datetime
from os.path import exists

import json_log_formatter
from configargparse import ArgumentParser
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.x509.oid import ExtensionOID
from prometheus_client import start_http_server
from prometheus_client.core import GaugeMetricFamily, REGISTRY

parser = ArgumentParser(auto_env_var_prefix='APP_')
parser.add_argument('--cert-paths', required=True, type=str)
parser.add_argument('--debug',
                    default="",
                    type=str,
                    help='Debug level logging'
                    )

arguments = parser.parse_args()

log = logging.getLogger()


class SslExporter(object):
    gauges = {}

    def __init__(self, paths):
        self.paths = paths

    def collect(self):

        self.gauges['ssl_valid_days'] = GaugeMetricFamily(
            'ssl_valid_days',
            'Ssl cert valid days',
            value=None,
            labels=['domain']
        )

        for path in self.paths:
            with open(path.strip(), 'rb') as f:
                try:
                    cert = x509.load_pem_x509_certificate(
                        f.read(), default_backend()
                    )
                except ValueError:
                    log.exception('Cannot read certificate',
                                  extra={'cert': path})
                    return []
            self.get_metrics(cert)

        for name, data in self.gauges.items():
            yield data

    def get_metrics(self, cert):

        not_valid_after = cert.not_valid_after
        log.debug(
            'Ssl not valid after date',
            extra={'not_valid_after_date': str(not_valid_after)}
        )

        left = not_valid_after - datetime.utcnow()
        log.debug(
            'Ssl cert valid days',
            extra={'valid_days': str(left.days)}
        )

        ext = cert.extensions.get_extension_for_oid(
            ExtensionOID.SUBJECT_ALTERNATIVE_NAME
        )
        dns_names_list = ext.value.get_values_for_type(x509.DNSName)
        log.debug(
            'DNS names of cert',
            extra={'dns_names': str(dns_names_list)}
        )

        for domain in dns_names_list:
            self.gauges['ssl_valid_days'].add_metric(
                [domain], int(left.days))


if __name__ == "__main__":
    if bool(arguments.debug):
        log.setLevel(logging.DEBUG)
    else:
        log.setLevel(logging.ERROR)
    handler = logging.StreamHandler()
    formatter = json_log_formatter.JSONFormatter()
    handler.setFormatter(formatter)
    log.addHandler(handler)

    paths = [
        path.strip() for path in arguments.cert_paths.split(',')
    ]
    for path in paths:
        if not exists(path):
            log.error('File %s does not exists', path)
            exit(1)

    start_http_server(8000)
    collector = SslExporter(paths)
    REGISTRY.register(collector)
    while True:
        time.sleep(1)
