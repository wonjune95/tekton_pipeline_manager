// 형식 검사처럼 보이지만 증명하지 못하는 형태 — 모두 탐지되어야 한다
import { exec } from "child_process";

export function notAnchored(req: any, res: any) {
  const name: string = req.params.name;
  if (!/^[a-z]+/.test(name)) return res.sendStatus(400); // 끝($)이 없다
  // ruleid: mois-1-05-os-command-injection-js
  exec("id " + name);
}

export function dotAllowed(req: any, res: any) {
  const name: string = req.params.name;
  if (!/^.+$/.test(name)) return res.sendStatus(400); // 아무 글자나
  // ruleid: mois-1-05-os-command-injection-js
  exec("id " + name);
}

export function spaceAllowed(req: any, res: any) {
  const name: string = req.params.name;
  if (!/^[\w ;]+$/.test(name)) throw new Error("bad"); // 공백·; 허용
  // ruleid: mois-1-05-os-command-injection-js
  exec("id " + name);
}

export function negatedWrapper(req: any, res: any) {
  const name: string = req.params.name;
  if (!(/^[a-z]+$/.test(name) || req.query.skip)) return res.sendStatus(400);
  // ruleid: mois-1-05-os-command-injection-js
  exec("id " + name);
}

export function eqLooseMatch(req: any, res: any) {
  const mode: string = req.query.mode;
  if (mode == "fast") {
    // ruleid: mois-1-05-os-command-injection-js
    exec("run --" + mode);
  }
}

export function useInCondition(req: any, res: any) {
  const mode: string = req.query.mode;
  // ruleid: mois-1-05-os-command-injection-js
  if (exec("x " + mode) && /^[a-z]+$/.test(mode)) {
    res.end();
  }
}
