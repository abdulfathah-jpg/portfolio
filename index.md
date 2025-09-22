---
layout: home
image: images/main_banner1.jpg
---

{% assign about_page = site.pages | where: "title", "About" | first %} 
{{ about_page.content | markdownify }}
