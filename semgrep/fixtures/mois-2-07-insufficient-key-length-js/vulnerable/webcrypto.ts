export async function makeKeys(): Promise<CryptoKeyPair> {
  return window.crypto.subtle.generateKey(
    {
      name: 'RSA-OAEP',
      // ruleid: mois-2-07-insufficient-key-length-js
      modulusLength: 1024,
      publicExponent: new Uint8Array([1, 0, 1]),
      hash: 'SHA-256',
    },
    true,
    ['encrypt', 'decrypt'],
  );
}

export function ecKey() {
  // ruleid: mois-2-07-insufficient-key-length-js
  return require('crypto').generateKeyPairSync('ec', { namedCurve: 'P-192' });
}
