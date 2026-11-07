# Applies the UTAC Keryx 0.6.6 changes to the built UTAC_Keryx_v0.6.5_local.html (Marc, 7 November 2026):
#  - the buttons editor no longer requires Speak to be the largest button;
#  - the main buttons show only their icon (the label stays as the accessible name and tooltip);
#  - Undo and Redo join the main buttons (and the editor) and leave the tools row under the message;
#  - new Documents tab: a simple manager of longer plain-text documents to prepare and say later.
# Usage: python3 patch066.py UTAC_Keryx_v0.6.5_local.html UTAC_Keryx_v0.6.6_local.html
# GPL-3.0-or-later.
import sys, re, json
src,dst=sys.argv[1],sys.argv[2]
s=open(src,encoding='utf-8',newline='').read()
def rep(a,b,count=1):
    global s
    n=s.count(a); assert n==count,(a[:70],n); s=s.replace(a,b)
def repall(a,b):
    global s
    assert s.count(a)>=1,a[:70]; s=s.replace(a,b)
J=lambda x:json.dumps(x,ensure_ascii=False)
s=re.sub(r'(?<!/\* )0\.6\.5(?!:)','0.6.6',s)

# ---------- 1. Speak no longer has to be the largest button
rep(" const area=k=>L[k][2]*L[k][3];for(const k of shown)if(k!=='speak'&&area(k)>=area('speak'))return tr('Parlar ha de ser més gran que la resta de botons.','Hablar debe ser más grande que el resto de botones.');\n","")
repall(' Parlar sempre és visible i sempre és el botó més gran.',' Parlar sempre és visible.')
repall(' Hablar siempre es visible y siempre es el botón más grande.',' Hablar siempre es visible.')
repall(' Hitz egin beti dago ikusgai eta beti da botoirik handiena.',' Hitz egin beti dago ikusgai.')
repall(' Falar sempre está visible e sempre é o botón máis grande.',' Falar sempre está visible.')
repall(' Speak is always shown and is always the largest button.',' Speak is always shown.')
repall(' Parler est toujours visible et toujours le plus grand bouton.',' Parler est toujours visible.')
DESC_OLD='Parlar, Aturar, Mostrar, Esborrar paraula, Esborrar-ho tot i Nou missatge. Parlar sempre és el botó més gran.'
DESC_NEW='Parlar, Aturar, Mostrar, Esborrar paraula, Esborrar-ho tot, Desfer, Refer i Nou missatge.'
for old,new in [("Hitz egin, Gelditu, Erakutsi, Hitza ezabatu, Dena ezabatu eta Mezu berria. Hitz egin botoia beti da handiena.","Hitz egin, Gelditu, Erakutsi, Hitza ezabatu, Dena ezabatu, Desegin, Berregin eta Mezu berria."),
                ("Falar, Deter, Mostrar, Borrar palabra, Borralo todo e Nova mensaxe. Falar sempre é o botón máis grande.","Falar, Deter, Mostrar, Borrar palabra, Borralo todo, Desfacer, Refacer e Nova mensaxe."),
                ("Speak, Stop, Show, Delete word, Clear all and New message. Speak is always the largest button.","Speak, Stop, Show, Delete word, Clear all, Undo, Redo and New message."),
                ("Parler, Arrêter, Afficher, Effacer le mot, Tout effacer et Nouveau message. Parler est toujours le plus grand bouton.","Parler, Arrêter, Afficher, Effacer le mot, Tout effacer, Annuler, Rétablir et Nouveau message."),
                ("Hablar, Detener, Mostrar, Borrar palabra, Borrarlo todo y Nuevo mensaje. Hablar siempre es el botón más grande.","Hablar, Detener, Mostrar, Borrar palabra, Borrarlo todo, Deshacer, Rehacer y Nuevo mensaje.")]:
    rep(old,new)
repall(DESC_OLD,DESC_NEW)

