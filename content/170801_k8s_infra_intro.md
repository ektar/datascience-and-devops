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

# Expected Cost

Given that this is a project intended primary for personal use, I've been quite
careful in making selections that minimize cost wherever possible.  As an example,
a default installation of some of the software can make use of Virtual Private
Clouds with private networks, which require a special interface ("NAT") for
computers on that network to reach the outside.  That's all great for security,
but that default NAT device from Amazon can cost as much as a single compute VM,
and needs to be running 24/7.

The solution I've come up with consists of the following:

- [Base infrastructure](https://aws.amazon.com/ec2/pricing/on-demand/)

    - Master node: t2.micro - $ 0.0116/hr, approx $8/mo
     
        The master is the node that is really managing K8s and helping to determine
        which compute node gets which work.  It needs to always be running, but
        doesn't require significant memory or cpu so can be a very low powered
        instance.
  
    - "Admin" node: 2 x t2.small - $ 0.023/hr, approx $16/mo * 2, $32/mo
   
        I designate 2 nodes to be "administration" nodes - nodes that are on 24/7
        to run basic connectively functionality like the LDAP user authentication
        database, the SSH point of entry, and network ingresses as we launch 
        server applications.  
  
- Storage

    - [Elastic File System (EFS)](https://aws.amazon.com/efs/pricing/) - $ 0.30/GB/mo
    
        I use EFS as main storage for home directories.  It's not cheap for large
        data ($30/mo for 100 GB, for comparison, Dropbox is $9/mo for 1 TB), but
        it's extremely convenient and reliable, a true file system (unlike Dropbox),
        and for configurations and environments is a great no-hassle way to get
        started.  It's pay for what you use, so if you keep this to just configurations
        it can be as low as $5/mo.  The other great thing about EFS is that it's
        really a managed NFS service, so all of your containers can connect to it
        simultaneously.
  
    - [Elastic Block Store (EBS) SSD](https://aws.amazon.com/ebs/pricing/) - $ 0.10/GB/mo
  
        SSD storage is required for the root file systems of all nodes.  I generally
        set these to fairly small sizes (10-20 GB), so total cost for my 3 permanent
        nodes is only ~$5/mo
  
    - [Elastic Block Store (EBS) Magnetic](https://aws.amazon.com/ebs/pricing/) - $ 0.045/GB/mo
  
        Magnetic block storage is considerably cheaper than EFS, but also is much
        less convenient as only a single container can mount an EBS volume at any
        given time.  I do use these in the intial tutorials for storing databases 
        (e.g. LDAP data) as only a single container needs access.  In future
        tutorials I plan to show how to launch an NFS server hosted in K8s (based
        on [Ganesha](https://github.com/nfs-ganesha/nfs-ganesha/wiki)), which
        will offer a low-cost alternative to EFS for larger data.  I'll also demonstrate
        use of [rook.io](https://rook.io/) for k8s-native distributed storage,
        backed by EBS.
  
    - [Simple Storage Service (S3)](https://aws.amazon.com/s3/pricing/) - $ 0.023/GB/mo

        This is going to be the bread-and-butter long term storage for my environment,
        as it's most appropriate for large datasets.  While traditional tools
        like Python are only just starting to work with object storage, Spark
        can use it quite effectively.

- Advanced Compute

    - Jupyter Hub
    
        My initial tutorials will deploy a single-instance juptyerhub that will
        be shared by any users of the system.  The instance can be sized
        according to administrator preference, and depending on workload
        can make use of spot priced instances which can often be 80% discounted
        compared to reserved instances.
  
    - Spark
  
        Spark is a great candidate for using spot instances - you can have several
        instances designated as spark administrators that are smaller and always on,
        then a much larger pool of large workers that are spot instances - they
        will go in and out of the cluster, but will work hard when they join and will
        be extremely cost effective.  The whole cluster only needs to be launched
        as needed, and can be destroyed when not in use.
  
    - GPU Nodes

        Like the other compute nodes, these only need to be provisioned when needed.
        A great advantage with this infrastructure is that all cuda/cudnn drivers
        are in the docker container, so setup time is on the order of minutes -
        compared to hours if doing everything from scratch.

All told, base cost of the system to leave running 24/7 is ~$50/month, which will
allow users to login, edit code, and launch simple jobs in the jupyterhub container.
Heavier computation will raise the cost, but in proportion to the size of the job,
and since these are generally able to use spot instances the prices can be quite reasonable.

As an example, a t2.xlarge instance that is normally $ 0.16/hr on the reserved
market can generally be had for approx $ 0.05/hr in spot - this has 4 cores
and 16 GB of ram, which is plenty for many investigations.  For larger work you
can go to a m5.12xlarge, a monster with 48 cores and 192 GB ram - normally $2.3/hr on 
reserved market, but only $ 0.75 on spot.

To give an estimate for personal side projects... let's say a user is able
to really buckle down on a problem every ~3 months and spend a week straight
on preliminary investigations, with a weekend of heavy duty compute to finish
training, hyperparameter searches, etc.  The rest of the time the administration
nodes are sufficient for general coding, writing paper abstracts/posters, etc.

In this scenario our cost for the year would be something like:

- 12 x $50 for administration  ($600)

- 4 x 7 x 24 x $ 0.05/hr for a t2.xlarge for exploratory work  ($33)

- 4 x 2 x 24 x $ 0.75/hr for a m5.12xlarge for heavy duty analysis ($144)

- 1 TB data in S3 for the year = 1000 GB * .023/GB/mo * 12 = ($276)

Total annual cost: $1053

Even including the purchase of that Chromebook to access these resources, and adding
cost to expand for spark and other things, it would still take 2-3 years to match
the price of a new MacBook, and you have the advantage of being able to scale to
2-100 nodes and access GPU and other resources whenever you need.

# Security

Pellentesque feugiat felis at purus ultrices, ut consequat arcu finibus. Sed gravida leo a lorem eleifend auctor. Ut ex nunc, pharetra non suscipit in, tincidunt a magna. Ut vitae urna vitae lectus faucibus ultricies. Quisque vel nisl eget nulla porta dapibus quis ac ipsum. Vestibulum rutrum, odio vitae accumsan blandit, lectus orci iaculis dolor, facilisis sagittis velit lectus non dui. Donec id leo pellentesque, pretium justo et, vestibulum metus. Nam elit eros, euismod id rhoncus aliquam, auctor sed nibh.

# Limitations

Pellentesque feugiat felis at purus ultrices, ut consequat arcu finibus. Sed gravida leo a lorem eleifend auctor. Ut ex nunc, pharetra non suscipit in, tincidunt a magna. Ut vitae urna vitae lectus faucibus ultricies. Quisque vel nisl eget nulla porta dapibus quis ac ipsum. Vestibulum rutrum, odio vitae accumsan blandit, lectus orci iaculis dolor, facilisis sagittis velit lectus non dui. Donec id leo pellentesque, pretium justo et, vestibulum metus. Nam elit eros, euismod id rhoncus aliquam, auctor sed nibh.
