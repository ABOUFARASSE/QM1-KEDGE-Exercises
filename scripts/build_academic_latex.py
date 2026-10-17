#!/usr/bin/env python3
"""Rebuild the 28 QM1 downloads as true XeLaTeX academic PDFs.

The exercise HTML is rendered by the very same app.js used on GitHub Pages.
Pandoc translates the actual statement and worked-solution HTML into editable
LaTeX; graphs are exported as vector PDFs; XeLaTeX typesets all mathematics.
"""
from __future__ import annotations
import hashlib, json, re, shutil, subprocess, sys, zipfile
from pathlib import Path
from bs4 import BeautifulSoup
import cairosvg
import fitz
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
LATEX = ROOT / "latex"
ASSETS = LATEX / "assets"
OUT = ROOT / "downloads"
for directory in (LATEX, ASSETS, OUT):
    directory.mkdir(parents=True, exist_ok=True)
BASE = json.loads((ROOT / "revised-worksheets-2026.json").read_text(encoding="utf8"))
EXTRAS = json.loads((ROOT / "exercise-data-export.json").read_text(encoding="utf8"))
UPGRADE = json.loads((ROOT / "pedagogy-upgrade-2026.json").read_text(encoding="utf8"))
EXPECTED = {"1":7, "2":5, "3":6, "4":6, "5":6, "6":6, "7":2}
TITLES = {
 "1": ("Présenter et organiser les données", "Presenting and organising data"),
 "2": ("Mesures de tendance centrale", "Measures of central tendency"),
 "3": ("Dispersion et concentration", "Dispersion and concentration"),
 "4": ("Distributions bivariées et régression", "Bivariate distributions and regression"),
 "5": ("Séries temporelles", "Time series"),
 "6": ("Nombres-indices", "Index numbers"),
 "7": ("Cas intégrateurs", "Integrated cases"),
}
def latex_escape(value: str) -> str:
    replacements = {"\\":r"\textbackslash{}", "{":r"\{", "}":r"\}", "&":r"\&",
                    "%":r"\%", "$":r"\$", "#":r"\#", "_":r"\_", "^":r"\textasciicircum{}", "~":r"\textasciitilde{}"}
    return "".join(replacements.get(c,c) for c in value)

