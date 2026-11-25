const fs = require('fs');
const fsp = require('fs/promises');
const { exec, execSync, spawn } = require('child_process');

function setup(dir, file) {
  // ruleid: mois-2-03-insecure-permission-js
  fs.chmodSync(file, 0o777);
  // ruleid: mois-2-03-insecure-permission-js
  fs.chmod(file, 0o666, (err) => {});
  // ruleid: mois-2-03-insecure-permission-js
  fs.chmod(file, '777', () => {});
  // ruleid: mois-2-03-insecure-permission-js
  fs.chmodSync(file, 511);
  // ruleid: mois-2-03-insecure-permission-js
  fs.fchmodSync(3, 0o646);
  // ruleid: mois-2-03-insecure-permission-js
  fs.mkdirSync(dir, 0o777);
  // ruleid: mois-2-03-insecure-permission-js
  fs.mkdirSync(dir, { recursive: true, mode: 0o777 });
  // ruleid: mois-2-03-insecure-permission-js
  fs.writeFileSync(file, 'data', { mode: 0o666 });
  // ruleid: mois-2-03-insecure-permission-js
  fs.openSync(file, 'w', 0o622);
  // ruleid: mois-2-03-insecure-permission-js
  fs.createWriteStream(file, { flags: 'a', mode: 438 });
  // ruleid: mois-2-03-insecure-permission-js
  process.umask(0);
  // ruleid: mois-2-03-insecure-permission-js
  exec('chmod 777 ' + file);
  // ruleid: mois-2-03-insecure-permission-js
  execSync(`chmod -R o+w ${dir}`);
  // ruleid: mois-2-03-insecure-permission-js
  spawn('chmod', ['666', file]);
}

async function setupAsync(file) {
  // ruleid: mois-2-03-insecure-permission-js
  await fsp.chmod(file, 0o777);
}
