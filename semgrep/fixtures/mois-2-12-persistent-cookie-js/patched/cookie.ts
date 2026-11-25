import Cookies from 'js-cookie';
import { cookies } from 'next/headers';

export function saveToken(token: string): void {
  // ok: mois-2-12-persistent-cookie-js 세션 쿠키
  Cookies.set('token', token, { secure: true, sameSite: 'strict' });
}

export async function action(token: string) {
  // ok: mois-2-12-persistent-cookie-js Next.js 는 초: 1시간
  cookies().set('session', token, { httpOnly: true, maxAge: 60 * 60 });
}
