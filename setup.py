# encoding: utf-8
from __future__ import absolute_import, print_function
from setuptools import setup, find_packages


__version__ = '0.4'
__author__ = 'Pavel Sofrony <pavel@sofrony.ru>'


setup(
    name='ssl-exporter',
    version=__version__,
    author=__author__,
    author_email='pavel@sofrony.ru',
    license="MIT",
    description="Prometheus exporter for ssl certs",
    platforms="all",
    packages=find_packages(),
    install_requires=(
        'asn1crypto==0.24.0',
        'cffi==1.11.5',
        'colorlog==4.0.2',
        'ConfigArgParse==0.14.0',
        'cryptography==2.5',
        'fast-json==0.3.2',
        'JSON-log-formatter==0.2.0',
        'prettylog==0.2.0',
        'prometheus-client==0.5.0',
        'pycparser==2.19',
        'raven==6.10.0',
        'six==1.12.0',
        'ujson==1.35',
    ),
    entry_points={
        'console_scripts': [
            'ssl_exporter = ssl_exporter.ssl_exporter:main',
        ],
    },
    extras_require={
        ':python_version < "3.7"': 'typing >= 3.6.5',
    },
)
