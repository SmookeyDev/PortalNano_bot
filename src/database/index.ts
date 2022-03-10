import { MongoClient } from "mongodb";

let client: MongoClient;

const ConnectDB = async () => {
    if (!client) {
        client = await MongoClient.connect(`mongodb://${process.env.DB_USER}:${process.env.DB_PASS}@${process.env.DB_HOST}:${process.env.DB_PORT}/?authSource=admin&readPreference=primary&appname=MongoDB%20Compass&ssl=false` || "");
    }
    return client.db(process.env.DB_NAME || "");
}

export { ConnectDB };