import amanobot
import time
import amanobot
import amanobot.aio
import sqlite3
import feedparser
import requests
import asyncio

from os                import environ
from decouple          import config
from amanobot.aio.loop import MessageLoop
from datetime          import datetime
from decimal           import Decimal
from handles           import *

API = "https://vault.nanocrawler.cc/api/node-api"
REPRESENTATIVE = "nano_1j78msn5omp8jrjge8txwxm4x3smusa1cojg7nuk8fdzoux41fqeeogg5aa1" # endereço do node representativo da Nano Brasil
GROUP_TYPE = ["group", "supergroup"]
ADMIN_TYPE = ["administrator", "owner", "creator"]

TOKEN = config('TOKEN') 
SUDOS = [ int(id) for id in config('SUDOS').split() ]
MAINTAINERS = [ int(id) for id in config('MAINTAINERS').split() ]
texts = json.load(open('texts.json'))
lang = "pt"
##DEFS
  
async def handle(msg):
    conn = sqlite3.connect('portalnano.db')
    conne = conn.cursor()
    conn.execute('''CREATE TABLE IF NOT EXISTS REGISTERED
         (ID INTEGER PRIMARY KEY AUTOINCREMENT     NOT NULL,
         USERID           TEXT    NOT NULL);''')
    conn.execute('''CREATE TABLE IF NOT EXISTS LASTNEW
         (ID INTEGER PRIMARY KEY AUTOINCREMENT     NOT NULL,
         LINK           TEXT    NOT NULL);''')
    conn.execute('''CREATE TABLE IF NOT EXISTS BLOCKS
         (ID INTEGER PRIMARY KEY AUTOINCREMENT     NOT NULL,
         USERID           TEXT    NOT NULL);''')

    conn.execute('''CREATE TABLE IF NOT EXISTS FAUCET
         (ID INTEGER PRIMARY KEY AUTOINCREMENT     NOT NULL,
         USERID           TEXT    NOT NULL,
         WALLET           TEXT    NOT NULL,
         BLOCK           TEXT    NOT NULL);''')

    conn.execute('''CREATE TABLE IF NOT EXISTS SETTINGS
         (ID INTEGER PRIMARY KEY AUTOINCREMENT     NOT NULL,
         FPRICE           TEXT    NOT NULL,
         FSET           TEXT    NOT NULL);''')

    content_type, chat_type, chat_id = amanobot.glance(msg)
    if content_type == 'text': msgtext = msg['text']
    else: msgtext = "Vazio"
    try:username = msg['from']['username']
    except:username = 'Vazio'
    try:print("=======================================\nChat: {}\nNome: {}\nTipo: {}\nMensagem: {}\n=======================================\n".format(msg['chat']['type'], msg['from']['first_name'], content_type, msgtext))
    except:pass
    try:
        if checkblock(msg['from']['id']) == 'block': return None
    except:pass
##COMMANDS
##INFOS
    if msgtext == '/start' or msgtext == '/start@PortalNano_bot':
        await bot.sendMessage(chat_id, texts["START"][lang].format(msg['from']['first_name']))
    if msgtext == '/info' or msgtext == '/info@PortalNano_bot':
        await bot.sendMessage(chat_id, texts["INFO"][lang])
    if msgtext == '/donate' or msgtext == '/donate@PortalNano_bot':
        await bot.sendPhoto(chat_id, texts["DONATE_IMAGE_URL"]["pt"], caption=texts["DONATE"][lang], parse_mode="html")
    if msgtext == '/help' or msgtext == '/help@PortalNano_bot':
        await bot.sendMessage(chat_id, texts["HELP"][lang], parse_mode="Markdown")
    if msgtext == '/creditos' or msgtext == '/creditos@PortalNano_bot':
        await bot.sendMessage(chat_id, texts["CREDITS"][lang], parse_mode="markdown")
