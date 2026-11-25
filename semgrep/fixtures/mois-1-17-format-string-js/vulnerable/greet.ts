// import 형태
import { sprintf } from 'sprintf-js';
import * as util from 'util';

export function greet(req: any) {
  // ruleid: mois-1-17-format-string-js
  return sprintf(req.body.template, { user: req.user });
}
