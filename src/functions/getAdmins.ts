import bot from '../helpers/bot';

const getAdmins = async (chat_id: number) => {
  const getChatAdmins = await bot.telegram.getChatAdministrators(chat_id);
  const AdminList = getChatAdmins.map((admin) => admin.user.id);
  return AdminList;
};

export default getAdmins;
