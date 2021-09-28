const MongoClient = require('mongodb').MongoClient
require('../../.env')

const ConnectDB = async () => {
    const uri = `mongodb://${DB_USER}:${DB_PASS}@${DB_HOST}:${DB_PORT}/?authSource=admin&readPreference=primary&appname=MongoDB%20Compass&ssl=false`
    const client = new MongoClient(uri);
    await client.connect();

    return client.db("portalnano");
}

module.exports = { ConnectDB }