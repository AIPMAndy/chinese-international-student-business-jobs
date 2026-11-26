(()=>{'use strict';
 const menu=document.querySelector('.menu-button'),nav=document.querySelector('.navlinks');
 if(menu&&nav){
   const mobile=window.matchMedia('(max-width:700px)');
   const isOpen=()=>menu.getAttribute('aria-expanded')==='true';
   const setOpen=open=>{menu.setAttribute('aria-expanded',String(open));nav.classList.toggle('open',open)};
   menu.addEventListener('click',()=>setOpen(mobile.matches&&!isOpen()));
   nav.querySelectorAll('a').forEach(a=>a.addEventListener('click',()=>setOpen(false)));
   document.addEventListener('keydown',event=>{
     if(event.key==='Escape'&&mobile.matches&&isOpen()){
       event.preventDefault();setOpen(false);menu.focus();
     }
   });
   const header=menu.closest('.nav');
   if(header)header.addEventListener('focusout',event=>{
     if(isOpen()&&event.relatedTarget&&!header.contains(event.relatedTarget))setOpen(false);
   });
   mobile.addEventListener('change',()=>setOpen(false));
 }
 document.querySelectorAll('[data-filter]').forEach(button=>button.addEventListener('click',()=>{const key=button.dataset.filter;document.querySelectorAll('[data-filter]').forEach(b=>b.setAttribute('aria-pressed',String(b===button)));let count=0;document.querySelectorAll('.route[data-key]').forEach(card=>{card.hidden=key!=='all'&&card.dataset.key!==key;if(!card.hidden)count++});const status=document.querySelector('#filter-status');if(status)status.textContent=`显示 ${count} 条职能路线。`; }));
 const copy=document.querySelector('#copy-wechat'),copyStatus=document.querySelector('#copy-status');
 if(copy)copy.addEventListener('click',async()=>{try{await navigator.clipboard.writeText('AIPMAndy');copyStatus.textContent='已复制微信号：AIPMAndy'}catch{copyStatus.textContent='请手动复制微信号：AIPMAndy'}});
 const input=document.querySelector('#guide-search'),results=document.querySelector('#search-results'),status=document.querySelector('#search-status'),clear=document.querySelector('#clear-guide-search');
 let timer;
 if(input&&results&&status){
   const render=()=>{
     clearTimeout(timer);
     results.replaceChildren();
     const q=input.value.trim().toLocaleLowerCase();
     if(clear)clear.disabled=!q;
     if(!q){status.textContent='可搜索职能、地区、案例和准备方法。';return;}
     const entries=Array.isArray(window.GUIDE_SEARCH)?window.GUIDE_SEARCH:[];
     const found=entries.filter(entry=>(entry.title+' '+entry.text).toLocaleLowerCase().includes(q));
     const matches=found.slice(0,15);
     status.textContent=found.length?`找到 ${found.length} 条相关内容${found.length>15?'（显示前 15 条）':''}。`:'没有匹配内容，试试“咨询”“德国”“毕业”或“现金”。';
     for(const entry of matches){
       const li=document.createElement('li'),a=document.createElement('a'),p=document.createElement('p');
       a.href=entry.href;
       a.textContent=entry.title;
       const idx=entry.text.toLocaleLowerCase().indexOf(q);
       const begin=Math.max(0,idx-30);
       p.textContent=(begin?'…':'')+entry.text.slice(begin,begin+135)+'…';
       li.append(a,p);results.append(li);
     }
   };
   input.addEventListener('input',()=>{clearTimeout(timer);timer=setTimeout(render,120);if(clear)clear.disabled=!input.value.trim();});
   if(clear)clear.addEventListener('click',()=>{input.value='';render();input.focus();});
 }
})();
