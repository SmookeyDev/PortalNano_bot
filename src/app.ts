import bot from './helpers/bot';
import moment from 'moment';
import './commands';

bot.on('message', (ctx: any) => {
  const username =
    ctx.message.from.username != undefined
      ? ctx.message.from.username
      : ctx.message.from.first_name;
  console.log(
    `[${moment().format('DD/MM/YYYY HH:mm:ss')}] ${username} - ${ctx.message.text} (${ctx.message.from.id})`,
  );
});

bot.launch().then(() => {
  console.info(`\n${bot.botInfo?.username} is running. (ID: ${bot.botInfo?.id})`);
});
