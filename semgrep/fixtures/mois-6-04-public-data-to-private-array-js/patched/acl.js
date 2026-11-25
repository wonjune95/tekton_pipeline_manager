class Acl {
  #allowed = new Set();

  replace(allowed) {
    // ok: mois-6-04-public-data-to-private-array-js 복사본
    this.#allowed = new Set(allowed);
  }
}
module.exports = Acl;
