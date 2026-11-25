export class Account {
  private roles: string[] = [];
  public tags: string[] = [];
  private name = 'a';

  getRoles(): string[] {
    // ok: mois-6-03-private-array-returned-js 복사본
    return [...this.roles];
  }

  getTags(): string[] {
    // ok: mois-6-03-private-array-returned-js 공개 필드
    return this.tags;
  }

  getName(): string {
    // ok: mois-6-03-private-array-returned-js 문자열은 바꿀 수 없다
    return this.name;
  }

  private rawRoles(): string[] {
    // ok: mois-6-03-private-array-returned-js 비공개 메서드
    return this.roles;
  }
}
