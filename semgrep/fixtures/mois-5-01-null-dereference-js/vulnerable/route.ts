export function idOf(path: string): number {
  const re = /\/items\/(\d+)/;
  const found = re.exec(path);
  // ruleid: mois-5-01-null-dereference-js
  return parseInt(found[1], 10);
}
