export const depth = (n: number): number =>
  // ruleid: mois-3-02-infinite-loop-recursion-js
  1 + depth(n - 1);

export class Tree {
  visit(node: Node): void {
    this.emit(node);
    // ruleid: mois-3-02-infinite-loop-recursion-js
    this.visit(node.parent);
  }
  emit(node: Node): void {}
}
