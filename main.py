import amanobot
import time
import amanobot
import sqlite3
import new
import feedparser
import requests

from os              import environ
from decouple        import config
from amanobot.loop   import MessageLoop
from datetime        import datetime
from decimal         import Decimal
from numberFunctions import limitDecimals, convert

environ["BANANO_HTTP_PROVIDER_URI"] = "https://api.nanex.cc"

import bananopy.banano as nano

##SQLITE


##TOKEN
TOKEN = config('TOKEN') #Token do Portal

REPRESENTATIVE = "nano_1j78msn5omp8jrjge8txwxm4x3smusa1cojg7nuk8fdzoux41fqeeogg5aa1" # endereço do node representativo da Nano Brasil

sudos = [392285660, 884455410, 103893853]

##DEFS

def handle(msg):
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
    if msg['text'] == '/start' or msg['text'] == '/start@PortalNano_bot':
        bot.sendMessage(chat_id, "Olá {}. Ao usar /registrar, você receberá atualizações do nosso portal.".format(msg['from']['first_name']))
    if msg['text'] == '/info' or msg['text'] == '/info@PortalNano_bot':
        bot.sendMessage(chat_id, "O Portal Nano tem como missão informar, instruir e apresentar a Nano para todos. Trazer o melhor conteúdo sobre essa tecnologia e demais novidades sobre o mundo das criptomoedas. Nano é a Luz!\n\nhttp://portalnano.com.br")
    if msg['text'] == '/donate' or msg['text'] == '/donate@PortalNano_bot':
        bot.sendPhoto(chat_id, "https://portalnano.com.br/wp-content/uploads/2020/06/nano-addres-420x420.png", caption=f"Faça-nos uma doação: <code>nano_37d1td77mifoowrziawdtas9ggenhjqhf745oinf8f1g949jygcw9hzhtdrt</code>", parse_mode="html")
    if msg['text'] == '/help' or msg['text'] == '/help@PortalNano_bot':
        bot.sendMessage(chat_id, "📲 *Lista de Comandos*\n\n/start - Inicia do Bot.\n/info - Mostra informações do portal.\n/donate - Mostra uma carteira NANO destinada a receber doações ao portal.\n/creditos - Mostra os desenvolvedores do bot e um endereço de doação para apoiar-los\n/registrar - Ativa o recebimento de noticias.\n/cancelar - Cancela o recebimento de noticias.\n/ultimas - Lista as ultimas 5 noticias lançadas no portal.\n/cot - Mostra a atual cotação da NANO.\n/sugerir - Possibilita nos sugerir uma nova funcionalidade ou noticia.\n/elogiar - Possibilita nos elogiar :)\n/ganhar - Recebe uma pequena quantia em nano.", parse_mode="Markdown")
    if msg['text'] == '/creditos' or msg['text'] == '/creditos@PortalNano_bot':
        bot.sendMessage(chat_id, "🖥 *Creditos*\n\n*Desenvolvedor:* @xSmookeyBR\n*Endereço para me apoiar:* ```nano_1qecfwuccd79n7q8sbbza7pyrtq1njxfigbouniuiooez9iaemjoresz78ic```", parse_mode="markdown")
