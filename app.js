const $ = selector => document.querySelector(selector);
const $$ = selector => [...document.querySelectorAll(selector)];
const page = document.body.dataset.page;

async function getConfig() {
  const response = await fetch(`config.json?t=${Date.now()}`, { cache: 'no-store' });
  if (!response.ok) throw new Error('Configuration unavailable');
  return response.json();
}

async function sha256(text) {
  const data = new TextEncoder().encode(text);
  const hash = await crypto.subtle.digest('SHA-256', data);
  return [...new Uint8Array(hash)].map(byte => byte.toString(16).padStart(2, '0')).join('');
}

async function initialisePortal() {
  try {
    const config = await getConfig();
    let openCount = 0;
    $$('.chapter-card').forEach(card => {
      const chapter = card.dataset.chapter;
      const chapterConfig = config.chapters?.[chapter];
      const isOpen = Boolean(chapterConfig?.open);
      if (isOpen) openCount += 1;
      card.classList.toggle('locked', !isOpen);
      card.querySelector('.availability').textContent = isOpen ? 'Available now' : 'Coming later';
      const link = card.querySelector('a');
      link.setAttribute('aria-disabled', String(!isOpen));
      link.tabIndex = isOpen ? 0 : -1;
      if (!isOpen) link.addEventListener('click', event => event.preventDefault());
    });
    $('#courseProgress').textContent = `${openCount} of 6 chapters available`;
    $('#courseBar').style.width = `${100 * openCount / 6}%`;
  } catch (error) {
    $('#courseProgress').textContent = 'Course access currently unavailable';
  }
}

async function initialiseChapter() {
  const chapter = document.body.dataset.chapter;
  const storagePrefix = `qm1-v2-ch${chapter}`;
  let chapterConfig = null;
  let unlocked = sessionStorage.getItem(`${storagePrefix}-unlocked`) === '1';
  const hideSolutionsButton = document.createElement('button');
  hideSolutionsButton.type = 'button';
  hideSolutionsButton.className = 'hide-solutions-button';
  hideSolutionsButton.hidden = true;
  $('#codeForm').appendChild(hideSolutionsButton);

  function setSolutions(open, message = '') {
    unlocked = open;
    document.body.classList.toggle('solutions-visible', open);
    $('#statusDot').classList.toggle('open', open);
    const fr = document.body.dataset.lang === 'fr';
    $('#statusText').textContent = open ? (fr ? 'Corrigés accessibles' : 'Solutions available') : (fr ? 'Corrigés verrouillés' : 'Solutions locked');
    hideSolutionsButton.textContent = fr ? 'Masquer les corrigés' : 'Hide solutions';
    hideSolutionsButton.hidden = !open;
    if (message) $('#codeMessage').textContent = message;
    if (open) sessionStorage.setItem(`${storagePrefix}-unlocked`, '1');
    else sessionStorage.removeItem(`${storagePrefix}-unlocked`);
  }

  hideSolutionsButton.addEventListener('click', () => {
    const fr = document.body.dataset.lang === 'fr';
    setSolutions(false, fr ? 'Les corrigés ont été masqués.' : 'The solutions have been hidden.');
  });

  async function refreshAccess() {
    try {
      const config = await getConfig();
      chapterConfig = config.chapters?.[chapter];
      const chapterOpen = Boolean(chapterConfig?.open);
      $('#chapterGate').hidden = chapterOpen;
      document.body.classList.toggle('chapter-locked', !chapterOpen);
      if (!chapterOpen) return;
      if (chapterConfig.solutionsOpen) setSolutions(true, config.messageWhenOpen);
      else setSolutions(unlocked);
    } catch (error) {
      $('#statusText').textContent = unlocked ? 'Solutions available' : 'Offline mode';
    }
  }

  $('#codeForm').addEventListener('submit', async event => {
    event.preventDefault();
    const code = $('#accessCode').value.trim();
    if (!code || !chapterConfig) return;
    const hash = await sha256(code);
    if (hash === chapterConfig.codeHash) {
      setSolutions(true, document.body.dataset.lang === 'fr' ? 'Code correct — les corrigés détaillés sont maintenant visibles.' : 'Correct code — detailed solutions are now visible.');
      $('#accessCode').value = '';
    } else {
      $('#codeMessage').textContent = document.body.dataset.lang === 'fr' ? 'Code incorrect. Vérifiez le code communiqué pendant la séance.' : 'Incorrect code. Check the code provided during the session.';
    }
  });

  $$('.hint-button').forEach(button => button.addEventListener('click', () => {
    const hint = button.nextElementSibling;
    hint.classList.toggle('visible');
    const fr = document.body.dataset.lang === 'fr';
    button.textContent = hint.classList.contains('visible') ? (fr ? 'Masquer l’aide méthodologique' : 'Hide method prompt') : (fr ? 'Afficher l’aide méthodologique' : 'Show method prompt');
  }));

  const checks = $$('.done input');
  function updateProgress() {
    const completed = checks.filter(check => check.checked).length;
    $('#progressText').textContent = `${completed} / ${checks.length} completed`;
    $('#progressBar').style.width = `${100 * completed / checks.length}%`;
    localStorage.setItem(`${storagePrefix}-progress`, JSON.stringify(checks.map(check => check.checked)));
  }
  const saved = JSON.parse(localStorage.getItem(`${storagePrefix}-progress`) || '[]');
  checks.forEach((check, index) => {
    check.checked = Boolean(saved[index]);
    check.addEventListener('change', updateProgress);
  });
  updateProgress();
  initialiseLanguage(chapter);
  await refreshAccess();
  setInterval(refreshAccess, 15000);
}

