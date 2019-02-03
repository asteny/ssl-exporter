import logging
import time
from datetime import datetime
from os.path import exists

from configargparse import ArgumentParser
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.x509.oid import ExtensionOID
from prettylog import basic_config
from prometheus_client import start_http_server
from prometheus_client.core import GaugeMetricFamily, REGISTRY

parser = ArgumentParser(auto_env_var_prefix='APP_')
parser.add_argument('--host-address', type=str, default='0.0.0.0')
parser.add_argument('--port', type=int, default='9001')
parser.add_argument('--cert-paths', required=True, type=str)
parser.add_argument('--debug',
                    default="",
                    type=str,
                    help='Debug level logging'
                    )
parser.add_argument('--log-level', type=str, default="INFO")
parser.add_argument('--log-format', type=str, default="color")

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
            labels=['domain', 'serial_number']
        )

        for path in self.paths:
            with open(path.strip(), 'rb') as f:
                try:
                    cert = x509.load_pem_x509_certificate(
                        f.read(), default_backend()
                    )
                except ValueError:
                    log.exception('Cannot read certificate - %r', path)
                    return []
            self.get_metrics(cert)

        for name, data in self.gauges.items():
            yield data

    def get_metrics(self, cert):

        not_valid_after = cert.not_valid_after
        log.debug(
            'Ssl not valid after date - %r',
            str(not_valid_after)
        )

        left = not_valid_after - datetime.utcnow()
        log.debug(
            'Ssl cert valid days - %r',
            left.days
        )

        ext = cert.extensions.get_extension_for_oid(
            ExtensionOID.SUBJECT_ALTERNATIVE_NAME
        )
        dns_names_list = ext.value.get_values_for_type(x509.DNSName)
        log.debug(
            'DNS names of cert - %r',
            dns_names_list
        )

        log.debug(
            'Ssl cert serial number - %r',
            cert.serial_number
        )

        for domain in dns_names_list:
            self.gauges['ssl_valid_days'].add_metric(
                [domain, str(cert.serial_number)], int(left.days))


if __name__ == "__main__":

    basic_config(level=arguments.log_level.upper(),
                 buffered=False,
                 log_format=arguments.log_format
                 )

    paths = [
        path.strip() for path in arguments.cert_paths.split(',')
    ]
    for path in paths:
        if not exists(path):
            log.error('File %r does not exists', path)
            exit(1)

    start_http_server(addr=arguments.host_address, port=arguments.port)
    collector = SslExporter(paths)
    REGISTRY.register(collector)
    while True:
        time.sleep(1)