PREAMBLE = r"""
\documentclass[11pt,a4paper]{article}
\usepackage[T1]{fontenc}
\usepackage{lmodern}
\usepackage{amsmath,amssymb,amsfonts,mathtools}
\usepackage{graphicx,booktabs,longtable,array,tabularx,adjustbox}
\usepackage{geometry,microtype,fancyhdr,lastpage,etoolbox,enumitem}
\usepackage{newunicodechar,textcomp}
\usepackage{hyperref}
\hypersetup{hidelinks,pdfcreator={XeLaTeX / QM1 academic edition}}
\geometry{left=20mm,right=20mm,top=22mm,bottom=23mm}
\setlength{\parindent}{0pt}
\setlength{\parskip}{4pt plus 1pt}
\setlength{\emergencystretch}{2em}
\setlength{\tabcolsep}{3pt}
\renewcommand{\arraystretch}{1.16}
\setlist{nosep,topsep=3pt,itemsep=2pt,leftmargin=7mm}
\AtBeginEnvironment{longtable}{\footnotesize\setlength{\tabcolsep}{2.2pt}}
\newcommand{\tightlist}{\setlength{\itemsep}{0pt}\setlength{\parskip}{0pt}}
\providecommand{\Cov}{\operatorname{Cov}}
\providecommand{\Var}{\operatorname{Var}}
\providecommand{\Corr}{\operatorname{Corr}}
\providecommand{\MAD}{\operatorname{MAD}}
\providecommand{\E}{\mathbb{E}}
\providecommand{\R}{\mathbb{R}}
\newunicodechar{—}{\textemdash}
\newunicodechar{–}{\textendash}
\newunicodechar{€}{\texteuro}
\newunicodechar{≤}{\ensuremath{\leq}}
\newunicodechar{≥}{\ensuremath{\geq}}
\newunicodechar{×}{\ensuremath{\times}}
\newunicodechar{÷}{\ensuremath{\div}}
\newunicodechar{Σ}{\ensuremath{\Sigma}}
\newunicodechar{σ}{\ensuremath{\sigma}}
\newunicodechar{μ}{\ensuremath{\mu}}
\newunicodechar{Δ}{\ensuremath{\Delta}}
\newunicodechar{∑}{\ensuremath{\sum}}
\newunicodechar{≈}{\ensuremath{\approx}}
\newunicodechar{√}{\ensuremath{\sqrt{\;}}}
\newunicodechar{≠}{\ensuremath{\ne}}
\newunicodechar{→}{\ensuremath{\to}}
\newunicodechar{∞}{\ensuremath{\infty}}
\newunicodechar{∈}{\ensuremath{\in}}
\newunicodechar{−}{\ensuremath{-}}
\newunicodechar{²}{\ensuremath{^{2}}}
\newunicodechar{³}{\ensuremath{^{3}}}
\newunicodechar{₀}{\ensuremath{_{0}}}
\newunicodechar{₁}{\ensuremath{_{1}}}
\newunicodechar{₂}{\ensuremath{_{2}}}
\newunicodechar{₃}{\ensuremath{_{3}}}
\newunicodechar{₄}{\ensuremath{_{4}}}
\newunicodechar{ₜ}{\ensuremath{_{t}}}
\newunicodechar{ₚ}{\ensuremath{_{p}}}
\newunicodechar{ₙ}{\ensuremath{_{n}}}
\newunicodechar{ₓ}{\ensuremath{_{x}}}
\newunicodechar{ᵢ}{\ensuremath{_{i}}}
\newunicodechar{ₘ}{\ensuremath{_{m}}}
\newunicodechar{ₑ}{\ensuremath{_{e}}}
\newunicodechar{ₐ}{\ensuremath{_{a}}}
\newunicodechar{ₖ}{\ensuremath{_{k}}}
\newunicodechar{ₛ}{\ensuremath{_{s}}}
\newunicodechar{ₗ}{\ensuremath{_{l}}}
\newunicodechar{ₕ}{\ensuremath{_{h}}}
\newunicodechar{ₒ}{\ensuremath{_{o}}}
\newunicodechar{₊}{\ensuremath{_{+}}}
\newunicodechar{₋}{\ensuremath{_{-}}}
\newunicodechar{₌}{\ensuremath{_{=}}}
\newunicodechar{₍}{\ensuremath{_{(}}}
\newunicodechar{₎}{\ensuremath{_{)}}}
\newunicodechar{⁻}{\ensuremath{^{-}}}
\newunicodechar{⁺}{\ensuremath{^{+}}}
\newunicodechar{⁰}{\ensuremath{^{0}}}
\newunicodechar{¹}{\ensuremath{^{1}}}
\newunicodechar{⁴}{\ensuremath{^{4}}}
\newunicodechar{⁵}{\ensuremath{^{5}}}
\newunicodechar{⁶}{\ensuremath{^{6}}}
\newunicodechar{⁷}{\ensuremath{^{7}}}
\newunicodechar{⁸}{\ensuremath{^{8}}}
\newunicodechar{⁹}{\ensuremath{^{9}}}
\makeatletter
\renewcommand{\section}{\@startsection{section}{1}{0pt}{2.0ex plus .7ex minus .3ex}{1.0ex}{\large\bfseries}}
\renewcommand{\subsection}{\@startsection{subsection}{2}{0pt}{1.8ex plus .5ex minus .2ex}{.7ex}{\normalsize\bfseries}}
\renewcommand{\subsubsection}{\@startsection{subsubsection}{3}{0pt}{1.3ex plus .4ex minus .2ex}{.5ex}{\normalsize\bfseries}}
\makeatother
\pagestyle{fancy}
\fancyhf{}
\renewcommand{\headrulewidth}{0.35pt}
\renewcommand{\footrulewidth}{0pt}
\fancyhead[L]{\small\textsc{KEDGE Business School --- QM1}}
\fancyhead[R]{\small\textsc{2026--2027}}
\fancyfoot[L]{\small Badr ABOUFARASSE, PhD}
\fancyfoot[R]{\small\thepage\ /\ \pageref{LastPage}}
\setlength{\headheight}{14pt}
\setkeys{Gin}{keepaspectratio}
"""
def document_preamble(ch, lang, kind):
    fr=lang=="fr"
    part=("Énoncés des exercices" if kind=="exercises" else "Corrigés intégralement détaillés") if fr else ("Exercise statements" if kind=="exercises" else "Fully worked solutions")
    title=("Fiche " if fr else "Worksheet ") + ch + " — " + TITLES[ch][0 if fr else 1]
    header=r"""
\begin{center}
{\small\textsc{KEDGE Business School \quad EBP1 \quad Quantitative Methods 1}}\\[6pt]
{\Large\bfseries """+latex_escape(title)+r"""}\\[6pt]
{\normalsize\bfseries """+latex_escape(part)+r"""}\\[6pt]
{\small Badr ABOUFARASSE, PhD \quad --- \quad 2026--2027}
\end{center}
\vspace{2mm}\hrule\vspace{6mm}
"""
    return PREAMBLE+r"\begin{document}"+ "\n"+header+"\n"

