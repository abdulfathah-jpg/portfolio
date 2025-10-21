---
title: "The Question of Semantics"
excerpt_separator: "<!--more-->"
categories:
  - project1
tags:
  - Reflective Posts
  - Machine Learning
image: images/cer.jpg
---

<!--more-->

One of the first things that struck me while reading about Character Error Rate (CER) and Word Error Rate (WER) was the kind of quantitative precision they offer, but also the qualitative void they create. This tension feels familiar to us from the long-standing debate in digital humanities between quantitative and qualitative approaches.

CER and WER are excellent numerical benchmarks for evaluating structured documentation: applications, forms, anything iterative where human engagement relies on a background of formal evaluation. But the same cannot be said for many historical manuscripts we attempt to digitize. Imagine pre-automation handwritten texts: using CER or WER, an OCR model produce text that is syntactically correct yet semantically nonsensical to a reader. It would still achieve a low error score. Or conversely, a human-like transcription with minor deviations could be penalized heavily. For instance, in Persian texts, an OCR-generated transcription might reproduce every character accurately according to the model, while a human transcription might capture semantic subtleties and contextual conventions that the model misses entirely. The metrics would favor the OCR output, even though the human version may convey meaning more faithfully.

Consider a Persian manuscript: the original reads “پادشاه به باغ رفت تا گل‌ها را ببرد” (“The king went to the garden to pick the flowers”). An OCR transcription might produce “پادشاه به باغ رفت تا گل‌ها را بو کِشد,” changing the verb and altering meaning. WER still scores it highly because word correspondence is close. An alternative transcription, semantically faithful, may write “پادشاهِ به باغِ رفت تا گُل‌ها را بِبَرَد” with diacritics. WER penalizes this, giving a lower score, even though meaning is preserved. Numeric metrics favor visual accuracy over semantic fidelity.

The challenge extends further with spelling, grammar, and formatting variations in handwritten texts, or older conventions. I recently encountered this myself while correcting a Persian manuscript transcription: a comma appeared above a word, and I initially transcribed it as a hyphen to match the visual representation. In reality, it could correctly be rendered as an Arabic-style comma, reflecting historical writing conventions. CER treats this as a mistake, ignoring the nuance, because it evaluates absolute character correspondence rather than contextual meaning.

This highlights a limitation: current OCR evaluation metrics do not capture the qualitative consciousness embedded in human reading. Can machine learning ever embed this “consciousness” in a meaningful way? Perhaps not in the philosophical sense, but we can approximate it through semantic metrics like BLEU, METEOR, and ROUGE, which evaluate meaning rather than just characters. Pairing these with human evaluation paradigms opens the door to models that could machine learn from human judgment, in same way a transcription model learns from human corrections. This would in fact create specialized models for the kinds of manuscripts we are dealing with.
