# Applies the UTAC Keryx 0.6.10 change to the built UTAC_Keryx_v0.6.9_local.html (Marc, 2026-11-08):
# - panel cards scroll by default (new setting key panelScroll, default true; the 0.6.9 listMode is dropped,
#   so every profile starts in scroll once and can go back to fixed pages in Settings -> Access);
# - in a phrase folder, the Up button sits in the toolbar row, as tall as New folder and New phrase;
# - two buttons before "Amagar panell" make everything inside the panel bigger or smaller (70 %-160 %, per profile).
# Usage: python3 patch0610.py UTAC_Keryx_v0.6.9_local.html UTAC_Keryx_v0.6.10_local.html
import sys, re, json
src,dst=sys.argv[1],sys.argv[2]
s=open(src,encoding='utf-8',newline='').read()
def rep(a,b,count=1):
    global s
    n=s.count(a); assert n==count,(a[:90],n); s=s.replace(a,b)
s=re.sub(r'(?<!/\* )0\.6\.9(?![:\d])','0.6.10',s)

# Settings
rep("actionsPosition:'bottom',listMode:'pages',","actionsPosition:'bottom',panelScroll:true,panelScale:1,")
rep("for(const [k,a] of Object.entries({listMode:['pages','scroll'],theme:THEMES.ids,","for(const [k,a] of Object.entries({theme:THEMES.ids,")
rep("for(const k of ['readLetters','readWords','readSentences','uppercase',","for(const k of ['readLetters','readWords','readSentences','panelScroll','uppercase',")
rep("['controlSize',1,1.4]","['controlSize',1,1.4],['panelScale',0.7,1.6]")
rep("p.listMode||'pages',v=>{set('listMode',v);","p.panelScroll?'scroll':'pages',v=>{set('panelScroll',v==='scroll');")
rep("document.documentElement.classList.toggle('list-scroll',prefs().listMode==='scroll');",
    "document.documentElement.classList.toggle('list-scroll',prefs().panelScroll);document.documentElement.style.setProperty('--panel-scale',prefs().panelScale||1);")
s=s.replace("prefs().listMode==='scroll'","prefs().panelScroll")
assert 'listMode' not in s

# Up button in the toolbar row
rep("const up=button(tr('Amunt','Arriba'),()=>openFolder(path.length>1?path[path.length-2].id:null),'soft','folderUp');up.setAttribute('aria-label',tr('Tornar a la carpeta superior','Volver a la carpeta superior'));bar.append(up);","")
rep("n.append(controls);if(activeView==='phrases'&&phraseFolder)n.append(folderBar());",
    "if(activeView==='phrases'&&phraseFolder){const path=folderPath(phraseFolder);const up=button(tr('Amunt','Arriba'),()=>openFolder(path.length>1?path[path.length-2].id:null),'soft folder-up','folderUp');up.setAttribute('aria-label',tr('Tornar a la carpeta superior','Volver a la carpeta superior'));up.dataset.focusKey='folder-up';controls.prepend(up);}n.append(controls);if(editingList)n.append(el('p',{class:'notice edit-notice',role:'status'},tr('Mode d’edició: toca una frase o una carpeta per canviar-la, moure-la o eliminar-la. Prem «Acabar edició» per tornar a fer-les servir.','Modo de edición: toca una frase o una carpeta para cambiarla, moverla o eliminarla. Pulsa «Terminar edición» para volver a usarlas.')));if(activeView==='phrases'&&phraseFolder)n.append(folderBar());")
# Clearer edit button
rep("controls.append(button(editingList?tr('Acabar edició','Terminar edición'):tr('Editar','Editar'),()=>{editingList=!editingList;renderWorkspace();},editingList?'soft':'')",
    "controls.append(button(editingList?tr('Acabar edició','Terminar edición'):innerWidth<=600?tr('Editar','Editar'):activeView==='phrases'?tr('Editar frases i carpetes','Editar frases y carpetas'):tr('Editar frases','Editar frases'),()=>{editingList=!editingList;renderWorkspace();},editingList?'primary':'',editingList?'check':'edit')")

# Panel size buttons
rep("$('workspace-header').hidden=!panelOpen;",
    "$('workspace-header').hidden=!panelOpen;"
    "{let z=$('panel-zoom');if(!z){z=el('div',{id:'panel-zoom',class:'panel-zoom',role:'group','data-scan-group':'panel-zoom'});$('toggle-panel').before(z);}"
    "z.setAttribute('aria-label',tr('Mida dels elements del panell','Tamaño de los elementos del panel'));clear(z);const now=Math.round((prefs().panelScale||1)*10)/10;"
    "const mk=(d,label,text,key)=>{const b=button(text,()=>{const v=Math.round(Math.min(1.6,Math.max(0.7,(prefs().panelScale||1)+d))*10)/10;if(v===prefs().panelScale)return;prefs().panelScale=v;persist();applyAppearance();renderWorkspace();notify(tr('Mida del panell: ','Tamaño del panel: ')+Math.round(v*100)+' %');},'soft panel-zoom-btn');b.setAttribute('aria-label',label);b.title=label;b.dataset.focusKey=key;return b;};"
    "const minus=mk(-0.1,tr('Elements del panell més petits','Elementos del panel más pequeños'),'A−','panel-smaller'),plus=mk(0.1,tr('Elements del panell més grans','Elementos del panel más grandes'),'A+','panel-bigger');"
    "minus.setAttribute('aria-disabled',String(now<=0.7));plus.setAttribute('aria-disabled',String(now>=1.6));z.append(minus,plus);}")

