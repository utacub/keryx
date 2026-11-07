# Applies the UTAC Keryx 0.6.3 changes to the built UTAC_Keryx_v0.6.2_local.html.
# Usage: python3 patch063.py UTAC_Keryx_v0.6.2_local.html UTAC_Keryx_v0.6.3_local.html
# GPL-3.0-or-later.
import sys, re, json
src,dst=sys.argv[1],sys.argv[2]
s=open(src,encoding='utf-8',newline='').read()
def rep(a,b,count=1):
    global s
    n=s.count(a); assert n==count,(a[:60],n); s=s.replace(a,b)
s=re.sub(r'(?<!/\* )0\.6\.2(?!:)','0.6.3',s)

# --- new instructions in the editor (all six languages)
OLD="Toca un botó de la graella per seleccionar-lo. Després mou-lo, canvia’n la mida o toca una casella buida per portar-l’hi. Parlar sempre és visible i sempre és el botó més gran."
NEW="Arrossega un botó per moure’l, o la seva cantonada per canviar-ne la mida. També pots tocar un botó per seleccionar-lo i fer servir els controls («Mostrar controls»), o tocar una casella buida per portar-l’hi. Parlar sempre és visible i sempre és el botó més gran."
TR={'eu':"Arrastatu botoi bat mugitzeko, edo bere izkina tamaina aldatzeko. Botoi bat ukitu eta kontrolak ere erabil ditzakezu («Erakutsi kontrolak»), edo gelaxka huts bat ukitu hara eramateko. Hitz egin beti dago ikusgai eta beti da botoirik handiena.",
    'gl':"Arrastra un botón para movelo, ou a súa esquina para cambiar o tamaño. Tamén podes tocar un botón para seleccionalo e usar os controis («Mostrar controis»), ou tocar unha casa baleira para levalo alí. Falar sempre está visible e sempre é o botón máis grande.",
    'en':"Drag a button to move it, or its corner to resize it. You can also tap a button to select it and use the controls (“Show controls”), or tap an empty cell to put it there. Speak is always shown and is always the largest button.",
    'fr':"Faites glisser un bouton pour le déplacer, ou son coin pour changer sa taille. Vous pouvez aussi toucher un bouton pour le sélectionner et utiliser les commandes (« Afficher les commandes »), ou toucher une case vide pour l’y mettre. Parler est toujours visible et toujours le plus grand bouton."}
for lang,v in TR.items():
    rep('"%s":{"'%lang,'"%s":{'%lang+json.dumps(NEW,ensure_ascii=False)+':'+json.dumps(v,ensure_ascii=False)+',"')
rep("tr('%s','Toca un botón de la cuadrícula para seleccionarlo. Después muévelo, cambia su tamaño o toca una casilla vacía para llevarlo allí. Hablar siempre es visible y siempre es el botón más grande.')"%OLD,
    "tr('%s','Arrastra un botón para moverlo, o su esquina para cambiar su tamaño. También puedes tocar un botón para seleccionarlo y usar los controles («Mostrar controles»), o tocar una casilla vacía para llevarlo allí. Hablar siempre es visible y siempre es el botón más grande.')"%NEW)

# --- the selected button gets a resize handle in its corner
rep("b.dataset.key=k;grid.append(b);}","b.dataset.key=k;if(k===sel)b.append(el('i',{class:'ae-handle','aria-hidden':'true'}));grid.append(b);}")

