class Acl {
  #allowed = ['read'];

  list() {
    // ok: mois-6-03-private-array-returned-js 복사본
    return this.#allowed.slice();
  }

  #raw() {
    // ok: mois-6-03-private-array-returned-js 비공개 메서드
    return this.#allowed;
  }
}
module.exports = Acl;
