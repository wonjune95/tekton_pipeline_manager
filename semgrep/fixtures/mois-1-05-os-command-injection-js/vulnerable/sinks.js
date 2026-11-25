// 운영체제 명령어 삽입 — 셸 실행 sink 형태별
const cp = require("child_process");
const { exec, execSync: runSync, spawn, execFile } = require("node:child_process");
const shell = require("shelljs");
const express = require("express");
const app = express();

app.get("/ping", (req, res) => {
  const host = req.query.host;
  // ruleid: mois-1-05-os-command-injection-js
  cp.exec("ping -c 1 " + host, (err, out) => res.send(out));
  // ruleid: mois-1-05-os-command-injection-js
  exec(`nslookup ${host}`);
  // ruleid: mois-1-05-os-command-injection-js
  runSync("dig " + req.body.name);
  // ruleid: mois-1-05-os-command-injection-js
  shell.exec("whois " + host);
});

app.post("/run", (req, res) => {
  const { tool, arg } = req.body;
  // ruleid: mois-1-05-os-command-injection-js
  spawn(tool, ["--version"]);
  // ruleid: mois-1-05-os-command-injection-js
  spawn("sh", ["-c", "tar czf out.tgz " + arg]);
  // ruleid: mois-1-05-os-command-injection-js
  execFile("cmd.exe", ["/c", arg]);
  // ruleid: mois-1-05-os-command-injection-js
  execFile("ls", [arg], { shell: true });
  // ruleid: mois-1-05-os-command-injection-js
  cp.spawnSync("psql", ["-c", arg]);
  res.end();
});
