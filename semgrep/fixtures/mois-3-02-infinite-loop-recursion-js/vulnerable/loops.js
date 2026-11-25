async function poll(queue) {
  // ruleid: mois-3-02-infinite-loop-recursion-js
  while (true) {
    const job = await queue.next();
    handle(job); // break 는 주석일 뿐
  }
}

function spin(state) {
  // ruleid: mois-3-02-infinite-loop-recursion-js
  for (;;) {
    state.tick();
  }
}

function spin2(state) {
  // ruleid: mois-3-02-infinite-loop-recursion-js
  do {
    state.tick();
  } while (true);
}

function spin3(state) {
  // ruleid: mois-3-02-infinite-loop-recursion-js
  while (1) state.tick();
}

function walk(node) {
  console.log(node.name);
  // ruleid: mois-3-02-infinite-loop-recursion-js
  walk(node.parent);
}

function logOnly(n) {
  if (n < 0) {
    console.log('negative');
  }
  // ruleid: mois-3-02-infinite-loop-recursion-js
  return logOnly(n - 1);
}

const countdown = function (n) {
  // ruleid: mois-3-02-infinite-loop-recursion-js
  return countdown(n - 1);
};
