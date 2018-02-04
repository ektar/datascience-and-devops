Title: Workbench Outline
Date: 2017-08-10 05:00
Category: Infrastructure
Tags: kubernetes, aws, docker, data science
Author: Eric Carlson
Series: k8s-based-ds-workbench
slug: k8s-based-ds-workbench-outline
Status: draft

[TOC]

# tl;dr.

- Prereqs
    - Amazon Account + IAM user for cloud9
    - Domain registered and managed in route 53
    - Github Account, fork of ds-do code
- Setup Bootstrapping environment
    - Use cloud9 to create an initial bootstrapping environment
    - Setup conda python environment, configuration file
- Launch Kubernetes
    - Edit config file with your settings
    - Create kops config
    - Edit instance groups as needed
    - Launch K8s
    - Connect and test
- Launch base DS-DO Infrastructure
    - Create EFS-based storage for user directories
    - Launch LDAP
    - Launch Bastion and Administration nodes
- Launch Jupyterhub Service

# Prereqs

## Local computer setup

## Amazon account and IAM sub user

## Domain

Step 2 only from:

https://aws.amazon.com/getting-started/tutorials/get-a-domain/

## Github

Account, create fork

# Initial launching environment

## Cloud 9 overview

## Create python environment

## Clone github fork

## Python environment & Conda

## Configure SSH to connect to environment (Optional)

# Launch Kubernetes

## Edit config file

## Create kops template

## Launch kubernetes and test

## Launch Ingress and test

# DSDO Infrastructure Deployment - LDAP

## Overview

## Create TLS Certificates

## Deploy LDAP + LDAP-UI

## Configuration

## Maintenance

# DSDO Infrastructure Deployment - Storage and Access Nodes

## EFS

## Bastion

## Administration Terminal

## Copy LetsEncrypt folders

# Launch Jupyterhub