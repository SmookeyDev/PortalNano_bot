import bot from '../helpers/bot';
import Big from 'big.js';
import axios from 'axios';

const toMnano = (value: number) => {
    const multNANO = Big('1000000000000000000000000000000');
    return Big(value).div(multNANO).toFixed(2).toString()
};

export default bot.command('node', (ctx) => {
    let props = ctx.message.text.split(" ")
    let value = props[1] ? props[1] : 'nano_1j78msn5omp8jrjge8txwxm4x3smusa1cojg7nuk8fdzoux41fqeeogg5aa1'

    axios.get(`https://mynano.ninja/api/accounts/${value}`).then(function (response) {
        const data = response.data
        ctx.replyWithMarkdown(`
📊 Estatísticas do Node *${data.alias}*

*Peso de voto:* Ӿ${toMnano(data.votingweight)}
*Quantidade de delegadores:* ${data.delegators}\n\n` + 'Ajude a descentralizar a Nano! Delegue suas Nanos para o nosso node: ```nano_1j78msn5omp8jrjge8txwxm4x3smusa1cojg7nuk8fdzoux41fqeeogg5aa1```')
    }).catch(err => {
        ctx.replyWithMarkdown('_Esse node não existe, não está online ou não é um representante principal._', { reply_to_message_id: ctx.message.message_id })
    })
});