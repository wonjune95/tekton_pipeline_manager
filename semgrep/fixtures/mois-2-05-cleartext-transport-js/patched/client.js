const axios = require('axios');

async function send(user, port) {
  // ok: mois-2-05-cleartext-transport-js https
  await fetch('https://api.example.com/login', { method: 'POST', body: JSON.stringify(user) });
  // ok: mois-2-05-cleartext-transport-js 같은 호스트(개발 서버)
  await axios.get('http://localhost:3000/api/users');
  // ok: mois-2-05-cleartext-transport-js 같은 호스트, 포트는 변수
  await fetch(`http://127.0.0.1:${port}/health`);
  // ok: mois-2-05-cleartext-transport-js 상대 경로 (페이지와 같은 프로토콜)
  await axios.post('/api/users', user);
  const api = axios.create({
    // ok: mois-2-05-cleartext-transport-js https
    baseURL: 'https://api.example.com',
  });
  // ok: mois-2-05-cleartext-transport-js wss
  const ws = new WebSocket('wss://chat.example.com/socket');
  return [api, ws];
}
