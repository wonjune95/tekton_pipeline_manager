import CryptoJS from 'crypto-js';

export class AuthConfig {
  // ruleid: mois-2-06-hardcoded-secret-js
  private clientSecret: string = 'c1ient-s3cret';

  constructor() {
    // ruleid: mois-2-06-hardcoded-secret-js
    this.accessToken = 'ghp_abcdefABCDEF1234567890';
  }

  encrypt(data: string): string {
    // ruleid: mois-2-06-hardcoded-secret-js
    return CryptoJS.AES.encrypt(data, 'front-end-key-1').toString();
  }
}

// ruleid: mois-2-06-hardcoded-secret-js
export const ADMIN_PWD = process.env['ADMIN_PWD'] ?? 'changeme1';
