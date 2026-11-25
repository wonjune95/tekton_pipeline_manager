// Angular 의 XSRF 헤더 전송을 끔
import { NgModule } from '@angular/core';
import { HttpClientModule, HttpClientXsrfModule, provideHttpClient, withNoXsrfProtection } from '@angular/common/http';

@NgModule({
  // ruleid: mois-1-11-csrf-js
  imports: [HttpClientModule, HttpClientXsrfModule.disable()],
})
export class AppModule {}

export const appConfig = {
  // ruleid: mois-1-11-csrf-js
  providers: [provideHttpClient(withNoXsrfProtection())],
};
