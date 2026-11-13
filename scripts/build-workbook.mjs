import fs from 'node:fs/promises';
import path from 'node:path';
import { FileBlob, SpreadsheetFile, Workbook } from '@oai/artifact-tool';

// Run with the bundled Node runtime from a temporary directory whose node_modules
// points to CODEX_PRIMARY_RUNTIME_NODE_MODULES. Pass the repository as argument 1
// and, optionally, an intermediate output directory as argument 2.
const repo = path.resolve(process.argv[2] || process.cwd());
const outputDir = path.resolve(process.argv[3] || path.join(path.dirname(repo), 'outputs', 'business-job-workbook'));
const spec = JSON.parse(await fs.readFile(path.join(repo, 'templates/workbook-spec.json'), 'utf8'));
await fs.mkdir(outputDir, { recursive: true });
await fs.mkdir(path.join(repo, 'downloads'), { recursive: true });
await fs.mkdir(path.join(repo, 'templates/csv'), { recursive: true });

const wb = Workbook.create();
const font = 'Arial';
const colors = { ink:'#172033', muted:'#5B6578', line:'#D7DEE7', input:'#145DB6', pale:'#F3F6FA', sample:'#FFF8E8', warning:'#FDE9E7' };
const widths = {
  '职能选择':[16,19,15,15,15,16,14,14,55],
  '岗位研究':[22,17,37,18,24,22,36,43,31,43,69,17,46],
  '能力证据':[16,23,32,43,24,40,43,33,34,42],
  '行动计划':[16,22,33,34,45,33,43,18,17,42],
  '申请记录':[16,25,31,18,26,18,18,18,18,20,37,45],
  '面试复盘':[16,25,18,27,43,45,43,27,43,43],
  '资格核验':[16,33,43,48,70,23,18,20,50]
};
const tableNames = ['CareerChoice','JobResearch','AbilityEvidence','ActionPlan','ApplicationLog','InterviewReview','EligibilityReview'];
const letters = n => { let r=''; for(let x=n;x>0;x=Math.floor((x-1)/26)) r=String.fromCharCode(65+(x-1)%26)+r; return r; };
const layouts=[];
const sheets = spec.sheets.map(s => wb.worksheets.add(s.name));
const dates = new Set(['核对日期','截止日期','提交日期','测评日期','面试日期','结果日期','规则适用或生效日期']);

function cellText(value, header) {
  if(value===null || value===undefined) return null;
  if(dates.has(header) && typeof value==='string' && /^\d{4}-\d{2}-\d{2}$/.test(value)) return new Date(value+'T00:00:00Z');
  return value;
}
function list(sheet, address, values) {
  sheet.getRange(address).dataValidation={rule:{type:'list',values}};
}
function rowStyle(sheet, address, fill) {
  sheet.getRange(address).format.fill=fill;
}

