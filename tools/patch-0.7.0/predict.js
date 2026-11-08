/* UTAC Keryx 0.7.0 — word prediction for physical keyboards. GPL-3.0-or-later.
 * Offline n-gram engine: completes the word being typed and proposes the next one.
 * General model: lex/<lang>.json (word frequencies + word pairs, see tools/lexicon/build_lexicon.py).
 * Personal model: words, pairs and triples from the messages the person speaks, kept per profile and language
 * on this device, with a slow decay so that recent use counts more (cache model; Kuhn & De Mori, 1990).
 * A word that is not in the general vocabulary is only proposed after it has been used twice. */
const KeryxPredict=(()=>{
 const APOS=/[’]/g;
 const fold=s=>String(s).normalize('NFD').replace(/[̀-ͯ]/g,'').toLocaleLowerCase().replace(APOS,"'");
 const lower=s=>String(s).normalize('NFC').toLocaleLowerCase().replace(APOS,"'");
 const ELIDE={ca:/^([ldsmtn]['’])(.*)$/iu,fr:/^((?:jusqu|lorsqu|puisqu|quoiqu|qu|[ldjcnsmt])['’])(.*)$/iu};
 const TOKEN=/[\p{L}\p{N}](?:[\p{L}\p{N}·-]|['’](?=[\p{L}]))*['’]?/gu;
 const HALF_DAYS=60,MAX={u:3000,b:5000,t:5000},MIN_NEW=2,SEP='\u0001';
 const lex={},loading={};
 function prepare(d){
  const words=d.words.split('\n'),n=words.length,low=words.map(lower),folded=low.map(fold);
  const order=Array.from({length:n},(_,i)=>i).sort((a,b)=>folded[a]<folded[b]?-1:folded[a]>folded[b]?1:a-b);
  const keys=order.map(i=>folded[i]);const index=new Map();low.forEach((w,i)=>{if(!index.has(w))index.set(w,i);});
  const zipf=Float32Array.from(d.zipf,z=>z/10);const next=new Map();
  for(const [k,row]of Object.entries(d.next||{}))next.set(Number(k),row);
  return{lang:d.lang,words,low,folded,order,keys,index,zipf,next,src:d.src||''};
 }
 function load(lang,base='lex/'){
  if(lex[lang])return Promise.resolve(lex[lang]);
  if(!loading[lang])loading[lang]=fetch(base+lang+'.json').then(r=>{if(!r.ok)throw Error('HTTP '+r.status);return r.json();}).then(d=>lex[lang]=prepare(d)).catch(e=>{delete loading[lang];throw e;});
  return loading[lang];
 }
 const ready=lang=>lex[lang]||null;
 const today=()=>Math.floor(Date.now()/864e5);
 const emptyModel=()=>({u:{},b:{},t:{},x:[]});
 function cleanModel(m){
  const out=emptyModel();if(!m||typeof m!=='object')return out;
  for(const k of ['u','b','t'])if(m[k]&&typeof m[k]==='object'&&!Array.isArray(m[k]))for(const [w,v]of Object.entries(m[k])){if(w.length<=200&&Array.isArray(v)&&Number.isFinite(v[0])&&v[0]>0&&Number.isFinite(v[1]))out[k][w]=k==='u'&&typeof v[2]==='string'&&v[2].length<=100?[v[0],v[1],v[2]]:[v[0],v[1]];}
  if(Array.isArray(m.x))out.x=m.x.filter(w=>typeof w==='string'&&w.length<=100).slice(-500);
  return out;
 }
 const decay=(v,now)=>v[0]*Math.pow(0.5,Math.max(0,now-v[1])/HALF_DAYS);
 function splitElision(lang,tok){const re=ELIDE[lang];if(!re)return[tok];const m=tok.match(re);return m&&m[2]?[m[1],m[2]]:[tok];}
 /* Sentences of lower-case tokens; `forms` keeps how each word was written when it was not at a sentence start. */
 function sentences(lang,text){
  const out=[];for(const part of String(text).split(/[.!?¡¿\n…]+/u)){const toks=[];for(const m of part.matchAll(TOKEN)){if(/\d/u.test(m[0]))continue;for(const t of splitElision(lang,m[0]))toks.push(t.replace(APOS,"'"));}if(toks.length)out.push(toks);}return out;
 }
 function bump(map,key,now,form){const v=map[key];if(v){v[0]=decay(v,now)+1;v[1]=now;if(form!==undefined){if(form)v[2]=form;else v.length=2;}}else map[key]=form?[1,now,form]:[1,now];}
 function prune(map,max,now){const keys=Object.keys(map);if(keys.length<=max*1.1)return;keys.sort((a,b)=>decay(map[a],now)-decay(map[b],now));for(const k of keys.slice(0,keys.length-max))delete map[k];}
 function learn(model,lang,text){
  model.rev=(model.rev||0)+1;const now=today(),blocked=new Set(model.x);let n=0;
  for(const toks of sentences(lang,text)){
   const low=toks.map(lower);
   low.forEach((w,i)=>{if(blocked.has(w))return;const original=toks[i];const form=i>0&&original!==w&&original!==original.toLocaleUpperCase()?original:(i>0?'':undefined);bump(model.u,w,now,form);n++;
    const p1=i?low[i-1]:'<s>';if(!blocked.has(p1))bump(model.b,p1+SEP+w,now);
    if(i>=1){const p2=i>=2?low[i-2]:'<s>';if(!blocked.has(p2)&&!blocked.has(p1))bump(model.t,p2+SEP+p1+SEP+w,now);}});
  }
  prune(model.u,MAX.u,now);prune(model.b,MAX.b,now);prune(model.t,MAX.t,now);return n;
 }
 function forget(model,word){model.rev=(model.rev||0)+1;const w=lower(word);delete model.u[w];for(const k of ['b','t'])for(const key of Object.keys(model[k]))if(key.split(SEP).includes(w))delete model[k][key];if(!model.x.includes(w))model.x.push(w);if(model.x.length>500)model.x.shift();}
 function unforget(model,word){model.rev=(model.rev||0)+1;const w=lower(word);model.x=model.x.filter(x=>x!==w);}
 function learned(model){const now=today();return Object.entries(model.u).map(([w,v])=>({word:v[2]||w,key:w,uses:Math.round(decay(v,now)*10)/10})).sort((a,b)=>b.uses-a.uses||a.word.localeCompare(b.word));}
 /* Words and pairs of the person's own phrase bank: always known, never decay. */
 function phraseModel(lang,texts){const m={u:new Map(),b:new Map(),n:0};for(const text of texts)for(const toks of sentences(lang,text)){const low=toks.map(lower);low.forEach((w,i)=>{m.u.set(w,(m.u.get(w)||0)+1);m.n++;const k=(i?low[i-1]:'<s>')+SEP+w;m.b.set(k,(m.b.get(k)||0)+1);});}return m;}
 function context(lang,before){
  const tail=before.split(/[.!?¡¿\n…]/u).pop();const toks=[];for(const m of tail.matchAll(TOKEN)){if(/\d/u.test(m[0])){toks.length=0;continue;}for(const t of splitElision(lang,m[0]))toks.push(lower(t));}
  const p1=toks.length?toks[toks.length-1]:'<s>',p2=toks.length>1?toks[toks.length-2]:'<s>';return{p1,p2,start:!toks.length};
 }
 const caches=new WeakMap();
 function indexOf(model,now){let c=caches.get(model);if(c&&c.rev===model.rev&&c.now===now)return c;
  c={rev:model.rev,now,uTotal:0,b:new Map(),t:new Map()};for(const v of Object.values(model.u))c.uTotal+=decay(v,now);c.uTotal=c.uTotal||1;
  for(const k of ['b','t'])for(const [key,v]of Object.entries(model[k])){const cut=key.lastIndexOf(SEP);const ctx=key.slice(0,cut+1),w=key.slice(cut+1);let e=c[k].get(ctx);if(!e)c[k].set(ctx,e={total:0,words:[]});const d=decay(v,now);e.total+=d;e.words.push(w);}
  caches.set(model,c);return c;}
 function suggest({text,cursor,lang,model,phrases,count=3}){
  const L=lex[lang];if(!L)return[];model=model||emptyModel();
  const prefix=text.slice(0,cursor);let token=(prefix.match(/[\p{L}\p{N}’'·-]+$/u)||[''])[0];if(/\d/u.test(token))return[];
  let typed=token,lead='';const el=ELIDE[lang]&&token.match(ELIDE[lang]);if(el){lead=el[1];typed=el[2];}
  const before=prefix.slice(0,cursor-typed.length);
  if(!typed){ // next word: after a space, or straight after an elided article such as l'
   if(!lead){if(!/\s$/u.test(before))return[];const head=before.trimEnd();if(head&&!/[\p{L}\p{N}’'.!?…,;:)»"]$/u.test(head))return[];if(!head)return[];}
  }
  const ctx=context(lang,lead?before:before);const now=today(),blocked=new Set(model.x);
  const X=indexOf(model,now),uTotal=X.uTotal;
  const tPref=ctx.p2+SEP+ctx.p1+SEP,bPref=ctx.p1+SEP;const tE=X.t.get(tPref),bE=X.b.get(bPref);const tTot=tE?.total||1,bTot=bE?.total||1;
  const baseCtx=L.index.has(ctx.p1)?L.next.get(L.index.get(ctx.p1)):ctx.p1==='<s>'?L.next.get(-1):null;
  const baseNext=new Map();if(baseCtx){for(let i=1;i<baseCtx.length;i+=2)baseNext.set(L.low[baseCtx[i]],baseCtx[i+1]/baseCtx[0]);}
  const ph=phrases||{u:new Map(),b:new Map(),n:0};let phCtx=0;for(const [k,v]of ph.b)if(k.startsWith(bPref))phCtx+=v;
  const ft=fold(typed),lt=lower(typed);const cands=new Map();
  const score=w=>{
   const u=model.u[w],b=model.b[bPref+w],t=model.t[tPref+w],i=L.index.get(w);
   let s=0;if(t)s+=0.30*decay(t,now)/tTot;if(b)s+=0.22*decay(b,now)/bTot;s+=0.18*(baseNext.get(w)||0);
   if(u)s+=0.12*decay(u,now)/uTotal;if(ph.n){s+=0.06*(ph.u.get(w)||0)/ph.n;if(phCtx)s+=0.10*(ph.b.get(bPref+w)||0)/phCtx;}
   if(i!==undefined)s+=0.08*Math.pow(10,L.zipf[i]-9);return s;};
  const known=w=>L.index.has(w)||(model.u[w]&&decay(model.u[w],now)>=MIN_NEW-0.01)||ph.u.has(w);
  const add=(w,fw)=>{if(cands.has(w)||blocked.has(w)||w.endsWith("'")||!known(w))return;if(typed){if(!(fw||fold(w)).startsWith(ft)||w===lt)return;}let s=score(w);if(typed&&!w.startsWith(lt))s*=0.6;if(s>0)cands.set(w,s);};
  if(typed){
   let lo=0,hi=L.keys.length;while(lo<hi){const mid=(lo+hi)>>1;if(L.keys[mid]<ft)lo=mid+1;else hi=mid;}
   // the most frequent words of the range, plus every word the context, the person or the phrases bring
   const range=[];for(let j=lo;j<L.keys.length&&L.keys[j].startsWith(ft);j++)range.push(L.order[j]);
   if(range.length>300){range.sort((x,y)=>x-y);range.length=300;}
   for(const i of range)add(L.low[i],L.folded[i]);
   for(const w of baseNext.keys())add(w);
   for(const w of bE?.words||[])add(w);
   for(const w of tE?.words||[])add(w);
   for(const w of Object.keys(model.u))add(w);for(const w of ph.u.keys())add(w);
  }else{
   for(const w of baseNext.keys())add(w);
   for(const w of bE?.words||[])add(w);
   for(const w of tE?.words||[])add(w);
   for(const k of ph.b.keys())if(k.startsWith(bPref))add(k.slice(bPref.length));
  }
  const capital=typed?(typed.length>1&&typed===typed.toLocaleUpperCase()&&typed!==typed.toLocaleLowerCase()?'upper':typed[0]!==typed[0].toLocaleLowerCase()?'first':''):(!lead&&ctx.start&&/^\P{L}*\p{Lu}/u.test(text)?'first':'');
  const list=[...cands.entries()].sort((a,b)=>b[1]-a[1]).slice(0,count);
  return list.map(([w])=>{const i=L.index.get(w);let v=model.u[w]?.[2]||(i!==undefined?L.words[i]:w);if(capital==='upper')v=v.toLocaleUpperCase();else if(capital==='first')v=v[0].toLocaleUpperCase()+v.slice(1);return{label:v,value:v,kind:'word',start:cursor-typed.length,end:cursor};});
 }
 return{load,ready,suggest,learn,forget,unforget,learned,phraseModel,cleanModel,emptyModel,fold,sentences};
})();
if(typeof module!=='undefined')module.exports=KeryxPredict;
