const bot = require("../helpers/bot")

const getAdmins = async (chat_id) => {
    const getChatAdmins = await bot.telegram.getChatAdministrators(chat_id);
    const AdminList = getChatAdmins.map(admin => admin.user.id);
    return AdminList;
}

module.exports = getAdmins