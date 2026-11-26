/* Static official-source search and TXT export; data never leaves the browser. */
(()=>{'use strict';
const script=document.querySelector('#source-data'),grid=document.querySelector('#source-grid');
if(!script||!grid)return;
const data=JSON.parse(script.textContent),cards=[...grid.querySelectorAll('.source-record')];
const input=document.querySelector('#source-search'),type=document.querySelector('#source-type'),priority=document.querySelector('#source-priority'),more=document.querySelector('#source-more'),status=document.querySelector('#source-status');
const normalize=s=>String(s??'').normalize('NFKC').toLocaleLowerCase('zh-CN');
const terms=data.map(s=>normalize([s.id,s.title,s.url,s.scope,s.claim,s.supports,s.limitation,s.limitations].join(' ')));
const exportButton=document.querySelector('#source-export');
let matches=data,limit=25;
function render(){
 const q=normalize(input.value.trim());
 matches=data.filter((s,i)=>(type.value==='all'||s.type===type.value)&&(!priority.checked||s.priority)&&(!q||terms[i].includes(q)));
 const ids=new Set(matches.slice(0,limit).map(s=>s.id));
 cards.forEach(card=>{card.hidden=!ids.has(card.dataset.id)});
 status.textContent='符合条件 '+matches.length+' 条；当前显示 '+Math.min(limit,matches.length)+' 条。原核对日期不代表实时有效。';
 more.hidden=matches.length<=limit;
 exportButton.disabled=matches.length===0;
 if(!matches.length)status.textContent+=' 没有匹配记录，请修改或清空筛选后再下载。';
}
for(const field of [input,type,priority])field.addEventListener(field===input?'input':'change',()=>{limit=25;render()});
more.addEventListener('click',()=>{limit+=25;render()});
document.querySelector('#source-reset').addEventListener('click',()=>{input.value='';type.value='all';priority.checked=false;limit=25;render();input.focus()});
exportButton.addEventListener('click',()=>{
 if(!matches.length)return;
 const lines=['商科求职官方来源核验清单（历史研究）','作者：AI酋长Andy｜星觉科技','微信：AIPMAndy｜个人官网：https://metaver.vip/｜公司官网：https://www.a6no1.cn/｜服务：https://metaver.vip/services','原记录核对日不是今日招聘状态，请自行重查雇主/政府原文。','筛选条目：'+matches.length,''];
 matches.forEach((s,i)=>lines.push((i+1)+'. ['+s.id+'] '+s.title,'类型：'+s.type+'｜历史核对：'+(s.checked||'未登记'),'适用范围：'+(s.scope||'见原文'),'支持内容：'+(s.claim||s.supports||'需核实'),'已记录限制：'+(s.limitation||s.limitations||'需核实'),'原始来源：'+s.url,'今日核查结果：________  实际核查日期：________',''));
 const url=URL.createObjectURL(new Blob(['\uFEFF',lines.join('\r\n')],{type:'text/plain;charset=utf-8'}));
 const link=document.createElement('a');link.href=url;link.download='andy-business-source-review.txt';link.click();
 setTimeout(()=>URL.revokeObjectURL(url),1000);
});
render();
})();