// 이스케이프 · 필터 객체
import ldap from 'ldapjs';
import ldapEscape from 'ldap-escape';
import { Client, EqualityFilter } from 'ldapts';

const client = ldap.createClient({ url: 'ldap://ldap.example.com' });
const ts = new Client({ url: 'ldaps://ldap.example.com' });

export function login(req: any, res: any) {
  // ok: mois-1-10-ldap-injection-js ldap-escape 필터 이스케이프
  client.search('dc=example,dc=com', { filter: ldapEscape.filter`(uid=${req.body.uid})` }, () => res.end());
}

export async function find(req: any) {
  // ok: mois-1-10-ldap-injection-js 필터 객체로 값을 넘긴다
  const filter = new EqualityFilter({ attribute: 'mail', value: req.query.mail });
  return ts.search('dc=example,dc=com', { filter, scope: 'sub' });
}

export async function attrs(req: any) {
  // ok: mois-1-10-ldap-injection-js filter 가 아닌 옵션
  return ts.search('dc=example,dc=com', { filter: '(objectClass=person)', attributes: [req.query.attr] });
}
