from psaw import PushshiftAPI
import datetime as dt

api = PushshiftAPI()

start_epoch=int(dt.datetime(2021, 5, 15).timestamp())

listt= list(api.search_comments(after=start_epoch,
                            subreddit='wallstreetbets',
                            filter=['comments','author', 'title', 'subreddit'],
                            limit=100))

print(listt)