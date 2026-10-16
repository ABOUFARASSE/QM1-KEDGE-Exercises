const $=s=>document.querySelector(s),$$=s=>[...document.querySelectorAll(s)];
const page=document.body.dataset.page,VERSION='20261017-inline-solutions-v2';
const CHAPTERS={1:{en:'Data presentation',fr:'Présenter et organiser les données',leadEn:'Organise, classify and represent data using the methods required in QM1.',leadFr:'Organiser, classer et représenter les données avec les méthodes exigées en QM1.'},2:{en:'Measures of central tendency',fr:'Mesures de tendance centrale',leadEn:'Calculate and interpret mode, median, quartiles and the appropriate means.',leadFr:'Calculer et interpréter mode, médiane, quartiles et les moyennes adaptées.'},3:{en:'Dispersion and concentration',fr:'Dispersion et concentration',leadEn:'Measure variability and concentration using the indicators covered in the course.',leadFr:'Mesurer la dispersion et la concentration à l’aide des indicateurs du cours.'},4:{en:'Bivariate distributions and regression',fr:'Distributions bivariées et régression',leadEn:'Study correlation, linear adjustment and forecasting with the course conventions.',leadFr:'Étudier corrélation, ajustement linéaire et prévision selon les conventions du cours.'},5:{en:'Time series',fr:'Séries temporelles',leadEn:'Analyse trend, moving averages, seasonality and quarterly forecasts.',leadFr:'Analyser tendance, moyennes mobiles, saisonnalité et prévisions trimestrielles.'},6:{en:'Index numbers',fr:'Nombres-indices',leadEn:'Construct and interpret elementary and synthetic price, quantity and value indices.',leadFr:'Construire et interpréter les indices élémentaires et synthétiques de prix, quantité et valeur.'},7:{en:'Integrated cases',fr:'Cas intégrateurs',leadEn:'Combine the main QM1 methods in continuous-assessment and final-exam style cases.',leadFr:'Mobiliser les principales méthodes de QM1 dans des cas de type contrôle continu et examen final.'}};
const I18N={en:{portalTitle:'Progressive exercise programme',portalLead:'Seven bilingual practice sheets aligned with the QM1 course, with printable statements and detailed solutions.',howTitle:'How to work',how1:'Choose English or French with the language button.',how2:'Open a chapter and work directly from the exercises displayed on the page.',how3:'Download the statement in French or English whenever needed.',how4:'Enter the session code to reveal the detailed solution immediately below each exercise.',how5:'After unlocking, switch language freely between the French and English solutions.',openChapter:'Open chapter',available:'Available now',later:'Coming later',chapterLabel:'CHAPTER',notReleased:'Not released yet',notReleasedText:'This chapter will become available when your lecturer opens it.',returnMenu:'Return to the course menu',allChapters:'← All chapters',chapterWord:'CHAPTER',resourceStatus:'Resources',bilingualPack:'Bilingual pack',packNote:'Exercises are displayed on the page; detailed solutions appear after the session code.',liveAccess:'LIVE SOLUTION ACCESS',unlockTitle:'Unlock the detailed solutions',unlockText:'Use the session code supplied by your lecturer. Access remains active for this browser session.',sessionCode:'Session code',unlock:'Unlock',printable:'PRINTABLE RESOURCES',downloadsTitle:'Download the chapter',downloadsText:'The exercise PDFs remain available as optional printable versions. Solution PDFs appear after unlocking.',statements:'Exercise statements',solutions:'Detailed solutions',locked:'Solutions locked',open:'Solutions available',hide:'Hide solutions',hidden:'The solutions have been hidden.',correct:'Correct code — detailed solutions are now visible.',incorrect:'Incorrect code. Check the code provided during the session.',courseAvailable:(n,t)=>`${n} of ${t} chapters available`,offline:'Course access currently unavailable'},fr:{portalTitle:'Programme progressif d’exercices',portalLead:'Sept fiches bilingues alignées sur le cours QM1, avec énoncés affichés directement dans la page et versions PDF imprimables.',howTitle:'Comment travailler',how1:'Choisissez le français ou l’anglais avec le bouton de langue.',how2:'Ouvrez un chapitre et travaillez directement à partir des exercices affichés dans la page.',how3:'Téléchargez l’énoncé en français ou en anglais si vous souhaitez une version imprimable.',how4:'Saisissez le code de séance pour afficher le corrigé détaillé immédiatement sous chaque exercice.',how5:'Après déverrouillage, passez librement du corrigé français au corrigé anglais.',openChapter:'Ouvrir le chapitre',available:'Disponible',later:'À venir',chapterLabel:'CHAPITRE',notReleased:'Pas encore disponible',notReleasedText:'Ce chapitre sera accessible lorsque votre enseignant l’ouvrira.',returnMenu:'Retour au menu du cours',allChapters:'← Tous les chapitres',chapterWord:'CHAPITRE',resourceStatus:'Ressources',bilingualPack:'Pack bilingue',packNote:'Les exercices sont affichés dans la page ; le corrigé détaillé apparaît après le code de séance.',liveAccess:'ACCÈS AUX CORRIGÉS',unlockTitle:'Débloquer les corrigés détaillés',unlockText:'Utilisez le code de séance communiqué par votre enseignant. L’accès reste actif pendant cette session du navigateur.',sessionCode:'Code de séance',unlock:'Débloquer',printable:'RESSOURCES IMPRIMABLES',downloadsTitle:'Télécharger le chapitre',downloadsText:'Les PDF restent disponibles comme versions imprimables optionnelles. Les corrigés PDF apparaissent après déverrouillage.',statements:'Énoncés',solutions:'Corrigés détaillés',locked:'Corrigés verrouillés',open:'Corrigés accessibles',hide:'Masquer les corrigés',hidden:'Les corrigés ont été masqués.',correct:'Code correct — les corrigés détaillés sont maintenant visibles.',incorrect:'Code incorrect. Vérifiez le code communiqué pendant la séance.',courseAvailable:(n,t)=>`${n} chapitre${n>1?'s':''} disponible${n>1?'s':''} sur ${t}`,offline:'Accès au cours momentanément indisponible'}};
const CONTENT_PATHS={1:'content/chapter-1.js',2:'content/chapter-2.js',3:'content/chapter-3.js',4:'content/chapter-4.js',5:'content/c5.js',6:'content/c6.js',7:'content/case7.js'};
let mathJaxLoading=null;
function ensureMathJax(){if(window.MathJax&&typeof window.MathJax.typesetPromise==='function')return Promise.resolve(window.MathJax);if(mathJaxLoading)return mathJaxLoading;window.MathJax={tex:{inlineMath:[['$','$']],displayMath:[['$$','$$']],processEscapes:true,macros:{Cov:"\\operatorname{Cov}",Var:"\\operatorname{Var}",sd:"\\sigma",E:"\\mathbb{E}",R:"\\mathbb{R}"}},chtml:{scale:1.02},options:{skipHtmlTags:['script','noscript','style','textarea','pre','code']}};mathJaxLoading=new Promise((resolve,reject)=>{const s=document.createElement('script');s.src='https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js';s.async=true;s.onload=()=>resolve(window.MathJax);s.onerror=reject;document.head.appendChild(s)});return mathJaxLoading}
function prepareMath(node){if(!node)return;const escapedPercent=String.fromCharCode(92)+'%';node.querySelectorAll('.math-line').forEach(el=>{if(el.dataset.mathPrepared==='1')return;el.textContent=el.textContent.replaceAll('%',escapedPercent);el.dataset.mathPrepared='1'})}
function typesetMath(...nodes){nodes.filter(Boolean).forEach(prepareMath);ensureMathJax().then(()=>{const targets=nodes.filter(Boolean);if(window.MathJax.typesetPromise)window.MathJax.typesetPromise(targets).catch(()=>{})}).catch(()=>{})}
async function getConfig(){const r=await fetch(`config.json?t=${Date.now()}`,{cache:'no-store'});if(!r.ok)throw new Error('config');return r.json()}
async function sha256(text){const data=new TextEncoder().encode(text),hash=await crypto.subtle.digest('SHA-256',data);return [...new Uint8Array(hash)].map(b=>b.toString(16).padStart(2,'0')).join('')}
function getLang(){return localStorage.getItem('qm1-language')==='fr'?'fr':'en'}
function setLangPref(lang){localStorage.setItem('qm1-language',lang);document.documentElement.lang=lang;document.body.dataset.lang=lang}
function translateStatic(lang){const t=I18N[lang];$$('[data-i18n]').forEach(el=>{const k=el.dataset.i18n;if(typeof t[k]==='string')el.textContent=t[k]});const sw=$('#languageSwitch');if(sw)sw.textContent=lang==='fr'?'English':'Français'}
function bindLanguage(handler){const sw=$('#languageSwitch');if(sw)sw.addEventListener('click',()=>{const lang=getLang()==='fr'?'en':'fr';setLangPref(lang);handler(lang)})}
function loadChapterContent(chapter){return new Promise((resolve,reject)=>{window.QM1_CHAPTER_CONTENT=null;const s=document.createElement('script');s.src=`${CONTENT_PATHS[chapter]}?v=${VERSION}`;s.onload=()=>window.QM1_CHAPTER_CONTENT?resolve(window.QM1_CHAPTER_CONTENT):reject(new Error('content'));s.onerror=reject;document.head.appendChild(s)})}
async function initialisePortal(){const apply=lang=>{translateStatic(lang);$$('.chapter-card').forEach(card=>{const i=+card.dataset.chapter,c=CHAPTERS[i];card.querySelector('h2').textContent=lang==='fr'?c.fr:c.en;card.querySelector('.chapter-copy>p:last-child').textContent=lang==='fr'?c.leadFr:c.leadEn;card.querySelector('.chapter-copy .eyebrow').textContent=`${I18N[lang].chapterLabel} ${i}`;card.querySelector('.chapter-action a').textContent=I18N[lang].openChapter});refresh(lang)};async function refresh(lang){try{const cfg=await getConfig();let open=0,cards=$$('.chapter-card');cards.forEach(card=>{const yes=Boolean(cfg.chapters?.[card.dataset.chapter]?.open);if(yes)open++;card.classList.toggle('locked',!yes);card.querySelector('.availability').textContent=yes?I18N[lang].available:I18N[lang].later;const a=card.querySelector('a');a.setAttribute('aria-disabled',String(!yes));a.tabIndex=yes?0:-1;a.onclick=yes?null:e=>e.preventDefault()});$('#courseProgress').textContent=I18N[lang].courseAvailable(open,cards.length);$('#courseBar').style.width=`${100*open/cards.length}%`}catch(e){$('#courseProgress').textContent=I18N[lang].offline}}const lang=getLang();setLangPref(lang);apply(lang);bindLanguage(apply)}

