---
layout: page
title: Decisions
permalink: /decisions/
---

Architecture decision records: the context, the options considered, the decision and its consequences. Every answer to an open question in the project brief becomes one.

{% assign adrs = site.pages | where_exp: "p", "p.path contains 'decisions/ADR-'" | sort: "path" -%}
{% for d in adrs -%}
- [{{ d.title }}]({{ d.url | relative_url }}) — {{ d.status }}
{% endfor %}
