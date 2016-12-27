Title: Add a control node to our AWS compute environment
Date: 2016-12-11 05:00
Category: infrastructure
Tags: aws
Author: Eric Carlson
slug: aws-compute-environment-p2
Series: aws-compute-infrastructure
Status: published

[TOC]

Now that we have a secure private network and a bastion node setup, we can start configuring 
internal servers.  Our goal is to configure as few servers as possible - not only is this easier
(hooray for lazy sys admins!), it's also more repeatable and more secure as it's easier to inspect 
and verify.  Ideally we will only minimally configure a single server to act as a deployment server, 
and all other servers will be automatically configured.  

## Create a control node virtual machine

![AWS VPC]({filename}/images/161211_setup_aws_environment/aws-step-01.png)
![AWS VPC]({filename}/images/161211_setup_aws_environment/aws-step-02.png)
![AWS VPC]({filename}/images/161211_setup_aws_environment/aws-step-03.png)
![AWS VPC]({filename}/images/161211_setup_aws_environment/aws-step-04.png)
![AWS VPC]({filename}/images/161211_setup_aws_environment/aws-step-05.png)
![AWS VPC]({filename}/images/161211_setup_aws_environment/aws-step-06.png)

## Configure SSH to login through bastion node
 
## Create environment for Ansible

## Use AWS Directory Service for user authentication

## Setup EFS for a shared user file system