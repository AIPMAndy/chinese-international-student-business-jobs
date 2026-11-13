#!/usr/bin/env python3
"""Validate the deliverable, references and local website without network access.
This does not assert that every external URL is open or that a policy is current.
"""
import csv, hashlib, json, re, subprocess, sys, zipfile
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
from xml.etree import ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
failures=[]; results={}
def check(condition, message):
    if not condition:failures.append(message)
def read_json(p):return json.loads(p.read_text(encoding='utf-8'))

sources=read_json(ROOT/'research/sources.json')
ids={x['id'] for x in sources}
check(len(ids)==len(sources),'Duplicate source IDs')
for item in sources:
    for field in ['id','title','url','scope','checked','type','claim','limitation']:
        check(bool(item.get(field)),f"Missing source field {item.get('id')}/{field}")
    check(item['url'].startswith('https://'),f"Non-HTTPS source {item['id']}")
    check(bool(re.fullmatch(r'\d{4}-\d{2}-\d{2}',item['checked'])),f"Invalid check date {item['id']}")
results['sources']={'records':len(sources),'unique_urls':len({s['url'] for s in sources})}

content=list((ROOT/'content').rglob('*.md'))
check(len(content)==18,'Expected 18 main chapters')
routes=list((ROOT/'content/routes').glob('*.md'))
check(len(routes)==6,'Expected 6 distinct route entries')
for p in content:
    value=p.read_text()
    for tag in ['输入','操作','输出','验收','错误处理']:
        check(tag in value,f'{p.relative_to(ROOT)} missing {tag}')
    for ref in re.findall(r'\b(?:RT|RG|CF|BS)\d{2}\b',value):
        check(ref in ids,f'{p.relative_to(ROOT)} cites unknown {ref}')
results['chapters']={'main':len(content),'routes':len(routes)}

matrix=read_json(ROOT/'research/region-matrix.json')
check(len(matrix)==31,'Expected 31 region entries')
check(len({r['country'] for r in matrix})==31,'Duplicate region entries')
for item in matrix:
    for key in ['country','coverage','work_route','job_channel','graduate_program','timing','materials','next_action','gaps','checked']:
        check(bool(item.get(key)),f"Region {item.get('country')} lacks {key}")
    check(set(item['source_ids'])<=ids,f"Unknown region source: {item['country']}")
results['regions']=len(matrix)

md_paths=[p for folder in ['content','cases','templates','research'] for p in (ROOT/folder).rglob('*.md')]
md_paths += [p for p in ROOT.glob('*.md')]
md_links=0
for p in md_paths:
    value=p.read_text()
    for href in re.findall(r'\[[^\]]*\]\(([^\s)]+)(?:\s+[^)]*)?\)',value):
        if href.startswith(('http://','https://','mailto:','#')):continue
        target=unquote(href.split('#')[0]);md_links+=1
        check((p.parent/target).exists(),f'Missing Markdown link: {p.relative_to(ROOT)} -> {target}')
results['markdown_local_links']=md_links

class Page(HTMLParser):
    def __init__(self,text):
        super().__init__();self.refs=[];self.ids=set();self.viewport=False;self.titles=0;self.lang='';self.text=[]
        self.feed(text)
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'id' in a:self.ids.add(a['id'])
        if tag=='html':self.lang=a.get('lang','')
        if tag=='title':self.titles+=1
        if tag=='meta' and a.get('name')=='viewport':self.viewport=True
        for attr in ['href','src']:
            if attr in a:self.refs.append(a[attr])
    def handle_data(self,data):self.text.append(data)

dist=ROOT/'dist'; pages={p:Page(p.read_text()) for p in dist.rglob('*.html')}
html_links=0
for p,page in pages.items():
    check(page.viewport and page.lang=='zh-CN' and page.titles==1,f'Page metadata: {p.relative_to(ROOT)}')
    check('AIPMAndy' in ''.join(page.text),f'Brand missing: {p.relative_to(ROOT)}')
    check('**' not in ''.join(page.text),f'Unrendered bold markers: {p.relative_to(ROOT)}')
    for href in page.refs:
        parsed=urlsplit(href)
        if parsed.netloc in ('metaver.vip','www.a6no1.cn'):
            check(href in ('https://metaver.vip/','https://www.a6no1.cn/'),f'Malformed public brand URL: {p.relative_to(ROOT)} -> {href}')
        if parsed.scheme or parsed.netloc or href.startswith('data:'):continue
        html_links+=1
        part=unquote(parsed.path)
        target=(dist/part.lstrip('/') if part.startswith('/') else p.parent/part).resolve() if part else p.resolve()
        if target.is_dir():target=target/'index.html'
        check(target.exists(),f'Broken site link: {p.relative_to(dist)} -> {href}')
        if parsed.fragment and target in pages:
            check(unquote(parsed.fragment) in pages[target].ids,f'Broken fragment: {p.relative_to(dist)} -> {href}')
results['website']={'html_pages':len(pages),'local_links_checked':html_links,'metadata_and_brand_checked':True}