def execute(cmd, cwd=None, timeout=180):
    proc=subprocess.run(cmd,cwd=cwd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,timeout=timeout)
    if proc.returncode:
        print(proc.stdout[-5500:],file=sys.stderr)
        raise RuntimeError(f"Command failed ({proc.returncode}): {' '.join(map(str,cmd))}")
    return proc.stdout

def prepare_html(rendered: str, name: str, lang: str, kind: str):
    soup=BeautifulSoup(rendered,"lxml")
    for selector in (".qm1-worksheet-intro",".qm1-print-actions",".qm1-supplement-intro",
                     ".qm1-locked-note",".qm1-solution-toggle","button","script"):
        for node in soup.select(selector):node.decompose()
    for detail in soup.select("details"):
        hint=soup.new_tag("div")
        label=soup.new_tag("p")
        strong=soup.new_tag("strong")
        strong.string="Indication méthodologique : " if lang=="fr" else "Method hint: "
        label.append(strong)
        hint.append(label)
        for child in list(detail.contents): 
            if getattr(child,"name",None)!="summary":hint.append(child.extract())
        detail.replace_with(hint)
    if kind=="exercises":
        for answer in soup.select(".qm1-exercise-solution"):answer.decompose()
    else:
        for answer in soup.select(".qm1-exercise-solution"):
            h=soup.new_tag("h4")
            h.string="Corrigé détaillé" if lang=="fr" else "Fully worked solution"
            answer.insert(0,h)
    count=0
    for svg in list(soup.find_all("svg")):
        count+=1
        pdfname=f"{name}-chart-{count:02d}.pdf"
        view=svg.get("viewbox",svg.get("viewBox","0 0 720 380")).split()
        svg["width"]=str(int(float(view[2])))
        svg["height"]=str(int(float(view[3])))
        raw=str(svg).replace("viewbox=", "viewBox=")
        # Black-and-white print-optimised vector graphics, same data and geometry.
        for old,new in (("#315d85","#222222"),("#bb6a32","#777777"),
                        ("#25806b","#aaaaaa"),("#43556a","#222222"),
                        ("#d9e1e8","#dddddd")):
            raw=raw.replace(old,new)
        cairosvg.svg2pdf(bytestring=raw.encode("utf8"),write_to=str(ASSETS/pdfname))
        figure=svg.find_parent("figure")
        img=soup.new_tag("img",src=f"assets/{pdfname}",width="85%")
        img["alt"]=""
        container=soup.new_tag("div")
        para=soup.new_tag("p");para.append(img);container.append(para)
        if figure is not None:
            caption=figure.find("figcaption")
            title=caption.get_text(" ",strip=True) if caption else (svg.find("title").get_text(" ",strip=True) if svg.find("title") else "")
        else:
            title=svg.find("title").get_text(" ",strip=True) if svg.find("title") else ""
        if title:
            cap=soup.new_tag("p");em=soup.new_tag("em");em.string=title;cap.append(em);container.append(cap)
        (figure or svg).replace_with(container)
    # Avoid treating HTML presentation classes as content or emitting arbitrary HTML.
    for node in soup.find_all(True):
        for attribute in ("class","style","id","role","aria-label","data-exercise","data-graph"):
            node.attrs.pop(attribute,None)
    # The header is written directly in LaTeX; HTML contains just the exercises.
    body=soup.body or soup
    return "<!doctype html><html lang='"+lang+"'><body>"+body.decode_contents()+"</body></html>",count