for(let index=0; index<spec.sheets.length; index++) {
  const s=spec.sheets[index], sheet=sheets[index];
  const head=index===0?13:6;
  const start=head+1;
  const end=head+s.rows.length+s.blank_rows;
  const last=letters(s.headers.length);
  const all=sheet.getRange(`A1:${last}${end}`);
  sheet.showGridLines=false;
  sheet.tabColor=index===0?colors.ink:'#718096';
  all.format.font={name:font,size:11,color:colors.ink};
  all.format.verticalAlignment='center';
  all.format.rowHeight=24;
  all.format.wrapText=true;
  for(let c=0;c<s.headers.length;c++) sheet.getRange(`${letters(c+1)}1:${letters(c+1)}${end}`).format.columnWidth=widths[s.name][c];
  sheet.getRange(`A1:${last}1`).format.rowHeight=10;
  sheet.getRange('A2').values=[[index===0?spec.title:s.name]];
  sheet.getRange(`A2:${last}2`).format.rowHeight=31;
  sheet.getRange(`A2:${last}2`).format.wrapText=false;
  sheet.getRange('A2').format.font={name:font,size:16,bold:true,color:colors.ink};
  sheet.getRange(`A2:${last}2`).format.borders={bottom:{style:'thin',color:colors.line}};
  sheet.getRange('A3').values=[[index===0?'蓝字可填写；浅灰为公式。样例不是客户记录。排序分不代表招聘概率。':s.notes]];
  sheet.getRange(`A3:${last}3`).format.wrapText=false;
  sheet.getRange('A3').format.font={name:font,size:11,color:colors.muted};
  if(index===0) {
    sheet.getRange('A4').values=[['作者：'+spec.author]];
    sheet.getRange('D4').values=[['微信：'+spec.wechat]];
    sheet.getRange('G4').values=[['公众号：'+spec.official_account]];
    sheet.getRange(`A4:${last}5`).format.wrapText=false;
    sheet.getRange('A5').values=[[spec.personal_site]];
    sheet.getRange('D5').values=[[spec.company_site]];
    sheet.getRange('G5').values=[['版本 '+spec.version+'  '+spec.date]];
    sheet.getRange('A7').values=[['先核实资格，再填四项 0 至 3 分；未知留空；不要把真实个人信息上传公开仓库。']];
    sheet.getRange(`A7:${last}7`).format.wrapText=false;
    sheet.getRange('A7').format.font={name:font,size:11,color:colors.muted};
    sheet.getRange('A9').values=[['排序权重']];
    sheet.getRange('A10').values=[['可修改；合计须为100%']];
    sheet.getRange('A10:C10').format.wrapText=false;
    sheet.getRange('D9:I9').values=[['任务证据','业务表达','可补足程度','偏好','权重合计','输入检查']];
    sheet.getRange('D9:I9').format.font={name:font,size:11,bold:true,color:colors.ink};
    sheet.getRange('D9:I9').format.horizontalAlignment='center';
    sheet.getRange('D10:G10').values=[[.4,.25,.2,.15]];
    sheet.getRange('D10:G10').format={fill:'#FFF3CF',font:{name:font,size:11,color:colors.input},horizontalAlignment:'center'};
    sheet.getRange('D10:H10').setNumberFormat('0%');
    sheet.getRange('H10').formulas=[['=SUM(D10:G10)']];
    sheet.getRange('H10').format.horizontalAlignment='center';
    sheet.getRange('I10').formulas=[['=IF(AND(COUNT(D10:G10)=4,MIN(D10:G10)>=0,MAX(D10:G10)<=1,ABS(H10-1)<0.000001),"可计算","请检查权重")']];
    sheet.getRange('I10').conditionalFormats.add('containsText',{text:'请检查',format:{fill:colors.warning,font:{bold:true,color:'#A22424'}}});
    sheet.getRange('A11').values=[['四项均为 0 至 3 分。每项须在右栏写依据；0 分有效，留空表示未知。可补足程度应符合计划期。']];
    sheet.getRange(`A11:${last}11`).format.wrapText=false;
    sheet.getRange('A11').format.font={name:font,size:11,color:colors.muted};
    for(const r of [6,8,12]) sheet.getRange(`A${r}:${last}${r}`).format.rowHeight=8;
  } else {
    sheet.getRange('A4').values=[['蓝字为可编辑输入。下方预留填写行；使用前替换样例。未知日期留空，按真实事件填写。']];
    sheet.getRange(`A4:${last}4`).format.wrapText=false;
    sheet.getRange('A4').format.font={name:font,size:11,color:colors.muted};
  }

  sheet.getRange(`A${head}:${last}${head}`).values=[s.headers];
  const data=s.rows.map(row => row.map((v,c)=>cellText(v,s.headers[c])));
  sheet.getRange(`A${start}:${last}${start+data.length-1}`).values=data;
  const table=sheet.tables.add(`A${head}:${last}${end}`,true,tableNames[index]);
  table.style='TableStyleLight9';
  table.showFilterButton=true;
  const header=sheet.getRange(`A${head}:${last}${head}`);
  header.format={fill:colors.ink,font:{name:font,size:11,bold:true,color:'#FFFFFF'},horizontalAlignment:'center',verticalAlignment:'center',wrapText:true,rowHeight:36};
  header.format.borders={insideVertical:{style:'thin',color:'#FFFFFF'}};
  const body=sheet.getRange(`A${start}:${last}${end}`);
  body.format.font={name:font,size:11,color:colors.input};
  body.format.verticalAlignment='top';
  body.format.rowHeight=30;
  for(let r=start;r<=end;r++) rowStyle(sheet,`A${r}:${last}${r}`,r<start+data.length?colors.sample:(r%2===0?'#F8FAFC':'#FFFFFF'));
  sheet.getRange(`A${start}:${last}${start+data.length-1}`).format.rowHeight=index===0?44:52;
  for(let c=0;c<s.headers.length;c++) {
    const address=`${letters(c+1)}${start}:${letters(c+1)}${end}`;
    if(dates.has(s.headers[c])) {
      sheet.getRange(address).setNumberFormat('yyyy-mm-dd');
      sheet.getRange(address).format.horizontalAlignment='center';
    }
  }
  list(sheet,`A${start}:A${end}`,['真实记录','教学模拟','填写示例','真实岗位研究示例']);
  if(index===0) {
    list(sheet,`C${start}:C${end}`,['待确认','满足','不满足']);
    sheet.dataValidations.add({range:`D${start}:G${end}`,rule:{type:'whole',operator:'between',formula1:0,formula2:3}});
    sheet.getRange(`D${start}:H${end}`).format.horizontalAlignment='center';
    const f=`=IF(AND(C${start}="满足",COUNT(D${start}:G${start})=4,MIN(D${start}:G${start})>=0,MAX(D${start}:G${start})<=3,$I$10="可计算"),SUMPRODUCT(D${start}:G${start},$D$10:$G$10)/3*100,"")`;
    sheet.getRange(`H${start}`).formulas=[[f]];
    sheet.getRange(`H${start}:H${end}`).fillDown();
    sheet.getRange(`H${start}:H${end}`).setNumberFormat('0.0');
    sheet.getRange(`H${start}:H${end}`).format.font={name:font,size:11,color:colors.ink,bold:true};
    sheet.getRange(`H${start}:H${end}`).format.fill=colors.pale;
    sheet.getRange(`C${start}:C${end}`).conditionalFormats.add('containsText',{text:'待确认',format:{fill:'#FFF0C2',font:{color:'#825E0C'}}});
    sheet.getRange(`C${start}:C${end}`).conditionalFormats.add('containsText',{text:'不满足',format:{fill:colors.warning,font:{color:'#A22424'}}});
  }
  if(s.name==='能力证据') list(sheet,`E${start}:E${end}`,['真实工作','学校项目','自主研究','教学模拟','课程或自主模拟','课程证书']);
  if(s.name==='行动计划') list(sheet,`I${start}:I${end}`,['未开始','进行中','待复核','已完成','已停止']);
  if(s.name==='申请记录') {
    list(sheet,`D${start}:D${end}`,['待确认','满足','不满足']);
    list(sheet,`J${start}:J${end}`,['尚未提交','已提交','收到测评','面试中','等待结果','已拒绝','已获录用','已撤回']);
  }
  if(s.name==='资格核验') list(sheet,`H${start}:H${end}`,['待确认','符合所核条件','不符合所核条件','需补材料']);
  sheet.freezePanes.freezeRows(head);
  sheet.freezePanes.freezeColumns(index===0?2:2);
  layouts.push({name:s.name,head,start,end,last,columns:s.headers.length});

  // CSV is the editable source template. Excel-only formulas intentionally remain
  // blank; their specification is in csv/README.md and the XLSX owns calculation.
  const quote=v => '"'+String(v??'').replaceAll('"','""')+'"';
  const csvRows=[s.headers,...s.rows,...Array.from({length:s.blank_rows},()=>Array(s.headers.length).fill(''))];
  await fs.writeFile(path.join(repo,'templates/csv',`${String(index+1).padStart(2,'0')}-${tableNames[index]}.csv`),'\uFEFF'+csvRows.map(row=>row.map(quote).join(',')).join('\r\n')+'\r\n','utf8');
}

