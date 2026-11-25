import { createHash } from 'crypto';

export const hash = (s: string): string =>
  // ok: mois-2-04-weak-hash-js SHA3-256
  createHash('sha3-256').update(s).digest('hex');

export async function fingerprint(buf: ArrayBuffer): Promise<ArrayBuffer> {
  // ok: mois-2-04-weak-hash-js WebCrypto SHA-256
  return crypto.subtle.digest('SHA-256', buf);
}
