// require(…).exec 로 함수만 꺼낸 형태
const exec = require("child_process").exec;
const spawnSync = require("child_process").spawnSync;

module.exports.ping = function (req, res) {
  // ruleid: mois-1-05-os-command-injection-js
  exec("ping -c 2 " + req.body.address, (err, stdout) => res.send(stdout));
  // ruleid: mois-1-05-os-command-injection-js
  spawnSync(req.body.tool);
};
