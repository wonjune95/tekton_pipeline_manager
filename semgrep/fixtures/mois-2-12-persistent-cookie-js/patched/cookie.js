const session = require('express-session');

app.use(session({
  secret: process.env.SESSION_SECRET,
  // ok: mois-2-12-persistent-cookie-js 30분
  cookie: { httpOnly: true, secure: true, maxAge: 30 * 60 * 1000 },
}));

function login(req, res) {
  // ok: mois-2-12-persistent-cookie-js 1일 (진단가이드: 안전)
  res.cookie('remember', req.user.id, { maxAge: 24 * 60 * 60 * 1000, httpOnly: true });
  // ok: mois-2-12-persistent-cookie-js 세션 쿠키(만료 미지정)
  res.cookie('sid', req.sessionID, { httpOnly: true, secure: true });
  res.end();
}

async function koaLogin(ctx) {
  // ok: mois-2-12-persistent-cookie-js Koa 는 밀리초: 1시간
  ctx.cookies.set('uid', ctx.state.user.id, { maxAge: 3600000 });
}

function fastifyLogin(request, reply) {
  // ok: mois-2-12-persistent-cookie-js Fastify 는 초: 1시간
  reply.setCookie('uid', request.user.id, { maxAge: 3600 });
}

function browser(token) {
  // ok: mois-2-12-persistent-cookie-js 1시간
  document.cookie = 'token=' + token + '; max-age=3600; path=/';
}