# ---------- 2. Undo and Redo among the main buttons; side grid 2 × 6
repall('· 2 × 5','· 2 × 6')
rep("const ACTION_GRID={side:{cols:2,rows:5},bottom:{cols:12,rows:2}};","const ACTION_GRID={side:{cols:2,rows:6},bottom:{cols:12,rows:2}};")
rep("['clear','clear-all','trash'],['new','new-message','new']];","['clear','clear-all','trash'],['undo','undo','undo'],['redo','redo','redo'],['new','new-message','new']];")
rep("const ACTION_DEFAULTS={side:{speak:[0,0,2,2,1],stop:[0,2,1,1,1],show:[1,2,1,1,1],word:[0,3,1,1,1],clear:[1,3,1,1,1],new:[0,4,2,1,1]},bottom:{speak:[0,0,4,1,1],stop:[4,0,2,1,1],show:[6,0,2,1,1],word:[8,0,1,1,1],clear:[9,0,1,1,1],new:[10,0,2,1,1]}};",
    "const ACTION_DEFAULTS={side:{speak:[0,0,2,2,1],stop:[0,2,1,1,1],show:[1,2,1,1,1],word:[0,3,1,1,1],clear:[1,3,1,1,1],undo:[0,4,1,1,1],redo:[1,4,1,1,1],new:[0,5,2,1,1]},bottom:{speak:[0,0,4,1,1],stop:[4,0,1,1,1],show:[5,0,1,1,1],word:[6,0,1,1,1],clear:[7,0,1,1,1],undo:[8,0,1,1,1],redo:[9,0,1,1,1],new:[10,0,2,1,1]}};")
rep("clear:tr('Esborrar-ho tot','Borrarlo todo'),new:tr('Nou missatge','Nuevo mensaje')}[k];}",
    "clear:tr('Esborrar-ho tot','Borrarlo todo'),undo:tr('Desfer','Deshacer'),redo:tr('Refer','Rehacer'),new:tr('Nou missatge','Nuevo mensaje')}[k];}")
# Settings check: layouts saved before 0.6.6 have no Undo/Redo, so they start hidden there.
rep("const grids={side:[2,5],bottom:[12,2]};","const grids={side:[2,6],bottom:[12,2]};")
rep("for(const id of ['speak','stop','show','word','clear','new']){const v=L[id];",
    "for(const id of ['speak','stop','show','word','clear','undo','redo','new']){const v=L[id];if(v===undefined&&(id==='undo'||id==='redo')){o[id]=[0,0,1,1,0];continue;}")
# The built-in arrangement is now the default grid, so the editor and the screen always match.
rep("const n=$('composer-actions');if(!n)return;const kind=actionLayoutKind(),L=prefs().actionLayouts?.[kind];",
    "const n=$('composer-actions');if(!n)return;const kind=actionLayoutKind(),L=prefs().actionLayouts?.[kind]||(kind==='bottom'&&(n.clientWidth||innerWidth)<700?ACTION_NARROW_BOTTOM:ACTION_DEFAULTS[kind]);")
# On narrow screens the default bottom arrangement uses two rows, so every button stays easy to touch.
rep("function actionLayoutKind(){","const ACTION_NARROW_BOTTOM={speak:[0,0,6,1,1],stop:[6,0,3,1,1],show:[9,0,3,1,1],word:[0,1,2,1,1],clear:[2,1,2,1,1],undo:[4,1,2,1,1],redo:[6,1,2,1,1],new:[8,1,4,1,1]};\nfunction actionLayoutKind(){")
rep(" add(tr('Desfer','Deshacer'),()=>undo(false),'undo','undo');add(tr('Refer','Rehacer'),()=>undo(true),'redo','redo');\n","")
rep("n.append(speak,stop,show,word,wipe,fresh);applyActionLayout();",
    "const back=button(tr('Desfer','Deshacer'),()=>undo(false),'edit-history','undo');back.id='undo';back.dataset.edit='true';const again=button(tr('Refer','Rehacer'),()=>undo(true),'edit-history','redo');again.id='redo';again.dataset.edit='true';"
    "for(const b of [speak,stop,show,word,wipe,back,again,fresh]){const name=b.querySelector('span:not(.icon)')?.textContent||'';b.title=name;b.setAttribute('aria-label',name);}"
    "n.append(speak,stop,show,word,wipe,back,again,fresh);applyActionLayout();")

