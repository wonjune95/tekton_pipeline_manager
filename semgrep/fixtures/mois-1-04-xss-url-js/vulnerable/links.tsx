// 외부 입력을 링크 · 스크립트 주소로 사용
import React from 'react';
import { useSearchParams, useParams } from 'react-router-dom';
import DOMPurify from 'dompurify';
import escapeHtml from 'escape-html';
import { DomSanitizer } from '@angular/platform-browser';

export function Profile() {
  const [params] = useSearchParams();
  const site = params.get('site');
  const { img } = useParams();
  return (
    <div>
      {/* ruleid: mois-1-04-xss-url-js */}
      <a className="link" href={site}>홈페이지</a>
      {/* ruleid: mois-1-04-xss-url-js */}
      <iframe src={img} />
      {/* 속이는 예: DOMPurify · 이스케이프는 javascript: 를 지우지 않는다 */}
      {/* ruleid: mois-1-04-xss-url-js */}
      <a href={DOMPurify.sanitize(site)}>a</a>
      {/* ruleid: mois-1-04-xss-url-js */}
      <form action={escapeHtml(site)} />
      {/* 속이는 예: 맨 앞 리터럴이 스킴을 정하지 못함 ("java" + "script:…") */}
      {/* ruleid: mois-1-04-xss-url-js */}
      <a href={'java' + site}>b</a>
      {/* ruleid: mois-1-04-xss-url-js */}
      <a href={`${site}/about`}>c</a>
    </div>
  );
}

export function dom() {
  const target = new URLSearchParams(location.search).get('next');
  const a = document.createElement('a');
  // ruleid: mois-1-04-xss-url-js
  a.href = target;
  const s = document.createElement('script');
  // ruleid: mois-1-04-xss-url-js
  s.src = location.hash.substring(1);
  // ruleid: mois-1-04-xss-url-js
  a.setAttribute('href', target);
}

export class Viewer {
  url: any;
  constructor(private sanitizer: DomSanitizer) {
    // ruleid: mois-1-04-xss-url-js
    this.url = this.sanitizer.bypassSecurityTrustResourceUrl(location.hash);
  }
}
