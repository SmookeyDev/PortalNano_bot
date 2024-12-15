import bot from '../helpers/bot';

export default bot.command(['credits', 'creditos'], (ctx) => {
  const message = `
🖥 *Creditos*
  
*Desenvolvedor:* @SmookeyDev
*Contribuidores:* @AT35000, @igorcmelo e @JgBr123
      
*Endereço para nos apoiar:* \`nano_1qecfwuccd79n7q8sbbza7pyrtq1njxfigbouniuiooez9iaemjoresz78ic\`
`;

  ctx.reply(message, { parse_mode: 'MarkdownV2' });
});
