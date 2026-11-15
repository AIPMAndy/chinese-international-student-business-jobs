#!/usr/bin/env python3
"""Independently typeset a book from the source Markdown; not a website printout.
Requires reportlab, fonttools, lxml and Noto CJK fonts. The fonts are subset and
converted to TrueType outlines for embedding; no font files are redistributed.
"""
from __future__ import annotations
import json, re, os, html, hashlib, subprocess, sys
from pathlib import Path
from collections import Counter
from lxml import html as LH
from fontTools.ttLib import TTFont as FTFont
from fontTools import subset
from fontTools.fontBuilder import FontBuilder
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.pens.cu2quPen import Cu2QuPen
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.units import mm
from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, PageBreak, LongTable, TableStyle, KeepTogether, Flowable, CondPageBreak
from reportlab.platypus.tableofcontents import TableOfContents

ROOT=Path(__file__).resolve().parents[1]
TMP=ROOT/'tmp'/'pdf';TMP.mkdir(parents=True,exist_ok=True)
DEST=ROOT/'downloads'/'business-careers-guide.pdf';DEST.parent.mkdir(exist_ok=True)
BOOK=json.loads((ROOT/'book.json').read_text())
WIDTH,HEIGHT=176*mm,250*mm
LEFT=RIGHT=17*mm; TOP=21*mm; BOTTOM=20*mm
TEXTW=WIDTH-LEFT-RIGHT
INK=colors.HexColor('#1b231e');GREEN=colors.HexColor('#40664a');MUTED=colors.HexColor('#60695e');LINE=colors.HexColor('#d5dccf');PALE=colors.HexColor('#eef2e8');PAPER=colors.HexColor('#fbfcf8')
SITE='https://aipmandy.github.io/chinese-international-student-business-jobs'
normalize=lambda s: str(s).replace('\u2011','-').replace('\u2013','-').replace('\u2014','-').replace('\u00a0',' ')
texts='\n'.join((ROOT/c['path']).read_text() for c in BOOK['chapters'])
fixed='中国留学生商科岗位求职保姆级攻略完整训练册作者AI酋长Andy微信公众号个人官网公司官网目录六条职能路线查岗位做证据练面试参考来源资料版本免费开放教学模拟商业服务可选不承诺录用或薪资输入操作输出验收错误处理备注分数使用范围未验证下载与更新北美欧洲亚洲大洋洲回国申请版权与授权读者填写示例附录来源目录阅读指引咨询金融会计市场品牌运营供应链商业经营分析销售商务拓展导航页扫码索引页年月日0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz@:/._-+#%()[]<>+×÷＝≥≤→•·，。：；！？（）《》「」【】、页'
LATIN_FALLBACK={'ł'}
chars=(set(normalize(texts+fixed))|set(chr(n) for n in range(32,127)))-LATIN_FALLBACK

def embed_font(weight):
    src=Path('/usr/share/fonts/opentype/noto')/f'NotoSansCJK-{weight}.ttc'
    fingerprint=hashlib.sha256(''.join(sorted(chars)).encode()).hexdigest()[:12]
    out=TMP/f'BookSans-{weight}-{fingerprint}.ttf'
    if out.exists():return str(out)
    font=FTFont(str(src),fontNumber=2)
    cmap=font.getBestCmap();missing=[c for c in chars if ord(c)>31 and ord(c) not in cmap and not c.isspace()]
    if missing:print('Font missing:',repr(''.join(sorted(missing))))
    opts=subset.Options();opts.layout_features=[];opts.name_IDs=['*'];opts.name_legacy=True;opts.name_languages=['*']
    ss=subset.Subsetter(options=opts);ss.populate(unicodes=[ord(c) for c in chars]);ss.subset(font)
    gs=font.getGlyphSet();order=font.getGlyphOrder();glyphs={}
    for name in order:
        pen=TTGlyphPen(gs);qpen=Cu2QuPen(pen,max_err=1.0,reverse_direction=True);gs[name].draw(qpen);glyphs[name]=pen.glyph()
    fb=FontBuilder(font['head'].unitsPerEm,isTTF=True);fb.setupGlyphOrder(order);fb.setupCharacterMap(font.getBestCmap());fb.setupGlyf(glyphs)
    fb.setupHorizontalMetrics(dict(font['hmtx'].metrics));fb.setupHorizontalHeader(ascent=font['hhea'].ascent,descent=font['hhea'].descent)
    os2=font['OS/2'];fb.setupOS2(sTypoAscender=os2.sTypoAscender,sTypoDescender=os2.sTypoDescender,sTypoLineGap=os2.sTypoLineGap,usWinAscent=os2.usWinAscent,usWinDescent=os2.usWinDescent)
    fb.setupNameTable({'familyName':'Andy Book Sans','styleName':weight,'uniqueFontIdentifier':'AndyBookSans'+weight,'fullName':'Andy Book Sans '+weight,'psName':'AndyBookSans-'+weight,'version':'Version 1.0','copyright':'Noto Sans CJK, Adobe and Google; SIL Open Font License 1.1. Subset for this publication.'})
    fb.setupPost();fb.setupMaxp();fb.save(str(out));return str(out)

