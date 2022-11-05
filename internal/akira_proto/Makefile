BASE_DIR := $(dir $(realpath $(lastword $(MAKEFILE_LIST))))
REPOSITORY_ROOT := $(realpath $(BASE_DIR)../../)

define BUF
	@docker run --rm --volume "$(REPOSITORY_ROOT):/workspace" -e HOME=/tmp --workdir /workspace/internal/akira_proto -u `id -u`:`id -g` bufbuild/buf $(1)
endef

.PHONY: all generate lint

all: generate

lint:
	$(call BUF,lint)

generate:
	$(call BUF,generate)

update:
	$(call BUF,mod update)
