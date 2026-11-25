import mysql from 'mysql2/promise';

export async function names(): Promise<string[]> {
  // ok: mois-5-02-resource-leak-js finally 에서 end()
  const conn = await mysql.createConnection({ host: 'db' });
  try {
    const [rows] = await conn.query('SELECT name FROM t');
    return rows as string[];
  } finally {
    await conn.end();
  }
}
