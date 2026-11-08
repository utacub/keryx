# Applies the UTAC Keryx 0.6.12 change to the built UTAC_Keryx_v0.6.11_local.html (Marc, 2026-11-08):
# the Documents tab gets the same folder navigation as Phrases: folders up to three levels, Up button,
# breadcrumb, New folder / New document / Import, and the same Edit mode (tap an item to rename, move or delete it).
# Document folders are kept per profile in localStorage 'utac.keryx.docfolders.v1'; each document may carry `folder`.
# Usage: python3 patch0612.py UTAC_Keryx_v0.6.11_local.html UTAC_Keryx_v0.6.12_local.html
import sys, re, json
src,dst=sys.argv[1],sys.argv[2]
s=open(src,encoding='utf-8',newline='').read()
def rep(a,b,count=1):
    global s
    n=s.count(a); assert n==count,(a[:90],n); s=s.replace(a,b)
s=re.sub(r'(?<!/\* )0\.6\.11(?![:\d])','0.6.12',s)

# Store and helpers
rep("let docsStore=null,openDocId=null,docsPage=0;",
"""let docsStore=null,openDocId=null,docsPage=0,docFolder=null,docFolderStore=null;
/* 0.6.12: document folders, like the phrase folders (up to three levels), kept per profile. */
const DOCF_KEY='utac.keryx.docfolders.v1';
function dfAll(){if(!docFolderStore){try{const raw=JSON.parse(localStorage.getItem(DOCF_KEY)||'{}');docFolderStore=raw&&typeof raw==='object'&&!Array.isArray(raw)?raw:{};}catch{docFolderStore={};}}const id=profile().id;let list=Array.isArray(docFolderStore[id])?docFolderStore[id].filter(f=>f&&typeof f.id==='string'&&typeof f.name==='string'):[];
 const ids=new Set(list.map(f=>f.id));for(const f of list){if(f.parent&&!ids.has(f.parent))delete f.parent;}for(const f of list){let d=1,c=f,seen=new Set([f.id]);while(c.parent){c=list.find(x=>x.id===c.parent);if(!c||seen.has(c.id)||++d>FOLDER_LEVELS){delete f.parent;break;}seen.add(c.id);}}docFolderStore[id]=list;return list;}
function dfSave(){try{localStorage.setItem(DOCF_KEY,JSON.stringify(docFolderStore));return true;}catch{notify(tr('No s’ha pogut desar el document','No se ha podido guardar el documento'));return false;}}
function dfOf(id){return id?dfAll().find(f=>f.id===id):null;}
function dfPath(id){const out=[];let c=dfOf(id);while(c&&out.length<10){out.unshift(c);c=dfOf(c.parent);}return out;}
function dfDepth(id){return dfPath(id).length;}
function dfSubtree(id){const out=new Set([id]);let grew=true;while(grew){grew=false;for(const c of dfAll())if(c.parent&&out.has(c.parent)&&!out.has(c.id)){out.add(c.id);grew=true;}}return out;}
function dfHeight(id){const kids=dfAll().filter(c=>c.parent===id);return 1+(kids.length?Math.max(...kids.map(k=>dfHeight(k.id))):0);}
function dfName(id){return dfPath(id).map(f=>f.name).join(' › ');}
function dfCount(id){const ids=dfSubtree(id);return docsAll().filter(d=>ids.has(d.folder)).length;}
function dfOptions(){const out=[];const walk=pid=>{for(const c of dfAll().filter(c=>(c.parent||null)===pid)){out.push([c.id,dfName(c.id)]);walk(c.id);}};walk(null);return out;}
function docFolderOf(d){return d.folder&&dfOf(d.folder)?d.folder:null;}
function openDocFolder(id){docFolder=id||null;docsPage=0;renderWorkspace();resetAccess();requestAnimationFrame(()=>{if(keyboardInput||prefs().access!=='direct'){const first=$('docs-grid')?.querySelector('button');if(first)focusSafely(first);}});}
function docFolderBar(){const bar=el('nav',{class:'folder-bar','data-scan-group':'document-folder-path','aria-label':tr('Carpeta actual','Carpeta actual')});const path=dfPath(docFolder);
 bar.append(button(tr('Documents','Documentos'),()=>openDocFolder(null),'flat crumb'));
 path.forEach((c,i)=>{bar.append(el('span',{class:'crumb-sep','aria-hidden':'true'},'›'));if(i<path.length-1)bar.append(button(c.name,()=>openDocFolder(c.id),'flat crumb'));else bar.append(el('strong',{class:'crumb-current','aria-current':'location'},c.name));});
 return bar;}
function editDocFolder(id=null,parent=docFolder){
 const f=dfOf(id);const input=el('input',{type:'text',maxlength:100,value:f?f.name:''});const error=el('p',{class:'error-text',role:'alert'});
 let par=f?(f.parent||null):(parent||null);const own=f?dfSubtree(f.id):new Set(),height=f?dfHeight(f.id):1;
 const options=[['',tr('Nivell superior','Nivel superior')],...dfOptions().filter(([cid])=>!own.has(cid)&&dfDepth(cid)+height<=FOLDER_LEVELS)];
 const body=[field(tr('Nom de la carpeta','Nombre de la carpeta'),input),field(tr('Dins de','Dentro de'),selectControl(options,par||'',v=>par=v||null),tr('Fins a tres nivells de carpetes.','Hasta tres niveles de carpetas.')),error];
 if(f){const move=delta=>{const list=dfAll(),sib=list.filter(c=>(c.parent||null)===(f.parent||null)),k=sib.indexOf(f),other=sib[k+delta];if(!other)return;const a=list.indexOf(f),b=list.indexOf(other);[list[a],list[b]]=[list[b],list[a]];dfSave();renderWorkspace();notify(tr('Carpeta moguda.','Carpeta movida.'));};body.push(el('div',{class:'button-row'},button(tr('Moure abans','Mover antes'),()=>move(-1)),button(tr('Moure després','Mover después'),()=>move(1))));}
 const save=()=>{const name=input.value.trim();if(!name){error.textContent=tr('Escriu un nom.','Escribe un nombre.');return;}if(par&&dfDepth(par)+height>FOLDER_LEVELS){error.textContent=tr('Hi pot haver tres nivells de carpetes com a màxim.','Puede haber tres niveles de carpetas como máximo.');return;}
  let target=f;if(f)f.name=name.slice(0,100);else{if(dfAll().length>=100){error.textContent=tr('Hi pot haver 100 carpetes com a màxim.','Puede haber 100 carpetas como máximo.');return;}target={id:'docf-'+Date.now().toString(36)+Math.random().toString(36).slice(2,7),name:name.slice(0,100)};dfAll().push(target);}
  if(par)target.parent=par;else delete target.parent;dfSave();closeDialog();renderWorkspace();notify(f?tr('Carpeta desada.','Carpeta guardada.'):tr('Carpeta creada.','Carpeta creada.'));};
 const actions=[button(tr('Cancel·lar','Cancelar'),closeDialog),button(tr('Desar','Guardar'),save,'primary','save')];
 if(f)actions.unshift(button(tr('Eliminar','Eliminar'),()=>confirmDialog(tr('Eliminar carpeta','Eliminar carpeta'),tr('Els documents i les carpetes que conté es mouran a: ','Los documentos y las carpetas que contiene se moverán a: ')+(f.parent?dfName(f.parent):tr('Documents','Documentos')),()=>{
  const to=f.parent||null;for(const d of docsAll())if(d.folder===f.id){if(to)d.folder=to;else delete d.folder;}for(const c of dfAll())if(c.parent===f.id){if(to)c.parent=to;else delete c.parent;}
  docFolderStore[profile().id]=dfAll().filter(c=>c.id!==f.id);if(docFolder===f.id)docFolder=to;dfSave();docsSave();closeDialog();renderWorkspace();notify(tr('Carpeta eliminada.','Carpeta eliminada.'));},()=>editDocFolder(id)),'danger'));
 openDialog(f?tr('Editar carpeta','Editar carpeta'):tr('Nova carpeta','Nueva carpeta'),body,actions);activeTarget=input;}
function editDocItem(d){
 const input=el('input',{type:'text',maxlength:'120',value:d.title||'',placeholder:tr('Document sense títol','Documento sin título')});let where=docFolderOf(d)||'';
 const options=[['',tr('Nivell superior','Nivel superior')],...dfOptions()];
 const move=delta=>{const list=docsAll(),sib=list.filter(x=>docFolderOf(x)===docFolderOf(d)),k=sib.indexOf(d),other=sib[k+delta];if(!other)return;const a=list.indexOf(d),b=list.indexOf(other);[list[a],list[b]]=[list[b],list[a]];docsSave();renderWorkspace();notify(tr('Document mogut.','Documento movido.'));};
 const body=[field(tr('Títol del document','Título del documento'),input),field(tr('Carpeta','Carpeta'),selectControl(options,where,v=>where=v)),el('div',{class:'button-row'},button(tr('Moure abans','Mover antes'),()=>move(-1)),button(tr('Moure després','Mover después'),()=>move(1)))];
 const save=()=>{d.title=input.value.slice(0,120);if(where)d.folder=where;else delete d.folder;d.changed=Date.now();docsSave();closeDialog();renderWorkspace();notify(tr('Document desat.','Documento guardado.'));};
 openDialog(tr('Editar document','Editar documento'),body,[button(tr('Eliminar','Eliminar'),()=>docDelete(d),'danger'),button(tr('Obrir','Abrir'),()=>{closeDialog();docOpen(d);}),button(tr('Cancel·lar','Cancelar'),closeDialog),button(tr('Desar','Guardar'),save,'primary','save')]);activeTarget=input;}""")

