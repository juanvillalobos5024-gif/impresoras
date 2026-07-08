const { MongoClient } = require('mongodb');
let attachDatabasePool = null;
try {
  attachDatabasePool = require('@vercel/functions').attachDatabasePool;
} catch (e) {
  // optional on local/dev
}

const uri = process.env.MONGODB_URI;
if (!uri) {
  console.error('MONGODB_URI not set. Set it in Vercel or .env.local');
}

const options = {};

let client;
let clientPromise;

if (process.env.NODE_ENV === 'development') {
  // In development use a global variable so the client is cached across module reloads
  if (!global._mongoClientPromise) {
    client = new MongoClient(uri, options);
    if (attachDatabasePool) {
      try { attachDatabasePool(client); } catch (e) { /* ignore */ }
    }
    global._mongoClientPromise = client.connect();
  }
  clientPromise = global._mongoClientPromise;
} else {
  // In production create a new client per lambda invocation but attach pool helper if available
  client = new MongoClient(uri, options);
  if (attachDatabasePool) {
    try { attachDatabasePool(client); } catch (e) { /* ignore */ }
  }
  clientPromise = client.connect();
}

module.exports = { clientPromise };
