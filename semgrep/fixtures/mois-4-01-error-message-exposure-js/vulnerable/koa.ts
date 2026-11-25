import Koa from 'koa';
const app = new Koa();

app.use(async (ctx, next) => {
  try {
    await next();
  } catch (err) {
    ctx.status = 500;
    // ruleid: mois-4-01-error-message-exposure-js
    ctx.body = { message: (err as Error).message };
  }
});
