import * as fs from 'fs';
import { promises as fsp } from 'fs';

export async function prepare(dir: string): Promise<void> {
  // ruleid: mois-2-03-insecure-permission-js
  await fsp.mkdir(dir, { recursive: true, mode: 0o757 });
  // ruleid: mois-2-03-insecure-permission-js
  fs.appendFileSync(`${dir}/app.log`, 'start\n', { mode: 0o666 });
  // ruleid: mois-2-03-insecure-permission-js
  process.umask(0o000);
}
