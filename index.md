---
layout: home
image: images/main_banner1.jpg
---

{% assign about_page = site.pages | where: "permalink", "/about/" | first %}
{{ about_page.excerpt | markdownify }}

[Read more →]({{ about_page.url }})
