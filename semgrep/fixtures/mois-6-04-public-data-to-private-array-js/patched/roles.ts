export class Account {
  private roles: string[] = [];
  public tags: string[] = [];

  setRoles(roles: string[]): void {
    // ok: mois-6-04-public-data-to-private-array-js 복사본
    this.roles = [...roles];
  }

  setTags(tags: string[]): void {
    // ok: mois-6-04-public-data-to-private-array-js 공개 필드
    this.tags = tags;
  }

  private load(roles: string[]): void {
    // ok: mois-6-04-public-data-to-private-array-js 비공개 메서드
    this.roles = roles;
  }
}