# New documents go into the open folder
rep("created:Date.now(),changed:Date.now()};list.unshift(d);docsSave();return d;}",
    "created:Date.now(),changed:Date.now()};if(docFolder&&dfOf(docFolder))d.folder=docFolder;list.unshift(d);docsSave();return d;}")

# Documents list with the Phrases toolbar, edit mode and breadcrumb
rep(""" n.append(el('div',{class:'panel-toolbar','data-scan-group':'documents-actions'},el('p',{},tr('Textos llargs per preparar abans i dir quan vulguis. Es desen en aquest dispositiu.','Textos largos para preparar antes y decir cuando quieras. Se guardan en este dispositivo.')),button(tr('Document nou','Documento nuevo'),()=>{const d=docNew();if(d)docOpen(d);},'flat','new'),button(tr('Importar .txt','Importar .txt'),docImport,'flat','upload')),el('div',{id:'docs-grid',class:'history-grid'}),el('div',{id:'docs-pager',class:'pager','data-scan-group':'documents-pages'}));""",
""" if(docFolder&&!dfOf(docFolder))docFolder=null;
 const kids=dfAll().some(c=>(c.parent||null)===docFolder),here=docsAll().some(d=>docFolderOf(d)===docFolder);
 const controls=el('div',{class:'library-controls with-folders docs-controls','data-scan-group':'documents-actions'});
 if(docFolder){const path=dfPath(docFolder);const up=button(tr('Amunt','Arriba'),()=>openDocFolder(path.length>1?path[path.length-2].id:null),'soft folder-up','folderUp');up.setAttribute('aria-label',tr('Tornar a la carpeta superior','Volver a la carpeta superior'));up.dataset.focusKey='doc-folder-up';controls.append(up);}
 const edit=button(editingList?tr('Acabar edició','Terminar edición'):innerWidth<=600?tr('Editar','Editar'):kids&&here?tr('Editar documents i carpetes','Editar documentos y carpetas'):kids?tr('Editar carpetes','Editar carpetas'):tr('Editar documents','Editar documentos'),()=>{editingList=!editingList;renderWorkspace();},editingList?'primary':'',editingList?'check':'edit');edit.dataset.focusKey='doc-edit';
 const add=button(tr('Document nou','Documento nuevo'),()=>{const d=docNew();if(d)docOpen(d);},'soft','new');add.dataset.focusKey='doc-new';controls.append(edit,add);
 if(dfDepth(docFolder)<FOLDER_LEVELS){const nf=button(tr('Nova carpeta','Nueva carpeta'),()=>editDocFolder(null,docFolder),'soft','folderNew');nf.dataset.focusKey='doc-folder-new';controls.append(nf);}
 const imp=button(tr('Importar .txt','Importar .txt'),docImport,'soft','upload');imp.dataset.focusKey='doc-import';controls.append(imp);n.append(controls);
 if(editingList)n.append(el('p',{class:'notice edit-notice',role:'status'},tr('Mode d’edició: toca un element per canviar-lo, moure’l o eliminar-lo. Prem «Acabar edició» per tornar a fer-los servir.','Modo de edición: toca un elemento para cambiarlo, moverlo o eliminarlo. Pulsa «Terminar edición» para volver a usarlos.')));
 if(docFolder)n.append(docFolderBar());
 n.append(el('div',{id:'docs-grid',class:'history-grid'}),el('div',{id:'docs-pager',class:'pager','data-scan-group':'documents-pages'}));""")

