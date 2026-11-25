export async function sync(api: Api): Promise<void> {
  try {
    await api.push();
  // ok: mois-4-02-empty-catch-js 다시 던진다
  } catch (e: unknown) {
    throw new Error('push failed', { cause: e });
  }
}
