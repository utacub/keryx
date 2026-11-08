# Applies the UTAC Keryx 0.6.9 change to the built UTAC_Keryx_v0.6.8_local.html (Marc, 2026-11-08):
# - Phrases tab works with folders: the top level shows the folders (the former categories), and inside each folder
#   its phrases as before. New folders can be made down to three levels. The category drop-down and the
#   Categories button are removed; buttons to create and manage folders and phrases are added.
# - Settings -> Access: panel cards in fixed pages (as until now) or in a scrolling list.
# - Main buttons: the side grid is 3 x 6 and the group also holds Save (as phrase) and More, which leave the writing area.
# Usage: python3 patch069.py UTAC_Keryx_v0.6.8_local.html UTAC_Keryx_v0.6.9_local.html
import sys, re, json
src,dst=sys.argv[1],sys.argv[2]
s=open(src,encoding='utf-8',newline='').read()
def rep(a,b,count=1):
    global s
    n=s.count(a); assert n==count,(a[:90],n); s=s.replace(a,b)
s=re.sub(r'(?<!/\* )0\.6\.8(?!:)','0.6.9',s)

# ---------- Data: folders are categories with an optional parent, at most three levels ----------
rep("const cids=new Set();const categories=p.categories.map(c=>{const id=str(c.id,80,true);if(cids.has(id))throw Error('Duplicate category');cids.add(id);return{id,texts:texts(c.texts,100)};});",
    "const cids=new Set();const categories=p.categories.map(c=>{const id=str(c.id,80,true);if(cids.has(id))throw Error('Duplicate category');cids.add(id);const out={id,texts:texts(c.texts,100)};if(typeof c.parent==='string'&&c.parent.length<=80)out.parent=c.parent;return out;});"
    "{const by=new Map(categories.map(c=>[c.id,c]));for(const c of categories)if(c.parent&&(!by.has(c.parent)||c.parent===c.id))delete c.parent;for(const c of categories){let d=1,x=c;const seen=new Set([c.id]);while(x.parent){if(seen.has(x.parent)||d>=3){delete c.parent;break;}seen.add(x.parent);x=by.get(x.parent);d++;}}}")
# Settings: list mode
rep("actionsPosition:'bottom',uppercase:false,","actionsPosition:'bottom',listMode:'pages',uppercase:false,")
rep("for(const [k,a] of Object.entries({theme:THEMES.ids,","for(const [k,a] of Object.entries({listMode:['pages','scroll'],theme:THEMES.ids,")
# Main button layouts: side grid 3 x 6, Save and More join the group
i=s.index("function actionLayouts(raw){"); j=s.index("return out;}",i)+len("return out;}")
seg=s[i:j]
seg2=seg.replace("const grids={side:[2,6],bottom:[12,2]};","const grids={side:[3,6],bottom:[12,2]};")
seg2=seg2.replace("for(const id of ['speak','stop','show','word','clear','undo','redo','new']){const v=L[id];if(v===undefined&&(id==='undo'||id==='redo')){o[id]=[0,0,1,1,0];continue;}",
                  "const missing=[];for(const id of ['speak','stop','show','word','clear','undo','redo','save','more','new']){const v=L[id];if(v===undefined&&['undo','redo','save','more'].includes(id)){o[id]=[0,0,1,1,0];if(id==='save'||id==='more')missing.push(id);continue;}")
seg2=seg2.replace("if(ok&&o.speak[4]===1)out[k]=o;",
                  "if(ok)for(const id of missing){const busy=(x,y)=>Object.values(o).some(v=>v[4]&&x>=v[0]&&x<v[0]+v[2]&&y>=v[1]&&y<v[1]+v[3]);let done=false;for(let y=0;y<R&&!done;y++)for(let x=0;x<C&&!done;x++)if(!busy(x,y)){o[id]=[x,y,1,1,1];done=true;}}if(ok&&o.speak[4]===1)out[k]=o;")
assert seg2.count('missing')==3 and '[3,6]' in seg2, 'actionLayouts'
s=s[:i]+seg2+s[j:]

