const { clientPromise } = require('../../lib/mongodb');

module.exports = async function handler(req, res) {
  try {
    const client = await clientPromise;
    const db = client.db();
    const items = await db.collection('items').find({}).limit(50).toArray();
    res.status(200).json(items);
  } catch (e) {
    console.error(e);
    res.status(500).json({ error: 'Error connecting to database' });
  }
};
