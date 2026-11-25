import Koa from 'koa';
const app = new Koa();

app.use(async (ctx, next) => {
  // ok: mois-6-01-shared-field-in-singleton-js 요청 범위 state
  ctx.state.userId = ctx.state.user.id;
  await next();
});
