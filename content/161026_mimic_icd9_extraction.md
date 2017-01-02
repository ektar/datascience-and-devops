Title: ICD9 Taxonomy Extraction from MIMIC III
Date: 2016-10-26 05:00
Category: Data Science
Tags: data science, icd9, mimic, pandas
Author: Eric Carlson
Series: icd9-based-patient-selection
slug: mimic-icd9-taxonomy-extraction
Status: published

[TOC]

In the previous post I showed a convenient way to navigate the ICD9 hierarchy with Python, now let's
use that to extract the full taxonomy of ICD9 codes for patients who we'll using to train a 
classifier.  In this post we'll be extracting the original ICD9 codes for all patients of interest
from the MIMIC database, extracting the ICD9 hierarchy, and saving the results for later analysis. 

The full notebook is available [here](/notebooks/mit_freq_fliers/161015_structured_data_collection.ipynb), 
but the bulk of the work happens in the accessory file `structured_data_utils.py`, which we import 
and access as `sdu`.  In the selection below I walk through using the routines in this library  

{% notebook mit_freq_fliers/161015_structured_data_collection.ipynb cells[65:95] %}

## Supporting code

{% include_code mit_freq_fliers/structured_data_utils.py lang:python %}

