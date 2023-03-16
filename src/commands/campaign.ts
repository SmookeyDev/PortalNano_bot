import axios from 'axios';
import bot from '../helpers/bot';
import client from '../helpers/nano';
import toMnano from '../lib/toMnano';
import moment from 'moment';

const getDolarPrice = async () => {
    const lastDay = moment().subtract(1, 'days').format('MM-DD-YYYY');
    const response = await axios.get(`https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/CotacaoDolarDia(dataCotacao=@dataCotacao)?@dataCotacao=%27${lastDay}%27&$top=100&$format=json`);
    const price = response.data.value[0];
    return price.cotacaoVenda;
}

const getGoal = async (account: string) => {
    const response = await axios.get('https://api.coinpaprika.com/v1/tickers/xno-nano?quotes=USD,BRL,BTC')
    const quotes = response.data.quotes
    const coinPrice = quotes.USD.price;
    const dollarPrice = await getDolarPrice();

    return ((27.90 / dollarPrice) / coinPrice).toFixed(6);
}

export default bot.command(['campaign', 'campanha'], async (ctx) => {
    const history = await client.account_history('nano_1qecfwuccd79n7q8sbbza7pyrtq1njxfigbouniuiooez9iaemjoresz78ic', 100);

    const filteredHistory = history.history.filter(transaction => {
        const transactionDate = moment.unix(transaction.local_timestamp);
        return transactionDate.isAfter(moment().subtract(30, 'days'));
    });

    const lastBalance = toMnano(filteredHistory.reduce((acc: any, item: any) => acc + Number(item.amount), 0), 6);

    const lastTransactionsMessage = filteredHistory.map(transaction => {
        return `${transaction.account} - ${toMnano(transaction.amount, 6)} - ${moment.unix(transaction.local_timestamp).format('DD/MM/YYYY HH:mm:ss')}`
    }).join('\n')

    const campaignGoal = await getGoal('nano_1qecfwuccd79n7q8sbbza7pyrtq1njxfigbouniuiooez9iaemjoresz78ic')
    const missingToGoal = (Number(campaignGoal) - Number(lastBalance)).toFixed(6)

    ctx.replyWithMarkdown(`💸 *Campanha para custear o servidor do bot* 💸

*Saldo dos ultimos 30 dias:* Ӿ${lastBalance}
*Meta:* Ӿ${campaignGoal} (Faltam: Ӿ${missingToGoal})

*Doações recentes:*
${lastTransactionsMessage}

*Doe para ajudar a manter o bot online:*` + "\n```nano_1qecfwuccd79n7q8sbbza7pyrtq1njxfigbouniuiooez9iaemjoresz78ic```", { reply_to_message_id: ctx.message.message_id })

});