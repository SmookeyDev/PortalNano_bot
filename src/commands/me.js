const bot = require("../helpers/bot");
const { Markup } = require('telegraf');


bot.command("/me", ctx => {
    const username = ctx.from.username ? `*Usuário:* @${ctx.from.username}` : ""

    if (ctx.chat.type == "private") {
        ctx.replyWithMarkdown(`👤 *Seus dados* 👤
        
*ID:* ${ctx.from.id}
*Nome:* ${ctx.from.first_name}
${username}
        `)
    }

    else {
        const link = ctx.chat.username ? `*Link:* https://t.me/${ctx.chat.username}` : ""

        ctx.telegram.sendMessage(ctx.message.from.id, `👤 *Seus dados* 👤
*ID:* ${ctx.from.id}
*Nome:* ${ctx.from.first_name}
${username}
    
👥 Informações do chat 👥
*ID:* ${ctx.chat.id}
*Nome:* ${ctx.chat.title}
${link}`, { parse_mode: "Markdown" })
        .then(() => {
            ctx.replyWithMarkdown(`[Enviado em chat privado.](https://t.me/${bot.botInfo.username})`, { reply_to_message_id: ctx.message.message_id, disable_web_page_preview: true })
        }).catch(() => {
            ctx.replyWithMarkdown('_Erro ao enviar a mensagem no privado, inicie o bot._', Markup.inlineKeyboard([
                Markup.button.url('Iniciar bot', `https://t.me/${bot.botInfo.username}?start=`)
            ]))
        })
    }

})