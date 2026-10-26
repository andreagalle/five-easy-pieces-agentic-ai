---
layout: page
title: Prompts
permalink: /prompts/
---

Only the prompts that changed the direction of the work, rendered in English, each with one line of context and a link to the journal entry it belongs to. No secrets, no personal data.

{% assign prompts = site.pages | where_exp: "p", "p.path contains 'prompts/2'" | sort: "path" -%}
{% for p in prompts -%}
- [{{ p.title }}]({{ p.url | relative_url }})
{% endfor %}
