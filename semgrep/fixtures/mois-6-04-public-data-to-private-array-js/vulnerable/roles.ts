export class Account {
  private roles: string[] = [];
  private history: string[];

  constructor(history: string[]) {
    // ruleid: mois-6-04-public-data-to-private-array-js
    this.history = history;
  }

  setRoles(roles: string[]): void {
    // ruleid: mois-6-04-public-data-to-private-array-js
    this.roles = roles;
  }
}
