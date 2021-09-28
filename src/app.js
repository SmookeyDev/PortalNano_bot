const bot = require('./helpers/bot')
const path = require('path')
const fs = require('fs')

fs.readdirSync(path.join(__dirname, 'commands')).forEach(function(file){
    require('./commands/' + file)
})

bot.launch().then(() => {
    console.info(`${bot.botInfo.username} is running.`)
})