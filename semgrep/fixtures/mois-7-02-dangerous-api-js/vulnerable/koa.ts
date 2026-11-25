import Koa from 'koa';
const app = new Koa();

app.use(async (ctx) => {
  if (ctx.path === '/kill') {
    // ruleid: mois-7-02-dangerous-api-js
    process.kill(process.pid, 'SIGTERM');
  }
});