rep(""" const n=$('docs-grid'),pager=$('docs-pager');if(!n)return;const list=docsAll();const size=prefs().panelScroll?Math.max(1,list.length):Math.max(4,Math.min(10,Math.floor(((n.clientHeight||200)+4)/44)));n.style.setProperty('--rows',size);const count=Math.max(1,Math.ceil(list.length/size));docsPage=Math.max(0,Math.min(docsPage,count-1));clear(n);
 if(!list.length)n.append(el('p',{class:'empty'},tr('Encara no hi ha cap document desat.','Todavía no hay ningún documento guardado.')));
 list.slice(docsPage*size,(docsPage+1)*size).forEach((d,i)=>{const open=button(docName(d),()=>docOpen(d),'history-text');open.title=docName(d);const say=button(tr('Parlar','Hablar'),()=>speakText(d.text,prefs().lang),'','speak');say.setAttribute('aria-label',tr('Parlar','Hablar')+': '+docName(d));
  n.append(el('div',{class:'history-row','data-scan-group':'document-'+i},el('small',{},new Date(d.changed).toLocaleDateString(prefs().ui,{day:'numeric',month:'short'})+' · '+docWords(d.text)),open,say));});
 drawPager(pager,docsPage,count,list.length,page=>{docsPage=page;renderDocsPage();resetAccess();});""",
""" const n=$('docs-grid'),pager=$('docs-pager');if(!n)return;const items=[...dfAll().filter(c=>(c.parent||null)===docFolder).map(f=>({f})),...docsAll().filter(d=>docFolderOf(d)===docFolder).map(d=>({d}))];const size=prefs().panelScroll?Math.max(1,items.length):Math.max(4,Math.min(10,Math.floor(((n.clientHeight||200)+4)/44)));n.style.setProperty('--rows',size);const count=Math.max(1,Math.ceil(items.length/size));docsPage=Math.max(0,Math.min(docsPage,count-1));clear(n);
 if(!items.length)n.append(el('p',{class:'empty'},docFolder?tr('Aquesta carpeta és buida. Afegeix-hi un document o una carpeta.','Esta carpeta está vacía. Añade un documento o una carpeta.'):tr('Textos llargs per preparar abans i dir quan vulguis. Es desen en aquest dispositiu.','Textos largos para preparar antes y decir cuando quieras. Se guardan en este dispositivo.')));
 items.slice(docsPage*size,(docsPage+1)*size).forEach((it,i)=>{
  if(it.f){const f=it.f,total=dfCount(f.id);const open=button(f.name,()=>editingList?editDocFolder(f.id):openDocFolder(f.id),'history-text folder-text','folder');open.append(el('span',{class:'folder-count'},String(total)));open.title=f.name;open.dataset.focusKey='doc-folder:'+f.id;open.setAttribute('aria-label',tr('Carpeta: ','Carpeta: ')+f.name+' · '+total);
   const row=el('div',{class:'history-row folder-row','data-scan-group':'document-'+i},open);if(editingList){const e=button(tr('Editar','Editar'),()=>editDocFolder(f.id),'doc-edit-btn','edit');e.setAttribute('aria-label',tr('Editar carpeta: ','Editar carpeta: ')+f.name);e.dataset.focusKey='doc-folder-edit:'+f.id;row.append(e);}n.append(row);return;}
  const d=it.d;const open=button(docName(d),()=>editingList?editDocItem(d):docOpen(d),'history-text');open.title=docName(d);open.dataset.focusKey='doc:'+d.id;
  const say=editingList?button(tr('Editar','Editar'),()=>editDocItem(d),'doc-edit-btn','edit'):button(tr('Parlar','Hablar'),()=>speakText(d.text,prefs().lang),'','speak');say.setAttribute('aria-label',(editingList?tr('Editar: ','Editar: '):tr('Parlar','Hablar')+': ')+docName(d));say.dataset.focusKey='doc-say:'+d.id;
  n.append(el('div',{class:'history-row','data-scan-group':'document-'+i},el('small',{},new Date(d.changed).toLocaleDateString(prefs().ui,{day:'numeric',month:'short'})+' · '+docWords(d.text)),open,say));});
 drawPager(pager,docsPage,count,items.length,page=>{docsPage=page;renderDocsPage();resetAccess();});""")

