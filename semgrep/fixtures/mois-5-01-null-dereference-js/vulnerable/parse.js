function version(ua) {
  // ruleid: mois-5-01-null-dereference-js
  return ua.match(/Chrome\/(\d+)/)[1];
}

function count(text) {
  // ruleid: mois-5-01-null-dereference-js
  return text.match(new RegExp('\\n', 'g')).length;
}

function token(header) {
  // ruleid: mois-5-01-null-dereference-js
  return /^Bearer (.+)$/.exec(header)[1];
}

function parts(s) {
  const m = s.match(/^(\w+)-(\d+)$/);
  log('parsed');
  // ruleid: mois-5-01-null-dereference-js
  return { name: m[1], id: Number(m[2]) };
}

function weakCheck(s) {
  const m = /(\d+)/.exec(s);
  if (!m) {
    log('no match');
  }
  // ruleid: mois-5-01-null-dereference-js
  return m.index;
}

function color(style, other) {
  if (/^rgb\((\d+)\)$/.test(other)) {
    const c = /^rgb\((\d+)\)$/.exec(style);
    // ruleid: mois-5-01-null-dereference-js
    return Number(c[1]);
  }
  return 0;
}
