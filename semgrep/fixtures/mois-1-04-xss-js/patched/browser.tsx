// 안전한 화면 출력
import React from 'react';
import DOMPurify from 'dompurify';
import Koa from 'koa';
import { useSearchParams } from 'react-router-dom';

function render() {
  const q = new URLSearchParams(location.search).get('q');
  // ok: mois-1-04-xss-js textContent 는 HTML 로 해석하지 않는다
  document.getElementById('out').textContent = q;
  // ok: mois-1-04-xss-js DOMPurify 기본 설정으로 정화
  document.getElementById('box').innerHTML = DOMPurify.sanitize(location.hash);
  // ok: mois-1-04-xss-js jQuery text() 는 텍스트로 넣는다
  $('#t').text(q);
}

export function Note() {
  const [params] = useSearchParams();
  const note = params.get('note');
  // ok: mois-1-04-xss-js JSX 텍스트는 React 가 이스케이프한다
  return (
    <div>
      <p>{note}</p>
      <div dangerouslySetInnerHTML={{ __html: DOMPurify.sanitize(note) }} />
    </div>
  );
}

const app = new Koa();
app.use(async (ctx) => {
  // ok: mois-1-04-xss-js 객체는 JSON 으로 응답
  ctx.body = { name: ctx.query.name };
});
app.use(async (ctx) => {
  ctx.type = 'text/plain';
  // ok: mois-1-04-xss-js 앞에서 text/plain 으로 지정
  ctx.body = ctx.query.name;
});
