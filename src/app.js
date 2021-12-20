const bot = require('./helpers/bot');
const path = require('path');
const moment = require('moment');
const fs = require('fs');

fs.readdirSync(path.join(__dirname, 'commands')).forEach(function (file) {
    require('./commands/' + file)
});

bot.on('message', (ctx) => {
    const username = ctx.message.from.username != undefined ? ctx.message.from.username : ctx.message.from.first_name
    console.log(`[${moment().format('DD/MM/YYYY HH:mm:ss')}] ${username} - ${ctx.message.text} (${ctx.message.from.id})`)
});

bot.launch().then(() => {
    console.info(`${bot.botInfo.username} is running.\n`)
});