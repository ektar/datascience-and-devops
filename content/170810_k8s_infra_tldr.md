Title: Kubernetes-based Data Science Workbench: TL;DR.
Date: 2017-08-10 05:00
Category: Infrastructure
Tags: kubernetes, aws, docker, data science
Author: Eric Carlson
Series: k8s-based-ds-workbench
slug: k8s-based-ds-workbench-tldr
Status: published

[TOC]

Now we'll start getting to the fun part - actually deploying our infrastructure
and launching a basic jupyterhub deployment.  While I've simplified many
steps, I've left many other intentionally exposed - to offer opportunities
for customization and to expose how things work.  What follows is a condensed
summary of the steps we'll be taking.

# Prereqs

There are a few things that need to be taken care of before we can
really get started:

- Amazon Account + IAM user for cloud9
    
    We'll be using AWS for our cloud hosting provider, and their web-based
    IDE for bootstrapping the environment.
    
- Domain registered and managed in route 53
    
    Many of the scripts depend on being able to manipulate DNS records -
    this is for acquiring secure web certificates for some of our
    services, as well as to generally make it easy to connect.

- Github Account, fork of ds-do code

    While all of the steps can be entered manually at the command line,
    the tutorial would be ~10x longer if I listed all of those steps
    explicitly.  To make it as easy as possible without dumbing down
    I've created a series of Python scripts to wrap many of the commands.
    You'll be creating your own fork of the code base so you can track
    your own changes, and hopefully submit pull requests if you
    find any bugs or have suggestions for improvement.

# Setup Bootstrapping environment

One of my design goals was to have minimal requirements for the non-cloud
environment.  This is both to reduce costs, and to simplify the instructions
as it's easier to create a reproducable cloud environment than a reproducable
laptop environment (windows vs linux vs mac, different versions, etc...).  The
steps we'll be going through are:

- Use cloud9 to create an initial bootstrapping environment

    I use Amazon's Cloud9 service to quickly create a virtual machine on 
    AWS, and to have a nice web-based development environment that places
    no requirements for the local environment other than access to a web
    browser.
    
- Setup conda python environment, configuration file

    [Conda](https://anaconda.org/anaconda/python) is used as a python environment
    manager.  We'll be running through creating a basic conda environment
    and getting started with the project.

# Launch Kubernetes

One of the easiest ways to launch Kubernetes (K8s) on AWS is 
[KOPS](https://github.com/kubernetes/kops) - Kubernetes Operations.  It provides
a relatively simple command line client for cluster management, and does a nice
job of storing the state of your cluster in S3.  We'll be using that tool, along
with my wrapper scripts, to launch a K8s cluster.

- Edit config file with your settings

    All settings for my launching scripts have been consolidated to a single
    yaml file.  We'll add our domain and other settings to that file to
    prepare for the other steps.
    
- Create kops config
 
    KOPS accepts a configuration file with details of AWS regions, subnets,
    and other info.  We'll run a script, `create-kops-config` to create this
    configuration file based on settings discovered from our Cloud9 environment.

- Edit instance groups as needed

    KOPS has the concept of `instance groups`, which are templates for virtual
    machines that will be used for different roles in the cluster.  We'll
    configure a few that will be our K8s master nodes and our permanent
    nodes that will be available 24/7 to run authentication and basic connectivity
    services.

- Launch K8s

    Will use the `kops` command to launch our cluster

# Launch base DS-DO Infrastructure

With our K8s cluster available we can now use it to host other essential
administrative services like authentication and connectivity systems.

- Launch network ingress, dashboard, and monitoring

    The initial cluster kops deploys is fairly bare-bones.  We'll be adding
    the K8s dashboard and monitoring services so we can easily inspect the
    cluster state.  We'll also be using the ds-do script `launch-ingress`
    to launch a network ingress service, which will allow us to access
    these dashboard services and future services like Jupyter and Spark.

- Create EFS-based storage for user directories

    We'll be
    leveraging Amazon's managed NFS file system storage as an easy way
    to provide this essential part of a datascience environment.  It
    can be somewhat tricky to setup correctly, so we'll use the ds-do script
    `prepare-efs` to get it launched.

- Launch LDAP

    All of our future services will require knowledge of usernames, passwords,
    SSH keys, user IDs, and other info.  LDAP is a natural fit for this,
    but can also be tricky to setup.  We'll be using the ds-do script
    `create-certs` to interact with [Let's Encrypt](https://letsencrypt.org/)
    to get valid TLS encryption certificates, then `launch-ldap` to deploy
    the basic LDAP service as well as a web-based administration interface
    for adding and managing users.

- Launch Bastion and Administration nodes

    While we're not strictly following the bastion network topology, I still
    like to have a single point of entry to the cluster - it reduces
    attack surface area, and frees us to update and create/destroy
    other internal servers as they are segregated from the essential function
    of network access.  We'll be using the ds-do scripts `launch-bastion`
    and `launch-terminal` to deploy a bare-bones bastion server for network
    access, and another container that will have more installed tools
    and can be used for the majority of administration tasks.

# Launch the JupyterHub Service

As a first real use of the system we'll be deploying a new KOPS instance
group, along with the [JupyterHub](http://jupyterhub.readthedocs.io/) multi-user 
datascience environment.  This
will make use of our LDAP system to handle user authentication, and be backed
by our EFS for user home directories.  In our environment with few users this
node can afford to be interrupted (for now), so we'll cover how to use
AWS spot pricing on these nodes to get high-powered compute resources
at 20% of the list cost.
