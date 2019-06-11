Title: Update - Integrating Pelican changes since initial deploy
Date: 2018-03-17 05:00
Category: 
Tags: python, website, github
Author: Eric Carlson
slug: pelican-jupyter-update
Series: pelican-website
Status: published
Summary: 
    A reader recently pointed out that I hadn't actually tested math display
    in Jupyter (Thanks Ben!).  Here are the steps I had to take to get
    that working... 

[TOC]

# Initial problem discovery

After [Ben's comment](https://disqus.com/home/discussion/datascidevops/configure_pelican_for_jupyter_notebooks_code_and_math_display/#comment-3799164961) 
I tried editing my original jupyter test notebook
with a few sample [formulas](http://jupyter-notebook.readthedocs.io/en/stable/examples/Notebook/Working%20With%20Markdown%20Cells.html)
and discovered that they didn't display properly - instead of displaying
nice summations, I saw raw code in the webpage:

```
$e^{i\pi} + 1 = 0$

$$e^x=\sum_{i=0}^\infty \frac{1}{i!}x^i$$
```

# Tracking down the issue

I expected that there may be a mathjax problem - it seems this kind of thing
can often stem from javascript resources being missing, or trying to be
loaded from alternate domains and getting blocked due to https lock downs, etc.
Looking into the dev console of Chrome, however, didn't yield anything obvious.

Some quick googling resulted in a recent post similar to this:
- https://github.com/getpelican/pelican-plugins/issues/933

It looks like the location of the mathjax library has changed, and this
broke my theme, pelican-bootstrap3.  It's been a few years since I set everything
up so it was time to update anyway, and this was good motivation.

# Resolution

In the end I wound up upgrading my theme (pelican-bootstrap3), integrating
a merge request that hasn't been approved yet, and adding a new plugin
that bootstrap3 now requires.  While I was at it I also added a plugin (Summary)
to give me more control over the text used for post summaries.

## Add latest bootstrap3 theme

Most of the pelican instructions have you point to a `pelican-theme` or 
`pelican-plugin` directory and go from there.  I don't love that configuration
as I like to have all dependency versions explicitly listed in version control,
and this introduces an external dependency with unrecorded versions.  I could
add the pelican-plugin/theme repos as git submodules (and may do that in the
future), but there are so many I don't want so 
for now I just copy in the handful of resources I need as I need them.

On my cloud dev environment I have an external code area where I keep all
code I clone from github or gitlab or other sources, and I just browsed to there
and updated my local repos of plugins and themes.  I then used rsync to copy over
any changes from github into my local repo:

```
$ rsync -av --delete ~/code/ext/github/getpelican/pelican-themes/pelican-bootstrap3/ <path_to_blog>/themes/pelican-bootstrap3/
```

Since I last installed bootstrap3 they've started requiring enabling of 
internationalization support - don't forget to add the i18 pelican plugin,
enable the plugin in your `pelicanconf.py` file, and set your jinja
environment as described in the docs:

```
JINJA_ENVIRONMENT = {'extensions': ['jinja2.ext.i18n']}
```

## Integrate merge request

In the course of researching the problem I found that the url for mathjax
has changed.  There is currently a 5-day-old [merge request](https://github.com/yamalcaraz/pelican-themes/commit/eb85b9f4de34bb345dfc19ba73ac998b2cf1306b)
to fix it, but it hasn't been accepted into the bootstrap3 theme yet.

The MR is a 1-liner, just changing the url for mathjax on line 146 of `pelican-bootstrap3/templates/includes/liquid_tags_nb_header.html` to:
```
https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.0/MathJax.js?config=TeX-AMS_HTML
```

I just made the change manually myself to the copy in my blog's repo

# Proof of working

{% notebook 180317-math-test.ipynb %}

## In case urls change in the future...

As of the writing of the article, the above section renders as follows in
Chrome v65:

![Jupyter Math]({static}/images/180317-jupyter-math/jupyter-math.png)
