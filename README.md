# Analyse what Japanese people are posting on Yahoo! forum with BERTopic
The goal of this project is understanding types of parenting concerns in Japanese based on what people post on Yahoo! Chiebukuro forum. 
I first scraped forum parenting-related posts with a set of keywords using Selenium. After cleaning the scraped data, BERTopic was used to cluster the posts into categories. 

The full result is summarised [here]([url](https://note.com/ati_sum/n/n236c2669b6dd#4a63873f-5949-45e0-9d3c-2014159a7322)).

# Files 
There are five files created for this project. 

1. yahoo_scraping_default.py
   This file is for scraping posts on Yahoo! Chiebukuro focum based on a set of keywords, without setting any filtering.
   * I run this on PyCharm.

2. yahoo_scraping_sorting.py
   This file allows scraping posts on Yahoo! Chiebukuro focum based on a set of keywords, with filtering (e.g. when you want posts based on latest post dates etc)
    * I run this on PyCharm.

3. data cleaning_and_nplot.py
   This file serves two purposes; 1) It cleans text data by removing unwanted signs and Japanese particles (助詞) as well as converting post date format, and 2) It creates charts to visualize what top keywords and a network of associated words using nplot.
    * I run this on PyCharm.
  
4. stopwords-ja.txt
   This file contains stopwords in Japanese that should be ignored while BERTopic goes through the data in analysis. This is used in running the BERTopic code below.
  
5. BERTopic in Japanese_analysing parenting concerns.ipynb
   This file contains the code to run BERTopic for Japanese posts. Stopwords-ja.txt will be used in this code.   
    * I run this on Google Colaboratory

# Last updated
2023.08.29
