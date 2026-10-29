# Entry points for humans and for Claude Code (CLAUDE.md §7).
# Every command an article quotes must be reachable from here or from scripts/.

PYTHON ?= $(shell command -v python3.12 2>/dev/null || command -v python3)
MMDC ?= mmdc
# shellcheck from the system if installed, otherwise its official image (the Codespace has Docker).
SHELLCHECK ?= $(shell command -v shellcheck 2>/dev/null || echo "docker run --rm -v $(CURDIR):/mnt:ro -w /mnt koalaman/shellcheck:v0.10.0")
# actionlint checks the workflows; sandbox.yml only runs after a merge, so its mistakes must be caught before.
ACTIONLINT ?= $(shell command -v actionlint 2>/dev/null || echo "docker run --rm -v $(CURDIR):/repo:ro -w /repo rhysd/actionlint:1.7.12")
DIAGRAM_SIZE ?= 1600
# matplotlib lives in a git-ignored .venv (scripts/post-create.sh, requirements-plots.txt).
VENV_PYTHON ?= .venv/bin/python

TEST_DIRS := $(sort $(dir $(wildcard examples/*/tests/)))
DIAGRAMS := $(patsubst %.mmd,%.png,$(wildcard articles/*/assets/*.mmd site/assets/img/*.mmd))

.PHONY: help check-env login test lint article-check diagrams site-check site-build

help: ## List targets
	@grep -E '^[a-zA-Z0-9_%-]+:.*## ' $(MAKEFILE_LIST) | awk -F':.*## ' '{ printf "  %-12s %s\n", $$1, $$2 }'

check-env: ## Read-only report: sbx, KVM, sign-in, cloud access, Python
	@scripts/check-env.sh

login: ## Sign sbx in to Docker: headless with the DOCKER_ID/DOCKER_PAT secrets, else in the browser
	@scripts/sbx-login.sh

test: ## Host-side unit tests for every example that has tests/
	@if [ -z "$(TEST_DIRS)" ]; then echo "no tests yet"; exit 0; fi; \
	status=0; \
	for d in $(TEST_DIRS); do \
		ex=$${d%tests/}; \
		echo "== $$ex"; \
		(cd $$ex && PYTHONPATH=$(CURDIR)/examples/_shared $(PYTHON) -m unittest discover -s tests -t .) || status=1; \
	done; \
	exit $$status

lint: ## shellcheck every shell script, actionlint the workflows, byte-compile the Python scripts
	@$(SHELLCHECK) scripts/*.sh examples/*/run.sh && echo "shellcheck: ok"
	@$(ACTIONLINT) && echo "actionlint: ok"
	@$(PYTHON) -m py_compile scripts/gen-header.py scripts/article-check.py scripts/plots.py && echo "py_compile: ok"

article-check: ## Articles past 'idea': Medium format, disclosure, tag links, length
	@$(PYTHON) scripts/article-check.py

compare-%: ## Run deterministic example NN on the host and in a cloud sandbox; fail unless results match
	@scripts/compare-host-cloud.sh $$(ls -d examples/$*-*/ | head -1)

run-%: ## Run example NN through scripts/sbx-run.sh (e.g. make run-01; SBX_TARGET=local)
	@script=$$(ls examples/$*-*/run.sh 2>/dev/null | head -1); \
	if [ -z "$$script" ]; then echo "error: examples/$*-*/run.sh does not exist yet" >&2; exit 1; fi; \
	$$script

plots-%: ## Draw article NN's charts from its last recorded run (make run-NN or compare-NN first)
	@$(VENV_PYTHON) scripts/plots.py $*

diagrams: $(DIAGRAMS) ## Render every Mermaid source (*.mmd) to PNG

%.png: %.mmd
	$(MMDC) --quiet -i $< -o $@ --size $(DIAGRAM_SIZE) -b white

header-%: ## Draft a header illustration via OpenRouter: make header-00 … header-06, or header-favicon
	@scripts/gen-header.py $*

site-check: ## Journal front matter, session numbering, credential scan
	@scripts/site-check.sh

site-build: ## site-check plus a full build with GitHub's Pages builder image (needs Docker)
	@SITE_BUILD=1 scripts/site-check.sh
