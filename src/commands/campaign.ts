import axios from 'axios';
import bot from '../helpers/bot';
import client from '../helpers/nano';
import toMnano from '../lib/toMnano';
import moment from 'moment';
import escapeMarkdownV2 from '../lib/escapeMarkdownV2';
import config from '../config';

const getGoal = async () => {
  const { data } = await axios.get(
    'https://api.coinpaprika.com/v1/tickers/xno-nano?quotes=USD,BRL,BTC',
  );
  const coinPrice = data.quotes.USD.price;
  return parseFloat((5 / coinPrice).toFixed(6));
};

const formatTransaction = (transaction: any) => {
  const account = escapeMarkdownV2(transaction.account);
  const amount = escapeMarkdownV2(toMnano(Number(transaction?.amount), 6));
  const timestamp = moment.unix(Number(transaction?.local_timestamp)).format('DD/MM/YYYY HH:mm:ss');
  return `[${account} - Ӿ${amount} - ${timestamp}](https://nanolooker.com/block/${transaction.hash})`;
};

export default bot.command(['campaign', 'campanha'], async (ctx) => {
  try {
    const { history } = await client.account_history(config.NANO_WALLET, 100);
    const filteredHistory = history?.filter((transaction) => {
      const transactionDate = moment.unix(Number(transaction?.local_timestamp));
      return (
        transactionDate.isAfter(moment().subtract(30, 'days')) && transaction.type === 'receive'
      );
    });

    const lastBalance = parseFloat(
      toMnano(
        filteredHistory?.reduce((acc: any, item: any) => acc + Number(item.amount), 0),
        6,
      ),
    );
    const lastTransactionsMessage =
      filteredHistory?.map(formatTransaction).join('\n') ||
      'Nenhuma doação recebida nos últimos 30 dias';

    const campaignGoal = await getGoal();
    const diff = parseFloat(Math.max(0, campaignGoal - lastBalance).toFixed(6));

    const escapedText = {
      lastBalance: escapeMarkdownV2(lastBalance.toString()),
      campaignGoal: escapeMarkdownV2(campaignGoal.toString()),
      missingToGoal: escapeMarkdownV2(diff.toString()),
    };

    const text = `💸 *Campanha para custear o servidor do bot* 💸

*Saldo dos últimos 30 dias:* Ӿ${escapedText.lastBalance}
*Meta:* Ӿ${escapedText.campaignGoal} \\(Faltam: Ӿ${escapedText.missingToGoal}\\)

*Doações recentes:*
${lastTransactionsMessage}

*Doe para ajudar a manter o bot online:*
\`${config.NANO_WALLET}\``;

    ctx.replyWithMarkdownV2(text);
  } catch (err) {
    console.error(err);
    ctx.replyWithMarkdownV2('_Ocorreu um erro ao obter os dados_');
  }
});
