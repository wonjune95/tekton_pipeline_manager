// 외부 입력으로 LDAP 필터 · 기준 DN 을 만듦
const ldap = require('ldapjs');
const ldapEscape = require('ldap-escape');
const client = ldap.createClient({ url: 'ldap://ldap.example.com' });

app.post('/login', (req, res) => {
  const uid = req.body.uid;
  // ruleid: mois-1-10-ldap-injection-js
  client.search('ou=people,dc=example,dc=com', { filter: '(uid=' + uid + ')', scope: 'sub' }, (err, r) => res.end());
});

app.get('/group', (req, res) => {
  const filter = `(&(objectClass=group)(cn=${req.query.cn}))`;
  // ruleid: mois-1-10-ldap-injection-js
  client.search('dc=example,dc=com', { filter, scope: 'sub' }, () => res.end());
});

app.get('/ou', (req, res) => {
  const opts = {
    // ruleid: mois-1-10-ldap-injection-js
    filter: '(mail=' + req.query.mail + ')',
    scope: 'sub',
  };
  // ruleid: mois-1-10-ldap-injection-js
  client.search('ou=' + req.query.ou + ',dc=example,dc=com', opts, () => res.end());
});

app.get('/parse', (req, res) => {
  // ruleid: mois-1-10-ldap-injection-js
  const f = ldap.parseFilter(req.query.f);
  res.json(f.toString());
});

// 속이는 예: DN 용 이스케이프를 필터에 씀 (( ) * 를 막지 못한다)
app.get('/dnesc', (req, res) => {
  // ruleid: mois-1-10-ldap-injection-js
  client.search('dc=example,dc=com', { filter: ldapEscape.dn`(uid=${req.query.uid})` }, () => res.end());
});
