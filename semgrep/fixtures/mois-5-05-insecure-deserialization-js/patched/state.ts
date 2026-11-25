import { Controller, Post, Body } from '@nestjs/common';
import { parse } from './state-parser';

@Controller('state')
export class StateController {
  @Post()
  restore(@Body() body: { state: string }) {
    // ok: mois-5-05-insecure-deserialization-js 직접 만든 parse(라이브러리 아님)
    return parse(body.state);
  }
}
