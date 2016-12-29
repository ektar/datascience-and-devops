Title: Deploy Kubernetes for container orchestration
Date: 2016-12-13 05:00
Category: infrastructure
Tags: aws, kubernetes, docker
Author: Eric Carlson
slug: aws-compute-environment-p4
Series: aws-compute-infrastructure
Status: published

[TOC]

Installing a container orchestration layer will allow us to quickly deploy anything in the huge
ecosystem of available docker services.  This can include database servers like Postgres or MariaDB,
message brokers like RabbitMq, medical informatics servers like HAPI FHIR, or our own services.  There 
are several options, including Kubernetes, Docker Swarm, Mesos, Rancher, etc., and even more traditional
PaaS offerings like Cloud Foundry to consider. 

In this post I'll focus on [Kubernetes](http://www.infoworld.com/article/3118345/cloud-computing/why-kubernetes-is-winning-the-container-war.html), 
for the following reasons:
 
  * Developed by Google (codename `Borg`), a company I trust for engineering, to manage "hundreds 
    of thousands of jobs, from many thousands of different applications, 
    across a number of clusters each with up to tens of thousands of machines"
  * Easy to deploy to environments I care about - AWS, local computer, on-prem cluster, etc
  * Managed versions available, e.g. Google Container service
  * Vibrant open source community
  * Adoption by other important projects, e.g. Spring Cloud Data Flow
  
This post will deploy Kubernetes to our private network, and we'll be able to use our ssh configuration
to easily tunnel in and access.  In this system I'm focused on creating a cluster for my internal
use, but Kubernetes can of course be used for full system deployment of internet-facing applications.
  
# Configure local deployment environment

We need to setup our local environment for creating a kubernetes cluster and deploying
applications.  Here, I'm using [KOPS](https://github.com/kubernetes/kops), a system for
"Production Grade K8s Installation, Upgrades, and Management".
  
First we'll install the kops and aws command line tools on our system (here, mac)

	$ brew update && brew install --HEAD kops
	$ brew install kubernetes-cli
	$ brew update && brew install awscli
	$ brew install bison
	$ brew install oniguruma
	$ brew install jq
	
# Create the necessary AWS infrastructure

Make sure AWS is configured with our credentials

	$ aws configure
	AWS Access Key ID: xxx
	AWS Secret Access Key: xxx
	Default region name [None]: us-east-1
	Default output format [None]:
	
Create a bucket where kops will store our cluster configuration	
	
	$ aws s3api create-bucket --bucket etccluster-kubnet-state-store --region us-east-1

Set environment variables for the tools to use

	$ export NAME=kubenet.datasciencedevops.com
	$ export KOPS_STATE_STORE=s3://etccluster-kubnet-state-store

Create DNS routes (needed by kops)

	$ ID=$(uuidgen) && aws route53 create-hosted-zone --name ${NAME} --caller-reference $ID
	$ aws route53 list-hosted-zones | jq '.HostedZones[] | select(.Name=="kubenet.datasciencedevops.com.") | .Id'
	"/hostedzone/Z3B4FBNOV4X88L"

	$ aws route53 get-hosted-zone --id "/hostedzone/Z3B4FBNOV4X88L" | jq .DelegationSet.NameServers
	[
	  "ns-1982.awsdns-55.co.uk",
	  "ns-1501.awsdns-59.org",
	  "ns-117.awsdns-14.com",
	  "ns-949.awsdns-54.net"
	]

# Deploy Kubernetes

Now we can actually define and create the cluster

Choose an availability zone

	$ aws ec2 describe-availability-zones --region us-east-1

All of my other services are in 1a, so I'll use that.
	
Next we create a cluster using the following options:

  * zones=us-east-1a - The zone to create in
  * node-size=t2.medium - The size of nodes
  * master-size=t2.medium - The size of masters
  * ssh-public-key=<ssh-key>.pub - Our ssh key
  * vpc=vpc-76fc0511 - The virtual private cloud created previously
  * network-cidr=10.0.0.0/16 - Network mask to use, set by our VPC
  * associate-public-ip=false - We want everything going through our bastion node, no public ip 
  * name=${NAME} - The name of our cluster, from environment
	
