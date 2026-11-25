const crypto = require('crypto');
const jwt = require('jsonwebtoken');
const session = require('express-session');
const mysql = require('mysql');

// ruleid: mois-2-06-hardcoded-secret-js
const DB_PASSWORD = 'P@ssw0rd!';
// ruleid: mois-2-06-hardcoded-secret-js
let apiKey = 'AKIA1234567890ABCDEF';

const pool = mysql.createPool({
  host: 'db.internal',
  user: 'app',
  // ruleid: mois-2-06-hardcoded-secret-js
  password: 'app1234!',
});

app.use(session({
  // ruleid: mois-2-06-hardcoded-secret-js
  secret: 'keyboard-cat',
  resave: false,
}));

module.exports = {
  // ruleid: mois-2-06-hardcoded-secret-js
  'api_key': 'sk_live_51H8xYz',
  // ruleid: mois-2-06-hardcoded-secret-js
  jwtSecret: process.env.JWT_SECRET || 'superSecret',
};

function issue(user) {
  // ruleid: mois-2-06-hardcoded-secret-js
  return jwt.sign({ id: user.id }, 'my-jwt-signing-key', { expiresIn: '1h' });
}

function check(token) {
  // ruleid: mois-2-06-hardcoded-secret-js
  return jwt.verify(token, 'my-jwt-signing-key');
}

// ruleid: mois-2-06-hardcoded-secret-js
const hmac = (data) => crypto.createHmac('sha256', 'pa4qacea4VK9t9nGv7yZtwmj').update(data).digest('hex');

function encrypt(text, iv) {
  // ruleid: mois-2-06-hardcoded-secret-js
  const c = crypto.createCipheriv('aes-128-gcm', '0123456789abcdef', iv);
  return c.update(text);
}

function login(req, res) {
  // ruleid: mois-2-06-hardcoded-secret-js
  if (req.body.password === 'admin123') {
    return res.send('ok');
  }
}

// ruleid: mois-2-06-hardcoded-secret-js
const MONGO_URL = 'mongodb://admin:s3cret@mongo.internal:27017/app';