# --- dragging: move a button, or resize it from its corner. The buttons stay, because dragging is not possible for everyone (WCAG 2.2, 2.5.7).
DRAG=r""" /* 0.6.3: drag to move, drag the corner to resize. Moving onto a button of the same size swaps them. */
 const cellAt=e=>{const r=grid.getBoundingClientRect(),cs=getComputedStyle(grid),px=parseFloat(cs.paddingLeft)||0,py=parseFloat(cs.paddingTop)||0,w=r.width-2*px,h=r.height-2*py;return [Math.max(0,Math.min(g.cols-1,Math.floor((e.clientX-r.left-px)/w*g.cols))),Math.max(0,Math.min(g.rows-1,Math.floor((e.clientY-r.top-py)/h*g.rows)))];};
 const swapInto=(copy,k,old)=>{const m=copy[k],hit=ACTION_BUTTONS.map(a=>a[0]).filter(o=>o!==k&&copy[o][4]&&m[0]<copy[o][0]+copy[o][2]&&copy[o][0]<m[0]+m[2]&&m[1]<copy[o][1]+copy[o][3]&&copy[o][1]<m[1]+m[3]);if(hit.length===1){const o=copy[hit[0]];if(o[2]===old[2]&&o[3]===old[3]){o[0]=old[0];o[1]=old[1];}}return copy;};
 let drag=null,suppressClick=false;
 grid.addEventListener('pointerdown',e=>{const item=e.target.closest('.ae-item');if(!item||(e.pointerType==='mouse'&&e.button!==0))return;const k=item.dataset.key,it=drafts[kind][k],[cx,cy]=cellAt(e);drag={k,resize:!!e.target.closest('.ae-handle'),dx:cx-it[0],dy:cy-it[1],old:it.slice(),x0:e.clientX,y0:e.clientY,moved:false,copy:null,item,id:e.pointerId};try{item.setPointerCapture(e.pointerId);}catch{}});
 grid.addEventListener('pointermove',e=>{if(!drag||e.pointerId!==drag.id)return;if(!drag.moved&&Math.hypot(e.clientX-drag.x0,e.clientY-drag.y0)<6)return;e.preventDefault();drag.moved=true;grid.classList.add('ae-dragging');drag.item.classList.add('ae-moving');
  const [cx,cy]=cellAt(e),copy=clone(drafts[kind]),m=copy[drag.k];
  if(drag.resize){m[2]=Math.max(1,Math.min(g.cols-m[0],cx-m[0]+1));m[3]=Math.max(1,Math.min(g.rows-m[1],cy-m[1]+1));}
  else{const over=ACTION_BUTTONS.map(a=>a[0]).find(o=>o!==drag.k&&copy[o][4]&&cx>=copy[o][0]&&cx<copy[o][0]+copy[o][2]&&cy>=copy[o][1]&&cy<copy[o][1]+copy[o][3]),t=over&&copy[over];
   if(t&&t[2]===drag.old[2]&&t[3]===drag.old[3]){m[0]=t[0];m[1]=t[1];t[0]=drag.old[0];t[1]=drag.old[1];}
   else{m[0]=Math.max(0,Math.min(g.cols-m[2],cx-drag.dx));m[1]=Math.max(0,Math.min(g.rows-m[3],cy-drag.dy));swapInto(copy,drag.k,drag.old);}}
  drag.copy=copy;const problem=actionLayoutProblem(copy,kind,drag.k);drag.item.classList.toggle('ae-invalid',!!problem);drag.item.style.gridColumn=(m[0]+1)+' / span '+m[2];drag.item.style.gridRow=(m[1]+1)+' / span '+m[3];for(const it of grid.querySelectorAll('.ae-item')){const o=it.dataset.key;if(o===drag.k)continue;const q=copy[o];it.style.gridColumn=(q[0]+1)+' / span '+q[2];it.style.gridRow=(q[1]+1)+' / span '+q[3];}say(problem);});
 const endDrag=e=>{if(!drag||e.pointerId!==drag.id)return;const d=drag;drag=null;grid.classList.remove('ae-dragging');if(!d.moved)return;suppressClick=true;setTimeout(()=>{suppressClick=false;},0);sel=d.k;
  const problem=d.copy?actionLayoutProblem(d.copy,kind,d.k):'';if(d.copy&&!problem){drafts[kind]=d.copy;say('');}else if(problem)say(problem);draw(true);};
 grid.addEventListener('pointerup',endDrag);grid.addEventListener('pointercancel',e=>{if(drag){drag.copy=null;endDrag(e);}});
 grid.addEventListener('click',e=>{if(suppressClick){e.stopPropagation();e.preventDefault();}},true);
"""
rep(" draw();\n openDialog(tr('Edició dels botons principals'",DRAG+" draw();\n openDialog(tr('Edició dels botons principals'")

