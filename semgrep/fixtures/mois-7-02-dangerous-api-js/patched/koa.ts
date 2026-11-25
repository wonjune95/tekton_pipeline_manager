import Koa from 'koa';
const app = new Koa();

app.use(async (ctx) => {
  // ok: mois-7-02-dangerous-api-js 상태 코드로 응답
  ctx.status = 404;
});
