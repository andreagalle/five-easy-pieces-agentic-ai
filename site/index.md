---
layout: page
title: Home
permalink: /
---

This site is the public record of how *Five Easy Pieces on Agentic AI w/ Docker Sandboxes* is made: a seven-part Medium series that reads Chapter 2 of Russell & Norvig's *Artificial Intelligence: A Modern Approach* (4th ed.) as the vocabulary for today's agentic AI, and runs each of the five agent types in Docker Sandboxes. Every program in the series runs in disposable sandboxes, locally or in the cloud, with the same commands.

The work happens in a GitHub Codespace with Claude Code. Claude writes most of the raw material on this site as the work happens: [journal]({{ "/journal/" | relative_url }}) entries, [decisions]({{ "/decisions/" | relative_url }}), the [workflow]({{ "/workflow/" | relative_url }}). The author edits and decides.

The plan in one page: [the five pieces]({{ "/pieces/" | relative_url }}). It covers what each agent does, where an LLM comes in and why, and whether the sandbox is actually needed.

The illustrations, including the site icon, are AI-generated with Google's Nano Banana 2 via OpenRouter, from prompts kept in the repository's `illustrations/` folder.

## Series status

| ID | Article | Status | Code |
|----|---------|--------|------|
{% for a in site.data.series.articles -%}
| {{ a.id }} | {% if a.medium_url != "" %}[{{ a.title }}]({{ a.medium_url }}){% else %}{{ a.title }}{% endif %} | {{ a.status }} | {% if a.code_tag != "" %}`{{ a.code_tag }}`{% else %}—{% endif %} |
{% endfor %}

## Latest journal entries

{% assign entries = site.pages | where_exp: "p", "p.path contains 'journal/2'" | sort: "path" | reverse -%}
{% for e in entries limit: 5 -%}
- [{{ e.title }}]({{ e.url | relative_url }}) — {{ e.date | date: "%Y-%m-%d" }}
{% endfor %}