pdfmetrics.registerFont(TTFont('Book',embed_font('Regular')))
pdfmetrics.registerFont(TTFont('BookBold',embed_font('Bold')))
pdfmetrics.registerFontFamily('Book',normal='Book',bold='BookBold',italic='Book',boldItalic='BookBold')
pdfmetrics.registerFont(TTFont('Latin','/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf'))

def style(name,**kw):
    base=dict(fontName='Book',fontSize=10.1,leading=15.8,textColor=INK,spaceAfter=7,wordWrap='CJK',allowWidows=0,allowOrphans=0,splitLongWords=True)
    base.update(kw);return ParagraphStyle(name,**base)
ST={
 'body':style('Body'),
 'english':style('English',fontSize=9.6,leading=14.4,wordWrap='LTR'),
 'small':style('Small',fontSize=8.5,leading=13.8,textColor=MUTED,spaceAfter=7),
 'chapter':style('ChapterTitle',fontName='BookBold',fontSize=24,leading=33,spaceAfter=18,keepWithNext=True),
 'h2':style('H2',fontName='BookBold',fontSize=14,leading=21,spaceBefore=12,spaceAfter=7,keepWithNext=True),
 'h3':style('H3',fontName='BookBold',fontSize=11.3,leading=18,spaceBefore=10,spaceAfter=6,keepWithNext=True),
 'h4':style('H4',fontName='BookBold',fontSize=10.3,leading=17,spaceBefore=8,spaceAfter=6,keepWithNext=True),
 'quote':style('Quote',fontSize=9.7,leading=16.4,backColor=PALE,borderPadding=10,leftIndent=10,rightIndent=8,spaceBefore=6,spaceAfter=14),
 'bullet':style('Bullet',leftIndent=11,firstLineIndent=-11,spaceAfter=6),
 'code':style('Code',fontSize=8.5,leading=13.5,backColor=PALE,borderPadding=9,spaceBefore=5,spaceAfter=13),
 'cell':style('Cell',fontSize=8.6,leading=13.8,spaceAfter=0),
 'cellhead':style('CellHead',fontName='BookBold',fontSize=8.6,leading=13.6,spaceAfter=0),
 'kicker':style('Kicker',fontSize=9.1,leading=15,textColor=GREEN,spaceAfter=11,keepWithNext=True),
 'source':style('Source',fontSize=8.0,leading=12.7,spaceAfter=6,textColor=MUTED),
 'sourcehead':style('SourceHead',fontName='BookBold',fontSize=10.5,leading=16,spaceBefore=12,spaceAfter=7,keepWithNext=True),
}

chapter_map={c['path']:f'ch-{i}' for i,c in enumerate(BOOK['chapters'])}
chapter_map['cases/01-consulting/README.md']=chapter_map.get('cases/01-consulting/brief.md','')
chapter_map['cases/02-finance-accounting/README.md']=chapter_map.get('cases/02-finance-accounting/brief.md','')
current_file=''

def escape(s):
    value=html.escape(normalize(s or ''),quote=False)
    for char in LATIN_FALLBACK:value=value.replace(char,f'<font name="Latin">{char}</font>')
    return value
