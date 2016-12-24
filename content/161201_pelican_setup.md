Title: Setting up a Pelican website on github 
Date: 2016-12-01 05:00
Category: 
Tags: python, website, github
Author: Eric Carlson
slug: pelican-website
Status: published
Summary: Overview of how to setup the Pelican static website generator and launch a website on GitHub 

I've run various personal websites since the AOL era - first based on Microsoft's Front Page, then
switching to hand-crafted HTML, which got tiresome.  I switched to PHP Gallery for managing my 
photography sites and Drupal for my home site, a combination that served its purpose but was also
overkill for my needs, and required more maintenance than I wanted to invest.  

The goal of latest website is to focus more on datascience topics, so I needed a low-maintenance
system for easily generating nice looking content with mixed equations, figures, code, and text.
I generally hate GUIs, so was definitely looking for something more text based.  I'm a long-time
reader of Jake VanderPlas' blog, [Pythonic Perambulations](https://jakevdp.github.io/), and in
inspecting his setup it looked perfect for my needs.  He's using [Pelican](http://docs.getpelican.com/en/stable/index.html)
static website generator for the main content, with plugins for Jupyter Notebooks to allow easy
code additions.  The system uses either MarkDown or ReStructured Text for content, and can easily
launch to many output platforms - GitHub, S3, personal hosting, etc.

Below I'll go through the steps needed to create this website, and a few tests demonstrating 
capabilities.

## Local environment

Prepare pelican directory

	:::bash
	$ mkdir ektar-pelican
	$ cd ektar-pelican

Create a conda environment to nicely encapsulate website dependencies (saved to `environment.yml`)

	:::yaml
	----
	# run: conda env create --file environment.yml
	name: ektar-pelican
	dependencies:
	- anaconda
	- beautifulsoup4
	- flake8
	- ipython
	- ipython[notebook]
	- Markdown
	- matplotlib
	- nbconvert
	- numpy
	- pandas
	- pelican
	- pip
	- python>=3.5
	---

Create anaconda environment

	:::bash
	$ conda env create --file environment.yml

Activate environment

	:::bash
	$ source activate ektar-pelican

Now use the Pelican tools to create a basic website template

	:::bash
	$ pelican-quickstart

Following the prompts...

	> Where do you want to create your new web site? [.]
	> What will be the title of this web site? Data Science DevOps
	> Who will be the author of this web site? Eric T. Carlson
	> What will be the default language of this web site? [en]
	> Do you want to specify a URL prefix? e.g., http://example.com   (Y/n) n
	> Do you want to enable article pagination? (Y/n) n
	> What is your time zone? [Europe/Paris] America/New_York
	> Do you want to generate a Fabfile/Makefile to automate generation and publishing? (Y/n) Y
	> Do you want an auto-reload & simpleHTTP script to assist with theme and site development? (Y/n) Y
	> Do you want to upload your website using FTP? (y/N) N
	> Do you want to upload your website using SSH? (y/N) N
	> Do you want to upload your website using Dropbox? (y/N) N
	> Do you want to upload your website using S3? (y/N) N
	> Do you want to upload your website using Rackspace Cloud Files? (y/N) N
	> Do you want to upload your website using GitHub Pages? (y/N) Y
	> Is this your personal page (username.github.io)? (y/N) Y
	Done. Your new project is available at /Users/ecarlson/code/etc/ektar-pelican

Now, test it out

	:::bash
	$ make html
	$ make serve

![Bare Website]({filename}/images/161201_pelican_setup/bare-website.png)

Basics are working, now to get it connected to GitHub...

## Github Setup

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

## Final Pelican Configuration

Now add pelican plugins and themes and activate as needed...

	:::bash
	$ cd ~/code/ext
	$ git clone --recursive https://github.com/getpelican/pelican-plugins

Also add theme to start, using Jake Vanderplaas' since he wrote the notebook plugin I'm using, should work together...

	:::bash
	$ git submodule add https://github.com/jakevdp/pelican-octopress-theme.git themes/octopress

Add liquid plugin to pelicon conf and add theme (`pelicanconf.py`):

	PLUGIN_PATHS = ['/Users/ecarlson/code/external/pelican-plugins', ]
	PLUGINS = ['liquid_tags.img', 'liquid_tags.video',
			   'liquid_tags.youtube', 'liquid_tags.vimeo',
			   'liquid_tags.include_code', 'liquid_tags.notebook']

	NOTEBOOK_DIR = 'notebooks'
	
	EXTRA_HEADER = open('_nb_header.html').read().decode('utf-8') if os.path.exists('_nb_header.html') else None
	
	THEME = 'themes/octopress'
	
I also set to default articles as draft mode:

	DEFAULT_METADATA = {
		'status': 'draft',
	}

With these changes we should now be able to create Jupyter notebooks and include them in our blog
posts (tests below).

Lastly, I like to modify my jupyter to auto-save python files when saving .ipynb - this makes it
easier in git to tell what changed from version to version, as often meaninglss changes (e.g.
re-running a notebook, which changes cell numbering) result in a commit log noise.

`~/.jupyter/jupyter_notebook_config.py`:

	:::python
	import os
	from subprocess import check_call
	
	def post_save(model, os_path, contents_manager):
		"""post-save hook for converting notebooks to .py scripts"""
		if model['type'] != 'notebook':
			return # only do this for notebooks
		d, fname = os.path.split(os_path)
		check_call(['ipython', 'nbconvert', '--to', 'script', fname], cwd=d)
	
	c = get_config()
	c.FileContentsManager.post_save_hook = post_save

## Markup Test

Python code:

    #!python
    print("The path-less shebang syntax *will* show line numbers.")
    print('Testing 1 2 3')
    
Bash code:
	
	#!bash
	for n in t1 t2 t3; do
	  echo $n
	done


Notebook test:

{% notebook 161201_pelican_setup/test_notebook.ipynb %}


## References

https://h-gens.github.io/getting-started-with-pelican-and-ipython-notebooks.html
https://pages.github.com/
https://github.com/getpelican/pelican-themes/tree/master/pelican-bootstrap3
https://rjweiss.github.io/articles/2014_03_31/testing-ipython-integration/
http://danielfrg.com/blog/2013/03/08/pelican-ipython-notebook-plugin/
http://docs.getpelican.com/en/3.1.1/getting_started.html