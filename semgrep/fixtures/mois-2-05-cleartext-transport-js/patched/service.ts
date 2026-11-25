import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({ providedIn: 'root' })
export class UserService {
  private hostServer = 'https://auth.example.com';
  constructor(private http: HttpClient) {}

  login(body: { email: string; password: string }) {
    // ok: mois-2-05-cleartext-transport-js https 상수에 이어 붙인 경로
    return this.http.post(this.hostServer + '/rest/user/login', body);
  }
}
