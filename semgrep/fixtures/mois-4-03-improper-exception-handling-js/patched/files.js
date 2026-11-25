const fs = require('fs');

function save(file, body, done) {
  // ok: mois-4-03-improper-exception-handling-js 오류를 확인한다
  fs.writeFile(file, body, function (err) {
    if (err) return done(err);
    done();
  });
}

function show(file, res, next) {
  // ok: mois-4-03-improper-exception-handling-js 오류를 다음 처리기로 넘긴다
  fs.readFile(file, 'utf8', (err, data) => {
    if (err) {
      next(err);
      return;
    }
    res.send(data);
  });
}

function check(file, cb) {
  // ok: mois-4-03-improper-exception-handling-js fs.exists 콜백의 첫 인자는 존재 여부
  fs.exists(file, (exists) => cb(exists));
}

function forward(file, cb) {
  // ok: mois-4-03-improper-exception-handling-js 콜백을 그대로 넘김
  fs.unlink(file, cb);
}
