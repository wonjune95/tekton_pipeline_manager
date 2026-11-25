import * as jose from 'jose';

export function claims(token: string) {
  // ruleid: mois-2-10-improper-signature-verification-js
  const { payload } = jose.UnsecuredJWT.decode(token);
  return payload;
}

import { UnsecuredJWT } from 'jose';

export function claims2(token: string) {
  // ruleid: mois-2-10-improper-signature-verification-js
  return UnsecuredJWT.decode(token).payload;
}