rep("const ACTION_GRID={side:{cols:2,rows:6},bottom:{cols:12,rows:2}};","const ACTION_GRID={side:{cols:3,rows:6},bottom:{cols:12,rows:2}};")
rep("['undo','undo','undo'],['redo','redo','redo'],['new','new-message','new']];","['undo','undo','undo'],['redo','redo','redo'],['save','save-phrase','save'],['more','more-tools','edit'],['new','new-message','new']];")
rep("const ACTION_DEFAULTS={side:{speak:[0,0,2,2,1],stop:[0,2,1,1,1],show:[1,2,1,1,1],word:[0,3,1,1,1],clear:[1,3,1,1,1],undo:[0,4,1,1,1],redo:[1,4,1,1,1],new:[0,5,2,1,1]},bottom:{speak:[0,0,4,1,1],stop:[4,0,1,1,1],show:[5,0,1,1,1],word:[6,0,1,1,1],clear:[7,0,1,1,1],undo:[8,0,1,1,1],redo:[9,0,1,1,1],new:[10,0,2,1,1]}};",
    "const ACTION_DEFAULTS={side:{speak:[0,0,3,2,1],stop:[0,2,1,1,1],show:[1,2,1,1,1],save:[2,2,1,1,1],word:[0,3,1,1,1],clear:[1,3,1,1,1],more:[2,3,1,1,1],undo:[0,4,1,1,1],redo:[1,4,1,1,1],new:[2,4,1,1,1]},bottom:{speak:[0,0,3,1,1],stop:[3,0,1,1,1],show:[4,0,1,1,1],word:[5,0,1,1,1],clear:[6,0,1,1,1],undo:[7,0,1,1,1],redo:[8,0,1,1,1],save:[9,0,1,1,1],more:[10,0,1,1,1],new:[11,0,1,1,1]}};")
rep("const ACTION_NARROW_BOTTOM={speak:[0,0,6,1,1],stop:[6,0,3,1,1],show:[9,0,3,1,1],word:[0,1,2,1,1],clear:[2,1,2,1,1],undo:[4,1,2,1,1],redo:[6,1,2,1,1],new:[8,1,4,1,1]};",
    "const ACTION_NARROW_BOTTOM={speak:[0,0,4,1,1],stop:[4,0,2,1,1],show:[6,0,2,1,1],save:[8,0,2,1,1],more:[10,0,2,1,1],word:[0,1,2,1,1],clear:[2,1,2,1,1],undo:[4,1,2,1,1],redo:[6,1,2,1,1],new:[8,1,4,1,1]};")
rep("undo:tr('Desfer','Deshacer'),redo:tr('Refer','Rehacer'),new:tr('Nou missatge','Nuevo mensaje')}[k];}",
    "undo:tr('Desfer','Deshacer'),redo:tr('Refer','Rehacer'),save:tr('Desar frase','Guardar frase'),more:tr('Més eines','Más herramientas'),new:tr('Nou missatge','Nuevo mensaje')}[k];}")
rep(" add(tr('Desar','Guardar'),()=>editPhrase(null,$('message').value),'save','save-phrase').setAttribute('aria-label',tr('Desar frase','Guardar frase'));\n add(tr('Més','Más'),editingDialog,'edit').setAttribute('aria-label',tr('Més eines d’edició','Más herramientas de edición'));\n","")
rep("again.id='redo';again.dataset.edit='true';for(const b of [speak,stop,show,word,wipe,back,again,fresh]){",
    "again.id='redo';again.dataset.edit='true';const keep=button(tr('Desar frase','Guardar frase'),()=>editPhrase(null,$('message').value,prefs().lang,phraseFolder),'save-phrase','save');keep.id='save-phrase';const more=button(tr('Més eines','Más herramientas'),editingDialog,'more-tools','edit');more.id='more-tools';for(const b of [speak,stop,show,word,wipe,back,again,keep,more,fresh]){")
rep("n.append(speak,stop,show,word,wipe,back,again,fresh);applyActionLayout();","n.append(speak,stop,show,word,wipe,back,again,keep,more,fresh);applyActionLayout();")

