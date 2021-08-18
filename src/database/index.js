const MongoClient = require('mongodb').MongoClient
require('../../.env')

const uri = `mongodb://${DB_USER}:${DB_PASS}@${DB_HOST}:${DB_PORT}/?authSource=admin&readPreference=primary&appname=MongoDB%20Compass&ssl=false`

const client = new MongoClient(uri);