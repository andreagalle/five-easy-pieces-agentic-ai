# Entry points for humans and for Claude Code (CLAUDE.md §7).
# Every command an article quotes must be reachable from here or from scripts/.

PYTHON ?= $(shell command -v python3.12 2>/dev/null || command -v python3)
MMDC ?= mmdc
# shellcheck from the system if installed, otherwise its official image (the Codespace has Docker).
SHELLCHECK ?= $(shell command -v shellcheck 2>/dev/null || echo "docker run --rm -v $(CURDIR):/mnt:ro -w /mnt koalaman/shellcheck:v0.10.0")
DIAGRAM_SIZE ?= 1600

TEST_DIRS := $(sort $(dir $(wildcard examples/*/tests/)))
DIAGRAMS := $(patsubst %.mmd,%.png,$(wildcard articles/*/assets/*.mmd site/assets/img/*.mmd))

.PHONY: help check-env test lint article-check diagrams site-check site-build

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

lint: ## shellcheck every shell script; byte-compile the Python scripts
	@$(SHELLCHECK) scripts/*.sh examples/*/run.sh && echo "shellcheck: ok"
	@$(PYTHON) -m py_compile scripts/gen-header.py scripts/article-check.py && echo "py_compile: ok"

article-check: ## Articles past 'idea': Medium format, disclosure, tag links, length
	@$(PYTHON) scripts/article-check.py

run-%: ## Run example NN through scripts/sbx-run.sh (e.g. make run-01; SBX_TARGET=local)
	@script=$$(ls examples/$*-*/run.sh 2>/dev/null | head -1); \
	if [ -z "$$script" ]; then echo "error: examples/$*-*/run.sh does not exist yet" >&2; exit 1; fi; \
	$$script

diagrams: $(DIAGRAMS) ## Render every Mermaid source (*.mmd) to PNG

%.png: %.mmd
	$(MMDC) --quiet -i $< -o $@ --size $(DIAGRAM_SIZE) -b white

header-%: ## Draft a header illustration via OpenRouter: make header-00 … header-06, or header-favicon
	@scripts/gen-header.py $*

site-check: ## Journal front matter, session numbering, credential scan
	@scripts/site-check.sh

site-build: ## site-check plus a full build with GitHub's Pages builder image (needs Docker)
	@SITE_BUILD=1 scripts/site-check.sh
