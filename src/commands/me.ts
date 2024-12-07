import bot from '../helpers/bot';
import { Markup } from 'telegraf';

export default bot.command('me', (ctx) => {
  const username = ctx.from.username ? `*Usuário:* @${ctx.from.username}` : '';

  if (ctx.chat.type == 'private') {
    ctx.replyWithMarkdownV2(`👤 *Seus dados* 👤
        
*ID:* ${ctx.from.id}
*Nome:* ${ctx.from.first_name}
${username}
        `);
  } else if (ctx.chat.type == 'group' || ctx.chat.type == 'supergroup') {
    const link = ctx.chat['username'] ? `*Link:* https://t.me/${ctx.chat['username']}` : '';

    ctx.telegram
      .sendMessage(
        ctx.message.from.id,
        `👤 *Seus dados* 👤
*ID:* ${ctx.from.id}
*Nome:* ${ctx.from.first_name}
${username}
    
👥 Informações do chat 👥
*ID:* ${ctx.chat.id}
*Nome:* ${ctx.chat.title}
${link}`,
        { parse_mode: 'Markdown' },
      )
      .then(() => {
        ctx.replyWithMarkdownV2(
          `[Enviado em chat privado.](https://t.me/${bot.botInfo?.username})`,
        );
      })
      .catch(() => {
        ctx.replyWithMarkdownV2(
          '_Erro ao enviar a mensagem no privado, inicie o bot_',
          Markup.inlineKeyboard([
            Markup.button.url('Iniciar bot', `https://t.me/${bot.botInfo?.username}?start=`),
          ]),
        );
      });
  } else {
    ctx.replyWithMarkdownV2(
      '_Este comando só pode ser usado em chats privados ou grupos_',
      Markup.inlineKeyboard([
        Markup.button.url('Iniciar bot', `https://t.me/${bot.botInfo?.username}?start=/me`),
      ]),
    );
  }
});
