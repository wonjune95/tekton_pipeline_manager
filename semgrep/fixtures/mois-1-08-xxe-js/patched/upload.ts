// 엔티티 치환 · 외부 DTD 를 끈 파싱
import * as libxmljs from 'libxmljs';
import { XMLParser } from 'fast-xml-parser';
import { ParseOption } from 'libxml2-wasm';

export function parse(data: string) {
  // ok: mois-1-08-xxe-js noent 를 주지 않음 (기본값 false)
  const a = libxmljs.parseXml(data, { noblanks: true });
  // ok: mois-1-08-xxe-js noent: false
  const b = libxmljs.parseXmlString(data, { noent: false, dtdload: false });
  // ok: mois-1-08-xxe-js fast-xml-parser 는 외부 엔티티를 읽지 않는다
  const c = new XMLParser().parse(data);
  // ok: mois-1-08-xxe-js 엔티티 치환이 아닌 옵션
  const d = ParseOption.XML_PARSE_NOBLANKS;
  return [a, b, c, d];
}
