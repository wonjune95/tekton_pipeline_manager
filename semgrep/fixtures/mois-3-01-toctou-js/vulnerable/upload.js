const fs = require('fs');
const path = require('path');

function saveReport(dir, name, data) {
  const target = path.join(dir, name);
  if (!fs.existsSync(target)) {
    // ruleid: mois-3-01-toctou-js
    fs.writeFileSync(target, data);
  }
}

function removeIfExists(file) {
  if (fs.existsSync(file)) {
    // ruleid: mois-3-01-toctou-js
    fs.unlinkSync(file);
  }
}

function readConfig(file) {
  if (!fs.existsSync(file)) return null;
  // ruleid: mois-3-01-toctou-js
  return fs.readFileSync(file, 'utf8');
}

function ensureDir(dir) {
  if (!fs.existsSync(dir)) {
    // ruleid: mois-3-01-toctou-js
    fs.mkdirSync(dir);
  }
}

function rotate(file) {
  try {
    fs.accessSync(file, fs.constants.W_OK);
  } catch (e) {
    return;
  }
  if (fs.statSync(file).size > 1024) {
    // ruleid: mois-3-01-toctou-js
    fs.renameSync(file, file + '.1');
  } else {
    log('small');
  }
}

function elseBranch(file) {
  if (fs.existsSync(file)) {
    log('exists');
  } else {
    // ruleid: mois-3-01-toctou-js
    fs.writeFileSync(file, '');
  }
}

function callbackCheck(file, cb) {
  fs.access(file, (err) => {
    if (err) return cb(err);
    // ruleid: mois-3-01-toctou-js
    fs.unlink(file, cb);
  });
}

function streamCheck(file, res) {
  if (fs.existsSync(file)) {
    // ruleid: mois-3-01-toctou-js
    fs.createReadStream(file).pipe(res);
  }
}
