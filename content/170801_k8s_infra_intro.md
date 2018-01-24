Title: Kubernetes-based Data Science Workbench: Intro
Date: 2017-08-01 05:00
Category: Infrastructure
Tags: kubernetes, aws, docker, data science
Author: Eric Carlson
Series: k8s-based-ds-workbench
slug: k8s-based-ds-workbench-intro
Status: published

[TOC]

One of the most daunting tasks of getting going on a personal data science
project can be just getting started with the environment.  What I generally want
is instant access to the latest technology stack (hopefully at low cost), 
allowing me to get to work quickly while also exploring the most recent tools and 
sharpening my skills.  While there are some quick-start environments around, 
most seem to suffer from significant vendor lock-in, limiting the actual 
usefulness of the environments.

# Overview

I recently parted ways with my MacBook Pro laptop and faced a decision - buy
another, or try something new?  It would be convenient to just go with
what I'm comfortable with, but I've been experimenting with lots of interesting 
technology lately and want to see if I can do better.

If I were to purchase a new personal computer for data science projects I'd
be most tempted by a 15" MacBook Pro.  My main motivations for Mac are how
close it is to Linux, while still being friendly for applications like
Adobe Lightroom/Photoshop and Finale/Sibelius music editing software
(hobbiest photographer with composer wife).  I used Linux on my desktop/laptop
for ~10 years, but finally just got sick of compiling video drivers or plugging
my laptop into a projector and having to edit X11 config files to make it work.
While I've been extremely happy with the Macs, the downsides for modern data science
are:

- Locked into the hardware - Once I've paid $4k for a computer I can be hesitant
  to use anything else.  While that $4k computer may be tremendous overkill for
  many day-to-day tasks, it can be underpowered for anything of scale.

- Unreproducable - The traditional laptop model is essentially a that of a pet - I carefully
  curate what software gets installed, and over time I end up with a snowflake - 
  different from every other computer, completly unreproducable, and if I lose it
  I'm screwed.  I can try to use conda/virtual environments to let others reproduce
  my code, but that can often only go so far.

- Lack of community - Ideally I'd love to be able to build and share with others,
  as people create great new things, being able to quickly deploy and access those
  resources, and share back to the community.  This is extremely difficult
  when everyone only has access to completely different environments.  With all 
  the great tools now available (TensorFlow, PyTorch, SparkNLP, etc) this is
  increasingly improtant to me.

- Lack of continuity to scale - Getting a pet project working on a laptop is one
  thing, getting it running at scale and being served with high availability is
  often a completely separate step, but it doesn't have to be!  I'm convinced
  that it's now possible to have a personal environment that's easy and cheap to build
  and that can allow both exploratory model development and potential large-scale
  training and high-availability deployment as needed.

In this series of posts I'll describe my decisions in building a better personal
data science environment -
one that is cost-similar to that new laptop, but that allows large-scale model
building and facilites reliable algorithm deployment and pipelining.

# Design Goals

Some of the user stories that I have in mind for this project are:

- As a data scientist I need to be able to access the latest software quickly.
  There can be a wide range of such software, including standard relational databases
  (Postgres, MariaDB), next-generation databases (Mongo, Elastic Search, OrientDB,
  Cassandra), scalable compute infrastructure (Spark, Dask), and more.
  
- As a data scientist I need to be able to spend the minimal time necessary to
  prepare and manage my environemnt, so that I can spend the majority of my time
  performing data science rather than systems administration tasks.

- As a user I need to be able to reliably and simply access the systems - it
  should not require more than 1-2 steps to be up and running after the infrastructure
  is created.

- As a researcher engaging in personal projects (as opposed to commercial) the 
  infrastructure needs to be inexpensive - defined here
  as cost-similar to the Mac laptop ($4000) over a 2 year time frame.

- As a community member, everything I build and use should be open source and openly licensed
  so that I can share my learnings and benefit from other's comments.

- As a data scientist I should be able to have quick access to high-end hardware
  as needed (e.g. GPU), but I shouldn't pay for resources that aren't in use.

- As a data scientist I should be able to cost-effectively scale up as needed - 
  even for personal projects data sets can easily get into terabyte range, and 
  it must be possible to scale storage and compute resources to accomodate.

- As a user I want to be free from vendor tie-in - able to move between companies
  as prices or capabilities change or my needs vary.

- As a community member it should be possible to invite others into my environment - 
  easy to setup new accounts and collaborate with fellow researchers.

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

In my work at Philips I became extremely familiar with the benefits of virtualization
and containerization, deploying a medium-sized OpenStack deployment for data scientists
to more effectively access self-service environemnts, then deploying Rancher and 
Kubernetes on top of it to allow for rapid sharing of reproducable data science
environments.  

## Hosting Provider

## Administrator Experience

## User Experience

# Expected Cost

Pellentesque feugiat felis at purus ultrices, ut consequat arcu finibus. Sed gravida leo a lorem eleifend auctor. Ut ex nunc, pharetra non suscipit in, tincidunt a magna. Ut vitae urna vitae lectus faucibus ultricies. Quisque vel nisl eget nulla porta dapibus quis ac ipsum. Vestibulum rutrum, odio vitae accumsan blandit, lectus orci iaculis dolor, facilisis sagittis velit lectus non dui. Donec id leo pellentesque, pretium justo et, vestibulum metus. Nam elit eros, euismod id rhoncus aliquam, auctor sed nibh.

# Security

Pellentesque feugiat felis at purus ultrices, ut consequat arcu finibus. Sed gravida leo a lorem eleifend auctor. Ut ex nunc, pharetra non suscipit in, tincidunt a magna. Ut vitae urna vitae lectus faucibus ultricies. Quisque vel nisl eget nulla porta dapibus quis ac ipsum. Vestibulum rutrum, odio vitae accumsan blandit, lectus orci iaculis dolor, facilisis sagittis velit lectus non dui. Donec id leo pellentesque, pretium justo et, vestibulum metus. Nam elit eros, euismod id rhoncus aliquam, auctor sed nibh.

# Limitations

Pellentesque feugiat felis at purus ultrices, ut consequat arcu finibus. Sed gravida leo a lorem eleifend auctor. Ut ex nunc, pharetra non suscipit in, tincidunt a magna. Ut vitae urna vitae lectus faucibus ultricies. Quisque vel nisl eget nulla porta dapibus quis ac ipsum. Vestibulum rutrum, odio vitae accumsan blandit, lectus orci iaculis dolor, facilisis sagittis velit lectus non dui. Donec id leo pellentesque, pretium justo et, vestibulum metus. Nam elit eros, euismod id rhoncus aliquam, auctor sed nibh.
