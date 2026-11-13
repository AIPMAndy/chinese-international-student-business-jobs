#!/usr/bin/env python3
"""Create portable training and source bundles without credentials or recursion."""
import hashlib, json, os, shutil, zipfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
DEST=ROOT/'downloads'; DEST.mkdir(exist_ok=True)
STAMP=(2026,11,13,12,0,0)
PREFIX='chinese-international-student-business-jobs'

def add(archive, path, arcname):
    info=zipfile.ZipInfo(arcname,STAMP)
    info.compress_type=zipfile.ZIP_DEFLATED
    info.external_attr=(0o100755 if path.suffix=='.sh' else 0o100644)<<16
    archive.writestr(info,path.read_bytes())

kitreadme='''# 中国留学生商科岗位求职：模板与案例包

作者：AI 酋长 Andy｜微信 AIPMAndy｜公众号 AI酋长Andy
个人官网：https://metaver.vip/｜公司官网：https://www.a6no1.cn/
版本：1.0 · 2026-11-13

先读 templates/README.md，再选 cases/ 下的一条路线。每套包含题面、数据、参考解、评分与追问；printable-data.md 是可打印输入。
downloads/business-job-workbook.xlsx 包含七张可编辑表。templates/csv/ 可用表格软件导入；CSV 不保留公式、样式或下拉。
所有案例与申请样例都是完整教学模拟，不是真实客户经历，不应写成已完成的商业工作。
content/ 是独立可读的完整正文。SOURCES.md 和 research/ 给出官方来源、日期与限制。
正式网站采用 GitHub Pages；发布状态见完整项目中的 VERIFY.md。
目标地址：https://aipmandy.github.io/chinese-international-student-business-jobs/ （未完成线上验收前仅为目标地址）
免费内容完整开放；可选咨询承接职业方向判断、申请材料诊断与面试陪跑，不承诺录用或薪资。
授权：原创文字与合成数据 CC BY 4.0，代码 MIT。见随包授权文件。
'''
kit=DEST/'templates-and-cases.zip'
with zipfile.ZipFile(kit,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
    info=zipfile.ZipInfo('business-careers-kit/README.md',STAMP);info.compress_type=zipfile.ZIP_DEFLATED
    z.writestr(info,kitreadme)
    for folder in ['content','templates','cases','research']:
        for p in sorted((ROOT/folder).rglob('*')):
            if p.is_file() and '__pycache__' not in p.parts:add(z,p,'business-careers-kit/'+p.relative_to(ROOT).as_posix())
    for name in ['SOURCES.md','LICENSE','CONTENT_LICENSE.md','THIRD_PARTY_NOTICES.md','downloads/business-job-workbook.xlsx']:
        add(z,ROOT/name,'business-careers-kit/'+name)

# Put the same portable files inside the prebuilt offline website before packing.
static_downloads=ROOT/'dist'/'downloads';static_downloads.mkdir(parents=True,exist_ok=True)
for filename in ['business-careers-guide.pdf','business-job-workbook.xlsx','templates-and-cases.zip']:
    shutil.copy2(DEST/filename,static_downloads/filename)
source=DEST/'repository-source.zip'
skip_dirs={'.git','.openai','node_modules','tmp','.venv','__pycache__'}
skip_files={'downloads/repository-source.zip','dist/downloads/repository-source.zip','audit/downloads-manifest.json','downloads/SHA256SUMS.txt','dist/downloads/SHA256SUMS.txt'}
with zipfile.ZipFile(source,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
    for p in sorted(ROOT.rglob('*')):
        if not p.is_file():continue
        rel=p.relative_to(ROOT)
        if any(part in skip_dirs for part in rel.parts) or rel.as_posix() in skip_files:continue
        if rel.as_posix().startswith(('audit/rendered/','audit/screenshots/')):continue
        add(z,p,PREFIX+'/'+rel.as_posix())

records=[]
for name in ['business-careers-guide.pdf','business-job-workbook.xlsx','templates-and-cases.zip','repository-source.zip']:
    p=DEST/name
    records.append({'file':'downloads/'+name,'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
(ROOT/'audit').mkdir(exist_ok=True)
(ROOT/'audit/downloads-manifest.json').write_text(json.dumps({'version':'1.0','date':'2026-11-13','files':records},ensure_ascii=False,indent=2)+'\n')
(DEST/'SHA256SUMS.txt').write_text(''.join(f"{r['sha256']}  {Path(r['file']).name}\n" for r in records))
print(json.dumps({'files':records},ensure_ascii=False,indent=2))
