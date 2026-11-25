async function poll(queue) {
  // ok: mois-3-02-infinite-loop-recursion-js break 로 빠져나온다
  while (true) {
    const job = await queue.next();
    if (!job) break;
    handle(job);
  }
}

function find(items) {
  // ok: mois-3-02-infinite-loop-recursion-js return 으로 빠져나온다
  for (;;) {
    const x = items.shift();
    if (x.ok) return x;
  }
}

function fact(n) {
  if (n <= 1) return 1;
  // ok: mois-3-02-infinite-loop-recursion-js 기저 조건이 있다
  return n * fact(n - 1);
}

function walk(node) {
  // ok: mois-3-02-infinite-loop-recursion-js 조건 안에서만 재귀 호출
  if (node.parent) walk(node.parent);
}

function walk2(node) {
  // ok: mois-3-02-infinite-loop-recursion-js && 로 끝을 확인
  node.parent && walk2(node.parent);
}

function retry(task) {
  // ok: mois-3-02-infinite-loop-recursion-js 타이머 콜백은 호출 스택이 쌓이지 않는다
  setTimeout(() => retry(task), 1000);
}
