export async function sync(api: Api): Promise<void> {
  // ruleid: mois-4-02-empty-catch-js
  try {
    await api.push();
  } catch (e: unknown) {
  }
}
