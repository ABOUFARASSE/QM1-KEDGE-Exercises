#!/usr/bin/env python3
"""Generate and audit 28 complete QM1 PDFs using the website's real rendering functions."""
import hashlib, json, os, re, sys, zipfile
from pathlib import Path
import fitz
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'downloads'
OUT.mkdir(exist_ok=True)
BASE=json.loads((ROOT/'revised-worksheets-2026.json').read_text(encoding='utf-8'))
EXTRAS=json.loads((ROOT/'exercise-data-export.json').read_text(encoding='utf-8'))
UPGRADE=json.loads((ROOT/'pedagogy-upgrade-2026.json').read_text(encoding='utf-8'))
TITLES={
'1':('Présenter et organiser les données','Presenting and organising data'),
'2':('Mesures de tendance centrale','Measures of central tendency'),
'3':('Dispersion et concentration','Dispersion and concentration'),
'4':('Distributions bivariées et régression','Bivariate distributions and regression'),
'5':('Séries temporelles','Time series'),
'6':('Nombres-indices','Index numbers'),
'7':('Cas intégrateurs','Integrated cases')}
EXPECTED={'1':7,'2':5,'3':6,'4':6,'5':6,'6':6,'7':2}
MATHJAX=ROOT/'node_modules/mathjax-full/es5/tex-svg.js'
if not MATHJAX.exists(): raise RuntimeError('Install mathjax-full before running.')
CSS=r"""
@page{size:A4;margin:17mm 14mm 19mm}
*{box-sizing:border-box}
html,body{font-family:"Liberation Serif","DejaVu Serif",serif;font-size:11pt;color:#17232e;line-height:1.43}
body{margin:0}
.pdf-cover{border-bottom:1.3px solid #334b5c;padding:16mm 0 12mm;margin-bottom:9mm}
.pdf-cover h1{font-size:22pt;line-height:1.2;margin:7mm 0 3mm}
.pdf-cover h2{font-size:15pt;font-weight:400;margin:0 0 5mm}
.pdf-cover .eyebrow{font:700 9pt "Liberation Sans",sans-serif;letter-spacing:.7px}
.pdf-cover .part{font-weight:700;font-size:12pt}
.pdf-cover .author{font-size:9pt;margin-top:10mm}
.qm1-print-actions,.qm1-locked-note,.qm1-solution-toggle,.qm1-hint summary,.qm1-supplement-intro{display:none!important}
.qm1-worksheet-intro{margin-bottom:7mm}
.qm1-worksheet-intro h2{font-size:13pt}
.qm1-stage{break-before:page}
.qm1-stage-heading{border-bottom:1px solid #9faab5;margin:0 0 5mm}
.qm1-stage-heading h2{font-size:14pt;margin:0 0 2mm}
.qm1-stage-heading p{font-size:9pt;margin:0 0 3mm}
.qm1-exercise-pair{margin:5mm 0 9mm;break-inside:auto}
.qm1-exercise-meta{font:8pt "Liberation Sans",sans-serif;color:#46586b;margin:0 0 2mm}
.exercise-block{margin:0 0 4mm}
.qm1-exercise-solution{display:block!important;visibility:visible!important;border-top:1px solid #9faab5;padding-top:4mm;margin-top:3mm}
.qm1-exercise-solution:before{content:"CORRIGÉ DÉTAILLÉ";display:block;font:700 8pt "Liberation Sans",sans-serif;letter-spacing:.5px;margin:0 0 3mm;color:#36506a}
html[lang=en] .qm1-exercise-solution:before{content:"FULLY WORKED SOLUTION"}
h2,h3,h4{break-after:avoid}
h3{font-size:12pt;margin:4mm 0 2mm}
h4{font-size:11pt}
p{margin:2mm 0 3mm;orphans:3;widows:3}
li{margin:1mm 0;orphans:2;widows:2}
ul,ol{padding-left:6mm}
.table-wrap{overflow:visible!important;max-width:100%}
table{border-collapse:collapse;width:100%;font-size:8.3pt;margin:3mm 0 4mm;table-layout:auto}
thead{display:table-header-group}
tr{break-inside:avoid}
td,th{border:.5px solid #a6b1bb;padding:1.2mm .8mm;text-align:center;vertical-align:middle;overflow-wrap:anywhere}
th{background:#e7edf2}
table td:first-child,table th:first-child{text-align:left}
figure{max-width:100%;margin:4mm auto;break-inside:avoid}
figure svg{width:100%!important;height:auto!important;max-height:95mm}
figcaption{font-size:8pt;color:#526474;text-align:center}
svg text{font-family:"Liberation Sans",sans-serif}
mjx-container{max-width:100%}
mjx-container[display=true]{margin:2.8mm 0!important}
mjx-container svg{max-width:100%}
.qm1-hint{display:block}
.qm1-hint p{display:block}
.center{text-align:center}
"""
MANIFEST=[]
with sync_playwright() as p:
    browser=p.chromium.launch(headless=True,args=['--no-sandbox','--disable-dev-shm-usage'])
    page=browser.new_page(viewport={'width':1120,'height':1500},device_scale_factor=1)
    page.set_content('<!doctype html><html lang="fr"><head><meta charset="utf-8"></head><body data-page="pdf"></body></html>')
    page.add_script_tag(path=str(ROOT/'app.js'))
    page.evaluate("""() => {window.MathJax={
       tex:{inlineMath:[['$','$']],displayMath:[['$$','$$']],processEscapes:true,
       macros:{Cov:'\\\\operatorname{Cov}',Var:'\\\\operatorname{Var}',sd:'\\\\sigma',E:'\\\\mathbb{E}',R:'\\\\mathbb{R}'}},
       svg:{fontCache:'local'},options:{skipHtmlTags:['script','noscript','style','textarea','pre','code'],enableMenu:false}
    }}""")
    page.add_script_tag(path=str(MATHJAX))
    page.wait_for_function("() => window.MathJax && typeof window.MathJax.typesetPromise === 'function'",timeout=30000)
    page.add_style_tag(content=CSS)
    for ch in map(str,range(1,8)):
        for lang in ('fr','en'):
            for kind in ('exercises','solutions'):
                info=page.evaluate("""(d) => {
                    const {ch,lang,kind,base,extras,upgrade,titles}=d;
                    document.documentElement.lang=lang;
                    if(window.MathJax.typesetClear)window.MathJax.typesetClear([document.body]);
                    const result=renderPairedWorksheet(ch,lang,base.statement,base.solution,extras,upgrade);
                    const part=lang==='fr'?(kind==='exercises'?'Énoncés complets':'Corrigés détaillés'):(kind==='exercises'?'Complete exercises':'Fully worked solutions');
                    const title=lang==='fr'?'Fiche '+ch:'Worksheet '+ch;
                    const cover='<header class="pdf-cover"><div class="eyebrow">KEDGE BUSINESS SCHOOL · QM1 · 2026–2027</div><h1>'+title+'</h1><h2>'+titles+'</h2><div class="part">'+part+'</div><div class="author">Badr ABOUFARASSE, PhD</div></header>';
                    document.body.innerHTML=cover+'<main id="pdf-main">'+result+'</main>';
                    for(const hint of document.querySelectorAll('details'))hint.open=true;
                    for(const btn of document.querySelectorAll('.qm1-print-actions,.qm1-locked-note,.qm1-solution-toggle'))btn.remove();
                    if(kind==='exercises')for(const answer of document.querySelectorAll('.qm1-exercise-solution'))answer.remove();
                    renderQM1Charts(document.body);
                    const pairs=[...document.querySelectorAll('.qm1-exercise-pair')];
                    const keys=pairs.map(x=>x.dataset.exercise);
                    const solutions=pairs.map(x=>x.querySelector('.qm1-exercise-solution')?.textContent.trim().length||0);
                    return {keys,solutions,charts:document.querySelectorAll('figure svg').length,
                      unresolved:document.querySelectorAll('figure.qm1-chart[data-graph]').length,
                      title:document.querySelector('h1').textContent};
                }""",{'ch':ch,'lang':lang,'kind':kind,'base':BASE[ch][lang],'extras':EXTRAS,'upgrade':UPGRADE,'titles':TITLES[ch][0 if lang=='fr' else 1]})
                expected=set(UPGRADE['metadata'][ch])
                assert len(info['keys'])==EXPECTED[ch],(ch,lang,kind,info['keys'])
                assert len(set(info['keys']))==EXPECTED[ch],(ch,lang,kind,'duplicate keys',info['keys'])
                assert set(info['keys'])==expected,(ch,lang,kind,'missing',expected-set(info['keys']),'extra',set(info['keys'])-expected)
                if kind=='solutions':assert min(info['solutions'])>=100,(ch,lang,'empty/short solution',info['solutions'])
                else:assert not any(info['solutions']),(ch,lang,'solutions leaked')
                assert info['unresolved']==0,(ch,lang,'unrendered graphs')
                page.evaluate("""async () => {await MathJax.typesetPromise([document.body]);await document.fonts.ready}""")
                errs=page.locator('mjx-merror').all_text_contents()
                assert not errs,(ch,lang,kind,'MathJax errors',errs[:6])
                count_math=page.locator('mjx-container').count()
                assert count_math>=2,(ch,lang,kind,'missing math rendering')
                name=f'chapter-{ch}-{kind}-{lang}.pdf'
                path=OUT/name
                footer='<div style="font-size:8px;color:#526171;width:100%;padding:0 14mm;display:flex;justify-content:space-between"><span>KEDGE QM1 · Badr ABOUFARASSE</span><span><span class="pageNumber"></span> / <span class="totalPages"></span></span></div>'
                page.pdf(path=str(path),format='A4',print_background=True,display_header_footer=True,header_template='<div></div>',footer_template=footer,margin={'top':'17mm','bottom':'19mm','left':'14mm','right':'14mm'},prefer_css_page_size=True)
                pdf=fitz.open(str(path))
                assert len(pdf)>=2 and path.stat().st_size>8000,(name,len(pdf),path.stat().st_size)
                assert all(abs(pg.rect.width-595)<2 and abs(pg.rect.height-842)<2 for pg in pdf),name
                text_content=' '.join(pg.get_text() for pg in pdf)
                assert len(text_content)>500,(name,'not searchable')
                assert 'Solution unavailable' not in text_content and 'Corrigé indisponible' not in text_content,name
                rec={'file':name,'chapter':int(ch),'language':lang,'type':kind,'exercises':len(info['keys']),'pages':len(pdf),
                     'charts':info['charts'],'math_elements':count_math,'bytes':path.stat().st_size,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
                MANIFEST.append(rec)
                print('VALIDATED',name,rec['pages'],'pages;',rec['exercises'],'items;',rec['math_elements'],'equations;',rec['charts'],'graphs',flush=True)
                pdf.close()
    browser.close()
assert len(MANIFEST)==28
assert sum(r['exercises'] for r in MANIFEST if r['type']=='exercises')==76
archive=OUT/'QM1_2026-2027_28_PDF_FR_EN.zip'
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=7) as z:
    for r in MANIFEST:z.write(OUT/r['file'],arcname=r['file'])
MANIFEST.append({'file':archive.name,'type':'complete_archive','bytes':archive.stat().st_size,'sha256':hashlib.sha256(archive.read_bytes()).hexdigest()})
(OUT/'QM1_PDF_manifest_2026.json').write_text(json.dumps(MANIFEST,indent=2,ensure_ascii=False),encoding='utf-8')
print('PASS: 28 PDFs, 38 paired exercises/cases per language, 2 modes, full archive',flush=True)
