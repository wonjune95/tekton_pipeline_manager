const micromatch = require('micromatch');

function version(ua) {
  // ok: mois-5-01-null-dereference-js 옵셔널 체이닝
  return ua.match(/Chrome\/(\d+)/)?.[1];
}

function parts(s) {
  const m = s.match(/^(\w+)-(\d+)$/);
  if (!m) return null;
  // ok: mois-5-01-null-dereference-js null 이면 빠져나갔다
  return { name: m[1], id: Number(m[2]) };
}

function parts2(s) {
  const m = s.match(/^(\w+)$/);
  // ok: mois-5-01-null-dereference-js 조건 안에서 사용
  return m ? m[1] : null;
}

function parts3(s) {
  const m = /(\d+)/.exec(s);
  if (m) {
    // ok: mois-5-01-null-dereference-js 조건 안에서 사용
    use(m[1]);
  }
}

function files(list) {
  // ok: mois-5-01-null-dereference-js micromatch.match 는 배열을 돌려준다
  return micromatch.match(list, '*.js').length;
}

function color(style) {
  if (/^rgb\((\d+)\)$/.test(style)) {
    const c = /^rgb\((\d+)\)$/.exec(style);
    // ok: mois-5-01-null-dereference-js 같은 정규식으로 test() 한 if 안
    return Number(c[1]);
  }
  return 0;
}
