import { createDecipheriv } from 'crypto';

export function decrypt(buf: Buffer, key: Buffer, iv: Buffer, tag: Buffer): Buffer {
  // ok: mois-2-04-weak-cipher-js AES-256-GCM
  const d = createDecipheriv('aes-256-gcm', key, iv, { authTagLength: 16 });
  d.setAuthTag(tag);
  return Buffer.concat([d.update(buf), d.final()]);
}
