// libxmljs2 기본 import · libxml2-wasm 옵션
import libxml from 'libxmljs2';
import { ParseOption } from 'libxml2-wasm';

export function parse(data: string) {
  // ruleid: mois-1-08-xxe-js
  return libxml.parseXml(data, { noblanks: true, 'noent': true, nocdata: true });
}

export async function parseWasm(libxml2: any, data: string) {
  // ruleid: mois-1-08-xxe-js
  const option = libxml2.ParseOption.XML_PARSE_NOENT | libxml2.ParseOption.XML_PARSE_NOBLANKS;
  // ruleid: mois-1-08-xxe-js
  const flags = ParseOption.XML_PARSE_DTDLOAD;
  return libxml2.XmlDocument.fromString(data, { option: option | flags });
}
