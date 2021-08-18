const bot = require('../helpers/bot')

bot.command('creditos', ctx => {
    ctx.replyWithMarkdown(`
🖥 *Creditos*

*Desenvolvedor:* @SmookeyDev
*Contribuidores:* @AT35000, @igorcmelo e @JgBr123.
    
*Endereço para me apoiar:*` + '```nano_1qecfwuccd79n7q8sbbza7pyrtq1njxfigbouniuiooez9iaemjoresz78ic```')
})