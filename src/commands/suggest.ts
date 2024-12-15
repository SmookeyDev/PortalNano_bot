import config from '../config';
import bot from '../helpers/bot';
import escapeMarkdownV2 from '../lib/escapeMarkdownV2';

export default bot.command(['suggest', 'sugerir'], (ctx) => {
  const props = ctx.message.text.split(' ');
  if (!props[1]) {
    ctx.replyWithMarkdownV2('_Por favor, digite a sua sugestão_');
  } else {
    ctx.telegram.sendMessage(
      config.ADMIN_CHAT,
      `
📝 *Sugestão*

*Sugestão:* ${escapeMarkdownV2(props[1])}
*Usuário:* ${escapeMarkdownV2(ctx.message.from.username)}
*ID:* ${ctx.message.from.id}
`,
      { parse_mode: 'MarkdownV2' },
    );

    ctx.replyWithMarkdownV2('_Sua sugestão foi enviada com sucesso_');
  }
});