##FUNCS
    if msg['text'] == '/registrar' or msg['text'] == '/registrar@PortalNano_bot':
        conne.execute("SELECT * FROM REGISTERED WHERE USERID = {}".format(msg['chat']['id']))
        if conne.fetchone() is not None:
            if msg['chat']['type'] == 'group' or msg['chat']['type'] == 'supergroup':
                bot.sendMessage(chat_id, "Ops, este grupo já está registrado. Para receber as noticias em particular, vá ao privado do bot e digite /registrar.")
            elif msg['chat']['type'] == 'channel':
                bot.sendMessage(chat_id, "Ops, este canal já está registrado.")
            else:
                bot.sendMessage(chat_id, "Ops {}, você já está registrado. Para cancelar o recebimento das noticias digite /cancelar.".format(msg['from']['first_name']))
        else:
            conne.execute("INSERT INTO REGISTERED (ID, USERID) \
                VALUES (NULL, {})".format(msg['chat']['id']))
            conn.commit()
            bot.sendMessage(chat_id, "Inscrição efetuada com sucesso, agora você irá receber noticias do portal. Use /ganhar seguido do endereço da sua carteira nano para ganhar uma pequena quantia.")
    if msg['text'] == '/cancelar' or msg['text'] == '/cancelar@PortalNano_bot':
        conne.execute("SELECT * FROM REGISTERED WHERE USERID = {}".format(msg['chat']['id']))
        if conne.fetchone() is not None:
            conne.execute("DELETE FROM REGISTERED WHERE USERID = {}".format(msg['chat']['id']))
            conn.commit()
            bot.sendMessage(chat_id, "Inscrição cancelada com sucesso, agora você não irá mais receber noticias do portal.")
        else:
            bot.sendMessage(chat_id, "Ops, você ainda não está registrado.")
    if msg['text'] == '/ultimas' or msg['text'] == '/ultimas@PortalNano_bot':
        a = feedparser.parse("https://portalnano.com.br/blog/feed")
        cont = 4
        while cont > -1:
            b = a.entries[cont]
            cont -= 1
            time.sleep(2)
            bot.sendMessage(chat_id, b.link)
        bot.sendMessage(chat_id, "Estas foram as últimas notícias.")
    if msg['text'].split(' ')[0] == '/cot' or msg['text'].split(' ')[0] == '/cot@PortalNano_bot':
        a = requests.get('https://api.coinpaprika.com/v1/tickers/nano-nano?quotes=BRL,USD,BTC').json()
        try:
            inputx = float(msg[u'text'].split(' ', 1)[1])
        except ValueError: inputx = 'invalid'
        except: inputx = None
        if inputx == 'invalid' or inputx == 0:
            bot.sendMessage(chat_id, '❌ Valor invalido.')
        elif inputx == None or inputx == 1:
            bot.sendMessage(chat_id, "📊 Cotação Nano\n\nRank: {}\n\nBRL: R${} ({}%) {}\nUSD: ${} ({}%) {}\nBTC: {} ₿ ({}%) {}\n\nVol, 24h: ${:,.0f} ({}%) {}\nMarket Cap: ${:,.0f} ({}%) {}\n\n🕒 {}".format(a['rank'] ,"%.2f" % a['quotes']['BRL']['price'], a['quotes']['BRL']['percent_change_24h'], cotsignal(a['quotes']['BRL']['percent_change_24h']),"%.2f" %  a['quotes']['USD']['price'], a['quotes']['USD']['percent_change_24h'], cotsignal(a['quotes']['USD']['percent_change_24h']),"%.8f" % a['quotes']['BTC']['price'], a['quotes']['BTC']['percent_change_24h'], cotsignal(a['quotes']['BTC']['percent_change_24h']),int(a['quotes']['USD']['volume_24h']), a['quotes']['USD']['volume_24h_change_24h'], cotsignal(a['quotes']['USD']['volume_24h_change_24h']), int(a['quotes']['USD']['market_cap']), a['quotes']['USD']['market_cap_change_24h'], cotsignal(a['quotes']['USD']['market_cap_change_24h']), datetime.now().strftime("%d/%m/%Y %H:%M:%S")))
        else:
            bot.sendMessage(chat_id, "📊 Cotação {} Nano's\n\nRank: {}\n\nBRL: R${} ({}%) {}\nUSD: ${} ({}%) {}\nBTC: {} ₿ ({}%) {}\n\nVol, 24h: ${:,.0f} ({}%) {}\nMarket Cap: ${:,.0f} ({}%) {}\n\n🕒 {}".format(inputx ,a['rank'] ,"%.2f" % (a['quotes']['BRL']['price'] * inputx), a['quotes']['BRL']['percent_change_24h'], cotsignal(a['quotes']['BRL']['percent_change_24h']),"%.2f" %  (a['quotes']['USD']['price'] * inputx), a['quotes']['USD']['percent_change_24h'], cotsignal(a['quotes']['USD']['percent_change_24h']),"%.8f" %  (a['quotes']['BTC']['price'] * inputx), a['quotes']['BTC']['percent_change_24h'], cotsignal(a['quotes']['BTC']['percent_change_24h']),int(a['quotes']['USD']['volume_24h']), a['quotes']['USD']['volume_24h_change_24h'], cotsignal(a['quotes']['USD']['volume_24h_change_24h']), int(a['quotes']['USD']['market_cap']), a['quotes']['USD']['market_cap_change_24h'], cotsignal(a['quotes']['USD']['market_cap_change_24h']), datetime.now().strftime("%d/%m/%Y %H:%M:%S")))
    
    if msg['text'] == '/node' or msg['text'] == '/node@PortalNano_bot':
        try:
            delegators_count = nano.delegators_count(REPRESENTATIVE)['count']
            representatives_online = nano.representatives_online(weight = True)['representatives']
            representative_weight = Decimal(representatives_online[REPRESENTATIVE]['weight'])
            online_weight = Decimal(sum([representatives_online[representative]['weight'] for representative in representatives_online]))
            percentage_delegated = (representative_weight * 100) / online_weight

            bot.sendMessage(chat_id, 'Estatísticas do node NanoBrasil:\n\nPeso de voto: {} nanos\n% do peso de voto online: {}%\nQuantidade de delegadores: {}\n\nAjude a descentralizar a nano! Delegue suas nanos para o nosso node:\n<code>{}</code>'.format(limitDecimals(convert(representative_weight), 2), limitDecimals(percentage_delegated, 2), delegators_count, REPRESENTATIVE), parse_mode = 'HTML')
        except:
            bot.sendMessage(chat_id, 'Algo deu errado ao pegar as estatisticas do node.')
    
    if msg['text'].split(' ')[0] == '/sugerir' or msg['text'].split(' ')[0] == '/sugerir@PortalNano_bot':
        try:
            input = msg[u'text'].split(' ', 1)[1]
        except:
            input = None
        if input == None:
            bot.sendMessage(chat_id, 'Erro: você não informou nenhum conteúdo.')
        else:
            bot.sendMessage(chat_id, '💭 Sugestão enviada com sucesso, agradecemos a sua contribuição.')
            bot.sendMessage(-1001450559410, '💭 <b>Nova sugestão.</b>\n\n<b>Usuário:</b> @{}\n<b>ID do Usuário:</b> {}\n\n<b>Conteúdo:</b> {}'.format(username, msg['from']['id'], input), parse_mode='HTML')

    if msg['text'].split(' ')[0] == '/elogiar' or msg['text'].split(' ')[0] == '/elogiar@PortalNano_bot':
        try:
            input = msg[u'text'].split(' ', 1)[1]
        except:
            input = None
        if input == None:
            bot.sendMessage(chat_id, 'Erro: você não informou nenhum conteúdo.')
        else:
            bot.sendMessage(chat_id, '💭 Elogio enviado com sucesso, agradecemos a sua contribuição.')
            bot.sendMessage(-1001450559410, '💭 <b>Novo elogio.</b>\n\n<b>Usuário:</b> @{}\n<b>ID do Usuário:</b> {}\n\n<b>Conteúdo:</b> {}'.format(username, msg['from']['id'], input), parse_mode='HTML')

    if msg['text'].split(' ')[0] == '/ganhar' or msg['text'].split(' ')[0] == '/ganhar@PortalNano_bot':
        conne.execute("SELECT * FROM SETTINGS")
        fset = None
        fprice = None
        for i in conne.fetchall():
            fprice = i[1]
            fset = i[2]
        try:input = msg[u'text'].split(' ', 1)[1]
        except:input = None
        if fset == 'off': return bot.sendMessage(chat_id, 'Opa, neste momento essa função se encontra em manutenção. Tente novamente mais tarde.')
        conne.execute("SELECT * FROM REGISTERED WHERE USERID = {}".format(msg['from']['id']))
        if conne.fetchone() is None: return bot.sendMessage(chat_id, 'Opa, pra você poder usar nosso faucet precisa estar registrado. Use /registrar no privado.')
        if input == None:
            bot.sendMessage(chat_id, 'Erro: você não informou nenhum endereço. Use: /ganhar <endereço>')
        else: 
            conne.execute("SELECT * FROM FAUCET WHERE WALLET = ?", (input,))
            if conne.fetchone() is not None:
                return bot.sendMessage(chat_id, 'Ops! você já ganhou suas nanos!')
            conne.execute("SELECT * FROM FAUCET WHERE USERID = {}".format(msg['from']['id']))
            if conne.fetchone() is not None:
                return bot.sendMessage(chat_id, 'Ops! você já ganhou suas nanos!')
            else:
                bot.sendMessage(chat_id, 'Aguarde...')
                header = {'Authorization': f'{config("AUTHORIZATION")}'}
                body = {'to': input, 'pin': f'{config("PIN")}', 'amount': fprice}
                a = requests.post(f'{config("ROUTE")}', headers=header, data=body).json()
                if a['meta']['message'] == 'fundos enviados':
                    sql = ''' INSERT INTO FAUCET(ID, USERID, WALLET, BLOCK)
                              VALUES(NULL, ?, ?, ?) '''
                    values = (msg['from']['id'], input, a['envelope']['block'])
                    conne.execute(sql, values)
                    conn.commit()
                    bot.sendMessage(chat_id, 'Quantia enviada com sucesso para a wallet informada. Você pode checar a transação em https://nanocrawler.cc/explorer/block/{}'.format(a['envelope']['block']))
                else:
                    bot.sendMessage(chat_id, 'Ocorreu algum problema, entre em contato com um dos desenvolvedores: @xSmookeyBR ou @Marcosnunesmbs')
