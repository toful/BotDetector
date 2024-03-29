# BotDetector
Final Degree project which consists in an application that allows you to distinguish between a normal user Twitter account and a Bot

## Pre-requisites

### Getting Twitter API keys
In order to access Twitter's API, we need to get the API key, API secret, Access token and Access token secret from Twitter:

1. Create a twitter account if you do not already have one.
2. Go to https://apps.twitter.com/ and log.
3. Click on "Create New App".
4. Fill out the form, agree to the terms, and click "Create your Twitter application".
5. Click on "API keys" tab, and copy your "API key" and "API secret".
6. Click on "Create my access token", and copy your "Access token" and "Access token secret".

### Installing dependencies
Can install all packages with the command:

    pip3 install -r requirements.txt

Or install each one of the packages:

#### Installing Jupyter with pip
You can install Jupyter using Anaconda but you may wish to install Jupyter using Python’s package manager, pip, as I have done.
If you have Python 3 installed:

    python3 -m pip install --upgrade pip
    python3 -m pip install jupyter

More information in: [Jupyter](https://jupyter.org/install.html)

#### Installing Tweepy
You can install the latest version by using pip/easy_install to pull it from PyPI:

    pip3 install tweepy

Or you can also use Git to clone the repository from GitHub and install it manually:

    git clone https://github.com/tweepy/tweepy.git
    cd tweepy
    python setup.py install

More information in: [Tweepy](https://tweepy.readthedocs.io/en/v3.5.0/)

#### Installing Pandas
Pandas can be installed via pip from PyPI. [Pandas](https://pandas.pydata.org/pandas-docs/stable/install.html)

    pip3 install pandas

#### Installing scikit-learn
If you already have a working installation of numpy and scipy, the easiest way to install scikit-learn is using pip. [scikit-learn](https://scikit-learn.org/stable/install.html)

    pip3 install -U scikit-learn

#### Installing matplotlib
Matplotlib can be installed via pip from PyPI. [Matplotlib](https://matplotlib.org/3.1.0/users/installing.html) 

    python3 -m pip install -U matplotlib

#### Installing seaborn
Seaborn can be installed via pip from PyPI. [Seaborn](https://seaborn.pydata.org/installing.html) 

    pip3 install seaborn


## Usage
### Data Analysis and Model Generation
**Generate the models**
```jupyter notebook DataAnalysis.ipynb```

### Tweet Analyzer tool
**1. Capture tweets containing a certain Hashtag**
```python3 tweet_collector.py [Hashtag]```

**2. Process the tweets captured**  
```python3 tweet_processor.py [tweets_file]```

**3. Evaluate all users**
```python3 user_processor.py [users_file]```

**4. Generate the interacion graph**
```python3 graph_generator.py [users_file] [links_file]```

### User Analyzer tool
**1. Analyze Twitter User's probability of being a Bot**
```python3 user_analyzer.py [Hashtag]```


## Structure
```
/
├─db
│  ├─
├─src       
│  ├─DataAnalysis.ipynb     From an existing dataset, generates the machine learning models to analyse the twitter users
│  ├─tweet_collector.py   Capture all tweets containing a hashtag specifyed by parameter
│  ├─tweet_processor.py     Processes all tweets captured by the twitter streaming module
│  ├─user_analyzer.py       Calculates the probability of a user of being a bot
│  ├─user_processor.py      Calculates the probabilities of all users specifyed in the input file of being a bot
│  ├─graph_generator.py     Generates the interaction graph between all users processed 
│  ├─modules
│  │    ├─aux_functions.py  Auxiliar funcions to generate the models input from a user
│  ├─models         Folder that contains the machine learning algorithms
│  ├─results        Folder that containd all results
├─credentials.txt   File containing the Twitter API keys
├─requirements.txt
├─LICENSE

```

## Author

* **Cristòfol Daudén Esmel** - [toful](https://github.com/toful)