# --- the tap controls start hidden behind a "Show controls" button; with scanning or dwell they start shown (Marc, 2026-11-07)
T3={"Mostrar controls":["Erakutsi kontrolak","Mostrar controis","Show controls","Afficher les commandes"],"Amagar controls":["Ezkutatu kontrolak","Ocultar controis","Hide controls","Masquer les commandes"]}
for i,lang in enumerate(['eu','gl','en','fr']):
    ins=''.join(json.dumps(k,ensure_ascii=False)+':'+json.dumps(v[i],ensure_ascii=False)+',' for k,v in T3.items())
    rep('"%s":{"'%lang,'"%s":{'%lang+ins+'"')
rep(" const save=()=>{",
    " if(typeof aeControlsOpen==='undefined'||aeControlsOpen===null)aeControlsOpen=prefs().access!=='direct';controls.hidden=!aeControlsOpen;\n"
    " const ctlToggle=button('',()=>{aeControlsOpen=controls.hidden;controls.hidden=!aeControlsOpen;paintToggle();if(aeControlsOpen)controls.querySelector('button')?.focus({preventScroll:true});},'ae-toggle-controls');ctlToggle.setAttribute('aria-controls','ae-controls');controls.id='ae-controls';\n"
    " const paintToggle=()=>{clear(ctlToggle).append(icon('down'),el('span',{},controls.hidden?tr('Mostrar controls','Mostrar controles'):tr('Amagar controls','Ocultar controles')));ctlToggle.setAttribute('aria-expanded',String(!controls.hidden));ctlToggle.classList.toggle('open',!controls.hidden);};paintToggle();\n"
    " const save=()=>{")
rep("kindRow,grid,el('p',{class:'ae-selected-line'},tr('Seleccionat: ','Seleccionado: '),selName),controls,status,",
    "kindRow,grid,el('div',{class:'ae-selected-row'},el('p',{class:'ae-selected-line'},tr('Seleccionat: ','Seleccionado: '),selName),ctlToggle),controls,status,")
rep("function actionEditor(kind=actionLayoutKind(),drafts=null,selected='speak'){","let aeControlsOpen=null;\nfunction actionEditor(kind=actionLayoutKind(),drafts=null,selected='speak'){")

CSS="""
/* 0.6.3: dragging in the editor of the main buttons */
.ae-grid{touch-action:none;user-select:none;-webkit-user-select:none}
.ae-item{cursor:grab}.ae-dragging .ae-item{cursor:grabbing}
.ae-item.ae-moving{z-index:3;opacity:.92;box-shadow:0 4px 14px #0004}
.ae-item.ae-invalid{outline:4px dashed var(--danger)!important;outline-offset:2px}
.ae-dragging .ae-cell{border-color:var(--muted)}
.ae-handle{position:absolute;right:0;bottom:0;width:26px;height:26px;cursor:nwse-resize;touch-action:none;border-radius:9px 0 7px 0;background:linear-gradient(135deg,transparent 0 45%,currentColor 45% 55%,transparent 55% 65%,currentColor 65% 75%,transparent 75%)}
.ae-bottom .ae-handle{width:16px;height:16px}
.ae-selected-row{display:flex;align-items:center;justify-content:space-between;gap:8px;flex-wrap:wrap}.ae-toggle-controls .icon{transition:transform .15s}.ae-toggle-controls.open .icon{transform:rotate(180deg)}
"""
i=s.rindex('</style>'); s=s[:i]+CSS+s[i:]
open(dst,'w',encoding='utf-8',newline='').write(s)
print('ok',dst)
