---
title: "Mapping Islam on the UNESCO List"
excerpt_separator: "<!--more-->"
categories:
  - project1
tags:
  - Projects
  - Heritage
  - Machine Learning
image: images/yemenbanner.jpg
---

Can we identify historical trends in the share of Islam-related sites among UNESCO World Heritage inscriptions from 1978 to the present? How has the relative representation of the Islamic world changed over time, and what can these patterns reveal about broader historical, political, and institutional shifts within UNESCO and across Muslim-majority countries?

<!--more-->

## What we did:

1.	Data: We used a local copy of the WHL description files (one text file per site). Each filename begins with a year (e.g. 1978_0001.txt), which we used as the inscription year.

2.	Keyword search (hypothesis): We marked a site as “Islam-related” if its description contains any of the words: mosque, muslim, or islam (case-insensitive).
            
    *	Important caveat: the presence of these words is an imperfect proxy. Some relevant sites might not use those words in the description; some mentions might be incidental (e.g., a comparative remark, or mention of a mosque in passing). So, there is a margin of error. Moreover, wording in site descriptions may change over time (editing conventions, translation changes, or differences in who writes the description). This can affect the the number of mentions independent of real heritage prioritization.

3.  Two counts:
             
    *	Absolute: number of sites per year with any keyword match.

    * Relative: percentage of that year’s newly inscribed sites that match the keyword. This controls for years with unusually many or few inscriptions.

4.	Smoothing: To see medium-term trends, we grouped years into five-year bins, summed the yearly percentages in each bin and then divided by the actual number of years that contributed data to that bin (some bins lack one or more years). This creates a true five-year average percentage for each bin.

5.	Visualization: We plotted the five-year averages as a bar chart with labels like 1978–1982, 1983–1987, etc. The bar chart plotted in five-year averages makes temporal shifts immediately visible. However, in this case, individual years with fewer or higher percentages can swing the average five-year percentages dramatically. To tackle this problem, we often refer to individual year data for more nuance in the argument.

A more detailed workflow of the process could be viwed in the [Google Collab Platform](https://colab.research.google.com/drive/1bacC14g2-toGkpJajazivGi-H1DGQPqp?authuser=1#scrollTo=0HMqajL5r2Wn)

![Yearwise (1978-2025) Relative Share of UNESCO Muslim Heritage sites]({{site.baseurl}}images/yearwise_bar.png)

![Five Year Average Share of UNESCO Muslim Heritage sites]({{site.baseurl}}images/fiveyear_bar.png)

## Trends Across Time

Our bar chart result reveals a fascinating and non-linear pattern:

*	Starting in 1978, Islamic-related sites made up roughly 14% of all new inscriptions.

* This proportion rose steadily through the 1980s, reaching around 20% between 1983–1987.

*	After 1988, the proportion dropped sharply to around 11%, and remained relatively low through the early 1990s.

*	In the early 2000s, however, we observe a resurgence, peaking at over 21% between 2003 and 2007, the highest five-year average in the dataset.

*	Through the 2010s, Islamic heritage remained prominently represented before declining slightly in the early 2020s to about 12%.

When looking at specific years, 1985 and 2003 stand out as peaks - around 30% and 29% of all sites added - while 1994, 1998, and 2005 marked lows, sites related to Islam accounted for only 3% of all sites.

## Historical Interpretation: Why These Patterns?

The fluctuations in the chart is not random, they mirror larger historical, political, and institutional shifts within UNESCO and across the Islamic world.

#### 1. Early Growth (1978–1987): Expansion

The initial rise in Islamic-related World Heritage listings during the mid-1980s reflected UNESCO’s maturation phase. The World Heritage Convention (1972) was still young, but by the early 1980s the nomination process had stabilized. Under Director-General Amadou-Mahtar M’Bow (1974–1987), UNESCO sought greater geographic balance, countering its early Eurocentrism.

Meanwhile, Muslim-majority countries such as Morocco, Egypt, Iran, Turkey, Pakistan, and Yemen began using heritage nominations as tools of cultural diplomacy and postcolonial identity-building. The 1979 Iranian Revolution sparked a broader Islamic cultural revival, prompting restoration of key cities like Fez, Kairouan, Lahore, and Sana’a. Combined with oil wealth and the creation of ISESCO (1982), these efforts coincided with UNESCO’s growing recognition of living urban environments, a model that fit Islamic medinas and mosques particularly well.

#### 2. The Decline (Late 1980s–1990s): Diversification

The drop around 1988 came as UNESCO broadened its focus to include natural, industrial, and non-Islamic sites. It was seeking greater global balance after many key Islamic sites were already listed. At the same time, budget cuts and the withdrawal of the U.S. and U.K. (1984–1997) from UNESCO reduced resources. This slowed down new nominations from developing Islamic countries that relied on UNESCO’s support.

#### 3. Resurgence (Early 2000s): Global Attention to the Islamic World

The sharp rebound in the early 2000s coincides with a period of intense global focus on the Islamic world following 9/11 and the “War on Terror.” While this attention was political, it also spurred academic, cultural, and preservationist interest in Islamic heritage. UNESCO, emphasizing cultural dialogue and mutual understanding, supported more nominations from Muslim-majority countries

#### Recent Years (2010s–2020s): Renewed Balance

In recent decades, the percentage has gradually decreased again —   likely because of greater regional diversification and increasing attention to Africa, Oceania, and the Americas. By 2023–2027, Islamic-related sites account for roughly 12%, indicating a normalization after earlier peaks.

To conclude, by systematically analyzing site descriptions — counting keywords, calculating yearly percentages, and averaging over five-year bins — we were able to track historical trends in Islamic-related World Heritage inscriptions. The results show fluctuations shaped by UNESCO policies, geopolitical events, and cultural priorities: a surge in the 1980s, a decline in the 1990s, and a resurgence in the early 2000s. 

