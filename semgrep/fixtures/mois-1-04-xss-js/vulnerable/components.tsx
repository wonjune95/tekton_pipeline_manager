// React · Angular · Handlebars 에서 이스케이프를 끄는 자리
import React from 'react';
import { useParams, useSearchParams } from 'react-router-dom';
import Handlebars from 'handlebars';
import { Component } from '@angular/core';
import { DomSanitizer } from '@angular/platform-browser';

export function Article() {
  const { body } = useParams();
  const [params] = useSearchParams();
  const note = params.get('note');
  return (
    <div>
      {/* ruleid: mois-1-04-xss-js */}
      <div className="a" dangerouslySetInnerHTML={{ __html: body }} />
      {/* ruleid: mois-1-04-xss-js */}
      {React.createElement('p', { dangerouslySetInnerHTML: { __html: note } })}
    </div>
  );
}

export function helper() {
  // ruleid: mois-1-04-xss-js
  return new Handlebars.SafeString('<b>' + location.search + '</b>');
}

@Component({ selector: 'app-search', template: '<div [innerHTML]="html"></div>' })
export class SearchComponent {
  html: any;
  constructor(private sanitizer: DomSanitizer) {
    // ruleid: mois-1-04-xss-js
    this.html = this.sanitizer.bypassSecurityTrustHtml(location.hash);
  }
}