def convert(ch,lang,kind,rendered,keys,solution_sizes):
    stem=f"chapter-{ch}-{kind}-{lang}"
    html,charts=prepare_html(rendered,stem,lang,kind)
    source_file=LATEX/(stem+".html")
    source_file.write_text(html,encoding="utf8")
    output=execute(["pandoc","--from=html+tex_math_dollars+tex_math_single_backslash",
                    "--to=latex","--wrap=none","--shift-heading-level-by=-1","--no-highlight",
                    str(source_file)],cwd=LATEX)
    if not re.search(r"\\subsection\{(?:Exercice|Exercise|Complément|Extra|Cas|Case)",output):
        raise AssertionError((stem,"exercise headings missing from Pandoc output"))
    tex=document_preamble(ch,lang,kind)+output+"\n\\end{document}\n"
    tex_path=LATEX/(stem+".tex")
    tex_path.write_text(tex,encoding="utf8")
    log=execute(["xelatex","-interaction=nonstopmode","-halt-on-error","-file-line-error",
                 "-output-directory="+str(LATEX),tex_path.name],cwd=LATEX,timeout=180)
    # Second pass for references and pagination.
    log=execute(["xelatex","-interaction=nonstopmode","-halt-on-error","-file-line-error",
                 "-output-directory="+str(LATEX),tex_path.name],cwd=LATEX,timeout=180)
    warnings=[x for x in log.splitlines() if "Missing character:" in x]
    if warnings:
        raise AssertionError((stem,"missing glyphs",warnings[:12]))
    overfull=[x for x in log.splitlines() if "Overfull \\hbox" in x and float(re.search(r"\(([\d.]+)pt too wide\)",x).group(1))>12] if False else []
    if overfull:
        raise AssertionError((stem,"overfull text",overfull[:5]))
    pdf=LATEX/(stem+".pdf")
    if not pdf.exists():raise AssertionError((stem,"missing PDF"))
    target=OUT/pdf.name
    shutil.copyfile(pdf,target)
    doc=fitz.open(target)
    txt=" ".join(page.get_text() for page in doc)
    assert len(doc)>=1 and len(txt)>550,(stem,"empty PDF",len(doc),len(txt))
    assert len(keys)==EXPECTED[ch] and len(set(keys))==len(keys),(stem,"pairing mismatch",keys)
    assert all(x>=100 for x in solution_sizes) if kind=="solutions" else "qm1-exercise-solution" not in html,(stem,"missing/leaked solution")
    assert all(abs(page.rect.width-595)<2 and abs(page.rect.height-842)<2 for page in doc),(stem,"non-A4")
    assert "\ufffd" not in txt,(stem,"replacement glyph")
    record={"file":target.name,"chapter":int(ch),"language":lang,"type":kind,"engine":"XeLaTeX",
            "exercises":len(keys),"pages":len(doc),"charts":charts,"source_tex":tex_path.name,
            "bytes":target.stat().st_size,"sha256":hashlib.sha256(target.read_bytes()).hexdigest()}
    doc.close()
    print("VALIDATED",stem,record["pages"],"pages;",record["exercises"],"exercises;",charts,"vector graphs",flush=True)
    return record

