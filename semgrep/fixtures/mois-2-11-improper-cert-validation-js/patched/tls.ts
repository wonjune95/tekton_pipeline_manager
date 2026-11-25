import * as nodemailer from 'nodemailer';

export const transport = nodemailer.createTransport({
  host: 'smtp.example.com',
  port: 587,
  // ok: mois-2-11-improper-cert-validation-js 최소 TLS 버전만 지정, 검증은 기본값
  tls: { minVersion: 'TLSv1.2' },
});
