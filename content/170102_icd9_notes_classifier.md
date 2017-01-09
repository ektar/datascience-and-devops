Title: ICD9-based encounter classification on MIMIC III
Date: 2017-01-02 05:00
Category: Data Science
Tags: data science, icd9, mimic, pandas, machine learning, sklearn, logistic regression
Author: Eric Carlson
Series: icd9-based-patient-selection
slug: mimic-icd9-encounter-classification
Status: published

[TOC]

We saw in the [previous post]({filename}/161230_icd9_notes_selector.md) that there is promise
to using ICD9 codes for pre-classifying encounters more likely to have our concepts of interest.  In
this post we'll walk through building simple logistic regression classifiers based on a training
data set, and will evaluate their performance on a test data set.

## Overview

As described in the [previous post]({filename}/161230_icd9_notes_selector.md), our goal here is
to build a classifier based on anything except free text data to select encounters more likely
to have notes containing concepts of interest (e.g. 'substance abuse').  The reason for this is that
we want to build up our dataset and pre-select notes more likely to have our concepts, which are
normally of low prevalence in the overall dataset.  We will later use these notes to train NLP
classifiers to detect the presence of concepts in individual notes based on the text of the note.

In the previous post we found that many of the concepts have patterns of ICD9 codes that are more 
likely than normal to appear when the concept is present in a patient's notes.  This is promising
for us in building a classifier as we know that there is information in the ICD9 codes relating
to the class labels.  It also tells us that we can build a classifier based on purely linear
interactions (e.g. a + b) and likely will not need to include cross terms (e.g. a*b) to get decent
performance.

## Approach

In this notebook I'll be using [scikit-learn](http://scikit-learn.org/)'s implementation
of logistic regression, and specifically their 
[LogisticRegressionCV](http://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegressionCV.html)
module, which implements a cross-validation loop to choose hyper-parameters for L2 regularization,
which will be used to whittle down our feature set from 181 features to a more reasonable number
of only relevant features.  

One go-to option I could have used is 
[adaboost](http://scikit-learn.org/stable/modules/generated/sklearn.ensemble.AdaBoostClassifier.html).  Adaboost 
can suffer from the problem that it tends to over-weight mislabeled datapoints - each "decision stump"
is trained in serial with previous wrongly labeled data points being given extra weight.  In this problem I
don't want that as it's expected that ICD9 codes won't give good labels that match the notes - this is especially
true because the ICD9 codes cover a patient's entire multi-day ICU stay, which may have 20 notes, some of which
have our concepts and others don't.  In those cases, every note will have the ICD9 codes assigned
but only some notes may have the concepts.

Another option was [random forest](http://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html),
but that also has its problems.  In particular, I wanted to be able to look more at feature importance - 
RF has a method of inspecting that, but it's not as straight-forward as for logistic regression.  That said,
RF is great if I have many features that represent continuous measurements, as those can be problematic
in LR as you'd have to normalize everything to comparable ranges for the weights to be comparable.

The overall process followed here is:

  1. Randomly assign every note to either test or training set by assigning a random number, then
     comparing this random number to a threshold (0.3) to create a 70% - 30% training/test data split.
     
  2. For each category, perform the following
  
    1. Create a logistic regression classifier using [LogisticRegressionCV](http://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegressionCV.html)
    
    2. Extract the feature weights and print the most important features
    
    3. Use the classifier to predict labels for our test dataset
    
    4. Find the 50% sensitivity point, corresponding to the threshold at which a point has a 50-50
       chance of being a true positive or a false negative.  We'll use this threshold for labeling
       our points later.

    5. Evaluate performance by calculating and plotting the [ROC curve](https://en.wikipedia.org/wiki/Receiver_operating_characteristic)
       and confusion matrix.
       

## Conclusion

Overall, very promising results!  We can see that we get AUC performances between 0.75 and 0.80,
which will definitely improve our selection of notes for annotation above chance, and improve our
final data set.  

Looking in detail we see that the intuition we got from looking at the ICD9 code odds ratios
was confirmed by the logistic regression feature weights.  A few examples below:

  * Advanced.Heart.Disease
  
    * (code, 420-429)	OTHER FORMS OF HEART DISEASE
    * (code, 410-414)	ISCHEMIC HEART DISEASE
    * (code, 393-398)	CHRONIC RHEUMATIC HEART DISEASE
    * (code, 785)	Symptoms involving cardiovascular system
    
  * Advanced.Lung.Disease
  
    * (code, 510-519)	OTHER DISEASES OF RESPIRATORY SYSTEM
    * (code, V46)	Other dependence on machines and devices
    * (code, 460-466)	ACUTE RESPIRATORY INFECTIONS
    * (code, 490-496)	CHRONIC OBSTRUCTIVE PULMONARY DISEASE AND ALLIED CONDITIONS
    
  * Alcohol.Abuse
  
    * (code, 570-579)	OTHER DISEASES OF DIGESTIVE SYSTEM
    * (code, 290-299)	PSYCHOSES
    * (code, V60)	Housing, household, and economic circumstances
    * (code, 070-079)	OTHER DISEASES DUE TO VIRUSES AND CHLAMYDIAE
    * (code, V08)	Asymptomatic human immunodeficiency virus [HIV] infection status
    
  * Obesity
  
    * (code, 270-279)	OTHER METABOLIC AND IMMUNITY DISORDERS
    * (code, 700-709)	OTHER DISEASES OF SKIN AND SUBCUTANEOUS TISSUE
    * (code, 510-519)	OTHER DISEASES OF RESPIRATORY SYSTEM
    * (code, 415-417)	DISEASES OF PULMONARY CIRCULATION
    * (code, 327)	ORGANIC SLEEP DISORDERS

There are some oddities, e.g. that Lung Disease's top-weighted code was "OSTEOPATHIES, 
CHONDROPATHIES, AND ACQUIRED MUSCULOSKELETAL DEFORMITIES" - possibly a medication for these is
related to lung disease, or it could be spurious, would require further investigation.

Also note that there is no way to assign causation here.  For example looking at Obesity, obesity
can lead to various diseases and sleep disorders, but people with sleep disorders and disease
can tend to exercise less or have low metabolism that contributes to weight gain.  Similarly,
alcohol abuse and addiction can lead to personal choices that contribute to poor economic 
circumstances, or people in poor economic circumstances can be predisposed to become alcohol 
abusers. 

## Notebook

Full notebook available [here](/notebooks/mit_freq_fliers/161024b_structured_data_classifier.ipynb)

{% notebook mit_freq_fliers/161024b_structured_data_classifier.ipynb cells[51:] %}
