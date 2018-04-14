# Provide two solutions to Reddit data

## 1. Download from public data set. THANKS pushshift.io. You are a life saver!

DATA SOURCE: https://files.pushshift.io/reddit/comments/

* **PROS:** It is really **big big big** data set, including comments data from 2015.12 to nearly the present. They are separated by month.

* **CONS:** It is really **big big big** data set. Closer to the present, bigger the dataset. For example,  comments of 2018.01 is about 8 Gb.(8Gb is a .bz2 compressed file, actually times it with 6 :)

* **USAGE:** 

   1. Environment:  Python3, requests, bs4

   2. Start:  

     ```bash
      cd public_data_set
      python download.py 2005-12 2018-02
     ```

     The arguments are starting month and ending month.

     Up to the first commitment, there are dataset from 2015-12 to 2018-02. Therefore, date before or after the span will cause error. Please edit the function accordingly. 

     After the python script, there comes a *download_links.txt*, which contains all the links you need, from start to end.

   3. Download:

      ```bash
      wget -c -i download_links.txt
      ```

   4. Extract:

      Since most of the data files are .bz2, try

      ```bash
      bzip2 -d *.bz2  # this will delete the original file
      bzip2 -dk *.bz2 # this will keep the original file
      ```

      *Note:* Due to the size, please remember to use tmux.

* **NOTE:** 
  * The file could be big...Please make sure of your disk space. Anyway, recommend a server.
  * It will cost a long long time to download depending on your network. It may be a issue if it shutdown or sleep during the time. The **-c** parameter can help but I didn't try. If you download them on a server, recommend using **tmux**.
  * Anything?


## 2. Download using my crawler.

DATA SOURCE: https://www.reddit.com/r/subreddit

 * **PROS:** You can download whatever you want according to subreddit.

 * **CONS:**

    * The dataset is not big enough. The crawler parse the pages given by Reddit. Specifically, 25 pages, 25 submissions one page, at most.
    * This is an experimental version so there is no IP pool, distributed database, multi-thread function...In a word, it is not so fast...but it is enough if your need is not that big.
    * According to the rule of reddit API, there are limitations when accessing the website. Please check it before you use this.

* **USAGE:**

  1. Environment: 

     1. Python3, requests, praw, pandas
     2. Please fill out the Reddit APP id and secret first.
        1. [Create a Reddit developed application](https://www.reddit.com/prefs/apps/) 
        2. Fill out the constructor with your own id and secret.
        3. Save and enjoy it.

  2. Start:

     ```bash
     cd scrape_reddit
     python reddit_crawler.py apple 2
     ```

     The arguments are subreddit and pages.

  3. Wait wait wait...if it works fine, there will be some notes saying the process.

  4. Success!

     ```bash
     cat comments.csv
     cat submissions.csv
     ```

* **NOTE:**

  * If you want to parse 25 pages of a subreddit, it will probably cost half an hour. Most of time wasted obeying the rule of API. To be specific, I sleep the scrip 60 seconds every page.
  * If you are not sure about the API rules, please do not change the default setting.
  *  Anything?



