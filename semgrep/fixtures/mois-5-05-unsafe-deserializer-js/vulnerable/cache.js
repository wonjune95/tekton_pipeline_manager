const serialize = require('node-serialize');
const yaml = require('js-yaml');
const fs = require('fs');

function loadCache(file) {
  // ruleid: mois-5-05-unsafe-deserializer-js
  return serialize.unserialize(fs.readFileSync(file, 'utf8'));
}

function loadPlugins(text) {
  // ruleid: mois-5-05-unsafe-deserializer-js
  return yaml.load(text, { schema: yaml.DEFAULT_FULL_SCHEMA });
}
