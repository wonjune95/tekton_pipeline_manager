function load(file) {
  let data = null;
  // ruleid: mois-4-02-empty-catch-js
  try {
    data = JSON.parse(read(file));
  } catch (e) {}
  return data;
}

function load2(file) {
  // ruleid: mois-4-02-empty-catch-js
  try {
    return JSON.parse(read(file));
  } catch {
    // 무시
  } finally {
    close(file);
  }
}

function fire(p) {
  // ruleid: mois-4-02-empty-catch-js
  p.catch(() => {});
  // ruleid: mois-4-02-empty-catch-js
  p.then(ok).catch(function (err) {});
  // ruleid: mois-4-02-empty-catch-js
  p.then(ok, (err) => {});
}
