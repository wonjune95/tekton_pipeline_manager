import { promises as dnsPromises } from 'dns';

const TRUSTED = ['gw.example.com'];

export async function allowed(ip: string): Promise<boolean> {
  const hosts = await dnsPromises.reverse(ip);
  // ruleid: mois-7-01-dns-security-decision-js
  return TRUSTED.includes(hosts[0]);
}
