// NestJS·Next.js 라우트
import { Controller, Get, Query } from "@nestjs/common";
import axios from "axios";
import { request } from "undici";

@Controller("hooks")
export class HookController {
  @Get("test")
  async test(@Query("endpoint") endpoint: string) {
    // ruleid: mois-1-12-ssrf-js
    return (await axios.post(endpoint, { ping: true })).data;
  }
}

export async function GET(request2: Request, req: any) {
  // ruleid: mois-1-12-ssrf-js
  const r = await request(req.query.u as string);
  return r.body;
}
