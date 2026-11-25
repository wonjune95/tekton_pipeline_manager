import { createHash } from 'crypto';

export const hash = (s: string): string =>
  // ruleid: mois-2-04-weak-hash-js
  createHash('md5').update(s).digest('hex');

export async function fingerprint(buf: ArrayBuffer): Promise<ArrayBuffer> {
  // ruleid: mois-2-04-weak-hash-js
  return window.crypto.subtle.digest('SHA-1', buf);
}
