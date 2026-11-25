// csurf 가 상태를 바꾸는 메서드를 검사하지 않게 함
const csrf = require('csurf');
const express = require('express');
const app = express();
// ruleid: mois-1-11-csrf-js
app.use(csrf({ cookie: true, ignoreMethods: ['GET', 'HEAD', 'OPTIONS', 'POST'] }));
