Title: ICD9 Navigation in Python
Date: 2016-10-25 05:00
Category: Data Science
Tags: data science, icd9
Author: Eric Carlson
Series: icd9-based-patient-selection
slug: icd9-python-navigation
Status: published

[TOC]

[ICD9](http://searchhealthit.techtarget.com/definition/ICD-9-CM), the International Statistical 
Classification of Diseases, is one of the common coding systems
often used in medical databases for indicating patient conditions.  A handy feature of it is that
it's a hierarchical system.  Just as the Dewey Decimal System lets someone quickly find a book on
geometry (library aisle 500 for "Natural sciences and mathematics", bookcase 510 for "Mathematics",
and shelf 516 for "Geometry"), the ICD9 allows researchers to drill down into disease categories, 
or up from a patient's specific diagnosis to a more general condition.

## Introduction

I'll be using the ICD9 taxonomy in later notebooks as a convenient way to reduce the number of
features for a classifier.  The problem I'll be working on is trying to predict whether a patient
has notes with a particular label (e.g. "substance abuse") from their ICD9 codes.  The difficulty
is that I don't have very many labeled notes and there are thousands of ICD9 codes.  Classification
based on such a dataset is likely to overfit - the machine learning algorithms can essentially
memorize the training dataset to achieve good performance, but the algorithm won't generalize.  By
using parent conditions (e.g. "Intestinal infectious diseases" rather than "Salmonella 
gastroenteritis") we can quickly group together patients who have meaningfully similar conditions.

Happily, I found a very convenient Python library for navigating this hierarchy, located 
[here](https://github.com/sirrice/icd9).  The notebook below walks through a few simple operations
with it, and in a later post I'll show how I combined it with scikit-learn to help select medical
notes for further annotation.

## Notebook

{% notebook mit_freq_fliers/161023a_icd9_testing.ipynb %}
