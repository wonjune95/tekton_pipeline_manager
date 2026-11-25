export const depth = (n: number): number => {
  if (n <= 0) return 0;
  // ok: mois-3-02-infinite-loop-recursion-js 기저 조건이 있다
  return 1 + depth(n - 1);
};

export class Tree {
  visit(node: Node | null): void {
    if (!node) {
      return;
    }
    // ok: mois-3-02-infinite-loop-recursion-js 기저 조건이 있다
    this.visit(node.parent);
  }
  sum(n: number): number {
    // ok: mois-3-02-infinite-loop-recursion-js 조건식
    return n > 0 ? n + this.sum(n - 1) : 0;
  }
}

import { formatLines } from './format';
export class View {
  lines: number[] = [];
  formatLines(): string {
    // ok: mois-3-02-infinite-loop-recursion-js 같은 이름의 바깥 함수 호출(메서드 재귀 아님)
    return formatLines(this.lines);
  }
}
