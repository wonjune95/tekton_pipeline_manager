import { promises as fsp } from 'fs';

export async function move(a: string, b: string): Promise<void> {
  // ok: mois-4-03-improper-exception-handling-js 실패하면 예외가 난다
  await fsp.rename(a, b);
}
