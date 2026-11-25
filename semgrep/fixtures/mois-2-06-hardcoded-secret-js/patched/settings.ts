export class AuthConfig {
  // ok: mois-2-06-hardcoded-secret-js 설정에서 주입
  private clientSecret: string = process.env.CLIENT_SECRET ?? '';

  // ok: mois-2-06-hardcoded-secret-js 저장소 키 이름
  static readonly REFRESH_TOKEN = 'refresh_token';
}

// ok: mois-2-06-hardcoded-secret-js 값이 필드 이름 그 자체
export const body = { privateKey: 'privateKey' };
