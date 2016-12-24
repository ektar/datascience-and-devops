Title: Setting up a Pelican website on github, part 1 
Date: 2016-12-01 05:00
Category: 
Tags: python, website, github
Author: Eric Carlson
slug: pelican-website-p1
Status: published
Summary: Overview of how to setup the Pelican static website generator

Part 1 of 3:

* [Part 2]({filename}161202_pelican_setup-p2.md)
* [Part 3]({filename}161203_pelican_setup-p3.md) 

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

[Part 2]({filename}161202_pelican_setup-p2.md)