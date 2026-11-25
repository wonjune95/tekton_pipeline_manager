import * as jose from 'jose';

export async function claims(token: string, key: Uint8Array) {
  // ok: mois-2-10-improper-signature-verification-js 서명 검증
  const { payload } = await jose.jwtVerify(token, key, { algorithms: ['HS256'] });
  return payload;
}