const choice=sheets[0];
const first=layouts[0].start,last=layouts[0].end;
const events=[];
const value=a=>choice.getRange(a).values[0][0];
const near=(x,y)=>typeof x==='number'&&Math.abs(x-y)<1e-7;
const expect=(label,ok,actual)=>{events.push({check:label,passed:!!ok,actual}); if(!ok) throw new Error(label+': '+JSON.stringify(actual));};
wb.recalculate();
expect('样例1得分',near(value(`H${first}`),200/3),value(`H${first}`));
expect('样例2得分',near(value(`H${first+1}`),175/3),value(`H${first+1}`));
expect('硬门槛待确认不计算',value(`H${first+2}`)==='',value(`H${first+2}`));
choice.getRange(`C${first}`).values=[['待确认']]; wb.recalculate();
expect('资格从满足改待确认时分数清空',value(`H${first}`)==='',value(`H${first}`));
choice.getRange(`C${first}`).values=[['满足']];
choice.getRange(`D${first}`).values=[[null]]; wb.recalculate();
expect('缺少一项评分不计算',value(`H${first}`)==='',value(`H${first}`));
choice.getRange(`D${first}`).values=[[0]]; wb.recalculate();
expect('零分为有效输入',near(value(`H${first}`),40),value(`H${first}`));
choice.getRange(`D${first}`).values=[[4]]; wb.recalculate();
expect('越界评分不计算',value(`H${first}`)==='',value(`H${first}`));
choice.getRange(`D${first}`).values=[[3]]; wb.recalculate();
expect('修改任务证据使分数更新',near(value(`H${first}`),80),value(`H${first}`));
choice.getRange(`D${first}`).values=[[2]];
choice.getRange('D10').values=[[.5]]; wb.recalculate();
expect('权重总和错误阻断结果',value(`H${first}`)===''&&value('I10')==='请检查权重',{score:value(`H${first}`),status:value('I10')});
choice.getRange('D10').values=[[.4]];
choice.getRange(`A${last}:G${last}`).values=[['教学模拟','扩展行测试','满足',3,3,3,3]]; wb.recalculate();
expect('最后预留行公式可用',near(value(`H${last}`),100),value(`H${last}`));
choice.getRange(`A${last}:G${last}`).clear({applyTo:'contents'});
wb.recalculate();
expect('临时测试数据已还原',near(value(`H${first}`),200/3)&&value(`H${last}`)==='',{first:value(`H${first}`),last:value(`H${last}`)});