##FUNCS
    if msgtext == '/registrar' or msgtext == '/registrar@PortalNano_bot':
        member_status = await bot.getChatMember(chat_id, msg['from']['id'])
        member_status = member_status["status"]
        if chat_type in GROUP_TYPE and member_status not in ADMIN_TYPE:
            await bot.sendMessage(chat_id, texts["NOT_ADMIN"][lang])
            return
        conne.execute("SELECT * FROM REGISTERED WHERE USERID = {}".format(msg['chat']['id']))
        if conne.fetchone() is not None:
            if msg['chat']['type'] == 'group' or msg['chat']['type'] == 'supergroup':
                await bot.sendMessage(chat_id, texts["REGISTERED_GROUP"][lang])
            elif msg['chat']['type'] == 'channel':
                await bot.sendMessage(chat_id, texts["REGISTERED_CHANNEL"][lang])
            else:
                await bot.sendMessage(chat_id, texts["REGISTERED_USER"][lang].format(msg['from']['first_name']))
        else:
            conne.execute("INSERT INTO REGISTERED (ID, USERID) \
                VALUES (NULL, {})".format(msg['chat']['id']))
            conn.commit()
            await bot.sendMessage(chat_id, texts["REGISTER_SUCCESS"][lang])
    if msgtext == '/cancelar' or msgtext == '/cancelar@PortalNano_bot':
        member_status = await bot.getChatMember(chat_id, msg['from']['id'])
        member_status = member_status["status"]
        if chat_type in GROUP_TYPE and member_status not in ADMIN_TYPE:
            await bot.sendMessage(chat_id, texts["NOT_ADMIN"][lang])
            return
        conne.execute("SELECT * FROM REGISTERED WHERE USERID = {}".format(msg['chat']['id']))
        if conne.fetchone() is not None:
            conne.execute("DELETE FROM REGISTERED WHERE USERID = {}".format(msg['chat']['id']))
            conn.commit()
            await bot.sendMessage(chat_id, texts["CANCEL_SUCCESS"][lang])
        else:
            await bot.sendMessage(chat_id, texts["NOT_REGISTERED"][lang])
    if msgtext == '/ultimas' or msgtext == '/ultimas@PortalNano_bot':
        a = await parse()
        cont = 4
        while cont > -1:
            b = a.entries[cont]
            cont -= 1
            await asyncio.sleep(2)
            await bot.sendMessage(chat_id, b.link)
        await bot.sendMessage(chat_id, texts["LAST_NEWS"][lang])
    if msgtext.split(' ')[0] == '/cot' or msgtext.split(' ')[0] == '/cot@PortalNano_bot':
        a = await nano_cot()
        try:
            inputx = float(msg[u'text'].split(' ', 1)[1])
        except ValueError: inputx = 'invalid'
        except: inputx = None
        if inputx == 'invalid' or inputx == 0:
            await bot.sendMessage(chat_id, '❌ Valor invalido.')
        elif inputx == None or inputx == 1:
            await bot.sendMessage(chat_id, "📊 Cotação Nano\n\nRank: {}\n\nBRL: R${} ({}%) {}\nUSD: ${} ({}%) {}\nBTC: {} ₿ ({}%) {}\n\nVol, 24h: ${:,.0f} ({}%) {}\nMarket Cap: ${:,.0f} ({}%) {}\n\n🕒 {}".format(a['rank'] ,"%.2f" % a['quotes']['BRL']['price'], a['quotes']['BRL']['percent_change_24h'], cotsignal(a['quotes']['BRL']['percent_change_24h']),"%.2f" %  a['quotes']['USD']['price'], a['quotes']['USD']['percent_change_24h'], cotsignal(a['quotes']['USD']['percent_change_24h']),"%.8f" % a['quotes']['BTC']['price'], a['quotes']['BTC']['percent_change_24h'], cotsignal(a['quotes']['BTC']['percent_change_24h']),int(a['quotes']['USD']['volume_24h']), a['quotes']['USD']['volume_24h_change_24h'], cotsignal(a['quotes']['USD']['volume_24h_change_24h']), int(a['quotes']['USD']['market_cap']), a['quotes']['USD']['market_cap_change_24h'], cotsignal(a['quotes']['USD']['market_cap_change_24h']), datetime.now().strftime("%d/%m/%Y %H:%M:%S")))
        else:
            await bot.sendMessage(chat_id, "📊 Cotação {} Nano's\n\nRank: {}\n\nBRL: R${} ({}%) {}\nUSD: ${} ({}%) {}\nBTC: {} ₿ ({}%) {}\n\nVol, 24h: ${:,.0f} ({}%) {}\nMarket Cap: ${:,.0f} ({}%) {}\n\n🕒 {}".format(inputx ,a['rank'] ,"%.2f" % (a['quotes']['BRL']['price'] * inputx), a['quotes']['BRL']['percent_change_24h'], cotsignal(a['quotes']['BRL']['percent_change_24h']),"%.2f" %  (a['quotes']['USD']['price'] * inputx), a['quotes']['USD']['percent_change_24h'], cotsignal(a['quotes']['USD']['percent_change_24h']),"%.8f" %  (a['quotes']['BTC']['price'] * inputx), a['quotes']['BTC']['percent_change_24h'], cotsignal(a['quotes']['BTC']['percent_change_24h']),int(a['quotes']['USD']['volume_24h']), a['quotes']['USD']['volume_24h_change_24h'], cotsignal(a['quotes']['USD']['volume_24h_change_24h']), int(a['quotes']['USD']['market_cap']), a['quotes']['USD']['market_cap_change_24h'], cotsignal(a['quotes']['USD']['market_cap_change_24h']), datetime.now().strftime("%d/%m/%Y %H:%M:%S")))

    if msgtext == '/node' or msgtext == '/node@PortalNano_bot':
        try:
            delegators_count = await delegator_count(account = REPRESENTATIVE, url=API)
            representatives_online = await reps_online(url=API)
            representatives_online = representatives_online['representatives']
            representative_weight = Decimal(representatives_online[REPRESENTATIVE]['weight'])
            online_weight = Decimal(sum([representatives_online[representative]['weight'] for representative in representatives_online]))
            percentage_delegated = (representative_weight * 100) / online_weight

            await bot.sendMessage(chat_id, texts["NODE"][lang].format(limitDecimals(convert(representative_weight), 2), limitDecimals(percentage_delegated, 2), delegators_count, REPRESENTATIVE), parse_mode = 'Markdown')
        except:
            await bot.sendMessage(chat_id, texts["ERROR_CONTACT"][lang])
    
    if msgtext.split(' ')[0] == '/sugerir' or msgtext.split(' ')[0] == '/sugerir@PortalNano_bot':
        try:
            input = msg[u'text'].split(' ', 1)[1]
        except:
            input = None
        if input == None:
            await bot.sendMessage(chat_id, texts["NO_CONTENT"][lang])
        else:
          for m in MAINTAINERS:
            await bot.sendMessage(m, texts["SUGGEST_NEW"][lang].format(username, msg['from']['id'], input), parse_mode='HTML')
          await bot.sendMessage(chat_id, texts["SUGGEST_SUCCESS"][lang])

    if msgtext.split(' ')[0] == '/elogiar' or msgtext.split(' ')[0] == '/elogiar@PortalNano_bot':
        try:
            input = msg[u'text'].split(' ', 1)[1]
        except:
            input = None
        if input == None:
            await bot.sendMessage(chat_id, texts["NO_CONTENT"][lang])
        else:
            for m in MAINTAINERS:
              await bot.sendMessage(m, texts["COMPLIMENT_NEW"][lang].format(username, msg['from']['id'], input), parse_mode='HTML')
            await bot.sendMessage(chat_id, texts["COMPLIMENT_SUCCESS"][lang])

    if msgtext.split(' ')[0] == '/ganhar' or msgtext.split(' ')[0] == '/ganhar@PortalNano_bot':
        conne.execute("SELECT * FROM SETTINGS")
        fset = None
        fprice = None
        for i in conne.fetchall():
            fprice = i[1]
            fset = i[2]
        try:input = msg[u'text'].split(' ', 1)[1]
        except:input = None
        if fset == 'off': 
            await bot.sendMessage(chat_id, texts["ERROR_MAINTENANCE"][lang])
            return
        conne.execute("SELECT * FROM REGISTERED WHERE USERID = {}".format(msg['from']['id']))
        if conne.fetchone() is None:
            await bot.sendMessage(chat_id, texts["EARN_REGISTER"][lang])
            return
        if input == None:
            await bot.sendMessage(chat_id, texts["EARN_NOADDRESS"][lang])
        else: 
            conne.execute("SELECT * FROM FAUCET WHERE WALLET = ?", (input,))
            if conne.fetchone() is not None:
                await bot.sendMessage(chat_id, texts["EARN_ALREADY"][lang])
                return
            conne.execute("SELECT * FROM FAUCET WHERE USERID = {}".format(msg['from']['id']))
            if conne.fetchone() is not None:
                await bot.sendMessage(chat_id, texts["EARN_ALREADY"][lang])
                return
            else:
                await bot.sendMessage(chat_id, 'Aguarde...')
                header = {'Authorization': f'{config("AUTHORIZATION")}'}
                body = {'to': input, 'pin': f'{config("PIN")}', 'amount': fprice}
                a = requests.post(f'{config("ROUTE")}', headers=header, data=body).json()
                if a['meta']['message'] == 'fundos enviados':
                    sql = ''' INSERT INTO FAUCET(ID, USERID, WALLET, BLOCK)
                              VALUES(NULL, ?, ?, ?) '''
                    values = (msg['from']['id'], input, a['envelope']['block'])
                    conne.execute(sql, values)
                    conn.commit()
                    await bot.sendMessage(chat_id, texts["EARN_SUCCESS"][lang].format(a['envelope']['block']))
                else:
                    await bot.sendMessage(chat_id, texts["ERROR_CONTACT"][lang])
