import { promises as fsp } from 'fs';

export async function readConfig(file: string): Promise<string | null> {
  try {
    // ok: mois-3-01-toctou-js 검사 없이 열고 오류로 처리
    return await fsp.readFile(file, 'utf8');
  } catch {
    return null;
  }
}
