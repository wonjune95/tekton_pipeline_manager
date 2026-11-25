const fs = require('fs');

function saveReport(target, data) {
  // ok: mois-3-01-toctou-js 검사 없이 'wx' 로 열어 이미 있으면 EEXIST 로 실패한다
  fs.writeFileSync(target, data, { flag: 'wx' });
}

function removeIfExists(file) {
  try {
    // ok: mois-3-01-toctou-js 검사 없이 지우고 ENOENT 를 처리한다
    fs.unlinkSync(file);
  } catch (e) {
    if (e.code !== 'ENOENT') throw e;
  }
}

function ensureDir(dir) {
  if (!fs.existsSync(dir)) {
    // ok: mois-3-01-toctou-js recursive 는 이미 있어도 실패하지 않는다
    fs.mkdirSync(dir, { recursive: true });
  }
}

function otherPath(a, b) {
  if (fs.existsSync(a)) {
    // ok: mois-3-01-toctou-js 검사한 경로와 다른 경로
    fs.unlinkSync(b);
  }
}
