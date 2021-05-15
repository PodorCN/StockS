import praw
import datetime
import mysql.connector
from sshtunnel import SSHTunnelForwarder
from unidecode import unidecode
import time

# TEMP Analyzer
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
analyzer = SentimentIntensityAnalyzer()

# SQL Connection Setting
sql_hostname = '127.0.0.1'
sql_username = 'RedditIO'
sql_password = 'DataIO123.'
sql_main_database = 'redditStore'
sql_port = 3306
ssh_host = 'sql.podor.ca'
ssh_user = 'root'
ssh_passwd = '3-qJ{ov_LH324aww'
ssh_port = 22
sql_ip = '1.1.1.1.1'

# Reddit Connection Setting
reddit = praw.Reddit(
     client_id="lMuoVyKT4Ax7Fg",
     client_secret="oL1GwLR6v8zt9rcBdmU-qJaXjLA_fg",
     user_agent="PodorCN"
 )

with SSHTunnelForwarder(
        (ssh_host, ssh_port),
        ssh_username=ssh_user,
        ssh_password=ssh_passwd,
        remote_bind_address=(sql_hostname, sql_port)) as tunnel:
    conn = mysql.connector.connect(host='127.0.0.1', user=sql_username,
            passwd=sql_password, db=sql_main_database,
            port=tunnel.local_bind_port)

    mycursor = conn.cursor()

    mycursor.execute("CREATE DATABASE IF NOT EXISTS reddit_data")

    sqlTableInit = """CREATE TABLE IF NOT EXISTS reddit_data.reddit_data_sentiment
    (date_time DATETIME,
    subreddit VARCHAR(500),
    title VARCHAR(500),
    body VARCHAR(2000),
    sentiment DECIMAL(5,4));"""

    sqlFormula = "INSERT INTO reddit_data.reddit_data_sentiment (date_time, subreddit, title, body, sentiment) VALUES (%s, %s, %s, %s, %s, %s)"
    counter = 0

    while True:
        if counter > 100:
            break
        try:
            subreddit = reddit.subreddit("wallstreetbets+investing+stocks+pennystocks+weedstocks+StockMarket+Trading+Daytrading+algotrading")
            for comment in subreddit.stream.comments(skip_existing=True):
                print("\r%d" % counter,end="")
                current_time = datetime.datetime.now()
                subreddit = str(comment.subreddit)
                title = str(comment.link_title)
                body = str(comment.body)
                if len(body) < 2000:
                    body = body
                else:
                    body = "body is too large, skipped"
                # We do not consier the case when the body is too large
                vs = analyzer.polarity_scores(unidecode(body))
                sentiment = vs['compound']
                db = (current_time,subreddit,title,body,sentiment)
                mycursor.execute(sqlFormula, db)
                conn.commit()
                counter += 1
                if counter > 100:
                    break
        except Exception as e:
            print(str(e))
            time.sleep(10)

    conn.close()
