const bot = require('../helpers/bot');
const axios = require('axios');
const { xml2json } = require("xml-js");

const getNews = async () => {
    const response = await axios.get('https://portalnano.com.br/blog/feed/')
    const data = response.data;
    const xmljson = JSON.parse(xml2json(data, { compact: true, spaces: 2 }));
    const filteredData = xmljson.rss.channel.item.map((data) => {
        return {
            title: data.title._text,
            link: data.link._text,
        }
    })
    return filteredData
};

bot.command(['last', 'ultimas'], async (ctx) => {
    const news = await getNews();
    const message = "*📰 Últimas notícias*\n\n" + news.map((data, index) => { return `${index + 1} - [${data.title}](${data.link})` }).join("\n")
    ctx.replyWithMarkdown(message, { disable_web_page_preview: true })
});