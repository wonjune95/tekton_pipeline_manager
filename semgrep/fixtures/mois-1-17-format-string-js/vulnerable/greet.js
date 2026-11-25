// 외부 입력을 sprintf-js 형식 문자열로 사용
const { sprintf, vsprintf: vs } = require('sprintf-js');
const sp = require('sprintf-js');

app.get('/greet', (req, res) => {
  const user = { name: 'kim', password: 'secret' };
  // ruleid: mois-1-17-format-string-js
  res.send(sprintf(req.query.fmt, { user }));
  // ruleid: mois-1-17-format-string-js
  res.send(vs(req.query.fmt, [user.name]));
  // ruleid: mois-1-17-format-string-js
  res.send(sp.sprintf('%s: ' + req.query.tpl, user.name));
});
