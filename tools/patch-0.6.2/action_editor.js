/* 0.6.2: editor of the main buttons. Each person can place, resize, show or hide the buttons on a grid: 2 × 5 for the side columns, 12 × 2 below the message. Speak is always shown and always the largest. Without a saved layout the built-in arrangement (which adapts to the screen) is used. */
const ACTION_GRID={side:{cols:2,rows:5},bottom:{cols:12,rows:2}};
const ACTION_BUTTONS=[['speak','speak','speak'],['stop','stop','stop'],['show','show-message','show'],['word','delete-word','backspace'],['clear','clear-all','trash'],['new','new-message','new']];
const ACTION_DEFAULTS={side:{speak:[0,0,2,2,1],stop:[0,2,1,1,1],show:[1,2,1,1,1],word:[0,3,1,1,1],clear:[1,3,1,1,1],new:[0,4,2,1,1]},bottom:{speak:[0,0,4,1,1],stop:[4,0,2,1,1],show:[6,0,2,1,1],word:[8,0,1,1,1],clear:[9,0,1,1,1],new:[10,0,2,1,1]}};
function actionLayoutKind(){return prefs().actionsPosition==='bottom'?'bottom':'side';}
function actionName(k){return {speak:tr('Parlar','Hablar'),stop:tr('Aturar','Detener'),show:tr('Mostrar','Mostrar'),word:tr('Esborrar paraula','Borrar palabra'),clear:tr('Esborrar-ho tot','Borrarlo todo'),new:tr('Nou missatge','Nuevo mensaje')}[k];}
function applyActionLayout(){
 const n=$('composer-actions');if(!n)return;const kind=actionLayoutKind(),L=prefs().actionLayouts?.[kind];
 for(const [,id] of ACTION_BUTTONS){const b=$(id);if(b){b.style.gridColumn='';b.style.gridRow='';b.hidden=false;}}
 if(!L){delete n.dataset.custom;n.style.gridTemplateColumns='';n.style.gridTemplateRows='';for(const [,id] of ACTION_BUTTONS){const b=$(id);if(b)n.append(b);}return;}
 const g=ACTION_GRID[kind];let rows=1;const order=[];
 for(const [k,id] of ACTION_BUTTONS){const b=$(id),it=L[k];if(!b)continue;if(!it||!it[4]){b.hidden=true;continue;}const [x,y,w,h]=it;b.style.gridColumn=(x+1)+' / span '+w;b.style.gridRow=(y+1)+' / span '+h;rows=Math.max(rows,y+h);order.push([y,x,b]);}
 n.dataset.custom='true';n.style.gridTemplateColumns='repeat('+g.cols+',minmax(0,1fr))';n.style.gridTemplateRows=kind==='bottom'?'repeat('+rows+',var(--action-row-h))':'repeat('+rows+',minmax(0,1fr))';
 order.sort((a,b)=>a[0]-b[0]||a[1]-b[1]).forEach(o=>n.append(o[2]));
}
function actionLayoutProblem(L,kind,sel=''){
 const g=ACTION_GRID[kind],shown=ACTION_BUTTONS.map(a=>a[0]).filter(k=>L[k][4]);
 for(const k of shown){const [x,y,w,h]=L[k];if(x<0||y<0||w<1||h<1||x+w>g.cols||y+h>g.rows)return tr('No hi cap dins de la graella.','No cabe dentro de la cuadrícula.');}
 for(let i=0;i<shown.length;i++)for(let j=i+1;j<shown.length;j++){const a=L[shown[i]],b=L[shown[j]];if(a[0]<b[0]+b[2]&&b[0]<a[0]+a[2]&&a[1]<b[1]+b[3]&&b[1]<a[1]+a[3])return tr('Aquest lloc ja l’ocupa ','Este lugar ya lo ocupa ')+'«'+actionName(shown[i]===sel?shown[j]:shown[i])+'».';}
 const area=k=>L[k][2]*L[k][3];for(const k of shown)if(k!=='speak'&&area(k)>=area('speak'))return tr('Parlar ha de ser més gran que la resta de botons.','Hablar debe ser más grande que el resto de botones.');
 return '';
}
function actionEditor(kind=actionLayoutKind(),drafts=null,selected='speak'){
 drafts=drafts||{side:clone(prefs().actionLayouts?.side||ACTION_DEFAULTS.side),bottom:clone(prefs().actionLayouts?.bottom||ACTION_DEFAULTS.bottom)};
 let sel=selected;const g=ACTION_GRID[kind];
 const status=el('p',{class:'ae-status',role:'status','aria-live':'polite'});
 const grid=el('div',{class:'ae-grid ae-'+kind,'data-scan-group':'action-editor-grid',role:'group','aria-label':tr('Graella dels botons','Cuadrícula de los botones')});
 grid.style.gridTemplateColumns='repeat('+g.cols+',minmax(0,1fr))';grid.style.gridTemplateRows='repeat('+g.rows+',minmax(0,1fr))';
 const selName=el('strong',{});
 const toggles=el('div',{class:'ae-toggles'});
 const say=(text)=>{status.textContent=text;status.classList.toggle('error-text',!!text);};
 const tryChange=(fn,focusSel=false)=>{const L=drafts[kind],copy=clone(L);fn(copy);const problem=actionLayoutProblem(copy,kind,sel);if(problem){say(problem);return false;}drafts[kind]=copy;say('');draw(focusSel);return true;};
 const move=(dx,dy)=>{const L=drafts[kind],a=L[sel];if(!a[4]){say(tr('Aquest botó està amagat.','Este botón está oculto.'));return;}
  const copy=clone(L),m=copy[sel];m[0]+=dx;m[1]+=dy;
  const others=ACTION_BUTTONS.map(x=>x[0]).filter(k=>k!==sel&&copy[k][4]&&m[0]<copy[k][0]+copy[k][2]&&copy[k][0]<m[0]+m[2]&&m[1]<copy[k][1]+copy[k][3]&&copy[k][1]<m[1]+m[3]);
  if(others.length===1){const o=copy[others[0]];if(o[2]===a[2]&&o[3]===a[3]){o[0]=a[0];o[1]=a[1];}}
  tryChange(L2=>Object.assign(L2,copy));};
 const resize=(dw,dh)=>tryChange(L=>{L[sel][2]+=dw;L[sel][3]+=dh;});
 const place=(cx,cy)=>{const a=drafts[kind][sel];if(!a[4]){say(tr('Aquest botó està amagat.','Este botón está oculto.'));return;}tryChange(L=>{L[sel][0]=Math.min(cx,g.cols-L[sel][2]);L[sel][1]=Math.min(cy,g.rows-L[sel][3]);});};
 const show=(k,on)=>{if(k==='speak')return;const L=drafts[kind];if(!on){tryChange(c=>{c[k][4]=0;});return;}
  if(tryChange(c=>{c[k][4]=1;}))return;
  for(const [w,h] of [[L[k][2],L[k][3]],[1,1]])for(let y=0;y+h<=g.rows;y++)for(let x=0;x+w<=g.cols;x++){const copy=clone(L);copy[k]=[x,y,w,h,1];if(!actionLayoutProblem(copy,kind)){drafts[kind]=copy;sel=k;say('');draw();return;}}
  say(tr('No queda lloc lliure. Fes més petit o amaga un altre botó.','No queda sitio libre. Haz más pequeño u oculta otro botón.'));draw();};
 function draw(focusSel=false){
  const L=drafts[kind];clear(grid);
  for(let y=0;y<g.rows;y++)for(let x=0;x<g.cols;x++){const c=el('button',{type:'button',class:'ae-cell','aria-label':tr('Casella buida','Casilla vacía')+' '+(x+1)+', '+(y+1)});c.style.gridColumn=String(x+1);c.style.gridRow=String(y+1);c.addEventListener('click',()=>place(x,y));grid.append(c);}
  for(const [k,,ic] of ACTION_BUTTONS){const it=L[k];if(!it[4])continue;const b=el('button',{type:'button',class:'ae-item ae-'+k+(k===sel?' ae-selected':''),'aria-pressed':String(k===sel)},icon(ic),el('span',{},actionName(k)));b.style.gridColumn=(it[0]+1)+' / span '+it[2];b.style.gridRow=(it[1]+1)+' / span '+it[3];b.addEventListener('click',()=>{sel=k;say('');draw(true);});b.dataset.key=k;grid.append(b);}
  selName.textContent=actionName(sel)+(L[sel][4]?'':' · '+tr('amagat','oculto'));
  clear(toggles);for(const [k] of ACTION_BUTTONS){const c=check(actionName(k),!!L[k][4],v=>show(k,v),k==='speak'?tr('Sempre visible.','Siempre visible.'):null);if(k==='speak')c.querySelector('input').disabled=true;toggles.append(c);}
  if(focusSel)grid.querySelector('.ae-selected')?.focus({preventScroll:true});
 }
 const kindRow=el('div',{class:'button-row ae-kinds'});
 for(const [k,label] of [['side',tr('Columna lateral · 2 × 5','Columna lateral · 2 × 5')],['bottom',tr('Sota el missatge · 12 × 2','Debajo del mensaje · 12 × 2')]]){const b=button(label,()=>actionEditor(k,drafts,sel),k===kind?'selected':'');b.setAttribute('aria-pressed',String(k===kind));kindRow.append(b);}
 const ctl=(label,fn,ic)=>{const b=button(label,fn,'ae-ctl',ic);b.dataset.edit='true';return b;};
 const controls=el('div',{class:'ae-controls','data-scan-group':'action-editor-controls'},
  ctl(tr('Esquerra','Izquierda'),()=>move(-1,0)),ctl(tr('Dreta','Derecha'),()=>move(1,0)),ctl(tr('Amunt','Arriba'),()=>move(0,-1)),ctl(tr('Avall','Abajo'),()=>move(0,1)),
  ctl(tr('Més ample','Más ancho'),()=>resize(1,0)),ctl(tr('Més estret','Más estrecho'),()=>resize(-1,0)),ctl(tr('Més alt','Más alto'),()=>resize(0,1)),ctl(tr('Més baix','Más bajo'),()=>resize(0,-1)));
 const save=()=>{const out={};for(const k of ['side','bottom']){const problem=actionLayoutProblem(drafts[k],k);if(problem){say(problem);return;}out[k]=JSON.stringify(drafts[k])===JSON.stringify(ACTION_DEFAULTS[k])?null:drafts[k];}prefs().actionLayouts=out;persist();applyActionLayout();scheduleFitMessage();notify(tr('Botons principals desats.','Botones principales guardados.'));settingsDialog('appearance');};
 const reset=()=>{drafts[kind]=clone(ACTION_DEFAULTS[kind]);say(tr('S’ha recuperat la disposició inicial. Desa per aplicar-la.','Se ha recuperado la disposición inicial. Guarda para aplicarla.'));draw();};
 const body=el('div',{class:'action-editor'},
  el('p',{class:'prose'},tr('Toca un botó de la graella per seleccionar-lo. Després mou-lo, canvia’n la mida o toca una casella buida per portar-l’hi. Parlar sempre és visible i sempre és el botó més gran.','Toca un botón de la cuadrícula para seleccionarlo. Después muévelo, cambia su tamaño o toca una casilla vacía para llevarlo allí. Hablar siempre es visible y siempre es el botón más grande.')),
  kindRow,grid,el('p',{class:'ae-selected-line'},tr('Seleccionat: ','Seleccionado: '),selName),controls,status,
  el('h3',{},tr('Botons visibles','Botones visibles')),toggles);
 draw();
 openDialog(tr('Edició dels botons principals','Edición de los botones principales'),[body],[button(tr('Restablir','Restablecer'),reset),button(tr('Cancel·lar','Cancelar'),()=>settingsDialog('appearance')),button(tr('Desar','Guardar'),save,'primary')],'scroll-dialog');
}
