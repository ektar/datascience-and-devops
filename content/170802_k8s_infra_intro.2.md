Title: Kubernetes-based Data Science Workbench: Intro - Design
Date: 2017-08-02 05:00
Category: Infrastructure
Tags: kubernetes, aws, docker, data science
Author: Eric Carlson
Series: k8s-based-ds-workbench
slug: k8s-based-ds-workbench-intro-design
Status: published

[TOC]

Now that we have some of our design goals in place for the new environment
we can start evaluating our options and creating the solution architecture.  It
will be critical to balance cost, performance, ease of administration, and ease
of use in order to make this a truly viable platform.

# Solution Architecture

## Primary Developer Interface

Since I plan to allocate the lion's share of the budget on cloud infrastructure
my personal interface will need to be relatively bare-boned.  I decided to go with
a Chromebook for this experiment - they can be had for surprisingly little these days,
while still packing great battery life, decent keyboards, and a linux terminal.

The specific model I ended up with is the [Asus C100P](https://www.amazon.com/ASUS-C100PA-DB01-Chromebook-Touchscreen-Laptop/dp/B00YY3X678)
flip-book.  I like that it transitions between a tablet and laptop, has ~9 hour
battery life, was available for ~$250, and still has a decent screen.

This places some additional interesting challenges for me, as the chromebooks have
little availability of native applications like IDE's.  Thankfully they do have
a full ssh terminal (although requires a bit of hackery to access it).  I use
evernote and dropbox extensively and they check those boxes.  Otherwise, however,
I'll need to used web-based tools.

When I first started this project I evaluated several web-based IDEs, including [Cloud 9](https://aws.amazon.com/cloud9/)
web-based IDE, [Che](https://www.eclipse.org/che/), and others.  C9 and Che were
the only that were really multi-language and comparable to PyCharm, my main IDE
normally.  Che was and still is fairly immature - the instructions are primarily
for running on a single host.  They have some initial directions for getting running
on Kubernetes, but it seems far from prime-time.  Cloud9, on the other hand, has
been a commercial offering for quite some time and is extremely useable.  I started
working with the product in early 2017 when I was paying $20/month.  I tried
for a while to find alternatives so that other data scientists wouldn't be locked
into this monthly charge, but Amazon bought Cloud9 in 2017 and has since made
it a free product.  I'm still excited to follow Che as it can be self-hosted,
but Cloud9 is a great alternative until then, and doesn't really lock into Amazon
services as it allows connection to other services via SSH and is still free.

## Infrastructure Management and Deployment

In my work at Philips I became extremely familiar with the virtualization
and containerization, deploying a medium-sized OpenStack deployment for data scientists
to more effectively access self-service environemnts, then deploying Rancher and 
Kubernetes on top of it to allow for rapid sharing of reproducable data science
environments.  The primary benefits I see are:

- Protection from hardware failure - if any of my underlying computers go down,
  I don't care.  In the case of OpenStack/AWS the VM will generally just get
  rescheduled elsewhere.  Most virtual environments also have easy ways to
  snapshot the "hard disk" to provide a good level of protection as well.  This
  protection is far greater if you go all the way to containers, where you treat
  the environment as immutable after creation - with build scripts (e.g. Dockerfile's)
  stored in version control (git), you can always rebuild the image at any time.

- Elimination of "Pets" - so often when managing individual computers, the systems
  evolve over time to the point that you can get scared of making too many changes
  for fear that some incompatability will arise and you can't recover.  As a result
  it gets increasingly important to attend to the care and feeding of the systems,
  carefully monitoring and making sure they're healthy.

- No "Snowflake" environments - related to the pet problem is the evolution of different  
  environments that were supposed to be identical.  One environment I worked in had
  a cluster of ~20 linux systems that were supposed to be identical, all running
  a job queuing software (PBS) for distributed computation.  The problem was that
  the computers had been manipulated by hand to the point that none of them was
  identical to the others - libraries and versions were all over the place, and programs
  that ran on some computers would refuse to run on others.  Systems
  are available to help improve this (e.g. Ansible, Puppet, Salt), but inevitably
  you get drift over time.

- Full data and result provinance - working with health care data I came to believe
  that tracking the provinance of my work was crucial.  How could anyone trust my
  models if I couldn't point exactly to the code that produce the model, the data
  the code was run against, the code in the pipeline that collected the data, and
  so on.  In an environment with "snowflakes" this is impossible - there is no
  tracking of the versions of software on the systems or their configurations,
  thus provinance is impossible.

At this point containers are hands-down the technology to go with, due to their
light weight, reproducability, tooling, and management infrastructure available.
The primary technology is of course Docker (though that's changing), and the 
main ways I've worked with to manage docker containers across a cluster of 
computers are Kubernetes, Mesos, Rancher, and Docker Swarm.  Of these I see
Kubernetes as the solution with the most growth potential and largest and healthiest
community.  Some of the main features I like about Kubernetes (also abbreviated "K8s")
are:

- Simple but flexible conceptual building blocks - Containers (single programs),
  Pods (Groups of 1 or more containers), Deployments (organization around managing pods),
  Services (Controlled network access to the pods), Jobs (repeatable executions),
  and more.  This matches well with the unix philosophy of having simple composable
  tools, and is engineered in an extremely flexible way that allows for defining
  custom resources and behaviors.

- Large community adoption - the project was started by Google (inspired by their
  "Borg" project), and has since been adopted across the industry.  This energy
  has resulted in rapid progress over the last few years, with tooling to deploy
  clusters and manage resources on them.

- No vendor lock in - unlike tools like Amazon's Elastic Container Service or
  platforms like Heroku, Kubernetes is completely open source and can be deployed
  on any cloud provider, a set of bare-metal on-prem machines, or even in your
  laptop.

- Access to advanced data-science tools - Newer versions of K8s are beginning
  to have native support for things like GPU accelerators for deep learning, which
  will be crucial for large scale data science in the future.  In addition, 
  computational software like Spark and database software like Cassandra are starting
  to support K8s more and more, making deployment of those complex systems relatively
  push-button.

## Hosting Provider

The main hosting providers I considered are AWS, Google, and Microsoft Azure,
with AWS and Google by far being my favorites.  Google's main advantage is that
they have much better native support for K8s, and now offer completly push-button
cluster deployment with free management nodes.  Amazon's large advantage is that
they have tons of services that I'm interested to also take advantage of, seem
to get newer GPUs faster (though maybe that's changing?).  

In the end I went with AWS -
I actually like that it will require some manual effort to create the cluster as
that will be a better learning/demo experience, and I already have significant amounts
of data in S3 and EBS/EFS that I want to connect to.  An additional benefit is
Amazon's purchase of Cloud9, which I'll make use of to kickstart the project.

## Administrator Experience

My goal administrator experience is for the end product to require very minimal
time to keep running and do basic tasks like adding users, creating new types
of computers, scaling nodes, or deploying new capabilities.  

To make infrastructure and application deployment as
simple and flexible as possible I'll be developing a set of Python scripts that
will read a common cluster definition file and simplify deployment and management.
My goal with this is that the administrator will be able to have a single point of
configuration, 

One area that is often quite complex (at least more time consuming than most data scientist
would like) is user management across a cluster - centralized user administration
is great but can be difficult to configure, and non-centralized user management
quickly becomes a nightmare.  The scripts I've written will also be deploying
a full LDAP solution with a web-based UI and default configuration, and all
containers will tie into this configuration to get usernames, user id's, ssh keys, etc.

## User Experience

My goal user experience for the data scientist and his/her colleagues is to be
as simple as possible to access the deployed resources and get to work.  I assume
ability to launch an ssh client as ssh tunneling is relatively simple and can
offer wonderful advantages in terms of security, as all traffic can be encrypted over
a single secured point of entry.

