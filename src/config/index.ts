import dotenv from 'dotenv';

dotenv.config();

export interface IConfig {
  BOT_TOKEN: string;
  ADMIN_CHAT: string;
  ROOTS: string;
  DB_URL: string;
  NANO_WALLET: string;
}

const Config = (): Partial<IConfig> => ({
  BOT_TOKEN: process.env.BOT_TOKEN,
  ADMIN_CHAT: process.env.ADMIN_CHAT,
  ROOTS: process.env.ROOTS,
  DB_URL: process.env.DB_URL,
  NANO_WALLET: process.env.NANO_WALLET,
});

const validateConfig = (config: Partial<IConfig>): IConfig => {
  const requiredConfig = Object.entries(config).filter(([, value]) => !value);

  if (requiredConfig.length) {
    throw new Error(
      `The following required config is missing: ${requiredConfig.map(([key]) => key).join(', ')}`,
    );
  }

  return config as IConfig;
};

const getConfig = (): IConfig => validateConfig(Config());

const config = getConfig();

export default config;
