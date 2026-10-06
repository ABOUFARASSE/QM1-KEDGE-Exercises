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
  const storagePrefix = `qm1-ch${chapter}`;
  let chapterConfig = null;
  let unlocked = localStorage.getItem(`${storagePrefix}-unlocked`) === '1';

  function setSolutions(open, message = '') {
    unlocked = open;
    document.body.classList.toggle('solutions-visible', open);
    $('#statusDot').classList.toggle('open', open);
    $('#statusText').textContent = open ? 'Solutions available' : 'Solutions locked';
    if (message) $('#codeMessage').textContent = message;
    if (open) localStorage.setItem(`${storagePrefix}-unlocked`, '1');
  }

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
      setSolutions(true, 'Correct code — detailed solutions are now visible.');
      $('#accessCode').value = '';
    } else {
      $('#codeMessage').textContent = 'Incorrect code. Check the code provided during the session.';
    }
  });

  $$('.hint-button').forEach(button => button.addEventListener('click', () => {
    const hint = button.nextElementSibling;
    hint.classList.toggle('visible');
    button.textContent = hint.classList.contains('visible') ? 'Hide method prompt' : 'Show method prompt';
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
  await refreshAccess();
  setInterval(refreshAccess, 15000);
}

if (page === 'portal') initialisePortal();
if (page === 'chapter') initialiseChapter();