# ---------- Access setting: fixed pages or scrolling list ----------
rep(",rangeField(tr('Filtre de repetició del mateix botó','Filtro de repetición del mismo botón'),'repeatMs',0,2000,100,x=>x?x+' ms':tr('Desactivat','Desactivado')));\n content.append(button(tr('Aplicar i provar l’accés'",
    ",rangeField(tr('Filtre de repetició del mateix botó','Filtro de repetición del mismo botón'),'repeatMs',0,2000,100,x=>x?x+' ms':tr('Desactivat','Desactivado')),field(tr('Fitxes dels panells','Fichas de los paneles'),selectControl([['pages',tr('Pàgines fixes, sense desplaçament','Páginas fijas, sin desplazamiento')],['scroll',tr('Llista amb desplaçament (scroll)','Lista con desplazamiento (scroll)')]],p.listMode||'pages',v=>{set('listMode',v);applyAppearance();renderWorkspace();}),tr('Respostes, frases, historial i documents: pàgines amb Anterior i Següent, o una sola llista que es desplaça.','Respuestas, frases, historial y documentos: páginas con Anterior y Siguiente, o una sola lista que se desplaza.')));\n content.append(button(tr('Aplicar i provar l’accés'")
rep("$('message').inputMode='text';}","$('message').inputMode='text';document.documentElement.classList.toggle('list-scroll',prefs().listMode==='scroll');}")
rep("qrows=Math.max(1,Math.min(Math.ceil(list.length/qcols)||1,Math.floor((qh+6)/(50*prefs().controlSize+6))))",
    "qrows=prefs().listMode==='scroll'?Math.max(1,Math.ceil(list.length/qcols)):Math.max(1,Math.min(Math.ceil(list.length/qcols)||1,Math.floor((qh+6)/(50*prefs().controlSize+6))))")
rep("const list=docsAll();const size=Math.max(4,Math.min(10,Math.floor(((n.clientHeight||200)+4)/44)));",
    "const list=docsAll();const size=prefs().listMode==='scroll'?Math.max(1,list.length):Math.max(4,Math.min(10,Math.floor(((n.clientHeight||200)+4)/44)));")
rep("const history=getSession().history;const size=Math.max(1,Math.min(5,Math.floor((n.clientHeight||200)/70)));",
    "const history=getSession().history;const size=prefs().listMode==='scroll'?Math.max(1,history.length):Math.max(1,Math.min(5,Math.floor((n.clientHeight||200)/70)));")

# ---------- Phrases tab: folders ----------
rep("activeView=id;panelOpen=true;listPage=0;historyPage=0;renderWorkspace();","activeView=id;panelOpen=true;listPage=0;historyPage=0;if(id==='phrases')phraseFolder=null;renderWorkspace();")
s=s.replace("activeCategory='all';","activeCategory='all';phraseFolder=null;")
rep("const controls=el('div',{class:'library-controls'+(activeView==='phrases'?' with-categories':''),'data-scan-group':'library-search'});",
    "const controls=el('div',{class:'library-controls'+(activeView==='phrases'?' with-folders':''),'data-scan-group':'library-search'});if(phraseFolder&&!folderOf(phraseFolder))phraseFolder=null;")
i=s.index(" if(activeView==='phrases'){const cats=selectControl([['all',tr('Totes les categories','Todas las categorías')]"); j=s.index("\n",i)
s=s[:i]+s[j+1:]
rep("button(tr('Nova frase','Nueva frase'),()=>editPhrase(),'soft','new'));\n if(activeView==='phrases')controls.append(button(tr('Categories','Categorías'),manageCategories,'flat'));\n n.append(controls,el('div',{id:'phrase-grid',class:'phrase-grid'}),",
    "button(tr('Nova frase','Nueva frase'),()=>editPhrase(null,'',prefs().lang,activeView==='phrases'?phraseFolder:null),'soft','new'));\n if(activeView==='phrases'&&folderDepth(phraseFolder)<3)controls.append(button(tr('Nova carpeta','Nueva carpeta'),()=>editFolder(null,phraseFolder),'soft','folderNew'));\n n.append(controls);if(activeView==='phrases'&&phraseFolder)n.append(folderBar());n.append(el('div',{id:'phrase-grid',class:'phrase-grid'}),")

