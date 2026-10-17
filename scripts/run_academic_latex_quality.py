#!/usr/bin/env python3
"""Run the high-assurance PDF build with final-output prose accounting."""
import re
import build_academic_latex_quality as q

_original_quality_prepare=q.prepare_html_quality

def prepare_final(rendered,name,lang,kind):
    html,_=_original_quality_prepare(rendered,name,lang,kind)
    # Completeness recall must compare the PDF with the exact post-filter HTML:
    # exercise PDFs exclude solutions; solution PDFs include them.
    q.SOURCE_PROSE[name]=q.prose_from_html(html)
    # Count only figures that remain in the final PDF HTML, not temporary assets
    # created before solution blocks are removed from statement-only PDFs.
    actual=len(re.findall(r'assets/[^"\']+\.pdf',html))
    q.CHART_COUNTS[name]=actual
    return html,actual

q.base.prepare_html=prepare_final

if __name__=="__main__":
    q.base.main()
    q.audit_outputs()
