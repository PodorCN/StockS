from psaw import PushshiftAPI
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
dataTimeFocus = [int(datetime.datetime(2021, 5, 2).timestamp()),int(datetime.datetime(2021, 5, 3).timestamp()),
    int(datetime.datetime(2021, 5, 4).timestamp()),int(datetime.datetime(2021, 5, 5).timestamp()),
    int(datetime.datetime(2021, 5, 6).timestamp()),int(datetime.datetime(2021, 5, 7).timestamp()),
    int(datetime.datetime(2021, 5, 8).timestamp()),int(datetime.datetime(2021, 5, 9).timestamp())]

api = PushshiftAPI()

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

    sqlTableInit = """CREATE TABLE IF NOT EXISTS reddit_data.reddit_data_sentiment2
    (postTime DATETIME,
    subreddit VARCHAR(500),
    body VARCHAR(2000),
    sentiment DECIMAL(5,4));"""

    mycursor.execute(sqlTableInit)
    counter = 0

    sqlFormula = "INSERT INTO reddit_data.reddit_data_sentiment2 (postTime, subreddit, body, sentiment) VALUES (%s, %s, %s, %s)"
    
    demoji.download_codes()

    for day in dataTimeFocus:
        dayList= list(api.search_comments(before=day,subreddit='wallstreetbets',limit=20000))
        for comment in dayList:
            try:
                curPostTime = comment.created_utc
                counter += 1
                print("\r%d                                                                                         " % counter,end="")
                curPostTime = datetime.datetime.fromtimestamp(curPostTime)
                subreddit = str(comment.subreddit)
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
                db = (curPostTime,subreddit,body,sentiment)
                mycursor.execute(sqlFormula, db)
                conn.commit()
            except Exception as e:
                print("\r"+str(e))
                #time.sleep(10)

    conn.close()

