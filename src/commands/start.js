const bot = require('../helpers/bot')

bot.start((ctx) => {
    ctx.telegram.sendMessage(ctx.message.chat.id, `Olá ${ctx.message.from.first_name}, obrigado por me iniciar. Ao usar /registrar você irá começar a receber atualizações do nosso portal.`)
});