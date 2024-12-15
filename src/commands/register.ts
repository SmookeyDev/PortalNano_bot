import { Markup } from 'telegraf';
import { ConnectDB } from '../database/index';
import getAdmins from '../functions/getAdmins';
import bot from '../helpers/bot';

export default bot.command(['register', 'registrar'], async (ctx) => {
  const db = await ConnectDB();

  if (ctx.chat.type == 'private') {
    const checkUser = await db.collection('users').findOne({ user_id: ctx.from.id });
    if (!checkUser) {
      db.collection('users').insertOne({
        user_id: ctx.from.id,
        subscription: { subscribed: true, subscribedAt: new Date() },
        createdAt: new Date(),
      });
      ctx.replyWithMarkdownV2('_Registro efetuado com sucesso_');
    } else if (!checkUser.subscription.subscribed) {
      db.collection('users').updateOne(
        { user_id: ctx.from.id },
        {
          $set: {
            'subscription.subscribed': true,
            'subscription.subscribedAt': new Date(),
          },
        },
      );
      ctx.replyWithMarkdownV2('_Registro efetuado com sucesso_');
    } else {
      ctx.replyWithMarkdownV2('_Você já se encontra registrado_');
    }
  } else if (ctx.chat.type == 'group' || ctx.chat.type == 'supergroup') {
    const admins = await getAdmins(ctx.chat.id);
    if (admins.includes(ctx.from.id)) {
      const checkGroup = await db.collection('groups').findOne({ chat_id: ctx.chat.id });
      if (!checkGroup) {
        db.collection('groups').insertOne({
          chat_id: ctx.chat.id,
          type: ctx.chat.type,
          subscription: { subscribed: true, subscribedAt: new Date() },
          createdAt: new Date(),
        });
        ctx.replyWithMarkdownV2('_Registro efetuado com sucesso_');
      } else if (!checkGroup.subscription.subscribed) {
        db.collection('groups').updateOne(
          { chat_id: ctx.chat.id },
          {
            $set: {
              'subscription.subscribed': true,
              'subscription.subscribedAt': new Date(),
            },
          },
        );
        ctx.replyWithMarkdownV2('_Registro efetuado com sucesso_');
      } else {
        ctx.replyWithMarkdownV2('_Esse grupo já se encontra registrado_');
      }
    } else {
      ctx.replyWithMarkdownV2(
        `_Você precisa ser administrador do grupo para executar esse comando_`,
      );
    }
  } else {
    ctx.replyWithMarkdownV2(
      '_Este comando só pode ser usado em chats privados ou grupos_',
      Markup.inlineKeyboard([
        Markup.button.url('Iniciar bot', `https://t.me/${bot.botInfo?.username}?start=/register`),
      ]),
    );
  }
});
