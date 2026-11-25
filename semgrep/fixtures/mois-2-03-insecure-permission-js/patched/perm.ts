import { promises as fsp } from 'fs';

export async function writeKey(path: string, pem: string): Promise<void> {
  // ok: mois-2-03-insecure-permission-js 키 파일은 소유자만 읽기·쓰기
  await fsp.writeFile(path, pem, { mode: 0o600 });
}
