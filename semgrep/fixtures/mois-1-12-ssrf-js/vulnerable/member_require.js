// require(…).get 으로 함수만 꺼낸 형태
const get = require("https").get;

module.exports.probe = function (req, res) {
  // ruleid: mois-1-12-ssrf-js
  get(req.query.target, (r) => res.sendStatus(r.statusCode));
};