FOLDERS=r"""/* 0.6.9: phrase folders. The former categories are the top-level folders; a folder can hold phrases and other
   folders, down to three levels. Hidden folders (and everything inside) stay out of the panel and of the search. */
let phraseFolder=null;
const FOLDER_LEVELS=3;
function folderOf(id){return id?profile().categories.find(c=>c.id===id):null;}
function folderPath(id){const out=[];let c=folderOf(id);while(c&&out.length<10){out.unshift(c);c=folderOf(c.parent);}return out;}
function folderDepth(id){return folderPath(id).length;}
function folderVisible(id){const path=folderPath(id);return path.length>0&&path.every(c=>prefs().enabledCategories.includes(c.id));}
function folderSubtree(id){const out=new Set([id]);let grew=true;while(grew){grew=false;for(const c of profile().categories)if(c.parent&&out.has(c.parent)&&!out.has(c.id)){out.add(c.id);grew=true;}}return out;}
function folderHeight(id){const kids=profile().categories.filter(c=>c.parent===id);return 1+(kids.length?Math.max(...kids.map(k=>folderHeight(k.id))):0);}
function folderName(id){return folderPath(id).map(categoryLabel).join(' › ');}
function folderCount(id){const ids=folderSubtree(id);return profile().phrases.filter(p=>ids.has(p.category)&&phraseText(p)).length;}
function folderOptions(){const out=[];const walk=(pid)=>{for(const c of profile().categories.filter(c=>(c.parent||null)===pid)){out.push([c.id,folderName(c.id)]);walk(c.id);}};walk(null);return out;}
function openFolder(id){phraseFolder=id||null;listPage=0;renderWorkspace();resetAccess();requestAnimationFrame(()=>{if(keyboardInput||prefs().access!=='direct'){const first=$('phrase-grid')?.querySelector('button');if(first)focusSafely(first);}});}
function folderBar(){const bar=el('nav',{class:'folder-bar','data-scan-group':'folder-path','aria-label':tr('Carpeta actual','Carpeta actual')});const path=folderPath(phraseFolder);
 const up=button(tr('Amunt','Arriba'),()=>openFolder(path.length>1?path[path.length-2].id:null),'soft','folderUp');up.setAttribute('aria-label',tr('Tornar a la carpeta superior','Volver a la carpeta superior'));bar.append(up);
 const root=button(tr('Frases','Frases'),()=>openFolder(null),'flat crumb');bar.append(root);
 path.forEach((c,i)=>{bar.append(el('span',{class:'crumb-sep','aria-hidden':'true'},'›'));if(i<path.length-1)bar.append(button(categoryLabel(c),()=>openFolder(c.id),'flat crumb'));else bar.append(el('strong',{class:'crumb-current','aria-current':'location'},categoryLabel(c)));});
 const edit=button(tr('Editar carpeta','Editar carpeta'),()=>editFolder(phraseFolder),'flat','edit');bar.append(el('span',{class:'spacer'}),edit);
 return bar;}
function editFolder(id=null,parent=phraseFolder){
 const f=folderOf(id),ui=prefs().ui;const input=el('input',{type:'text',maxlength:100,value:f?categoryLabel(f):''});const error=el('p',{class:'error-text',role:'alert'});
 let par=f?(f.parent||null):(parent||null),visible=f?prefs().enabledCategories.includes(f.id):true;
 const own=f?folderSubtree(f.id):new Set(),height=f?folderHeight(f.id):1;
 const options=[['',tr('Nivell superior','Nivel superior')],...folderOptions().filter(([cid])=>!own.has(cid)&&folderDepth(cid)+height<=FOLDER_LEVELS)];
 const where=selectControl(options,par||'',v=>par=v||null);
 const body=[field(tr('Nom de la carpeta','Nombre de la carpeta'),input),field(tr('Dins de','Dentro de'),where,tr('Fins a tres nivells de carpetes.','Hasta tres niveles de carpetas.')),check(tr('Visible al panell','Visible en el panel'),visible,v=>visible=v),error];
 if(f){const move=delta=>{const list=profile().categories,sib=list.filter(c=>(c.parent||null)===(f.parent||null)),k=sib.indexOf(f),other=sib[k+delta];if(!other)return;const a=list.indexOf(f),b=list.indexOf(other);[list[a],list[b]]=[list[b],list[a]];persist();renderWorkspace();notify(tr('Carpeta moguda.','Carpeta movida.'));};body.push(el('div',{class:'button-row'},button(tr('Moure abans','Mover antes'),()=>move(-1)),button(tr('Moure després','Mover después'),()=>move(1))));}
 const save=()=>{const name=input.value.trim();if(!name){error.textContent=tr('Escriu un nom.','Escribe un nombre.');return;}if(par&&folderDepth(par)+height>FOLDER_LEVELS){error.textContent=tr('Hi pot haver tres nivells de carpetes com a màxim.','Puede haber tres niveles de carpetas como máximo.');return;}
  let target=f;if(f){f.texts[ui]=name;}else{if(profile().categories.length>=100){error.textContent=tr('Hi pot haver 100 carpetes com a màxim.','Puede haber 100 carpetas como máximo.');return;}target={id:C.uid(),texts:{[ui]:name}};profile().categories.push(target);}
  if(par)target.parent=par;else delete target.parent;
  prefs().enabledCategories=prefs().enabledCategories.filter(x=>x!==target.id);if(visible)prefs().enabledCategories.push(target.id);
  persist();closeDialog();renderWorkspace();notify(f?tr('Carpeta desada.','Carpeta guardada.'):tr('Carpeta creada.','Carpeta creada.'));};
 const actions=[button(tr('Cancel·lar','Cancelar'),closeDialog),button(tr('Desar','Guardar'),save,'primary','save')];
 if(f&&profile().categories.length>1){const destination=f.parent?folderOf(f.parent):profile().categories.find(c=>c.id!==f.id&&!c.parent);if(destination)actions.unshift(button(tr('Eliminar','Eliminar'),()=>confirmDialog(tr('Eliminar carpeta','Eliminar carpeta'),tr('Les frases i les carpetes que conté es mouran a: ','Las frases y las carpetas que contiene se moverán a: ')+folderName(destination.id),()=>{
  profile().phrases.forEach(p=>{if(p.category===f.id)p.category=destination.id;});profile().categories.forEach(c=>{if(c.parent===f.id){if(destination.id===f.parent)c.parent=destination.id;else if(folderDepth(destination.id)+folderHeight(c.id)<=FOLDER_LEVELS)c.parent=destination.id;else delete c.parent;}});
  profile().categories=profile().categories.filter(c=>c.id!==f.id);prefs().enabledCategories=prefs().enabledCategories.filter(x=>x!==f.id);if(phraseFolder===f.id)phraseFolder=f.parent||null;persist();closeDialog();renderWorkspace();notify(tr('Carpeta eliminada.','Carpeta eliminada.'));},()=>editFolder(id)),'danger'));}
 openDialog(f?tr('Editar carpeta','Editar carpeta'):tr('Nova carpeta','Nueva carpeta'),body,actions);activeTarget=input;}
function renderPhraseGrid(){
 const n=$('phrase-grid'),pager=$('phrase-pager');if(!n||!pager)return;
 const browsing=activeView==='phrases'&&!query.trim();let folders=[],list;
 if(browsing){folders=profile().categories.filter(c=>(c.parent||null)===phraseFolder&&(editingList||prefs().enabledCategories.includes(c.id)));list=phraseFolder?profile().phrases.filter(p=>phraseText(p)&&p.category===phraseFolder):[];}
 else list=profile().phrases.filter(p=>phraseText(p)&&folderVisible(p.category)&&(activeView!=='favorites'||p.favorite)&&C.norm(phraseText(p)).includes(C.norm(query)));
 const items=[...folders.map(f=>({f})),...list.map(p=>({p}))];
 const cap=gridCapacity(n),size=prefs().listMode==='scroll'?Math.max(1,items.length):cap.size,count=Math.max(1,Math.ceil(items.length/size));listPage=Math.max(0,Math.min(listPage,count-1));clear(n);
 if(!items.length)n.append(el('p',{class:'empty'},browsing?(phraseFolder?tr('Aquesta carpeta és buida. Afegeix-hi una frase o una carpeta.','Esta carpeta está vacía. Añade una frase o una carpeta.'):tr('No hi ha cap carpeta visible. Crea’n una amb «Nova carpeta».','No hay ninguna carpeta visible. Crea una con «Nueva carpeta».')):tr('No hi ha frases aquí. Afegeix-ne una o canvia el filtre.','No hay frases aquí. Añade una o cambia el filtro.')));
 items.slice(listPage*size,(listPage+1)*size).forEach((it,i)=>{const card=el('div',{class:'phrase-card'+(it.f?' folder-card':''),'data-scan-group':'phrase-'+i});
  if(it.f){const f=it.f,hidden=!prefs().enabledCategories.includes(f.id),name=categoryLabel(f),total=folderCount(f.id);const b=button(name,()=>openFolder(f.id),'phrase-text folder-text','folder');b.append(el('small',{class:'folder-count'},String(total)));b.dataset.focusKey='folder:'+f.id;b.title=name;b.setAttribute('aria-label',tr('Carpeta: ','Carpeta: ')+name+' · '+total+(hidden?' · '+tr('amagada','oculta'):''));if(hidden)card.classList.add('folder-hidden');card.append(b);
   if(editingList){const e=button('✎',()=>editFolder(f.id),'phrase-edit');e.setAttribute('aria-label',tr('Editar carpeta: ','Editar carpeta: ')+name);e.dataset.focusKey='folder-edit:'+f.id;card.append(e);}n.append(card);return;}
  const p=it.p;const text=phraseText(p),b=button(text,()=>{if(editingList)return editPhrase(p.id);if(prefs().phraseAction==='speak')speakText(text,prefs().lang,true);else if(prefs().phraseAction==='show')showMessage(text);else insertPhrase(text);},'phrase-text');b.dataset.focusKey='phrase:'+p.id;b.title=text;card.append(b);const edit=button(editingList?'✎':p.favorite?'★':'☆',()=>editingList?editPhrase(p.id):toggleFavorite(p),'phrase-edit');edit.setAttribute('aria-label',editingList?tr('Editar: ','Editar: ')+text:(p.favorite?tr('Treure de favorits: ','Quitar de favoritos: '):tr('Afegir a favorits: ','Añadir a favoritos: '))+text);edit.dataset.focusKey='favorite:'+p.id;card.append(edit);n.append(card);});
 drawPager(pager,listPage,count,items.length,page=>{listPage=page;renderPhraseGrid();resetAccess();});
}
"""
i=s.index("function renderPhraseGrid(){"); j=s.index("function toggleFavorite(p){",i)
old=s[i:j]; assert 'drawPager(pager,listPage,count,list.length' in old
s=s[:i]+FOLDERS+s[j:]

