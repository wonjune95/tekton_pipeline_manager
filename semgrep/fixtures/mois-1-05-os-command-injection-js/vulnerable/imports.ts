// ES 모듈 import 형태와 Koa·NestJS 입력
import { execSync } from "child_process";
import * as child from "node:child_process";
import { exec as run } from "child_process";
import { Controller, Get, Query } from "@nestjs/common";

export async function koaHandler(ctx: any) {
  const file = ctx.query.file as string;
  // ruleid: mois-1-05-os-command-injection-js
  execSync(`cat ${file}`);
  // ruleid: mois-1-05-os-command-injection-js
  child.exec("convert " + ctx.request.body.src + " out.png");
  // ruleid: mois-1-05-os-command-injection-js
  run(ctx.headers["x-cmd"] as string);
}

@Controller("tools")
export class ToolsController {
  @Get("zip")
  zip(@Query("name") name: string) {
    // ruleid: mois-1-05-os-command-injection-js
    return execSync("zip -r out.zip " + name).toString();
  }
}