async function loadRevisedWorksheets(){try{const r=await fetch('revised-worksheets-2026.json?v='+VERSION,{cache:'no-store'});if(!r.ok)throw new Error('revised');return await r.json()}catch(e){return null}}
async function loadSupplementaryExercises(){try{const r=await fetch('exercise-data-export.json?v='+VERSION,{cache:'no-store'});if(!r.ok)throw new Error('extras');return await r.json()}catch(e){return null}}
function supplementHtml(chapter,lang,kind,source){
 const selected={'1':[1,2,3,4],'2':[0,1],'3':[0,1],'4':[1],'5':[1],'6':[0,1]};
 const items=source&&source.extended&&source.extended[chapter];
 const picks=selected[chapter]||[];
 if(!Array.isArray(items)||!picks.length)return '';
 const fr=lang==='fr',sol=kind==='solution';
 const title=sol?(fr?'Corrigés des exercices complémentaires':'Additional practice — solutions'):(fr?'Exercices complémentaires':'Additional practice');
 const cards=picks.map((idx,k)=>{
  const entry=items[idx];if(!entry)return '';
  const v=fr?entry.fr:entry;if(!v)return '';
  const heading='<h3>'+(fr?'Complément ':'Extra ')+(k+1)+' — '+(v.title||entry.title)+'</h3>';
  if(sol)return '<section class="solution-block">'+heading+(v.solution||'')+'</section>';
  const hint=v.hint?'<details class="qm1-hint"><summary>'+(fr?'Indice méthodologique':'Method hint')+'</summary><p>'+v.hint+'</p></details>':'';
  return '<section class="exercise-block">'+heading+(v.question||'')+hint+'</section>';
 }).join('');
 return '<article class="integrated-card '+(sol?'solution-card ':'')+'supplementary-card"><p class="eyebrow">'+(fr?'ENTRAÎNEMENT APPROFONDI':'ADVANCED PRACTICE')+'</p><h2>'+title+'</h2>'+cards+'</article>';
}


