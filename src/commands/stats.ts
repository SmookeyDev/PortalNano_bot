import checkRoot from '../functions/checkRoot';
import bot from '../helpers/bot';
import { ConnectDB } from '../database/index';

export default bot.command('stats', async (ctx) => {
  const db = await ConnectDB();
  const user_id = ctx.from.id;

  if (!(await checkRoot(user_id))) {
    ctx.replyWithMarkdownV2('_Você não tem permissão para executar esse comando_');
    return;
  }

  const users = await db.collection('users').find({}).toArray();
  const groups = await db.collection('groups').find({}).toArray();

  const usersCount = users.length;
  const groupsCount = groups.length;

  const subscribedUsers = users.filter((user) => user.subscription.subscribed).length;
  const subscribedGroups = groups.filter((group) => group.subscription.subscribed).length;

  ctx.replyWithMarkdownV2(`🖥 Estatísticas

*Usuários:* ${usersCount} \\(*Ativos:* ${subscribedUsers}\\)
*Grupos:* ${groupsCount} \\(*Ativos:* ${subscribedGroups}\\)`);
});
