const bot = require('../helpers/bot')
const axios = require('axios')

const getNetworkData = async () => {
    const response = await axios.get('https://nanoticker.info/json/stats.json')
    const data = response.data;

    return {
        "cps": Math.round(data.CPSMedian * 100) / 100,
        "bps": Math.round(data.BPSMedian * 100) / 100,
        "blockCount": data.blockCountMedian,
        "cementedCount": data.cementedMedian,
        "cpsMax": Math.round(data.CPSMax * 100) / 100,
        "bpsMax": Math.round(data.BPSMax * 100) / 100,
        "blockCountMax": data.blockCountMax,
        "cementedCountMax": data.cementedMax,
    }
}

bot.command(['network', 'rede'], async (ctx) => {
    let props = ctx.message.text.split(" ")
    const data = await getNetworkData();

    if (props[1] == 'max') {
        ctx.replyWithMarkdown(`
📊 *Estatísticas da rede*

*CPS máximo:* ${data.cpsMax}
*BPS máximo:* ${data.bpsMax}
*Quantidade de blocos:* ${data.blockCountMax}
*Quantidade de blocos confirmados:* ${data.cementedCountMax}
            `)
    }
    else {
        ctx.replyWithMarkdown(`
📊 *Estatísticas da rede*

*CPS médio:* ${data.cps}
*BPS médio:* ${data.bps}
*Quantidade de blocos:* ${data.blockCount}
*Quantidade de blocos confirmados:* ${data.cementedCount}
            `)
    }
});