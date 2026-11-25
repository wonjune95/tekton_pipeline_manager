const session = require('express-session');
const cookieSession = require('cookie-session');

app.use(session({
  secret: process.env.SESSION_SECRET,
  // ruleid: mois-2-12-persistent-cookie-js
  cookie: { httpOnly: true, maxAge: 1000 * 60 * 60 * 24 * 30 },
}));

app.use(cookieSession({
  name: 'sess',
  keys: [process.env.KEY1],
  // ruleid: mois-2-12-persistent-cookie-js
  maxAge: 7 * 24 * 60 * 60 * 1000,
}));

function remember(req, res) {
  // ruleid: mois-2-12-persistent-cookie-js
  res.cookie('remember', req.user.id, { maxAge: 365 * 24 * 60 * 60 * 1000, httpOnly: true });
  // ruleid: mois-2-12-persistent-cookie-js
  res.cookie('token', req.user.token, { expires: new Date(Date.now() + 30 * 86400000) });
  // ruleid: mois-2-12-persistent-cookie-js
  req.session.cookie.maxAge = 14 * 24 * 3600 * 1000;
  res.end();
}

async function koaLogin(ctx) {
  // ruleid: mois-2-12-persistent-cookie-js
  ctx.cookies.set('uid', ctx.state.user.id, { maxAge: 2 * 86400000 });
}

function fastifyLogin(request, reply) {
  // ruleid: mois-2-12-persistent-cookie-js
  reply.setCookie('uid', request.user.id, { maxAge: 60 * 60 * 24 * 7 });
}

function browser(token) {
  // ruleid: mois-2-12-persistent-cookie-js
  document.cookie = 'token=' + token + '; max-age=31536000; path=/';
}

function rememberMe(req) {
  // ruleid: mois-2-12-persistent-cookie-js
  req.sessionOptions.maxAge = 30 * 24 * 60 * 60 * 1000;
}