function initialiseLanguage(chapter) {
  const translation = window.QM1_FR || window.QM1_FR_ALL?.[chapter];
  if (!translation) return;
  const status = document.querySelector('.status');
  const switcher = document.createElement('button');
  switcher.className = 'language-switch';
  switcher.type = 'button';
  status.parentElement.insertBefore(switcher, status);
  const originals = new Map();
  const remember = element => { if (element && !originals.has(element)) originals.set(element, element.innerHTML); };
  Object.keys(translation.page).forEach(key => {
    const selector = key.replace('@placeholder', '');
    remember(document.querySelector(selector));
  });
  $$('.levels a').forEach(remember);
  $$('.exercise').forEach(article => {
    ['.level','h2','.question','.hint','.solution'].forEach(selector => remember(article.querySelector(selector)));
  });
  $$('.done').forEach(label => label.dataset.en = 'Completed');

  function apply(lang) {
    document.documentElement.lang = lang;
    document.body.dataset.lang = lang;
    if (lang === 'fr') {
      for (const [key, value] of Object.entries(translation.page)) {
        const isPlaceholder = key.endsWith('@placeholder');
        const element = document.querySelector(key.replace('@placeholder', ''));
        if (isPlaceholder) element.placeholder = value; else element.innerHTML = value;
      }
      $$('.levels a').forEach((link, index) => link.textContent = translation.nav[index]);
      $$('.exercise').forEach(article => {
        const tr = translation.exercises[article.dataset.ex];
        article.querySelector('.level').textContent = tr.level;
        article.querySelector('h2').textContent = tr.title;
        article.querySelector('.question').innerHTML = tr.question;
        article.querySelector('.hint').textContent = tr.hint;
        article.querySelector('.solution').innerHTML = tr.solution;
      });
      $$('.done').forEach(label => { label.lastChild.textContent = ' Terminé'; });
      $$('.hint-button').forEach(button => { button.textContent = button.nextElementSibling.classList.contains('visible') ? 'Masquer l’aide méthodologique' : 'Afficher l’aide méthodologique'; });
      switcher.textContent = 'English';
    } else {
      for (const [element, content] of originals.entries()) element.innerHTML = content;
      document.querySelector('#accessCode').placeholder = 'Enter the session code';
      $$('.done').forEach(label => { label.lastChild.textContent = ' Completed'; });
      $$('.hint-button').forEach(button => { button.textContent = button.nextElementSibling.classList.contains('visible') ? 'Hide method prompt' : 'Show method prompt'; });
      switcher.textContent = 'Français';
    }
    const completed = $$('.done input').filter(check => check.checked).length;
    const total = $$('.done input').length;
    $('#progressText').textContent = lang === 'fr' ? `${completed} / ${total} terminés` : `${completed} / ${total} completed`;
    const open = document.body.classList.contains('solutions-visible');
    $('#statusText').textContent = open ? (lang === 'fr' ? 'Corrigés accessibles' : 'Solutions available') : (lang === 'fr' ? 'Corrigés verrouillés' : 'Solutions locked');
    const hideSolutionsButton = document.querySelector('.hide-solutions-button');
    if (hideSolutionsButton) hideSolutionsButton.textContent = lang === 'fr' ? 'Masquer les corrigés' : 'Hide solutions';
    localStorage.setItem('qm1-language', lang);
  }
  switcher.addEventListener('click', () => apply(document.body.dataset.lang === 'fr' ? 'en' : 'fr'));
  apply(localStorage.getItem('qm1-language') === 'fr' ? 'fr' : 'en');
}

if (page === 'portal') initialisePortal();
if (page === 'chapter') initialiseChapter();
