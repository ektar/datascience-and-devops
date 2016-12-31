Title: MIMIC II to MIMIC III Note Matching
Date: 2016-10-20 05:00
Category: Data Science
Tags: data science, mimic, notes, pandas, sqlalchemy
Author: Eric Carlson
slug: mimic-iii-note-matching
Status: published

[TOC]

One tricky thing to deal with in the transition from MIMIC II to MIMIC III has been that
IDs have changed and are sometimes missing, so work that a collaborating team did to annotate 
patient notes in MIMIC II is not translatable to MIMIC III.  This notebook shows one way to discover 
note relationships between the two datasets.

## Introduction

I've been working with the fantastic MIMIC dataset for several years now, and have been excited
by the new MIMIC III release.  It cleans up a lot of the old structure, adds content, and generally
is just a lot nicer to use.  (Thanks to all involved!)  In the process of developing the new
system the old way of identifying patients was reset, making it difficult to translate work from 
MIMIC II to MIMIC III.  

As an example, in the previous dataset the team had created annotations
such as "Patient 1's 3rd ICU stay has notes with indications of advanced heart failure" and "Patient 1's
7th ICU stay has
notes with indication of substance abuse".  In the new dataset the patient numbers are consistent
but the ICU stay indications are removed and times are all shifted differently, so we can't directly
apply our old annotations to the nte notes.  Ideally one could just
take a hash of the notes (e.g. MD5) and create a mapping, but the de-identification process changed
as well, so the same original note text will be different in the two output datasets we have
access to.
  
## Approach

The first part of the notebook goes through the following steps

1. Connect to MIMIC II and MIMIC III databases using SQLAlchemy
2. Load notes labeled by our annotators
3. Verify that the annotated notes match the MIMIC II source (expected)
4. Check whether they match the MIMIC III data (they did not)

I did find that subject IDs were consistent between datasets - an observation that greatly reduces
the potential search space of matches for each note.  Using this observation I was able to take
each annotated note and only try to match it to each of the same subject's notes in MIMIC III. To
identify matches, I first tried MD5 hashes - this did not work as the de-identification procedure
changed between datasets (the same source note was presented differently in the two datasets, 
causing the hash to differ).  I finally settled on a distance heuristic combining the overall note 
length, the similarity of the beginning of the note (first several hundred characters, excluding
whitespace), and the similarity of the end of the note (last several hundred characters).  When there
were multiple possible matches for a note, the note with the aggregate lowest distance was chosen
as the most probable match.

In this case thresholds for the heuristic distance measure and overall matches were chosen by
inspection, and that resulted in reasonable results.  A larger problem, or a problem with less
constrained population for potential note matches, would require a different approach - e.g.
pre-clustering (by topic, word frequency, etc), making use of extracted patient demographics (sex,
age, race), or likely diagnoses.  One could also apply more rigorous optimization for the thresholds
to balance false positives and false negatives, or could apply automated approaches to developing
distance thresholds (e.g. based on semisupervised learning).

## Notebook

{% notebook mit_freq_fliers/161020_mimic_iii_note_matching.ipynb %}

## Supporting code

{% include_code mit_freq_fliers/mimic_extraction_utils.py lang:python %}

{% include_code mit_freq_fliers/etc_utils.py lang:python %}

{% include_code mit_freq_fliers/environment.yml lang:yaml %}

{% include_code mit_freq_fliers/Makefile %}