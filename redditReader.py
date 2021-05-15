import praw
import datetime

reddit = praw.Reddit(
     client_id="lMuoVyKT4Ax7Fg",
     client_secret="oL1GwLR6v8zt9rcBdmU-qJaXjLA_fg",
     user_agent="PodorCN"
 )

subreddit = reddit.subreddit("wallstreetbets+investing+stocks+pennystocks+weedstocks+StockMarket+Trading+Daytrading+algotrading")
for comment in subreddit.stream.comments(skip_existing=True):
    current_time = datetime.datetime.now()
    subreddit = str(comment.subreddit)
    author = str(comment.author)
    title = str(comment.link_title)
    body = str(comment.body)
    print("Body: "+body)
    print("subreddit: "+subreddit)
    print("author: "+author)
    print("title: "+title)
    break

