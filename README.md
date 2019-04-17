# BotDetector
Final Degree project which consists in an application that allows you to distinguish between a normal user Twitter account and a Bot

## Pre-requisites

### Getting Twitter API keys
In order to access Twitter Streaming API, we need to get the API key, API secret, Access token and Access token secret from Twitter:

1. Create a twitter account if you do not already have one.
2. Go to https://apps.twitter.com/ and log.
3. Click on "Create New App".
4. Fill out the form, agree to the terms, and click "Create your Twitter application".
5. Click on "API keys" tab, and copy your "API key" and "API secret".
6. Click on "Create my access token", and copy your "Access token" and "Access token secret".

### Installing Jupyter with pip
You can install Jupyter using Anaconda but you may wish to install Jupyter using Python’s package manager, pip, as I have done.
If you have Python 3 installed:

    python3 -m pip install --upgrade pip
    python3 -m pip install jupyter

More information in: [Jupyter](https://jupyter.org/install.html)

### Installing Tweepy
You can install the latest version by using pip/easy_install to pull it from PyPI:

    pip install tweepy

Or you can also use Git to clone the repository from GitHub and install it manually:

    git clone https://github.com/tweepy/tweepy.git
    cd tweepy
    python setup.py install


### Installing Pandas
Pandas can be installed via pip from PyPI. [Pandas](https://pandas.pydata.org/pandas-docs/stable/install.html)

    pip install pandas

### Installing scikit-learn
If you already have a working installation of numpy and scipy, the easiest way to install scikit-learn is using pip

    pip install -U scikit-learn


## Author

* **Cristòfol Daudén Esmel** - [toful](https://github.com/toful)
