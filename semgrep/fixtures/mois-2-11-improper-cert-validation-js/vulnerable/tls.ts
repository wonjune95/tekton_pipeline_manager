import * as nodemailer from 'nodemailer';

export const transport = nodemailer.createTransport({
  host: 'smtp.example.com',
  port: 587,
  // ruleid: mois-2-11-improper-cert-validation-js
  tls: { rejectUnauthorized: false },
});

// ruleid: mois-2-11-improper-cert-validation-js
process.env['NODE_TLS_REJECT_UNAUTHORIZED'] = '0';