# Same edit pattern in every tab: pencil + "Editar <what>" and the edit-mode notice (Marc, 2026-11-08)
rep(":innerWidth<=600?tr('Editar','Editar'):activeView==='phrases'?tr('Editar frases i carpetes','Editar frases y carpetas'):tr('Editar frases','Editar frases')",
    ":innerWidth<=600?tr('Editar','Editar'):activeView==='favorites'?tr('Editar favorits','Editar favoritos'):query.trim()?tr('Editar frases','Editar frases'):!phraseFolder?tr('Editar carpetes','Editar carpetas'):profile().categories.some(c=>c.parent===phraseFolder)?tr('Editar frases i carpetes','Editar frases y carpetas'):tr('Editar frases','Editar frases')")
rep("button(tr('Personalitzar','Personalizar'),manageQuick,'flat')","button(innerWidth<=600?tr('Editar','Editar'):tr('Editar respostes','Editar respuestas'),manageQuick,'','edit')")
s=s.replace("tr('Mode d’edició: toca una frase o una carpeta per canviar-la, moure-la o eliminar-la. Prem «Acabar edició» per tornar a fer-les servir.','Modo de edición: toca una frase o una carpeta para cambiarla, moverla o eliminarla. Pulsa «Terminar edición» para volver a usarlas.')",
            "tr('Mode d’edició: toca un element per canviar-lo, moure’l o eliminar-lo. Prem «Acabar edició» per tornar a fer-los servir.','Modo de edición: toca un elemento para cambiarlo, moverlo o eliminarlo. Pulsa «Terminar edición» para volver a usarlos.')")

CSS="""
/* 0.6.10: panel size buttons and Up button in the toolbar row */
.panel-zoom{display:flex;gap:6px;margin-left:auto;margin-right:8px;flex-shrink:0}
.panel-zoom-btn{min-width:44px;font-weight:700;font-size:15px;padding:5px 10px}
.panel-zoom-btn[aria-disabled=true]{opacity:.45}
#workspace-body{zoom:var(--panel-scale,1)}
.library-controls .folder-up{flex:0 0 auto}\n@media(max-width:480px){#workspace-tabs button>span{position:absolute;width:1px;height:1px;overflow:hidden;clip-path:inset(50%);white-space:nowrap}#workspace-tabs button{min-width:0;flex:1}}\n@media(max-width:600px){.folder-bar>button:last-child>span{position:absolute;width:1px;height:1px;overflow:hidden;clip-path:inset(50%)}}\n.edit-notice{flex-shrink:0;margin:0;padding:6px 10px;font-size:13px}
@media(max-width:600px){.library-controls input[type=search]{order:-1}.panel-zoom{margin-right:4px;gap:4px}.panel-zoom-btn{min-width:36px;padding:4px 6px;font-size:13px}}
"""
i=s.rindex('</style>'); s=s[:i]+CSS+s[i:]

T={
"Editar frases i carpetes":["Editatu esaldiak eta karpetak","Editar frases e cartafoles","Edit phrases and folders","Modifier les phrases et les dossiers"],
"Editar frases":["Editatu esaldiak","Editar frases","Edit phrases","Modifier les phrases"],
"Mode d’edició: toca un element per canviar-lo, moure’l o eliminar-lo. Prem «Acabar edició» per tornar a fer-los servir.":["Edizio modua: ukitu elementu bat aldatzeko, mugitzeko edo ezabatzeko. Sakatu «Amaitu edizioa» berriro erabiltzeko.","Modo de edición: toca un elemento para cambialo, movelo ou eliminalo. Preme «Rematar edición» para volver usalos.","Edit mode: tap an item to change, move or delete it. Press “Finish editing” to use them again.","Mode modification : touchez un élément pour le modifier, le déplacer ou le supprimer. Appuyez sur « Terminer la modification » pour les utiliser à nouveau."],
"Editar favorits":["Editatu gogokoak","Editar favoritos","Edit favourites","Modifier les favoris"],
"Editar carpetes":["Editatu karpetak","Editar cartafoles","Edit folders","Modifier les dossiers"],
"Editar respostes":["Editatu erantzunak","Editar respostas","Edit replies","Modifier les réponses"],
"Mida dels elements del panell":["Paneleko elementuen tamaina","Tamaño dos elementos do panel","Size of the panel items","Taille des éléments du panneau"],
"Mida del panell: ":["Panelaren tamaina: ","Tamaño do panel: ","Panel size: ","Taille du panneau : "],
"Elements del panell més petits":["Paneleko elementu txikiagoak","Elementos do panel máis pequenos","Smaller panel items","Éléments du panneau plus petits"],
"Elements del panell més grans":["Paneleko elementu handiagoak","Elementos do panel máis grandes","Larger panel items","Éléments du panneau plus grands"],
}
i=s.index('const KeryxI18n=(()=>{const dictionaries=')+len('const KeryxI18n=(()=>{const dictionaries=')
for li,lang in enumerate(['eu','gl','en','fr']):
    key='"'+lang+'":{'; k=s.index(key,i)+len(key)
    s=s[:k]+''.join(json.dumps(ca,ensure_ascii=False)+':'+json.dumps(v[li],ensure_ascii=False)+',' for ca,v in T.items())+s[k:]
open(dst,'w',encoding='utf-8',newline='').write(s)
print('ok',dst)
