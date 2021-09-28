const bot = require('../helpers/bot')

bot.command('help', ctx => {
    ctx.telegram.sendMessage(ctx.message.chat.id, `
📲 Lista de Comandos

/start - Inicia o bot.
/info - Mostra informações do portal.
/donate - Mostra uma carteira NANO destinada a receber doações ao portal.
/creditos - Mostra os desenvolvedores do bot e um endereço de doação para apoiar-los.
/registrar - Ativa o recebimento de noticias.
/cancelar - Cancela o recebimento de noticias.
/ultimas - Lista as ultimas 5 noticias lançadas no portal.
/cot - Mostra a atual cotação da NANO.
/sugerir - Possibilita nos sugerir uma nova funcionalidade ou noticia.
/elogiar - Possibilita nos elogiar :)
/ganhar - Recebe uma pequena quantia em nano.
/node - Mostra algumas estátisticas do node NanoBrasil.
/rede - Mostra algumas informações da rede da Nano.
/me - Envia algumas informações sobre o grupo e/ou usuário.
    `)
})