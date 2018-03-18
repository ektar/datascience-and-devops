#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals
import os
import sys

AUTHOR = 'Eric T. Carlson'
SITENAME = 'Data Science and DevOps'
SITEURL = ''
EMAIL_ADDR = 'site_datascidevops@carlsonhome.net'

PATH = 'content'
STATIC_PATHS = ['downloads', 'images', 'notebooks']
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
             ('Github', 'https://github.com/ektar'),
             ('Github', 'https://github.com/erictcgs')
         )

MARKDOWN = {
    'extension_configs': {
        'markdown.extensions.codehilite': {'css_class': 'highlight'},
        'markdown.extensions.toc': {'anchorlink': True},
        'markdown.extensions.admonition': {},
        'markdown.extensions.extra': {},
        'markdown.extensions.meta': {},
    },
    'output_format': 'html5',
}

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

PLUGIN_PATHS = ['plugins', ]
PLUGINS = ['liquid_tags.img', 'liquid_tags.video',
           'liquid_tags.youtube', 'liquid_tags.vimeo',
           'liquid_tags.include_code', 'liquid_tags.notebook',
           'i18n_subsites', 'summary']

NOTEBOOK_DIR = 'notebooks'
CODE_DIR = 'notebooks'

EXTRA_HEADER = open('_nb_header.html').read() if os.path.exists('_nb_header.html') else None

DEFAULT_METADATA = {
    'status': 'draft'
}

DISQUS_SITENAME = 'datascidevops'
DISQUS_DISPLAY_COUNTS = True

THEME = 'themes/pelican-bootstrap3'

sys.path.append(os.curdir)
from themeconf import *

JINJA_ENVIRONMENT = {'extensions': ['jinja2.ext.i18n']}

PLUGINS.extend(['code_include', 'extract_toc', 'series',
                'better_codeblock_line_numbering', 'tag_cloud', 'simple_footnotes'])

TYPOGRIFY = True
