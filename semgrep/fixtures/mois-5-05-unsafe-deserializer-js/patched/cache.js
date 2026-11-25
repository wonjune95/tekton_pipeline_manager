const yaml = require('js-yaml');
const fs = require('fs');

function loadCache(file) {
  // ok: mois-5-05-unsafe-deserializer-js JSON
  return JSON.parse(fs.readFileSync(file, 'utf8'));
}

function loadPlugins(text) {
  // ok: mois-5-05-unsafe-deserializer-js 안전 스키마
  return yaml.load(text, { schema: yaml.CORE_SCHEMA });
}