# The document editor opens in a large window: writing area on the left, actions on the right (Marc, 2026-11-08)
i=s.index("function renderDocEditor(n,d){");k=s.index("\n}\n",i)+3
s=s[:i]+"""function renderDocEditor(d){
 const title=el('input',{type:'text',id:'doc-title',maxlength:'120',placeholder:tr('Document sense títol','Documento sin título'),'aria-label':tr('Títol del document','Título del documento')});title.value=d.title;
 const area=el('textarea',{id:'doc-text',class:'doc-text',spellcheck:'true','aria-label':tr('Text del document','Texto del documento')});area.value=d.text;area.lang=prefs().lang;
 const words=el('small',{class:'doc-words'},docWords(d.text));
 let timer=0;const save=()=>{clearTimeout(timer);if(d.title===title.value.slice(0,120)&&d.text===area.value.slice(0,DOC_MAX_CHARS))return;d.title=title.value.slice(0,120);d.text=area.value.slice(0,DOC_MAX_CHARS);d.changed=Date.now();words.textContent=docWords(d.text);docsSave();};
 const later=()=>{clearTimeout(timer);timer=setTimeout(save,400);words.textContent=docWords(area.value);};title.addEventListener('input',later);area.addEventListener('input',later);title.addEventListener('change',save);area.addEventListener('blur',save);
 const part=()=>{const a=area.selectionStart,b=area.selectionEnd;return a!==b?area.value.slice(a,b):area.value;};
 const say=button(tr('Parlar','Hablar'),()=>{save();speakText(part(),prefs().lang);},'primary','speak');say.title=tr('Llegeix la selecció o tot el document','Lee la selección o todo el documento');
 const stop=button(tr('Aturar','Detener'),()=>speech.stop(),'','stop');
 const show=button(tr('Mostrar','Mostrar'),()=>{save();const text=part();if(!text.trim())return;showMessage(text);dialogClose=()=>requestAnimationFrame(()=>docOpen(d));},'','show');
 const toMessage=button(tr('Al missatge','Al mensaje'),()=>{save();const text=part();if(!text.trim())return;closeDialog();insertPhrase(text);},'','new');toMessage.title=tr('Copia el text, o la part seleccionada, al missatge','Copia el texto, o la parte seleccionada, al mensaje');
 const exp=button(tr('Exportar .txt','Exportar .txt'),()=>{save();docExport(d);},'','download');
 const del=button(tr('Eliminar','Eliminar'),()=>{save();docDelete(d,()=>docOpen(d));},'danger-text','trash');
 const done=button(tr('Tancar','Cerrar'),closeDialog,'soft','check');
 const editor=el('div',{class:'doc-editor doc-window'},el('div',{class:'doc-main'},el('div',{class:'doc-head','data-scan-group':'document-head'},title,words),area),el('div',{class:'doc-actions doc-side','data-scan-group':'document-actions'},say,stop,show,toMessage,exp,del,el('span',{class:'spacer'}),done));
 openDialog(tr('Document','Documento'),[editor],[],'scroll-dialog doc-dialog',()=>{save();renderWorkspace();});
 requestAnimationFrame(()=>{area.focus({preventScroll:true});activeTarget=area;});
}
"""+s[k:]
rep("function docOpen(d){openDocId=d?.id||null;renderWorkspace();if(d)requestAnimationFrame(()=>$('doc-text')?.focus());}",
    "function docOpen(d){openDocId=null;if(d)renderDocEditor(d);}")
