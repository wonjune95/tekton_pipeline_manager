// require(…).readFileSync 로 함수만 꺼낸 형태
const readFileSync = require("fs").readFileSync;
const copyFileSync = require("fs").copyFileSync;

module.exports.show = function (req, res) {
  // ruleid: mois-1-03-path-traversal-js
  res.type("text/plain").end(readFileSync("/srv/" + req.query.f));
  // ruleid: mois-1-03-path-traversal-js
  copyFileSync("/srv/template.txt", req.body.to);
};
