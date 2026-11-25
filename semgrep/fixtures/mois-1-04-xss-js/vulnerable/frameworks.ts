// Koa · Fastify · NestJS · Node http
import Koa from 'koa';
import Fastify from 'fastify';
import DOMPurify from 'dompurify';
import * as http from 'http';
import { Controller, Get, Query } from '@nestjs/common';

const app = new Koa();
app.use(async (ctx) => {
  // ruleid: mois-1-04-xss-js
  ctx.body = '<p>' + ctx.query.name + '</p>';
});

const fastify = Fastify();
fastify.get('/f', async (request, reply) => {
  // ruleid: mois-1-04-xss-js
  reply.type('text/html').send(request.query.q);
});

http.createServer((req, res) => {
  // ruleid: mois-1-04-xss-js
  res.end('<p>' + req.url + '</p>');
});

@Controller('search')
export class SearchController {
  @Get()
  find(@Query('q') q: string) {
    // ruleid: mois-1-04-xss-js
    return `<p>검색어: ${q}</p>`;
  }

  // 속이는 예: DOMPurify 에 옵션을 주면 정화로 인정하지 않는다 (ADD_TAGS 등으로 script 를 허용할 수 있다)
  @Get('opt')
  opt(@Query('q') q: string) {
    // ruleid: mois-1-04-xss-js
    return '<div>' + DOMPurify.sanitize(q, { ADD_TAGS: ['script'] }) + '</div>';
  }
}
