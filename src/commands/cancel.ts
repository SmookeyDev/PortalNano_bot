import { ConnectDB } from "../database/index";
import getAdmins from "../functions/getAdmins";
import bot from '../helpers/bot'
import { Markup } from 'telegraf';


export default bot.command(['cancel', 'cancelar'], async (ctx) => {
    const db = await ConnectDB();
    const chat_type = ctx.chat.type;
    const message_id = ctx.message.message_id;

    if (chat_type == "private") {
        const checkUser = await db.collection("users").findOne({ "user_id": ctx.from.id });
        if (!checkUser) {
            ctx.replyWithMarkdown("_Você não está registrado._", { reply_to_message_id: message_id });
        }
        else if (checkUser.subscription.subscribed) {
            db.collection("users").updateOne({ "user_id": ctx.from.id }, { $set: { "subscription.subscribed": false, "subscription.subscribedAt": new Date() } });
            ctx.replyWithMarkdown("_Cancelamento efetuado com sucesso._", { reply_to_message_id: message_id });
        }
        else {
            ctx.replyWithMarkdown("_Você não está registrado._", { reply_to_message_id: message_id });
        }
    }
    else if (chat_type == "group" || chat_type == "supergroup") {
        const checkAdmin = await getAdmins(ctx.chat.id);
        if (checkAdmin.includes(ctx.from.id)) {
            const checkGroup = await db.collection("groups").findOne({ "chat_id": ctx.chat.id })
            if (!checkGroup) {
                ctx.replyWithMarkdown("_Você não está registrado._", { reply_to_message_id: message_id });
            }
            else if (checkGroup.subscription.subscribed) {
                db.collection("groups").updateOne({ "chat_id": ctx.chat.id }, { $set: { "subscription.subscribed": false, "subscription.subscribedAt": new Date() } })
                ctx.replyWithMarkdown("_Cancelamento efetuado com sucesso._", { reply_to_message_id: message_id });
            }
            else {
                ctx.replyWithMarkdown("_Você não está registrado._", { reply_to_message_id: message_id });
            }
        }
        else {
            ctx.replyWithMarkdown("_Você precisa ser administrador do grupo para executar esse comando._", { reply_to_message_id: message_id });
        }
    }
    else {
        ctx.replyWithMarkdown('_Este comando só pode ser usado em chats privados ou grupos._', Markup.inlineKeyboard([
            Markup.button.url('Iniciar bot', `https://t.me/${bot.botInfo?.username}?start=/cancel`)
        ]))
    }

});