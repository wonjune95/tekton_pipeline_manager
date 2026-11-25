// CSRF 보호를 켠 설정
import csurf from 'csurf';
import express from 'express';
import { HttpClientXsrfModule, provideHttpClient, withXsrfConfiguration } from '@angular/common/http';

const app = express();
// ok: mois-1-11-csrf-js 기본 ignoreMethods (GET · HEAD · OPTIONS)
app.use(csurf({ cookie: true, ignoreMethods: ['GET', 'HEAD', 'OPTIONS'] }));

export const imports = [
  // ok: mois-1-11-csrf-js 쿠키 · 헤더 이름만 바꾼다
  HttpClientXsrfModule.withOptions({ cookieName: 'XSRF', headerName: 'X-XSRF' }),
];
export const providers = [provideHttpClient(withXsrfConfiguration({ cookieName: 'XSRF' }))];
