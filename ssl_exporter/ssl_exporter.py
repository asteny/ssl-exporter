import logging
import os
import time
from datetime import datetime
from pathlib import Path

from configargparse import ArgumentParser
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.x509.oid import ExtensionOID
from cryptography.x509.extensions import ExtensionNotFound
from prettylog import basic_config
from prometheus_client import start_http_server
from prometheus_client.core import GaugeMetricFamily, REGISTRY

parser = ArgumentParser(
    default_config_files=[os.path.join("/etc/ssl-exporter.conf")],
    auto_env_var_prefix="APP_",
)

parser.add_argument("--host-address", type=str, default="0.0.0.0")
parser.add_argument("--port", type=int, default="9001")
parser.add_argument("--cert-paths", required=True, type=str)
parser.add_argument("--log-level", type=str, default="INFO")
parser.add_argument("--log-format", type=str, default="color")

arguments = parser.parse_args()

log = logging.getLogger()


class SslExporter(object):
    gauges = {}

    def __init__(self, cert_paths: str):
        self.cert_paths = cert_paths

    def collect(self):

        self.gauges["ssl_valid_days"] = GaugeMetricFamily(
            "ssl_valid_days",
            "Ssl cert valid days",
            value=None,
            labels=["domain", "file_name", "serial_number"],
        )

        paths = [path.strip() for path in self.cert_paths.split(",")]
        for p in paths:
            path = Path(p)
            if not path.exists():
                log.error("File %r does not exists", path)
                exit(1)
            self.get_metrics(path)

        for name, data in self.gauges.items():
            yield data

    def get_metrics(self, path: Path):
        with open(path, "rb") as f:
            try:
                cert = x509.load_pem_x509_certificate(
                    f.read(), default_backend()
                )
            except ValueError:
                log.exception("Cannot read certificate - %r", path)
                return []
        file_name = path.name
        log.debug("File name of cert - %r", file_name)

        not_valid_after = cert.not_valid_after
        log.debug("Ssl not valid after date - %r", str(not_valid_after))

        left = not_valid_after - datetime.utcnow()
        log.debug("Ssl cert valid days - %r", left.days)

        log.debug("Ssl cert serial number - %r", cert.serial_number)

        try:
            ext = cert.extensions.get_extension_for_oid(
                ExtensionOID.SUBJECT_ALTERNATIVE_NAME
            )
            dns_names_list = ext.value.get_values_for_type(x509.DNSName)
        except ExtensionNotFound:
            dns_names_list = ["noname"]

        log.debug("DNS names of cert - %r", dns_names_list)

        for domain in dns_names_list:
            self.gauges["ssl_valid_days"].add_metric(
                [domain, file_name, str(cert.serial_number)], int(left.days)
            )


def main():
    basic_config(
        level=arguments.log_level.upper(),
        buffered=False,
        log_format=arguments.log_format,
    )

    start_http_server(addr=arguments.host_address, port=arguments.port)
    collector = SslExporter(arguments.cert_paths)
    REGISTRY.register(collector)
    while True:
        time.sleep(1)


if __name__ == "__main__":
    main()
