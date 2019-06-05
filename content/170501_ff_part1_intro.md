Title: Deep learning models for text-based patient phenotyping 
Date: 2017-05-01 05:00
Category: Data Science
Tags: data science, deep learning, mimic
Author: Eric Carlson
Series: frequent-flier-phenotyping
slug: dl-text-phenotyping-intro
Status: published

[TOC]

This year I've had the pleasure of participating in a team at MIT identifying
characteristics that make patients likely to be intensive care unit "Frequent Fliers" - patients
with multiple ICU admissions in a short time span.  This series will explore the implementation
of text-based patient phenotyping we use as a first step towards this goal. 

## Overview

Patients who experience frequent Intensive Care Unit (ICU) re-admission ("Frequent Fliers") are at
high risk of negative outcomes, even relative to other ICU patients (already at ~10-20% mortality 
rates), with observed mortality rates of 40% or more[ref][Acute heart failure: how to cut down on "frequent flyers"](http://www.todayshospitalist.com/Acute-heart-failure-how-to-cut-down-on-frequent-flyers/)[/ref].
In addition to the impact to the patient himself, these patients account for an estimated 50%
of ICU costs, despite only making up approximately 5% of the ICU population[ref][The Happy Hospitalist](http://thehappyhospitalist.blogspot.com/2012/12/Attitudes-About-Frequent-Flyers-In-Hospital-From-Doctors-Nurses-someecard-Explanation.html)[/ref].

While the problem of Frequent Fliers is widely recognized, the solution is elusive as the causes
are varied and complex.  In some cases the traditional health system could play a larger role, by
highlighting comorbidities or complications that that may call for more intensive discharge 
disposition planning or other interventions.  Other cases, however, stem from socio-economic causes
such as food or housing insecurity, psychological problems, or other issues that our current health
system is poorly suited to address.  One representative account describes a patient with several
comorbidities, primarily congestive heart failure (CHF) and chronic kidney disease (CKD), complicated
by psychological issues[ref]["Yes, We Do Give Frequent Flyer (S)Miles"](http://journalofethics.ama-assn.org/2009/03/mnar1-0903.html)[/ref].
Pilot programs have begun to implement more holistic responses[ref][Two Ways to Deal with ED "Frequent Fliers"](http://www.physiciansweekly.com/two-ways-deal-emergency-department-frequent-flyers/)[/ref], but these are far from common.

Last year I was able to attend Dr. Leo Celi's Secondary Analysis of Health Records 
course[ref][Secondar Analysis of Health Records](http://criticaldata.mit.edu/course/)[/ref], and had
the good fortune of pairing up with a great team of students and physicians to investigate these problems
further.  We've recently published our first paper on Arxiv[ref][Comparing Rule-Based and Deep Learning Models for Patient Phenotyping](https://arxiv.org/abs/1703.08705)[/ref]
in which we describe a deep learning method for extracting frequent-flier-related patient phenotypes 
from free text notes.  This is an important first step to the investigating the problem of frequent 
fliers, as many of the concepts that contribute to this problem (e.g. medication non-compliance,
substance abuse) are poorly represented in structured data elements.

## Approach

The general approach taken was as follows:

  1. The team clinicians identified 10 patient phenotypes that are recognized for being contributing
  	factors for ICU readmission, while also being difficult to assess from structured data.  Examples 
  	include chronic pain, alcohol abuse, depression, and medication non-compliance.  
  	 
  2. Discharge summaries and nursing notes were extracted from MIMIC 2, and a random sample of ~1000
    notes were inspected by the team clinicians and annotated with the presence or absence of the
    determined clinical concepts.
    
  3. As several concepts have a low prevalence in the patient population, an imbalanced class problem
    arose.  To address this we sought to increase the number of positive examples in our annotated
    dataset.  Classifiers were created using our already-annotated notes, to use ICD9 codes as inputs
    and identify patients with increased probability of having notes with our concepts.  ICD9 codes were
    used as they were not used elsewhere in this analysis, and so may reduce the potential for an
    Ouroboros issue of the analysis output contributing to the input.  This classification task is 
    described in the [ICD9-based encounter classification series]({static}/170102_icd9_notes_classifier.md).
    Notes classifed with those algorithms as being likely positives were extracted, annotated, and
    added to our dataset.
    
  4. Word embeddings were trained, using the [gensim](https://radimrehurek.com/gensim/) implementation
    of word2vec.  As word2vec is a completely unsupervised method, we were able to train embeddings 
    using notes from all ~50,000 patients, not just the ~1,000 we'd annotated.  This greatly improved
    the quality of the calcuated embeddings.
    
  5. Rules-based concept discovery (based on the [cTakes](http://ctakes.apache.org/) tool) was used
    as a baseline for further algorithm comparison.
    
  6. A deep learning model was defined and trained on our dataset, and compared to the rules-based
    method.

## Series Overview

The series focuses on the development of the deep learning model, and is broken into several sections:

  - ICD9-based phenotype classification, covered previously
  - Word2Vec embedding training
  - Deep-learning phenotyping implementation in Keras
  
## References