##SUDOS
    if msg['text'] == '/stats':
        if msg['from']['id'] in sudos:
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
            bot.sendMessage(chat_id, "👨‍👨‍👦*Registrados*\n\nGrupos: {}\nUsuários: {}\n\n💦*Faucet*\n\nTipados: {}\nValor: {}\nEstado: {}".format(group, user, tip, fprice, fset),parse_mode= 'Markdown')
    if msg['text'].split(' ')[0] == '/promover':
        if msg['from']['id'] in sudos:
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
                        bot.sendMessage(chat_id, "Erro: não foi informado nenhum conteúdo")
                try: 
                    if content != "photo":
                        bot.sendMessage(i[1], msg[u'text'].split(' ', 1)[1])
                    else:
                        try:
                            bot.sendPhoto(i[1], msg['reply_to_message']['photo'][1]['file_id'], msg['reply_to_message']['caption'])
                        except:
                            bot.sendPhoto(i[1], msg['reply_to_message']['photo'][1]['file_id'])
                except:
                    if i[1][:1] == '-':
                        groupx += 1
                    else:
                        userx += 1
                    conne.execute("DELETE FROM REGISTERED WHERE USERID = {}".format(i[1]))
                    conn.commit()

            bot.sendMessage(chat_id, "📢Promoção Completa\n\n*Grupos:* {}\n*Usuários:* {}".format(group-groupx, user-userx), parse_mode= 'Markdown')
    if msg['text'].split(' ')[0] == '/json':
        if msg['from']['id'] in sudos:
            bot.sendMessage(chat_id, msg)

    if msg['text'].split(' ')[0] == '/block':
        if msg['from']['id'] in sudos:
            try:
                input = msg[u'text'].split(' ', 1)[1]
            except:
                input = None
            if input == None:
                bot.sendMessage(chat_id, 'Erro: você não informou nenhum conteúdo.')
            else:
                conne.execute("SELECT * FROM BLOCKS WHERE USERID = {}".format(input))
                if conne.fetchone() is not None:
                    bot.sendMessage(chat_id, 'Erro: esse usuário já esta bloqueado.')
                else:
                    conne.execute("INSERT INTO BLOCKS (ID, USERID) \
                        VALUES (NULL, {})".format(input))
                    conn.commit()
                    bot.sendMessage(chat_id, 'Bloqueio efetuado com sucesso, agora esse usuário não pode mais usar nenhum comando.')


    if msg['text'].split(' ')[0] == '/unblock':
        if msg['from']['id'] in sudos:
            try:
                input = msg[u'text'].split(' ', 1)[1]
            except:
                input = None
            if input == None:
                bot.sendMessage(chat_id, 'Erro: você não informou nenhum conteúdo.')
            else:
                conne.execute("SELECT * FROM BLOCKS WHERE USERID = {}".format(input))
                if conne.fetchone() is None:
                    bot.sendMessage(chat_id, 'Erro: esse usuário não está bloqueado.')
                else:
                    conne.execute("DELETE FROM BLOCKS WHERE USERID = {}".format(input))
                    conn.commit()
                    bot.sendMessage(chat_id, 'Desbloqueado com sucesso, agora esse usuário pode usar o bot novamente.')

    if msg['text'] == '/blocklist':
        if msg['from']['id'] in sudos:
            conne.execute('SELECT USERID FROM BLOCKS')
            bot.sendMessage(chat_id, conne.fetchall())

    if msg['text'] == '/freset':
        if msg['from']['id'] in sudos:
            conne.execute("SELECT * FROM FAUCET")
            count = 0
            for i in conne.fetchall():
                count +=1
                conne.execute("DELETE FROM FAUCET WHERE ID = {}".format(i[0]))
            conn.commit()
            if count == 0: return bot.sendMessage(chat_id, '❌ *A tabela já esta vazia.*', parse_mode='markdown')
            bot.sendMessage(chat_id, '🔥 *Tabela resetada.*\n\n*Pessoas:* {}'.format(count), parse_mode='markdown')

    if msg['text'].split(' ')[0] == '/fset':
        if msg['from']['id'] in sudos:
            input = msg[u'text'].split(' ', 1)[1]
            if input == 'on' or input == 'off':
                conne.execute("UPDATE SETTINGS SET FSET = ? WHERE ID = 1", [input])
                conn.commit()
                bot.sendMessage(chat_id, 'Sucesso, o faucet foi setado como {}'.format(input))
            else:
                bot.sendMessage(chat_id, '❌ Opção invalida.')
    
    if msg['text'].split(' ')[0] == '/fprice':
        if msg['from']['id'] in sudos:
            try:input = float(msg[u'text'].split(' ', 1)[1])
            except ValueError: input = 0
            if input > 0:
                conne.execute("UPDATE SETTINGS SET FPRICE = ? WHERE ID = 1", [input])
                conn.commit()
                bot.sendMessage(chat_id, 'Sucesso, o preço foi ajustado para {}'.format(input))
            else:
                bot.sendMessage(chat_id, '❌ Valor invalido.')
            