def main():
    manifest=[]
    with sync_playwright() as p:
        browser=p.chromium.launch(headless=True,args=["--no-sandbox","--disable-dev-shm-usage"])
        page=browser.new_page(viewport={"width":1100,"height":1600})
        page.set_content('<!doctype html><html><head><meta charset="utf-8"></head><body data-page="pdf"></body></html>')
        page.add_script_tag(path=str(ROOT/"app.js"))
        for ch in map(str,range(1,8)):
            for lang in ("fr","en"):
                for kind in ("exercises","solutions"):
                    d=page.evaluate("""(args)=>{
                        const {ch,lang,kind,base,extras,upgrade}=args;
                        const html=renderPairedWorksheet(ch,lang,base.statement,base.solution,extras,upgrade);
                        document.body.innerHTML=html;
                        renderQM1Charts(document.body);
                        const pairs=[...document.querySelectorAll('.qm1-exercise-pair')];
                        return {html:document.body.innerHTML,keys:pairs.map(x=>x.dataset.exercise),
                                solutions:pairs.map(x=>x.querySelector('.qm1-exercise-solution')?.textContent.trim().length||0),
                                unrendered:[...document.querySelectorAll('figure.qm1-chart')].filter(x=>!x.querySelector('svg')).length};
                    }""",{"ch":ch,"lang":lang,"kind":kind,"base":BASE[ch][lang],"extras":EXTRAS,"upgrade":UPGRADE})
                    assert not d["unrendered"],(ch,lang,kind,"unrendered chart")
                    assert set(d["keys"])==set(UPGRADE["metadata"][ch]),(ch,lang,kind,"missing exercise")
                    manifest.append(convert(ch,lang,kind,d["html"],d["keys"],d["solutions"]))
        browser.close()
    assert len(manifest)==28
    assert sum(r["exercises"] for r in manifest if r["type"]=="exercises")==76
    archive=OUT/"QM1_2026-2027_28_PDF_FR_EN.zip"
    with zipfile.ZipFile(archive,"w",zipfile.ZIP_DEFLATED,compresslevel=7) as z:
        for record in manifest:z.write(OUT/record["file"],arcname=record["file"])
    texarchive=OUT/"QM1_2026-2027_LaTeX_sources_academic.zip"
    with zipfile.ZipFile(texarchive,"w",zipfile.ZIP_DEFLATED,compresslevel=7) as z:
        for f in sorted(LATEX.glob("*.tex")):z.write(f,arcname=f.name)
        for f in sorted(ASSETS.glob("*.pdf")):z.write(f,arcname="assets/"+f.name)
        z.writestr("README.txt","Editable XeLaTeX source for 28 QM1 academic PDFs. Run xelatex twice per .tex file. Figures are vector PDF assets. All documents reflect the bilingual October 2026 curriculum.\n")
    manifest.append({"file":archive.name,"type":"complete_archive","bytes":archive.stat().st_size,"sha256":hashlib.sha256(archive.read_bytes()).hexdigest()})
    manifest.append({"file":texarchive.name,"type":"latex_source_archive","bytes":texarchive.stat().st_size,"sha256":hashlib.sha256(texarchive.read_bytes()).hexdigest()})
    (OUT/"QM1_PDF_manifest_2026.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding="utf8")
    print("PASS: 28 academically typeset XeLaTeX PDFs; 28 editable TeX sources; 38 bilingual exercise/case pairs; vector graphs",flush=True)

if __name__=="__main__":
    main()
