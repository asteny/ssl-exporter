NAME = ssl-exporter
VERSION = 0.5
ITERATION = 0
UID ?= 0

all: build_xenial build_bionic

build_xenial: download_xenial
	chmod -Rv 644 build/contrib/
	fpm -s dir -f -t deb \
		-n $(NAME)_xenial \
		-v $(VERSION) \
		--iteration $(ITERATION) \
		--after-install build/contrib/$(NAME).postinstall \
		--after-remove build/contrib/$(NAME)r.postrm \
		-p build/packages \
		build/contrib/$(NAME).service=/lib/systemd/system/$(NAME).service \
		build/contrib/$(NAME).defaults=/etc/default/$(NAME) \
		build/contrib/$(NAME).preset=/usr/lib/systemd/system-preset/$(NAME).preset \
		build/contrib/$(NAME).conf=/etc/$(NAME).conf \
		/tmp/$(NAME)_ubuntu-16.04=/usr/bin/$(NAME)

build_bionic: download_bionic
	chmod -Rv 644 build/contrib/
	fpm -s dir -f -t deb \
		-n $(NAME)_bionic \
		-v $(VERSION) \
		--iteration $(ITERATION) \
		--after-install build/contrib/$(NAME).postinstall \
		--after-remove build/contrib/$(NAME)r.postrm \
		-p build/packages \
		build/contrib/$(NAME).service=/lib/systemd/system/$(NAME).service \
		build/contrib/$(NAME).defaults=/etc/default/$(NAME) \
		build/contrib/$(NAME).preset=/usr/lib/systemd/system-preset/$(NAME).preset \
		build/contrib/$(NAME).conf=/etc/$(NAME).conf \
		/tmp/$(NAME)_ubuntu-18.04=/usr/bin/$(NAME)

build_xenial:
	cd /tmp && wget https://github.com/asteny/ssl-exporter/releases/download/v$(VERSION)/ssl_exporter_ubuntu-16.04

build_bionic
	cd /tmp && wget https://github.com/asteny/ssl-exporter/releases/download/v$(VERSION)/ssl_exporter_ubuntu-18.04
