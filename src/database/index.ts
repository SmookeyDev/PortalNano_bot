import { MongoClient } from "mongodb";

let client: MongoClient;

const ConnectDB = async () => {
    if (!client) {
        client = await MongoClient.connect(process.env.DB_URL || "");
    }
    return client.db(process.env.DB_NAME || "");
}

export { ConnectDB };