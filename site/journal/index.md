---
layout: page
title: Journal
permalink: /journal/
---

One entry per working session, written by Claude at the end of the session and edited by the author. Entries record what was done, including what didn't work.

{% assign entries = site.pages | where_exp: "p", "p.path contains 'journal/2'" | sort: "path" | reverse -%}
{% for e in entries -%}
- [{{ e.title }}]({{ e.url | relative_url }}) — {{ e.date | date: "%Y-%m-%d" }}
{% endfor %}