def inline(node):
    out=escape(node.text)
    for child in node:
        tag=child.tag if isinstance(child.tag,str) else ''
        inner=inline(child)
        if tag in ('strong','b'):part=f'<b>{inner}</b>'
        elif tag in ('em','i'):part=inner
        elif tag=='br':part='<br/>'
        elif tag=='code':part=f'<font color="#31543b">{inner}</font>'
        elif tag=='a':
            href=child.get('href','')
            if href.startswith(('https://','http://')):target=href
            elif href.startswith('#'):target=''
            else:
                resolved=os.path.normpath(str(Path(current_file).parent/href.split('#')[0])).replace('\\','/')
                target='#'+chapter_map[resolved] if resolved in chapter_map else SITE+'/files/'+resolved
            part=f'<link href="{html.escape(target,quote=True)}" color="#31543b">{inner}</link>' if target else inner
        else:part=inner
        out+=part+escape(child.tail)
    return out

def para(text,kind='body'):
    return Paragraph(text or ' ',ST[kind])

def table_node(node):
    rows=node.xpath('.//tr');raw=[]
    for r in rows:
        raw.append([inline(c) for c in r if c.tag in ('td','th')])
    if not raw:return []
    cols=max(map(len,raw));raw=[r+['']*(cols-len(r)) for r in raw]
    if cols>4:
        output=[];heads=raw[0]
        for row in raw[1:]:
            bits=[]
            for label,value in zip(heads,row):bits.append(f'<b>{label}</b>：{value}')
            output.append(KeepTogether([para('<br/>'.join(bits),'quote')]))
        return output
    def textlen(s):return len(re.sub('<[^>]+>','',s))
    scores=[max(8,min(50,sum(textlen(r[i]) for r in raw)/len(raw)))**.5 for i in range(cols)]
    # Keep quantitative columns legible; no narrow label columns.
    widths=[TEXTW*s/sum(scores) for s in scores]
    minw=TEXTW*(.18 if cols==4 else .22 if cols==3 else .25)
    widths=[max(minw,w) for w in widths];widths=[TEXTW*w/sum(widths) for w in widths]
    data=[[para(v,'cellhead' if j==0 else 'cell') for v in r] for j,r in enumerate(raw)]
    table=LongTable(data,colWidths=widths,repeatRows=1,hAlign='LEFT',splitByRow=1,splitInRow=1)
    cmds=[('BACKGROUND',(0,0),(-1,0),PALE),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),8),('LINEBELOW',(0,0),(-1,0),.6,LINE),('LINEBELOW',(0,1),(-1,-1),.3,LINE)]
    for j in range(2,len(raw),2):cmds.append(('BACKGROUND',(0,j),(-1,j),colors.HexColor('#f7f9f3')))
    table.setStyle(TableStyle(cmds))
    # Keep small data tables together; the preceding heading binds to the table.
    table_height=table.wrap(TEXTW,HEIGHT)[1]
    unit=KeepTogether([table]) if len(raw)<=12 and table_height<(HEIGHT-TOP-BOTTOM)*.65 else table
    return [unit,Spacer(1,10)]

