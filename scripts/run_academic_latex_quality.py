#!/usr/bin/env python3
"""Run the high-assurance PDF build with final-output prose accounting."""
import build_academic_latex_quality as q

_original_quality_prepare=q.prepare_html_quality

def prepare_final(rendered,name,lang,kind):
    html,count=_original_quality_prepare(rendered,name,lang,kind)
    # Completeness recall must compare the PDF with the exact post-filter HTML:
    # exercise PDFs exclude solutions; solution PDFs include them.
    q.SOURCE_PROSE[name]=q.prose_from_html(html)
    return html,count

q.base.prepare_html=prepare_final

if __name__=="__main__":
    q.base.main()
    q.audit_outputs()
