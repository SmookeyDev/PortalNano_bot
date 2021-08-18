const bot = require('./helpers/bot')
require('./commands/start')
require('./commands/help')
require('./commands/cot')
require('./commands/node')
require('./commands/info')
require('./commands/credits')

bot.launch().then(() => {
    console.info(`${bot.botInfo.username} is running.`)
})