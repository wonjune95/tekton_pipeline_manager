import { rename } from 'fs';

export function move(a: string, b: string): void {
  // ruleid: mois-4-03-improper-exception-handling-js
  rename(a, b, () => console.log('moved'));
}
