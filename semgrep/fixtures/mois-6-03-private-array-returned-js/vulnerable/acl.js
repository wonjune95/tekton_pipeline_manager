class Acl {
  #allowed = ['read'];

  list() {
    // ruleid: mois-6-03-private-array-returned-js
    return this.#allowed;
  }
}
module.exports = Acl;