case_dirs=sorted(p for p in (ROOT/'cases').iterdir() if p.is_dir())
check(len(case_dirs)==6,'Expected 6 case packs')
case_results=[]
for folder in case_dirs:
    readme=folder/'README.md';check(readme.exists(),f'Case README absent: {folder.name}')
    check((folder/'printable-data.md').exists(),f'Printable inputs absent: {folder.name}')
    check('模拟' in readme.read_text(),f'Simulation label absent: {folder.name}')
    for data in folder.glob('*.csv'):
        with data.open(newline='',encoding='utf-8-sig') as stream:
            rows=list(csv.reader(stream))
        check(bool(rows) and len(rows[0])>1,f'Empty CSV {data.name}')
        check(all(len(r)==len(rows[0]) for r in rows),f'CSV field-count mismatch {data.name}')
    verifier=folder/'verify.py'
    if verifier.exists():
        r=subprocess.run([sys.executable,str(verifier)],cwd=ROOT,capture_output=True,text=True)
        check(r.returncode==0,f'Calculation failed {folder.name}: {r.stderr[-300:]}')
        case_results.append({'case':folder.name,'exit_code':r.returncode})
cf=ROOT/'scripts/verify-finance-consulting.py'
if cf.exists():
    r=subprocess.run([sys.executable,str(cf)],cwd=ROOT,capture_output=True,text=True)
    check(r.returncode==0,f'Consulting/finance calculation failed: {r.stderr[-300:]}')
    case_results.append({'case':'consulting-and-finance','exit_code':r.returncode})
results['case_calculations']=case_results

xlsx=ROOT/'downloads/business-job-workbook.xlsx'
with zipfile.ZipFile(xlsx) as archive:
    check(archive.testzip() is None,'XLSX CRC failure')
    worksheets=[n for n in archive.namelist() if re.fullmatch(r'xl/worksheets/sheet\d+\.xml',n)]
    tables=[n for n in archive.namelist() if re.fullmatch(r'xl/tables/table\d+\.xml',n)]
    check(len(worksheets)==7 and len(tables)==7,'Workbook sheet/table count')
    formulas=0
    ns={'m':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
    for name in worksheets:
        tree=ET.fromstring(archive.read(name));formulas+=len(tree.findall('.//m:f',ns))
        check(bool(tree.findall('.//m:pane',ns)),f'Freeze pane absent: {name}')
        check(bool(tree.findall('.//m:dataValidation',ns)),f'Validation absent: {name}')
        for cell in tree.findall('.//m:c',ns):
            check(cell.get('t')!='e',f'Cached spreadsheet error: {name}/{cell.get("r")}')
results['workbook']={'sheets':len(worksheets),'tables':len(tables),'formula_cells':formulas,'native_excel_tested':False}

try:
    import fitz
except ImportError:
    results['pdf']={'status':'not_run','reason':'PyMuPDF is not installed'}
else:
    pdf=fitz.open(ROOT/'downloads/business-careers-guide.pdf')
    pdf_text='\n'.join(page.get_text() for page in pdf)
    check('**' not in pdf_text,'Unrendered bold syntax in PDF')
    check('\ufffd' not in pdf_text,'Replacement characters in PDF')
    check('AIPMAndy' in pdf_text and 'AI酋长Andy' in pdf_text,'PDF brand missing')
    for pageno,page in enumerate(pdf,1):
        check(len(page.get_text().strip())>70,f'Blank/suspiciously empty PDF page {pageno}')
        for word in page.get_text('words'):
            x0,y0,x1,y1=word[:4]
            check(x0>=-.5 and y0>=-.5 and x1<=page.rect.width+.5 and y1<=page.rect.height+.5,f'PDF text outside page {pageno}')
    book=read_json(ROOT/'book.json')
    check(len(pdf.get_toc())==len(book['chapters']),'PDF bookmark/chapter count mismatch')
    results['pdf']={'pages':len(pdf),'bookmarks':len(pdf.get_toc()),'links':sum(len(p.get_links()) for p in pdf),'render_check':'audit/pdf-render-check.json','human_review':'audit/pdf-review-final.json'}

download_names=['business-careers-guide.pdf','business-job-workbook.xlsx','templates-and-cases.zip','repository-source.zip']
for name in download_names:
    p=ROOT/'downloads'/name
    check(p.exists() and p.stat().st_size>1000,f'Download missing/empty: {name}')
    target=dist/'downloads'/name
    if p.exists() and target.exists():check(hashlib.sha256(p.read_bytes()).digest()==hashlib.sha256(target.read_bytes()).digest(),f'Download mismatch: {name}')
    if p.exists() and name.endswith('.zip'):
        with zipfile.ZipFile(p) as z:
            check(z.testzip() is None,f'ZIP CRC error: {name}')
            check(all(not n.startswith('/') and '..' not in Path(n).parts for n in z.namelist()),f'Unsafe ZIP paths: {name}')
            check(not any('/.git/' in n or '/.openai/' in n for n in z.namelist()),f'Private deployment metadata included: {name}')
results['downloads']={'count':4,'crc_and_local_static_identity_checked':True}
report={'date':'2026-11-13','status':'passed' if not failures else 'failed','results':results,'failure_count':len(failures),'failures':failures,'limits':['External pages were researched separately; this script does not claim all external links remain live.','Native Excel desktop was not tested.','Human PDF and live browser checks are separate records.']}
(ROOT/'audit').mkdir(exist_ok=True)
(ROOT/'audit/static-validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(report,ensure_ascii=False,indent=2))
sys.exit(bool(failures))
