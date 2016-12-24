#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals
import os

AUTHOR = 'Eric T. Carlson'
SITENAME = 'Data Science and DevOps'
SITEURL = ''

PATH = 'content'
STATIC_PATHS = ['downloads', 'images']
ARTICLE_SAVE_AS = '{date:%Y}/{slug}.html'
ARTICLE_URL = '{date:%Y}/{slug}.html'

TIMEZONE = 'America/New_York'

DEFAULT_LANG = 'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (
         ('While My MCMC Gently Samples', 'http://twiecki.github.io/'),
         ('Pythonic Perambulations', 'https://jakevdp.github.io/'),
         ('Normal Deviate', 'https://normaldeviate.wordpress.com/'),
         ('Statistical Modeling, Causal Inference, and Social Science', 'http://andrewgelman.com/'),
         ('Edwin Chan', 'http://blog.echen.me/'),
         ('Hunch', 'http://hunch.net/'),
         ('Walking Randomly', 'http://www.walkingrandomly.com/'),
         ('Kaggle Blog', 'http://blog.kaggle.com/'),
         ('Wes McKinney', 'http://wesmckinney.com/'),
         ('Google Datascience', 'http://www.unofficialgoogledatascience.com/'),
)

# Social widget
SOCIAL = (
             ('LinkedIn', 'https://www.linkedin.com/in/erictcarlson'),
         )

DEFAULT_PAGINATION = False

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

PLUGIN_PATHS = ['/Users/ecarlson/code/external/pelican-plugins', ]
PLUGINS = ['liquid_tags.img', 'liquid_tags.video',
           'liquid_tags.youtube', 'liquid_tags.vimeo',
           'liquid_tags.include_code', 'liquid_tags.notebook']

NOTEBOOK_DIR = 'notebooks'

EXTRA_HEADER = open('_nb_header.html').read() if os.path.exists('_nb_header.html') else None

THEME = 'themes/octopress'

DEFAULT_METADATA = {
    'status': 'draft',
}