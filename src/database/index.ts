import { MongoClient } from 'mongodb';
import config from '../config';

let client: MongoClient;

const ConnectDB = async () => {
  if (!client) {
    client = await MongoClient.connect(config.DB_URL || '');
  }
  return client.db();
};

export { ConnectDB };
