function escapeMarkdownV2(text) {
  const specialChars = /[\\`*_{}[\]()#+\-.!]/g;
  return text?.replace(specialChars, '\\$&');
}

export default escapeMarkdownV2;
