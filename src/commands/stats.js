const checkRoot = require('../functions/checkRoot');
const bot = require('../helpers/bot')
const { ConnectDB } = require("../database/index")

bot.command('stats', async (ctx) => {
    const db = await ConnectDB()
    const user_id = ctx.from.id

    if (!await checkRoot(user_id)) {
        ctx.replyWithMarkdown("_Você não tem permissão para executar esse comando._", { reply_to_message_id: ctx.message.message_id });
        return;
    }

    const users = await db.collection('users').find({}).toArray();
    const groups = await db.collection('groups').find({}).toArray();

    const usersCount = users.length;
    const groupsCount = groups.length;

    const subscribedUsers = users.filter(user => user.subscription.subscribed).length;
    const subscribedGroups = groups.filter(group => group.subscription.subscribed).length;

    ctx.replyWithMarkdown(`🖥 Estatísticas

*Usuários:* ${usersCount} (*Ativos:* ${subscribedUsers})
*Grupos:* ${groupsCount} (*Ativos:* ${subscribedGroups})`, { reply_to_message_id: ctx.message.message_id })
});