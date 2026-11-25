// 맨 앞을 고정한 주소
import React from 'react';
import { useParams } from 'react-router-dom';

export function Article() {
  const { slug, page } = useParams();
  return (
    <div>
      {/* ok: mois-1-04-xss-url-js 고정 경로로 시작 */}
      <a href={`/articles/${slug}`}>글</a>
      {/* ok: mois-1-04-xss-url-js 고정 스킴 · 호스트로 시작 */}
      <img src={'https://cdn.example.com/img/' + slug} />
      {/* ok: mois-1-04-xss-url-js 쿼리 · 조각으로 시작 */}
      <a href={'?page=' + page}>다음</a>
      <a href={'#' + slug}>여기</a>
      {/* ok: mois-1-04-xss-url-js URL 인코딩하면 : 가 남지 않는다 */}
      <a href={encodeURIComponent(slug)}>상대</a>
    </div>
  );
}

export function dom() {
  const a = document.createElement('a');
  // ok: mois-1-04-xss-url-js 고정 경로로 시작
  a.href = '/search?q=' + encodeURIComponent(location.hash);
  a.setAttribute('href', '/user/' + location.hash.slice(1));
}
