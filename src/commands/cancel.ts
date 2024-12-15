import { ConnectDB } from '../database/index';
import getAdmins from '../functions/getAdmins';
import bot from '../helpers/bot';
import { Markup } from 'telegraf';

export default bot.command(['cancel', 'cancelar'], async (ctx) => {
  const db = await ConnectDB();
  const chat_type = ctx.chat.type;
  const message_id = ctx.message.message_id;

  if (chat_type == 'private') {
    const checkUser = await db.collection('users').findOne({ user_id: ctx.from.id });
    if (!checkUser) {
      ctx.replyWithMarkdownV2('_Você não está registrado_');
    } else if (checkUser.subscription.subscribed) {
      db.collection('users').updateOne(
        { user_id: ctx.from.id },
        {
          $set: {
            'subscription.subscribed': false,
            'subscription.subscribedAt': new Date(),
          },
        },
      );
      ctx.replyWithMarkdownV2('_Cancelamento efetuado com sucesso_');
    } else {
      ctx.replyWithMarkdownV2('_Você não está registrado_');
    }
  } else if (chat_type == 'group' || chat_type == 'supergroup') {
    const checkAdmin = await getAdmins(ctx.chat.id);
    if (checkAdmin.includes(ctx.from.id)) {
      const checkGroup = await db.collection('groups').findOne({ chat_id: ctx.chat.id });
      if (!checkGroup) {
        ctx.replyWithMarkdownV2('_Você não está registrado_');
      } else if (checkGroup.subscription.subscribed) {
        db.collection('groups').updateOne(
          { chat_id: ctx.chat.id },
          {
            $set: {
              'subscription.subscribed': false,
              'subscription.subscribedAt': new Date(),
            },
          },
        );
        ctx.replyWithMarkdownV2('_Cancelamento efetuado com sucesso_');
      } else {
        ctx.replyWithMarkdownV2('_Você não está registrado_');
      }
    } else {
      ctx.replyWithMarkdownV2(
        '_Você precisa ser administrador do grupo para executar esse comando_',
      );
    }
  } else {
    ctx.replyWithMarkdownV2(
      '_Este comando só pode ser usado em chats privados ou grupos_',
      Markup.inlineKeyboard([
        Markup.button.url('Iniciar bot', `https://t.me/${bot.botInfo?.username}?start=/cancel`),
      ]),
    );
  }
});