# Phrase editor: folder instead of category, new phrases go to the open folder
rep("function editPhrase(id=null,initial='',lang=prefs().lang){const p=profile().phrases.find(p=>p.id===id);const original=p?clone(p):{id:C.uid(),texts:{},category:profile().categories[0].id,favorite:false};",
    "function editPhrase(id=null,initial='',lang=prefs().lang,folder=null){const p=profile().phrases.find(p=>p.id===id);const original=p?clone(p):{id:C.uid(),texts:{},category:(folderOf(folder)?folder:(profile().categories.find(c=>!c.parent&&prefs().enabledCategories.includes(c.id))||profile().categories[0]).id),favorite:false};")
rep("const cat=selectControl(profile().categories.map(c=>[c.id,categoryLabel(c)]),category,v=>category=v);","const cat=selectControl(folderOptions(),category,v=>category=v);")
rep("field(tr('Categoria','Categoría'),cat),check(tr('Favorita','Favorita')","field(tr('Carpeta','Carpeta'),cat),check(tr('Favorita','Favorita')")
# Icons
rep("function icon(name){","PATHS.folder='M3 6h6l2 2h10v11H3z';PATHS.folderUp='M15 18l-6-6 6-6';PATHS.folderNew='M3 6h6l2 2h10v11H3zM12 11v5M9.5 13.5h5';\nfunction icon(name){")

