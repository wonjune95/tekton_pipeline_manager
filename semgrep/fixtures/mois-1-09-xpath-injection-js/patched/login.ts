// 질의문은 상수, 값은 XPath 변수로
import * as xpath from 'xpath';
import { evaluateXPathToNodes } from 'fontoxpath';

export function login(req: any, res: any, doc: Node) {
  // ok: mois-1-09-xpath-injection-js 값은 variables 로 넘긴다
  const nodes = xpath.parse('//user[name=$name]').select({ node: doc, variables: { name: req.body.user } });
  // ok: mois-1-09-xpath-injection-js fontoxpath 변수
  const r = evaluateXPathToNodes('//book[author = $a]', doc, null, { a: req.query.a });
  // ok: mois-1-09-xpath-injection-js 숫자로 바꾼 값
  const n = xpath.select1('//item[' + parseInt(req.query.idx, 10) + ']', doc);
  res.json({ nodes, r, n });
}
