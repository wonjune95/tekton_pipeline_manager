// 검증처럼 보이지만 증명하지 못하는 형태 — 모두 탐지되어야 한다
const { exec } = require("child_process");
const ALLOWED = ["status", "uptime"];
const CHANGED = ["a", "b"];
CHANGED.push("rm -rf /");
let LOOSE = ["a"];

function discarded(req, res) {
  const c = req.query.c;
  ALLOWED.includes(c); // 결과를 버림
  // ruleid: mois-1-05-os-command-injection-js
  exec(c);
}

function continues(req, res) {
  const c = req.query.c;
  if (!ALLOWED.includes(c)) {
    console.warn("not allowed", c); // 실패해도 계속 진행
  }
  // ruleid: mois-1-05-os-command-injection-js
  exec(c);
}

function insideFailBranch(req, res) {
  const c = req.query.c;
  if (!ALLOWED.includes(c)) {
    // ruleid: mois-1-05-os-command-injection-js
    exec(c);
    return res.status(400).end();
  }
}

function reassigned(req, res) {
  let c = req.query.c;
  if (!ALLOWED.includes(c)) return res.status(400).end();
  c = req.query.other;
  // ruleid: mois-1-05-os-command-injection-js
  exec(c);
}

function appended(req, res) {
  let c = req.query.c;
  if (!ALLOWED.includes(c)) return res.status(400).end();
  c += req.query.extra;
  // ruleid: mois-1-05-os-command-injection-js
  exec(c);
}

function andCombined(req, res) {
  const c = req.query.c;
  if (req.query.strict && !ALLOWED.includes(c)) return res.status(400).end();
  // ruleid: mois-1-05-os-command-injection-js
  exec(c);
}

function otherVariable(req, res) {
  const c = req.query.c;
  const d = req.query.d;
  if (!ALLOWED.includes(d)) return res.status(400).end();
  // ruleid: mois-1-05-os-command-injection-js
  exec(c);
}

function mutatedList(req, res) {
  const c = req.query.c;
  if (!CHANGED.includes(c)) return res.status(400).end();
  // ruleid: mois-1-05-os-command-injection-js
  exec(c);
}

function letList(req, res) {
  const c = req.query.c;
  if (!LOOSE.includes(c)) return res.status(400).end();
  // ruleid: mois-1-05-os-command-injection-js
  exec(c);
}

function nestedConditionalReturn(req, res) {
  const c = req.query.c;
  if (!ALLOWED.includes(c)) {
    if (req.query.debug) return res.end();
  }
  // ruleid: mois-1-05-os-command-injection-js
  exec(c);
}

function elseBranch(req, res) {
  const c = req.query.c;
  if (ALLOWED.includes(c)) {
    console.log("ok");
  } else {
    // ruleid: mois-1-05-os-command-injection-js
    exec(c);
  }
}

function positiveOr(req, res) {
  const c = req.query.c;
  if (ALLOWED.includes(c) || req.query.force) {
    // ruleid: mois-1-05-os-command-injection-js
    exec(c);
  }
}

function positiveWithElse(req, res) {
  const c = req.query.c;
  if (ALLOWED.includes(c)) {
    // ruleid: mois-1-05-os-command-injection-js
    exec(c);
  } else {
    res.status(400).end();
  }
}

function positiveReassigned(req, res) {
  let c = req.query.c;
  if (ALLOWED.includes(c)) {
    c = c + req.query.extra;
    // ruleid: mois-1-05-os-command-injection-js
    exec(c);
  }
}