Run the command:
	
	$ kops create cluster \
  	    --zones=us-east-1a \
	    --node-size=t2.medium \
	    --master-size=t2.medium \
	    --ssh-public-key=/Users/ecarlson/.ssh/acs-cdsint-admin.key.pub \
	    --vpc=vpc-76fc0511 \
	    --network-cidr=10.0.0.0/16 \
	    --associate-public-ip=false \
	    --name=${NAME}

At this point it should be locally configured, and the configuration stored to S3

	$ kops get cluster
	NAME			CLOUD	ZONES
	kubenet.datasciencedevops.com	aws	us-east-1a

We can edit the configuration, but I don't need that so I'll just deploy

	$ kops update cluster ${NAME} --yes
	...
	I1228 12:17:44.984315   28008 update_cluster.go:150] Exporting kubecfg for cluster
	Wrote config for etccluster.kubnet to "/Users/ecarlson/.kube/config"
	
	Cluster is starting.  It should be ready in a few minutes.
	
	Suggestions:
	 * list nodes: kubectl get nodes --show-labels
	 * ssh to the master: ssh -i ~/.ssh/id_rsa admin@api.etccluster.kubnet
	 * read about installing addons: https://github.com/kubernetes/kops/blob/master/docs/addons.md

At this point the master and worker nodes are deployed on AWS, but it's likely that they aren't 
actually starting Kubernetes as they may not have internet access without an assigned IP.  I have
an existing NAT deployed for my VPC and was able to just edit the routes of the new kubernetes
subnet to send 0.0.0.0 to that NAT, and edit the security group of the NAT gateway to allow.  If
you don't already have such a NAT you can create one for this subnet.  

# Connect to and test the cluster

Kubernetes is now deployed but we can't access it as it has no public IP.  We'll be adding the
master node to our ssh config file and creating tunnels to access internal services.  After
we create the tunnels the api service will be accessible on our localhost, but the names need
to resolve so the kubectl cli client can find the REST endpoint.  I just modified my host file
to allow that:

	127.0.1.1      api.kubenet.datasciencedevops.com

Next, edit .ssh/config to go through the bastion to our kubernetes master:

	Host bastion-panda
	  ForwardAgent yes
	  Hostname xxx
	  IdentityFile ~/.ssh/xxx
	  User xxx

	Host panda-*
	  ForwardAgent yes
	  ProxyCommand ssh -q bastion-panda nc -q0 %h 22
  	
	Host panda-kube
	  Hostname 10.0.47.124
	  IdentityFile ~/.ssh/xxx
	  User admin

Now can login to our kube to test, port forward from local 8080 to remote 8080

	$ ssh -L 8080:localhost:8080 panda-kube

That creates a ssh session on the master.  Run `curl https://www.google.com` to test internet
connectivity to verify the master and workers can get out.  If not then you may notice that there
are hung processes (e.g. `ps -ax` or `top`) waiting to download the containers they need to run
kubernetes.  You'll need to fix internet for them to finish setting up the cluster.

Once that's complete, you should be able to run the following commands on our local environment
to test the system.

First, update the local configuration to look to our localhost for the ssh tunnel

	$ kubectl config set-cluster kubenet.datasciencedevops.com --server=http://localhost:8080

Now try to connect to the cluster - if this succeeds then we're in!

	$ kubectl get nodes --show-labels
	NAME                          STATUS         AGE       LABELS
	ip-10-0-35-137.ec2.internal   Ready          15m       beta.kubernetes.io/arch=amd64,beta.kubernetes.io/instance-type=t2.medium,beta.kubernetes.io/os=linux,failure-domain.beta.kubernetes.io/region=us-east-1,failure-domain.beta.kubernetes.io/zone=us-east-1a,kubernetes.io/hostname=ip-10-0-35-137.ec2.internal
	ip-10-0-41-90.ec2.internal    Ready          15m       beta.kubernetes.io/arch=amd64,beta.kubernetes.io/instance-type=t2.medium,beta.kubernetes.io/os=linux,failure-domain.beta.kubernetes.io/region=us-east-1,failure-domain.beta.kubernetes.io/zone=us-east-1a,kubernetes.io/hostname=ip-10-0-41-90.ec2.internal
	ip-10-0-47-124.ec2.internal   Ready,master   17m       beta.kubernetes.io/arch=amd64,beta.kubernetes.io/instance-type=t2.medium,beta.kubernetes.io/os=linux,failure-domain.beta.kubernetes.io/region=us-east-1,failure-domain.beta.kubernetes.io/zone=us-east-1a,kubernetes.io/hostname=ip-10-0-47-124.ec2.internal,kubernetes.io/role=master