function worksheetSections(markup){
 const host=document.createElement('div');host.innerHTML=markup;
 const article=host.querySelector('article.revised-card');
 if(!article)return null;
 const groups=[],intro=[];let current=null;
 for(const node of [...article.childNodes]){
  const html=node.nodeType===1?node.outerHTML:(node.textContent||'');
  if(node.nodeType===1&&node.matches('h3.worksheet-exercise-title')){
   const title=node.textContent.replace(/\s+/g,' ').trim();
   const m=title.match(/^(?:Exercice|Exercise)\s+(\d+)\b|^(?:Case|Cas)\s+([A-Z])\b/i);
   const key=m?(m[1]?'E'+m[1]:'C'+m[2].toUpperCase()):'U'+groups.length;
   if(current&&current.key===key)current.html+=html;
   else{current={key,html};groups.push(current)}
  }else if(current)current.html+=html;
  else intro.push(html);
 }
 return {intro:intro.join(''),groups};
}
function renderPairedWorksheet(chapter,lang,statement,solution,extras){
 const fr=lang==='fr';
 const note='<p class="qm1-locked-note">'+(fr?'Corrigé disponible immédiatement sous cet exercice après saisie du code de séance (en haut de la page).':'The solution to this exercise appears immediately below after entering the session code (at the top of the page).')+'</p>';
 const q=worksheetSections(statement),a=worksheetSections(solution);
 let html='';
 if(q&&a&&q.groups.length){
  const answerMap=new Map(a.groups.map(g=>[g.key,g.html]));
  html='<article class="integrated-card revised-card qm1-worksheet-intro">'+q.intro+'</article>';
  html+=q.groups.map((part,i)=>{
   const answer=answerMap.get(part.key);
   if(!answer)console.warn('QM1: missing paired solution',chapter,lang,part.key);
   return '<article class="integrated-card revised-card qm1-exercise-pair" data-exercise="'+part.key+'"><section class="exercise-block">'+part.html+'</section>'+note+'<section class="solution-block solution-only qm1-exercise-solution" aria-label="'+(fr?'Corrigé de l’exercice':'Exercise solution')+'">'+(answer||'<p>Solution unavailable.</p>')+'</section></article>';
  }).join('');
 }else{
  // Preserve the legacy content as a safe fallback if the revised worksheet cannot load.
  const qRoot=document.createElement('div'),aRoot=document.createElement('div');
  qRoot.innerHTML=statement;aRoot.innerHTML=solution;
  const qBlocks=[...qRoot.querySelectorAll('.exercise-block')],aBlocks=[...aRoot.querySelectorAll('.solution-block')];
  if(qBlocks.length&&qBlocks.length===aBlocks.length){
   html=qBlocks.map((block,i)=>'<article class="integrated-card qm1-exercise-pair">'+block.outerHTML+note+'<div class="solution-only qm1-exercise-solution">'+aBlocks[i].outerHTML+'</div></article>').join('');
  }else html=statement+'<section class="solution-only">'+solution+'</section>';
 }
 const extrasQ=supplementHtml(chapter,lang,'statement',extras);
 const extrasA=supplementHtml(chapter,lang,'solution',extras);
 if(extrasQ&&extrasA){
  const qRoot=document.createElement('div'),aRoot=document.createElement('div');
  qRoot.innerHTML=extrasQ;aRoot.innerHTML=extrasA;
  const qBlocks=[...qRoot.querySelectorAll('.exercise-block')],aBlocks=[...aRoot.querySelectorAll('.solution-block')];
  if(qBlocks.length===aBlocks.length){
   html+='<article class="integrated-card supplementary-card qm1-supplement-intro"><p class="eyebrow">'+(fr?'ENTRAÎNEMENT APPROFONDI':'ADVANCED PRACTICE')+'</p><h2>'+(fr?'Exercices complémentaires':'Additional practice')+'</h2></article>';
   html+=qBlocks.map((block,i)=>'<article class="integrated-card supplementary-card qm1-exercise-pair">'+block.outerHTML+note+'<div class="solution-only qm1-exercise-solution">'+aBlocks[i].outerHTML+'</div></article>').join('');
  }else console.warn('QM1: supplementary pairing mismatch',chapter,lang,qBlocks.length,aBlocks.length);
 }
 return html;
}

