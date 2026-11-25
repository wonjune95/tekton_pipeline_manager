// 안전한 이동 (브라우저) — 탐지되면 안 된다
import { useParams } from "react-router-dom";

export function Article() {
  const { slug } = useParams();
  const edit = () => {
    // ok: mois-1-07-open-redirect-js "/editor/" 로 고정된 상대 경로
    window.location.href = "/editor/" + slug;
  };
  return <button onClick={edit}>edit</button>;
}

export function logout() {
  // ok: mois-1-07-open-redirect-js 고정 주소
  location.assign("/login");
}
