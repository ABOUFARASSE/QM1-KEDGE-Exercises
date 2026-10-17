#!/usr/bin/env python3
"""High-assurance QM1 LaTeX PDF build.

This wrapper keeps the established XeLaTeX pipeline, but fixes and audits the
figure conversion path that could silently create blank vector figures. It also
checks source-to-PDF prose coverage and suspicious internal white space on all
28 downloadable PDFs before publication.
"""
from __future__ import annotations
import importlib.util, json, re, sys
from collections import Counter
from pathlib import Path
from urllib.parse import unquote

import fitz
import matplotlib.pyplot as plt
import numpy as np
from bs4 import BeautifulSoup

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
spec=importlib.util.spec_from_file_location("qm1_base_builder", HERE/"build_academic_latex.py")
base=importlib.util.module_from_spec(spec); spec.loader.exec_module(base)

SOURCE_PROSE={}
CHART_COUNTS={}


def words(text):
    text=text.lower().replace("’", "'").replace("–", "-").replace("—", "-")
    return re.findall(r"[a-zà-öø-ÿ0-9]+", text)


def prose_from_html(html):
    # TeX/math extraction differs by renderer, so completeness is checked on
    # prose, labels, list items and table text independently of math glyphs.
    html=re.sub(r"\$\$.*?\$\$", " ", html, flags=re.S)
    html=re.sub(r"\$.*?\$", " ", html, flags=re.S)
    soup=BeautifulSoup(html, "lxml")
    for tag in soup(["script", "style", "svg"]):
        tag.decompose()
    return soup.get_text(" ", strip=True)


def recall(source, pdftext):
    a=Counter(words(source)); b=Counter(words(pdftext))
    if not a: return 1.0
    return sum(min(n,b[w]) for w,n in a.items())/sum(a.values())


def graph_pdf(d, path):
    """Render one data-driven QM1 chart as a non-empty vector PDF."""
    fig,ax=plt.subplots(figsize=(6.7,3.5))
    typ=d.get("type")
    xs=d.get("breaks") or d.get("xs") or []
    values=d.get("values") or []
    series=d.get("series") or []
    if typ=="histogram":
        widths=[xs[i+1]-xs[i] for i in range(len(values))]
        ax.bar(xs[:-1],values,width=widths,align="edge",edgecolor="black",linewidth=.7)
    elif typ=="bars":
        ax.bar(xs,values,edgecolor="black",linewidth=.7)
    elif typ=="scatter":
        ax.scatter(xs,values)
        line=d.get("line")
        if line:
            xx=np.array([min(xs),max(xs)],dtype=float)
            ax.plot(xx,line["a"]*xx+line["b"])
    elif typ in ("lines","step"):
        for s in series:
            vals=np.array([np.nan if v is None else v for v in s.get("values",[])],dtype=float)
            if typ=="step":
                ax.step(xs,vals,where="post",marker="o",label=s.get("label", ""))
            else:
                ax.plot(xs,vals,marker="o",label=s.get("label", ""))
        if any(s.get("label") for s in series):
            ax.legend(frameon=False,fontsize=8)
    else:
        plt.close(fig)
        raise AssertionError((path.name,"unsupported graph type",typ))
    marker=d.get("marker")
    if marker:
        ax.scatter([marker["x"]],[marker["y"]],zorder=5)
        ax.annotate(str(marker["y"]),(marker["x"],marker["y"]),xytext=(5,7),textcoords="offset points",fontsize=8)
    if d.get("ymax") is not None:
        ax.set_ylim(0,d["ymax"])
    elif typ in ("bars","histogram"):
        ax.set_ylim(bottom=0)
    ax.set_xlabel(d.get("xlabel","x"),fontsize=9)
    ax.set_ylabel(d.get("ylabel","y"),fontsize=9)
    ax.tick_params(labelsize=8)
    ax.grid(axis="y",alpha=.22,linewidth=.6)
    ax.spines[["top","right"]].set_visible(False)
    fig.tight_layout(); fig.savefig(path,format="pdf",bbox_inches="tight"); plt.close(fig)
    doc=fitz.open(path); pg=doc[0]
    ok=bool(pg.get_drawings() or pg.get_text().strip())
    doc.close()
    if not ok:
        raise AssertionError((path.name,"blank vector chart"))


_original_prepare=base.prepare_html

