SHELL := /bin/bash
CWD := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))
ME := $(shell whoami)

lint:
	./db_utils/bin-lint.sh

tests:
	./db_utils/bin-tests.sh

fix_own:
	@echo "me: $(ME)"
	sudo chown $(ME):$(ME) -R .
