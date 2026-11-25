import { createCipheriv, createDecipheriv } from 'crypto';

export function legacyDecrypt(buf: Buffer, key: Buffer, iv: Buffer): Buffer {
  // ruleid: mois-2-04-weak-cipher-js
  const d = createDecipheriv('des-ede3', key, iv);
  return Buffer.concat([d.update(buf), d.final()]);
}

export function seedEcb(buf: Buffer, key: Buffer): Buffer {
  // ruleid: mois-2-04-weak-cipher-js
  const c = createCipheriv('seed-ecb', key, null);
  return c.update(buf);
}
