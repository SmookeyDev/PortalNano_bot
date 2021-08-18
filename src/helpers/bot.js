const {Telegraf} = require('telegraf');
require('../../.env')

const bot = new Telegraf(BOT_TOKEN);

module.exports = bot