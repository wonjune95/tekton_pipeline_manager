const fs = require('fs');
const { execSync, spawn } = require('child_process');

function setup(dir, file, mode) {
  // ok: mois-2-03-insecure-permission-js 소유자 전용
  fs.chmodSync(file, 0o600);
  // ok: mois-2-03-insecure-permission-js 그룹 읽기까지만
  fs.chmod(file, 0o640, (err) => { if (err) throw err; });
  // ok: mois-2-03-insecure-permission-js 디렉터리 소유자 전용
  fs.mkdirSync(dir, { recursive: true, mode: 0o700 });
  // ok: mois-2-03-insecure-permission-js others 는 읽기·실행만
  fs.mkdirSync(dir, 0o755);
  // ok: mois-2-03-insecure-permission-js 파일 소유자 전용
  fs.writeFileSync(file, 'secret', { mode: 0o600 });
  // ok: mois-2-03-insecure-permission-js 일반적인 umask
  process.umask(0o077);
  // ok: mois-2-03-insecure-permission-js 실행 권한만 추가
  execSync(`chmod 750 ${file}`);
  // ok: mois-2-03-insecure-permission-js 소유자 쓰기
  spawn('chmod', ['u+w', file]);
  // ok: mois-2-03-insecure-permission-js fetch 의 mode 는 파일 권한이 아님
  fetch('https://api.example.com/x', { mode: 'cors' });
}
