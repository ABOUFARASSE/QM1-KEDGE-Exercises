from pathlib import Path
from io import BytesIO
import json, re

from bs4 import BeautifulSoup, NavigableString, Tag
import cairosvg
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle,
    ListFlowable, ListItem, Image, KeepTogether
)

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'downloads'
OUT.mkdir(exist_ok=True)
DATA = json.loads((ROOT / 'exercise-data-export.json').read_text(encoding='utf-8'))

pdfmetrics.registerFont(TTFont('DejaVu', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'))
pdfmetrics.registerFont(TTFont('DejaVu-Bold', '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'))
pdfmetrics.registerFont(TTFont('DejaVu-Oblique', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'))

RED = colors.HexColor('#E40046')
BLUE = colors.HexColor('#234F76')
INK = colors.HexColor('#17171A')
MUTED = colors.HexColor('#62636B')
LINE = colors.HexColor('#D9DADF')
SOFT = colors.HexColor('#F5F5F7')

CHAPTERS = {
    1: {'en': 'Data Presentation', 'fr': 'Présentation des données'},
    2: {'en': 'Measures of Central Tendency', 'fr': 'Mesures de tendance centrale'},
    3: {'en': 'Dispersion and Concentration', 'fr': 'Dispersion et concentration'},
    4: {'en': 'Bivariate Distributions', 'fr': 'Distributions bivariées'},
    5: {'en': 'Time Series', 'fr': 'Séries temporelles'},
    6: {'en': 'Statistical Index Numbers', 'fr': 'Nombres-indices statistiques'},
}

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='BodyDV', parent=styles['BodyText'], fontName='DejaVu', fontSize=11.2, leading=17, textColor=INK, spaceAfter=7))
styles.add(ParagraphStyle(name='QuestionDV', parent=styles['BodyDV'], fontSize=11.6, leading=18))
styles.add(ParagraphStyle(name='SmallDV', parent=styles['BodyDV'], fontSize=9.3, leading=13, textColor=MUTED))
styles.add(ParagraphStyle(name='ExerciseTitle', parent=styles['Heading2'], fontName='DejaVu-Bold', fontSize=18, leading=22, textColor=INK, spaceAfter=10))
styles.add(ParagraphStyle(name='Level', parent=styles['BodyDV'], fontName='DejaVu-Bold', fontSize=8.5, leading=11, textColor=BLUE, spaceAfter=3))
styles.add(ParagraphStyle(name='SolutionTitle', parent=styles['Heading3'], fontName='DejaVu-Bold', fontSize=14, leading=18, textColor=RED, spaceBefore=8, spaceAfter=8))
styles.add(ParagraphStyle(name='CoverCourse', parent=styles['BodyDV'], fontName='DejaVu-Bold', fontSize=10, leading=13, alignment=TA_CENTER, textColor=RED, spaceAfter=12))
styles.add(ParagraphStyle(name='CoverTitle', parent=styles['Title'], fontName='DejaVu-Bold', fontSize=27, leading=33, alignment=TA_CENTER, textColor=INK, spaceAfter=16))
styles.add(ParagraphStyle(name='CoverType', parent=styles['Heading2'], fontName='DejaVu', fontSize=18, leading=22, alignment=TA_CENTER, textColor=MUTED, spaceAfter=35))
styles.add(ParagraphStyle(name='CoverAuthor', parent=styles['BodyDV'], fontName='DejaVu-Bold', fontSize=13, leading=18, alignment=TA_CENTER))
styles.add(ParagraphStyle(name='Hint', parent=styles['BodyDV'], fontSize=10.3, leading=15, leftIndent=8, rightIndent=8, borderColor=BLUE, borderWidth=0, borderPadding=8, backColor=colors.HexColor('#F3F7FA'), spaceBefore=8, spaceAfter=12))


def tex_plain(value):
    value = value or ''
    replacements = {'\\times': '×', '\\sum': 'Σ', '\\sqrt': '√', '\\bar': '', '\\mathrm': '', '\\leq': '≤', '\\geq': '≥', '\\%': '%'}
    for old, new in replacements.items(): value = value.replace(old, new)
    value = re.sub(r'\\[a-zA-Z]+', '', value)
    value = value.replace('{', '').replace('}', '').replace('$', '')
    return value


def prepare_soup(fragment):
    soup = BeautifulSoup(f'<div>{fragment or ""}</div>', 'html.parser')
    for math in soup.find_all('math'):
        ann = math.find('annotation', attrs={'encoding': 'application/x-tex'})
        math.replace_with(NavigableString(tex_plain(ann.get_text() if ann else math.get_text(' ', strip=True))))
    return soup.div


def inline_html(tag):
    raw = tag.decode_contents() if isinstance(tag, Tag) else str(tag)
    raw = raw.replace('<strong>', '<b>').replace('</strong>', '</b>').replace('<em>', '<i>').replace('</em>', '</i>')
    raw = re.sub(r'<br\s*/?>', '<br/>', raw, flags=re.I)
    raw = re.sub(r'</?(?!b\b|i\b|sup\b|sub\b|br\b)[a-zA-Z][^>]*>', '', raw)
    return raw.strip() or ' '


def paragraph_from(tag, style='BodyDV'):
    return Paragraph(inline_html(tag), styles[style])


def table_flow(table_tag):
    rows = []
    for tr in table_tag.find_all('tr'):
        cells = tr.find_all(['th', 'td'], recursive=False)
        if not cells: cells = tr.find_all(['th', 'td'])
        rows.append([Paragraph(cell.get_text(' ', strip=True), styles['SmallDV']) for cell in cells])
    if not rows: return Spacer(1, 1)
    max_cols = max(len(row) for row in rows)
    for row in rows:
        row.extend([Paragraph('', styles['SmallDV'])] * (max_cols - len(row)))
    col_width = 174*mm / max_cols
    tbl = Table(rows, colWidths=[col_width]*max_cols, repeatRows=1, hAlign='LEFT')
    tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), SOFT), ('TEXTCOLOR',(0,0),(-1,-1),INK),
        ('FONTNAME',(0,0),(-1,-1),'DejaVu'), ('GRID',(0,0),(-1,-1),0.45,LINE),
        ('VALIGN',(0,0),(-1,-1),'MIDDLE'), ('LEFTPADDING',(0,0),(-1,-1),5),
        ('RIGHTPADDING',(0,0),(-1,-1),5), ('TOPPADDING',(0,0),(-1,-1),5), ('BOTTOMPADDING',(0,0),(-1,-1),5)
    ]))
    return KeepTogether([Spacer(1, 4), tbl, Spacer(1, 8)])


