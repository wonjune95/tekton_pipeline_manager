import serializeToJs from 'serialize-to-js';

export function decode(s: string): unknown {
  // ruleid: mois-5-05-unsafe-deserializer-js
  return serializeToJs.deserialize(s);
}
