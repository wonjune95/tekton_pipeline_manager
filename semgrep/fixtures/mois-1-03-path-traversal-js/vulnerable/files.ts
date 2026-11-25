// ES 모듈 import 형태와 NestJS
import { readFileSync } from "fs";
import * as fse from "fs-extra";
import { Controller, Get, Param } from "@nestjs/common";

@Controller("docs")
export class DocsController {
  @Get(":name")
  get(@Param("name") name: string) {
    // ruleid: mois-1-03-path-traversal-js
    return readFileSync("/srv/docs/" + name, "utf8");
  }
}

export async function remove(ctx: any) {
  // ruleid: mois-1-03-path-traversal-js
  await fse.remove(ctx.params.dir);
}