def parse_nodes(nodes,is_sources=False):
    flow=[]
    for node in nodes:
        tag=node.tag if isinstance(node.tag,str) else ''
        if tag=='h1':continue
        if tag in ('h2','h3','h4','h5'):
            kind='sourcehead' if is_sources and tag=='h2' else tag if tag in ST else 'h4'
            flow.append(para(inline(node),kind))
        elif tag=='p':
            plain=node.text_content().strip()
            # Chapters remain branded in the page furniture. Avoid repeated
            # author-only tails becoming almost empty pages in the bound book.
            if current_file!='content/00-start.md' and (
                (plain.startswith(('作者：','作者:','维护者：')) and 'AIPMAndy' in plain)
                or (plain.startswith('个人官网') and '公司官网' in plain)
                or plain.startswith('免费内容完整开放；咨询用于')
                or plain.startswith('免费内容完整开放。咨询可用于')
            ):continue
            kind='source' if is_sources else 'small' if plain.startswith('数据字典：') else 'english' if len(plain)>30 and not re.search(r'[\u3400-\u9fff]',plain) else 'body'
            p=para(inline(node),kind)
            if plain.startswith('覆盖状态：'):p.keepWithNext=True
            flow.append(p)
        elif tag=='table':
            parts=table_node(node)
            if parts and isinstance(parts[0],KeepTogether):
                # Bind the heading AND a short source/units paragraph to the
                # actual table, avoiding nested keep-with-next wrappers.
                start=None
                for distance in range(1,min(3,len(flow))+1):
                    previous=flow[-distance]
                    if not isinstance(previous,Paragraph):break
                    if previous.style.name in ('H2','H3','H4'):
                        start=len(flow)-distance;break
                    if len(previous.getPlainText())>300:break
                if start is not None:
                    group=flow[start:]+parts[0]._content
                    flow=flow[:start];parts[0]=KeepTogether(group)
            flow+=parts
        elif tag in ('ul','ol'):
            for i,li in enumerate(node):
                lead=f'{i+1}. ' if tag=='ol' else '• '
                # Nested lists get their own lines instead of dropped text.
                sub=[]
                text=escape(li.text)
                for child in li:
                    if child.tag in ('ul','ol'):sub+=parse_nodes([child],is_sources)
                    elif child.tag=='p':text+=inline(child)+'<br/>'
                    else:
                        wrapper=LH.Element('span');wrapper.append(LH.fromstring(LH.tostring(child)));text+=inline(wrapper)
                flow.append(para(lead+text,'bullet'));flow+=sub
        elif tag=='blockquote':
            bits=[inline(c) for c in node if c.tag!='ul']
            flow.append(para('<br/>'.join(bits),'quote'))
            for c in node:
                if c.tag=='ul':flow+=parse_nodes([c],is_sources)
        elif tag=='pre':
            t=escape(node.text_content()).replace('\n','<br/>')
            flow.append(para(t,'code'))
        elif tag=='hr':flow.append(Spacer(1,10))
        elif tag in ('div','section'):flow+=parse_nodes(node,is_sources)
        elif tag:flow.append(para(inline(node),'body'))
    return flow