# ---------- 3. Documents tab
rep("['history','Historial','Historial','history']]){","['history','Historial','Historial','history'],['documents','Documents','Documentos','document']]){")
rep(" if(activeView==='history'){renderHistory(n);return;}"," if(activeView==='history'){renderHistory(n);return;}\n if(activeView==='documents'){renderDocuments(n);return;}")
DOCS=r"""
/* 0.6.6: Documents. Longer plain-text documents the person prepares in advance and says when they want.
   They are kept in this browser, per profile, apart from the copies of settings; each one can be exported as .txt. */
const DOCS_KEY='utac.keryx.documents.v1',DOCS_MAX=200,DOC_MAX_CHARS=200000;
let docsStore=null,openDocId=null,docsPage=0;
function docsAll(){if(!docsStore){try{const raw=JSON.parse(localStorage.getItem(DOCS_KEY)||'{}');docsStore=raw&&typeof raw==='object'&&!Array.isArray(raw)?raw:{};}catch{docsStore={};}}const id=profile().id;if(!Array.isArray(docsStore[id]))docsStore[id]=[];docsStore[id]=docsStore[id].filter(d=>d&&typeof d.id==='string'&&typeof d.text==='string');return docsStore[id];}
function docsSave(){try{localStorage.setItem(DOCS_KEY,JSON.stringify(docsStore));return true;}catch{notify(tr('No s’ha pogut desar el document','No se ha podido guardar el documento'));return false;}}
function docName(d){return (d.title||'').trim()||tr('Document sense títol','Documento sin título');}
function docWords(text){const n=(text.match(/[\p{L}\p{N}’'·-]+/gu)||[]).length;return tr('{n} paraules','{n} palabras').replace('{n}',n);}
function docNew(title='',text=''){const list=docsAll();if(list.length>=DOCS_MAX){notify(tr('Ja hi ha 200 documents. Esborra’n algun abans de crear-ne un altre.','Ya hay 200 documentos. Borra alguno antes de crear otro.'));return null;}const d={id:'doc-'+Date.now().toString(36)+Math.random().toString(36).slice(2,7),title:title.slice(0,120),text:text.slice(0,DOC_MAX_CHARS),created:Date.now(),changed:Date.now()};list.unshift(d);docsSave();return d;}
function docOpen(d){openDocId=d?.id||null;renderWorkspace();if(d)requestAnimationFrame(()=>$('doc-text')?.focus());}
function docImport(){const input=el('input',{type:'file',accept:'.txt,text/plain',multiple:'multiple',hidden:true});document.body.append(input);input.addEventListener('change',async()=>{let last=null;for(const f of [...input.files]){if(f.size>2e6){notify(tr('No s’ha pogut obrir aquest fitxer','No se ha podido abrir este archivo'));continue;}try{const text=await f.text();last=docNew(f.name.replace(/\.[^.]+$/,''),text.replace(/\r\n?/g,'\n'))||last;}catch{notify(tr('No s’ha pogut obrir aquest fitxer','No se ha podido abrir este archivo'));}}input.remove();if(last){docsPage=0;docOpen(last);}});input.click();}
function docExport(d){const a=el('a',{href:URL.createObjectURL(new Blob([d.text],{type:'text/plain;charset=utf-8'})),download:docName(d).replace(/[\\/:*?"<>|]+/g,'-').slice(0,80)+'.txt'});document.body.append(a);a.click();setTimeout(()=>{URL.revokeObjectURL(a.href);a.remove();},1000);}
function docDelete(d){confirmDialog(tr('Eliminar','Eliminar'),tr('Vols esborrar «{titol}» d’aquest dispositiu? No es podrà recuperar.','¿Quieres borrar «{titol}» de este dispositivo? No se podrá recuperar.').replace('{titol}',docName(d)),()=>{const list=docsAll();const i=list.findIndex(x=>x.id===d.id);if(i>=0)list.splice(i,1);docsSave();openDocId=null;closeDialog();renderWorkspace();});}
function renderDocuments(n){
 const doc=openDocId&&docsAll().find(d=>d.id===openDocId);
 if(doc){renderDocEditor(n,doc);return;}openDocId=null;
 n.append(el('div',{class:'panel-toolbar','data-scan-group':'documents-actions'},el('p',{},tr('Textos llargs per preparar abans i dir quan vulguis. Es desen en aquest dispositiu.','Textos largos para preparar antes y decir cuando quieras. Se guardan en este dispositivo.')),button(tr('Document nou','Documento nuevo'),()=>{const d=docNew();if(d)docOpen(d);},'flat','new'),button(tr('Importar .txt','Importar .txt'),docImport,'flat','upload')),el('div',{id:'docs-grid',class:'history-grid'}),el('div',{id:'docs-pager',class:'pager','data-scan-group':'documents-pages'}));
 renderDocsPage();requestAnimationFrame(()=>{if($('docs-grid'))renderDocsPage();});
}
function renderDocsPage(){
 const n=$('docs-grid'),pager=$('docs-pager');if(!n)return;const list=docsAll();const size=Math.max(1,Math.min(5,Math.floor((n.clientHeight||200)/70)));n.style.setProperty('--rows',size);const count=Math.max(1,Math.ceil(list.length/size));docsPage=Math.max(0,Math.min(docsPage,count-1));clear(n);
 if(!list.length)n.append(el('p',{class:'empty'},tr('Encara no hi ha cap document desat.','Todavía no hay ningún documento guardado.')));
 list.slice(docsPage*size,(docsPage+1)*size).forEach((d,i)=>{const open=button(docName(d),()=>docOpen(d),'history-text');open.title=docName(d);const say=button(tr('Parlar','Hablar'),()=>speakText(d.text,prefs().lang),'','speak');say.setAttribute('aria-label',tr('Parlar','Hablar')+': '+docName(d));
  n.append(el('div',{class:'history-row','data-scan-group':'document-'+i},el('small',{},new Date(d.changed).toLocaleDateString(prefs().ui,{day:'numeric',month:'short'})+' · '+docWords(d.text)),open,say));});
 drawPager(pager,docsPage,count,list.length,page=>{docsPage=page;renderDocsPage();resetAccess();});
}
function renderDocEditor(n,d){
 const title=el('input',{type:'text',id:'doc-title',maxlength:'120',placeholder:tr('Document sense títol','Documento sin título'),'aria-label':tr('Títol del document','Título del documento')});title.value=d.title;
 const area=el('textarea',{id:'doc-text',class:'doc-text',spellcheck:'true','aria-label':tr('Text del document','Texto del documento')});area.value=d.text;area.lang=prefs().lang;
 const words=el('small',{class:'doc-words'},docWords(d.text));
 let timer=0;const save=()=>{clearTimeout(timer);d.title=title.value.slice(0,120);d.text=area.value.slice(0,DOC_MAX_CHARS);d.changed=Date.now();words.textContent=docWords(d.text);docsSave();};
 const later=()=>{clearTimeout(timer);timer=setTimeout(save,400);};title.addEventListener('input',later);area.addEventListener('input',later);title.addEventListener('change',save);area.addEventListener('blur',save);
 const part=()=>{const a=area.selectionStart,b=area.selectionEnd;return a!==b?area.value.slice(a,b):area.value;};
 const back=button(tr('Tornar','Volver'),()=>{save();openDocId=null;renderWorkspace();},'flat','down');back.classList.add('doc-back');
 const say=button(tr('Parlar','Hablar'),()=>{save();speakText(part(),prefs().lang);},'primary','speak');say.title=tr('Llegeix la selecció o tot el document','Lee la selección o todo el documento');
 const show=button(tr('Mostrar','Mostrar'),()=>{save();showMessage(part());},'','show');
 const toMessage=button(tr('Al missatge','Al mensaje'),()=>{save();insertPhrase(part());},'','new');toMessage.title=tr('Copia el text, o la part seleccionada, al missatge','Copia el texto, o la parte seleccionada, al mensaje');
 const exp=button(tr('Exportar .txt','Exportar .txt'),()=>{save();docExport(d);},'','download');
 const del=button(tr('Eliminar','Eliminar'),()=>{save();docDelete(d);},'danger-text','trash');
 n.append(el('div',{class:'doc-editor'},el('div',{class:'doc-head','data-scan-group':'document-head'},back,title,words),area,el('div',{class:'doc-actions','data-scan-group':'document-actions'},say,show,toMessage,exp,del)));
}
"""
rep("function renderHistory(n){",DOCS.strip()+"\naddEventListener('resize',()=>{if(!prefs().actionLayouts?.[actionLayoutKind()])requestAnimationFrame(applyActionLayout);});\nfunction renderHistory(n){")
# Icon for importing
rep("const PATHS={globe:","const PATHS={document:'M6 2h9l5 5v15H6V2Zm9 0v5h5M9 12h8M9 16h8M9 8h3',upload:'M12 16V4m-5 5 5-5 5 5M4 16v5h16v-5',globe:")
# A different profile shows its own documents.
T={
 'Textos llargs per preparar abans i dir quan vulguis. Es desen en aquest dispositiu.':['Aldez aurretik prestatzeko eta nahi duzunean esateko testu luzeak. Gailu honetan gordetzen dira.','Textos longos para preparar antes e dicir cando queiras. Gárdanse neste dispositivo.','Longer texts to prepare in advance and say whenever you want. They are saved on this device.','Des textes longs à préparer à l’avance et à dire quand vous voulez. Ils sont enregistrés sur cet appareil.'],
 'Importar .txt':['Inportatu .txt','Importar .txt','Import .txt','Importer .txt'],
 'Exportar .txt':['Esportatu .txt','Exportar .txt','Export .txt','Exporter .txt'],
 'Al missatge':['Mezura','Á mensaxe','To message','Vers le message'],
 'Text del document':['Dokumentuaren testua','Texto do documento','Document text','Texte du document'],
 '{n} paraules':['{n} hitz','{n} palabras','{n} words','{n} mots'],
 'Ja hi ha 200 documents. Esborra’n algun abans de crear-ne un altre.':['Dagoeneko 200 dokumentu daude. Ezabatu bat beste bat sortu aurretik.','Xa hai 200 documentos. Borra algún antes de crear outro.','There are already 200 documents. Delete one before creating another.','Il y a déjà 200 documents. Supprimez-en un avant d’en créer un autre.'],
 'Llegeix la selecció o tot el document':['Hautapena edo dokumentu osoa irakurtzen du','Le a selección ou todo o documento','Reads the selection or the whole document','Lit la sélection ou tout le document'],
 'Copia el text, o la part seleccionada, al missatge':['Testua, edo hautatutako zatia, mezura kopiatzen du','Copia o texto, ou a parte seleccionada, á mensaxe','Copies the text, or the selected part, to the message','Copie le texte, ou la partie sélectionnée, dans le message'],
 'Document nou':None,'Documents':None,'Títol del document':None,'Document sense títol':None,'Encara no hi ha cap document desat.':None,'Eliminar':None,'Tornar':None,
}
for i,lang in enumerate(['eu','gl','en','fr']):
    ins=''.join(J(k)+':'+J(v[i])+',' for k,v in T.items() if v)
    rep('"%s":{"'%lang,'"%s":{'%lang+ins+'"')

