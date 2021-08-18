const bot = require('../helpers/bot')
const Big = require('big.js')
const axios = require('axios')

function toMnano(value) {
    const multNANO = Big('1000000000000000000000000000000');
    return Big(value).div(multNANO).toFixed(2).toString()
}

bot.command('node', ctx => {
    let props = ctx.message.text.split(" ")
    let value = props[1] ? props[1] : 'nano_1j78msn5omp8jrjge8txwxm4x3smusa1cojg7nuk8fdzoux41fqeeogg5aa1'

    axios.get(`https://mynano.ninja/api/accounts/${value}`).then(function (response) {
        data = response.data
        ctx.replyWithMarkdown(`
📊 Estatísticas do Node *${data.alias}*

*Peso de voto:* ${toMnano(data.votingweight)} Nanos
*Quantidade de delegadores:* ${data.delegators}\n\n` + 'Ajude a descentralizar a Nano! Delegue suas Nanos para o nosso node: ```nano_1j78msn5omp8jrjge8txwxm4x3smusa1cojg7nuk8fdzoux41fqeeogg5aa1```')
    }).catch(err => {
        ctx.reply('Esse node não existe, não está online ou não é um representante principal.')
    })
})