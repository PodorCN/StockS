import praw
import datetime
import mysql.connector
from sshtunnel import SSHTunnelForwarder
from unidecode import unidecode
import time
import demoji

# TEMP Analyzer
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
analyzer = SentimentIntensityAnalyzer()

# SQL Connection Setting
sql_hostname = '127.0.0.1'
sql_username = 'RedditIO'
sql_password = 'DataX123.'
sql_main_database = 'reddit'
sql_port = 3306
ssh_host = 'prd.podor.ca'
ssh_user = 'root'
ssh_passwd = '!Ez8,=7k%tyv,m,Z'
ssh_port = 22
sql_ip = '1.1.1.1.1'

# Reddit Connection Setting
reddit = praw.Reddit(
     client_id="lMuoVyKT4Ax7Fg",
     client_secret="oL1GwLR6v8zt9rcBdmU-qJaXjLA_fg",
     user_agent="PodorCN1"
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
    (postTime DATETIME,
    subreddit VARCHAR(500),
    title VARCHAR(500),
    body VARCHAR(2000),
    sentiment DECIMAL(5,4));"""

    mycursor.execute(sqlTableInit)

    sqlFormula = "INSERT INTO reddit_data.reddit_data_sentiment (postTime, subreddit, title, body, sentiment) VALUES (%s, %s, %s, %s, %s)"
    counter = 0
    counter2 =0


    
    mycursor.execute("ALTER DATABASE `%s` CHARACTER SET 'utf8' COLLATE 'utf8_unicode_ci'" % 'reddit_data')

    demoji.download_codes()

    while True:
        counter2 += 1
        counter = 0
        if counter2 > 100:
            break
        subreddit = reddit.subreddit("wallstreetbets+investing+stocks+pennystocks+weedstocks+StockMarket+Trading+Daytrading+algotrading")
        for comment in subreddit.stream.comments(skip_existing=True):
            try:
                curPostTime = comment.created_utc
                if curPostTime < (time.time() - 604800):
                    continue
                print("\r%d                                                                                         " % counter,end="")
                curPostTime = datetime.datetime.fromtimestamp(curPostTime)
                subreddit = str(comment.subreddit)
                title = str(comment.link_title)
                body = demoji.replace(comment.body)
                Rdict = demoji.findall(body)

                for key in Rdict:
                    body = body.replace(key,Rdict[key])
                
                if len(body) < 2000:
                    body = body
                else:
                    body = ' '
                # We do not consier the case when the body is too large
                vs = analyzer.polarity_scores(unidecode(body))
                sentiment = vs['compound']
                db = (curPostTime,subreddit,title,body,sentiment)
                mycursor.execute(sqlFormula, db)
                conn.commit()
                counter += 1
                if counter > 100:
                    break
            except Exception as e:
                print("\r"+str(e))
                #time.sleep(10)

    conn.close()

