import requests
import re
import praw
from datetime import date
import csv
import pandas as pd
import time
import sys

class Crawler(object):
    '''
        basic_url is the reddit site.
        headers is for requests.get method
        REX is to find submission ids.
    '''
    def __init__(self, subreddit="apple"):
        '''
            Initialize a Crawler object.
                subreddit is the topic you want to parse. default is r"apple"
            basic_url is the reddit site.
            headers is for requests.get method
            REX is to find submission ids.
            submission_ids save all the ids of submission you will parse.
            reddit is an object created using praw API. Please check it before you use.
        '''
        self.basic_url = "https://www.reddit.com"
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}
        self.REX = re.compile(r"<div class=\" thing id-t3_[\w]+")
        self.subreddit = subreddit
        self.submission_ids = []
        self.reddit = praw.Reddit(client_id="your_id", client_secret="your_secret", user_agent="subreddit_comments_crawler")

    def get_submission_ids(self, pages=2):
        '''
            Collect all ids of submissions..
            One page has 25 submissions.
            page url: https://www.reddit.com/r/subreddit/?count25&after=t3_id
                id(after) is the last submission from last page.
        '''
#         This is page url.
        url = self.basic_url + "/r/" + self.subreddit

        if pages <= 0:
            return []

        text = requests.get(url, headers=self.headers).text
        ids = self.REX.findall(text)
        ids = list(map(lambda x: x[-6:], ids))
        if pages == 1:
            self.submission_ids = ids
            return ids

        count = 0
        after = ids[-1]
        for i in range(1, pages):
            count += 25
            temp_url = self.basic_url + "/r/" + self.subreddit + "?count=" + str(count) + "&after=t3_" + ids[-1]
            text = requests.get(temp_url, headers=self.headers).text
            temp_list = self.REX.findall(text)
            temp_list = list(map(lambda x: x[-6:], temp_list))
            ids += temp_list
            if count % 100 == 0:
                time.sleep(60)
        self.submission_ids = ids
        return ids

    def get_comments(self, submission):
        '''
            Submission is an object created using praw API.
        '''
#         Remove all "more comments".
        submission.comments.replace_more(limit=None)
        comments = []
        for each in submission.comments.list():
            try:
                comments.append((each.id, each.link_id[3:], each.author.name, date.fromtimestamp(each.created_utc).isoformat(), each.score, each.body) )
            except AttributeError as e: # Some comments are deleted, we cannot access them.
#                 print(each.link_id, e)
                continue
        return comments

    def save_comments_submissions(self, pages):
        '''
            1. Save all the ids of submissions.
            2. For each submission, save information of this submission. (submission_id, #comments, score, subreddit, date, title, body_text)
            3. Save comments in this submission. (comment_id, submission_id, author, date, score, body_text)
            4. Separately, save them to two csv file.

            Note: You can link them with submission_id.
            Warning: According to the rule of Reddit API, the get action should not be too frequent. Safely, use the defalut time span in this crawler.
        '''

        print("Start to collect all submission ids...")
        self.get_submission_ids(pages)
        print("Start to collect comments...This may cost a long time depending on # of pages.")
        submission_url = self.basic_url + "/r/" + self.subreddit + "/comments/"
        comments = []
        submissions = []
        count = 0
        for idx in self.submission_ids:
            temp_url = submission_url + idx
            submission = self.reddit.submission(url=temp_url)
            submissions.append((submission.name[3:], submission.num_comments, submission.score, submission.subreddit_name_prefixed, date.fromtimestamp(submission.created_utc).isoformat(), submission.title, submission.selftext))
            temp_comments = self.get_comments(submission)
            comments += temp_comments
            count += 1
            print(str(count) + " submissions have got...")
            if count % 50 == 0:
                time.sleep(60)
        comments_fieldnames = ["comment_id", "submission_id", "author_name", "post_time", "comment_score", "text"]
        df_comments = pd.DataFrame(comments, columns=comments_fieldnames)
        df_comments.to_csv("comments.csv")
        submissions_fieldnames = ["submission_id", "num_of_comments", "submission_score", "submission_subreddit", "post_date", "submission_title", "text"]
        df_submission = pd.DataFrame(submissions, columns=submissions_fieldnames)
        df_submission.to_csv("submissions.csv")
        return df_comments


if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) != 2:
        print("Wrong number of args...")
        exit()

    subreddit, pages = args
    c = Crawler(subreddit)
    c.save_comments_submissions(int(pages))
