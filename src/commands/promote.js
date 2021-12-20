const bot = require('../helpers/bot')
const { ConnectDB } = require('../database/index')
const checkRoot = require('../functions/checkRoot')

bot.command(['promote', 'promover'], async (ctx) => {
    const db = await ConnectDB();
    const user_id = ctx.from.id;

    const props = ctx.message.text.split(' ');

    if (!await checkRoot(user_id)) {
        ctx.replyWithMarkdown("_Você não tem permissão para executar esse comando._", { reply_to_message_id: ctx.message.message_id });
        return;
    }

    const getUsers = (await db.collection('users').find({ 'subscription.subscribed': true }).toArray()).map(user => { return { "id": user.user_id, "type": 'private' } });
    const getGroups = (await db.collection('groups').find({ 'subscription.subscribed': true }).toArray()).map(group => { return { "id": group.chat_id, "type": group.type } });

    const getAll = [...getUsers, ...getGroups];
    for (item of getAll) {
        ctx.telegram.sendMessage(item.id, props[1]).catch(() => {
            if (item.type == 'private') db.collection('users').updateOne({ user_id: item.id }, { $set: { "subscription.subscribed": false } })
            else db.collection('groups').updateOne({ chat_id: item.id }, { $set: { "subscription.subscribed": false } })
        })
    }
    ctx.replyWithMarkdown('_Todos os usuários e grupos foram notificados com sucesso!_', { reply_to_message_id: ctx.message.message_id })
});