class Cover(Flowable):
    def __init__(self):Flowable.__init__(self);self.width=TEXTW;self.height=HEIGHT-TOP-BOTTOM-2
    def draw(self):
        c=self.canv;c.saveState();c.translate(-LEFT,-BOTTOM+2)
        c.setFillColor(INK);c.rect(0,0,WIDTH,HEIGHT,fill=1,stroke=0)
        c.setStrokeColor(colors.HexColor('#52604f'));c.setLineWidth(.5);c.line(34,HEIGHT-54,WIDTH-34,HEIGHT-54)
        c.setFont('Book',8.5);c.setFillColor(colors.HexColor('#b4c1ac'));c.drawString(34,HEIGHT-37,'AI CHIEF ANDY / BUSINESS CAREERS / 2026')
        c.setFont('BookBold',29);c.setFillColor(colors.HexColor('#f4f6ee'))
        for i,t in enumerate(['中国留学生','商科岗位求职','保姆级攻略']):c.drawString(34,HEIGHT-140-i*48,t)
        c.setFont('Book',11);c.setFillColor(colors.HexColor('#b9c9af'));c.drawString(35,HEIGHT-322,'选职能。读岗位。做证据。练面试。')
        y=HEIGHT-385
        labels=['01  咨询与专业服务','02  金融、会计与财务','03  市场与品牌','04  运营与供应链','05  商业与经营分析','06  销售与商务拓展']
        for i,t in enumerate(labels):
            x=35+(i%2)*(TEXTW/2+5);yy=y-(i//2)*48;c.setStrokeColor(colors.HexColor('#414c3e'));c.line(x,yy+15,x+TEXTW/2-18,yy+15);c.setFont('Book',9.3);c.drawString(x,yy,t)
        c.setStrokeColor(colors.HexColor('#52604f'));c.line(34,109,WIDTH-34,109)
        c.setFont('BookBold',12);c.setFillColor(colors.HexColor('#f4f6ee'));c.drawString(34,84,'AI酋长Andy')
        c.setFont('Book',8.3);c.setFillColor(colors.HexColor('#b4c1ac'));c.drawString(34,65,'流量 AI 联合创始人、星觉 AI 创始人 · 星觉科技 · 北京');c.drawString(34,45,'微信 AIPMAndy · 免费完整开放  /  VERSION 1.0  /  2026-11-13')
        c.setFont('Book',46);c.setFillColor(colors.HexColor('#8ca282'));c.drawRightString(WIDTH-33,47,'06')
        c.restoreState()

class BookDoc(BaseDocTemplate):
    def __init__(self,*args,**kwargs):
        self.current_section='阅读指引';self.headings=[];super().__init__(*args,**kwargs)
    def beforeDocument(self):self.current_section='阅读指引';self.headings=[]
    def afterFlowable(self,flowable):
        if isinstance(flowable,Paragraph) and getattr(flowable,'_chapter_key',None):
            key=flowable._chapter_key;title=flowable.getPlainText();self.canv.bookmarkPage(key);self.canv.addOutlineEntry(title,key,0,False);self.notify('TOCEntry',(0,title,self.page,key));self.headings.append({'title':title,'page':self.page,'key':key});self.current_section=flowable._section

def page_decor(c,doc):
    if doc.page==1:return
    c.saveState();c.setFillColor(PAPER);c.rect(0,0,WIDTH,HEIGHT,fill=1,stroke=0)
    c.setFont('Book',7.3);c.setFillColor(MUTED);c.drawString(LEFT,HEIGHT-12.5*mm,'中国留学生商科求职 / AI酋长Andy')
    c.setStrokeColor(LINE);c.setLineWidth(.4);c.line(LEFT,HEIGHT-15*mm,WIDTH-RIGHT,HEIGHT-15*mm)
    c.line(LEFT,14*mm,WIDTH-RIGHT,14*mm);c.setFont('Book',7);c.drawString(LEFT,9.3*mm,'微信 AIPMAndy · 免费完整开放 · 2026-11-13');c.drawRightString(WIDTH-RIGHT,9.3*mm,str(doc.page));c.restoreState()

def get_html():
    helper=TMP/'markdown-book.mjs'
    helper.write_text('''import fs from "node:fs";import path from "node:path";import{createRequire}from"node:module";import{pathToFileURL}from"node:url";let rq=createRequire(path.join(process.argv[2],"package.json"));let p;try{p=rq.resolve("marked")}catch{rq=createRequire(path.join(process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES,"resolve.cjs"));p=rq.resolve("marked")}const{marked}=await import(pathToFileURL(p));const b=JSON.parse(fs.readFileSync(path.join(process.argv[2],"book.json")));process.stdout.write(JSON.stringify(b.chapters.map(c=>({path:c.path,html:marked.parse(fs.readFileSync(path.join(process.argv[2],c.path),"utf8"))}))));''')
    res=subprocess.run([os.environ.get('CODEX_PRIMARY_RUNTIME_NODE','node'),str(helper),str(ROOT)],capture_output=True,text=True,check=True);return {x['path']:x['html'] for x in json.loads(res.stdout)}

doc=BookDoc(str(DEST),pagesize=(WIDTH,HEIGHT),leftMargin=LEFT,rightMargin=RIGHT,topMargin=TOP,bottomMargin=BOTTOM,title=BOOK['title'],author=BOOK['author'],subject='留学生商科职能选择、申请路径与专业案例训练',pageCompression=1,allowSplitting=1)
doc.addPageTemplates(PageTemplate(id='Book',frames=[Frame(LEFT,BOTTOM,TEXTW,HEIGHT-TOP-BOTTOM,id='normal',leftPadding=0,rightPadding=0,topPadding=0,bottomPadding=0)],onPage=page_decor))
story=[Cover(),PageBreak(),para('阅读指引 / BEFORE YOU START','kicker'),para('先选一条路线，<br/>再完成一份证据。','chapter')]
story += [para('本书帮助你回答三个问题：我适合哪类商科职能，如何满足岗位要求，怎样证明自己能做。请按目标地区、实际职责和招聘入口使用，不按专业名称无差别投递。'),para('每一步都写输入、操作、输出、验收与错误处理。所有案例和候选人样例均明确标注为教学模拟；课程、证书和模拟不能冒充实际工作经历。','quote'),para('作者与版本','h2'),para('AI酋长Andy · 流量 AI 联合创始人、星觉 AI 创始人 · 星觉科技 · 北京<br/>微信：AIPMAndy<br/>版本：1.0 · 核对日期：2026-11-13'),para(f'<link href="{SITE}" color="#31543b">GitHub Pages（发布状态见 VERIFY.md）</link><br/><link href="https://metaver.vip/" color="#31543b">个人官网 metaver.vip</link> · <link href="https://www.a6no1.cn/" color="#31543b">公司官网 www.a6no1.cn</link>'),para('范围与使用','h2'),para('覆盖北美、欧洲、亚洲、大洋洲及回国申请。非洲、南美洲不在本册范围；各国家和职能的覆盖深度不同。政策、职位状态和批次日期以官方现行页面为准。来源表区分适用范围和限制。'),para('免费内容完整开放。职业方向判断、材料诊断与面试陪跑是自愿选择的服务，不承诺录用或薪资。原创文字与教学数据 CC BY 4.0；网站代码 MIT。第三方来源、商标与招聘内容归各权利人。','small'),PageBreak(),para('目录 / CONTENTS','kicker'),para('从问题进入正文','chapter')]
toc=TableOfContents();toc.levelStyles=[style('TOC',fontSize=9.0,leading=15,spaceBefore=0,spaceAfter=0,leftIndent=0,rightIndent=20)];toc.tableStyle=TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),0),('TOPPADDING',(0,0),(-1,-1),2),('BOTTOMPADDING',(0,0),(-1,-1),2)]);toc.dotsMinLevel=0;story.append(toc)
htmls=get_html()
for i,ch in enumerate(BOOK['chapters']):
    current_file=ch['path']
    # The practice section is one continuous workbook. Its short question,
    # data and answer subsections need room to begin, not a mandatory new page.
    in_workbook=current_file.startswith('cases/') or current_file=='templates/README.md'
    first_workbook=current_file=='cases/01-consulting/brief.md'
    story.append(CondPageBreak(240) if in_workbook and not first_workbook else PageBreak())
    story.append(para(f'{ch["section"]} / {i+1:02d}','kicker'))
    title=para(escape(ch['title']),'chapter');title._chapter_key=f'ch-{i}';title._section=ch['section'];story.append(title)
    parsed=LH.fragment_fromstring(normalize(htmls[current_file]),create_parent='div');story+=parse_nodes(parsed,current_file=='SOURCES.md')
