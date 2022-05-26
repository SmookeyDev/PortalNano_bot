import bot from '../helpers/bot';
import axios from 'axios';
import moment from 'moment';
import { Markup } from 'telegraf';

const validNumber = (value: number) => {
    return !isNaN(value) && value > 0 && value != undefined
};

const formatPercent = (value: number) => {
    const emoji = value < 1 ? '🔻' : '🔺'
    return (`(${value}%) ${emoji}`)
};

const formatter = new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: 2
});

const getData = async (value: number) => {
    try {
        const response = await axios.get('https://api.coinpaprika.com/v1/tickers/xno-nano?quotes=USD,BRL,BTC')
        let quotes = response.data.quotes
        let title = value > 0 ? `📊 Cotação Ӿ${value}` : `📊 Cotação Nano`
        
        return `
    ${title}
            
Rank: ${response.data.rank}
            
BRL: R$${(quotes.BRL.price * value).toFixed(2)} ${formatPercent(quotes.BRL.percent_change_24h)}
USD: $${(quotes.USD.price * value).toFixed(2)} ${formatPercent(quotes.USD.percent_change_24h)}
BTC: ${(quotes.BTC.price * value).toFixed(8)} ₿ ${formatPercent(quotes.BTC.percent_change_24h)}
            
Vol, 24h: ${formatter.format(quotes.USD.volume_24h)} ${formatPercent(quotes.USD.volume_24h_change_24h)}
Market Cap: ${formatter.format(quotes.USD.market_cap)} ${formatPercent(quotes.USD.market_cap_change_24h)}
          
🕒 ${moment().format('DD/MM/YYYY HH:mm:ss')}
            `
    }
    catch{
        return 'Erro ao obter dados.'
    }
};

export default bot.command('cot', async (ctx) => {
    let props = ctx.message.text.split(" ")
    let value = Number(props[1] ? props[1] : 1)

    if (!validNumber(value)) {
        ctx.replyWithMarkdown('_Digite um valor válido._', { reply_to_message_id: ctx.message.message_id })
        return;
    }

    const data = await getData(value)
    ctx.replyWithMarkdown(data, Markup.inlineKeyboard([
        Markup.button.callback('Atualizar', `refresh ${value}`)
    ]))
});

bot.action(/refresh [-+]?(\d*[\.|\,]\d+|\d+)/, async (ctx) => {
    const value = Number(ctx.match[1])

    const data = await getData(value)
    ctx.editMessageText(data, Markup.inlineKeyboard([
        Markup.button.callback('Atualizar', `refresh ${value}`)
    ]))
});