import time
import demoji

print(time.time())
demoji.download_codes()

tweet = """
... #startspreadingthenews yankees win great start by ๐๐พ going 5strong innings with 5kโs๐ฅ ๐
... solo homerun ๐๐ with 2 solo homeruns and๐น 3run homerunโฆ ๐คก ๐ฃ๐ผ ๐จ๐ฝโโ๏ธ with rbiโs โฆ ๐ฅ๐ฅ
... ๐ฒ๐ฝ and ๐ณ๐ฎ to close the game๐ฅ๐ฅ!!!โฆ.
... WHAT A GAME!!..
... """

Rdict = demoji.findall(tweet)

for key in Rdict:
    tweet = tweet.replace(key,Rdict[key])

print(tweet)

