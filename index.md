---
layout: home
image: images/main_banner1.jpg
---

{% assign about_page = site.pages | where: "permalink", "/about/" | first %}

{{ about_page.content | split:"<!--more-->" | first | markdownify }}

[Read More →]({{ site.baseurl }}{{ about_page.url }})
