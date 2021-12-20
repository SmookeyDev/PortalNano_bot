const bot = require("../helpers/bot")
require('../../.env')

bot.command(['suggest', 'sugerir'], (ctx) => {
    const props = ctx.message.text.split(" ")
    if (!props[1]) {
        ctx.replyWithMarkdown("_Por favor, digite a sua sugestão._", { reply_to_message_id: ctx.message.message_id })
    }
    else {
        ctx.telegram.sendMessage(ADMIN_CHAT, `
📝 *Sugestão*

*Sugestão:* ${props[1]}
*Usuário:* ${ctx.message.from.username}
*ID:* ${ctx.message.from.id}
        `, { parse_mode: 'MarkdownV2' })

        ctx.replyWithMarkdown('_Sua sugestão foi enviada com sucesso!_', { reply_to_message_id: ctx.message.message_id })
    }
});