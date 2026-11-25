import Koa from 'koa';
const app = new Koa();
let userId: string | undefined;

app.use(async (ctx, next) => {
  // ruleid: mois-6-01-shared-field-in-singleton-js
  userId = ctx.state.user.id;
  await next();
});