async function initialiseChapter(){const chapter=document.body.dataset.chapter,c=CHAPTERS[chapter],prefix=`qm1-v4-ch${chapter}`;let cfg=null,unlocked=sessionStorage.getItem(`${prefix}-unlocked`)==='1',contentApi=null;ensureMathJax();try{contentApi=await loadChapterContent(chapter)}catch(e){contentApi={statement:lang=>`<article class="integrated-card"><h2>${lang==='fr'?'Contenu momentanément indisponible':'Content temporarily unavailable'}</h2></article>`,solution:()=>''}}const [revisedAll,extraAll]=await Promise.all([loadRevisedWorksheets(),loadSupplementaryExercises()]);const revised=revisedAll&&revisedAll[chapter];const access=$('.access-card'),statementHost=document.createElement('section');statementHost.id='statementHost';access.after(statementHost);$$('.viewer-card').forEach(el=>el.remove());function renderContent(lang){if(window.MathJax&&typeof window.MathJax.typesetClear==='function')window.MathJax.typesetClear([statementHost]);const statement=(revised&&revised[lang]&&revised[lang].statement)||contentApi.statement(lang);const solution=(revised&&revised[lang]&&revised[lang].solution)||contentApi.solution(lang);statementHost.innerHTML=renderPairedWorksheet(chapter,lang,statement,solution,extraAll);typesetMath(statementHost)}function updateLanguage(lang){translateStatic(lang);$('#chapterTitle').textContent=lang==='fr'?c.fr:c.en;$('#chapterLead').textContent=lang==='fr'?c.leadFr:c.leadEn;$('#accessCode').placeholder=lang==='fr'?'Saisir le code de la séance':'Enter the session code';renderContent(lang);$('#statusText').textContent=unlocked?I18N[lang].open:I18N[lang].locked;$('#hideSolutions').textContent=I18N[lang].hide}function setSolutions(open,message=''){unlocked=open;document.body.classList.toggle('solutions-visible',open);$('#statusDot').classList.toggle('open',open);if(open)sessionStorage.setItem(`${prefix}-unlocked`,'1');else sessionStorage.removeItem(`${prefix}-unlocked`);$('#hideSolutions').hidden=!open;if(message)$('#codeMessage').textContent=message;updateLanguage(getLang())}async function refresh(){try{const all=await getConfig();cfg=all.chapters?.[chapter];const chapterOpen=Boolean(cfg?.open);$('#chapterGate').hidden=chapterOpen;document.body.classList.toggle('chapter-locked',!chapterOpen);if(!chapterOpen)return;if(cfg.solutionsOpen&&!unlocked){setSolutions(true,all.messageWhenOpen||'');return}$('#statusDot').classList.toggle('open',unlocked);$('#statusText').textContent=unlocked?I18N[getLang()].open:I18N[getLang()].locked}catch(e){$('#statusText').textContent=unlocked?I18N[getLang()].open:'Offline mode'}}$('#codeForm').addEventListener('submit',async e=>{e.preventDefault();const code=$('#accessCode').value.trim();if(!code||!cfg)return;const hash=await sha256(code);if(hash===cfg.codeHash){setSolutions(true,I18N[getLang()].correct);$('#accessCode').value=''}else $('#codeMessage').textContent=I18N[getLang()].incorrect});$('#hideSolutions').addEventListener('click',()=>setSolutions(false,I18N[getLang()].hidden));const lang=getLang();setLangPref(lang);updateLanguage(lang);bindLanguage(updateLanguage);await refresh();setInterval(refresh,15000)}
if(page==='portal')initialisePortal();if(page==='chapter')initialiseChapter();