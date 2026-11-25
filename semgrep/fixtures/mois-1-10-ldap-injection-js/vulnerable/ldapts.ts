// ldapts
import { Client } from 'ldapts';
import { Body, Controller, Post } from '@nestjs/common';

@Controller('auth')
export class AuthController {
  private client = new Client({ url: 'ldaps://ldap.example.com' });

  @Post()
  async login(@Body('user') user: string) {
    // ruleid: mois-1-10-ldap-injection-js
    const { searchEntries } = await this.client.search('dc=example,dc=com', { scope: 'sub', filter: `(uid=${user})` });
    return searchEntries.length > 0;
  }
}