rep(" const doc=openDocId&&docsAll().find(d=>d.id===openDocId);\n if(doc){renderDocEditor(n,doc);return;}openDocId=null;\n"," openDocId=null;\n")
rep("function docDelete(d){confirmDialog(","function docDelete(d,back=closeDialog){confirmDialog(")
rep("openDocId=null;closeDialog();renderWorkspace();});}","openDocId=null;closeDialog();renderWorkspace();},back);}")
rep("button(tr('Eliminar','Eliminar'),()=>docDelete(d),'danger')","button(tr('Eliminar','Eliminar'),()=>docDelete(d,()=>editDocItem(d)),'danger')")

# Panel size buttons: magnifier icons, right next to "Amagar panell" (Marc, 2026-11-08)
rep("PATHS.folderUp='M15 18l-6-6 6-6';","PATHS.folderUp='M15 18l-6-6 6-6';PATHS.zoomIn='M17 10.5a6.5 6.5 0 1 1-13 0a6.5 6.5 0 1 1 13 0M15.2 15.2 21 21M7.5 10.5h6M10.5 7.5v6';PATHS.zoomOut='M17 10.5a6.5 6.5 0 1 1-13 0a6.5 6.5 0 1 1 13 0M15.2 15.2 21 21M7.5 10.5h6';")
rep("const mk=(d,label,text,key)=>{const b=button(text,","const mk=(d,label,ic,key)=>{const b=button('',")
rep("},'soft panel-zoom-btn');","},'soft panel-zoom-btn',ic);")
rep("'A−','panel-smaller'","'zoomOut','panel-smaller'")
rep("'A+','panel-bigger'","'zoomIn','panel-bigger'")

