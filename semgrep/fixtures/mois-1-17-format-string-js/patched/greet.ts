// 형식은 상수, 입력은 인자
import { sprintf } from 'sprintf-js';
import * as util from 'util';

export function greet(req: any) {
  // ok: mois-1-17-format-string-js 형식이 상수
  const a = sprintf('안녕하세요 %s', req.query.name);
  // ok: mois-1-17-format-string-js util.format 은 인자만 바꾼다 (대상 아님)
  const b = util.format(req.query.fmt, 'x');
  return a + b;
}
