const bot = require("../helpers/bot");
const axios = require('axios')
const moment = require('moment')

function formatPercent(value) {
    emoji = value < 1 ? '🔻' : '🔺'
    return (`(${value}%) ${emoji}`)
}

const formatter = new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: 2
})

bot.command('cot', ctx => {
    let props = ctx.message.text.split(" ")
    let value = props[1] ? props[1] : 1

    axios.get('https://api.coinpaprika.com/v1/tickers/NANO-NANO?quotes=USD,BRL,BTC,EUR').then(function (response) {
        let quotes = response.data.quotes
        let title = value > 1 ? `📊 Cotação ${value} Nano's` : `📊 Cotação Nano`

        ctx.telegram.sendMessage(ctx.message.chat.id, `
${title}

Rank: ${response.data.rank}

BRL: R$${(quotes.BRL.price * value).toFixed(2)} ${formatPercent(quotes.BRL.percent_change_24h)}
USD: $${(quotes.USD.price * value).toFixed(2)} ${formatPercent(quotes.USD.percent_change_24h)}
EUR: €${(quotes.EUR.price * value).toFixed(2)} ${formatPercent(quotes.EUR.percent_change_24h)}
BTC: ${(quotes.BTC.price * value).toFixed(8)} ₿ ${formatPercent(quotes.BTC.percent_change_24h)}

Vol, 24h: ${formatter.format(quotes.USD.volume_24h)} ${formatPercent(quotes.USD.volume_24h_change_24h)}
Market Cap: ${formatter.format(quotes.USD.market_cap)} ${formatPercent(quotes.USD.market_cap_change_24h)}

🕒 ${moment().format('DD/MM/YYYY HH:mm:ss')}
`)
    })


})