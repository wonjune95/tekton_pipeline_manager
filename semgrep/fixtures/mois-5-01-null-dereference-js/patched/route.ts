export function idOf(path: string): number {
  const found = /\/items\/(\d+)/.exec(path);
  if (found === null) {
    throw new Error('bad path');
  }
  // ok: mois-5-01-null-dereference-js null 이면 던졌다
  return parseInt(found[1], 10);
}
