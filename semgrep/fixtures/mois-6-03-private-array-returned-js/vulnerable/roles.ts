export class Account {
  private roles: string[] = [];
  private readonly grants = new Map<string, boolean>();
  private history: string[];

  constructor() {
    this.history = [];
  }

  getRoles(): string[] {
    // ruleid: mois-6-03-private-array-returned-js
    return this.roles;
  }

  get grantMap(): Map<string, boolean> {
    // ruleid: mois-6-03-private-array-returned-js
    return this.grants;
  }

  public getHistory(): string[] {
    // ruleid: mois-6-03-private-array-returned-js
    return this.history;
  }
}