Great, now let's install the dashboard for visualization

	$ kubectl create -f https://raw.githubusercontent.com/kubernetes/kops/master/addons/kubernetes-dashboard/v1.4.0.yaml

If that worked then we should be able to browse to localhost:8080/ui to view

![Kubernetes]({filename}/images/161213_setup_kubernetes/step-01.png)

Success!

# Deploy an application to our cluster

To test the system, let's deploy a simple web server, nginx:

	$ kubectl run my-nginx --image=nginx --replicas=2 --port=80
	$ kubectl get pods
	NAME                       READY     STATUS    RESTARTS   AGE
	my-nginx-379829228-2qln8   1/1       Running   0          1h
	my-nginx-379829228-fzt2u   1/1       Running   0          1h
	
	$ kubectl get deployments
	NAME       DESIRED   CURRENT   UP-TO-DATE   AVAILABLE   AGE
	my-nginx   2         2         2            2           1h

![Kubernetes]({filename}/images/161213_setup_kubernetes/step-02.png)

From those commands we see that we've deployed 2 nginx replicas, essentially 2 copies of the
same microservice running our web server.  We'll create a simple load balancer on top of them - 
this will make the servers accessible from outside, and will recover if either of them fail for
any reason (e.g. if the underlying VM is destroyed).  

	$ kubectl expose deployment my-nginx --port=80 --type=LoadBalancer
	
	$ kubectl get services -o wide
	
	NAME         CLUSTER-IP      EXTERNAL-IP   PORT(S)        AGE       SELECTOR
	kubernetes   100.64.0.1      <none>        443/TCP        2h        <none>
	my-nginx     100.71.27.183   <pending>     80:30836/TCP   5m        run=my-nginx

![Kubernetes]({filename}/images/161213_setup_kubernetes/step-03.png)

Now we see that nginx has a cluster ip of 100.71.27.183 and port 80, with no external ip.  That's
ok as we're using our ssh magic to tunnel through, no external ip necessary.

To connect, let's stop our previous ssh session and create a new one with this `-D 8099` option
added.  This will create a socks proxy

	$ ssh -L 8080:localhost:8080 -D 8099 panda-kube

I like to keep Firefox around for a proxy web client, you can configure it by going to the 
network panel of the advanced settings and pointing it at localhost:8099 like so:

![Kubernetes]({filename}/images/161213_setup_kubernetes/firefox-proxy.png)

Now in firefox we should be able to browse to the IP we saw before, 100.71.27.183:

![Kubernetes]({filename}/images/161213_setup_kubernetes/step-04.png)

It worked!  Let's clean up now...

	$ kubectl delete deployment,service my-nginx

	deployment "my-nginx" deleted
	service "my-nginx" deleted

![Kubernetes]({filename}/images/161213_setup_kubernetes/step-05.png)

# Conclusion

At this point we have a working Kubernetes cluster running in our private VPC on AWS.  Next we
can add nodes (e.g. using spot instances for very cheap processing), add services (postgres,
spark, etc), and more.

# Kubernetes overviews

Here are a few good overviews of how to use kubernetes and some of the underlying concepts. 

* https://research.google.com/pubs/pub43438.html
* http://thenewstack.io/kubernetes-an-overview/
* https://www.digitalocean.com/community/tutorials/an-introduction-to-kubernetes
* https://deis.com/blog/2016/kubernetes-overview-pt-1/
* https://deis.com/blog/2016/kubernetes-overview-pt-2/

# References

* https://github.com/kubernetes/kops/blob/master/docs/aws.md
* https://www.nivenly.com/k8s-aws-private-networking/
* https://stevesloka.com/2016/03/24/access-kubernetes-master-behind-bastion-box/
* http://kubernetes.io/docs/user-guide/accessing-the-cluster/
