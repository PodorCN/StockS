from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import mysql.connector
import datetime
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from unidecode import unidecode
import time
import pandas as pd
import json
analyzer = SentimentIntensityAnalyzer()

# Insert your twitter API key here 
ckey=""
csecret=""
atoken=""
asecret=""

#connect to a mysql server 
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


class twitterScanner(StreamListener):
    def on_data(self,data):
        all_data = json.loads(data)
        current_time = datetime.datetime.now()
        author = str(all_data['user']['screen_name'])
        tweet = str(all_data["text"])
        vs = analyzer.polarity_scores(unidecode(tweet))
        sentiment = vs['compound']
        db = (current_time, author, tweet,sentiment)
        mycursor.execute(sqlFormula, db)
        mydb.commit()
    def on_error(self,status):
        print(status)

with SSHTunnelForwarder(
        (ssh_host, ssh_port),
        ssh_username=ssh_user,
        ssh_password=ssh_passwd,
        remote_bind_address=(sql_hostname, sql_port)) as tunnel:
    conn = mysql.connector.connect(host='127.0.0.1', user=sql_username,
            passwd=sql_password, db=sql_main_database,
            port=tunnel.local_bind_port)


    mycursor = conn.cursor()


    sql_command = """CREATE TABLE emp2 (
    staff_number INTEGER PRIMARY KEY,
    fname VARCHAR(20),
    lname VARCHAR(30),
    gender CHAR(1),
    joining DATE);"""
    


    mycursor.execute(sql_command)
    sql_command = """INSERT INTO emp VALUES (23, "Rishabh", "Bansal", "M", "2014-03-28");"""
    mycursor.execute(sql_command)

    sql_command = """INSERT INTO emp VALUES (1, "Bill", "Gates", "M", "1980-10-28");"""
    mycursor.execute(sql_command)

    conn.commit()

    print(mycursor.rowcount, "record inserted.")

    conn.close()




## Connecting to twitter and establishing a live stream 
while True:
    try:
        auth = OAuthHandler(ckey, csecret)
        auth.set_access_token(atoken, asecret)
        twitterStream = Stream(auth, listener())
        twitterStream.filter(track=["$"]) #this tracks any tweet with a $ symbol. Unlike Reddit, a large proportion of twitter users use $ before the stock tickers
    except Exception as e:
        print(str(e))