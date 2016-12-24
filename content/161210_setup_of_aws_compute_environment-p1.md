Title: Secure compute environment on AWS, part 1 
Date: 2016-12-10 05:00
Category: infrastructure
Tags: aws
Author: Eric Carlson
slug: aws-compute-environment-p1
Status: published
Summary: Creation of the networking and bastion server for a secure compute environment on AWS 

I do most of my analysis now on cloud infrastructure as much as possible.  The primary advantages
are:

1. I can quickly scale compute resources as needed for large problems
2. I can access unlimited cheap storage (e.g. S3) as needed
3. I can get by with a cheaper and lighter laptop as it's only acting as a thin client
4. My hardware doesn't go obsolete - as processing, disks, and gpu get cheaper they become available for rent as needed
5. I can quickly deploy advanced technology like hadoop clusters, Kubernetes, etc

One concern using the cloud is security - it's easy to quickly create an ubuntu server on AWS, but
there's always the worry that you'll leave an open port or that a service will become vulnerable
and you'll be too slow to apply the patches.  A great way around this is to make use of a Bastion
Node - a server that has very limited access (generally ssh only) and only serves to provide
access to the rest of the internal systems.  By only running an ssh server you are dramatically
reducing surface area for potential attacks, and reducing the necessary maintenance overhead
of keeping things up to date.  Internal servers can be much more fully featured and more open to
each other, and you can be much less concerned about intrusions.  A downside is that you now
have to go through this bastion node to access internal servers, but with a properly configured
ssh config file this becomes nearly transparent.
 
An overview diagram of what we'll setup is below:

![Bare Website]({filename}/images/161210_setup_of_aws_compute_environment/environment_overview.png)

The primary components:

* Bastion node for access the network, from there we can connect to any server in our private net.  
* Jupyter server for web-based analysis in Python, R, Julia or others.
* A Kubernetes cluster will be deployed for quickly launching services. 
* EMR Hadoop environments can be connected for Spark other services on demand.  
* A control node for will be created to configure everything. 
* A NAT router is added to provide internet access to the internal nodes, for security updates, github access, etc
 