def figure_flow(figure, chapter, index):
    items = []
    caption = figure.find('figcaption')
    if caption: items.append(Paragraph(f'<b>{caption.get_text(" ", strip=True)}</b>', styles['BodyDV']))
    svg = figure.find('svg')
    if svg:
        try:
            png = cairosvg.svg2png(bytestring=str(svg).encode('utf-8'), output_width=1300)
            viewbox = svg.get('viewBox', '0 0 720 300').split()
            ratio = float(viewbox[3]) / float(viewbox[2]) if len(viewbox) == 4 else 0.42
            width = 165*mm
            height = min(75*mm, width*ratio)
            items.append(Image(BytesIO(png), width=width, height=height))
        except Exception:
            items.append(Paragraph('[Graph available on the interactive platform]', styles['SmallDV']))
    note = figure.find(class_='figure-note')
    if note: items.append(Paragraph(note.get_text(' ', strip=True), styles['SmallDV']))
    return KeepTogether(items + [Spacer(1, 8)])


def fragment_flowables(fragment, chapter=0, index=0, body_style='BodyDV'):
    root = prepare_soup(fragment)
    output = []
    for child in root.children:
        if isinstance(child, NavigableString):
            if child.strip(): output.append(Paragraph(child.strip(), styles[body_style]))
            continue
        if child.name in ('p', 'h4'):
            output.append(paragraph_from(child, body_style))
        elif child.name in ('ol', 'ul'):
            items = [ListItem(Paragraph(inline_html(li), styles[body_style]), leftIndent=10) for li in child.find_all('li', recursive=False)]
            output.append(ListFlowable(items, bulletType='1' if child.name == 'ol' else 'bullet', start='1', leftIndent=20, bulletFontName='DejaVu', bulletFontSize=10, spaceAfter=7))
        elif child.name == 'table': output.append(table_flow(child))
        elif child.name == 'div' and 'table-wrap' in (child.get('class') or []):
            table = child.find('table')
            if table: output.append(table_flow(table))
        elif child.name == 'figure': output.append(figure_flow(child, chapter, index))
        elif child.name in ('h3',): output.append(Paragraph(child.get_text(' ', strip=True), styles['SolutionTitle']))
        else:
            output.extend(fragment_flowables(inner(child), chapter, index, body_style))
    return output


