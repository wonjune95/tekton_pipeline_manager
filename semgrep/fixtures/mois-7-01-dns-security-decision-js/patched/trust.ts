export function reversed(list: string[]): string[] {
  const out = list.slice();
  // ok: mois-7-01-dns-security-decision-js 배열 reverse 는 DNS 가 아니다
  return out.reverse().filter((x) => x === 'a');
}
