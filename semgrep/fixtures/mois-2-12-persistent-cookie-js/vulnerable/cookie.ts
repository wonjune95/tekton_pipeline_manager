import Cookies from 'js-cookie';
import { cookies } from 'next/headers';
import { NextResponse } from 'next/server';

export function saveToken(token: string): void {
  // ruleid: mois-2-12-persistent-cookie-js
  Cookies.set('token', token, { expires: 7 });
}

export async function action(token: string) {
  // ruleid: mois-2-12-persistent-cookie-js
  cookies().set('session', token, { httpOnly: true, maxAge: 60 * 60 * 24 * 30 });
}

export function middleware(token: string) {
  const response = NextResponse.next();
  // ruleid: mois-2-12-persistent-cookie-js
  response.cookies.set('session', token, { maxAge: 31536000 });
  return response;
}