def inner(tag): return ''.join(str(x) for x in tag.contents)


def load_english_base(chapter):
    soup = BeautifulSoup((ROOT / f'chapter-{chapter}.html').read_text(encoding='utf-8'), 'html.parser')
    exercises = []
    for article in soup.select('article.exercise'):
        exercises.append({
            'level': article.select_one('.level').get_text(' ', strip=True),
            'title': article.select_one('h2').get_text(' ', strip=True),
            'question': inner(article.select_one('.question')),
            'hint': article.select_one('.hint').get_text(' ', strip=True),
            'solution': inner(article.select_one('.solution')),
        })
    return exercises


def all_exercises(chapter, lang):
    if lang == 'en': base = load_english_base(chapter)
    else:
        tr = DATA['translations'][str(chapter)]
        base = [tr['exercises'][str(i)] for i in range(1, 6)]
    for item in DATA['extended'].get(str(chapter), []):
        base.append({k: item[k] for k in ('title','level','question','hint','solution')} if lang == 'en' else item['fr'])
    return base


def footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(LINE); canvas.setLineWidth(0.4); canvas.line(18*mm, 14*mm, 192*mm, 14*mm)
    canvas.setFont('DejaVu', 7.5); canvas.setFillColor(MUTED)
    canvas.drawString(18*mm, 9*mm, 'Badr ABOUFARASSE, PhD. · KEDGE Business School')
    canvas.drawRightString(192*mm, 9*mm, str(doc.page))
    canvas.restoreState()


def build(chapter, lang, kind):
    is_fr = lang == 'fr'
    title = CHAPTERS[chapter][lang]
    kind_label = ('Corrigés détaillés' if kind == 'solutions' else "Série d’exercices") if is_fr else ('Detailed solutions' if kind == 'solutions' else 'Exercise series')
    file = OUT / f'chapter-{chapter}-{kind}-{lang}.pdf'
    doc = SimpleDocTemplate(str(file), pagesize=A4, rightMargin=18*mm, leftMargin=18*mm, topMargin=18*mm, bottomMargin=20*mm, title=f'{title} — {kind_label}', author='Badr ABOUFARASSE, PhD.')
    story = [Spacer(1, 22*mm), Image(str(ROOT/'logoKedge.png'), width=92*mm, height=35*mm), Spacer(1, 22*mm),
             Paragraph((f'MÉTHODES QUANTITATIVES 1 · CHAPITRE {chapter}' if is_fr else f'QUANTITATIVE METHODS 1 · CHAPTER {chapter}'), styles['CoverCourse']),
             Paragraph(title, styles['CoverTitle']), Paragraph(kind_label, styles['CoverType']),
             Spacer(1, 20*mm), Paragraph('Badr ABOUFARASSE, PhD.', styles['CoverAuthor']), Paragraph('KEDGE Business School', styles['CoverAuthor']), PageBreak()]
    exercises = all_exercises(chapter, lang)
    for i, ex in enumerate(exercises, 1):
        story += [Paragraph(ex['level'], styles['Level']), Paragraph(f'{i}. {ex["title"]}', styles['ExerciseTitle'])]
        story += fragment_flowables(ex['question'], chapter, i, 'QuestionDV')
        prompt = ('<b>Aide méthodologique.</b> ' if is_fr else '<b>Method prompt.</b> ') + ex['hint']
        story += [Paragraph(prompt, styles['Hint'])]
        if kind == 'solutions':
            story += fragment_flowables(ex['solution'], chapter, i, 'BodyDV')
        if i < len(exercises): story.append(PageBreak())
    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    return file


if __name__ == '__main__':
    outputs = []
    for chapter in range(1, 7):
        for lang in ('en', 'fr'):
            for kind in ('exercises', 'solutions'):
                outputs.append(build(chapter, lang, kind))
    for output in outputs: print(output.name)