# Opening the tab starts at the top level, like Phrases
rep("if(id==='phrases')phraseFolder=null;","if(id==='phrases')phraseFolder=null;if(id==='documents')docFolder=null;")

CSS="""
/* 0.6.12: document folders */
#docs-grid .folder-row{background:var(--subtle)}
#docs-grid .folder-row .history-text{font-weight:700;color:var(--primary);display:flex;align-items:center;gap:8px}
#docs-grid .folder-row .history-text>span:not(.icon):not(.folder-count){flex:1;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
#docs-grid .folder-count{margin-left:auto;font-weight:600;font-size:12px;color:var(--muted);padding-left:6px}
#docs-grid .doc-edit-btn{flex-shrink:0;padding-inline:12px}
@media(max-width:600px){#docs-grid .doc-edit-btn>span:not(.icon){position:absolute;width:1px;height:1px;overflow:hidden;clip-path:inset(50%)}}
#dialog.doc-dialog{width:min(1500px,calc(100vw - 32px));height:calc(var(--app-height) - 32px)}
@media(max-width:600px){#dialog.doc-dialog{width:calc(100vw - 14px);height:calc(var(--app-height) - 14px)}}
#dialog.doc-dialog .dialog-body{overflow:hidden;padding:12px 16px}
#dialog.doc-dialog .dialog-footer,#dialog.doc-dialog .dialog-pagination{display:none}
#dialog.doc-dialog .settings-page{height:100%;justify-content:stretch}
.doc-window{display:grid;grid-template-columns:minmax(0,1fr) minmax(150px,200px);grid-template-rows:minmax(0,1fr);gap:14px;height:100%}
.doc-main{display:grid;grid-template-rows:auto minmax(0,1fr);gap:8px;min-height:0;min-width:0}
.doc-main .doc-head input{flex:1;min-width:0;font-size:18px;font-weight:700}
.doc-window .doc-text{font-size:20px;line-height:1.55}
.doc-side{display:flex;flex-direction:column;flex-wrap:nowrap;gap:8px;min-height:0;overflow-y:auto}
.doc-side button{width:100%;justify-content:flex-start;min-height:48px}
.doc-side .spacer{flex:1}
@media(max-width:600px){.doc-window{grid-template-columns:minmax(0,1fr);grid-template-rows:minmax(0,1fr) auto;gap:8px}.doc-side{flex-direction:row;flex-wrap:wrap;overflow:visible}.doc-side button{width:auto;flex:1 1 30%;min-height:42px;justify-content:center}.doc-side .spacer{display:none}.doc-window .doc-text{font-size:17px}#dialog.doc-dialog .dialog-body{padding:8px}}
.docs-controls{flex-wrap:wrap}.docs-controls button{flex:1 1 auto}.docs-controls .folder-up{flex:0 0 auto}
@media(max-width:600px){.library-controls.docs-controls button{grid-column:span 3}.library-controls.docs-controls button.folder-up{grid-column:span 6}#docs-grid .folder-row .history-text{display:flex}}

/* 0.6.12: zoom buttons beside the panel toggle; folders drawn as folders (tab on top, thicker border), no folder icon */
#workspace-header .panel-zoom{margin-left:auto;margin-right:0}#workspace-header>.panel-toggle{margin-left:8px!important}
.panel-zoom .panel-zoom-btn{min-height:40px;height:40px}
.panel-zoom-btn{display:inline-flex;align-items:center;justify-content:center;padding:4px 8px}
.panel-zoom-btn>span:empty{display:none}
.panel-zoom-btn .icon{width:24px;height:24px}
.folder-card,#docs-grid .folder-row{position:relative;overflow:visible;border:2px solid var(--primary);border-radius:0 11px 11px 11px;margin-top:9px;background:var(--subtle)}
.folder-card::before,#docs-grid .folder-row::before{content:'';position:absolute;left:-2px;top:-10px;width:38%;max-width:120px;min-width:48px;height:12px;background:var(--subtle);border:2px solid var(--primary);border-bottom:0;border-radius:8px 8px 0 0;pointer-events:none}
.folder-card .folder-text>.icon,#docs-grid .folder-row .history-text>.icon{display:none}
.folder-card>button,#docs-grid .folder-row>button{border-radius:0 9px 9px 9px;background:transparent}
.folder-card>button+button,#docs-grid .folder-row>button+button{border-radius:0 9px 9px 0}
#docs-grid .folder-row>button.history-text>span:not(.icon){position:static!important;width:auto!important;height:auto!important;overflow:hidden;clip-path:none!important}
.folder-card.folder-hidden{border-style:dashed}.folder-card.folder-hidden::before{border-style:dashed}
"""
i=s.rindex('</style>'); s=s[:i]+CSS+s[i:]

