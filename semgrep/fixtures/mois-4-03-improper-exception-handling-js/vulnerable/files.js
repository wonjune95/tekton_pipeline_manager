const fs = require('fs');

function cleanup(file) {
  // ruleid: mois-4-03-improper-exception-handling-js
  fs.unlink(file, () => {});
}

function save(file, body, done) {
  // ruleid: mois-4-03-improper-exception-handling-js
  fs.writeFile(file, body, function (err) {
    done();
  });
}

function show(file, res) {
  // ruleid: mois-4-03-improper-exception-handling-js
  fs.readFile(file, 'utf8', (err, data) => {
    res.send(data);
  });
}