##SUDOS
    if msgtext == '/stats':
        if msg['from']['id'] in SUDOS:
            conne.execute("SELECT * FROM REGISTERED")
            group = 0
            user = 0
            tip = 0
            fprice = None
            fset = None
            for i in conne.fetchall():
                if i[1][:1] == '-':
                    group += 1
                else:
                    user += 1
            conne.execute("SELECT * FROM FAUCET")
            for i in conne.fetchall():
                tip += 1
            conne.execute("SELECT * FROM SETTINGS")
            for i in conne.fetchall():
                fprice = i[1]
                fset = i[2]
            await bot.sendMessage(chat_id, texts["STATS"][lang].format(group, user, tip, fprice, fset),parse_mode= 'Markdown')
    if msgtext.split(' ')[0] == '/promover':
        if msg['from']['id'] in SUDOS:
            conne.execute("SELECT * FROM REGISTERED")
            group = 0
            user = 0
            groupx = 0
            userx = 0
            for i in conne.fetchall():
                if i[1][:1] == '-':
                    group += 1
                else:
                    user += 1
                content = ""
                try:
                    msg[u'text'].split(' ', 1)[1] 
                    content = "text"
                except:
                    try:
                        msg['reply_to_message']['photo'][1]['file_id']
                        content = "photo"
                    except:
                        await bot.sendMessage(chat_id, texts["NO_CONTENT"][lang])
                try: 
                    if content != "photo":
                        await bot.sendMessage(i[1], msg[u'text'].split(' ', 1)[1])
                    else:
                        try:
                            await bot.sendPhoto(i[1], msg['reply_to_message']['photo'][1]['file_id'], msg['reply_to_message']['caption'])
                        except:
                            await bot.sendPhoto(i[1], msg['reply_to_message']['photo'][1]['file_id'])
                except:
                    if i[1][:1] == '-':
                        groupx += 1
                    else:
                        userx += 1
                    conne.execute("DELETE FROM REGISTERED WHERE USERID = {}".format(i[1]))
                    conn.commit()

            await bot.sendMessage(chat_id, texts["PROMOTE"][lang].format(group-groupx, user-userx), parse_mode= 'Markdown')
    if msgtext.split(' ')[0] == '/json':
        if msg['from']['id'] in SUDOS:
            await bot.sendMessage(chat_id, msg)

    if msgtext.split(' ')[0] == '/block':
        if msg['from']['id'] in SUDOS:
            try:
                input = msg[u'text'].split(' ', 1)[1]
            except:
                input = None
            if input == None:
                await bot.sendMessage(chat_id, texts["NO_CONTENT"][lang])
            else:
                conne.execute("SELECT * FROM BLOCKS WHERE USERID = {}".format(input))
                if conne.fetchone() is not None:
                    await bot.sendMessage(chat_id, texts["ERROR_BLOCK"][lang])
                else:
                    conne.execute("INSERT INTO BLOCKS (ID, USERID) \
                        VALUES (NULL, {})".format(input))
                    conn.commit()
                    await bot.sendMessage(chat_id, texts["BLOCK_SUCCESS"][lang])


    if msgtext.split(' ')[0] == '/unblock':
        if msg['from']['id'] in SUDOS:
            try:
                input = msg[u'text'].split(' ', 1)[1]
            except:
                input = None
            if input == None:
                await bot.sendMessage(chat_id, texts["NO_CONTENT"][lang])
            else:
                conne.execute("SELECT * FROM BLOCKS WHERE USERID = {}".format(input))
                if conne.fetchone() is None:
                    await bot.sendMessage(chat_id, texts["ERROR_UNBLOCK"][lang])
                else:
                    conne.execute("DELETE FROM BLOCKS WHERE USERID = {}".format(input))
                    conn.commit()
                    await bot.sendMessage(chat_id, texts["UNBLOCK_SUCCESS"][lang])

    if msgtext == '/blocklist':
        if msg['from']['id'] in SUDOS:
            conne.execute('SELECT USERID FROM BLOCKS')
            await bot.sendMessage(chat_id, conne.fetchall())

    if msgtext == '/freset':
        if msg['from']['id'] in SUDOS:
            conne.execute("SELECT * FROM FAUCET")
            count = 0
            for i in conne.fetchall():
                count +=1
                conne.execute("DELETE FROM FAUCET WHERE ID = {}".format(i[0]))
            conn.commit()
            if count == 0:
                await bot.sendMessage(chat_id, texts["FAUCET_EMPTY"][lang], parse_mode='markdown')
                return
            await bot.sendMessage(chat_id, texts["FRESET_SUCCESS"][lang].format(count), parse_mode='markdown')

    if msgtext.split(' ')[0] == '/fset':
        if msg['from']['id'] in SUDOS:
            input = msg[u'text'].split(' ', 1)[1]
            if input == 'on' or input == 'off':
                conne.execute("UPDATE SETTINGS SET FSET = ? WHERE ID = 1", [input])
                conn.commit()
                await bot.sendMessage(chat_id, texts["FSET_SUCCESS"][lang].format(input))
            else:
                await bot.sendMessage(chat_id, texts["INVALID_OPTION"][lang])
    
    if msgtext.split(' ')[0] == '/fprice':
        if msg['from']['id'] in SUDOS:
            try:input = float(msg[u'text'].split(' ', 1)[1])
            except ValueError: input = 0
            if input > 0:
                conne.execute("UPDATE SETTINGS SET FPRICE = ? WHERE ID = 1", [input])
                conn.commit()
                await bot.sendMessage(chat_id, texts["FPRICE_SUCCESS"][lang].format(input))
            else:
                await bot.sendMessage(chat_id, texts["INVALID_VALUE"][lang])
            