def checkblock(userid):
    conn = sqlite3.connect('portalnano.db')
    conne = conn.cursor()
    conne.execute("SELECT * FROM BLOCKS WHERE USERID = {}".format(userid))
    if conne.fetchone() is not None:
        return 'block'
    else:
        return 'unblock'

def cotsignal(argument):
    if str(argument)[:1] == "-":
        return "🔻"
    else:
        return "🔺"

##CHECK NEWS    
def exlast():
    conn = sqlite3.connect('portalnano.db')
    conne = conn.cursor()
    if new.first_new() != new.db_new():
        conne.execute("SELECT * FROM REGISTERED")
        for i in conne.fetchall():
            try:
                bot.sendMessage(i[1], new.first_new())
            except:
                conne.execute("DELETE FROM REGISTERED WHERE USERID = {}".format(i[1]))
                conn.commit()

        try:conne.execute("UPDATE LASTNEW SET LINK = ? WHERE ID = 1", [new.first_new()])
        except:conne.execute("INSERT INTO LASTNEW (ID, LINK) \
                        VALUES (1, {})".format(new.first_new()))
        conn.commit()


#TURN BOT ON AND WORKING
bot = amanobot.Bot(TOKEN)
MessageLoop(bot, handle).run_as_thread()

while 1:
    try:exlast()
    except:pass
    time.sleep(10)
