import mysql from 'mysql2/promise';
import { promises as fsp } from 'fs';

export async function names(): Promise<string[]> {
  // ruleid: mois-5-02-resource-leak-js
  const conn = await mysql.createConnection({ host: 'db' });
  const [rows] = await conn.query('SELECT name FROM t');
  await conn.end();
  return rows as string[];
}

export async function head(file: string): Promise<string> {
  // ruleid: mois-5-02-resource-leak-js
  const fh = await fsp.open(file, 'r');
  const { buffer } = await fh.read(Buffer.alloc(8), 0, 8, 0);
  return buffer.toString();
}
