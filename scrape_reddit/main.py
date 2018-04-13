

reddit = Crawler()
ids = reddit.get_submission_ids(100)
comments = reddit.save_comments_submissions()
