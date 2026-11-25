// pug·handlebars 템플릿 원문과 브라우저 입력
import pug from "pug";
import * as Handlebars from "handlebars";

export function preview(ctx: any) {
  // ruleid: mois-1-02-code-injection-js
  ctx.body = pug.render(ctx.request.body.source);
  // ruleid: mois-1-02-code-injection-js
  const tpl = Handlebars.compile(ctx.query.layout as string);
  return tpl({});
}

export function widget() {
  const code = decodeURIComponent(location.hash.slice(1));
  // ruleid: mois-1-02-code-injection-js
  window.setTimeout(code, 0);
}
