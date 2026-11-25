import { Controller, Get, Injectable, Query, Scope } from '@nestjs/common';

@Injectable({ scope: Scope.REQUEST })
export class RequestContext {
  private user = '';
  set(user: string): void {
    // ok: mois-6-01-shared-field-in-singleton-js 요청마다 새 인스턴스
    this.user = user;
  }
}

@Controller('orders')
export class OrdersController {
  private readonly repo: Repo;
  constructor(repo: Repo) {
    // ok: mois-6-01-shared-field-in-singleton-js 생성자는 한 번만 실행된다
    this.repo = repo;
  }

  @Get()
  find(@Query('id') id: string) {
    // ok: mois-6-01-shared-field-in-singleton-js 지역 변수
    var lastId = id;
    lastId = lastId.trim();
    return this.repo.find(lastId);
  }
}