CSS="""
/* 0.6.9: phrase folders */
.folder-bar{display:flex;align-items:center;gap:4px;flex-shrink:0;min-height:34px;overflow:hidden}
.folder-bar button{min-height:32px;font-size:12px;padding:5px 9px;white-space:nowrap}
.folder-bar .crumb{color:var(--primary)}.folder-bar .crumb-sep{color:var(--muted)}
.folder-bar .crumb-current{font-size:13px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;min-width:0}
.folder-card{background:var(--subtle)}
.folder-card .folder-text{font-weight:700;color:var(--primary);gap:8px}
.folder-card .folder-text>span{flex:1}
.folder-card .folder-count{margin-left:auto;font-weight:600;font-size:12px;color:var(--muted);padding-left:6px}
.folder-card.folder-hidden{opacity:.6;border-style:dashed}
@media(max-width:600px){.library-controls.with-folders input[type=search]{grid-column:span 6}.library-controls.with-folders button{grid-column:span 2}.folder-bar .crumb-current{max-width:40vw}}
/* 0.6.9: panel cards as a scrolling list */
html.list-scroll .phrase-grid,html.list-scroll .quick-grid,html.list-scroll .history-grid{grid-template-rows:none!important;grid-auto-rows:minmax(calc(58px * var(--control-scale,1)),auto);overflow-y:auto;align-content:start;overscroll-behavior:contain}
html.list-scroll #docs-grid{grid-auto-rows:40px}
html.list-scroll #phrase-pager,html.list-scroll #history-pager,html.list-scroll #docs-pager,html.list-scroll #quick-pager{display:none!important}
/* 0.6.9: 3 x 6 grid in the button editor */
.ae-grid.ae-side{width:min(100%,330px)}
"""
i=s.rindex('</style>'); s=s[:i]+CSS+s[i:]

