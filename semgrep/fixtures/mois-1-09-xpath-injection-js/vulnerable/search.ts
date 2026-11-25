// 브라우저 · fontoxpath
import { evaluateXPathToNodes } from 'fontoxpath';

export function find(xmlDoc: Document) {
  const q = new URLSearchParams(location.search).get('q');
  // ruleid: mois-1-09-xpath-injection-js
  const r = document.evaluate("//book[title='" + q + "']", xmlDoc, null, XPathResult.ANY_TYPE, null);
  // ruleid: mois-1-09-xpath-injection-js
  const r2 = xmlDoc.evaluate('//book[@id=' + location.hash.slice(1) + ']', xmlDoc, null, 0, null);
  // ruleid: mois-1-09-xpath-injection-js
  const r3 = evaluateXPathToNodes('//book[author = "' + q + '"]', xmlDoc);
  return [r, r2, r3];
}
