import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({ providedIn: 'root' })
export class UserService {
  constructor(private http: HttpClient) {}

  login(body: { email: string; password: string }) {
    // ruleid: mois-2-05-cleartext-transport-js
    return this.http.post('http://auth.example.com/rest/user/login', body);
  }
}

export function subscribe(): EventSource {
  // ruleid: mois-2-05-cleartext-transport-js
  return new EventSource('http://events.example.com/stream');
}
