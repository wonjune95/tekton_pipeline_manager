import { Controller, Get, Injectable, Query } from '@nestjs/common';

@Injectable()
export class CartService {
  private items: string[] = [];
  private owner = '';

  add(user: string, item: string): void {
    // ruleid: mois-6-01-shared-field-in-singleton-js
    this.owner = user;
    this.items.push(item);
  }
}

@Controller('orders')
export class OrdersController {
  private lastId = '';
  constructor(private readonly cart: CartService) {}

  @Get()
  find(@Query('id') id: string) {
    // ruleid: mois-6-01-shared-field-in-singleton-js
    this.lastId = id;
    return this.lastId;
  }
}
