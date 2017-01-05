Title: Exploration into usefulness of ICD9 codes for predicting encounter note content
Date: 2016-12-30 05:00
Category: Data Science
Tags: data science, icd9, mimic, pandas
Author: Eric Carlson
Series: icd9-based-patient-selection
slug: mimic-icd9-usefulness-for-classification
Status: published

[TOC]

With the background work done in the previous posts, let's get to the meat of the problem.  I'm
currently working with a team from an excellent MIT course, 
[Secondary Analysis of Health Records](http://criticaldata.mit.edu/course/), led by Dr. Leo Anthony 
Celi. My team is composed of 4 clinicians and 3 data scientists, and we are looking into the problem 
of "frequent fliers" in the ICU - patients who frequently cycle into the ICU for care.  If a
classifier can be created to predict which patients are likely to be in this group, a hospital may
be able to create a program addressing these patients to help prevent these readmissions.

## Overview

An interesting aspect of the question is that many of the factors likely contributing to a patient 
being a "frequent flier" are not well represented in structured medical records.  As an example, 
a patient who is a substance abuser is very likely to be a "frequent flier", but many of these 
patients would not have any specific label identifying them as a substance abuser. Luckily we have
access to the notes from the medical staff written during the patient's stays, and in these notes
are often great clues indicating the conditions we're interested in.  Our task, then, is to design
an NLP-based classifer that will process these notes and provide an indication of whether any of
our concepts are present, e.g. whether the patient is a substance abuser.

Our team is pursuing a supervised learning approach, in which the clinicians on our team have labeled
1000 notes randomly selected from a pool of 40,000, and the data scientists are training classifiers
for our concepts.  What we've found is that some concepts are very low prevalence - e.g. for 1000
notes there are concepts that only have 20 or fewer positive examples.  The problem this presents
is that the machine learning algorithms are likely to discover spurious correlations that are not
true in general application - e.g. if all 20 patients happen to be from a neighborhood that is 
referenced in the note then the classifier may "think" that a note with that neighborhood referenced
means the patient is a substance abuser, and if that neighborhood isn't referenced then the patient
is not a substance abuser.

In order to create a more balanced dataset we decided to enlarge the dataset by having the 
clinicians label additional notes, but wanted to select notes that were more likely than chance
to contain our concepts.  

One option was to use our existing text-based classifiers to choose 
un-annotated notes, annotate those new notes, and use those all to train new classifiers.  The 
problem with this option is that its circular and will re-enforce the existing classifier biases:
notes that are in the true-positive region of the classifier will be selected for annotation and 
training, but the were already being correctly identified, false-positive notes will be selected
and annotated which may be helpful to improve specificity, but false-negative notes will not be
included and so sensitivity will not improve.

The alternate option I pursue here is to use a separate mode of data for a secondary classifier
that will only be used to select notes for annotation.  I base this classifier on ICD9 diagnosis
codes during the patient's stay.  In this way I avoid the circular problem of using the same
classifier to choose its own training data - there still may be issues of bias, but hopefully
this will be minimized, and will optimize our annotation time.

## Approach

The full notebook is available [here](/notebooks/mit_freq_fliers/161024b_structured_data_classifier.ipynb),
but the main first result of the notebook is highlighted below.  This first result is an inspection
of how informative the ICD9 codes are to whether the notes will have a particular concept or not.

A summary of the steps taken are as follows:

  1. Load patient data from previous post
  2. Inspect the number of ICD9 codes in the dataset

     This is especially important because of the low prevalence of notes and relatively small
     overall dataset.  If the dataset is much "wider" than it is "tall" - if there are relatively
     few labels compared to the number of possible features to consider - it is unlikely that 
     resulting classifiers will perform well on general datasets as overfitting is likely.  Here
     we find that there were 1852 raw ICD9 codes found.  When we go to only top-level ICD9 codes
     using the previously explored ICD9 taxonomy we get only 42 codes.  Going to one level down
     we get 181 codes, and two levels down we get 632 codes.
     
  3. Choose an ICD9 clustering level, assign each note with a 1 or a 0 whether that ICD9 cluster
     was present
     
     These will end up being the input feature vectors for our classifier - the presence of
     ICD9 clusters being used to predict whether the note has a particular class label.  I start
     with "level 1" as by experience 181 codes seemed feasible, but this would just be a first pass -
     for a real problem we could try different levels and determine the best.
     
  4. Get an idea of how informative the ICD9 codes will be for building a classifier by looking
     at the odds ratios.  Essentially, looking for codes that are more likely than average
     to be present for particular concepts.  If a concepts has many ICD9 codes that are much
     more likely to be present than it's likely we'll be able to build a good classifer, whereas
     if all of the codes are present in a distribution similar to the population it will be 
     challenging (though possibly combinations of codes are more likely present, etc.)

## Conclusion

It turns out that this worked better than expected!  Several concepts have expected ICD9 code 
relationships, a great indication that this method is given sensible results overall.  Some examples below:

  * 'Advanced.Cancer'
 	
 	* (code, 190-199)	MALIGNANT NEOPLASM OF OTHER AND UNSPECIFIED SITES
 	* (code, V87)	OTHER SPECIFIED PERSONAL EXPOSURES AND HISTORY PRESENTING HAZARDS TO HEALTH	
 	* (code, 170-176)	MALIGNANT NEOPLASM OF BONE, CONNECTIVE TISSUE, SKIN, AND BREAST
 	
  * 'Advanced.Lung.Disease'
  
  	* (code, 980-989)	TOXIC EFFECTS OF SUBSTANCES CHIEFLY NONMEDICINAL AS TO SOURCE
  	* (code, E869)	Accidental poisoning by other gases and vapors
  	* (code, 799.1)	Respiratory arrest
  	* (code, V46)	Other dependence on machines and devices
  	* (code, 460-466)	ACUTE RESPIRATORY INFECTIONS
  	
What was interesting was looking at the more nebulous concepts such as alcohol abuse or depression,
concepts that aren't necessarily well represented by the billing codes.  We see that a cluster
of ICD9 codes appears to be more likely for these groups in ways that are sensible and 
expected in hindsight, but surprising that they were found.

  * 'Alcohol.Abuse'

    * (code, 840-848)	SPRAINS AND STRAINS OF JOINTS AND ADJACENT MUSCLES
    * (code, V62)	Other psychosocial circumstances
    * (code, E980)	Poisoning by solid or liquid substances, undetermined whether accidentally or purposely inflicted	
    * (code, E967)	Perpetrator of child and adult abuse
    * (code, V69)	Problems related to lifestyle
    
  * 'Depression'
  
  	* (code, E931)	Other anti-infectives
  	* (code, E960)	Fight, brawl, rape
  	* (code, E967)	Perpetrator of child and adult abuse
  	
  * 'Other.Substance.Abuse'
  
  	* (code, E960)	Fight, brawl, rape
  	* (code, 840-848)	SPRAINS AND STRAINS OF JOINTS AND ADJACENT MUSCLES
  	* (code, 070-079)	OTHER DISEASES DUE TO VIRUSES AND CHLAMYDIAE

In the next post we'll follow this up by building classifiers and seeing what kind of performance
we can attain.

## Notebook

Full notebook available [here](/notebooks/mit_freq_fliers/161024b_structured_data_classifier.ipynb)

{% notebook mit_freq_fliers/161024b_structured_data_classifier.ipynb cells[26:51] %}
