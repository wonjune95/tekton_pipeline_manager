// 브라우저에서 같은 서버 API 호출 — 탐지되면 안 된다
import { useParams } from "react-router-dom";

export function Article() {
  const { slug } = useParams();
  // ok: mois-1-12-ssrf-js "/api/" 로 고정된 같은 서버 경로
  fetch(`/api/articles/${slug}`).then((r) => r.json());
  return <div />;
}
