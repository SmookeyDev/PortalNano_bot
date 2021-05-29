import feedparser
import sqlite3
import aiohttp

def cotsignal(argument):
    if str(argument)[:1] == "-":
        return "🔻"
    else:
        return "🔺"

def limitDecimals(number, decimals):
    return int(number * 10 ** decimals) / 10 ** decimals

def convert(raw):
    return raw / 10 ** 30

async def parse():
    p = feedparser.parse("https://portalnano.com.br/blog/feed")
    return p

def first_new():
    a = feedparser.parse("https://portalnano.com.br/blog/feed")
    b = a.entries[0]
    c = b.link
    return c

def db_new():
    conn = sqlite3.connect('portalnano.db')
    conne = conn.cursor()
    conne.execute("SELECT * FROM LASTNEW")
    l = conne.fetchone()
    if l: return (l[1])
    return l

def last_new():
    a = feedparser.parse("https://portalnano.com.br/blog/feed")
    cont = 0
    listx = []
    while cont < 5:
        b = a.entries[cont]
        listx.append(b.link)

async def representative_info():
    async with aiohttp.ClientSession() as session:
        async with session.get('https://mynano.ninja/api/accounts/principals') as response:
            r = await response.json()
    return r

async def network_stats():
    async with aiohttp.ClientSession() as session:
        async with session.get('https://nanoticker.info/json/stats.json') as response:
            r = await response.json()
    j = {
        "cps": limitDecimals(r["CPSMedian"], 2),
        "bps": limitDecimals(r["BPSMedian"], 2),
        "blockCount": r["blockCountMedian"],
        "cementedCount": r["cementedMedian"],
        "backlog": r["blockCountMedian"] - r["cementedMedian"],
        "secondsRemaining": (r["blockCountMedian"] - r["cementedMedian"]) / (r["CPSMedian"] - r["BPSMedian"]),
        "cpsMax": limitDecimals(r["CPSMax"], 2),
        "bpsMax": limitDecimals(r["BPSMax"], 2),
        "blockCountMax": r["blockCountMax"],
        "cementedCountMax": r["cementedMax"],
        "backlogMax": r["blockCountMax"] - r["cementedMax"],
        "secondsRemainingMax": (r["blockCountMax"] - r["cementedMax"]) / (r["CPSMax"] - r["BPSMax"]),
    }
    return j

async def nano_cot():
    async with aiohttp.ClientSession() as session:
        async with session.get('https://api.coinpaprika.com/v1/tickers/nano-nano?quotes=BRL,USD,BTC') as response:
            r = await response.json()
    return r