CSS="""
/* 0.6.6: main buttons show only their icon; the label stays as the accessible name and tooltip. */
.composer-actions button>span:not(.icon){position:absolute!important;width:1px!important;height:1px!important;overflow:hidden!important;clip-path:inset(50%)!important;white-space:nowrap!important}
#composer-actions.composer-actions button kbd{display:none!important}
.tabs{grid-template-columns:repeat(6,minmax(0,1fr))!important}
.tabs button{min-width:0}.tabs button span{min-width:0;overflow:hidden;text-overflow:ellipsis}
#composer-actions.composer-actions button .icon{display:inline-block!important;width:clamp(20px,46cqmin,30px);height:clamp(20px,46cqmin,30px)}
#composer-actions.composer-actions .speak .icon{width:clamp(24px,40cqmin,44px);height:clamp(24px,40cqmin,44px)}
.composer-actions button{gap:0}
/* 0.6.6: Documents tab */
.doc-editor{display:grid;grid-template-rows:auto minmax(0,1fr) auto;gap:8px;height:100%;min-height:0}
.doc-head{display:flex;align-items:center;gap:8px;min-width:0}
.doc-head input{flex:1;min-width:0;min-height:40px;font:inherit;font-weight:700;padding:6px 10px;border:1px solid var(--border);border-radius:10px;background:var(--surface);color:var(--text)}
.doc-back .icon{transform:rotate(90deg)}
.doc-words{color:var(--muted);white-space:nowrap}
.doc-text{width:100%;height:100%;min-height:0;resize:none;font:inherit;font-size:18px;line-height:1.5;padding:10px 12px;border:1px solid var(--border);border-radius:10px;background:var(--surface);color:var(--text);overflow:auto}
.doc-actions{display:flex;flex-wrap:wrap;gap:8px}
.doc-actions button{min-height:40px}
@media(max-width:600px),(max-height:500px){.doc-actions button>span:not(.icon){position:absolute;width:1px;height:1px;overflow:hidden;clip-path:inset(50%)}.doc-actions button{min-width:44px;justify-content:center}.doc-text{font-size:16px}}
"""
i=s.rindex('</style>'); s=s[:i]+CSS+s[i:]
open(dst,'w',encoding='utf-8',newline='').write(s)
print('ok',dst)
