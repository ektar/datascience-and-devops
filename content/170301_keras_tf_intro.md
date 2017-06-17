Title: Getting started with Keras + Tensorflow
Date: 2017-03-01 05:00
Category: Data Science
Tags: data science, deep learning, keras, tensorflow
Author: Eric Carlson
slug: keras-tensorflow-getting-started
Status: published

[TOC]

I've recently been upgrading my toolset to the latest versions of Python, Keras, and Tensorflow, all
running on a docker-based GPU-enabled deployment of Jupyter with CUDA 8 installed.  In this notebook
I walk through a quick test to verify that the GPU is recognized and is working, and define and 
train a basic CNN for the classic MNIST digit recognition task.

## Overview

This entry is pretty self explanatory, pretty much going through the basics of loading modules,
checking GPU detection, and model definition.

I found that the following references were helpful to get going:

  * https://elitedatascience.com/keras-tutorial-deep-learning-in-python
  
    First network I saw and what was implemented

  * https://blog.keras.io/keras-as-a-simplified-interface-to-tensorflow-tutorial.html
  
    For adapting for TensorFlow (had been Theano) and 2.0 api 

  * http://machinelearningmastery.com/handwritten-digit-recognition-using-convolutional-neural-networks-python-keras/
  
    Very similar network, also comparison to other networks and some nice explanations
  
In addition to the above, this notebooks makes a few improvements for the latest library
versions, and adaptations for Python 3.x.

## General Notes

As long as the libraries are installed properly, this notebook should be able to be executed as-is.
While the epochs are running it can be instructive to check your GPU status, e.g. using `nvidia-smi`.

I observed the following output before execution:

	$ nvidia-smi
	Sat Jun 17 19:05:40 2017
	+-----------------------------------------------------------------------------+
	| NVIDIA-SMI 375.66                 Driver Version: 378.13                    |
	|-------------------------------+----------------------+----------------------+
	| GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
	| Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
	|===============================+======================+======================|
	|   0  Tesla M40 24GB      Off  | 0000:00:06.0     Off |                    0 |
	| N/A   37C    P0    58W / 250W |  21798MiB / 22939MiB |      0%      Default |
	+-------------------------------+----------------------+----------------------+
	
	+-----------------------------------------------------------------------------+
	| Processes:                                                       GPU Memory |
	|  GPU       PID  Type  Process name                               Usage      |
	|=============================================================================|
	+-----------------------------------------------------------------------------+

And this while running:

	$ nvidia-smi
	Sat Jun 17 19:09:25 2017
	+-----------------------------------------------------------------------------+
	| NVIDIA-SMI 375.66                 Driver Version: 378.13                    |
	|-------------------------------+----------------------+----------------------+
	| GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
	| Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
	|===============================+======================+======================|
	|   0  Tesla M40 24GB      Off  | 0000:00:06.0     Off |                    0 |
	| N/A   39C    P0    74W / 250W |  21915MiB / 22939MiB |     28%      Default |
	+-------------------------------+----------------------+----------------------+
	
	+-----------------------------------------------------------------------------+
	| Processes:                                                       GPU Memory |
	|  GPU       PID  Type  Process name                               Usage      |
	|=============================================================================|
	+-----------------------------------------------------------------------------+

Note power increase of 16 W, slight temperature increase (2C), GPU utilization from 0 to 28%.

I was surprised that no processes appeared in the process list, will need to look into that.

## Notebook

Full notebook available [here](/notebooks/deep-learning/170301-deep-learning-intro.ipynb)

{% notebook deep-learning/170301-deep-learning-intro.ipynb %}
