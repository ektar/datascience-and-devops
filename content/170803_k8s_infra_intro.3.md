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

Pellentesque feugiat felis at purus ultrices, ut consequat arcu finibus. Sed gravida leo a lorem eleifend auctor. Ut ex nunc, pharetra non suscipit in, tincidunt a magna. Ut vitae urna vitae lectus faucibus ultricies. Quisque vel nisl eget nulla porta dapibus quis ac ipsum. Vestibulum rutrum, odio vitae accumsan blandit, lectus orci iaculis dolor, facilisis sagittis velit lectus non dui. Donec id leo pellentesque, pretium justo et, vestibulum metus. Nam elit eros, euismod id rhoncus aliquam, auctor sed nibh.

# Limitations

Pellentesque feugiat felis at purus ultrices, ut consequat arcu finibus. Sed gravida leo a lorem eleifend auctor. Ut ex nunc, pharetra non suscipit in, tincidunt a magna. Ut vitae urna vitae lectus faucibus ultricies. Quisque vel nisl eget nulla porta dapibus quis ac ipsum. Vestibulum rutrum, odio vitae accumsan blandit, lectus orci iaculis dolor, facilisis sagittis velit lectus non dui. Donec id leo pellentesque, pretium justo et, vestibulum metus. Nam elit eros, euismod id rhoncus aliquam, auctor sed nibh.
