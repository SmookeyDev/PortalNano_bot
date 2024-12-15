import { Telegraf } from 'telegraf';
import config from '../config';

const bot = new Telegraf(config.BOT_TOKEN || '');

export default bot;
