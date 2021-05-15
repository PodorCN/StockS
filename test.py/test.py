import time
import demoji

print(time.time())
demoji.download_codes()

tweet = """
... #startspreadingthenews yankees win great start by 🎅🏾 going 5strong innings with 5k’s🔥 🐂
... solo homerun 🌋🌋 with 2 solo homeruns and👹 3run homerun… 🤡 🚣🏼 👨🏽‍⚖️ with rbi’s … 🔥🔥
... 🇲🇽 and 🇳🇮 to close the game🔥🔥!!!….
... WHAT A GAME!!..
... """

Rdict = demoji.findall(tweet)

for key in Rdict:
    tweet = tweet.replace(key,Rdict[key])

print(tweet)