T={
"Editar documents i carpetes":["Editatu dokumentuak eta karpetak","Editar documentos e cartafoles","Edit documents and folders","Modifier les documents et les dossiers"],
"Editar documents":["Editatu dokumentuak","Editar documentos","Edit documents","Modifier les documents"],
"Editar document":["Editatu dokumentua","Editar documento","Edit document","Modifier le document"],
"Document desat.":["Dokumentua gorde da.","Documento gardado.","Document saved.","Document enregistré."],
"Document mogut.":["Dokumentua mugitu da.","Documento movido.","Document moved.","Document déplacé."],
"Aquesta carpeta és buida. Afegeix-hi un document o una carpeta.":["Karpeta hau hutsik dago. Gehitu dokumentu bat edo karpeta bat.","Este cartafol está baleiro. Engade un documento ou un cartafol.","This folder is empty. Add a document or a folder.","Ce dossier est vide. Ajoutez un document ou un dossier."],
"Els documents i les carpetes que conté es mouran a: ":["Barruko dokumentuak eta karpetak hona mugituko dira: ","Os documentos e os cartafoles que contén moveranse a: ","The documents and folders inside will be moved to: ","Les documents et les dossiers qu’il contient seront déplacés vers : "],
}
i=s.index('const KeryxI18n=(()=>{const dictionaries=')+len('const KeryxI18n=(()=>{const dictionaries=')
for li,lang in enumerate(['eu','gl','en','fr']):
    key='"'+lang+'":{'; k=s.index(key,i)+len(key)
    s=s[:k]+''.join(json.dumps(ca,ensure_ascii=False)+':'+json.dumps(v[li],ensure_ascii=False)+',' for ca,v in T.items())+s[k:]
open(dst,'w',encoding='utf-8',newline='').write(s)
print('ok',dst)
