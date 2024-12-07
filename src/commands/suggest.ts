import config from '../config';
import bot from '../helpers/bot';

export default bot.command(['suggest', 'sugerir'], (ctx) => {
  const props = ctx.message.text.split(' ');
  if (!props[1]) {
    ctx.replyWithMarkdownV2('_Por favor, digite a sua sugestão_');
  } else {
    ctx.telegram.sendMessage(
      config.ADMIN_CHAT,
      `
📝 *Sugestão*

*Sugestão:* ${props[1]}
*Usuário:* ${ctx.message.from.username}
*ID:* ${ctx.message.from.id}
`,
      { parse_mode: 'MarkdownV2' },
    );

    ctx.replyWithMarkdownV2('_Sua sugestão foi enviada com sucesso!_');
  }
});
