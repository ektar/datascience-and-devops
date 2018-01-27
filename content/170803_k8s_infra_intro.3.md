Title: Kubernetes-based Data Science Workbench: Intro - Considerations
Date: 2017-08-03 05:00
Category: Infrastructure
Tags: kubernetes, aws, docker, data science
Author: Eric Carlson
Series: k8s-based-ds-workbench
slug: k8s-based-ds-workbench-intro-considerations
Status: published

[TOC]

We've sketched out a rough architecture at this point, time to get an estimate
of expected cost, and think through how well we can expect it to meet our original
design goals.  Besides overall user experience, I find it's important to carefully
think through the limitations of any project - what a thing _can't_ do is important
as what it can.  (Avoid scope creep!)  Lastly, it's always important to include
non-functional design requirements like security, performance, etc, as these can
make or break the project.

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

Security of these kinds of systems are always foremost on my mind.  While it's
tempting to focus on just the data science aspects, it's no fun when your account
gets shut down because someone's gotten in and been routing spam mail through
your servers, mining bitcoin, or other uninvited activities.

My typical approach is to have a VPC with public and private subnets, described
[here](https://docs.aws.amazon.com/AmazonVPC/latest/UserGuide/VPC_Scenario2.html).
This used to be time consuming to put together, but with Amazon's 
[wizards](https://console.aws.amazon.com/vpc/home?region=us-east-1#wizardFullpagePublicAndPrivate:)
it's become quite easy.  Following their wizard will result in a private cloud
environment with 2 subnets - one that has direct public access where you would
launch any internet-facing servers, and another that accesses websites through
a proxy of some sort (e.g. a Network Address Translation (NAT) unit, or other),
and that has no direct connect for outside users to access.  

This type of setup is very nice from a security perspective as you dramatically
reduce your "attack surface area" - the number of computers, ports, and services
that are directly exposed to attack.  For my purposes I generally just launch
a single computer, known as a [Bastion Host](https://aws.amazon.com/blogs/security/controlling-network-access-to-ec2-instances-using-a-bastion-server/),
that only exposes a single port for tunneling, and that I use to connect to all
other internal hosts.  I'll write further posts on how I use ssh tunneling to
do this, but it can be surprisingly easy to configure and work with, and it allows
you to launch services like Jupyter, Spark, and other web applications inside
your private cloud with little to fear as they're not directly connected to
the internet, and as all of your activity is encrypted via your SSH tunnel.

Security is always an engineering challenge, in which you try to find the optimum
point that reduces risks of relevant attack vectors to an acceptible level, is
feasible to implement and maintain, and feasible for end users to use.  For this
project I decided that this VPC private-public configuration didn't meet the requirements,
primarily due to ease of implementation for data scientists, and also due to
cost with the default configurations.  For example, the NAT device that is required
for the computers in the private network to get outside connectivity (e.g. to download
debian package) costs $ 0.05/hr, or $ 36/mo!  I generally reduce costs by
configuring my bastion node to also serve as a NAT device, but that gets into
fairly low level linux configuration that is out of the scope of this blog.

The security approach I take here is to leverage Kubernetes itself, along with
Amazon security groups, to limit access to relevant nodes and ports.  Each of
the kubernetes nodes has both a public and private interface, which eliminates
the need for the NAT device and dramatically reduces the overhead cost.  The
default configuration will only expose the SSH port of the computers themselves,
the API port for the master (protected by K8s authentication and https), and
an SSH port for a container running inside the K8s cluster itself that will
serve as our Bastion entry point.  We will still be able to launch Jupyter,
Spark, and other services on our cluster, and because they are not exposed
with ingresses or with security groups they will be inaccessible by unauthorized
users.

# Limitations

Like any system, ours will not be all things to all people, and that's _ok_!
As currently designed, this is intended to really be a platform for a datascientist
and several of his/her collaborators.  As such, I'm really focusing on making
a generic platform that can be expanded with the latest tools, at the expense
of developing a great user interface for new users.  I think this has the
benefit of exposing the internals and providing a good learning tool, but
it will certainly have some rough edges.

In particular, expected rough edges are:

- No central user interface - the administrator will need to use commandline
  tools to create new types of instances, set the numbers of instances, launch 
  new applications, etc.  I've tried to make this as user friendly as possible,
  but it's still a command line interface (CLI).

- Some linux experience is helpful - the project will be run from a linux
  Bash command line, and SSH (Secure Shell) is used to access the services.  The
  basics are easy to pick up and extremely beneficial for any data scientist,
  so I hope this doesn't drive anyone away, but it is an aspect of the environment.

- Limited auto scaling/automation - in a larger system with dozens/hundreds of
  VMs it would make sense to have all kinds of automation, e.g. monitoring the
  CPU usage of machines and creating new ones when capacity is being reached,
  or eliminating resources when there is downtime.  In a system with 3-5 computers,
  however, this would be overkill, and due to the budget constraints would likely
  be unwanted - e.g. I want to know when my friends are doing something that will
  result in a $1k credit card charge!

Despite these rough edges, I've been using this platform for the last several
months and already found it extremely enjoyable, and I hope you do, too!

On to the setup!