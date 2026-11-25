export async function makeKeys(): Promise<CryptoKeyPair> {
  return window.crypto.subtle.generateKey(
    // ok: mois-2-07-insufficient-key-length-js RSA 2048
    { name: 'RSA-PSS', modulusLength: 2048, publicExponent: new Uint8Array([1, 0, 1]), hash: 'SHA-256' },
    true,
    ['sign', 'verify'],
  );
}
