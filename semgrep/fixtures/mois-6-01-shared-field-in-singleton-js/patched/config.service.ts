import { Injectable } from '@angular/core';

@Injectable({ providedIn: 'root' })
export class ConfigService {
  private cached: unknown;
  load(): unknown {
    // ok: mois-6-01-shared-field-in-singleton-js Angular 서비스(브라우저 안의 싱글톤)
    this.cached = fetchConfig();
    return this.cached;
  }
}
