import { existsSync, unlinkSync } from 'node:fs';
import * as fse from 'fs-extra';

export function clear(p: string): void {
  if (existsSync(p)) {
    // ruleid: mois-3-01-toctou-js
    unlinkSync(p);
  }
}

export function write(p: string, body: string): void {
  if (!fse.existsSync(p)) {
    // ruleid: mois-3-01-toctou-js
    fse.writeFileSync(p, body);
  }
}

export function mkdirNoRecursive(p: string): void {
  if (!existsSync(p)) {
    // ruleid: mois-3-01-toctou-js
    fse.mkdirSync(p, { mode: 0o700 });
  }
}
