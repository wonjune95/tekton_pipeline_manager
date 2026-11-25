export function decode(s: string): unknown {
  // ok: mois-5-05-unsafe-deserializer-js JSON
  return JSON.parse(s);
}
