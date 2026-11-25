// 안전한 형태 (TypeScript) — 탐지되면 안 된다
import { execFileSync } from "child_process";

const MODES = ["fast", "slow"] as const;

export function build(req: any, res: any) {
  const mode: string = req.query.mode;
  if (!Number.isInteger(Number(mode))) return res.sendStatus(400);
  // ok: mois-1-05-os-command-injection-js 셸 없는 execFileSync, 실행 파일 고정
  execFileSync("make", ["build", "MODE=" + mode]);
  // ok: mois-1-05-os-command-injection-js 명령 문자열이 고정
  execFileSync("make", ["clean"]);
  res.end();
}

export function local(cmd: string) {
  const { execSync } = require("child_process");
  // ok: mois-1-05-os-command-injection-js 외부 입력이 아닌 함수 인자
  return execSync(cmd).toString();
}
