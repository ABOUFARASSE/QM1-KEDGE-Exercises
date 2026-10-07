const fs = require('fs');
const vm = require('vm');
const path = require('path');

function evaluate(file, beforeMarker = null) {
  let source = fs.readFileSync(path.join(__dirname, file), 'utf8');
  if (beforeMarker) source = source.split(beforeMarker)[0];
  const sandbox = { window: {} };
  vm.createContext(sandbox);
  vm.runInContext(source, sandbox, { filename: file });
  return sandbox.window;
}

const allTranslations = evaluate('translations-fr.js').QM1_FR_ALL;
const chapter1 = evaluate('chapter1-fr.js').QM1_FR;
const extended = evaluate('extended-exercises.js', '(function extendChapter').QM1_EXTENDED;
allTranslations['1'] = chapter1;

fs.writeFileSync(path.join(__dirname, 'exercise-data-export.json'), JSON.stringify({ translations: allTranslations, extended }, null, 2));
console.log('exercise-data-export.json');