def prepare_html_quality(rendered, name, lang, kind):
    soup=BeautifulSoup(rendered,"lxml")
    # The revised Chapter 1 overlay already supplies better data-driven versions
    # of the two legacy static charts. Keeping both created duplicate/orphan
    # captions and unnecessary white space, so the two legacy duplicates are
    # removed only in Chapter 1.
    if name.startswith("chapter-1-"):
        for f in list(soup.select("figure.qm1-chart:not([data-graph])")):
            f.decompose()
    n=0
    for f in list(soup.select("figure.qm1-chart[data-graph]")):
        n+=1
        try:
            d=json.loads(unquote(f.get("data-graph", "")))
        except Exception as exc:
            raise AssertionError((name,n,"invalid graph specification")) from exc
        pdfname=f"{name}-datachart-{n:02d}.pdf"
        graph_pdf(d,base.ASSETS/pdfname)
        img=soup.new_tag("img",src=f"assets/{pdfname}",width="82%"); img["alt"]=""
        holder=soup.new_tag("div"); p=soup.new_tag("p"); p.append(img); holder.append(p)
        cap=f.find("figcaption"); title=cap.get_text(" ",strip=True) if cap else d.get("title", "")
        if title:
            cp=soup.new_tag("p"); em=soup.new_tag("em"); em.string=title; cp.append(em); holder.append(cp)
        f.replace_with(holder)
    preprocessed=str(soup)
    SOURCE_PROSE[name]=prose_from_html(preprocessed)
    html,static_count=_original_prepare(preprocessed,name,lang,kind)
    CHART_COUNTS[name]=n+static_count
    return html,n+static_count

base.prepare_html=prepare_html_quality


def page_gaps(page):
    """Return large internal gaps after considering text, drawings and images."""
    bands=[]
    top,bottom=65,page.rect.height-55
    for b in page.get_text("blocks"):
        if b[3]>=top and b[1]<=bottom:
            bands.append((max(top,b[1]),min(bottom,b[3])))
    for d in page.get_drawings():
        r=d.get("rect")
        if r and r.y1>=top and r.y0<=bottom:
            bands.append((max(top,r.y0),min(bottom,r.y1)))
    for im in page.get_image_info():
        r=fitz.Rect(im["bbox"])
        if r.y1>=top and r.y0<=bottom:
            bands.append((max(top,r.y0),min(bottom,r.y1)))
    bands=sorted((a,b) for a,b in bands if b>a)
    merged=[]
    for a,b in bands:
        if not merged or a>merged[-1][1]+6: merged.append([a,b])
        else: merged[-1][1]=max(merged[-1][1],b)
    return [merged[i+1][0]-merged[i][1] for i in range(len(merged)-1)]


def audit_outputs():
    report=[]
    failures=[]
    for pdf in sorted(base.OUT.glob("chapter-*-*.pdf")):
        stem=pdf.stem
        doc=fitz.open(pdf)
        text=" ".join(p.get_text() for p in doc)
        src=SOURCE_PROSE.get(stem, "")
        r=recall(src,text)
        suspicious=[]
        for i,p in enumerate(doc):
            gaps=page_gaps(p)
            if gaps and max(gaps)>210:
                suspicious.append({"page":i+1,"gap_pt":round(max(gaps),1)})
        if r<0.93: failures.append((stem,"prose recall",round(r,4)))
        if suspicious: failures.append((stem,"suspicious whitespace",suspicious))
        if any(abs(p.rect.width-595)>2 or abs(p.rect.height-842)>2 for p in doc):
            failures.append((stem,"non-A4"))
        if "\ufffd" in text: failures.append((stem,"replacement glyph"))
        report.append({"file":pdf.name,"pages":len(doc),"prose_recall":round(r,4),
                       "charts":CHART_COUNTS.get(stem,0),"suspicious_whitespace":suspicious})
        doc.close()
    if len(report)!=28: failures.append(("corpus","expected 28 PDFs",len(report)))
    # Every vector chart asset must contain actual marks/text; blank graphics are
    # forbidden because they are visually indistinguishable from missing content.
    blank=[]
    for asset in sorted(base.ASSETS.glob("*.pdf")):
        d=fitz.open(asset); p=d[0]
        if not p.get_drawings() and not p.get_text().strip(): blank.append(asset.name)
        d.close()
    if blank: failures.append(("assets","blank charts",blank))
    quality=base.OUT/"QM1_PDF_quality_audit_2026.json"
    quality.write_text(json.dumps({"status":"PASS" if not failures else "FAIL",
                                   "pdf_count":len(report),"documents":report,"failures":failures},
                                  ensure_ascii=False,indent=2),encoding="utf8")
    if failures:
        raise AssertionError(failures)
    print("PASS: visual-completeness QA: 28 PDFs, no blank charts, no suspicious internal whitespace, prose recall >= 93%")


if __name__=="__main__":
    base.main()
    audit_outputs()