# ---------- Help texts ----------
rep("tr('Les frases s’insereixen al text. L’estrella les marca com a favorites. A «Editar frases» pots canviar-ne el text, la categoria i l’ordre o eliminar-les.'",
    "tr('A Frases, primer es veuen les carpetes; obre’n una per veure’n les frases. Les frases s’insereixen al text. L’estrella les marca com a favorites. Amb «Editar» pots canviar el text, la carpeta i l’ordre de les frases i de les carpetes, o eliminar-les. «Nova carpeta» crea carpetes fins a tres nivells.'")

# ---------- Translations ----------
T={
"Fitxes dels panells":["Panelen fitxak","Fichas dos paneis","Panel cards","Fiches des panneaux"],
"Pàgines fixes, sense desplaçament":["Orri finkoak, korritu gabe","Páxinas fixas, sen desprazamento","Fixed pages, no scrolling","Pages fixes, sans défilement"],
"Llista amb desplaçament (scroll)":["Korritzen den zerrenda (scroll)","Lista con desprazamento (scroll)","Scrolling list","Liste avec défilement (scroll)"],
"Respostes, frases, historial i documents: pàgines amb Anterior i Següent, o una sola llista que es desplaça.":["Erantzunak, esaldiak, historia eta dokumentuak: Aurrekoa eta Hurrengoa dituzten orriak, edo korritzen den zerrenda bakarra.","Respostas, frases, historial e documentos: páxinas con Anterior e Seguinte, ou unha soa lista que se despraza.","Replies, phrases, history and documents: pages with Previous and Next, or a single list that scrolls.","Réponses, phrases, historique et documents : des pages avec Précédent et Suivant, ou une seule liste qui défile."],
"Nova carpeta":["Karpeta berria","Novo cartafol","New folder","Nouveau dossier"],
"Editar carpeta":["Editatu karpeta","Editar cartafol","Edit folder","Modifier le dossier"],
"Editar carpeta: ":["Editatu karpeta: ","Editar cartafol: ","Edit folder: ","Modifier le dossier : "],
"Carpeta actual":["Uneko karpeta","Cartafol actual","Current folder","Dossier actuel"],
"Amunt":["Gora","Arriba","Up","Haut"],
"Tornar a la carpeta superior":["Itzuli goiko karpetara","Volver ao cartafol superior","Back to the parent folder","Revenir au dossier parent"],
"Frases":["Esaldiak","Frases","Phrases","Phrases"],
"Nom de la carpeta":["Karpetaren izena","Nome do cartafol","Folder name","Nom du dossier"],
"Dins de":["Honen barruan","Dentro de","Inside","Dans"],
"Nivell superior":["Goiko maila","Nivel superior","Top level","Niveau supérieur"],
"Fins a tres nivells de carpetes.":["Gehienez hiru karpeta-maila.","Ata tres niveis de cartafoles.","Up to three folder levels.","Jusqu’à trois niveaux de dossiers."],
"Visible al panell":["Panelean ikusgai","Visible no panel","Visible in the panel","Visible dans le panneau"],
"Carpeta moguda.":["Karpeta mugitu da.","Cartafol movido.","Folder moved.","Dossier déplacé."],
"Escriu un nom.":["Idatzi izen bat.","Escribe un nome.","Type a name.","Saisissez un nom."],
"Hi pot haver tres nivells de carpetes com a màxim.":["Gehienez hiru karpeta-maila egon daitezke.","Pode haber tres niveis de cartafoles como máximo.","There can be at most three folder levels.","Il peut y avoir au maximum trois niveaux de dossiers."],
"Hi pot haver 100 carpetes com a màxim.":["Gehienez 100 karpeta egon daitezke.","Pode haber 100 cartafoles como máximo.","There can be at most 100 folders.","Il peut y avoir au maximum 100 dossiers."],
"Carpeta desada.":["Karpeta gorde da.","Cartafol gardado.","Folder saved.","Dossier enregistré."],
"Carpeta creada.":["Karpeta sortu da.","Cartafol creado.","Folder created.","Dossier créé."],
"Eliminar carpeta":["Ezabatu karpeta","Eliminar cartafol","Delete folder","Supprimer le dossier"],
"Les frases i les carpetes que conté es mouran a: ":["Barruan dituen esaldiak eta karpetak hona mugituko dira: ","As frases e os cartafoles que contén moveranse a: ","The phrases and folders it contains will move to: ","Les phrases et les dossiers qu’il contient seront déplacés vers : "],
"Carpeta eliminada.":["Karpeta ezabatu da.","Cartafol eliminado.","Folder deleted.","Dossier supprimé."],
"Aquesta carpeta és buida. Afegeix-hi una frase o una carpeta.":["Karpeta hau hutsik dago. Gehitu esaldi bat edo karpeta bat.","Este cartafol está baleiro. Engade unha frase ou un cartafol.","This folder is empty. Add a phrase or a folder.","Ce dossier est vide. Ajoutez une phrase ou un dossier."],
"No hi ha cap carpeta visible. Crea’n una amb «Nova carpeta».":["Ez dago karpeta ikusgairik. Sortu bat «Karpeta berria» botoiarekin.","Non hai ningún cartafol visible. Crea un con «Novo cartafol».","There are no visible folders. Create one with “New folder”.","Aucun dossier visible. Créez-en un avec « Nouveau dossier »."],
"Carpeta: ":["Karpeta: ","Cartafol: ","Folder: ","Dossier : "],
"amagada":["ezkutatua","oculto","hidden","masqué"],
"Carpeta":["Karpeta","Cartafol","Folder","Dossier"],
"Desar frase":["Gorde esaldia","Gardar frase","Save phrase","Enregistrer la phrase"],
"Més eines":["Tresna gehiago","Máis ferramentas","More tools","Plus d’outils"],
"A Frases, primer es veuen les carpetes; obre’n una per veure’n les frases. Les frases s’insereixen al text. L’estrella les marca com a favorites. Amb «Editar» pots canviar el text, la carpeta i l’ordre de les frases i de les carpetes, o eliminar-les. «Nova carpeta» crea carpetes fins a tres nivells.":[
 "Esaldiak atalean, lehenik karpetak ikusten dira; ireki bat bere esaldiak ikusteko. Esaldiak testuan txertatzen dira. Izarrak gogoko gisa markatzen ditu. «Editatu» botoiarekin esaldien eta karpeten testua, karpeta eta ordena alda ditzakezu, edo ezabatu. «Karpeta berria» botoiak hiru mailara arteko karpetak sortzen ditu.",
 "En Frases vense primeiro os cartafoles; abre un para ver as súas frases. As frases insírense no texto. A estrela márcaas como favoritas. Con «Editar» podes cambiar o texto, o cartafol e a orde das frases e dos cartafoles, ou eliminalos. «Novo cartafol» crea cartafoles ata tres niveis.",
 "In Phrases you first see the folders; open one to see its phrases. Phrases are inserted into the text. The star marks them as favourites. With “Edit” you can change the text, folder and order of phrases and folders, or delete them. “New folder” creates folders up to three levels deep.",
 "Dans Phrases, on voit d’abord les dossiers ; ouvrez-en un pour voir ses phrases. Les phrases s’insèrent dans le texte. L’étoile les marque comme favorites. Avec « Modifier », vous pouvez changer le texte, le dossier et l’ordre des phrases et des dossiers, ou les supprimer. « Nouveau dossier » crée des dossiers jusqu’à trois niveaux."],
}
LANGS=['eu','gl','en','fr']
i=s.index('const KeryxI18n=(()=>{const dictionaries=')+len('const KeryxI18n=(()=>{const dictionaries=')
for li,lang in enumerate(LANGS):
    key='"'+lang+'":{'
    k=s.index(key,i)+len(key)
    add=''.join(json.dumps(ca,ensure_ascii=False)+':'+json.dumps(v[li],ensure_ascii=False)+',' for ca,v in T.items())
    s=s[:k]+add+s[k:]
for bad in ["tr('Categories','Categorías'),manageCategories","id='phrase-category'"]:
    assert bad not in s, bad
open(dst,'w',encoding='utf-8',newline='').write(s)
print('ok',dst)
