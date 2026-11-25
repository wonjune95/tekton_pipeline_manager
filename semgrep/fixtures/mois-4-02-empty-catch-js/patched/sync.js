const logger = require('./logger');

function load(file) {
  // ok: mois-4-02-empty-catch-js 기록 후 기본값
  try {
    return JSON.parse(read(file));
  } catch (e) {
    logger.warn('bad config', e);
    return {};
  }
}

function fire(p) {
  // ok: mois-4-02-empty-catch-js 기록한다
  p.catch((err) => logger.error(err));
  // ok: mois-4-02-empty-catch-js 기록한다
  p.then(ok, (err) => { logger.error(err); });
}
