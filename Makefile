# Entry points for humans and for Claude Code (CLAUDE.md §7).
# Every command an article quotes must be reachable from here or from scripts/.

PYTHON ?= $(shell command -v python3.12 2>/dev/null || command -v python3)
MMDC ?= mmdc
DIAGRAM_SIZE ?= 1600

TEST_DIRS := $(sort $(dir $(wildcard examples/*/tests/)))
DIAGRAMS := $(patsubst %.mmd,%.png,$(wildcard articles/*/assets/*.mmd site/assets/img/*.mmd))

.PHONY: help check-env test diagrams site-check site-build

help: ## List targets
	@grep -E '^[a-zA-Z0-9_%-]+:.*## ' $(MAKEFILE_LIST) | awk -F':.*## ' '{ printf "  %-12s %s\n", $$1, $$2 }'

check-env: ## Read-only report: sbx, KVM, sign-in, cloud access, Python
	@scripts/check-env.sh

test: ## Host-side unit tests for every example that has tests/
	@if [ -z "$(TEST_DIRS)" ]; then echo "no tests yet"; exit 0; fi; \
	status=0; \
	for d in $(TEST_DIRS); do \
		ex=$${d%tests/}; \
		echo "== $$ex"; \
		(cd $$ex && PYTHONPATH=$(CURDIR)/examples/_shared $(PYTHON) -m unittest discover -s tests -t .) || status=1; \
	done; \
	exit $$status

run-%: ## Run example NN through scripts/sbx-run.sh (e.g. make run-01; SBX_TARGET=local)
	@script=$$(ls examples/$*-*/run.sh 2>/dev/null | head -1); \
	if [ -z "$$script" ]; then echo "error: examples/$*-*/run.sh does not exist yet" >&2; exit 1; fi; \
	$$script

diagrams: $(DIAGRAMS) ## Render every Mermaid source (*.mmd) to PNG

%.png: %.mmd
	$(MMDC) --quiet -i $< -o $@ --size $(DIAGRAM_SIZE) -b white

header-%: ## Draft a header illustration for article NN via OpenRouter (e.g. make header-00)
	@scripts/gen-header.py $*

site-check: ## Journal front matter, session numbering, credential scan
	@scripts/site-check.sh

site-build: ## site-check plus a full build with GitHub's Pages builder image (needs Docker)
	@SITE_BUILD=1 scripts/site-check.sh
