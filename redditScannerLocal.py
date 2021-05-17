from psaw import PushshiftAPI
import datetime
import mysql.connector
#from sshtunnel import SSHTunnelForwarder
from unidecode import unidecode
import time
import demoji

# TEMP Analyzer
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
analyzer = SentimentIntensityAnalyzer()

# SQL Connection Setting
sql_hostname = 'localhost'
sql_username = 'RedditIO'
sql_password = 'DataX123.'
sql_main_database = 'reddit'
sql_port = 3306

# Reddit Connection Setting
dataTimeFocus = [int(datetime.datetime(2021, 5, 2).timestamp()), int(datetime.datetime(2021, 5, 3).timestamp()),
                int(datetime.datetime(2021, 5, 4).timestamp()), int(datetime.datetime(2021, 5, 5).timestamp()),
                int(datetime.datetime(2021, 5, 6).timestamp()), int(datetime.datetime(2021, 5, 7).timestamp()),
                int(datetime.datetime(2021, 5, 8).timestamp()), int(datetime.datetime(2021, 5, 9).timestamp()),
                int(datetime.datetime(2021, 5, 10).timestamp()), int(datetime.datetime(2021, 5, 11).timestamp()),
                int(datetime.datetime(2021, 5, 12).timestamp()), int(datetime.datetime(2021, 5, 13).timestamp()),
                int(datetime.datetime(2021, 5, 14).timestamp()), int(datetime.datetime(2021, 5, 15).timestamp()),
                int(datetime.datetime(2021, 5, 16).timestamp())]

startTime = int(datetime.datetime(2021, 5, 16).timestamp())

api = PushshiftAPI()

conn = mysql.connector.connect(host='127.0.0.1', user=sql_username,
                               passwd=sql_password, db=sql_main_database)

mycursor = conn.cursor()

mycursor.execute("CREATE DATABASE IF NOT EXISTS reddit_data")

sqlTableInit = """CREATE TABLE IF NOT EXISTS reddit_data.reddit_data_sentiment
    (postTime DATETIME,
    subreddit VARCHAR(500),
    body VARCHAR(2000),
    sentiment DECIMAL(5,4));"""

mycursor.execute(sqlTableInit)
counter = 0

sqlFormula = "INSERT INTO reddit_data.reddit_data_sentiment (postTime, subreddit, body, sentiment) VALUES (%s, %s, %s, %s)"

demoji.download_codes()
today = startTime

for i in range(120):
    dayList = list(api.search_comments(before=today, subreddit='wallstreetbets', limit=4000))
    today = int((datetime.datetime(2021, 5, 16)-datetime.timedelta(hours=6)).timestamp())
    for comment in dayList:
        try:
            curPostTime = comment.created_utc
            counter += 1
            print("\r%d                                                                                         " % counter, end="")
            curPostTime = datetime.datetime.fromtimestamp(curPostTime)
            subreddit = str(comment.subreddit)
            # title = str(comment.title)
            body = demoji.replace(comment.body)
            Rdict = demoji.findall(body)

            for key in Rdict:
                body = body.replace(key, Rdict[key])
            if len(body) < 2000:
                body = body
            else:
                body = ' '
            # We do not consier the case when the body is too large
            vs = analyzer.polarity_scores(unidecode(body))
            sentiment = vs['compound']
            db = (curPostTime, subreddit, body, sentiment)
            mycursor.execute(sqlFormula, db)
            conn.commit()
        except Exception as e:
            print("\r"+str(e))
            # time.sleep(10)

conn.close()
