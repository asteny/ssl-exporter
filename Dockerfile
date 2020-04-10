FROM ubuntu:xenial

RUN apt-get update && \
    apt-get install gnupg2 apt-transport-https ca-certificates -y && \
    apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 379CE192D401AB61 && \
    apt-get purge -y gnupg2 && \
    apt-get autoremove -y && \
    echo "deb https://dl.bintray.com/asten/ssl-exporter xenial main" | tee -a /etc/apt/sources.list.d/ssl-exporter.list && \
    apt-get update && \
    apt-get install ssl-exporter-xenial -y && \
    rm -rf /var/lib/apt/lists/*

CMD ["/usr/bin/ssl-exporter"]
