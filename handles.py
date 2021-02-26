import feedparser
import sqlite3

def cotsignal(argument):
    if str(argument)[:1] == "-":
        return "🔻"
    else:
        return "🔺"

def limitDecimals(number, decimals):
    return int(number * 10 ** decimals) / 10 ** decimals

def convert(raw):
    return raw / 10 ** 30

def first_new():
    a = feedparser.parse("https://portalnano.com.br/blog/feed")
    b = a.entries[0]
    c = b.link
    return c

def db_new():
    conn = sqlite3.connect('portalnano.db')
    conne = conn.cursor()
    conne.execute("SELECT * FROM LASTNEW")
    for i in conne.fetchall():
        return (i[1])

def last_new():
    a = feedparser.parse("https://portalnano.com.br/blog/feed")
    cont = 0
    listx = []
    while cont < 5:
        b = a.entries[cont]
        listx.append(b.link)