def checkblock(userid):
    conn = sqlite3.connect('portalnano.db')
    conne = conn.cursor()
    conne.execute("SELECT * FROM BLOCKS WHERE USERID = {}".format(userid))
    if conne.fetchone() is not None:
        return 'block'
    else:
        return 'unblock'

##CHECK NEWS    
async def exlast():
    conn = sqlite3.connect('portalnano.db')
    conne = conn.cursor()
    if first_new() != db_new():
        conne.execute("SELECT * FROM REGISTERED")
        for i in conne.fetchall():
            try:
                await bot.sendMessage(i[1], first_new())
            except:
                conne.execute("DELETE FROM REGISTERED WHERE USERID = {}".format(i[1]))
                conn.commit()

        try:conne.execute("UPDATE LASTNEW SET LINK = ? WHERE ID = 1", [first_new()])
        except:conne.execute("INSERT INTO LASTNEW (ID, LINK) \
                        VALUES (1, {})".format(first_new()))
        conn.commit()

class loopy(amanobot.loop.RunForeverAsThread):
    async def run_forever(self):
        while( True ):
            try: await exlast()
            except:pass
            print("repetido!")
            await asyncio.sleep(10)

#TURN BOT ON AND WORKING
bot = amanobot.aio.Bot(TOKEN)
loop = asyncio.get_event_loop()

loop.create_task(MessageLoop(bot, handle).run_forever())
loop.create_task(loopy().run_forever())

print('Listening ...')

loop.run_forever()