#!/usr/bin/env bash
# Checks for the making-of record (CLAUDE.md §9, §11 "Site"):
#   1. every journal entry has the §9.1 front matter and sections;
#   2. session numbers run 01..N with no gaps;
#   3. no credential-shaped strings anywhere in the working tree;
#   4. with SITE_BUILD=1 and Docker available, build site/ with the same
#      image GitHub's jekyll-build-pages action uses.
set -uo pipefail

root="$(cd "$(dirname "$0")/.." && pwd)"
cd "$root" || exit 1
failures=0
fail() { echo "FAIL: $*"; failures=$((failures + 1)); }

# 1. Journal entries
keys=(layout title date session pieces sbx_version model sandbox_runs)
sections=("Goal" "What we did" "Commands that mattered" "Decisions" "Dead ends and surprises" "Who did what" "Next")
entries=(site/journal/[0-9][0-9][0-9][0-9]-*.md)
if [ ! -e "${entries[0]}" ]; then
  fail "no journal entries in site/journal/"
  entries=()
fi
for f in "${entries[@]}"; do
  front="$(awk 'NR == 1 && /^---$/ { on = 1; next } on && /^---$/ { exit } on' "$f")"
  for k in "${keys[@]}"; do
    grep -q "^$k:" <<<"$front" || fail "$f: missing front matter key '$k'"
  done
  for s in "${sections[@]}"; do
    grep -qx "## $s" "$f" || fail "$f: missing section '## $s'"
  done
done

# 2. Session numbering
expected=1
for n in $(grep -h '^session:' "${entries[@]}" /dev/null | tr -dc '0-9\n' | sort -n); do
  [ "$((10#$n))" -eq "$expected" ] || fail "journal sessions: expected $(printf '%02d' $expected), found $n"
  expected=$((10#$n + 1))
done

# 3. Credential-shaped strings (tracked and untracked, ignored files excluded)
pattern='dckr_pat_[A-Za-z0-9_-]{8,}|sk-ant-[A-Za-z0-9_-]{8,}|ghp_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|-----BEGIN [A-Z ]*PRIVATE KEY-----'
if hits="$(git grep -nIE --untracked "$pattern" -- . ':!scripts/site-check.sh')"; then
  fail "credential-shaped strings found:"
  echo "$hits" | cut -c1-120
fi

# 4. Optional build with the GitHub Pages builder image
if [ "${SITE_BUILD:-0}" = 1 ]; then
  image="ghcr.io/actions/jekyll-build-pages:v1.0.13"
  if command -v docker >/dev/null; then
    out="$(mktemp -d)"
    # Same `github-pages build` the action's entrypoint runs, minus the entrypoint itself:
    # it always exports JEKYLL_GITHUB_TOKEN, and an empty token fails GitHub API auth.
    # Without a token, jekyll-github-metadata falls back to unauthenticated API calls.
    if docker run --rm --user "$(id -u):$(id -g)" -v "$root:/src:ro" -v "$out:/out" \
        -e JEKYLL_ENV=production -e PAGES_REPO_NWO="${GITHUB_REPOSITORY:-}" \
        --entrypoint /usr/local/bundle/bin/github-pages "$image" \
        build --source /src/site --destination /out/_site >"$out/build.log" 2>&1; then
      echo "site build: ok ($(find "$out/_site" -name '*.html' | wc -l) HTML files)"
    else
      fail "site build failed; last lines of the log:"
      tail -20 "$out/build.log"
    fi
    rm -rf "$out"
  else
    echo "site build: skipped (docker not available)"
  fi
fi

if [ "$failures" -eq 0 ]; then
  echo "site-check: ok"
else
  echo "site-check: $failures problem(s)"
  exit 1
fi