story+=[PageBreak(),para('下一步 / YOUR NEXT STEP','kicker'),para('选一个岗位，<br/>交一份能被追问的材料。','chapter'),para('今天不必读完全部章节。先核对一个目标岗位的资格与职责，再从对应案例开始。把自己的分析和限制讲清楚，就是下一步可检查的进展。'),para('完整模板与数据','h2'),para(f'GitHub Pages 已公开上线：<br/><link href="{SITE}/" color="#31543b">{SITE}/</link><br/>工作簿、CSV、SQL、Markdown 与案例题解已随完整资料包交付。'),para('作者：AI酋长Andy','h2'),para('流量 AI 联合创始人、星觉 AI 创始人 · 星觉科技 · 北京<br/>微信：<b>AIPMAndy</b><br/><link href="https://metaver.vip/" color="#31543b">个人官网：https://metaver.vip/</link><br/><link href="https://www.a6no1.cn/" color="#31543b">公司官网：https://www.a6no1.cn/</link>'),para('咨询入口承接职业方向判断、申请材料诊断与面试陪跑。免费内容可独立使用，不承诺录用或薪资。','quote')]
doc.multiBuild(story,maxPasses=5)
(TMP/'toc.json').write_text(json.dumps(doc.headings,ensure_ascii=False,indent=2))
print(json.dumps({'pdf':str(DEST),'bytes':DEST.stat().st_size,'chapters':len(BOOK['chapters']),'last_page':doc.page},ensure_ascii=False))
