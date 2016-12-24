Title: Setting up a Pelican website on github, part 2
Date: 2016-12-02 05:00
Category: 
Tags: python, website, github
Author: Eric Carlson
slug: pelican-website-p2
Status: published
Summary: Launching our Pelican website on Github 

Part 2 of 3:

* [Part 1]({filename}161201_pelican_setup-p1.md)
* [Part 3]({filename}161203_pelican_setup-p3.md) 


GitHub hosting is a quick and easy way to get content up, and is great when you're already familiar
with git and want to link to other content.  Basically, any content in the master branch of
a specially named repo in your account (`<username>.github.io`) will be served as your website.


To link with Pelican many people seem to create a new pelican branch, and the pelican Makefile
handles switching between branches for creating output.  I didn't find that very transparent so went
another route - I'm using git submodules to add the output directory as its own submodule, and I
have 2 repositories for content, one that is public (the html output named `<username>.github.io`),
and another that can be private with the Pelican code.

First, create a new repository with the name `<username>.github.io`, set to public.

![Bare Website]({filename}/images/161201_pelican_setup/github-setup.png)

Next, create a repository that will be for the Pelican generator code, I named mine `datascience-and-devops`.

Now link our local repo to the github repo:

	:::bash
	$ git init .
	$ cat .gitignore
	--- contents:
	__pycache__/
	---
	
	$ git add .gitignore
	$ git commit -m 'First commit'
	$ make clean
	$ git add .
	$ git commit -m 'First working site'
	$ git remote add origin https://github.com/ektar/datascience-and-devops
	$ git push
	
Add output

	$ rm -rf output/
	$ git submodule add https://github.com/ektar/ektar.github.io.git output	
	$ git commit -m 'Added output as submodule'
	$ git push
	
Then changed a few files to make everything work...

In Makefile, changed the `clean` and `github` command to the following:

	clean:
		[ ! -d $(OUTPUTDIR) ] || rm -rf $(OUTPUTDIR)/*

	github: publish
		cd $(OUTPUTDIR) && git add . && git commit -m 'adding changes' && git push

This will make it so that the clean command won't wipe out the git submodule, and the github
publish will work with our layout.

At this point the following should successfully publish our site:

	:::bash
	$ make clean
	$ make html
	$ make github

[Part 3]({filename}161203_pelican_setup-p3.md)