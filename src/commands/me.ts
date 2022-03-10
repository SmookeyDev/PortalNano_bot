import bot from '../helpers/bot';
import { Markup } from "telegraf"


export default bot.command('me', (ctx) => {
    const username = ctx.from.username ? `*Usuário:* @${ctx.from.username}` : ""

    if (ctx.chat.type == "private") {
        ctx.replyWithMarkdown(`👤 *Seus dados* 👤
        
*ID:* ${ctx.from.id}
*Nome:* ${ctx.from.first_name}
${username}
        `)
    }

    else if (ctx.chat.type == "group" || ctx.chat.type == "supergroup") {
        const link = ctx.chat['username'] ? `*Link:* https://t.me/${ctx.chat['username']}` : ""

        ctx.telegram.sendMessage(ctx.message.from.id, `👤 *Seus dados* 👤
*ID:* ${ctx.from.id}
*Nome:* ${ctx.from.first_name}
${username}
    
👥 Informações do chat 👥
*ID:* ${ctx.chat.id}
*Nome:* ${ctx.chat.title}
${link}`, { parse_mode: "Markdown" })
            .then(() => {
                ctx.replyWithMarkdown(`[Enviado em chat privado.](https://t.me/${bot.botInfo?.username})`, { reply_to_message_id: ctx.message.message_id, disable_web_page_preview: true })
            }).catch(() => {
                ctx.replyWithMarkdown('_Erro ao enviar a mensagem no privado, inicie o bot._', Markup.inlineKeyboard([
                    Markup.button.url('Iniciar bot', `https://t.me/${bot.botInfo?.username}?start=`)
                ]))
            })
    }
    else {
        ctx.replyWithMarkdown('_Este comando só pode ser usado em chats privados ou grupos._', Markup.inlineKeyboard([
            Markup.button.url('Iniciar bot', `https://t.me/${bot.botInfo?.username}?start=/me`)
        ]))
    }
});