const err=await wb.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A|#NUM!|#NULL!|#SPILL!|#CALC!',options:{useRegex:true,maxResults:100},summary:'final formula error scan',maxChars:2500});
await fs.writeFile(path.join(outputDir,'formula-error-scan.ndjson'),err.ndjson);
const summary=await wb.inspect({kind:'table',range:`职能选择!A${layouts[0].head}:I${first+2}`,include:'values,formulas',tableMaxRows:5,tableMaxCols:9,maxChars:6000});
await fs.writeFile(path.join(outputDir,'formula-inspection.ndjson'),summary.ndjson);

const xlsxPath=path.join(outputDir,'business-job-workbook.xlsx');
await (await SpreadsheetFile.exportXlsx(wb)).save(xlsxPath);
await fs.copyFile(xlsxPath,path.join(repo,'downloads/business-job-workbook.xlsx'));

const previews=[];
for(let i=0;i<layouts.length;i++) {
  const l=layouts[i];
  const segments=i===0?[`A1:I${l.start+3}`]:(l.columns>11?[`A1:F${l.start+2}`,`G1:J${l.start+2}`,`K1:${l.last}${l.start+2}`]:[`A1:E${l.start+2}`,`F1:${l.last}${l.start+2}`]);
  for(let j=0;j<segments.length;j++) {
    const preview=await wb.render({sheetName:l.name,range:segments[j],scale:1.4,format:'png'});
    const target=path.join(outputDir,`preview-${i+1}-${j+1}.png`);
    await fs.writeFile(target,new Uint8Array(await preview.arrayBuffer()));
    previews.push({sheet:l.name,range:segments[j],file:target});
  }
}

const reopened=await SpreadsheetFile.importXlsx(await FileBlob.load(xlsxPath));
reopened.recalculate();
const reopenedChoice=reopened.worksheets.getItem('职能选择');
const saved=reopenedChoice.getRange(`H${first}:H${first+2}`).values.map(r=>r[0]);
expect('XLSX重新导入保留公式结果',near(saved[0],200/3)&&near(saved[1],175/3)&&saved[2]==='',saved);
const verification={checked:spec.date,engine:'@oai/artifact-tool (bundled runtime); Excel desktop not executed',sheets:layouts,events,previews,export:xlsxPath,formula_error_scan:err.ndjson,visual_review:'pending'};
await fs.writeFile(path.join(outputDir,'workbook-validation.json'),JSON.stringify(verification,null,2)+'\n');

await fs.writeFile(path.join(repo,'templates/csv/README.md'),`# CSV 可编辑模板\n\n版本 ${spec.version}，${spec.date}。七张表对应工作簿七个入口。\n\n蓝色输入、下拉、冻结行列和排序公式在 Excel 工作簿中可用。CSV 只保留字段、样例和空白填写行，不保留格式、下拉或公式。职能选择 CSV 的排序分留空；自动计算请使用 business-job-workbook.xlsx。\n\n岗位研究含公开招聘来源样例；其他示例为教学模拟或填写示例，均不是客户记录。使用前替换示例。保留记录性质，不把模拟写成真实工作。不要把已填写的个人求职记录提交到公开仓库。\n\n排序分仅在硬门槛为“满足”、四项评分均为 0 至 3 且权重有效时计算。默认权重依次为 40%、25%、20%、15%，按加权分除以 3 再乘 100；结果仅用于个人排序，不是招聘概率。硬门槛待确认、不满足、评分缺失或权重合计不为100%时留空。权重在工作簿职能选择表 D10:G10 可编辑。\n\n数字零与未知不同。日期格式为 YYYY-MM-DD；未知日期留空。申请事件按实际发生填写，不从最后结果反推中间事件。\n\n作者：${spec.author}。微信：${spec.wechat}。公众号：${spec.official_account}。个人官网：${spec.personal_site}。公司官网：${spec.company_site}。免费内容完整开放，咨询用于方向判断、材料诊断和面试陪跑，不承诺录用或薪资。\n`,'utf8');
console.log(JSON.stringify({xlsx:path.join(repo,'downloads/business-job-workbook.xlsx'),outputDir,sheets:layouts.length,checks:events.length,previews:previews.length,formula_scan:err.ndjson},null,2));
