class Acl {
  #allowed = new Set();

  replace(allowed) {
    // ruleid: mois-6-04-public-data-to-private-array-js
    this.#allowed = allowed;
  }
}
module.exports = Acl;
