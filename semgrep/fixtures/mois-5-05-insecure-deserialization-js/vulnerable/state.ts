import * as Cryo from 'cryo';
import { Controller, Post, Body } from '@nestjs/common';

@Controller('state')
export class StateController {
  @Post()
  restore(@Body() body: { state: string }) {
    // ruleid: mois-5-05-insecure-deserialization-js
    return Cryo.parse(body.state);
  }
}
