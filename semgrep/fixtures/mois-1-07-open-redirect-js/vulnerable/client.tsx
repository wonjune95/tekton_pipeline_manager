// 신뢰되지 않는 URL 로 자동 이동 — 브라우저·Next.js
import { redirect } from "next/navigation";
import { NextResponse } from "next/server";
import { useSearchParams } from "react-router-dom";

export function LoginDone() {
  const [params] = useSearchParams();
  const target = params.get("next");
  const go = () => {
    // ruleid: mois-1-07-open-redirect-js
    window.location.href = target;
  };
  return <button onClick={go}>continue</button>;
}

export function legacy() {
  const hash = location.hash.substring(1);
  // ruleid: mois-1-07-open-redirect-js
  location.replace(hash);
  // ruleid: mois-1-07-open-redirect-js
  window.open(document.referrer);
}

export async function GET(request: Request) {
  const to = new URL(request.url).searchParams.get("to");
  // ruleid: mois-1-07-open-redirect-js
  return NextResponse.redirect(new URL(to, request.url));
}

export default async function Page({ searchParams }: any) {
  const u = useSearchParams().get("u");
  // ruleid: mois-1-07-open-redirect-js
  redirect(u);
}
